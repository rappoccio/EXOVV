#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--fileLo', type='string', action='store',
                  dest='fileLo',
                  default = 'QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut6_fullstat.root',
                  help='Input files for Low Pt')


parser.add_option('--fileLoMod', type='string', action='store',
                  dest='fileLoMod',
                  default = 'QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut7_fullstat.root',
                  help='Input files for Low Pt with Modified Tau')

parser.add_option('--fileHi', type='string', action='store',
                  dest='fileHi',
                  default = 'QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_pthi_taucut6_fullstats.root',
                  help='Input files for High Pt')


parser.add_option('--selection', type='string', action='store',
                  dest='selection',
                  help='Selection : 0 (ZV), 1 (WV), 2 (VV)')

parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "",
                  help='Output string for output file')

parser.add_option('--simulation', action='store_true',
                  dest='simulation',
                  default = None,
                  help='Is this simulation?')

parser.add_option('--lumi', type='float', action='store',
                  dest='lumi',
                  default = 1263,
                  help='Is this simulation?')

(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)

tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(42)
tlx.SetTextSize(0.057)
tlxmini = ROOT.TLatex()
tlxmini.SetNDC()
tlxmini.SetTextFont(42)
tlxmini.SetTextSize(0.037)

fLo = ROOT.TFile(options.fileLo)
fLoMod = ROOT.TFile(options.fileLoMod)
fHi = ROOT.TFile(options.fileHi)

hLo = fLo.Get("h" + str(options.selection) + "_jetrho_vs_tau21AK8").Clone()
hLo.SetName("hLo")
hLoMod = fLoMod.Get("h" + str(options.selection) + "_jetrho_vs_tau21AK8").Clone()
hLoMod.SetName("hLoMod")
hHi = fHi.Get("h" + str(options.selection) + "_jetrho_vs_tau21AK8").Clone()
hHi.SetName("hHi")

hLo.UseCurrentStyle()
hLoMod.UseCurrentStyle()
hHi.UseCurrentStyle()

hLo.Sumw2()
hLoMod.Sumw2()
hHi.Sumw2()

hLo.Scale(1.0 / hLo.Integral() )
hLoMod.Scale(1.0 / hLoMod.Integral() )
hHi.Scale(1.0 / hHi.Integral() )

cLo = ROOT.TCanvas("cLo", "cLo")
#cLo.SetTopMargin(0.18)
cLo.SetRightMargin(0.15)
hLo.GetYaxis().SetTitleOffset(1.0)
cLo.SetLogx()
cLo.SetLogz()
hLo.SetTitle("")
hLo.Draw("colz")
hLo.SetMaximum(0.2)
hLo.SetMinimum(1e-5)

profLo = hLo.ProfileX()
profLo.SetMarkerStyle(20)
profLo.Draw("same")

if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
    
tlxmini.DrawLatex(0.66, 0.86,  "200 < p_{T} < 350 GeV")
tlxmini.DrawLatex(0.66, 0.81, "m > 50 GeV")
tlxmini.DrawLatex(0.66, 0.76, "#tau_{21} < 0.6")
cLo.Update()

cLo.Print("tau_vs_rho_ptlo_taucut6" + options.outname + ".pdf", "pdf")
cLo.Print("tau_vs_rho_ptlo_taucut6" + options.outname + ".png", "png")

cLoMod = ROOT.TCanvas("cLoMod", "cLoMod")
#cLoMod.SetTopMargin(0.18)
cLoMod.SetRightMargin(0.15)
hLoMod.GetYaxis().SetTitleOffset(1.0)
cLoMod.SetLogx()
cLoMod.SetLogz()
hLoMod.SetTitle("")
hLoMod.Draw("colz")
hLoMod.SetMaximum(0.2)
hLoMod.SetMinimum(1e-5)

profLoMod = hLoMod.ProfileX()
profLoMod.SetMarkerStyle(20)
profLoMod.Draw("same")
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlxmini.DrawLatex(0.66, 0.86,  "200 < p_{T} < 350 GeV")
tlxmini.DrawLatex(0.66, 0.81, "m > 28.7 GeV")
tlxmini.DrawLatex(0.66, 0.76, "#tau_{21} < 0.65")
cLoMod.Update()

cLoMod.Print("tau_vs_rho_ptlo_taucut7" + options.outname + ".pdf", "pdf")
cLoMod.Print("tau_vs_rho_ptlo_taucut7" + options.outname + ".png", "png")

