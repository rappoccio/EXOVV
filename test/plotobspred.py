#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = None,
                  help='Input file, without the .root')


parser.add_option('--isData', action='store_true',
                  dest='isData',
                  default = False,
                  help='Is this data?')



parser.add_option('--blind', action='store_true',
                  dest='blind',
                  default = False,
                  help='Blind signal region?')



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetOptFit(0000)
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(42)
tlx.SetTextSize(0.057)


ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
#ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

f = ROOT.TFile(options.file + '.root')

hobs = f.Get("pred_mvvmod")
hpred= f.Get("pred_mvvmod_pred")

lumi = 2500

if not options.isData :
    hobs.Scale(lumi)
    hpred.Scale(lumi)


canv = ROOT.TCanvas('c1','c1', 800, 700)
canv.cd()
pad1 = ROOT.TPad('p1', 'p1', 0.,2./7.,1.0,1.0)
pad1.SetBottomMargin(0.)
pad2 = ROOT.TPad('p1', 'p1', 0.,0.,1.0,2./7.)
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.4)
pad1.Draw()
pad2.Draw()

pad1.cd()
hobs.SetMarkerStyle(20)
hpred.SetFillColor( ROOT.kYellow )
hpredclone = hpred.Clone()
hpredclone.SetName("hpredclone")
hpredclone.SetFillColor(1)
hpredclone.SetFillStyle(3004)
hpredclone.SetMarkerStyle(0)

#hpred.SetLineColor(2)
#hpred.SetMarkerColor(2)
#hpred.SetMarkerStyle(24)

hs = ROOT.THStack('hs', ';m_{VV} (GeV);Number')
if not options.blind : 
    hs.Add( hobs )
hs.Add( hpred, 'hist' )
hs.Draw("nostack")
hs.GetYaxis().SetTitleOffset(1.0)
#hs.GetXaxis().SetRangeUser(1000., 5000.)
hpredclone.Draw("same e3")
if not options.blind :
    hobs.Draw("same")
else :
    hobs.Draw("axis same")



leg = ROOT.TLegend(0.6,0.6,0.8,0.8)
if options.isData :
    leg.AddEntry( hobs, 'Data', 'p')
    leg.AddEntry( hpred, 'Predicted QCD', 'f')
else :
    leg.AddEntry( hobs, 'Observed QCD MC', 'p')
    leg.AddEntry( hpred, 'Predicted QCD MC', 'f')



leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.Draw()
ROOT.gPad.SetLogy()

if not options.isData: 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
else : 
    tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
    

ratio = hobs.Clone()
ratio.SetName('ratio')
ratio.Divide( hpred )
ratio.UseCurrentStyle()
ratio.SetFillStyle(3004)
ratio.SetFillColor(1)

pad2.cd()

ratio.SetMarkerStyle(1)
ratio.SetMarkerSize(0)
ratio.SetTitle(';' + hs.GetXaxis().GetTitle() + ';Ratio')


ratio.SetMinimum(0.)
ratio.SetMaximum(2.)
ratio.GetYaxis().SetNdivisions(2,4,0,False)
#ratio.GetXaxis().SetRangeUser(1000.,3500.)
if not options.blind : 
    ratio.Draw('e3')
else :
    ratio.Draw("axis")
#fit = ratio.Fit('pol1')
ratio.GetYaxis().SetTitleOffset(1.0)
ratio.GetXaxis().SetTitleOffset(3.0)
#ratio.SetTitleSize(20, "XYZ")


canv.cd()
canv.Update()

if not options.blind : 
    canv.Print(options.file + '_obspred.pdf', 'pdf')
    canv.Print(options.file + '_obspred.png', 'png')
else : 
    canv.Print(options.file + '_obspred_blind.pdf', 'pdf')
    canv.Print(options.file + '_obspred_blind.png', 'png')

