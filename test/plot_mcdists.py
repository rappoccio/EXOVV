#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--mcname', type='string', action='store',
                  dest='mcname',
                  default = '',
                  help='String to append to MC names')

parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht",
                  help='Output string for output file')


parser.add_option('--dir', type='string', action='store',
                  dest='dir',
                  default = "hists",
                  help='Directory containing root histograms')


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


#### MC
fmcNames = [
    'qcd_pt170to300',
    'qcd_pt300to470',
    'qcd_pt470to600',
    'qcd_pt600to800',
    'qcd_pt800to1000',
    'qcd_pt1000to1400',
    'qcd_pt1400to1800',
    'qcd_pt1800to2400',
    'qcd_pt2400to3200',
    'qcd_pt3200toInf',
]

lumi = 40.03 # pb-1

mcscales = [
    #xs / nevents * lumi
     117276. / 3468514. * lumi,
     7823 / 2936644. * lumi,
     648.2 / 1971800. * lumi,
     186.9 / 1981608. * lumi,
     32.293 / 1990208. * lumi,
     9.4183 / 1487712. * lumi,
     0.84265 / 197959. * lumi,
     0.114943 / 194924. * lumi,
     0.00682981 / 198383. * lumi,
     0.000165445 / 194528. * lumi
    ]

fmc = []
for imc,mcname in enumerate(fmcNames) :
    fmc.append( ROOT.TFile(options.dir + '/' + mcname + options.mcname + '.root') )
    


colors = [ 
            ROOT.kWhite,ROOT.kBlue - 10, ROOT.kBlue - 9, ROOT.kBlue - 7, ROOT.kBlue - 4, ROOT.kBlue,ROOT.kBlue +1,ROOT.kBlue +2, ROOT.kBlue +3, ROOT.kBlue+4     ]

logy = [ True, False, True, True, True, True, True, True, False, False ]
palette = [0, 2]


hists = ['ptAK8', 'yAK8', 'mAK8', 'msoftdropAK8', 'mprunedAK8', 'mtrimmedAK8', 'mfilteredAK8', 'tau21AK8', 'subjetDRAK8', 'jetzAK8']
titles = [
    'AK8 p_{T};p_{T} (GeV)',
    'AK8 Rapidity;y',
    'AK8 ungroomed mass;Mass (GeV)',
    'AK8 soft-drop mass, z_{cut}=0.1, #beta=0;Mass (GeV)',
    'AK8 pruned mass;Mass (GeV)',
    'AK8 trimmed mass;Mass (GeV)',
    'AK8 filtered mass;Mass (GeV)',
    'AK8 #tau_{21} = #tau_{2} / #tau_{1};#tau_{21}',
    'AK8 #Delta R between subjets;#Delta R',
    'AK8 Jet Fragmentation z = min(p_{T}^{i}, p_{T}^{j})/(p_{T}^{i} + p_{T}^{j});z'
    ]
stacks = []
canvs = []
legs = []

ROOT.gStyle.SetPadRightMargin(0.15)

for ihist,histname in enumerate(hists):

    mcstack = ROOT.THStack(histname + '_mcstack', titles[ihist])
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    for imc,mc in enumerate(fmc) :
        hist = mc.Get( histname )
        if options.rebin != None :
            hist.Rebin( options.rebin ) 
        hist.Scale( mcscales[imc] )
        hist.SetFillColor( colors[imc] )
        mcstack.Add( hist)
        leg.AddEntry( hist, fmcNames[imc], 'f')
    mcstack.Draw('hist')
    if logy[ihist] : 
        canv.SetLogy()
        mcstack.SetMinimum(0.1)
    leg.Draw()
    canv.Update()
    canvs.append(canv)
    stacks.append(mcstack)
    legs.append(leg)
    canv.Print( 'mcplots_' + histname + options.mcname + '.png', 'png')
    canv.Print( 'mcplots_' + histname + options.mcname + '.pdf', 'pdf')