cHi = ROOT.TCanvas("cHi", "cHi")
#cHi.SetTopMargin(0.18)
cHi.SetRightMargin(0.15)
hHi.GetYaxis().SetTitleOffset(1.0)
cHi.SetLogx()
cHi.SetLogz()
hHi.SetTitle("")
hHi.Draw("colz")
hHi.SetMaximum(0.2)
hHi.SetMinimum(1e-5)

profHi = hHi.ProfileX()
profHi.SetMarkerStyle(20)
profHi.Draw("same")
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlxmini.DrawLatex(0.66, 0.86,  "p_{T} > 350 GeV")
tlxmini.DrawLatex(0.66, 0.81, "m > 50 GeV")
tlxmini.DrawLatex(0.66, 0.76, "#tau_{21} < 0.6")
cHi.Update()

cHi.Print("tau_vs_rho_pthi_taucut6" + options.outname + ".pdf", "pdf")
cHi.Print("tau_vs_rho_pthi_taucut6" + options.outname + ".png", "png")


c1Lo = ROOT.TCanvas("c1Lo", "c1Lo")
h1Lo_All = fLo.Get("h" + str(options.selection) + "_rho_all").Clone()
h1Lo_All.SetName("h1Lo_All")
h1Lo_Sel = fLo.Get("h" + str(options.selection) + "_rho_tau21cut").Clone()
h1Lo_Sel.SetName("h1Lo_Sel")

h1Lo_All.Sumw2()
h1Lo_Sel.Sumw2()

nAll_Lo = h1Lo_All.Integral()
h1Lo_All.Scale( 1.0 / nAll_Lo )
h1Lo_Sel.Scale( 1.0 / nAll_Lo )


h1Lo_All.SetMarkerStyle(20)
h1Lo_Sel.SetMarkerStyle(24)


tlxmini.DrawLatex(0.6, 0.905, "200 < p_{T} < 350 GeV, #tau_{21} < 0.6")
h1Lo_All.SetTitle(";Jet #rho;Fraction")
h1Lo_All.GetYaxis().SetTitleOffset(1.0)

c1Lo.SetLogx()
c1Lo.SetLogy()
h1Lo_All.Draw()
h1Lo_Sel.Draw("same")
h1Lo_All.SetMaximum(0.2)
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlxmini.DrawLatex(0.6, 0.905, "200 < p_{T} < 350 GeV, #tau_{21} < 0.6")
c1Lo.Update()

c1Lo.Print("shape_ptlo_taucut6" + options.outname + ".pdf", "pdf")
c1Lo.Print("shape_ptlo_taucut6" + options.outname + ".png", "png")



c1LoMod = ROOT.TCanvas("c1LoMod", "c1LoMod")
h1LoMod_All = fLoMod.Get("h" + str(options.selection) + "_rho_all").Clone()
h1LoMod_All.SetName("h1LoMod_All")
h1LoMod_Sel = fLoMod.Get("h" + str(options.selection) + "_rho_tau21cut").Clone()
h1LoMod_Sel.SetName("h1LoMod_Sel")

h1LoMod_All.Sumw2()
h1LoMod_Sel.Sumw2()

nAll_LoMod = h1LoMod_All.Integral()
h1LoMod_All.Scale( 1.0 / nAll_LoMod )
h1LoMod_Sel.Scale( 1.0 / nAll_LoMod )


h1LoMod_All.SetMarkerStyle(22)
h1LoMod_Sel.SetMarkerStyle(26)
tlxmini.DrawLatex(0.6, 0.905, "200 < p_{T} < 350 GeV, #tau_{21} < 0.65")
h1LoMod_All.SetTitle(";Jet #rho;Fraction")
h1LoMod_All.GetYaxis().SetTitleOffset(1.0)

c1LoMod.SetLogx()
c1LoMod.SetLogy()
h1LoMod_All.Draw()
h1LoMod_Sel.Draw("same")
h1LoMod_All.SetMaximum(0.2)
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlxmini.DrawLatex(0.6, 0.905, "200 < p_{T} < 350 GeV, #tau_{21} < 0.65")
c1LoMod.Update()

c1LoMod.Print("shape_ptlo_taucut7" + options.outname + ".pdf", "pdf")
c1LoMod.Print("shape_ptlo_taucut7" + options.outname + ".png", "png")

