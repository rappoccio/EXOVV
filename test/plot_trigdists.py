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


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht",
                  help='Output string for output file')

parser.add_option('--dir', type='string', action='store',
                  dest='dir',
                  default = "",
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


f = ROOT.TFile(options.file)
trigs = [
#    'HLT_PFJet60',
#    'HLT_PFJet80',
#    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500' 
    ]

scales = [
    #66, 12, 4, 1, 1, 1
    66, 6, 3, 2, 1, 1
    ]
colors = [ #ROOT.kRed + 1,
            ROOT.kWhite, ROOT.kRed - 10, ROOT.kRed - 9, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed, ROOT.kRed + 1,    ]

logy = [ True, True, False, True, True, True, True, True, True, False, False ]
palette = [0, 2]


hists = ['pt0', 'ptAK8', 'yAK8', 'mAK8', 'msoftdropAK8', 'mprunedAK8', 'mtrimmedAK8', 'mfilteredAK8', 'tau21AK8', 'subjetDRAK8', 'jetzAK8']
titles = [
    'Leading AK4 p_{T};p_{T} (GeV)',
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
    stack = ROOT.THStack(histname + '_stack', titles[ihist])
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)    
    for itrig,trigname in enumerate(trigs) :
        s = trigname + '_' + histname
        print 'Getting ' + s
        hist = f.Get( s )
        hist.SetFillColor( colors[itrig] )
        if options.rebin != None :
            hist.Rebin( options.rebin )
        hist.Scale( scales[itrig] )
        stack.Add( hist )
        leg.AddEntry( hist, trigname, 'f')
    stack.Draw('hist')
    if logy[ihist] : 
        canv.SetLogy()
        stack.SetMinimum(0.1)
    leg.Draw()
    canv.Update()
    canvs.append(canv)
    stacks.append(stack)
    legs.append(leg)
    canv.Print( 'trigplots_' + histname + '.png', 'png')
    canv.Print( 'trigplots_' + histname + '.pdf', 'pdf')
