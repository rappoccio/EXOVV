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

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(25, "XYZ")
ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetTitleOffset(1.8, "Y")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

ptBinA = array.array('i', [  200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 13000])

mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])


def minmassbin_ungroomed(ibin) :
    if ptBinA[ibin] < 760:
        return 5
    else :
        return 6

def minmassbin_groomed(ibin) :
    return 4

def getProjsY( name, h, norm=True ) :
    projs = []
    for y in xrange( 1, h.GetNbinsY()+1 ) :
        proj = h.ProjectionX( name + '_' + h.GetName() + "_proj" + str(y), y, y, 'e' )
        if norm and proj.Integral("width") > 0.0 :            
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
    pad1.SetBottomMargin(0.022)
    pad2 = ROOT.TPad('pad' + canv.GetName() + '2', 'pad' + canv.GetName() + '2', 0., 0.0, 1.0, 0.3)
    pad2.SetTopMargin(0.05)
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
    'jecup', 'jecdn', 'jerup', 'jerdn', 'jmrup', 'jmrdn', 'puup', 'pudn', 'pdfup', 'pdfdn'
    ]

JECUP=systs.index('jecup')
JECDN=systs.index('jecdn')
JERUP=systs.index('jerup')
JERDN=systs.index('jerdn')
JMRUP=systs.index('jmrup')
JMRDN=systs.index('jmrdn')
PUUP=systs.index('puup')
PUDN=systs.index('pudn')
PDFUP=systs.index('pdfup')
PDFDN=systs.index('pdfdn')

datahist = fdata.Get(options.hist)
pyhist = fpythia8.Get(options.hist)
hwhist = fherwig.Get(options.hist)


