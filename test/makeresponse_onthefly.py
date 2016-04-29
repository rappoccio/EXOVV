#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import *

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "rho_plots",
                  help='Label for plots')


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

ROOT.gSystem.Load("RooUnfold/libRooUnfold")

ptBinA = array.array('d', [  200., 240., 310., 400., 530., 650., 760., 13000.])
nbinsPt = len(ptBinA) - 1

response = ROOT.RooUnfoldResponse()
response.SetName("2d_response")
trueVarHist = ROOT.TH2F('truehist2d', 'truehist2D', nbinsPt, ptBinA, 50, 0, 1000)
measVarHist = ROOT.TH2F('meashist2d', 'meashist2D', nbinsPt, ptBinA, 50, 0, 1000)
response.Setup(measVarHist, trueVarHist)

response_jecup = ROOT.RooUnfoldResponse()
response_jecup.SetName("2d_response_jecup")
response_jecup.Setup(measVarHist, trueVarHist)

response_jecdn = ROOT.RooUnfoldResponse()
response_jecdn.SetName("2d_response_jecdn")
response_jecdn.Setup(measVarHist, trueVarHist)

response_jerup = ROOT.RooUnfoldResponse()
response_jerup.SetName("2d_response_jerup")
response_jerup.Setup(measVarHist, trueVarHist)

response_jerdn = ROOT.RooUnfoldResponse()
response_jerdn.SetName("2d_response_jerdn")
response_jerdn.Setup(measVarHist, trueVarHist)


response_softdrop = ROOT.RooUnfoldResponse()
response_softdrop.SetName("2d_response_softdrop")
response_softdrop.Setup(measVarHist, trueVarHist)


response_softdrop_jecup = ROOT.RooUnfoldResponse()
response_softdrop_jecup.SetName("2d_response_softdrop_jecup")
response_softdrop_jecup.Setup(measVarHist, trueVarHist)

response_softdrop_jecdn = ROOT.RooUnfoldResponse()
response_softdrop_jecdn.SetName("2d_response_softdrop_jecdn")
response_softdrop_jecdn.Setup(measVarHist, trueVarHist)

response_softdrop_jerup = ROOT.RooUnfoldResponse()
response_softdrop_jerup.SetName("2d_response_softdrop_jerup")
response_softdrop_jerup.Setup(measVarHist, trueVarHist)

response_softdrop_jerdn = ROOT.RooUnfoldResponse()
response_softdrop_jerdn.SetName("2d_response_softdrop_jerdn")
response_softdrop_jerdn.Setup(measVarHist, trueVarHist)

