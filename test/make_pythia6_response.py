#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt
from operator import itemgetter

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "qcdmc_stitched_pythia6.root",
                  help='Label for plots')


parser.add_option('--maxEvents', type='int', action='store',
                  dest='maxEvents',
                  default = None,
                  help='Max events')
parser.add_option('--weightCut', type='float', action='store',
                  dest='weightCut',
                  default=0.01,
                  help='Discard Events with weight above the cut')

(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math
import random

ROOT.gSystem.Load("RooUnfold/libRooUnfold")

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 13000.])
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

h_m_fulldist = ROOT.TH1F("PFJet_m_AK8_fulldist", "Full Spectrum Mass (GeV)", 50, 0, 1000)
h_pt_fulldist = ROOT.TH1F("PFJet_pt_AK8_fulldist", "Full Spectrum P_{T}", nbinsPt, ptBinA)
h_pt_fulldist_softdrop = ROOT.TH1F("PFJet_pt_AK8SD_fulldist", "Full Spectrum P_{T}", nbinsPt, ptBinA)
h_m_fulldist_softdrop = ROOT.TH1F("PFJet_m_AK8SD_fulldist", "Full Spectrum Mass (GeV)", 50, 0, 1000)

h_m_drmatched = ROOT.TH1F("PFJet_m_AK8_drmatched", "Mass After dR Matching", 50, 0, 1000)
h_pt_drmatched = ROOT.TH1F("PFJet_pt_AK8_drmatched", "P_{T} After dR Matching", nbinsPt, ptBinA )
h_m_softdrop_drmatched = ROOT.TH1F("PFJet_m_AK8SD_drmatched", "SoftDrop Match After dR Matching", 50, 0, 1000)
h_pt_softdrop_drmatched = ROOT.TH1F("PFJet_pt_AK8SD_drmatched", "SoftDrop P_{T} After dR Matching", nbinsPt, ptBinA)

h_mreco_mgen = ROOT.TH1F("h_mreco_mgen", "Reco Mass/Gen Mass", 1000, 0, 2)
h_ptreco_ptgen = ROOT.TH1F("h_recopt_genpt", "Reco Pt/Gen Pt", 1000, 0, 2)


h_mreco_mgen_softdrop = ROOT.TH1F("h_mreco_mgen_softdrop", "SoftDrop Reco Mass/Gen Mass", 1000, 0, 2)
h_ptreco_ptgen_softdrop = ROOT.TH1F("h_ptreco_ptgen_softdrop", "SoftDrop Reco Pt/Gen Pt", 1000, 0, 2)

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

lumi = 2100



qcdIn =[
    ROOT.TFile("qcd_ptflat_pythia6.root")]

qcdWeights =[
    1    ]

trees = []
# Append the actual TTrees
for iq in qcdIn:
    trees.append( iq.Get("TreeEXOVV") )
fout = ROOT.TFile(options.outlabel, 'RECREATE')


