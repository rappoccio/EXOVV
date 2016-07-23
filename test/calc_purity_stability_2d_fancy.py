#! /usr/bin/env python

##################
# Get purity and stability plots for 2d responses
##################

import sys
import math

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'responses_otherway_qcdmc.root',
                  help='Input file')

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = '2d_response',
                  help='Response matrix')

(options, args) = parser.parse_args()
argv = []

import ROOT

ROOT.gSystem.Load("RooUnfold/libRooUnfold.so")
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)

f = ROOT.TFile(options.file)
r = f.Get(options.hist)
h2 = r.Hresponse()

title = 'Ungroomed'
if "softdrop" in options.hist :
    title = "Soft drop"
# Make the histograms
purity = ROOT.TH1F("purity", title + ";Bin;Fraction", h2.GetNbinsX(), 0, h2.GetNbinsX())
stability = ROOT.TH1F("stability", title + ";Fraction;Bin", h2.GetNbinsX(), 0, h2.GetNbinsX())

purity.GetYaxis().SetTitleOffset(0.8)

stability.SetLineColor(2)


ptbins =[  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
mbins = [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]



for irecopt in xrange( len(ptbins) ):
    for irecom in xrange( len(mbins) ):
        diag = 0
        tot = 0
        recopt = ptbins[irecopt]
        recom = mbins[irecom]
        recobin = irecom + len(ptbins) * irecopt
        for igenpt in xrange( len(ptbins) ):
            for igenm in xrange( len(mbins) ):
                genpt = ptbins[igenpt]
                genm = mbins[igenm]                
                genbin = igenm + len(ptbins) * igenpt
                if genm < genpt * 0.8 / math.sqrt(2.0) and recom < recopt * 0.8 / math.sqrt(2.0) :
                    if genbin == recobin :
                        diag += h2.GetBinContent(recobin, genbin)                
                    tot += h2.GetBinContent(recobin, genbin)
        if tot > 0.0001 :
            frac = diag / tot
        else :
            frac = 0
        purity.SetBinContent( recobin + 1, frac )
        

# Stability
for igenpt in xrange( len(ptbins) ):
    for igenm in xrange( len(mbins) ):
        diag = 0
        tot = 0
        genpt = ptbins[igenpt]
        genm = mbins[igenm]
        genbin = igenm + len(ptbins) * igenpt
        for irecopt in xrange( len(ptbins) ):
            for irecom in xrange( len(mbins) ):
                recopt = ptbins[irecopt]
                recom = mbins[irecom]                
                recobin = irecom + len(ptbins) * irecopt
                if recom < recopt * 0.8 / math.sqrt(2.0) and genm < genpt * 0.8 / math.sqrt(2.0) :
                    if recobin == genbin :
                        diag += h2.GetBinContent(recobin, genbin)                
                    tot += h2.GetBinContent(recobin, genbin)
        if tot > 0.0001 :
            frac = diag / tot
        else :
            frac = 0
        stability.SetBinContent( genbin + 1, frac )

print 'Purity: ', purity.Integral()
print 'Stability: ', stability.Integral()

c0 = ROOT.TCanvas("c0", "response")
h2.SetTitle(title + ';Reconstructed bin;Generated bin')
h2.Draw("colz")
c0.Update()
c0.Print("response_" + options.hist + ".pdf", "pdf")
c0.Print("response_" + options.hist + ".png", "png")

c1 = ROOT.TCanvas("c1", "xpurity")
leg = ROOT.TLegend(0.7, 0.7, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.AddEntry( purity, 'Purity', 'l')
leg.AddEntry( stability, 'Stability', 'l')
purity.Draw()
stability.Draw("same")
purity.SetMaximum(1.0)
purity.GetXaxis().SetRangeUser(0,400)
leg.Draw()
c1.Update()
outstr = "ungroomed"
c1.Print("purity_stability_" + options.hist + ".pdf", "pdf")
c1.Print("purity_stability_" + options.hist + ".png", "png")