dataprojs = getProjsY( name='data', h= datahist )
pyprojs = getProjsY( name='py', h=pyhist )
hwprojs = getProjsY( name='hw', h=hwhist )
pyprojsclone = []

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
    pyprojs[iptbin].UseCurrentStyle()
    c = ROOT.TCanvas("c" + str(iptbin), "c" + str(iptbin), 800, 600)
    pads = setupPads(c, allpads)
    pads[0].cd()
    pads[0].SetLogx()
    axisrange = []


    if 'AK8SD' in options.hist :
        minmassbin = minmassbin_groomed( iptbin )
    else : 
        minmassbin = minmassbin_ungroomed( iptbin )
    
    
    if iptbin == 11:
        axisrange = [mBinA[minmassbin],2000]
    elif iptbin > 7 and iptbin < 11:
        axisrange = [mBinA[minmassbin],1100]
    elif iptbin > 3 and iptbin < 8:
        axisrange = [mBinA[minmassbin],1100]
    elif iptbin < 4:
        axisrange = [mBinA[minmassbin],1100]


    for imbin in xrange( 1, minmassbin ) :
        pyprojs[iptbin].SetBinContent( imbin, 0.0 )
        pyprojs[iptbin].SetBinError( imbin, 0.0 )

    for imbin in xrange( minmassbin,dataprojs[iptbin].GetNbinsX()+1 ) :
        val = pyprojs[iptbin].GetBinContent( imbin )


        jecup = pysysprojs[JECUP][iptbin].GetBinContent( imbin )
        jecdn = pysysprojs[JECDN][iptbin].GetBinContent( imbin )
        jerup = pysysprojs[JERUP][iptbin].GetBinContent( imbin )
        jerdn = pysysprojs[JERDN][iptbin].GetBinContent( imbin )
        jmrup = pysysprojs[JMRUP][iptbin].GetBinContent( imbin )
        jmrdn = pysysprojs[JMRDN][iptbin].GetBinContent( imbin )
        puup = pysysprojs[PUUP][iptbin].GetBinContent( imbin )
        pudn = pysysprojs[PUDN][iptbin].GetBinContent( imbin )
        pdfup = pysysprojs[PDFUP][iptbin].GetBinContent( imbin )
        pdfdn = pysysprojs[PDFDN][iptbin].GetBinContent( imbin )
        hwval = hwprojs[iptbin].GetBinContent(imbin)
        
        #print ' pt,m = %6d,%6d : jec=(%8.3e-%8.3e), jer=(%8.3e - %8.3e), jmr=(%8.3e - %8.3e), pdf=(%8.3e - %8.3e)' % ( iptbin, imbin, jecup, jecdn, jerup, jerdn, jmrup, jmrdn, pdfup, pdfdn )
        errtot = 0.
        if abs(val) > 1e-20:
            errstat = pyprojs[iptbin].GetBinError ( imbin ) / val
            errtot = errstat**2 
            jec = (jecup - jecdn) * 0.5 / val
            jer = (jerup - jerdn) * 0.5 / val
            jmr = (jmrup - jmrdn) * 0.5 / val
            pu = (puup - pudn) * 0.5 / val
            pdf = (pdfup - pdfdn) * 0.5 / val
            psunc = (hwval - val) * 0.5 / val
            errtot += jec**2 + jer**2 + jmr**2 + pu**2 + pdf**2 + psunc**2
            errtot = sqrt(errtot) * val


        pyprojs[iptbin].SetBinError( imbin, errtot )
        hwprojs[iptbin].SetBinError( imbin, 1e-12 )
    pyprojsclone.append( pyprojs[iptbin].Clone( pyprojs[iptbin].GetName() + "_linestyle") )
    pyprojsclone[iptbin].SetLineColor(ROOT.kBlue)
    pyprojs[iptbin].SetFillStyle(3001)
    pyprojs[iptbin].SetFillColor(ROOT.kBlue)
    pyprojs[iptbin].SetMarkerStyle(0)
    pyprojs[iptbin].SetMarkerSize(0)
    hwprojs[iptbin].SetLineStyle(2)
    hwprojs[iptbin].SetLineColor(2)
    #hwprojs[iptbin].SetLineWidth(2)
    dataprojs[iptbin].SetMarkerStyle(20)
    stack = ROOT.THStack( "stack" + str(iptbin), ";;Normalized yield (1/GeV)" )
    stack.Add( pyprojs[iptbin], "e2 ][" )
    stack.Add( pyprojsclone[iptbin], "hist ][" )
    stack.Add( hwprojs[iptbin], "hist ][")
    stack.Add( dataprojs[iptbin], "e ][" )

    #pyprojs[iptbin].Draw("e2 same")
    #pyprojs[iptbin].GetXaxis().SetRangeUser(1,1300)
    #dataprojs[iptbin].Draw("e same")    
    stack.Draw("nostack")    
    stack.GetXaxis().SetRangeUser(axisrange[0],axisrange[1])
    if 'AK8SD' in options.hist :
        maxval = dataprojs[iptbin].GetBinContent( minmassbin + 1)
        stack.SetMaximum( maxval * 1.5 )
    else :
        maxval = dataprojs[iptbin].GetMaximum()
        stack.SetMaximum( maxval * 1.5  )

    stack.GetXaxis().SetTickLength(0.05)
    stacks.append(stack)
    tlx.DrawLatex(0.2, 0.926, "CMS Preliminary")
    tlx.DrawLatex(0.72, 0.926, "2.3 fb^{-1} (13 TeV)")

    

    #if 'AK8SD' not in options.hist :
    #    tlx2.DrawLatex( 0.3, 0.4, str(ptBinA[iptbin]) + ' < p_{T} < ' + str(ptBinA[iptbin+1]) + ' GeV' ) 
    #    leg = ROOT.TLegend(0.3, 0.6, 0.55, 0.85)
    #elif 'AK8SD' in options.hist :
    tlx2.DrawLatex( 0.6, 0.4, str(ptBinA[iptbin]) + ' < p_{T} < ' + str(ptBinA[iptbin+1]) + ' GeV' ) 
    leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry( dataprojs[iptbin], 'Data', 'p')
    leg.AddEntry( hwprojs[iptbin], 'HERWIG++ MC', 'l')
    leg.AddEntry( pyprojs[iptbin], 'PYTHIA8 MC', 'lf')
    leg.Draw()
    legs.append(leg)
    
    pads[1].cd()
    pads[1].SetLogx()
    ratio = pyprojs[iptbin].Clone("ratio" + pyprojs[iptbin].GetName() )
    #ratio.UseCurrentStyle()
    ratio2 = hwprojs[iptbin].Clone("ratio2" + hwprojs[iptbin].GetName() )
    #ratio2.UseCurrentStyle()




    if 'AK8SD' not in options.hist : 
        ratio.SetTitle(";Jet mass (GeV);MC / Data")
    else :
        ratio.SetTitle(";Groomed jet mass (GeV);MC / Data")
    ratio.Divide( dataprojs[iptbin] )
    ratio2.Divide( dataprojs[iptbin] )
    ratioline = ratio.Clone( "ratioclone" + pyprojs[iptbin].GetName() )
    ratioline.SetFillStyle(0)    
    for imbin in xrange( 1,hwprojs[iptbin].GetNbinsX()+1 ) :
        ratio2.SetBinError( imbin, 1e-12)
        ratioline.SetBinError( imbin, 1e-12)
    ratio.SetFillColor(ROOT.kBlue)
    ratio.SetFillStyle(3001)
    ratio.GetYaxis().SetNdivisions(2,4,0,False)
    ratio.GetXaxis().SetRangeUser(axisrange[0],axisrange[1])
    ratio.GetYaxis().SetRangeUser(0.5,1.5)
    ratio.GetXaxis().SetTickLength(0.09)
    ratio.GetXaxis().SetNoExponent()
    #ratio.GetXaxis().SetMoreLogLabels(True)
    ratio.SetMarkerStyle(0)
    ratio.SetMarkerSize(0)
    ratio.Draw("e2")
    ratioline.Draw("hist ][ same")
    ratio2.Draw("hist same ][")
    ratios.append(ratio)
    ratios.append(ratio2)
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

 
