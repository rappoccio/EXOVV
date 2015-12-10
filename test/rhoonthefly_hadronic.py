#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "rho_plots",
                  help='Label for plots')


parser.add_option('--isData', action='store_true',
                  dest='isData',
                  default = False,
                  help='Is data?')

parser.add_option('--ptMin', type='float', action='store',
                  dest='ptMin',
                  default = 200.,
                  help='Minimum pt')

parser.add_option('--ptMax', type='float', action='store',
                  dest='ptMax',
                  default = None,
                  help='Maximum pt')

parser.add_option('--massMin', type='float', action='store',
                  dest='massMin',
                  default = 0.,
                  help='Minimum mass')

parser.add_option('--massMax', type='float', action='store',
                  dest='massMax',
                  default = None,
                  help='Maximum mass')

parser.add_option('--tauCut', type='float', action='store',
                  dest='tauCut',
                  default = 0.6,
                  help='Tau Cut')


parser.add_option('--maxEvents', type='int', action='store',
                  dest='maxEvents',
                  default = None,
                  help='Max events')


(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math
import random

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

lumi = 2100


# QCD MC is actually 50 ns, need to fix this
qcdIn =[
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt170to300_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt300to470_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt470to600_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt600to800_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt800to1000_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt1000to1400_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt1400to1800_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt1800to2400_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt2400to3200_tree.root'),
    ROOT.TFile('/data/EXOVV/QCDTree/exovv_qcd_pt3200toInf_tree.root'),
    ]

qcdWeights =[
    0.033811597704377146,
    0.0026639252153138073,
    0.0003287351658383203,
    9.431734227960323e-05,
    1.6225942213075215e-05,
    6.3307279903637264e-06,
    4.256689516516046e-06,
    5.896811064825265e-07,
    3.4427395492557326e-08,
    8.504945303503866e-10
        ]

datasIn = [
    ROOT.TFile('/data/EXOVV/QCDTree/JetHT_Run2015D_B2GAnaFW_v74x_V8p4_25ns_Nov13silverJSON.root')
    ]



## HLT_PFHT200_v2	201.964	12.5688
## HLT_PFHT250_v2	202.346	12.5450
## HLT_PFHT300_v2	203.492	12.4744
## HLT_PFHT350_v3	214.185	11.8516
## HLT_PFHT400_v2	220.677	11.5029
## HLT_PFHT475_v2	240.154	10.5700
## HLT_PFHT600_v3	557.615	4.5523
## HLT_PFHT650_v3	633.096	4.0096
## HLT_PFHT800_v2  2538.436	1

# Got the trigweights from brilcalc :
# 
# setenv PATH $HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
# pip uninstall brilws
# pip install --install-option="--prefix=$HOME/.local" brilws
# brilcalc lumi --hltpath HLT_PFHT\* --normtag ~lumipro/public/normtag_file/OfflineNormtagV2.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt -u /pb
## trigWeights = [
##     12.4744,  #HT300
##     11.8516,  #HT350
##     11.5029,  #HT400
##     10.5700,  #HT475
##     4.5523,   #HT600
##     4.0096,   #HT650
##     1.0       #HT800
##     ]

# Apparently the lumis reported by brilcalc are not exactly corresponding to the prescales. I derived
# them myself. 

trigWeights = [
    1.0,      #HT800
    1.16,#4.0096,   #HT650
    26,#4.5523,   #HT600
    26,#10.5700,  #HT475
    26,#11.5029,  #HT400
    ]
    
dataTrees = []
qcdTrees = []
# Append the actual TTrees
for idata in range(0,len(datasIn)) :
    dataTrees.append( datasIn[idata].Get("TreeEXOVV") )
for iq in range(0,len(qcdIn)) :
    qcdTrees.append( qcdIn[iq].Get("TreeEXOVV") )


if options.isData :
    trees = dataTrees
else :
    trees = qcdTrees
xaxis = '#rho = (m/p_{T}R)^{2}'
variable = '(jet_mass_so/(jet_pt_so*0.8))**2'
histbins = '(30,0.0,0.3)'


rhobins = array.array('d', [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 1.0])
#rhobins = array.array('d', [0.0, 0.0001, 0.1, 1.0])
nrhobins = len(rhobins)-1


if options.isData : 
    fout = ROOT.TFile(options.outlabel + '_data.root', 'RECREATE')
else :
    fout = ROOT.TFile(options.outlabel + '_qcdmc.root', 'RECREATE')

ptMinStr = str(int(options.ptMin))
if options.ptMax != None :
    ptMaxStr = str(int(options.ptMax))
else :
    ptMaxStr = 'Inf'
massMinStr = str(int(options.massMin))
if options.massMax != None :
    massMaxStr = str(int(options.massMax))
else :
    massMaxStr = 'Inf'
    
tauVsRho = ROOT.TH2F('tauVsRho',';#rho;#tau_{21}', 25, 0, 1, 25, 0, 1)

ptHist = ROOT.TH1F('ptHist', 'ptHist', 400, 0., 4000.)
massHist = ROOT.TH1F('massHist', 'massHist', 400, 0., 400.)

rhoNum = ROOT.TH1F('rhoNum',
                   ';#rho;Number',
                   nrhobins, rhobins)
rhoDen = ROOT.TH1F('rhoDen',
                   ';#rho;Number',
                   nrhobins, rhobins)


for itree,t in enumerate(trees) :

    FatJetPt = array.array('f', [-1,-1])
    FatJetEta = array.array('f', [-1,-1])
    FatJetPhi = array.array('f', [-1,-1])
    FatJetMass = array.array('f', [-1,-1])
    FatJetMassSoftDrop = array.array('f', [-1,-1])
    FatJetTau21 = array.array('f', [-1,-1])
    FatJetRhoRatio = array.array('f', [-1,-1])
    Trig = array.array('i', [-1] )

    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetEta', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus ('FatJetRhoRatio', 1)
    t.SetBranchStatus ('FatJetTau21', 1)
    t.SetBranchStatus ('Trig', 1)

    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetEta', FatJetEta)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress ('FatJetRhoRatio', FatJetRhoRatio)
    t.SetBranchAddress ('FatJetTau21', FatJetTau21)
    t.SetBranchAddress ('Trig', Trig)
    
    entries = t.GetEntriesFast()
    print 'Processing tree ' + str(itree)
    

    if options.maxEvents != None :
        eventsToRun = options.maxEvents
    else :
        eventsToRun = entries
    for jentry in xrange( eventsToRun ):
        if jentry % 100000 == 0 :
            print 'processing ' + str(jentry)
        # get the next tree in the chain and verify
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break

        FatJet0 = ROOT.TLorentzVector()
        FatJet0.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])
        sdrho0 = FatJetRhoRatio[0]
        tau21_0 = FatJetTau21[0]

        FatJet1 = ROOT.TLorentzVector()
        FatJet1.SetPtEtaPhiM( FatJetPt[1], FatJetEta[1], FatJetPhi[1], FatJetMass[1])
        sdrho1 = FatJetRhoRatio[1]
        tau21_1 = FatJetTau21[1]



        ptAvg = (FatJetPt[0] + FatJetPt[1]) * 0.5
        if options.isData == False : 
            weight = qcdWeights[itree]
        else :
            trig = None
            if ((Trig[0] % 1000000) / 100000 == 1) and ptAvg >= 400 :
                trig = 0
            elif ((Trig[0] % 100000) / 10000 == 1) and 370 <= ptAvg and ptAvg < 400 :
                trig = 1
            elif ((Trig[0] % 10000) / 1000 == 1) and 320 <= ptAvg and ptAvg < 370  :
                trig = 2
            elif ((Trig[0] % 1000) / 100 == 1) and 260 <= ptAvg and ptAvg < 320  :
                trig = 3
            elif ((Trig[0] % 100) / 10 == 1) and 200 <= ptAvg and ptAvg < 260 :
                trig = 4
            else :
                continue
            weight = trigWeights[trig]


        tagIndex = random.randint(0,1)
        probeIndex = 1 - tagIndex


        if options.ptMax != None :
            ptMax = options.ptMax
        else :
            ptMax = 13000.
        if options.massMax != None :
            massMax = options.massMax
        else :
            massMax = 13000.
            
        if options.ptMin < FatJetPt[tagIndex] and FatJetPt[tagIndex] <= ptMax and \
          options.massMin < FatJetMassSoftDrop[tagIndex] and FatJetMassSoftDrop[tagIndex] <= massMax and \
          options.ptMin < FatJetPt[probeIndex] and FatJetPt[probeIndex] <= ptMax and \
          options.massMin < FatJetMassSoftDrop[probeIndex] and FatJetMassSoftDrop[probeIndex] <= massMax and \
          FatJetTau21[tagIndex] < options.tauCut :
          
          
            ptHist.Fill( FatJetPt[probeIndex], weight)
            massHist.Fill( FatJetMassSoftDrop[probeIndex], weight )
            tauVsRho.Fill( FatJetRhoRatio[probeIndex], FatJetTau21[probeIndex], weight )
            rhoDen.Fill( FatJetRhoRatio[probeIndex], weight )
            if FatJetTau21[probeIndex] < options.tauCut :
                rhoNum.Fill( FatJetRhoRatio[probeIndex], weight )



for ibin in xrange( 1, rhoNum.GetNbinsX() - 1) :
    binwidth = rhoNum.GetBinWidth(ibin)
    num = rhoNum.GetBinContent(ibin)
    den = rhoDen.GetBinContent(ibin)
    dnum = rhoNum.GetBinError(ibin)
    dden = rhoDen.GetBinError(ibin)
    if abs(num) > 0 :        
        rhoNum.SetBinContent( ibin, num/binwidth )
        rhoNum.SetBinError( ibin, dnum/binwidth )
    if abs(den) > 0 :        
        rhoDen.SetBinContent( ibin, den/binwidth )
        rhoDen.SetBinError( ibin, dden/binwidth )

rate = rhoNum.Clone()
rate.Divide(rhoNum,rhoDen,1,1,"b")
rate.SetName("rate")
fout.cd()
fout.Write()
fout.Close()
