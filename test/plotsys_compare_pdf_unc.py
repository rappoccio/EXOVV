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


fpythia8 = ROOT.TFile("responses_rejec_otherway_qcdmc_2dplots.root")

pyhist_nom = fpythia8.Get(options.hist)
pyhist_pdfup = fpythia8.Get(options.hist + '_syspdfup')
pyhist_pdfdn = fpythia8.Get(options.hist + '_syspdfdn')
pyhist_cteq = fpythia8.Get(options.hist + '_syscteq')
pyhist_mstw = fpythia8.Get(options.hist + '_sysmstw')


stacks = []
canvs = []
for ybin in xrange(1, pyhist_nom.GetNbinsY()+1 ) : 
    proj_nom = pyhist_nom.ProjectionX("nom" + str(ybin), ybin, ybin)
    proj_pdfup = pyhist_pdfup.ProjectionX("pdfup" + str(ybin), ybin, ybin)
    proj_pdfdn = pyhist_pdfdn.ProjectionX("pdfdn" + str(ybin), ybin, ybin)
    proj_cteq = pyhist_cteq.ProjectionX("cteq" + str(ybin), ybin, ybin)
    proj_mstw = pyhist_mstw.ProjectionX("mstw" + str(ybin), ybin, ybin)

    proj_nom.Scale( 1.0 / proj_nom.Integral() )
    proj_pdfup.Scale( 1.0 / proj_pdfup.Integral() )
    proj_pdfdn.Scale( 1.0 / proj_pdfdn.Integral() )
    proj_cteq.Scale( 1.0 / proj_cteq.Integral() )
    proj_mstw.Scale( 1.0 / proj_mstw.Integral() )

    for ibin in xrange( 1, proj_nom.GetNbinsX() ) :
        valnom = proj_nom.GetBinContent(ibin)
        if abs(valnom) > 0.00000001 :

            err = ( (proj_pdfup.GetBinContent(ibin) - proj_pdfdn.GetBinContent(ibin)) * 0.5 )
            valcteq = proj_cteq.GetBinContent(ibin)
            valmstw = proj_mstw.GetBinContent(ibin)
            proj_nom.SetBinContent( ibin, 1.0 )
            proj_nom.SetBinError( ibin, err / valnom )
            proj_cteq.SetBinContent( ibin, valcteq / valnom )
            proj_mstw.SetBinContent( ibin, valmstw / valnom )

        else :
            proj_nom.SetBinContent( ibin, 0.0 )
            proj_nom.SetBinError( ibin, 0. )
            proj_cteq.SetBinContent( ibin, 0. )
            proj_mstw.SetBinContent( ibin, 0. )


    proj_nom.SetFillColor(ROOT.kGray)
    proj_nom.SetFillStyle(1001)
    proj_cteq.SetLineStyle(2)
    proj_cteq.SetLineColor(2)
    proj_mstw.SetLineStyle(4)
    proj_mstw.SetLineColor(4)


    ## proj_nom_clone = proj_nom.Clone("clone")
    ## proj_nom_clone.Add( proj_nom, -1.0 )
    ## proj_cteq.Add( proj_nom, -1.0 )
    ## proj_mstw.Add( proj_nom, -1.0 )

    ## proj_nom_clone.Divide( proj_nom )
    ## proj_cteq.Divide( proj_nom )
    ## proj_mstw.Divide( proj_nom )

    canv = ROOT.TCanvas("c" + str(ybin), "c" + str(ybin) )
    hstack = ROOT.THStack("hstack" + str(ybin), "")
    hstack.Add( proj_nom, "e2")
    hstack.Add( proj_cteq, "hist")
    hstack.Add( proj_mstw, "hist")

    hstack.Draw("nostack")
    hstack.SetMinimum(0.0)
    hstack.SetMaximum(2.0)
    stacks.append(hstack)
    canvs.append(canv)