h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, 50, 0, 1000)
h_2DHisto_gen = ROOT.TH2F('PFJet_pt_m_AK8Gen', 'Generator Mass vs. P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, 50, 0, 1000)

h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, 50, 0, 1000)
h_2DHisto_genSD = ROOT.TH2F('PFJet_pt_m_AK8SDgen', 'Generator Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, 50, 0, 1000)


def getMatched( p4, coll, dRMax = 0.1) :
    if coll != None : 
        for i,c in enumerate(coll):
            if p4.DeltaR(c) < dRMax :
                return i
    return None

def ConvertPtRapPhiM( pt,y,phi,m ):
    val = exp(2.0*y)
    if abs(val - 1.0) < 0.000001 :
        return [pt, 0.0, phi, m]
    else : 
        fval = (val + 1.) / (val - 1.)
        fval2 = fval*fval - 1.0
        pz = sqrt( (pt*pt + m*m) / fval2 )
        tanthetahalf = pt / (sqrt(pt*pt + pz*pz) + pz)

        eta = -log( tanthetahalf )
        if y < 0 :
            eta *= -1.0
        return [pt,eta,phi,m]
    

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

lumi = 2600

qcdIn = []

filelocs = [
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    '/uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_3_patch2/src/Analysis/EXOVV/test/crab_tightmatch/crab_EXOVV_tightmatchQCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/results/*.root',
    ]

for ifileloc in xrange( len(filelocs) ) :

    fileloc = filelocs[ifileloc]
    t = ROOT.TChain("TreeEXOVV")
    t.Add( fileloc )
    qcdIn.append( t )


    
qcdWeights =[
     117276. / 6918748. * lumi,
     7823 / 5968960. * lumi,
     648.2 / 3977770. * lumi,
     186.9 / 3979884. * lumi,
     32.293 / 3973224. * lumi,
     9.4183 / 2953982. * lumi,
     0.84265 / 395725. * lumi,
     0.114943 / 393760. * lumi,
     0.00682981 / 398452. * lumi,
     0.000165445 / 391108. * lumi
    ]

fout = ROOT.TFile(options.outlabel + '_qcdmc.root', 'RECREATE')


for itree,t in enumerate(qcdIn) :
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1,-1])
    FatJetEta = array.array('f', [-1,-1])
    FatJetPhi = array.array('f', [-1,-1])
    FatJetMass = array.array('f', [-1,-1])
    FatJetMassSoftDrop = array.array('f', [-1,-1])
    FatJetTau21 = array.array('f', [-1,-1])
    FatJetCorrUp = array.array('f', [-1,-1])
    FatJetCorrDn = array.array('f', [-1,-1])
    FatJetRhoRatio = array.array('f', [-1,-1])
    NGenJet = array.array('i', [0] )
    GenJetPt = array.array('f', [-1,-1])
    GenJetEta = array.array('f', [-1,-1])
    GenJetPhi = array.array('f', [-1,-1])
    GenJetMass = array.array('f', [-1,-1])
    GenJetMassSoftDrop = array.array('f', [-1,-1])
    GenJetRhoRatio = array.array('f', [-1, -1])
    FatJetPtSoftDrop = array.array('f', [-1, -1])
    FatJetPhiSoftDrop = array.array('f', [-1, -1])
    FatJetRapSoftDrop = array.array('f', [-1, -1])
    GenJetPtSoftDrop = array.array('f', [-1, -1])
    GenJetPhiSoftDrop = array.array('f', [-1, -1])
    GenJetRapSoftDrop = array.array('f', [-1, -1])
    
    
    Trig = array.array('i', [-1] )

    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('NFatJet', 1)
    t.SetBranchStatus ('NGenJet', 1)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetEta', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus ('GenJetPt', 1)
    t.SetBranchStatus ('GenJetEta', 1)
    t.SetBranchStatus ('GenJetPhi', 1)
    t.SetBranchStatus ('GenJetMass', 1)
    t.SetBranchStatus ('GenJetMassSoftDrop', 1)    
    t.SetBranchStatus ('FatJetRhoRatio', 1)
    t.SetBranchStatus ('FatJetTau21', 1)
    t.SetBranchStatus ('FatJetCorrUp', 1)
    t.SetBranchStatus ('FatJetCorrDn', 1)
    t.SetBranchStatus ('Trig', 1)
    t.SetBranchStatus ('GenJetRhoRatio', 1)
    t.SetBranchStatus ('FatJetPtSoftDrop', 1)
    t.SetBranchStatus ('FatJetPhiSoftDrop', 1)
    t.SetBranchStatus ('FatJetRapSoftDrop', 1)
    t.SetBranchStatus ('GenJetPtSoftDrop', 1)
    t.SetBranchStatus ('GenJetPhiSoftDrop', 1)
    t.SetBranchStatus ('GenJetRapSoftDrop', 1)
    
    t.SetBranchAddress ('NFatJet', NFatJet)
    t.SetBranchAddress ('NGenJet', NGenJet)
    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetEta', FatJetEta)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress ('FatJetCorrUp', FatJetCorrUp)
    t.SetBranchAddress ('FatJetCorrDn', FatJetCorrDn)
    t.SetBranchAddress ('GenJetPt', GenJetPt)
    t.SetBranchAddress ('GenJetEta', GenJetEta)
    t.SetBranchAddress ('GenJetPhi', GenJetPhi)
    t.SetBranchAddress ('GenJetMass', GenJetMass)
    t.SetBranchAddress ('GenJetMassSoftDrop', GenJetMassSoftDrop)
    t.SetBranchAddress ('FatJetRhoRatio', FatJetRhoRatio)
    t.SetBranchAddress ('FatJetTau21', FatJetTau21)
    t.SetBranchAddress ('Trig', Trig)
    t.SetBranchAddress ('GenJetRhoRatio', GenJetRhoRatio)
    t.SetBranchAddress ('FatJetPtSoftDrop', FatJetPtSoftDrop)
    t.SetBranchAddress ('FatJetPhiSoftDrop', FatJetPhiSoftDrop)
    t.SetBranchAddress ('FatJetRapSoftDrop', FatJetRapSoftDrop)
    t.SetBranchAddress ('GenJetPtSoftDrop', GenJetPtSoftDrop)
    t.SetBranchAddress ('GenJetPhiSoftDrop', GenJetPhiSoftDrop)
    t.SetBranchAddress ('GenJetRapSoftDrop', GenJetRapSoftDrop)
    entries = t.GetEntries()
    
    

    if options.maxEvents != None :
        eventsToRun = options.maxEvents
    else :
        eventsToRun = entries
    print 'Processing tree ', itree, ' with number of entries ', entries, ', processing eventsToRun = ', eventsToRun
    for jentry in xrange( eventsToRun ):
        if jentry % 10000 == 0 :
            print 'processing ' + str(jentry)
        # get the next tree in the chain and verify
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break

        GenJets = []
        FatJets = []
        GenJetsMassSD = []
        FatJetsMassSD = []        
        GenJetsSD = []
        FatJetsSD = []
        weight = qcdWeights[itree]
        
        for igen in xrange( int(NGenJet[0]) ):
            GenJet = ROOT.TLorentzVector()
            GenJet.SetPtEtaPhiM( GenJetPt[igen], GenJetEta[igen], GenJetPhi[igen], GenJetMass[igen])            
            GenJets.append(GenJet)
            h_2DHisto_gen.Fill( GenJet.Perp(), GenJet.M(), weight )

            GenJetSD = ROOT.TLorentzVector()
            if GenJetPtSoftDrop[igen] != None and GenJetPtSoftDrop[igen] >= 0.0 : 
                [genpt,geneta,genphi,genm] = ConvertPtRapPhiM( GenJetPtSoftDrop[igen], GenJetRapSoftDrop[igen], GenJetPhiSoftDrop[igen], GenJetMassSoftDrop[igen] )
                GenJetSD.SetPtEtaPhiM( genpt, geneta, genphi, genm )
                GenJetsSD.append(GenJetSD)
                GenJetsMassSD.append( GenJetMassSoftDrop[igen] )
                h_2DHisto_genSD.Fill( GenJetSD.Perp(), GenJetSD.M(), weight)
            
        # First get the "Fills" and "Fakes" (i.e. we at least have a RECO jet)
        for ijet in xrange( int(NFatJet[0]) ):
            
            FatJet = ROOT.TLorentzVector()
            FatJet.SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])
