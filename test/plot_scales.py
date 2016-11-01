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
    'h2_mreco_mgen_softdrop',
    #'h2_ptreco_ptgen',
    #'h2_ptreco_ptgen_softdrop',
    ]
hists = []
canvs = []
fits = []
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kGreyScale)

for ihist in xrange( len(histstrs) ):

    htemp = f.Get(histstrs[ihist])



    
    for ibin in xrange( 1, htemp.GetNbinsX()) :
        yscale = 0.
        c1 = ROOT.TCanvas("c1" + str(ihist) + str(ibin), "c1" + str(ihist) + str(ibin) )
        for jbin in xrange( 1, htemp.GetNbinsY() ) :
            yscale += htemp.GetBinContent( ibin, jbin )
        if abs(yscale) < 1e-12 :
            continue
        for jbin in xrange( 1, htemp.GetNbinsY() ) :
            val = htemp.GetBinContent( ibin, jbin )
            htemp.SetBinContent( ibin, jbin, val/yscale )
            htemp.SetBinError( ibin, jbin, htemp.GetBinContent(ibin)/yscale )
        histproj = htemp.ProjectionY( htemp.GetName() + str(ibin) )
        histproj.Rebin(10)
        histproj.Sumw2()
        histproj.Scale(1.0/histproj.Integral())
        f1  = ROOT.TF1("f1" + str(ibin),"gaus", 0.9, 1.1)
        histproj.Fit("f1" + str(ibin), "LRM")
        #f1  = ROOT.TF1("f" + str(ibin),"ROOT::Math::crystalball_function(x, [0], [1], [2], [3])",0,2)
        #f1.SetParameters(1, 1, 1, 1)
        
        fits.append(f1)
        hists.append(histproj)
        canvs.append(c1)


    c = ROOT.TCanvas("c" + str(ihist), "c" + str(ihist), 600, 800)

    c.cd()
    canvs.append(c)
    
