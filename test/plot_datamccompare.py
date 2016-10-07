
#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'jetht.root',
                  help='Input file')

parser.add_option('--mcfile', type='string', action='store',
                  dest='mcfile',
                  default = '',
                  help='MC file')

parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht",
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
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(25,"XYZ")
ROOT.gStyle.SetTitleOffset(1.2, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")


#### Data
f = ROOT.TFile(options.file)



#Assuming MC File is already stitched together
fmc = ROOT.TFile( options.mcfile )




logy =  [ True,       False,      True,       True,         True,           False,          True ]
hists = ['h_pt_meas', 'h_y_meas', 'h_m_meas', 'h_msd_meas', 'h_tau21_meas', 'h_dphi_meas', 'h_ptasym_meas']



## titles = [
##     'AK8 p_{T};p_{T} (GeV)',
##     'AK8 Rapidity;y',
##     'AK8 ungroomed mass;Mass (GeV)',
##     'AK8 soft-drop mass, z_{cut}=0.1, #beta=0;Mass (GeV)',
##     'AK8 pruned mass;Mass (GeV)',
##     'AK8 trimmed mass;Mass (GeV)',
##     'AK8 filtered mass;Mass (GeV)',
##     'AK8 #tau_{21} = #tau_{2} / #tau_{1};#tau_{21}',
##     'AK8 #Delta R between subjets;#Delta R',
##     'AK8 Jet Fragmentation z = min(p_{T}^{i}, p_{T}^{j})/(p_{T}^{i} + p_{T}^{j});z',
##     'AK8 Neutral Hadron Energy Fraction;Fraction',
##     'AK8 Charged Hadron Energy Fraction;Fraction',
##     'AK8 Neutral E+M Energy Fraction;Fraction',
##     'AK8 Charged E+M Energy Fraction;Fraction',
##     'AK8 N constituents;Fraction',
##     'AK8 N charged hadrons;Fraction',
    
##     ]
datahists = []
mchists = []
ratios = []
canvs = []
legs = []
pads = []

ROOT.gStyle.SetPadRightMargin(0.15)

tlxs = []

resultbinwidths = [1., 4., 5., 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]

ptbins = ['#bf{p_{T} 200-260 GeV}','#bf{p_{T} 260-350 GeV}','#bf{p_{T} 350-460 GeV}','#bf{p_{T} 460-550 GeV}','#bf{p_{T} 550-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} 760-900 GeV}', '#bf{p_{T} 900-1000 GeV}', '#bf{p_{T} 1000-1100 GeV}','#bf{p_{T} 1100-1200 GeV}',
 '#bf{p_{T} 1200-1300 GeV}', '#bf{p_{T} > 1300 GeV}']



for ihist,histname in enumerate(hists):
    
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv', 800, 700)
    canv.SetBottomMargin(0.0)
    pad0 = ROOT.TPad( histname  + '_pad0', 'pad0', 0.0, 2./7., 1.0, 1.0 )
    pad1 = ROOT.TPad( histname  + '_pad1', 'pad1', 0.0, 0.0, 1.0, 2./7. )
    pads.append( [pad0,pad1] )
    pad0.SetBottomMargin(0.)
    pad1.SetTopMargin(0.)
    pad1.SetBottomMargin(0.4)
    pad0.Draw()
    pad1.Draw()
        
    pad0.cd()
    if ihist ==2 or ihist ==3:
        pad0.SetLogx()
    if ihist ==4:
        leg = ROOT.TLegend(0.61, 0.47, 0.70, 0.58)
    else:
        leg = ROOT.TLegend(0.71, 0.67, 0.80, 0.78)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    mchist = fmc.Get( histname )
#if ihist ==2 or ihist ==3:
        #    for ibin in xrange(1, mchist.GetNbinsX()+1):
        #    mchist.SetBinContent(ibin, mchist.GetBinContent(ibin) * 1./resultbinwidths[ibin-1])
        #    mchist.SetBinError(ibin, mchist.GetBinError(ibin) * 1./resultbinwidths[ibin-1])
        
    mchist.Sumw2()
    mchist.SetLineColor(1)
    if options.rebin != None :
        mchist.Rebin( options.rebin )
    leg.AddEntry(mchist, 'Pythia8', 'l')
    mchists.append( mchist )
            
    datahist = f.Get( histname )
#if ihist == 2 or ihist == 3:
        # for ibin in xrange(1, datahist.GetNbinsX()+1):
        #    datahist.SetBinContent(ibin, datahist.GetBinContent(ibin) * 1./resultbinwidths[ibin-1])
        #    datahist.SetBinError(ibin, datahist.GetBinError(ibin) * 1./resultbinwidths[ibin-1])
    datahist.Sumw2()
    datahist.SetMarkerStyle(20)
    #datahist.SetMarkerSize(12)
    if options.rebin != None :
        datahist.Rebin( options.rebin )
    leg.AddEntry(datahist, 'Data', 'p')
    datahists.append( datahist )

    mchist.Scale( datahist.Integral() / mchist.Integral() )
    datahist.GetXaxis().SetRangeUser(0.00, 1000000000.0)
    datahist.GetYaxis().SetTitle("Events per Bin")
    mchist.GetXaxis().SetRangeUser(0.00, 1000000000.0)
    datahist.Draw('e')

    mchist.Draw('hist same')
    datahist.Draw('e same')
    datahist.UseCurrentStyle()
    if ihist == 1 or ihist == 5:
        datahist.GetYaxis().SetLabelSize(15)
    mchist.UseCurrentStyle()
    datahist.GetXaxis().SetRangeUser(0.00, 1000000000.0)
    mchist.GetXaxis().SetRangeUser(0.00, 1000000000.0)
    mchist.Draw('hist same')
    datahist.Draw('e same')

    if logy[ihist] :
        pad0.SetLogy()
        datahist.SetMinimum(0.1)
    leg.Draw()
    canv.Update()
    canvs.append(canv)
    legs.append(leg)

    tlx = ROOT.TLatex()
    tlx.SetNDC()
    tlx.SetTextFont(43)
    tlx.SetTextSize(30)
    tlx.DrawLatex(0.35, 0.910, "CMS preliminary, 2.3 fb^{-1} (13 TeV)")
        
    pad1.cd()
    if ihist ==2 or ihist ==3:
        pad1.SetLogx()
    iratio = mchist.Clone()
    iratio.SetName( 'iratio_' + histname )
    iratio.GetYaxis().SetTitle('Pythia 8/Data')
    iratio.Divide( datahist )
    iratio.Draw('e')
    iratio.SetMinimum(0.0)
    iratio.SetMaximum(2.0)
    iratio.GetXaxis().SetRangeUser(0.00, 1000000000.0)
    iratio.GetYaxis().SetNdivisions(2,4,0,False)
    iratio.GetYaxis().SetTitleOffset(1.0)
    iratio.GetXaxis().SetTitleOffset(3.5)
    ratios.append(iratio)
    canv.cd()



    
    canv.Update()
    canv.Print( 'jetplots_' + histname + options.outname + '.png', 'png')
    canv.Print( 'jetplots_' + histname + options.outname + '.pdf', 'pdf')