#            [fatpt,fateta,fatphi,fatm] = ConvertPtRapPhiM( FatJetPt[ijet], FatJet.Rapidity(), FatJetPhi[ijet], FatJetMass[ijet] )
#            if abs (fateta - FatJetEta[ijet]) > 0.001 :
#                print 'bonehead, you did it wrong.'
#                print 'pt eta phi m rap = %8.4f %8.4f %8.4f %8.4f %8.4f ' % ( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet], fateta )
            igen = getMatched( FatJet, GenJets )
            h_2DHisto_meas.Fill( FatJet.Perp(), FatJet.M(), weight )
            FatJets.append(FatJet)

            

            FatJetSD = ROOT.TLorentzVector()
            igenSD = None
            if FatJetPtSoftDrop[ijet] != None and FatJetPtSoftDrop[ijet] >= 0.0: 
                [fatpt,fateta,fatphi,fatm] = ConvertPtRapPhiM( FatJetPtSoftDrop[ijet], FatJetRapSoftDrop[ijet], FatJetPhiSoftDrop[ijet], FatJetMassSoftDrop[ijet] )
                FatJetSD.SetPtEtaPhiM( fatpt, fateta, fatphi, fatm )
                FatJetsSD.append(FatJetSD)
                h_2DHisto_measSD.Fill( FatJetSD.Perp(), FatJetSD.M(), weight)                                       
                igenSD = getMatched( FatJetSD, GenJetsSD, dRMax = 0.02 )
            
            
            
            

            if igen != None :  # Here we have a "Fill"
                valup = getJER(FatJet.Eta(), +1) #JER nominal=0, up=+1, down=-1
                recopt = FatJet.Perp()
                genpt = GenJets[igen].Perp()
                deltapt = (recopt-genpt)*(valup-1.0)
                smearup = max(0.0, (recopt+deltapt)/recopt)
                valdn = getJER(FatJet.Eta(), -1) #JER nominal=0, dn=+1, down=-1
                recopt = FatJet.Perp()
                genpt = GenJets[igen].Perp()
                deltapt = (recopt-genpt)*(valdn-1.0)
                smeardn = max(0.0, (recopt+deltapt)/recopt)                
                
                                         
                response.Fill( FatJet.Perp(), FatJet.M(), GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecup.Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecdn.Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerup.Fill( FatJet.Perp() * smearup, FatJet.M()* smearup, GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerdn.Fill( FatJet.Perp() * smeardn, FatJet.M()* smeardn, GenJets[igen].Perp(), GenJets[igen].M(), weight )


            else : # Here we have a "Fake"
                response.Fake( FatJet.Perp(), FatJet.M(), weight )
                response_jecup.Fake( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], weight )
                response_jecdn.Fake( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], weight )
                response_jerup.Fake( FatJet.Perp() * smearup, FatJet.M() * smearup, weight )
                response_jerdn.Fake( FatJet.Perp() * smeardn, FatJet.M() * smeardn, weight )

            if igenSD != None : 

                valup = getJER(FatJetSD.Eta(), +1) #JER nominal=0, up=+1, down=-1
                recopt = FatJetSD.Perp()
                genpt = GenJetsSD[igenSD].Perp()
                deltapt = (recopt-genpt)*(valup-1.0)
                smearup = max(0.0, (recopt+deltapt)/recopt)
                valdn = getJER(FatJetSD.Eta(), -1) #JER nominal=0, dn=+1, down=-1
                recopt = FatJetSD.Perp()
                genpt = GenJetsSD[igenSD].Perp()
                deltapt = (recopt-genpt)*(valdn-1.0)
                smeardn = max(0.0, (recopt+deltapt)/recopt)
                                
                response_softdrop.Fill( FatJetSD.Perp() , FatJetSD.M(), GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecup.Fill( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecdn.Fill( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerup.Fill( FatJetSD.Perp()  * smearup, FatJetSD.M() * smearup, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerdn.Fill( FatJetSD.Perp()  * smeardn, FatJetSD.M() * smeardn, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )

            else:               
                response_softdrop.Fake( FatJetSD.Perp() , FatJetSD.M(), weight )
                response_softdrop_jecup.Fake( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], weight )
                response_softdrop_jecdn.Fake( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], weight )
                response_softdrop_jerup.Fake( FatJetSD.Perp()  * smearup, FatJetSD.M() * smearup, weight )
                response_softdrop_jerdn.Fake( FatJetSD.Perp()  * smeardn, FatJetSD.M() * smeardn, weight )
        # Now get the "Misses" (i.e. we have no RECO jet)
        for igen in xrange( int(NGenJet[0]) ):
            ijet = getMatched( GenJets[igen], FatJets )
            if ijet == None :
                response.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecup.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecdn.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerup.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerdn.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
        # Now get the "Misses" (i.e. we have no RECO jet)
        for igenSD in xrange( len(GenJetsSD) ):
            ijetSD = getMatched( GenJetsSD[igenSD], FatJetsSD, dRMax = 0.05 )
            if ijetSD == None :
                response_softdrop.Miss( GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecup.Miss( GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecdn.Miss( GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerup.Miss( GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerdn.Miss( GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )



fout.cd()
#response.Hresponse().Draw()
response.Write()
response_jecup.Write()
response_jecdn.Write()
response_jerup.Write()
response_jerdn.Write()
h_2DHisto_gen.Write()
h_2DHisto_meas.Write()

h_2DHisto_measSD.Write()
h_2DHisto_genSD.Write()
response_softdrop.Write()
response_softdrop_jecup.Write()
response_softdrop_jecdn.Write()
response_softdrop_jerup.Write()
response_softdrop_jerdn.Write()

fout.Close()