c1Hi = ROOT.TCanvas("c1Hi", "c1Hi")
h1Hi_All = fHi.Get("h" + str(options.selection) + "_rho_all").Clone()
h1Hi_All.SetName("h1Hi_All")
h1Hi_Sel = fHi.Get("h" + str(options.selection) + "_rho_tau21cut").Clone()
h1Hi_Sel.SetName("h1Hi_Sel")

h1Hi_All.Sumw2()
h1Hi_Sel.Sumw2()

nAll_Hi = h1Hi_All.Integral()
h1Hi_All.Scale( 1.0 / nAll_Hi )
h1Hi_Sel.Scale( 1.0 / nAll_Hi )

h1Hi_All.SetMarkerStyle(21)
h1Hi_Sel.SetMarkerStyle(25)

h1Hi_All.SetTitle(";Jet #rho;Fraction")
h1Hi_All.GetYaxis().SetTitleOffset(1.0)

c1Hi.SetLogx()
c1Hi.SetLogy()
h1Hi_All.Draw()
h1Hi_Sel.Draw("same")
h1Hi_All.SetMaximum(0.2)
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlxmini.DrawLatex(0.6, 0.905, "p_{T} > 350 GeV, #tau_{21} < 0.6")
c1Hi.Update()

c1Hi.Print("shape_pthi_taucut6" + options.outname + ".pdf", "pdf")
c1Hi.Print("shape_pthi_taucut6" + options.outname + ".png", "png")

cRate = ROOT.TCanvas("cRate", "cRate")
rHi = h1Hi_Sel.Clone()
rHi.SetName("rHi")
rHi.Divide( rHi, h1Hi_All, 1.0, 1.0, "b")
rLo = h1Lo_Sel.Clone()
rLo.SetName("rLo")
rLo.Divide( rLo, h1Lo_All, 1.0, 1.0, "b")
rLoMod = h1LoMod_Sel.Clone()
rLoMod.SetName("rLoMod")
rLoMod.Divide( rLoMod, h1LoMod_All, 1.0, 1.0, "b")

for ibin in xrange(0, rLoMod.GetXaxis().GetNbins() ) :
    rVal = rLoMod.GetBinContent(ibin)
    if rVal < 0.00001 :
        rLoMod.SetBinContent(ibin, 0.0)
        rLoMod.SetBinError( ibin, 0.0)
        continue
    rHiVal = rHi.GetBinContent(ibin)
    diff = abs( rVal - rHiVal )
    err = rLoMod.GetBinError(ibin)
    err = math.sqrt( err*err+ 0.03*0.03*rVal*rVal)
    #err = math.sqrt( err*err + diff*diff )
    rLoMod.SetBinError( ibin, err)

rHi.SetMarkerStyle(20)
rLo.SetMarkerStyle(21)
rLoMod.SetMarkerStyle(25)
rHi.SetMarkerColor(1)
rLo.SetMarkerColor(2)
rLoMod.SetMarkerColor(2)
rLoMod.SetFillColor(2)
rLoMod.SetFillStyle(3003)


rHi.Draw()
rLo.Draw("same")
rLoMod.Draw("same e3")


rHi.SetTitle(";Jet #rho;Rate")
rHi.GetYaxis().SetTitleOffset(1.0)
cRate.SetLogx()

leg = ROOT.TLegend(0.54, 0.15, 0.84, 0.4)
leg.SetBorderSize(0)
leg.AddEntry( rHi, "p_{T} > 350 GeV, #tau < 0.6", 'p')
leg.AddEntry( rLo, "200 < p_{T} < 350 GeV, #tau < 0.6", 'p')
leg.AddEntry( rLoMod, "200 < p_{T} < 350 GeV, #tau < 0.65", 'p')
leg.Draw()
if options.simulation :
    tlx.DrawLatex(0.131, 0.905, "CMS Simulation #sqrt{s}=13 TeV")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")

cRate.Print("scaled_mistagrate" + options.outname + ".pdf", "pdf")
cRate.Print("scaled_mistagrate" + options.outname + ".png", "png")


fOut = ROOT.TFile("mistagRate_mod" + options.outname + ".root", "RECREATE")
rLoMod.Write()
fOut.Close()

fTruth = ROOT.TFile("mistagRate_truth" + options.outname + ".root", "RECREATE")
rTruth = rHi.Clone()
rTruth.SetName("rLoMod")
rTruth.Write()
fTruth.Close()
