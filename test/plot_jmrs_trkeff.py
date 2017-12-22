#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--postfix', type='string', action='store',
                  dest='postfix',
                  default = '',
                  help='Postfix for plots')



(options, args) = parser.parse_args()
argv = []

import math
import ROOT
import sys
import array
ROOT.gROOT.Macro("rootlogon.C")

canvs = []
rgs = []
effs = [1.00, 0.99, 0.98, 0.97, 0.96, 0.95]
effstrs = [ '100', '099', '098', '097', '096', '095' ]
for effstr in effstrs :
    
    f = ROOT.TFile("jmr_ungroomed_trkeff" + effstr + ".root")
    c = f.Get("totresc2_0")
    c.Draw()
    canvs.append(c)
    
    rg = c.GetPrimitive("rg_0").Clone( 'eff_' + effstr )    
    rgs.append( rg )

rg0 = rgs[0].Clone("rg0")
gs0 = rg0.GetListOfGraphs()

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])
r = 0.8 / math.sqrt(2.)
xmaxes = [ x * r for x in ptBinA ]
xmins = [ x / 20. for x in ptBinA ]

canvs = []
rgsdiv = []
for irg,rg in enumerate(rgs):
    ci = ROOT.TCanvas("c" + rg.GetName(), "c" + rg.GetName() )
    gs = rg.GetListOfGraphs()
    rgdiv = ROOT.TMultiGraph( rg.GetName() + "_div", "Track Efficiency = " + str(effs[irg]) + rg.GetTitle() + " Uncertainty")
    for ig,g in enumerate(gs):
        
        xdiv = array.array('d', [])
        ydiv = array.array('d', [])
        for i in xrange( g.GetN() ):
            x = ROOT.Double(0.0)
            y = ROOT.Double(0.0)
            y0 = ROOT.Double(0.0)
            dy = g.GetErrorY(i)
            
            g.GetPoint(i,x,y)
            gs0[ig].GetPoint(i,x,y0)
            if y0 > 0.0 and y > 0.0 and dy / y < 0.75 and x > xmins[ig] and x < xmaxes[ig] :
                xdiv.append( x )
                ydiv.append( (y-y0)/y0)
        gdiv = ROOT.TGraph( len(xdiv), xdiv, ydiv )        
        gdiv.SetName(g.GetName() + "_div")
        gdiv.SetLineStyle(g.GetLineStyle())
        gdiv.SetLineColor(g.GetLineColor())

        rgdiv.Add( gdiv )
    rgsdiv.append( rgdiv )

    ci.cd()
    rgdiv.Draw("AL")
    rgdiv.GetHistogram().SetTitleOffset(1.0, "Y")
    rgdiv.SetMinimum(0.0)
    rgdiv.SetMaximum(0.5)
    ci.Update()
    canvs.append(ci)
    ci.Print("jmr_unc_trkeff" + effstr[irg] + ".png", "png" )
    ci.Print("jmr_unc_trkeff" + effstr[irg] + ".pdf", "pdf" )
