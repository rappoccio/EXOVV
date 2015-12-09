#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = "/data/EXOVV/QCDTree/JetHT_Run2015D_B2GAnaFW_v74x_V8p4_25ns_Nov13silverJSON.root",
                  help='Input file')

(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math


f = ROOT.TFile(options.infile)

t = f.Get("TreeEXOVV")

cut1 = ("((Trig % 1000000) / 100000 == 1)")
cut2 = ("((Trig % 100000) / 10000 == 1) && !" + cut1)
cut3 = ("((Trig % 10000) / 1000 == 1) && !" + cut2)
cut4 = ("((Trig % 1000) / 100 == 1) && !" + cut3)
cut5 = ("((Trig % 100) / 10 == 1) && !" + cut4)
cut6 = ("((Trig % 10) / 1 == 1) && !" + cut5)


t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h1(500,0,1000)", cut1, "goff")
t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h2(500,0,1000)", cut2, "goff")
t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h3(500,0,1000)", cut3, "goff")
t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h4(500,0,1000)", cut4, "goff")
t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h5(500,0,1000)", cut5, "goff")
t.Draw("(FatJetPt[0] + FatJetPt[1]) * 0.5 >> h6(500,0,1000)", cut6, "goff")

h1 = ROOT.gDirectory.Get("h1")
h2 = ROOT.gDirectory.Get("h2")
h3 = ROOT.gDirectory.Get("h3")
h4 = ROOT.gDirectory.Get("h4")
h5 = ROOT.gDirectory.Get("h5")
h6 = ROOT.gDirectory.Get("h6")

ratios = []

hists = [h1,h2,h3,h4,h5]
colors =[ 1, 2, 3, 4, 6]
labels = [
    'HLT_PFHT800',
    'HLT_PFHT650',
    'HLT_PFHT600',
    'HLT_PFHT475',
    'HLT_PFHT400',
    'HLT_PFHT350'
    ]

prescales = [
    1.0,      #HT800
    1.16,#4.0096,   #HT650
    26,#4.5523,   #HT600
    26,#10.5700,  #HT475
    26,#11.5029,  #HT400
    26,#11.8516,  #HT350
    ]

hstack = ROOT.THStack("hstack", ';Jet p_{T};Number observed #times Prescale')
rstack = ROOT.THStack("rstack", ';Jet p_{T};Ratio')
leg = ROOT.TLegend(0.6, 0.6, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
for ihist,hist in enumerate( hists ) :
    hist.Scale( prescales[ihist] )
    hist.SetLineColor(colors[ihist])
    hstack.Add(hist)
    leg.AddEntry( hist, labels[ihist], 'l')
    if ihist != 0 :
        ratio = hist.Clone()
        ratio.Sumw2()
        ratio.SetMarkerColor( ratio.GetLineColor() )
        ratio.SetName( "ratio" + str(ihist))
        ratio.Divide( h1 )
        ratios.append(ratio)
        rstack.Add(ratio)
        
effs = []
leg2 = ROOT.TLegend(0.6, 0.2, 0.84, 0.4)
leg2.SetFillColor(0)
leg2.SetBorderSize(0)
effstack = ROOT.THStack("effstack", ";Jet p_{T};N(path x) / N(path x-1)")
for ihist in xrange(0, len(hists) - 1) :
    eff = hists[ihist].Clone()
    eff.SetName("eff" + str(ihist) )
    eff.Divide( hists[ihist + 1] )
    effs.append(effs)
    effstack.Add( eff )
    leg2.AddEntry( eff, labels[ihist], 'l')


c1 = ROOT.TCanvas("c1", "c1")
hstack.Draw("nostack")
hstack.SetMinimum(50)
leg.Draw()
c1.SetLogy()
c1.Print("prescaled_jet_data.png", "png")
c1.Print("prescaled_jet_data.pdf", "pdf")

c2 = ROOT.TCanvas("c2", "c2")
fits = [
    ROOT.TF1("fit2", "pol1", 400,1000),
    ROOT.TF1("fit3", "pol1", 400,1000),
    ROOT.TF1("fit4", "pol1", 400,1000),
    ROOT.TF1("fit5", "pol1", 400,1000),
    ROOT.TF1("fit6", "pol1", 400,1000),
    ROOT.TF1("fit7", "pol1", 400,1000),
    ]

for iratio,ratio in enumerate(ratios) :
    ratio.Fit( fits[iratio], 'LRM', "goff")
    fits[iratio].SetLineColor( ratio.GetLineColor() )
    
rstack.Draw("nostack")
for ifit,fit in enumerate( fits ) :
    fit.Draw("same")
    print "%6d : %6.4f" % (ifit, fit.Eval(500))
rstack.GetXaxis().SetRangeUser(400, 1000)
rstack.SetMinimum(500)
rstack.SetMaximum(1.2)
c2.Update()
c2.Print("prescaled_jet_data_findprescale.png", "png")
c2.Print("prescaled_jet_data_findprescale.pdf", "pdf")

c3 = ROOT.TCanvas("c3", "c3")
effstack.Draw("nostack")
effstack.GetXaxis().SetRangeUser(170,500)
effstack.SetMaximum(1.2)
leg2.Draw()
c3.Update()
c3.Print("prescaled_jet_data_findthreshold.png", "png")
c3.Print("prescaled_jet_data_findthreshold.pdf", "pdf")

