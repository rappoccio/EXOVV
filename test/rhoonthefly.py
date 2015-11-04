#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "nom",
                  help='Label for plots')

parser.add_option('--signalRegion', action='store_true',
                  dest='signalRegion',
                  default = False,
                  help='Plot signal region?')



(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math


ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

name = 'tau_vs_rho'

dataIn = ROOT.TFile( 'exovv_wv_v74x_v6_dataset6_ntuple.root' )
#wjetsIn = ROOT.TFile( 'NTUPLES/wjets_b2ganafw_v5_sel1_extracats_jecv5_updatedmcrw_ntuple.root' )

lumi = 1263.88

data = dataIn.Get("TreeEXOVV")


xaxis = '#rho = (m/p_{T}R)^{2}'
variable = 'FatJetRhoRatio[0]'
histbins = '(10,0,0.5)'
weightstr= ''

plotsToMake = [
    # name                        title                                                taucut mmin   mmax    ptmin ptmax   style
    ['pt200toInf_m0toInf_tau10',  'p_{T} > 200 GeV',                                    1.0,   0.,    13000., 200., 13000., 20],
    ['pt200toInf_m0toInf_tau06',  'p_{T} > 200 GeV',                                    0.6,   0.,    13000., 200., 13000., 24],#0
    ['pt200to350_m50toInf_tau10', '200 < p_{T} < 350 GeV, m > 50 GeV',                  1.0,  50.,    13000., 200., 350.,   20],
    ['pt200to350_m50toInf_tau06', '200 < p_{T} < 350 GeV, m > 50 GeV, #tau_{21} < 0.6', 0.6,  50.,    13000., 200., 350.,   24],#1
    ['pt200to350_m28toInf_tau10', '200 < p_{T} < 350 GeV, m > 28 GeV',                  1.0,  28.571, 13000., 200., 350.,   20],
    ['pt200to350_m28toInf_tau065','200 < p_{T} < 350 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 13000., 200., 350.,   24],#2
    ['pt350toInf_m50toInf_tau10', 'p_{T} > 350 GeV, m > 50 GeV',                        1.0,  50.,    13000., 350., 13000., 20],
    ['pt350toInf_m50toInf_tau06', 'p_{T} > 350 GeV, m > 50 GeV, #tau_{21} < 0.6',       0.6,  50.,    13000., 350., 13000., 24],#3
    ['pt200to275_m39toInf_tau10', '200 < p_{T} < 275 GeV, m > 39 GeV',                  1.0,  39.286, 13000., 200., 275.,   20],
    ['pt200to275_m39toInf_tau06', '200 < p_{T} < 275 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 13000., 200., 275.,   24],#4
    ['pt200to275_m28toInf_tau10', '200 < p_{T} < 275 GeV, m > 28 GeV',                  1.0,  28.571, 13000., 200., 275.,   20],
    ['pt200to275_m28toInf_tau065','200 < p_{T} < 275 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 13000., 200., 275.,   24],#5
    ['pt275to350_m39toInf_tau10', '275 < p_{T} < 350 GeV, m > 39 GeV',                  1.0,  39.286, 13000., 275., 350.,   20],
    ['pt275to350_m39toInf_tau06', '275 < p_{T} < 350 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 13000., 275., 350.,   24],#6
    ]
hdatas = []

huhcanv = []
for [ name, title, taucut, mMin, mMax, ptMin, ptMax, style ] in plotsToMake : 
    cut = '(' + \
      'LeptonPt[0] > 120. && LeptonPt[0] + METpt > 250. && FatJetRhoRatio[0] > 1e-3 &&' + \
      'LeptonIso[0] / LeptonPt[0] < 0.15' + '&&' \
      'FatJetTau21[0] < ' + str(taucut) +  '&&' \
      'FatJetMassSoftDrop[0] > ' + str(mMin) + '&&' + \
      'FatJetMassSoftDrop[0] <= ' + str(mMax) + '&&' + \
      'FatJetPt[0] > ' + str(ptMin) + '&&' + \
      'FatJetPt[0] <= ' + str(ptMax) + \
      ')'


    data.Draw(variable + " >> " + name + histbins, cut, 'goff')
    hdata = ROOT.gDirectory.Get(name)
    hdata.SetName(name)
    hdata.SetTitle( ';' + xaxis )
    hdata.SetMarkerStyle(style)
    hdata.Sumw2()
    hdatas.append(hdata)



canvs = []
rates = []
nlegs = []
for ndxToPlot in range(0, len(plotsToMake), 2) : 
    hdata1 = hdatas[ndxToPlot]
    hdata2 = hdatas[ndxToPlot+1]
    nleg = ROOT.TLegend(0.6, 0.6, 0.84, 0.74)
    nleg.SetFillColor(0)
    nleg.SetBorderSize(0)

    canvname = 'c' + str(ndxToPlot)
    c = ROOT.TCanvas(canvname, canvname)
    print 'Drawing : '
    print hdata1.GetName()
    print hdata2.GetName()
    hdata1.Draw('e')
    hdata2.Draw('e same')
    nleg.AddEntry( hdata1, 'All', 'p')
    nleg.AddEntry( hdata2, '#tau_{21} < ' + str( plotsToMake[ndxToPlot+1][2] ) , 'p')
    nleg.Draw()
    nlegs.append(nleg)

    tlx = ROOT.TLatex()
    tlx.SetNDC()
    tlx.SetTextFont(42)
    tlx.SetTextSize(0.057)
    tlx.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
    tlx.SetTextSize(0.025)

    tlxm = ROOT.TLatex()
    tlxm.SetNDC()
    tlxm.SetTextFont(42)
    tlxm.SetTextSize(0.047)
    tlxm.DrawLatex(0.4, 0.81, plotsToMake[ndxToPlot][1])
    tlxm.SetTextSize(0.025)    

    #c.SetLogx()
    c.Update()

    canvs.append(c)

    hrate = hdata2.Clone()
    hrate.SetName( 'rate_' + hdata2.GetName() )
    hrate.SetTitle( plotsToMake[ndxToPlot+1][1] )
    hrate.Divide( hdata2, hdata1, ROOT.Double(1), ROOT.Double(1), 'b')
    rates.append( hrate )
    
    c.Print( options.outlabel + '_' + hdata2.GetName() + '.png', 'png' )
    c.Print( options.outlabel + '_' + hdata2.GetName() + '.pdf', 'pdf' )



csum = ROOT.TCanvas('csum', 'csum', 600, 600)
csum.cd()
pad1 = ROOT.TPad('p1', 'p1',0.0, 0.0, 1.0, 0.2)
pad1.SetTopMargin(0)
pad1.SetBottomMargin(0.4)
pad1.SetLeftMargin(0.15)
pad1.Draw()
pad2 = ROOT.TPad('p2', 'p2',0.0, 0.2, 1.0, 1.0)
pad2.SetBottomMargin(0)
pad2.SetLeftMargin(0.15)
pad2.Draw()
pad2.cd()
rateMetaData = [
    [20, ROOT.kRed],
    [24, ROOT.kRed],
    [21, ROOT.kBlack],
    ]

ii = 0
leg = ROOT.TLegend(0.3, 0.02, 0.86, 0.3)
leg.SetFillColor(0)
leg.SetBorderSize(0)


if options.signalRegion :
    regions = [1,2,3]
else :
    regions = [4,5,6]

for irate in regions :
    rate = rates[irate]
    leg.AddEntry( rate, rate.GetTitle(), 'p')
    rate.SetMarkerStyle( rateMetaData[ii][0] )
    rate.SetMarkerColor( rateMetaData[ii][1] )
    rate.SetLineColor( rateMetaData[ii][1] )
    rate.SetTitle(';;Rate')
    rate.SetTitleSize(30, "XYZ")
    if ii == 0 :
        rate.Draw("")
    else : 
        rate.Draw("same")
    ii += 1
leg.Draw()

tlx2 = ROOT.TLatex()
tlx2.SetNDC()
tlx2.SetTextFont(42)
tlx2.SetTextSize(0.057)
tlx2.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
tlx2.SetTextSize(0.025)
pad1.cd()
if options.signalRegion :
    frac = rates[3].Clone()
    den = rates[2].Clone()
else : 
    frac = rates[6].Clone()
    den = rates[5].Clone()

frac.Divide(den)

frac.UseCurrentStyle()
frac.SetMarkerStyle(20)
frac.SetMarkerSize(1)
frac.SetTitle(';' + xaxis + ';Ratio')
frac.SetTitleSize(20, "XYZ")
frac.Draw("")
frac.Fit('pol0')
frac.SetMinimum(0.8)
frac.SetMaximum(1.2)
frac.GetYaxis().SetNdivisions(2,4,0,False)
frac.SetTitle('')
frac.GetXaxis().SetTitle( frac.GetXaxis().GetTitle() )
csum.cd()
pad1.SetLogx()
pad2.SetLogx()
csum.Update()
