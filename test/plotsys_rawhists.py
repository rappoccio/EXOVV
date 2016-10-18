#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "sysvars_raw",
                  help='Label for plots')

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = None,
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
#ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")




def getProjsY( name, h, norm=True ) :
    projs = []
    for y in xrange( 1, h.GetNbinsY()+1 ) :
        proj = h.ProjectionX( name + '_' + h.GetName() + "_proj" + str(y), y, y, 'e' )
        if norm and proj.Integral() > 0.0 :            
            proj.Scale( 1.0 / proj.Integral() )
        for x in xrange( 1,proj.GetNbinsX()+1 ) :
            val = proj.GetBinContent(x) / proj.GetBinWidth(x)
            err = proj.GetBinError(x) / proj.GetBinWidth(x)
            proj.SetBinContent( x, val )
            proj.SetBinError(x, err )        
        projs.append( proj )
    return projs


def setup1(canv):
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
    return [pad1,pad2]


datahists = []
pyhists = []
hwhists = []

fdata = ROOT.TFile("jetht_weighted_dataplots_otherway_repdf.root")
fpythia8 = ROOT.TFile("responses_repdf_otherway_qcdmc_2dplots.root")
fherwig = ROOT.TFile("qcdmc_herwig_otherway_repdf_2dplots.root")

systs = [
    'jecup', 'jecdn', 'jerup', 'jerdn', 'jmrup', 'jmrdn', 'pdfup', 'pdfdn'
    ]

JECUP=systs.index('jecup')
JECDN=systs.index('jecdn')
JERUP=systs.index('jerup')
JERDN=systs.index('jerdn')
JMRUP=systs.index('jmrup')
JMRDN=systs.index('jmrdn')
PDFUP=systs.index('pdfup')
PDFDN=systs.index('pdfdn')

datahist = fdata.Get(options.hist)
pyhist = fpythia8.Get(options.hist)
hwhist = fherwig.Get(options.hist)


dataprojs = getProjsY( name='data', h= datahist )
pyprojs = getProjsY( name='py', h=pyhist )
hwprojs = getProjsY( name='hw', h=hwhist )

pysysprojs = []

for isyst in xrange( len( systs ) ) : 
    pysysprojs.append( getProjsY( name='pysys',h=fpythia8.Get( options.hist + '_sys' + systs[isyst] ) ) )


canvs = []
stacks = []
allpads = []

for iptbin in xrange( len(dataprojs) ) :
    c = ROOT.TCanvas("c" + str(iptbin), "c" + str(iptbin), 600, 800)
    pads = setup1(c)
    pads[0].cd()
    #c.SetLogx()
    canvs.append(c)
    for imbin in xrange( 1,dataprojs[iptbin].GetNbinsX()+1 ) :
        val = pyprojs[iptbin].GetBinContent( imbin )
        errstat = pyprojs[iptbin].GetBinError ( imbin )
        errtot = errstat**2

        jecup = pysysprojs[JECUP][iptbin].GetBinContent( imbin )
        jecdn = pysysprojs[JECDN][iptbin].GetBinContent( imbin )
        jerup = pysysprojs[JERUP][iptbin].GetBinContent( imbin )
        jerdn = pysysprojs[JERDN][iptbin].GetBinContent( imbin )
        jmrup = pysysprojs[JMRUP][iptbin].GetBinContent( imbin )
        jmrdn = pysysprojs[JMRDN][iptbin].GetBinContent( imbin )
        pdfup = pysysprojs[PDFUP][iptbin].GetBinContent( imbin )
        pdfdn = pysysprojs[PDFDN][iptbin].GetBinContent( imbin )
        print ' pt,m = %6d,%6d : jec=(%8.3e-%8.3e), jer=(%8.3e - %8.3e), jmr=(%8.3e - %8.3e), pdf=(%8.3e - %8.3e)' % ( iptbin, imbin, jecup, jecdn, jerup, jerdn, jmrup, jmrdn, pdfup, pdfdn )
        if abs(val) > 0.001: 
            jec = (jecup - jecdn) * 0.5 / val
            jer = (jerup - jerdn) * 0.5 / val
            jmr = (jmrup - jmrdn) * 0.5 / val
            pdf = (pdfup - pdfdn) * 0.5 / val
            errtot += jec**2 + jer**2 + jmr**2 + pdf**2
        errtot = sqrt(errtot) * val
        pyprojs[iptbin].SetBinError( imbin, errtot )
    pyprojs[iptbin].SetFillStyle(3004)
    pyprojs[iptbin].SetFillColor(ROOT.kRed)
    pyprojs[iptbin].SetMarkerStyle(0)
    dataprojs[iptbin].SetMarkerStyle(20)
    stack = ROOT.THStack( )
    stack.Add( dataprojs[iptbin], "e" )
    stack.Add( pyprojs[iptbin], "e2" )

    #pyprojs[iptbin].Draw("e2 same")
    #pyprojs[iptbin].GetXaxis().SetRangeUser(1,1300)
    #dataprojs[iptbin].Draw("e same")
    stack.Draw("nostack")
    stacks.append(stack)

    pads[1].cd()
    frac = pyprojs[iptbin].Clone("frac" + pyprojs[iptbin].GetName() )
    frac.Divide( dataprojs[iptbin] )
    frac.Draw("e2")
    frac.GetYaxis().SetRangeUser(0,2)
     

    allpads.append(pads)



 
