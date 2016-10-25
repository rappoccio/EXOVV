#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = 'responses_rejec_otherway_qcdmc_2dplots.root',
                  help='String to append to MC names')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")

f = ROOT.TFile(options.infile)

histstrs = [
    #'h2_mreco_mgen',
    #'h2_mreco_mgen_softdrop',
    #'h2_ptreco_ptgen',
    'h2_ptreco_ptgen_softdrop',
    ]
hists = []
canvs = []
fits = []
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kGreyScale)

for ihist in xrange( len(histstrs) ):

    hists.append( f.Get(histstrs[ihist]) )



    
    for ibin in xrange( 1, hists[ihist].GetNbinsX()) :
        yscale = 0.
        c1 = ROOT.TCanvas("c1" + str(ihist) + str(ibin), "c1" + str(ihist) + str(ibin) )
        for jbin in xrange( 1, hists[ihist].GetNbinsY() ) :
            yscale += hists[ihist].GetBinContent( ibin, jbin )
        if abs(yscale) < 1e-12 :
            continue
        for jbin in xrange( 1, hists[ihist].GetNbinsY() ) :
            val = hists[ihist].GetBinContent( ibin, jbin )
            hists[ihist].SetBinContent( ibin, jbin, val/yscale )
            hists[ihist].SetBinError( ibin, jbin, hists[ihist].GetBinContent(ibin)/yscale )
        histproj = hists[ihist].ProjectionY( hists[ihist].GetName() + str(ibin) )
        histproj.Rebin(10)
        histproj.Sumw2()
        histproj.Scale(1.0/histproj.Integral())
        if histstrs[ihist] == "h2_mreco_mgen" : 
            f1  = ROOT.TF1("f1" + str(ibin),"landau", histproj.GetMean() - 1.5*histproj.GetRMS(), histproj.GetMean() + 1.5*histproj.GetRMS())
            histproj.Fit("f1" + str(ibin), "LRM")
        elif histstrs[ihist] == "h2_mreco_mgen_softdrop" :
            f1  = ROOT.TF1("f2" + str(ibin),"landau", histproj.GetMean() - 1.5*histproj.GetRMS(), histproj.GetMean() + 1.5*histproj.GetRMS())
            histproj.Fit("f2" + str(ibin), "LRM")
        elif histstrs[ihist] == "h2_ptreco_ptgen" :
            f1  = ROOT.TF1("f3" + str(ibin),"gaus", histproj.GetMean() - 1.5*histproj.GetRMS(), histproj.GetMean() + 1.5*histproj.GetRMS())
            histproj.Fit("f3" + str(ibin), "LRM")
        elif histstrs[ihist] == "h2_ptreco_ptgen_softdrop" :
            f1  = ROOT.TF1("f4" + str(ibin),"gaus", histproj.GetMean() - 1.5*histproj.GetRMS(), histproj.GetMean() + 1.5*histproj.GetRMS())
            histproj.Fit("f4" + str(ibin), "LRM")
        #f1  = ROOT.TF1("f" + str(ibin),"ROOT::Math::crystalball_function(x, [0], [1], [2], [3])",0,2)
        #f1.SetParameters(1, 1, 1, 1)
        
        fits.append(f1)
        hists.append(histproj)
        canvs.append(c1)


    c = ROOT.TCanvas("c" + str(ihist), "c" + str(ihist), 600, 800)

    c.cd()
    hists[ihist].GetXaxis().SetRangeUser(0, 1300)
    hists[ihist].Draw("colz")
    canvs.append(c)
    
