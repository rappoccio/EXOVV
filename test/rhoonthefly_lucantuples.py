#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "nom",
                  help='Label for plots')

parser.add_option('--weight', type='string', action='store',
                  dest='weight',
                  default = "wSampleWeight",
                  help='Weight for MC samples')

parser.add_option('--signalRegion', action='store_true',
                  dest='signalRegion',
                  default = False,
                  help='Plot signal region?')


parser.add_option('--hackedRho', action='store_true',
                  dest='hackedRho',
                  default = False,
                  help='Use hacked rho, softdrop mass, ungroomed pt')


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

weight = '*(' + options.weight + ')'

datasIn = [
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_el/WWTree_data.root' ),
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_mu/WWTree_data.root' ),
    ]

wjetsIn =[
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_el/WWTree_WJets.root' ),
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_mu/WWTree_WJets.root' ),
    ]

ttbarsIn = [
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_el/WWTree_TTbar.root' ),
    ROOT.TFile( '/data/EXOVV/WWTree_12nov_jecV6/WWTree_mu/WWTree_TTbar.root' ),
    ]

dataTrees = []
wjetsTrees = []
ttbarTrees = []
# Append the actual TTrees
for idata in range(0,len(datasIn)) :
    dataTrees.append( datasIn[idata].Get("otree") )
for iw in range(0,len(wjetsIn)) :
    wjetsTrees.append( wjetsIn[iw].Get("otree") )
for ittbar in range(0,len(ttbarsIn)) :
    ttbarTrees.append( ttbarsIn[ittbar].Get("otree") )



xaxis = '#rho = (m/p_{T}R)^{2}'
variable = '(jet_mass_so/(jet_pt_so*0.8))**2'
histbins = '(30,0.0,0.3)'


