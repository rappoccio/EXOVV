#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt

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


h_pt_meas = ROOT.TH1F("h_pt_meas", ";Jet p_{T} (GeV); Number", 150, 0, 3000)
h_y_meas = ROOT.TH1F("h_y_meas", ";Jet Rapidity; Number", 50, -2.5, 2.5 )
h_phi_meas = ROOT.TH1F("h_phi_meas", ";Jet #phi (radians); Number", 50, -ROOT.TMath.Pi(), ROOT.TMath.Pi() )
h_m_meas = ROOT.TH1F("h_m_meas", ";Jet Mass (GeV); Number", 50, 0, 500 )
h_msd_meas = ROOT.TH1F("h_msd_meas", ";Jet Soft Drop Mass (GeV); Number", 50, 0, 500 )
h_rho_meas = ROOT.TH1F("h_rho_meas", ";Jet (m/p_{T}R)^{2}; Number", 100, 0, 1.0 )
h_tau21_meas = ROOT.TH1F("h_tau21_meas", ";Jet #tau_{2}/#tau_{1}; Number", 50, 0, 1.0 )
h_dphi_meas = ROOT.TH1F("h_dphi_meas", ";Jet #phi (radians); Number", 50, 0, ROOT.TMath.TwoPi() )
h_ptasym_meas = ROOT.TH1F("h_ptasym_meas", ";Jet (p_{T1} - p_{T2}) / (p_{T1} + p_{T2}); Number", 50, 0, 1.0 )
h_rho_vs_tau_meas = ROOT.TH2F("h_rho_vs_tau21_meas", ";Jet (m/p_{T}R)^{2};Jet #tau_{2}/#tau_{1}", 100, 0, 1.0, 50, 0, 1.0 )


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
    ROOT.TFile('qcd_pt170to300_pdf_tree.root'),
    ROOT.TFile('qcd_pt300to470_pdf_tree.root'),
    ROOT.TFile('qcd_pt470to600_pdf_tree.root'),
    ROOT.TFile('qcd_pt600to800_pdf_tree.root'),
    ROOT.TFile('qcd_pt800to1000_pdf_tree.root'),
    ROOT.TFile('qcd_pt1000to1400_pdf_tree.root'),
    ROOT.TFile('qcd_pt1400to1800_pdf_tree.root'),
    ROOT.TFile('qcd_pt1800to2400_pdf_tree.root'),
    ROOT.TFile('qcd_pt2400to3200_pdf_tree.root'),
    ROOT.TFile('qcd_pt3200toInf_pdf_tree.root'),
    ]

qcdWeights =[
    0.10858888888888889,
#    0.033811597704377146,   #### Processing is broken for this, for now run on partial sample
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

trees = []
# Append the actual TTrees
for iq in qcdIn:
    trees.append( iq.Get("TreeEXOVV") )
fout = ROOT.TFile(options.outlabel + '_qcdmc.root', 'RECREATE')


for itree,t in enumerate(trees) :
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1,-1])
    FatJetEta = array.array('f', [-1,-1])
    FatJetRap = array.array('f', [-1,-1])
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
    GenJetPtSoftDrop = array.array('f', [-1, -1])
    
    
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

                
        if dphi > 2.0 :
            h_ptasym_meas.Fill( ptasym, weight )
        if ptasym < 0.3 :
            h_dphi_meas.Fill( dphi, weight )

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
            h_2DHisto_gen.Fill( GenJet.Perp(), GenJet.M(), weight )
            h_2DHisto_genSD.Fill( GenJetSD.Perp(), GenJetSD.M(), weight)
        # First get the "Fills" and "Fakes" (i.e. we at least have a RECO jet)
        for ijet in xrange( int(NFatJet[0]) ):
            
            FatJet = ROOT.TLorentzVector()
            FatJet.SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])
            
            FatJetSD = ROOT.TLorentzVector()
            FatJetSD.SetPtEtaPhiM( FatJetPtSoftDrop[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMassSoftDrop[ijet]  )
            
            FatJetsSD.append(FatJetSD)
            FatJets.append(FatJet)
           
            h_2DHisto_meas.Fill( FatJet.Perp(), FatJet.M(), weight )
            
            h_2DHisto_measSD.Fill( FatJetSD.Perp(), FatJetSD.M())

            igen = getMatched( FatJet, GenJets )

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
                
                response_softdrop.Fill( FatJetSD.Perp() , FatJetSD.M(), GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecup.Fill( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecdn.Fill( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerup.Fill( FatJetSD.Perp()  * smearup, FatJetSD.M() * smearup, GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerdn.Fill( FatJetSD.Perp()  * smeardn, FatJetSD.M() * smeardn, GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )




                # Make some data-to-MC plots

                h_2DHisto_meas.Fill( FatJetPt[ijet], FatJetMass[ijet], weight )
                h_2DHisto_measSD.Fill( FatJetPt[ijet], FatJetMassSoftDrop[ijet], weight )
                h_pt_meas.Fill( FatJetPt[ijet] , weight )
                h_y_meas.Fill( FatJetRap[ijet] , weight )
                h_phi_meas.Fill( FatJetPhi[ijet] , weight )
                h_m_meas.Fill( FatJetMass[ijet] , weight )
                h_msd_meas.Fill( FatJetMassSoftDrop[ijet] , weight )
                h_rho_meas.Fill( FatJetRhoRatio[ijet] , weight )
                h_tau21_meas.Fill( FatJetTau21[ijet] , weight )
                h_rho_vs_tau_meas.Fill( FatJetRhoRatio[ijet], FatJetTau21[ijet] , weight )
                
            else : # Here we have a "Fake"
                response.Fake( FatJet.Perp(), FatJet.M(), weight )
                response_jecup.Fake( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], weight )
                response_jecdn.Fake( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], weight )
                response_jerup.Fake( FatJet.Perp() * smearup, FatJet.M() * smearup, weight )
                response_jerdn.Fake( FatJet.Perp() * smeardn, FatJet.M() * smeardn, weight )
                
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

h_2DHisto_measSD.Write()
h_2DHisto_genSD.Write()
response_softdrop.Write()
response_softdrop_jecup.Write()
response_softdrop_jecdn.Write()
response_softdrop_jerup.Write()
response_softdrop_jerdn.Write()


h_pt_meas.Write()
h_y_meas.Write()
h_phi_meas.Write()
h_m_meas.Write()
h_msd_meas.Write()
h_rho_meas.Write()
h_tau21_meas.Write()
h_dphi_meas.Write()
h_ptasym_meas.Write()
h_rho_vs_tau_meas.Write()

fout.Close()
