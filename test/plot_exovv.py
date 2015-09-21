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


parser.add_option('--dir', type='string', action='store',
                  dest='dir',
                  default = "exovvhists",
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


#### Data

f = ROOT.TFile(options.dir + '/' + options.file)
#trigs = [
#    'HLT_PFJet140',
#    'HLT_PFJet200',
#    'HLT_PFJet260',
#    'HLT_PFJet320',
#    'HLT_PFJet400',
#    'HLT_PFJet450',
#    'HLT_PFJet500' 
#    ]

#scales = [
#    2000, 66, 12, 4, 1, 1, 1
#    ]

#### MC
fmcNames = [
    'exovv_qcd_pt170to300',
    'exovv_qcd_pt300to470',
    'exovv_qcd_pt470to600',
    'exovv_qcd_pt600to800',
    'exovv_qcd_pt800to1000',
    'exovv_qcd_pt1000to1400',
    'exovv_qcd_pt1400to1800',
    'exovv_qcd_pt1800to2400',
    'exovv_qcd_pt2400to3200',
    'exovv_qcd_pt3200toInf',
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

mcstacks = []
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
        # I'm an idiot and named the trigger histograms differently from the MC ones
        if 'nhfAK8' in histname or 'chfAK8' in histname or 'nefAK8' in histname or 'cefAK8' in histname or 'ncAK8' in histname or 'nchAK8' in histname :            
            hist = mc.Get( 'h_' + histname )
        else :
            hist = mc.Get( histname )
        print 'Getting MC : ' + histname
        if options.rebin != None :
            hist.Rebin( options.rebin )
        hist.Scale( mcscales[imc] )
        mcstack.Add( hist)
        

    s = histname
    print 'Getting ' + s
    hist = f.Get( s )
    hist.SetMarkerStyle(20)
    if options.rebin != None :
        hist.Rebin( options.rebin )

    hist.Draw('e')
    mcstack.GetStack().Last().Draw('hist same')
    hist.Draw('e same')

    
    if logy[ihist] : 
        canv.SetLogy()
        hist.SetMinimum(0.1)
    #leg.Draw()
    canv.Update()
    canvs.append(canv)
    mcstacks.append( mcstack )
    legs.append(leg)
    canv.Print( 'exovvplots_' + histname + options.outname + '.png', 'png')
    canv.Print( 'exovvplots_' + histname + options.outname + '.pdf', 'pdf')
