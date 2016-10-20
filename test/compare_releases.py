#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt

parser = OptionParser()


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "",
                  help='Histogram to plot')



(options, args) = parser.parse_args()
argv = []

print options

import ROOT
import array
import math
import random


ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetTitleOffset(1.5, "Y")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")


def setupPads(canv, pads):
    canv.cd()
    pad1 = ROOT.TPad('pad' + canv.GetName() + '1', 'pad' + canv.GetName() + '1', 0., 0.3, 1.0, 1.0)
    pad1.SetBottomMargin(0)
    pad2 = ROOT.TPad('pad' + canv.GetName() + '2', 'pad' + canv.GetName() + '2', 0., 0.0, 1.0, 0.3)
    pad2.SetTopMargin(0)
    pad1.SetLeftMargin(0.20)
    pad2.SetLeftMargin(0.20)
    pad2.SetBottomMargin(0.5)
    pad1.Draw()
    pad2.Draw()
    pads.append( [pad1,pad2] )
    return [pad1, pad2]



samples = [
    ['responses_repdf_otherway_qcdmc_2dplots.root', '7.6.x', 1, 1],
    ['responses_otherway_qcdmc.root',               '7.4.x', 2, 2]
    ]
    
names = [
    "h_pt_meas",	
    "h_y_meas",	
    "h_phi_meas",	
    "h_m_meas",	
    "h_msd_meas",	
    "h_rho_meas",	
    "h_tau21_meas",	
    "h_dphi_meas",	
    "h_ptasym_meas",	
    ]
hists = []
stacks = []
f = []
legs = []


for isample in xrange( len(samples) ) :
    f.append( ROOT.TFile(samples[isample][0] ) )

    hists.append( [] )

    for iname in xrange( len(names) ) :
        htemp = f[isample].Get(names[iname] )
        htemp.UseCurrentStyle()
        #if htemp.Integral() > 0 :
        #    htemp.Scale( 1.0 / htemp.Integral() )
        htemp.SetLineStyle(samples[isample][2])
        htemp.SetLineColor(samples[isample][3])
        
        hists[isample].append( htemp )

canvs = []
allpads = []
ratios = []
for iname in xrange( len(names) ) :
    c = ROOT.TCanvas("c" + str(iname), "c" + str(iname), 800, 600 )
    pads = setupPads(c, allpads)
    pads[0].cd()

    hists[0][iname].Draw("hist")
    hists[1][iname].Draw("hist same")
    leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry( hists[0][iname], samples[0][1], 'l' )
    leg.AddEntry( hists[1][iname], samples[1][1], 'l' )
    leg.Draw()
    legs.append(leg)
    max0 = hists[0][iname].GetMaximum()
    max1 = hists[1][iname].GetMaximum()
    maxtot = max( max0, max1) * 1.2
    hists[0][iname].SetMaximum(maxtot)
    pads[0].SetLogy()
    pads[0].Update()
    pads[1].cd()
    ratio = hists[1][iname].Clone( hists[1][iname].GetName() + "clone")
    ratio.Divide( hists[0][iname] )
    ratio.SetTitle("")
    ratio.GetYaxis().SetTitle("Ratio")
    ratio.Draw("e")
    ratio.GetYaxis().SetRangeUser(0.9,1.1)
    ratio.GetYaxis().SetNdivisions(2,4,0,False)
    ratios.append(ratio)
    pads[1].Update()
    c.Update()
    c.Print( 'compare_' + options.outname + names[iname] + ".png", "png")
    c.Print( 'compare_' + options.outname + names[iname] + ".pdf", "pdf")
    canvs.append(c)
    
    
