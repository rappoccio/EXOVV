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
ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetTitleOffset(1.5, "Y")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

ptBinA = array.array('i', [  200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 13000])



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


datahists = []
pyhists = []
hwhists = []

fdata = ROOT.TFile("jetht_weighted_dataplots_otherway_rejec.root")
fpythia8 = ROOT.TFile("responses_rejec_otherway_qcdmc_2dplots.root")
fherwig = ROOT.TFile("qcdmc_herwig_otherway_rejec_2dplots.root")

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
copies = []
ratios = []
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(25)

tlx2 = ROOT.TLatex()
tlx2.SetNDC()
tlx2.SetTextFont(43)
tlx2.SetTextSize(22)
legs = []

for iptbin in xrange( len(dataprojs) ) :
    c = ROOT.TCanvas("c" + str(iptbin), "c" + str(iptbin), 800, 600)
    pads = setupPads(c, allpads)
    pads[0].cd()
    pads[0].SetLogx()
    axisrange = []
    if iptbin == 11:
        axisrange = [1,2000]
    elif iptbin > 7 and iptbin < 11:
        axisrange = [1,900]
    elif iptbin > 3 and iptbin < 8:
        axisrange = [1,600]
    elif iptbin < 4:
        axisrange = [1,400]


    for imbin in xrange( 1,dataprojs[iptbin].GetNbinsX()+1 ) :
        val = pyprojs[iptbin].GetBinContent( imbin )


        jecup = pysysprojs[JECUP][iptbin].GetBinContent( imbin )
        jecdn = pysysprojs[JECDN][iptbin].GetBinContent( imbin )
        jerup = pysysprojs[JERUP][iptbin].GetBinContent( imbin )
        jerdn = pysysprojs[JERDN][iptbin].GetBinContent( imbin )
        jmrup = pysysprojs[JMRUP][iptbin].GetBinContent( imbin )
        jmrdn = pysysprojs[JMRDN][iptbin].GetBinContent( imbin )
        pdfup = pysysprojs[PDFUP][iptbin].GetBinContent( imbin )
        pdfdn = pysysprojs[PDFDN][iptbin].GetBinContent( imbin )
        hwval = hwprojs[iptbin].GetBinContent(imbin)
        
        #print ' pt,m = %6d,%6d : jec=(%8.3e-%8.3e), jer=(%8.3e - %8.3e), jmr=(%8.3e - %8.3e), pdf=(%8.3e - %8.3e)' % ( iptbin, imbin, jecup, jecdn, jerup, jerdn, jmrup, jmrdn, pdfup, pdfdn )
        errtot = 0.
        if abs(val) > 0.001:
            errstat = pyprojs[iptbin].GetBinError ( imbin ) / val
            errtot = errstat**2 
            jec = (jecup - jecdn) * 0.5 / val
            jer = (jerup - jerdn) * 0.5 / val
            jmr = (jmrup - jmrdn) * 0.5 / val
            pdf = (pdfup - pdfdn) * 0.5 / val
            psunc = (hwval - val) * 0.5 / val
            errtot += jec**2 + jer**2 + jmr**2 + pdf**2 + psunc**2
            errtot = sqrt(errtot) * val
        pyprojs[iptbin].SetBinError( imbin, errtot )
    pyprojs[iptbin].SetFillStyle(3001)
    pyprojs[iptbin].SetFillColor(ROOT.kBlue)
    pyprojs[iptbin].SetMarkerStyle(0)
    pyprojs[iptbin].SetMarkerSize(0)
    dataprojs[iptbin].SetMarkerStyle(20)
    stack = ROOT.THStack( "stack" + str(iptbin), ";;Fraction / GeV" )
    stack.Add( pyprojs[iptbin], "e2" )
    stack.Add( dataprojs[iptbin], "e" )

    #pyprojs[iptbin].Draw("e2 same")
    #pyprojs[iptbin].GetXaxis().SetRangeUser(1,1300)
    #dataprojs[iptbin].Draw("e same")
    stack.Draw("nostack")
    maxval = stack.GetMaximum()
    stack.SetMaximum( maxval * 0.6 )
    stack.GetXaxis().SetRangeUser(axisrange[0],axisrange[1])
    stacks.append(stack)
    tlx.DrawLatex(0.2, 0.926, "CMS Preliminary")
    tlx.DrawLatex(0.72, 0.926, "2.3 fb^{-1} (13 TeV)")

    

    if 'AK8SD' not in options.hist :
        tlx2.DrawLatex( 0.3, 0.4, "p_{T} = " + str(ptBinA[iptbin]) + '-' + str(ptBinA[iptbin+1]) + ' GeV' ) 
        leg = ROOT.TLegend(0.3, 0.6, 0.55, 0.85)
    elif 'AK8SD' in options.hist :
        tlx2.DrawLatex( 0.6, 0.4, "p_{T} = " + str(ptBinA[iptbin]) + '-' + str(ptBinA[iptbin+1]) + ' GeV' ) 
        leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry( dataprojs[iptbin], 'Data', 'p')
    leg.AddEntry( pyprojs[iptbin], 'PYTHIA8 MC', 'f')
    leg.Draw()
    legs.append(leg)
    
    pads[1].cd()
    pads[1].SetLogx()
    ratio = pyprojs[iptbin].Clone("ratio" + pyprojs[iptbin].GetName() )
    ratio.UseCurrentStyle()
    ratio.SetTitle(";Jet mass (GeV);MC / Data")
    ratio.Divide( dataprojs[iptbin] )
    ratio.SetFillColor(ROOT.kBlue)
    ratio.SetFillStyle(3001)
    ratio.GetYaxis().SetNdivisions(2,4,0,False)
    ratio.GetXaxis().SetRangeUser(axisrange[0],axisrange[1])
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.SetMarkerStyle(0)
    ratio.SetMarkerSize(0)
    ratio.Draw("e2")
    ratios.append(ratio)
    pads[0].Update()
    pads[1].Update()
    c.Update()
    canvs.append(c)

    if 'AK8SD' not in options.hist : 
        c.Print("jetplots_h_m_meas" + str(iptbin) + "jetht.png", "png")
        c.Print("jetplots_h_m_meas" + str(iptbin) + "jetht.pdf", "pdf")
    elif 'AK8SD' in options.hist : 
        c.Print("jetplots_h_msd_meas" + str(iptbin) + "jetht.png", "png")
        c.Print("jetplots_h_msd_meas" + str(iptbin) + "jetht.pdf", "pdf")

 
