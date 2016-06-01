#! /usr/bin/env python

##################
# Get purity and stability plots for 2d responses
##################

import sys


from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'qcd_76x_qcdmc.root',
                  help='Input file')

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = '2d_response_softdrop',
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

# Purity
for ireco in xrange(0, h2.GetNbinsX()):
    diag = 0
    tot = 0
    for igen in xrange(0, h2.GetNbinsX()):
        if ireco == igen :
            diag += h2.GetBinContent(ireco+1, igen+1)
        tot += h2.GetBinContent(ireco+1, igen+1)
    if tot > 0.0001:
        frac = diag/tot
    else :
        frac = 0
    purity.SetBinContent(ireco+1, frac )

# Stability
for igen in xrange(0, h2.GetNbinsX()):
    diag = 0
    tot = 0
    for ireco in xrange(0, h2.GetNbinsX()):
        if igen == ireco :
            diag += h2.GetBinContent(ireco+1, igen+1)
        tot += h2.GetBinContent(ireco+1,igen+1)
    if tot > 0.0001:
        frac = diag/tot
    else :
        frac = 0
    stability.SetBinContent(igen+1, frac )


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
leg.Draw()
c1.Update()
outstr = "ungroomed"
c1.Print("purity_stability_" + options.hist + ".pdf", "pdf")
c1.Print("purity_stability_" + options.hist + ".png", "png")
