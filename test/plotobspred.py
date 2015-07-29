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



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")


f = ROOT.TFile(options.file + '.root')

hobs = f.Get("pred_mvv")
hpred= f.Get("pred_mvv_pred")



hobs.SetMarkerStyle(20)
hpred.SetLineColor(2)
hpred.SetMarkerColor(2)
hpred.SetMarkerStyle(24)

hs = ROOT.THStack('hs', ';m_{VV} (GeV);Number')
hs.Add( hobs )
hs.Add( hpred )
hs.Draw("nostack")
hs.GetYaxis().SetTitleOffset(1.0)

leg = ROOT.TLegend(0.6,0.6,0.8,0.8)
leg.AddEntry( hobs, 'Observed', 'p')
leg.AddEntry( hpred, 'Predicted', 'p')

leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.Draw()

ROOT.gPad.Print(options.file + '_obspred.pdf', 'pdf')
ROOT.gPad.Print(options.file + '_obspred.png', 'png')