for itree,t in enumerate(trees) :
    Weight = array.array('f', [-1])
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1]*5)
    FatJetEta = array.array('f', [-1]*5)
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
    t.SetBranchStatus ('Weight', 1)
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
    t.SetBranchStatus ('GenJetPtSoftDrop', 1)
    t.SetBranchStatus ('FatJetPtSoftDrop', 1)
    
    t.SetBranchAddress ('Weight', Weight)
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
    t.SetBranchAddress ('GenJetPtSoftDrop', GenJetPtSoftDrop)
    entries = t.GetEntriesFast()
    print 'Processing tree ' + str(itree)


    if options.maxEvents != None :
        eventsToRun = options.maxEvents
    else :
        eventsToRun = entries
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
        FatJetz = []
        GenJetz = []
        weight = Weight[0]
        if 5e-7 < weight/(GenJetPt[0]+GenJetPt[1]):
            continue
        #print weight
        for igen in xrange( int(NGenJet[0]) ):
            GenJet = ROOT.TLorentzVector()
            GenJet.SetPtEtaPhiM( GenJetPt[igen], GenJetEta[igen], GenJetPhi[igen], GenJetMass[igen])
            GenJetSD = ROOT.TLorentzVector()
            GenJetSD.SetPtEtaPhiM( GenJetPtSoftDrop[igen], GenJetEta[igen], GenJetPhi[igen], GenJetMassSoftDrop[igen] )
            GenJets.append(GenJet)
            GenJetsSD.append(GenJetSD)
            GenJetsMassSD.append( GenJetMassSoftDrop[igen] )
            h_2DHisto_gen.Fill( GenJet.Perp(), GenJet.M(), weight )
            h_2DHisto_genSD.Fill( GenJetSD.Perp(), GenJetSD.M(), weight)
        



        if NFatJet[0] < 2 :
            continue
        if FatJetPt[0] < 220. :
            continue
        
        ptToSort = [ ]
        for ijet in xrange(NFatJet[0]):
            ptToSort.append( (ijet, FatJetPt[ijet] ) )

        ptSorted = sorted( ptToSort, key=itemgetter(1), reverse=True)

        indices = [ index[0] for index in ptSorted ]

        
        maxjet = indices[0]
        minjet = indices[1]
        pt0 = FatJetPt[maxjet]

        if pt0 > 13000. : # Sanity check
            continue
        if FatJetPt[minjet] < 220. : # require both jets to be >= 200 GeV
            continue


        ptasym = (FatJetPt[maxjet] - FatJetPt[minjet])/(FatJetPt[maxjet] + FatJetPt[minjet])
        dphi = ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[minjet] )


        passkin = ptasym < 0.3 and dphi > 2.0
        if not passkin :
            continue


        #First get the "Fills" and "Fakes" (i.e. we at least have a RECO jet)
        for ijet in [indices[0],indices[1]] :

            FatJet = ROOT.TLorentzVector()
            FatJet.SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])

            FatJetSD = ROOT.TLorentzVector()
            FatJetSD.SetPtEtaPhiM( FatJetPtSoftDrop[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMassSoftDrop[ijet]  )

            FatJetsSD.append(FatJetSD)
            FatJets.append(FatJet)




            h_2DHisto_meas.Fill( FatJet.Perp(), FatJet.M(), weight )
            h_2DHisto_measSD.Fill( FatJetSD.Perp(), FatJetSD.M(), weight)
 #           h_m_fulldist.Fill(FatJet.M(), weight)
 #           h_pt_fulldist.Fill(FatJet.Perp(), weight)
 #           h_pt_fulldist_softdrop.Fill(FatJetSD.Perp(), weight)
 #           h_m_fulldist_softdrop.Fill(FatJetSD.M(), weight)

            igen = getMatched( FatJet, GenJets )
            igenSD = getMatched(FatJetSD, GenJetsSD, dRMax=0.5)
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
                

#                h_ptreco_ptgen.Fill(FatJet.Perp()/GenJets[igen].Perp(), weight)
#                h_mreco_mgen.Fill(FatJet.M()/GenJets[igen].M(), weight)

#                h_m_drmatched.Fill(FatJet.M(), weight)
#                h_pt_drmatched.Fill(FatJet.Perp(), weight) 
            else : # Here we have a "Fake"
                response.Fake( FatJet.Perp(), FatJet.M(), weight )
                response_jecup.Fake( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], weight )
                response_jecdn.Fake( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], weight )
                response_jerup.Fake( FatJet.Perp() * smearup, FatJet.M() * smearup, weight )
                response_jerdn.Fake( FatJet.Perp() * smeardn, FatJet.M() * smeardn, weight )

            if igenSD != None:
                response_softdrop.Fill( FatJetSD.Perp() , FatJetSD.M(), GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecup.Fill( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecdn.Fill( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerup.Fill( FatJetSD.Perp()  * smearup, FatJetSD.M() * smearup, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerdn.Fill( FatJetSD.Perp()  * smeardn, FatJetSD.M() * smeardn, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
#                h_m_softdrop_drmatched.Fill(FatJetSD.M(), weight)
#                h_pt_softdrop_drmatched.Fill(FatJetSD.Perp(), weight)
#                h_mreco_mgen_softdrop.Fill(FatJetSD.M()/GenJetsSD[igenSD].M(), weight)
#                h_ptreco_ptgen_softdrop.Fill(FatJetSD.Perp()/GenJetsSD[igenSD].Perp(), weight)
            else:
                response_softdrop.Fake( FatJetSD.Perp() , FatJetSD.M(), weight )
                response_softdrop_jecup.Fake( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], weight )
                response_softdrop_jecdn.Fake( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], weight )
                response_softdrop_jerup.Fake( FatJetSD.Perp()  * smearup, FatJetSD.M() * smearup, weight )
                response_softdrop_jerdn.Fake( FatJetSD.Perp()  * smeardn, FatJetSD.M() * smeardn, weight )

        # Now get the "Misses" (i.e. we have no RECO jet)
        for igen in xrange( int(NGenJet[0]) ):
            ijet = getMatched( GenJets[igen], FatJets )
            ijetSD = getMatched( GenJetsSD[igen], FatJetsSD, dRMax=0.5 )
            if ijet == None :
                response.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecup.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecdn.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerup.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerdn.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight )


            if ijetSD == None:
                response_softdrop.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )



fout.cd()
#response.Hresponse().Draw()
response.Write()
response_jecup.Write()
response_jecdn.Write()
response_jerup.Write()
response_jerdn.Write()
h_2DHisto_gen.Write()
h_2DHisto_meas.Write()

#h_m_fulldist.Write()
#h_pt_fulldist.Write()
#h_m_fulldist_softdrop.Write()
#h_pt_fulldist_softdrop.Write()

#h_m_drmatched.Write()
#h_pt_drmatched.Write()
#h_m_softdrop_drmatched.Write()
#h_pt_softdrop_drmatched.Write()

#h_mreco_mgen.Write()
#h_ptreco_ptgen.Write()
#h_mreco_mgen_softdrop.Write()
#h_ptreco_ptgen_softdrop.Write()




h_2DHisto_measSD.Write()
h_2DHisto_genSD.Write()
response_softdrop.Write()
response_softdrop_jecup.Write()
response_softdrop_jecdn.Write()
response_softdrop_jerup.Write()
response_softdrop_jerdn.Write()

fout.Close()
