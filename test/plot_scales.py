#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = 'responses_rejec_tightgen_otherway_qcdmc_2dplots.root',
                  help='String to append to MC names')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")

f = ROOT.TFile(options.infile)

ptbinstrs = ['#bf{200 < p_{T} < 260 GeV}','#bf{260 < p_{T} < 350 GeV}','#bf{350 < p_{T} < 460 GeV}','#bf{460 < p_{T} < 550 GeV}','#bf{550 < p_{T} < 650 GeV}','#bf{650 < p_{T} < 760 GeV}', '#bf{760 < p_{T} < 900 GeV}', '#bf{900 < p_{T} < 1000 GeV}', '#bf{1000 < p_{T} < 1100 GeV}','#bf{1100 < p_{T} < 1200 GeV}',
    '#bf{1200 < p_{T} < 1300 GeV}', '#bf{p_{T} > 1300 GeV}']

histstrs = [
    'h2_mreco_mgen',
    'h2_mreco_mgen_softdrop_nomnom',
    #'h2_ptreco_ptgen',
    #'h2_ptreco_ptgen_softdrop',
    ]
hists = []
canvs = []
fits = []
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kGreyScale)

prelim = ROOT.TLatex()
prelim.SetNDC()
prelim.SetTextFont(43)
prelim.SetTextSize(30)

tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(25)

for ihist in xrange( len(histstrs) ):

    htemp = f.Get(histstrs[ihist])



    
    for ibin in xrange( 1, htemp.GetNbinsX()) :
        yscale = 0.
        c1 = ROOT.TCanvas("c1" + str(ihist) + '_' + str(ibin), "c1" + str(ihist) + '_' + str(ibin), 800, 600 )
        c1.SetBottomMargin(0.15)
        c1.SetLeftMargin(0.15)
        c1.SetRightMargin(0.15)
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
        prelim.DrawLatex(0.2, 0.926, "CMS Preliminary")
        prelim.DrawLatex(0.6, 0.926, "2.3 fb^{-1} (13 TeV)")

        
        tlx.DrawLatex( 0.2, 0.8, ptbinstrs[ibin - 1] )
        if 'softdrop' in histstrs[ihist] :
            histproj.SetTitle(  ';Groomed m_{reco}/m_{gen};Fraction'  )
        else :
            histproj.SetTitle(  ';Ungroomed m_{reco}/m_{gen};Fraction'  )


        c1.Update()
        histproj.GetXaxis().SetTitleOffset(1.0)
        histproj.GetYaxis().SetTitleOffset(1.0)
        stats = histproj.FindObject("stats")
        stats.SetX1NDC( 0.59 )
        stats.SetX2NDC( 0.85 )
        stats.SetY1NDC( 0.59 )
        stats.SetY2NDC( 0.85 )
        fits.append(f1)
        hists.append(histproj)
        canvs.append(c1)
        c1.Print('jetmass_fits_' + str(ihist) + '_' + str(ibin) + '.png', 'png')
        c1.Print('jetmass_fits_' + str(ihist) + '_' + str(ibin) + '.pdf', 'pdf')


    c = ROOT.TCanvas("c" + str(ihist), "c" + str(ihist), 600, 800)

    c.cd()
    canvs.append(c)
    
