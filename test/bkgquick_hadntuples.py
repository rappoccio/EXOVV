#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()


parser.add_option('--predFile', type='string', action='store',
                  dest='predFile',
                  default = "vv2500invpb_highpt_rate.root",
                  help='Predicted distribution file')


parser.add_option('--predHist', type='string', action='store',
                  dest='predHist',
                  default = "rLoMod",
                  help='Histogram from predFile to use as predicted rate')



parser.add_option('--modFile', type='string', action='store',
                  dest='modFile',
                  default = 'vv2500invpb_modfile.root',
                  help='File to get modified mass from')



parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "vv2500invpb_bkg_nom",
                  help='Label for plots')



parser.add_option('--tau21Cut', type='float', action='store',
                  default=0.6,
                  dest='tau21Cut',
                  help='Tau2 / Tau1 n-subjettiness cut')


parser.add_option('--sdmassCutLo', type='float', action='store',
                  default=50.,
                  dest='sdmassCutLo',
                  help='Lower softdrop mass cut')


parser.add_option('--sdmassCutHi', type='float', action='store',
                  default=105.,
                  dest='sdmassCutHi',
                  help='Upper softdrop mass cut')


parser.add_option('--isData', action='store_true',
                  default=False,
                  dest='isData',
                  help='Is this data?')


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

ROOT.gSystem.Load("libAnalysisPredictedDistribution")

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

lumi = 2500. 

# get the predicted distribution
predFile = ROOT.TFile( options.predFile )
hpredF = predFile.Get(options.predHist)
hpredF.SetName("junk")
hpred = ROOT.TH1D()
hpredF.Copy( hpred )
hpred.SetName("rLoMod")

if options.modFile != None : 
    fmod = ROOT.TFile( options.modFile )
    hModMassDist = fmod.Get("hModMass") # Need to run this script TWICE, first to get the MC-based mod mass, second to apply it. 
    hModMassDist.SetName("hModMassDist")
    binlo = hModMassDist.GetXaxis().FindBin( options.sdmassCutLo )
    binhi = hModMassDist.GetXaxis().FindBin( options.sdmassCutHi )
    maxbins = hModMassDist.GetNbinsX()
    for ibin in xrange(0,binlo) :
        hModMassDist.SetBinContent(ibin,0.0)
    for ibin in xrange(binhi, maxbins) :
        hModMassDist.SetBinContent(ibin,0.0)
    hModMassDist.Scale(1.0/hModMassDist.Integral())
    #modcanv = ROOT.TCanvas("modcanv", "modcanv")
    #hModMassDist.Draw()
    
f = ROOT.TFile( options.outlabel + '_predplots.root', "RECREATE")


hModMass = ROOT.TH1F("hModMass", "hModMass", 50, 0, 500.)


ROOT.SetOwnership( hpred, False )
predJetPt = ROOT.PredictedDistribution(hpred, "pred_jet_pt", "Jet p_{T} (GeV)", 30, 0, 3000.)
predJetMVV = ROOT.PredictedDistribution(hpred, "pred_mvv", "M_{VV} (GeV)", 50, 0.0, 5000.)
predJetMVVMod = ROOT.PredictedDistribution(hpred, "pred_mvvmod", "M_{VV} (GeV)", 50, 0.0, 5000.)
predJetSDMass = ROOT.PredictedDistribution(hpred, "pred_sdmass", "Soft Drop Mass", 50, 0.0, 250.)
predJetMass = ROOT.PredictedDistribution(hpred, "pred_jetmass", "Ungroomed Jet Mass", 50, 0.0, 250.)
predJetMassMod = ROOT.PredictedDistribution(hpred, "pred_jetmassmod", "Ungroomed Jet Mass", 50, 0.0, 250.)
predJetSDRho = ROOT.PredictedDistribution(hpred, "pred_sdrho", "Soft Drop Rho", 50, 0.0, 1.)

ROOT.SetOwnership( predJetPt, False )
ROOT.SetOwnership( predJetMVV, False )
ROOT.SetOwnership( predJetMVVMod, False )
ROOT.SetOwnership( predJetSDMass, False )
ROOT.SetOwnership( predJetMass, False )
ROOT.SetOwnership( predJetMassMod, False )

ROOT.SetOwnership( predJetSDRho, False )


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

    if options.maxEvents != None :
        eventsToRun = options.maxEvents
    else :
        eventsToRun = entries
    for jentry in xrange( eventsToRun ):
        if jentry % 100000 == 0 :
            print 'processing ' + str(jentry)
        # get the next tree in the chain and verify
        ientry = t.LoadTree( jentry )
        if ientry < 0:
            break

        # copy next entry into memory and verify
        nb = t.GetEntry( jentry )
        if nb <= 0:
            continue

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


        #if ptAvg < 1100. * 0.5 :
        #    continue
            
        FatJet = [ROOT.TLorentzVector(),ROOT.TLorentzVector()]
        taggable = [False,False]
        tagged = [False,False]
        for ijet in [0,1] : 
            FatJet[ijet].SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])
            taggable[ijet] = FatJet[ijet].Perp() > 350. and \
              options.sdmassCutLo < FatJetMassSoftDrop[ijet] and FatJetMassSoftDrop[ijet] < options.sdmassCutHi
            tagged[ijet] = FatJetTau21[ijet] < options.tau21Cut


        tagIndex = random.randint(0,1)
        probeIndex = 1 - tagIndex

        if taggable[0] == False or taggable[1] == False :
            continue
        if tagged[tagIndex] == False :
            continue

        hModMass.Fill( FatJet[probeIndex].M() )

        FatJetMod = [ ROOT.TLorentzVector( FatJet[0] ), ROOT.TLorentzVector( FatJet[1] ) ]
        if options.modFile != None :
            if FatJetMod[probeIndex].M() < options.sdmassCutLo or FatJetMod[probeIndex].M() > options.sdmassCutHi :
                massMod = hModMassDist.GetRandom()
            else :
                massMod = FatJetMod[probeIndex].M()
        else :
            massMod = FatJet[probeIndex].M()
        FatJetMod[probeIndex].SetPtEtaPhiM( FatJet[probeIndex].Perp(), FatJet[probeIndex].Eta(), FatJet[probeIndex].Phi(), massMod )
        vvCand = FatJet[tagIndex] + FatJet[probeIndex]
        vvCandMod = FatJet[tagIndex] + FatJetMod[probeIndex]


        predJetPt.Accumulate( FatJet[probeIndex].Perp(), FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetMVV.Accumulate( vvCand.M(), FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetMVVMod.Accumulate( vvCandMod.M(), FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetSDMass.Accumulate( FatJetMassSoftDrop[probeIndex], FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetMass.Accumulate( FatJet[probeIndex].M(), FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetMassMod.Accumulate( FatJetMod[probeIndex].M(), FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )
        predJetSDRho.Accumulate( FatJetRhoRatio[probeIndex], FatJetRhoRatio[probeIndex], tagged[probeIndex], weight )



predJetPt.SetCalculatedErrors()
predJetMVV.SetCalculatedErrors()
predJetMVVMod.SetCalculatedErrors()
predJetSDMass.SetCalculatedErrors()
predJetMass.SetCalculatedErrors()
predJetMassMod.SetCalculatedErrors()
predJetSDRho.SetCalculatedErrors()


f.cd()
f.Write()

f.Close()
