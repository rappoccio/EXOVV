#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "controplots",
                  help='Label for plots')


parser.add_option('--variable', type='string', action='store',
                  dest='variable',
                  default = "FatJetRhoRatio",
                  help='Variable to plot')


parser.add_option('--cut', type='string', action='store',
                  dest='cut',
                  default = 'FatJetPt[0] > 240',
                  help='Variable to plot')


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
#ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

lumi = 1263.88


dataIn = ROOT.TFile( 'exovv_wv_v74x_v6_dataset6_ntuple.root' )
data = dataIn.Get("TreeEXOVV")

wjetsIn =[
    [ ROOT.TFile( 'exovv_wjets_ht200to400_ntuple.root' ), 471.6/4936077. * lumi  / 1.95 ],
    [ ROOT.TFile( 'exovv_wjets_ht400to600_ntuple.root' ), 55.61/4640594. * lumi  / 1.94 ],
    [ ROOT.TFile( 'exovv_wjets_ht600toInf_ntuple.root' ), 18.81/4581841. * lumi  / 1.96 ]
]

ttbarsIn = [
    [ ROOT.TFile( 'exovv_ttbar_v74x_v6_ntuple.root' ), 831.76 / 19665194. * lumi / 0.98 ]
    ]

# Append the actual TTree to the end of the list
for iw in range(0,len(wjetsIn)) :
    wjetsIn[iw].append( wjetsIn[iw][0].Get("TreeEXOVV") )
for ittbar in range(0,len(ttbarsIn)) :
    ttbarsIn[ittbar].append( ttbarsIn[ittbar][0].Get("TreeEXOVV") )



variables = {
    'FatJetRhoRatio':[';#rho = (m/p_{T}R)^{2}','(100,0.0,1.0)'],
    'FatJetPt':[';Jet p_{T} (GeV)','(100,0.0,1000)'],
    'FatJetTau21':[';Jet #tau_{21}','(100,0.0,1.0)'],
    'LeptonPt':[';Lepton p_{T} (GeV)','(100,0.0,1000)'],
    }

variable = options.variable
xaxis = variables[variable][0]
histbins = variables[variable][1]
name = options.variable

hdatas = []
hwjets = []
httbars = []


cut = '(' + \
  '( (LeptonType[0] == 0 && LeptonPt[0] > 120. && METpt > 80.) || (LeptonType[0] == 1 && LeptonPt[0] > 55. && METpt > 40.) )  && ' + \
  'VlepPt[0] > 200. && ' + \
  'LeptonIso[0] / LeptonPt[0] < 0.10 && LeptonIso[0] < 20. &&' \
  'TMath::Sqrt(TMath::Power(FatJetEta[0]-LeptonEta[0],2)+TMath::Power(TVector2::Phi_0_2pi(FatJetPhi[0]-LeptonPhi[0]),2)) > TMath::PiOver2() &&' + \
  'TVector2::Phi_0_2pi( FatJetPhi[0] - METphi[0]) > TMath::PiOver2() &&' + \
  'TVector2::Phi_0_2pi( FatJetPhi[0] - VlepPhi[0]) > TMath::PiOver2() &&' + \
  'MaxBDisc < 0.6 &&' + \
  options.cut + \
  ')'

trig = '&& ((LeptonType[0] == 0 && Trig >= 7 ) || (LeptonType[0] == 1 && Trig <= 2))'

weightstr = '*(Weight)'

#'FatJetTau21[0] < ' + str(taucut) +  '&&' \
#'FatJetMassSoftDrop[0] > ' + str(mMin) + '&&' + \
#'FatJetMassSoftDrop[0] <= ' + str(mMax) + '&&' + \
#'FatJetPt[0] > ' + str(ptMin) + '&&' + \
#'FatJetPt[0] <= ' + str(ptMax) + '&&' \




style = 20

data.Draw(variable + " >> " + name + histbins, cut + trig, 'goff')
hdata = ROOT.gDirectory.Get(name)
hdata.SetName(name)
hdata.SetTitle( ';' + xaxis )
hdata.SetMarkerStyle(style)
hdata.Sumw2()
hdatas.append(hdata)

iwjetSum = None
for iwjet in wjetsIn :
    wjetIndex = wjetsIn.index(iwjet)
    wjetname = name + '_wjet' + str( wjetIndex )

    iwjet[2].Draw(variable + " >> " + wjetname + histbins, cut + weightstr, 'goff')
    hwjet = ROOT.gDirectory.Get(wjetname)
    hwjet.SetName(wjetname)
    hwjet.SetTitle( ';' + xaxis )
    hwjet.SetMarkerStyle(style)
    hwjet.Sumw2()
    hwjet.Scale( iwjet[1] )
    if wjetIndex == 0 :
        iwjetSum = hwjet.Clone()
    else :
        iwjetSum.Add( hwjet )
hwjets.append( iwjetSum)

ittbarSum = None
for ittbar in ttbarsIn :
    ttbarIndex = ttbarsIn.index(ittbar)
    ttbarname = name + '_ttbar' + str( ttbarIndex )

    ittbar[2].Draw(variable + " >> " + ttbarname + histbins, cut + weightstr, 'goff')
    httbar = ROOT.gDirectory.Get(ttbarname)
    httbar.SetName(ttbarname)
    httbar.SetTitle( ';' + xaxis )
    httbar.SetMarkerStyle(style)
    httbar.Sumw2()
    httbar.Scale( ittbar[1] )
    if ttbarIndex == 0 :
        ittbarSum = httbar.Clone()
    else :
        ittbarSum.Add( httbar )
httbars.append( ittbarSum)



canvs = []
rates = []
ratewjets = []
hstacks = []
nlegs = []
ndxToPlot = 0
hdata1 = hdatas[ndxToPlot]
hwjet1 = hwjets[ndxToPlot]
httbar1 = httbars[ndxToPlot]
nleg = ROOT.TLegend(0.6, 0.5, 0.84, 0.8)
nleg.SetFillColor(0)
nleg.SetBorderSize(0)
hwjet1.SetFillColor( ROOT.kRed )
httbar1.SetFillColor( ROOT.kGreen )

hstack1 = ROOT.THStack( hwjet1.GetName() + '_stack1', xaxis)
hstack1.Add( httbar1 )
hstack1.Add( hwjet1 )



hwjet1.SetTitle(';#rho = (m/p_{T}R)^{2};Fraction')

canvname = 'c' + str(ndxToPlot)
c = ROOT.TCanvas(canvname, canvname)
c.SetBottomMargin(0.15)
c.SetLeftMargin(0.15)
print 'Drawing : '
print hdata1.GetName()


hstack1.Draw('hist')

hdata1.Draw('e same')
maxscale = max( hstack1.GetMaximum(), hdata1.GetMaximum()) * 1.2
hstack1.SetMaximum( maxscale )

hstacks.append( hstack1 )


nleg.AddEntry( hdata1, 'Data', 'p')
nleg.AddEntry( hwjet1,   'W+Jets', 'f')
nleg.AddEntry( httbar1,   't#bar{t}', 'f')

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
#tlxm.DrawLatex(0.4, 0.81, plotsToMake[ndxToPlot][1])
tlxm.SetTextSize(0.025)    

#c.SetLogx()
c.Update()

canvs.append(c)

