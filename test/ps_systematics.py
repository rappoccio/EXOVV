from optparse import OptionParser
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, TFile, TH2
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TGraphErrors
from math import sqrt
from array import array
parser = OptionParser()
parser.add_option('--softdrop', action='store_true',
                dest='softdrop',
                default=False,
                help='do softdrop variation')
(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math
import random


ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")


psunfolded = TFile('PS_hists.root')
central = TFile('2DClosure.root')

h_herwig = psunfolded.Get('pyth8_uherwig')
h_herwig.Scale(1./h_herwig.Integral())
h_pythia8 = central.Get('pyth8_spanmass')
h_pythia8.Scale(1./h_pythia8.Integral())

h_herwigsd = psunfolded.Get('pyth8_uherwig_softdrop')
h_herwigsd.Scale(1./h_herwigsd.Integral())
h_pythia8sd = central.Get('pyth8_spanmassSD')
h_pythia8sd.Scale(1./h_pythia8sd.Integral())

h_herwig.Divide(h_pythia8)
h_herwigsd.Divide(h_pythia8sd)

if options.softdrop:
    h = h_herwigsd
    h8 = h_pythia8sd
else:
    h = h_herwig
    h8 = h_pythia8

reachedSmooth = False
for ibin in xrange(0,h.GetNbinsX()+1):
    #print ibin
    val = float(h.GetBinContent(ibin))
    #print val
    err = float(abs((h.GetBinContent(ibin)-h8.GetBinContent(ibin))))
    #print err
    if val != 0.0 :
        reachedSmoothUP = True
    else:
        reachedSmoothUP = False
    if reachedSmoothUP and err/val > 1.0 :
        h.SetBinContent(ibin, 0.)
        h.SetBinError( ibin, 0.)

c = ROOT.TCanvas("c", "c")
h.SetLineStyle(2)

h.Draw("hist")
if options.softdrop:
    title = 'Soft Drop Parton Shower'
else:
    title = 'Ungroomed Partion Shower'

h.GetYaxis().SetTitle(title + " Variation")
h.GetYaxis().SetTitleSize(15)
h.GetYaxis().SetLabelSize(15)
h.SetTitle(title + " Variation Unfolded")
h.GetXaxis().SetTitle("Jet Mass (GeV)")

h.SetMinimum(0.0)
h.SetMaximum(2.0)
if options.softdrop:
    c.SaveAs("PSUnfoldedSD.png")
else:
    c.SaveAs("PSUnfolded.png")
c.Update()



