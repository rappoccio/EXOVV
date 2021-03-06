#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "jackknife_otherway_repdf.root",
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

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])
nbinsPt = len(ptBinA) - 1
mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])
nbinsm = len(mBinA) - 1
trueVarHist = ROOT.TH2F('truehist2d', 'truehist2D', nbinsm, mBinA, nbinsPt, ptBinA)
measVarHist = ROOT.TH2F('meashist2d', 'meashist2D', nbinsm, mBinA, nbinsPt, ptBinA)

responsemod0 = ROOT.RooUnfoldResponse()
responsemod0.SetName("2d_response0")
responsemod0.Setup(measVarHist, trueVarHist)

responsemod1 = ROOT.RooUnfoldResponse()
responsemod1.SetName("2d_response1")
responsemod1.Setup(measVarHist, trueVarHist)

responsemod2 = ROOT.RooUnfoldResponse()
responsemod2.SetName("2d_response2")
responsemod2.Setup(measVarHist, trueVarHist)

responsemod3 = ROOT.RooUnfoldResponse()
responsemod3.SetName("2d_response3")
responsemod3.Setup(measVarHist, trueVarHist)

responsemod4 = ROOT.RooUnfoldResponse()
responsemod4.SetName("2d_response4")
responsemod4.Setup(measVarHist, trueVarHist)

responsemod5 = ROOT.RooUnfoldResponse()
responsemod5.SetName("2d_response5")
responsemod5.Setup(measVarHist, trueVarHist)

responsemod6 = ROOT.RooUnfoldResponse()
responsemod6.SetName("2d_response6")
responsemod6.Setup(measVarHist, trueVarHist)

responsemod7 = ROOT.RooUnfoldResponse()
responsemod7.SetName("2d_response7")
responsemod7.Setup(measVarHist, trueVarHist)

responsemod8 = ROOT.RooUnfoldResponse()
responsemod8.SetName("2d_response8")
responsemod8.Setup(measVarHist, trueVarHist)

responsemod9 = ROOT.RooUnfoldResponse()
responsemod9.SetName("2d_response9")
responsemod9.Setup(measVarHist, trueVarHist)


responsemod0_softdrop = ROOT.RooUnfoldResponse()
responsemod0_softdrop.SetName("2d_response_softdrop0")
responsemod0_softdrop.Setup(measVarHist, trueVarHist)

responsemod1_softdrop = ROOT.RooUnfoldResponse()
responsemod1_softdrop.SetName("2d_response_softdrop1")
responsemod1_softdrop.Setup(measVarHist, trueVarHist)

responsemod2_softdrop = ROOT.RooUnfoldResponse()
responsemod2_softdrop.SetName("2d_response_softdrop2")
responsemod2_softdrop.Setup(measVarHist, trueVarHist)

responsemod3_softdrop = ROOT.RooUnfoldResponse()
responsemod3_softdrop.SetName("2d_response_softdrop3")
responsemod3_softdrop.Setup(measVarHist, trueVarHist)

responsemod4_softdrop = ROOT.RooUnfoldResponse()
responsemod4_softdrop.SetName("2d_response_softdrop4")
responsemod4_softdrop.Setup(measVarHist, trueVarHist)

responsemod5_softdrop = ROOT.RooUnfoldResponse()
responsemod5_softdrop.SetName("2d_response_softdrop5")
responsemod5_softdrop.Setup(measVarHist, trueVarHist)

responsemod6_softdrop = ROOT.RooUnfoldResponse()
responsemod6_softdrop.SetName("2d_response_softdrop6")
responsemod6_softdrop.Setup(measVarHist, trueVarHist)

responsemod7_softdrop = ROOT.RooUnfoldResponse()
responsemod7_softdrop.SetName("2d_response_softdrop7")
responsemod7_softdrop.Setup(measVarHist, trueVarHist)

responsemod8_softdrop = ROOT.RooUnfoldResponse()
responsemod8_softdrop.SetName("2d_response_softdrop8")
responsemod8_softdrop.Setup(measVarHist, trueVarHist)

responsemod9_softdrop = ROOT.RooUnfoldResponse()
responsemod9_softdrop.SetName("2d_response_softdrop9")
responsemod9_softdrop.Setup(measVarHist, trueVarHist)




