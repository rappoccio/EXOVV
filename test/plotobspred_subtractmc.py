#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()


parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = "pred_mvv",
                  help='Input ttbar MC file, without the .root')


parser.add_option('--blind', action = 'store_true',
                  dest='blind',
                  default = False,
                  help='Blind data?')

parser.add_option('--isZ', action = 'store_true',
                  dest='isZ',
                  default = False,
                  help='Is this the Z channel?')


parser.add_option('--outstr', type='string', action='store',
                  dest='outstr',
                  default = None,
                  help='Output string')


parser.add_option('--fileData', type='string', action='store',
                  dest='fileData',
                  default = None,
                  help='Input data file, without the .root')


parser.add_option('--fileTTbar', type='string', action='store',
                  dest='fileTTbar',
                  default = None,
                  help='Input ttbar MC file, without the .root')


parser.add_option('--fileWJets', type='string', action='store',
                  dest='fileWJets',
                  default = None,
                  help='Input ttbar MC file, without the .root')




(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(42)
tlx.SetTextSize(0.057)


ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetOptFit(0000)
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

isMC = False
if options.fileData == None :
    isMC = True
    f = ROOT.TFile(options.fileWJets + '.root')
else :
    isMC = False
    f = ROOT.TFile(options.fileData + '.root')
    
fttbar = ROOT.TFile(options.fileTTbar + '.root')


hobs = f.Get(options.hist)
hpred= f.Get(options.hist + "_pred")

hobs_ttbar = fttbar.Get(options.hist)
hpred_ttbar= fttbar.Get(options.hist + "_pred")

xaxes = {
    "pred_mvv":[0.,6000.],
    "pred_mvvmod":[0.,6000.],
    "pred_jet_pt":[0.,5000.],
    "pred_sdmass":[0.,500.],
    "pred_jetmass":[0.,500.],
    "pred_jetmassmod":[0.,500.],
    "pred_sdrho":[0.,1.],
    }

xaxis = xaxes[options.hist]
    
lumi = 2110

ttbar_norm = 861.57 * lumi / 96834559.

hobs_ttbar.Scale( ttbar_norm )
hpred_ttbar.Scale( ttbar_norm )

if isMC :
#    hobs.Scale( 31.2749 * lumi / 1229879. )
#    hpred.Scale( 31.2749 * lumi / 1229879.  )
    hobs.Scale( lumi * 1.21 )
    hpred.Scale( lumi * 1.21 )

    
# subtract off weighted ttbar pretags, add in observed ttbar
hpred.Add( hpred_ttbar, -1.0 )
hpred.Add( hobs_ttbar )



canv = ROOT.TCanvas('c1','c1', 800, 700)
canv.cd()
pad1 = ROOT.TPad('p1', 'p1', 0.,2./7.,1.0,1.0)
pad1.SetBottomMargin(0.)
pad2 = ROOT.TPad('p1', 'p1', 0.,0.,1.0,2./7.)
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.4)
pad1.Draw()
pad2.Draw()

pad1.cd()
hobs.SetMarkerStyle(20)

hobs_ttbar.SetFillColor(ROOT.kGreen)
if options.isZ == False : 
    hpred.SetFillColor(ROOT.kRed)
else :
    hpred.SetFillColor(ROOT.kBlue-7)
#hpred.SetLineColor(2)
#hpred.SetMarkerColor(2)
#hpred.SetMarkerStyle(24)

hpredclone = hpred.Clone()
hpredclone.SetName("hpredclone")
hpredclone.SetFillColor(1)
hpredclone.SetFillStyle(3004)
hpredclone.SetMarkerStyle(0)

hobs_ttbar.SetMarkerStyle(0)

hs = ROOT.THStack('hs', ';m_{VV} (GeV);Number')
hs.Add( hobs_ttbar )
hs.Add( hpred )

hserrs = ROOT.THStack('hserrs', ';m_{VV} (GeV);Number')
hserrs.Add( hobs_ttbar, "hist")
hserrs.Add( hpredclone, "e3")

hs.Draw("hist")
hserrs.Draw("same")
if not options.blind : 
    hobs.Draw("same")
hs.Draw("axis same")
hs.GetYaxis().SetTitleOffset(1.0)
hs.GetXaxis().SetRangeUser( xaxis[0], xaxis[1])

hs.SetMinimum(1e-3)

eobs_1500 = ROOT.Double(0.)
nobs_1500 = hobs.IntegralAndError( hobs.GetXaxis().FindBin(1500.), hobs.GetXaxis().FindBin(2000.), eobs_1500 )
ebkg_1500 = ROOT.Double(0.)
nbkg_1500 = hs.GetStack().Last().IntegralAndError( hs.GetStack().Last().GetXaxis().FindBin(1500.), hs.GetStack().Last().GetXaxis().FindBin(2000.), ebkg_1500 )

print 'Expected background  1500-2000 : %6.2f +- %6.2f' % ( nbkg_1500, ebkg_1500)
print 'Observed             1500-2000 : %6.2f +- %6.2f' % ( nobs_1500, eobs_1500 )

leg = ROOT.TLegend(0.6,0.6,0.8,0.8)
if not isMC : 
    leg.AddEntry( hobs, 'Data', 'p')
else :
    leg.AddEntry( hobs, 'Observed MC', 'p')
if options.isZ == False :
    leg.AddEntry( hpred, 'Predicted W+Jets', 'f')
else :
    leg.AddEntry( hpred, 'Predicted Z+Jets', 'f')
leg.AddEntry( hobs_ttbar, 't#bar{t} MC', 'f')

leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.Draw()
ROOT.gPad.SetLogy()

tlx.DrawLatex(0.131, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
    

ratio = hobs.Clone()
ratio.SetName('ratio')
ratio.Divide( hs.GetHists().Last() )
ratio.GetXaxis().SetRangeUser( xaxis[0], xaxis[1])
ratio.UseCurrentStyle()
ratio.SetFillStyle(3004)
ratio.SetFillColor(1)

pad2.cd()

ratio.SetMarkerStyle(1)
ratio.SetMarkerSize(0)
ratio.SetTitle(';' + hs.GetXaxis().GetTitle() + ';Ratio')


ratio.SetMinimum(0.)
ratio.SetMaximum(2.)
ratio.GetYaxis().SetNdivisions(2,4,0,False)
#fit = ROOT.TF1("fit", "pol1", 500, 3000)
if not options.blind : 
    ratio.Draw('e3')
#    if isMC : 
#        ratio.Fit("fit", "LRM")
else :
    ratio.Draw("axis")
ratio.GetYaxis().SetTitleOffset(1.0)
ratio.GetXaxis().SetTitleOffset(3.0)
#ratio.SetTitleSize(20, "XYZ")

canv.cd()
canv.Update()


outstr = ''
if options.outstr != None :
    outstr = options.outstr
else :
    if not isMC :
        outstr = options.fileData
    else :
        outstr = options.fileWJets
        
canv.Print(outstr + '_obspred.pdf', 'pdf')
canv.Print(outstr + '_obspred.png', 'png')