plotsToMake = [
    # name                        title                                                taucut mmin   mmax    ptmin ptmax   mstyle
    ['pt200toInf_m0toInf_tau10',  'p_{T} > 200 GeV',                                    1.0,   0.,    13000., 200., 13000., 20],
    ['pt200toInf_m0toInf_tau06',  'p_{T} > 200 GeV',                                    0.6,   0.,    13000., 200., 13000., 24],#0
    ## ['pt200to350_m50toInf_tau10', '200 < p_{T} < 350 GeV, m > 50 GeV',                  1.0,  50.,    13000., 200., 350.,   20],
    ## ['pt200to350_m50toInf_tau06', '200 < p_{T} < 350 GeV, m > 50 GeV, #tau_{21} < 0.6', 0.6,  50.,    13000., 200., 350.,   24],#1
    ## ['pt200to350_m28toInf_tau10', '200 < p_{T} < 350 GeV, m > 28 GeV',                  1.0,  28.571, 13000., 200., 350.,   20],
    ## ['pt200to350_m28toInf_tau065','200 < p_{T} < 350 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 13000., 200., 350.,   24],#2
    ## ['pt350toInf_m50toInf_tau10', 'p_{T} > 350 GeV, m > 50 GeV',                        1.0,  50.,    13000., 350., 13000., 20],
    ## ['pt350toInf_m50toInf_tau06', 'p_{T} > 350 GeV, m > 50 GeV, #tau_{21} < 0.6',       0.6,  50.,    13000., 350., 13000., 24],#3
    ## ['pt200to275_m39toInf_tau10', '200 < p_{T} < 275 GeV, m > 39 GeV',                  1.0,  39.286, 13000., 200., 275.,   20],
    ## ['pt200to275_m39toInf_tau06', '200 < p_{T} < 275 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 13000., 200., 275.,   24],#4
    ## ['pt200to275_m28toInf_tau10', '200 < p_{T} < 275 GeV, m > 28 GeV',                  1.0,  28.571, 13000., 200., 275.,   20],
    ## ['pt200to275_m28toInf_tau065','200 < p_{T} < 275 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 13000., 200., 275.,   24],#5
    ## ['pt275to350_m39toInf_tau10', '275 < p_{T} < 350 GeV, m > 39 GeV',                  1.0,  39.286, 13000., 275., 350.,   20],
    ## ['pt275to350_m39toInf_tau06', '275 < p_{T} < 350 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 13000., 275., 350.,   24],#6
    #####
    ['pt200to350_m0toInf_tau10',  '200 < p_{T} < 350 GeV, m > 50 GeV',                  1.0,  50.,    105., 200., 350.,   20],
    ['pt200to350_m50toInf_tau06', '200 < p_{T} < 350 GeV, m > 50 GeV, #tau_{21} < 0.6', 0.6,  50.,    105., 200., 350.,   24],#1
    ['qt200to350_m0toInf_tau10',  '200 < p_{T} < 350 GeV, m > 50 GeV',                  1.0,  28.571, 105., 200., 350.,   20],
    ['pt200to350_m28toInf_tau065','200 < p_{T} < 350 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 105., 200., 350.,   24],#2
    ['pt350toInf_m0toInf_tau10',  'p_{T} > 350 GeV, m > 50 GeV',                        1.0,  50.,    105., 350., 13000., 20],
    ['pt350toInf_m50toInf_tau06', 'p_{T} > 350 GeV, m > 50 GeV, #tau_{21} < 0.6',       0.6,  50.,    105., 350., 13000., 24],#3
    ['pt200to275_m0toInf_tau10',  '200 < p_{T} < 275 GeV, m > 50 GeV',                  1.0,  39.286, 105., 200., 275.,   20],
    ['pt200to275_m39toInf_tau06', '200 < p_{T} < 275 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 105., 200., 275.,   24],#4
    ['qt200to275_m0toInf_tau10',  '200 < p_{T} < 275 GeV, m > 50 GeV',                  1.0,  28.571, 105., 200., 275.,   20],
    ['pt200to275_m28toInf_tau065','200 < p_{T} < 275 GeV, m > 28 GeV, #tau_{21} < 0.65',0.65, 28.571, 105., 200., 275.,   24],#5
    ['pt275to350_m0toInf_tau10',  '275 < p_{T} < 350 GeV, m > 50 GeV',                  1.0,  39.286, 105., 275., 350.,   20],
    ['pt275to350_m39toInf_tau06', '275 < p_{T} < 350 GeV, m > 39 GeV, #tau_{21} < 0.6', 0.6,  39.286, 105., 275., 350.,   24],#6    
    ]
hdatas = []
hwjets = []
httbars = []

rhobins = array.array('d', [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 1.0])
#rhobins = array.array('d', [0.0, 0.0001, 0.1, 1.0])
nrhobins = len(rhobins)-1

for [ name, title, taucut, mMin, mMax, ptMin, ptMax, style ] in plotsToMake :


    cuts = [
        '(l_pt > 120. && pfMET > 80.  && l_pt + pfMET  > 200. && '\
        'ungroomed_jet_pt >= ' + str(ptMin) + '&&'\
        'ungroomed_jet_pt <  ' + str(ptMax) + '&&'\
        'jet_mass_so >= ' + str(mMin) + '&&'\
        'jet_mass_so <  ' + str(mMax) + '&&'\
        'jet_tau2tau1 < ' + str(taucut)  + \
        ')',

        '(l_pt > 55.  && pfMET > 40.  && l_pt + pfMET  > 200. && '\
        'ungroomed_jet_pt >= ' + str(ptMin) + '&&'\
        'ungroomed_jet_pt <  ' + str(ptMax) + '&&'\
        'jet_mass_so >= ' + str(mMin) + '&&'\
        'jet_mass_so <  ' + str(mMax) + '&&'\
        'jet_tau2tau1 < ' + str(taucut) + \
        ')',
    ]

    
    
    idataSum = None
    for idata in dataTrees :
        dataIndex = dataTrees.index(idata)
        
        dataname = name + '_data' + str( dataIndex )
        hdata = ROOT.TH1D(dataname, ';' + xaxis, nrhobins, rhobins )
        
        idata.Draw(variable + " >> " + dataname, cuts[dataIndex], 'goff')
        #hdata = ROOT.gDirectory.Get(dataname)
        #hdata.SetName(dataname)
        #hdata.SetTitle( ';' + xaxis )
        hdata.SetMarkerStyle(style)
        #hdata.Sumw2()        
        if dataIndex == 0 :
            idataSum = hdata.Clone()
        else :
            idataSum.Add( hdata )
    hdatas.append( idataSum)
    


    iwjetSum = None
    for iwjet in wjetsTrees :
        wjetIndex = wjetsTrees.index(iwjet)
        wjetname = name + '_wjet' + str( wjetIndex )
        hwjet = ROOT.TH1D(wjetname, ';' + xaxis, nrhobins, rhobins )
        iwjet.Draw(variable + " >> " + wjetname, cuts[wjetIndex] + weight, 'goff')
        #hwjet = ROOT.gDirectory.Get(wjetname)
        #hwjet.SetName(wjetname)
        #hwjet.SetTitle( ';' + xaxis )
        hwjet.SetMarkerStyle(style)
        #hwjet.Sumw2()
        hwjet.Scale( lumi * 1.21 )
        if wjetIndex == 0 :
            iwjetSum = hwjet.Clone()
        else :
            iwjetSum.Add( hwjet )
    hwjets.append( iwjetSum)

    ittbarSum = None
    for ittbar in ttbarTrees :
        ttbarIndex = ttbarTrees.index(ittbar)
        ttbarname = name + '_ttbar' + str( ttbarIndex )
        httbar = ROOT.TH1D(ttbarname, ';' + xaxis, nrhobins, rhobins )
        ittbar.Draw(variable + " >> " + ttbarname, cuts[ttbarIndex] + weight, 'goff')
        #httbar = ROOT.gDirectory.Get(ttbarname)
        #httbar.SetName(ttbarname)
        #httbar.SetTitle( ';' + xaxis )
        httbar.SetMarkerStyle(style)
        #httbar.Sumw2()
        httbar.Scale( lumi )
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
for ndxToPlot in range(0, len(plotsToMake), 2) : 
    hdata1 = hdatas[ndxToPlot]
    hdata2 = hdatas[ndxToPlot+1]
    hwjet1 = hwjets[ndxToPlot]
    hwjet2 = hwjets[ndxToPlot+1]
    httbar1 = httbars[ndxToPlot]
    httbar2 = httbars[ndxToPlot+1]
    #hdata1.Add( httbar1, -1.0 )
    #hdata2.Add( httbar2, -1.0 )
    #datascale = 1.0 / hdata1.Integral()
    #hdata1.Scale( datascale )
    #hdata2.Scale( datascale )
    #wjetscale = 1.0 / hwjet1.Integral()
    #hwjet1.Scale( wjetscale )
    #hwjet2.Scale( wjetscale )
    nleg = ROOT.TLegend(0.6, 0.5, 0.84, 0.8)
    nleg.SetFillColor(0)
    nleg.SetBorderSize(0)
    hwjet1.SetFillColor( ROOT.kRed )
    hwjet2.SetFillColor( ROOT.kRed + 1)
    hwjet2.SetFillStyle( 3004 )
    httbar1.SetFillColor( ROOT.kGreen )
    httbar2.SetFillColor( ROOT.kGreen + 1)
    httbar2.SetFillStyle(3005)

    hstack1 = ROOT.THStack( hwjet1.GetName() + '_stack1', ';#rho = (m/p_{T}R)^{2};Fraction')
    hstack2 = ROOT.THStack( hwjet2.GetName() + '_stack2', ';#rho = (m/p_{T}R)^{2};Fraction')
    hstack1.Add( httbar1 )
    hstack1.Add( hwjet1 )
    hstack2.Add( httbar2 )
    hstack2.Add( hwjet2 )
    


    hwjet1.SetTitle(';#rho = (m/p_{T}R)^{2};Fraction')
    
    canvname = 'c' + str(ndxToPlot)
    c = ROOT.TCanvas(canvname, canvname)
    c.SetBottomMargin(0.15)
    c.SetLeftMargin(0.15)
    print 'Drawing : '
    print hdata1.GetName()
    print hdata2.GetName()

    
    hstack1.Draw('hist')
    hstack2.Draw('hist same')
    
    hdata1.Draw('e same')
    hdata2.Draw('e same')
    maxscale = max( hstack1.GetMaximum(), hdata1.GetMaximum()) * 1.2
    hstack1.SetMaximum( maxscale )

    hstacks.append( hstack1 )
    hstacks.append( hstack2 )
    
    nleg.AddEntry( hdata1, 'Data, All', 'p')
    nleg.AddEntry( hdata2, 'Data, #tau_{21} < ' + str( plotsToMake[ndxToPlot+1][2] ) , 'p')
    nleg.AddEntry( hwjet1,   'W+Jets, All', 'f')
    nleg.AddEntry( hwjet2,   'W+Jets, #tau_{21} < ' + str( plotsToMake[ndxToPlot+1][2] ) , 'f')
    nleg.AddEntry( httbar1,   't#bar{t}, All', 'f')
    nleg.AddEntry( httbar2,   't#bar{t}, #tau_{21} < ' + str( plotsToMake[ndxToPlot+1][2] ) , 'f')
            
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
    hrate.Add( httbar2, -1.0)
    hden = hdata1.Clone()
    hden.Add( httbar1, -1.0 )
    hrate.SetName( 'rate_' + hdata2.GetName() )
    
    hrate.SetTitle( plotsToMake[ndxToPlot+1][1] )
    hrate.Divide( hrate, hden, ROOT.Double(1), ROOT.Double(1), 'b')
    rates.append( hrate )

    hratewjet = hwjet2.Clone()
    hratewjet.SetFillStyle(0)
    hratewjet.SetName( 'ratewjet_' + hwjet2.GetName() )
    hratewjet.SetTitle( plotsToMake[ndxToPlot+1][1] )
    hratewjet.Divide( hwjet2, hwjet1, ROOT.Double(1), ROOT.Double(1), 'b')
    ratewjets.append( hratewjet )
    
    c.Print( options.outlabel + '_' + hdata2.GetName() + '.png', 'png' )
    c.Print( options.outlabel + '_' + hdata2.GetName() + '.pdf', 'pdf' )



for irate in rates :
    for ibin in range(1,irate.GetNbinsX()) :
        val = irate.GetBinContent(ibin)
        err = 0.
        if abs(val) > 0 : 
            err1 = irate.GetBinError(ibin) / val
            err2 = 0.05
            err = math.sqrt( err1**2 + err2**2) * val
        irate.SetBinError( ibin, err )


for irate in ratewjets :
    for ibin in range(1,irate.GetNbinsX()) :
        val = irate.GetBinContent(ibin)
        err = 0.
        if abs(val) > 0 : 
            err1 = irate.GetBinError(ibin) / val
            err2 = 0.05
            err = math.sqrt( err1**2 + err2**2) * val
        irate.SetBinError( ibin, err )

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
    [24, ROOT.kRed, 2, 3004],
    [20, ROOT.kRed, 1, 3001],
    [21, ROOT.kBlack, 1, 3001],
    ]

ii = 0
leg = ROOT.TLegend(0.17, 0.60, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetNColumns(3)

if options.signalRegion :
    regions = [1,2,3]
else :
    regions = [4,5,6]


closureErrors = []
prediction  = ratewjets[regions[1]]
truth = ratewjets[regions[2]]


# Get the difference in closure in MC, apply that as a systematic in data and MC
for ibin in xrange( 1, truth.GetNbinsX() ) :    
    val = prediction.GetBinContent(ibin)
    err1 = prediction.GetBinError(ibin)
    err2 = abs(prediction.GetBinContent(ibin) - truth.GetBinContent(ibin))
    prediction.SetBinError( ibin, math.sqrt(err1**2 + err2**2) )

    if val > 0.0 : 
        closureErrors.append( math.sqrt(err1**2 + err2**2) / val  )
    else :
        closureErrors.append( 0.0 )


for ival in closureErrors :
    print ' %6.4e' % (ival),
print ''

predictionData = rates[regions[1]]
for ibin in xrange( 1, predictionData.GetNbinsX() ) :
    err1 = predictionData.GetBinError(ibin)
    err2 = closureErrors[ibin-1] * predictionData.GetBinContent(ibin)
    predictionData.SetBinError( ibin, math.sqrt(err1**2 + err2**2) )    

    
for irate in regions :
    rate = rates[irate]
    ratewjet = ratewjets[irate]
    rate.SetMaximum(2)
    rate.SetMinimum(0)
    leg.AddEntry( rate, rate.GetTitle(), '')
    leg.AddEntry( rate, 'Data', 'p')
    rate.SetMarkerStyle( rateMetaData[ii][0] )
    rate.SetMarkerColor( rateMetaData[ii][1] )
    rate.SetLineColor( rateMetaData[ii][1] )
    rate.SetLineStyle( rateMetaData[ii][2] )
    rate.SetTitle(';;Rate')
    rate.SetTitleSize(30, "XYZ")

    
    if ii == 0 :
        rate.Draw("")
    else :
        #if irate != 3 : 
        rate.Draw("same")
    ratewjet.SetMarkerStyle(0)
    ratewjet.SetLineColor( rateMetaData[ii][1] )
    ratewjet.SetFillColor( rateMetaData[ii][1] )
    ratewjet.SetLineStyle( rateMetaData[ii][2] )
    ratewjet.SetFillStyle( rateMetaData[ii][3] )
    
    #ratewjet.SetFillColorAlpha( rateMetaData[ii][1], 0.35 )
    ratewjet.Draw("e3 same")
    leg.AddEntry( ratewjet, 'MC', 'f')
    rate.GetXaxis().SetRangeUser(1e-2,0.3)
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
frac.SetMinimum(0.)
frac.SetMaximum(2.0)
frac.GetYaxis().SetNdivisions(2,4,0,False)
frac.GetXaxis().SetNdivisions(4,8,0,False)

frac.SetTitle('')
frac.GetXaxis().SetTitle( frac.GetXaxis().GetTitle() )
frac.GetXaxis().SetTitleOffset(3.5)
frac.GetXaxis().SetRangeUser(1e-2,0.3)
csum.cd()
pad1.SetLogx()
pad2.SetLogx()
#pad2.SetLogy()

csum.Update()
csum.Print( options.outlabel + '_summary.png', 'png')
csum.Print( options.outlabel + '_summary.pdf', 'pdf')


print 'Writing output ROOT files'
fout = ROOT.TFile( options.outlabel + '_rate.root', 'RECREATE')
toWrite = rates[ regions[1] ].Clone()
toWrite.SetName("rLoMod")
toWriteWJET = ratewjets[ regions[1] ].Clone()
toWriteWJET.SetName("rLoModWJET")
toWrite.Write()
toWriteWJET.Write()
fout.Close()