h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_gen = ROOT.TH2F('PFJet_pt_m_AK8Gen', 'Generator Mass vs. P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)

h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_genSD = ROOT.TH2F('PFJet_pt_m_AK8SDgen', 'Generator Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)

def getMatched( p4, coll, dRMax = 0.1) :
    if coll != None : 
        for i,c in enumerate(coll):
            if p4.DeltaR(c) < dRMax :
                return i
    return None



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

lumi = 40.

qcdIn =[
    ROOT.TFile('qcdpy8_170to300_rejec.root'),
    ROOT.TFile('qcdpy8_300to470_rejec.root'),
    ROOT.TFile('qcdpy8_470to600_rejec.root'),
    ROOT.TFile('qcdpy8_600to800_rejec.root'),
    ROOT.TFile('qcdpy8_800to1000_rejec.root'),
    ROOT.TFile('qcdpy8_1000to1400_rejec.root'),
    ROOT.TFile('qcdpy8_1400to1800_rejec.root'),
    ROOT.TFile('qcdpy8_1800to2400_rejec.root'),
    ROOT.TFile('qcdpy8_2400to3200_rejec.root'),
    ROOT.TFile('qcdpy8_3200toinf_rejec.root'),
    ]
masslessSD = 0
qcdWeights =[
    117276.      / 6918748.,  #170to300    
    7823.        / 5968960.,  #300to470    
    648.2        / 3977770.,  #470to600    
    186.9        / 3979884.,  #600to800    
    32.293       / 3973224.,  #800to1000   
    9.4183       / 2953982.,  #1000to1400  
    0.84265      / 395725. ,  #1400to1800  
    0.114943     / 393760. ,  #1800to2400  
    0.00682981   / 398452. ,  #2400to3200  
    0.000165445  / 391108. ,  #3200toInf   
        ]

trees = []
# Append the actual TTrees
for iq in qcdIn:
    trees.append( iq.Get("TreeEXOVV") )
fout = ROOT.TFile(options.outlabel , 'RECREATE')


for itree,t in enumerate(trees) :
    NFatJet = array.array('i', [0] )
    
    NNPDF3weight_CorrDn = array.array('f', [-1.])
    NNPDF3weight_CorrUp = array.array('f', [-1.])

    FatJetPt = array.array('f', [-1]*5)
    FatJetEta = array.array('f', [-1]*5)
    FatJetRap = array.array('f', [-1]*5)
    FatJetPhi = array.array('f', [-1]*5)
    FatJetMass = array.array('f', [-1]*5)
    FatJetMassSoftDrop = array.array('f', [-1]*5)
    FatJetTau21 = array.array('f', [-1]*5)
    FatJetCorrUp = array.array('f', [-1]*5)
    FatJetCorrDn = array.array('f', [-1]*5)
    FatJetRhoRatio = array.array('f', [-1]*5)
    NGenJet = array.array('i', [0] )
    GenJetPt = array.array('f', [-1]*5)
    GenJetEta = array.array('f', [-1]*5)
    GenJetPhi = array.array('f', [-1]*5)
    GenJetMass = array.array('f', [-1]*5)
    GenJetMassSoftDrop = array.array('f', [-1]*5)
    GenJetRhoRatio = array.array('f', [-1]*5)
    FatJetPtSoftDrop = array.array('f', [-1]*5)
    GenJetPtSoftDrop = array.array('f', [-1]*5)
    
    
    Trig = array.array('i', [-1] )
    
    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('NFatJet', 1)
    t.SetBranchStatus ('NGenJet', 1)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetEta', 1)
    t.SetBranchStatus ('FatJetRap', 1)
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
    t.SetBranchStatus ('GenJetPtSoftDrop', 1)
    t.SetBranchStatus ('FatJetPtSoftDrop', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrDn', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrUp', 1)    


    t.SetBranchAddress ('NNPDF3weight_CorrDn', NNPDF3weight_CorrDn)
    t.SetBranchAddress ('NNPDF3weight_CorrUp', NNPDF3weight_CorrUp)
    t.SetBranchAddress ('NFatJet', NFatJet)
    t.SetBranchAddress ('NGenJet', NGenJet)
    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetEta', FatJetEta)
    t.SetBranchAddress ('FatJetRap', FatJetRap)
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
    t.SetBranchAddress ('GenJetPtSoftDrop', GenJetPtSoftDrop)
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

        GenJets = []
        FatJets = []
        GenJetsMassSD = []
        FatJetsMassSD = []        
        GenJetsSD = []
        FatJetsSD = []
        weight = qcdWeights[itree]

        maxjet = 0
        minjet = 1
        if FatJetPt[0] < FatJetPt[1] :
            maxjet = 1
            minjet = 0


        ptasym = (FatJetPt[maxjet] - FatJetPt[minjet])/(FatJetPt[maxjet] + FatJetPt[minjet])
        dphi = ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[minjet] )

        pdfweight_up = NNPDF3weight_CorrUp[0]
        pdfweight_dn = NNPDF3weight_CorrDn[0]        
    #    print "pdfweight up: " + str(pdfweight_up)
    #    print "pdfweight down: " + str(pdfweight_dn)
        
        passkin = ptasym < 0.3 and dphi > 2.0
        if not passkin :
            continue

        
        for igen in xrange( int(NGenJet[0]) ):
            GenJet = ROOT.TLorentzVector()
            GenJet.SetPtEtaPhiM( GenJetPt[igen], GenJetEta[igen], GenJetPhi[igen], GenJetMass[igen])
            GenJetSD = ROOT.TLorentzVector()
            GenJetSD.SetPtEtaPhiM( GenJetPtSoftDrop[igen], GenJetEta[igen], GenJetPhi[igen], GenJetMassSoftDrop[igen] )
            GenJets.append(GenJet)
            GenJetsSD.append(GenJetSD)
            GenJetsMassSD.append( GenJetMassSoftDrop[igen] )            
            h_2DHisto_gen.Fill( GenJet.M(), GenJet.Perp(), weight )
            h_2DHisto_genSD.Fill( GenJetSD.M(), GenJetSD.Perp(), weight)
        # First get the "Fills" and "Fakes" (i.e. we at least have a RECO jet)
        for ijet in xrange( int(NFatJet[0]) ):
            
            FatJet = ROOT.TLorentzVector()
            FatJet.SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])
            
            FatJetSD = ROOT.TLorentzVector()
            FatJetSD.SetPtEtaPhiM( FatJetPtSoftDrop[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMassSoftDrop[ijet]  )
            
            FatJetsSD.append(FatJetSD)
            FatJets.append(FatJet)
           
            h_2DHisto_meas.Fill(  FatJet.M(), FatJet.Perp(), weight )
            
            h_2DHisto_measSD.Fill( FatJetSD.M(), FatJet.Perp(), weight)

            igen = getMatched( FatJet, GenJets )
            igenSD = getMatched(FatJetSD, GenJetsSD, dRMax=0.5)
            
          
            if igen != None :  # Here we have a "Fill"
                
                if jentry % 10 != 0:
                    responsemod0.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 2:
                    responsemod2.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 3:
                    responsemod3.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 4:
                    responsemod4.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 5:
                    responsemod5.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 6:
                    responsemod6.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 7:    
                    responsemod7.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 8:
                    responsemod8.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 9:
                    responsemod9.Fill( FatJet.M(), FatJet.Perp(), GenJets[igen].M(), GenJets[igen].Perp(), weight )

                
            else : # Here we have a "Fake"
                if jentry % 10 != 0:
                    responsemod0.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 2:
                    responsemod2.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 3:
                    responsemod3.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 4:
                    responsemod4.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 5:
                    responsemod5.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 6:
                    responsemod6.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 7:
                    responsemod7.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 8:
                    responsemod8.Fake( FatJet.M(), FatJet.Perp(), weight )
                if jentry % 10 != 9:
                    responsemod9.Fake( FatJet.M(), FatJet.Perp(), weight )

            if igenSD != None:
                if jentry % 10 != 0:
                    responsemod0_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 2:
                    responsemod2_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 3:
                    responsemod3_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 4:
                    responsemod4_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 5:
                    responsemod5_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 6:
                    responsemod6_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 7:
                    responsemod7_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 8:
                    responsemod8_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )
                if jentry % 10 != 9:
                    responsemod9_softdrop.Fill(  FatJetSD.M(), FatJet.Perp(), GenJetsSD[igenSD].M(), GenJets[igenSD].Perp(), weight  )

            else:
                if jentry % 10 != 0:
                    responsemod0_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 2:
                    responsemod2_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 3:
                    responsemod3_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 4:
                    responsemod4_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 5:
                    responsemod5_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 6:
                    responsemod6_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 7:
                    responsemod7_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 8:
                    responsemod8_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )
                if jentry % 10 != 9:
                    responsemod9_softdrop.Fake( FatJetSD.M(), FatJet.Perp(), weight )

        # Now get the "Misses" (i.e. we have no RECO jet)
        for igen in xrange( int(NGenJet[0]) ):
            ijet = getMatched( GenJets[igen], FatJets )
            ijetSD = getMatched( GenJetsSD[igen], FatJetsSD, dRMax=0.5 )
            if ijet == None :
                if jentry % 10 != 0:
                    responsemod0.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 2:
                    responsemod2.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 3:
                    responsemod3.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 4:
                    responsemod4.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 5:
                    responsemod5.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 6:
                    responsemod6.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 7:
                    responsemod7.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 8:
                    responsemod8.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 9:
                    responsemod9.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
            if ijetSD == None:
                if jentry % 10 != 0:
                    responsemod0_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 1:
                    responsemod1_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 2:
                    responsemod2_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 3:
                    responsemod3_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 4:
                    responsemod4_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 5:
                    responsemod5_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 6:
                    responsemod6_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 7:
                    responsemod7_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 8:
                    responsemod8_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
                if jentry % 10 != 9:
                    responsemod9_softdrop.Miss( GenJets[igen].M(), GenJets[igen].Perp(), weight )
fout.cd()

responsemod0.Write()
responsemod1.Write()
responsemod2.Write()
responsemod3.Write()
responsemod4.Write()
responsemod5.Write()
responsemod6.Write()
responsemod7.Write()
responsemod8.Write()
responsemod9.Write()

responsemod0_softdrop.Write()
responsemod1_softdrop.Write()
responsemod2_softdrop.Write()
responsemod3_softdrop.Write()
responsemod4_softdrop.Write()
responsemod5_softdrop.Write()
responsemod6_softdrop.Write()
responsemod7_softdrop.Write()
responsemod8_softdrop.Write()
responsemod9_softdrop.Write()

fout.Close()
