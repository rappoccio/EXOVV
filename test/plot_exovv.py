#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'exovv_jetht.root',
                  help='Input file')

parser.add_option('--mcname', type='string', action='store',
                  dest='mcname',
                  default = '',
                  help='String to append to MC names')

parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "exovvplots",
                  help='Output string for output file')

parser.add_option('--rebin', type='int', action='store',
                  dest='rebin',
                  default = None,
                  help='Rebin if desired')



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")


#### Data

f = ROOT.TFile( options.file)
fmc = ROOT.TFile(options.mcname )
    

logy = [ True, False, True, True, True, True, True, True, False, False, False,False,False,False,False,False, ]

hists = ['h2_ptAK8', 'h2_yAK8','h2_mAK8','h2_msoftdropAK8','h2_tau21AK8','h2_jetrhoAK8','h2_mvv']
titles = [
    'AK8 p_{T};p_{T} (GeV)',
    'AK8 Rapidity;y',
    'AK8 ungroomed mass;Mass (GeV)',
     'AK8 soft-drop mass, z_{cut}=0.1, #beta=0;Mass (GeV)',
    'AK8 #tau_{21} = #tau_{2} / #tau_{1};#tau_{21}',
    'AK8 #rho = (m/p_{T}R)^{2};#tau_{21}#rho',
    'Diboson mass;m_{VV} (GeV)'
    ]

mchists = []
canvs = []
legs = []
pads = []
ratios = []

#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

for ihist,histname in enumerate(hists):    
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    mchist = fmc.Get( histname )
    pad0 = ROOT.TPad( histname + '_pad0', 'pad0', 0.0, 0.3, 1.0, 0.97 )
    pad1 = ROOT.TPad( histname + '_pad1', 'pad1', 0.0, 0.0, 1.0, 0.3 )

    pad0.SetBottomMargin(0.01)
    pad1.SetTopMargin(0.01)
    pad1.SetBottomMargin(0.5)
    
    pads.append( [pad0,pad1] )
    pad0.Draw()
    pad1.Draw()
    
    pad0.cd()
        

    s = histname
    print 'Getting ' + s
    hist = f.Get( s )
    hist.SetMarkerStyle(20)
    if options.rebin != None :
        mchist.Rebin( options.rebin )
        hist.Rebin( options.rebin )

    hist.Draw('e')
    mchist.Draw('hist same')
    hist.Draw('e same')
    hist.GetXaxis().SetLabelSize(0)

    
    if logy[ihist] : 
        hist.SetMinimum(0.1)
        pad0.SetLogy()
    #leg.Draw()

    pad1.cd()
    iratio = mchist.Clone()
    iratio.SetName( 'iratio_' + histname )
    iratio.Divide( hist )
    iratio.Draw('e')
    iratio.SetMinimum(0.0)
    iratio.SetMaximum(2.0)
    iratio.UseCurrentStyle()
    iratio.GetYaxis().SetNdivisions(2,4,0,False)
    iratio.SetTitle('')
    iratio.GetXaxis().SetTitle( hist.GetXaxis().GetTitle() )
    ratios.append(iratio)
    canv.cd()
    canv.Update()
    
    canvs.append(canv)
    pads.append( [pad0,pad1])
    legs.append(leg)
    mchists.append( mchist)
    canv.Print( 'exovvplots_' + histname + options.outname + '.png', 'png')
    canv.Print( 'exovvplots_' + histname + options.outname + '.pdf', 'pdf')
