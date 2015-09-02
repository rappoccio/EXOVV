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

parser.add_option('--mcname', type='string', action='store',
                  dest='mcname',
                  default = '',
                  help='String to append to MC names')

parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht",
                  help='Output string for output file')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")


#### Data

f = ROOT.TFile(options.file)
trigs = [
#    'HLT_PFJet60',
#    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500' 
    ]

scales = [
    2000, 66, 12, 4, 1, 1, 1
    ]

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
    fmc.append( ROOT.TFile(mcname + options.mcname + '.root') )
    

logy = [ True, False, True, True, True, True, True, True, False, False, False]#,False,False,False,False,False, ]

hists = ['ptAK8', 'yAK8', 'mAK8', 'msoftdropAK8', 'mprunedAK8', 'mtrimmedAK8', 'mfilteredAK8', 'tau21AK8', 'subjetDRAK8', 'jetzAK8']#, 'nhfAK8', 'chfAK8', 'nefAK8', 'cefAK8', 'ncAK8', 'nchAK8']
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
    'AK8 Jet Fragmentation z = min(p_{T}^{i}, p_{T}^{j})/(p_{T}^{i} + p_{T}^{j});z',
    'AK8 Neutral Hadron Energy Fraction;Fraction',
    'AK8 Charged Hadron Energy Fraction;Fraction',
    'AK8 Neutral E+M Energy Fraction;Fraction',
    'AK8 Charged E+M Energy Fraction;Fraction',
    'AK8 N constituents;Fraction',
    'AK8 N charged hadrons;Fraction',
    
    ]
stacks = []
mcstacks = []
canvs = []
legs = []

ROOT.gStyle.SetPadRightMargin(0.15)

for ihist,histname in enumerate(hists):
    stack = ROOT.THStack(histname + '_stack', titles[ihist])
    mcstack = ROOT.THStack(histname + '_mcstack', titles[ihist])
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    for imc,mc in enumerate(fmc) :
        hist = mc.Get( histname )
        hist.Scale( mcscales[imc] )
        mcstack.Add( hist)
        
    for itrig,trigname in enumerate(trigs) :
        s = trigname + '_' + histname
        print 'Getting ' + s
        hist = f.Get( s )
        hist.SetMarkerStyle(20)
        hist.Scale( scales[itrig] )
        stack.Add( hist )
        leg.AddEntry( hist, trigname, 'f')
    mcstack.GetStack().Last().Draw('hist')
    stack.GetStack().Last().Draw('e same')
    
    if logy[ihist] : 
        canv.SetLogy()
        stack.SetMinimum(0.1)
    #leg.Draw()
    canv.Update()
    canvs.append(canv)
    stacks.append(stack)
    mcstacks.append( mcstack )
    legs.append(leg)
    canv.Print( 'jetplots_' + histname + options.outname + '.png', 'png')
    canv.Print( 'jetplots_' + histname + options.outname + '.pdf', 'pdf')
