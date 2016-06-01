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


#### Data
f = ROOT.TFile(options.file)

#Assuming MC File is already stitched together
fmc = ROOT.TFile( options.mcfile )


logy = [ True, False, True, True, True, True, True, True, False, False, False,False,False,False,False,False, ]

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

for ihist,histname in enumerate(hists):
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    canv.SetBottomMargin(0.0)
    pad0 = ROOT.TPad( histname + '_pad0', 'pad0', 0.0, 0.2, 1.0, 1.0 )
    pad1 = ROOT.TPad( histname + '_pad1', 'pad1', 0.0, 0.0, 1.0, 0.2 )
    pads.append( [pad0,pad1] )
    pad0.Draw()
    pad1.Draw()
    
    pad0.cd()
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    mchist = fmc.Get( histname )
    mchist.Sumw2()
    if options.rebin != None :
        mchist.Rebin( options.rebin )
    mchists.append( mchist )


    datahist = f.Get( histname )
    datahist.Sumw2()
    if options.rebin != None :
        datahist.Rebin( options.rebin )
    datahists.append( datahist )
        

            

    datahist.Draw('e')
    mchist.Draw('hist same')
    datahist.Draw('e')

    
    if logy[ihist] : 
        canv.SetLogy()
        datahist.SetMinimum(0.1)
    #leg.Draw()
    canv.Update()
    canvs.append(canv)
    legs.append(leg)

    
    pad1.cd()
    iratio = mchist.Clone()
    iratio.SetName( 'iratio_' + histname )
    iratio.Divide( datahist )
    iratio.Draw('e')
    iratio.SetMinimum(0.0)
    iratio.SetMaximum(2.0)
    ratios.append(iratio)
    canv.cd()
    canv.Update()
    canv.Print( 'jetplots_' + histname + options.outname + '.png', 'png')
    canv.Print( 'jetplots_' + histname + options.outname + '.pdf', 'pdf')
