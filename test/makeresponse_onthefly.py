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

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 13000.])
nbinsPt = len(ptBinA) - 1
mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])
nbinsm = len(mBinA) - 1
response = ROOT.RooUnfoldResponse()
response.SetName("2d_response")
trueVarHist = ROOT.TH2F('truehist2d', 'truehist2D', nbinsPt, ptBinA, nbinsm, mBinA)
measVarHist = ROOT.TH2F('meashist2d', 'meashist2D', nbinsPt, ptBinA, nbinsm, mBinA)
response.Setup(measVarHist, trueVarHist)

response_pdfup = ROOT.RooUnfoldResponse()
response_pdfup.SetName("2d_response_pdfup")
response_pdfup.Setup(measVarHist, trueVarHist)

response_pdfdn = ROOT.RooUnfoldResponse()
response_pdfdn.SetName("2d_response_pdfdn")
response_pdfdn.Setup(measVarHist, trueVarHist)

response_softdrop_pdfup = ROOT.RooUnfoldResponse()
response_softdrop_pdfup.SetName("2d_response_softdrop_pdfup")
response_softdrop_pdfup.Setup(measVarHist, trueVarHist)

response_softdrop_pdfdn = ROOT.RooUnfoldResponse()
response_softdrop_pdfdn.SetName("2d_response_softdrop_pdfdn")
response_softdrop_pdfdn.Setup(measVarHist, trueVarHist)

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

response_jernom = ROOT.RooUnfoldResponse()
response_jernom.SetName("2d_response_jernom")
response_jernom.Setup(measVarHist, trueVarHist)

response_jmrup = ROOT.RooUnfoldResponse()
response_jmrup.SetName("2d_response_jmrup")
response_jmrup.Setup(measVarHist, trueVarHist)

response_jmrdn = ROOT.RooUnfoldResponse()
response_jmrdn.SetName("2d_response_jmrdn")
response_jmrdn.Setup(measVarHist, trueVarHist)

response_jmrnom = ROOT.RooUnfoldResponse()
response_jmrnom.SetName("2d_response_jmrnom")
response_jmrnom.Setup(measVarHist, trueVarHist)

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

response_softdrop_jernom = ROOT.RooUnfoldResponse()
response_softdrop_jernom.SetName("2d_response_softdrop_jernom")
response_softdrop_jernom.Setup(measVarHist, trueVarHist)

response_softdrop_jmrup = ROOT.RooUnfoldResponse()
response_softdrop_jmrup.SetName("2d_response_softdrop_jmrup")
response_softdrop_jmrup.Setup(measVarHist, trueVarHist)

response_softdrop_jmrdn = ROOT.RooUnfoldResponse()
response_softdrop_jmrdn.SetName("2d_response_softdrop_jmrdn")
response_softdrop_jmrdn.Setup(measVarHist, trueVarHist)

response_softdrop_jmrnom = ROOT.RooUnfoldResponse()
response_softdrop_jmrnom.SetName("2d_response_softdrop_jmrnom")
response_softdrop_jmrnom.Setup(measVarHist, trueVarHist)

h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, nbinsm, mBinA)
h_2DHisto_gen = ROOT.TH2F('PFJet_pt_m_AK8Gen', 'Generator Mass vs. P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, nbinsm, mBinA)

h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, nbinsm, mBinA)
h_2DHisto_genSD = ROOT.TH2F('PFJet_pt_m_AK8SDgen', 'Generator Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsPt, ptBinA, nbinsm, mBinA)


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

h_massup = ROOT.TH1F("h_massup", "JMR Up Variation", nbinsm, mBinA)
h_massdn = ROOT.TH1F("h_massdn", "JMR Down Variation", nbinsm, mBinA)
h_massnom = ROOT.TH1F("h_massnom", "JMR Nominal", nbinsm, mBinA)

h_massup_softdrop = ROOT.TH1F("h_massup_softdrop", "JMR Up Softdrop", nbinsm, mBinA)
h_massdn_softdrop = ROOT.TH1F("h_massdn_softdrop", "JMR Down Softdrop", nbinsm, mBinA)
h_massnom_softdrop = ROOT.TH1F("h_massnom_softdrop", "JMR Nominal Softdrop", nbinsm, mBinA)

h_mreco_mgen = ROOT.TH1F("h_mreco_mgen", "Reco Mass/Gen Mass", 1000, 0, 2)
h_ptreco_ptgen = ROOT.TH1F("h_ptreco_ptgen", "Reco Pt/Gen Pt", 1000, 0, 2)
h_mreco_mgen_softdrop = ROOT.TH1F("h_mreco_mgen_softdrop", "Reco Mass/Gen Mass Softdrop", 1000, 0, 2)
h_ptreco_ptgen_softdrop = ROOT.TH1F("h_ptreco_ptgen_softdrop", "Reco Pt/Gen Pt Softdrop", 1000, 0, 2)


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
    ROOT.TFile('qcd_pt170to300_newjec.root'),
    ROOT.TFile('qcd_pt300to470_newjec.root'),
    ROOT.TFile('qcd_pt470to600_newjec.root'),
    ROOT.TFile('qcd_pt600to800_newjec.root'),
    ROOT.TFile('qcd_pt800to1000_newjec.root'),
    ROOT.TFile('qcd_pt1000to1400_newjec.root'),
    ROOT.TFile('qcd_pt1400to1800_newjec.root'),
    ROOT.TFile('qcd_pt1800to2400_newjec.root'),
    ROOT.TFile('qcd_pt2400to3200_newjec.root'),
    ROOT.TFile('qcd_pt3200toInf_newjec.root'),
    ]
masslessSD = 0
qcdWeights =[
    0.036992995300193815,
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
            
            h_2DHisto_measSD.Fill( FatJetSD.Perp(), FatJetSD.M(), weight)

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
                                                
                valnom = getJER(FatJet.Eta(), 0)
                recopt = FatJet.Perp()
                genpt = GenJets[igen].Perp()
                deltapt = (recopt-genpt)*(valnom-1.0)
                smearnom = max(0.0, (recopt+deltapt)/recopt)
                
                jmrvalup = 1.2
                recomass = FatJet.M()
                genmass = GenJets[igen].M()
                deltamass = (recomass-genmass)*(jmrvalup-1.0)
                jmrup = max(0.0, (recomass+deltamass)/recomass) 
                
                jmrvaldn = 1.0
                recomass = FatJet.M()
                genmass = GenJets[igen].M()
                deltamass = (recomass-genmass)*(jmrvaldn-1.0)
                jmrdn = max(0.0, (recomass+deltamass)/recomass)

                jmrvalnom = 1.1
                recomass = FatJet.M()
                genmass = GenJets[igen].M()
                deltamass = (recomass-genmass)*(jmrvalnom-1.0)
                jmrnom = max(0.0, (recomass+deltamass)/recomass)


                response.Fill( FatJet.Perp(), FatJet.M(), GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecup.Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jecdn.Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerup.Fill( FatJet.Perp() * smearup, FatJet.M()* smearup, GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jerdn.Fill( FatJet.Perp() * smeardn, FatJet.M()* smeardn, GenJets[igen].Perp(), GenJets[igen].M(), weight )
                response_jernom.Fill(FatJet.Perp() * smearnom, FatJet.M()*smearnom, GenJets[igen].Perp(), GenJets[igen].M(), weight)
                
                response_jmrup.Fill( FatJet.Perp(), FatJet.M()*jmrup, GenJets[igen].Perp(), GenJets[igen].M(), weight)
                response_jmrdn.Fill( FatJet.Perp(), FatJet.M()*jmrdn, GenJets[igen].Perp(), GenJets[igen].M(), weight)
                response_jmrnom.Fill(FatJet.Perp(), FatJet.M()*jmrnom, GenJets[igen].Perp(), GenJets[igen].M(), weight)

                h_massup.Fill(FatJet.M()*jmrup, weight)
                h_massdn.Fill(FatJet.M()*jmrdn, weight)
                h_massnom.Fill(FatJet.M()*jmrnom, weight)

                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_pdfup.Fill( FatJet.Perp(), FatJet.M(), GenJets[igen].Perp(), GenJets[igen].M(), weight*pdfweight_up)
                    response_pdfdn.Fill( FatJet.Perp(), FatJet.M(), GenJets[igen].Perp(), GenJets[igen].M(), weight*pdfweight_dn)

                # Make some data-to-MC plots

#                h_2DHisto_meas.Fill( FatJetPt[ijet], FatJetMass[ijet], weight )
                h_pt_meas.Fill( FatJetPt[ijet] , weight )
                h_y_meas.Fill( FatJetRap[ijet] , weight )
                h_phi_meas.Fill( FatJetPhi[ijet] , weight )
                h_m_meas.Fill( FatJetMass[ijet] , weight )
                h_rho_meas.Fill( FatJetRhoRatio[ijet] , weight )
                h_tau21_meas.Fill( FatJetTau21[ijet] , weight )
                h_rho_vs_tau_meas.Fill( FatJetRhoRatio[ijet], FatJetTau21[ijet] , weight )
                if GenJets[igen].M() != 0:
                    h_mreco_mgen.Fill(FatJet.M()/GenJets[igen].M(), weight)
                else:
                    h_mreco_mgen.Fill(FatJet.M()/0.140, weight)
                h_ptreco_ptgen.Fill(FatJet.Perp()/GenJets[igen].Perp(), weight)        
            else : # Here we have a "Fake"
                response.Fake( FatJet.Perp(), FatJet.M(), weight )
                response_jecup.Fake( FatJet.Perp() * FatJetCorrUp[ijet], FatJet.M()* FatJetCorrUp[ijet], weight )
                response_jecdn.Fake( FatJet.Perp() * FatJetCorrDn[ijet], FatJet.M()* FatJetCorrDn[ijet], weight )
                response_jerup.Fake( FatJet.Perp() * smearup, FatJet.M() * smearup, weight )
                response_jerdn.Fake( FatJet.Perp() * smeardn, FatJet.M() * smeardn, weight ) 
                response_jernom.Fake(FatJet.Perp() * smearnom, FatJet.M() * smearnom,weight)
                response_jmrup.Fake( FatJet.Perp(), FatJet.M()*jmrup, weight)
                response_jmrnom.Fake(FatJet.Perp(), FatJet.M()*jmrnom, weight)
                response_jmrdn.Fake( FatJet.Perp(), FatJet.M()*jmrdn, weight)

                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_pdfup.Fake(FatJet.Perp(), FatJet.M(), weight*pdfweight_up)
                    response_pdfdn.Fake(FatJet.Perp(), FatJet.M(), weight*pdfweight_dn)


            if igenSD != None:
                
 #### be less conservative, define jes and jer for SD now
                valupSD = getJER(FatJetSD.Eta(), +1)
                recoptSD = FatJetSD.Perp()
                genptSD = GenJetsSD[igenSD].Perp()
                deltaptSD = (recoptSD-genptSD)*(valupSD-1.0)
                smearupSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)
        
                valdnSD = getJER(FatJetSD.Eta(), -1)
                recoptSD = FatJetSD.Perp()
                genptSD = GenJetsSD[igenSD].Perp()
                deltaptSD = (recoptSD-genptSD)*(valdnSD-1.0)
                smeardnSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)

                valnomSD = getJER(FatJetSD.Eta(), 0)
                recoptSD = FatJetSD.Perp()
                genptSD = GenJetsSD[igenSD].Perp()
                deltaptSD = (recoptSD-genptSD)*(valnomSD-1.0)
                smearnomSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)
        
                jmrvalnomSD = 1.1
                recomassSD = FatJetSD.M()
                genmassSD = GenJetsSD[igenSD].M()
                deltamassSD = (recomassSD-genmassSD)*(jmrvalnomSD-1.0)
                jmrnomSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)
  
                jmrvalupSD = 1.2
                recomassSD = FatJetSD.M()
                genmassSD = GenJetsSD[igenSD].M()
                deltamassSD = (recomassSD-genmassSD)*(jmrvalupSD-1.0)
                jmrupSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)

                jmrvaldnSD = 1.0
                recomassSD = FatJetSD.M()
                genmassSD = GenJetsSD[igenSD].M()
                deltamassSD = (recomassSD-genmassSD)*(jmrvaldnSD-1.0)
                jmrdnSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)

                response_softdrop.Fill( FatJetSD.Perp() , FatJetSD.M(), GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecup.Fill( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jecdn.Fill( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerup.Fill( FatJetSD.Perp()  * smearupSD, FatJetSD.M() * smearupSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jerdn.Fill( FatJetSD.Perp()  * smeardnSD, FatJetSD.M() * smeardnSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight )
                response_softdrop_jernom.Fill(FatJetSD.Perp() * smearnomSD, FatJetSD.M() * smearnomSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight)
                response_softdrop_jmrnom.Fill(FatJetSD.Perp(), FatJetSD.M()*jmrnomSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight)
                response_softdrop_jmrup.Fill(FatJetSD.Perp(), FatJetSD.M()*jmrupSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight)
                response_softdrop_jmrdn.Fill(FatJetSD.Perp(), FatJetSD.M()*jmrdnSD, GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight)
                h_massup_softdrop.Fill(FatJetSD.M()*jmrupSD, weight)
                h_massdn_softdrop.Fill(FatJetSD.M()*jmrdnSD, weight)
                h_massnom_softdrop.Fill(FatJetSD.M()*jmrnomSD, weight)
                if GenJetsSD[igenSD].M() != 0:
                    h_mreco_mgen_softdrop.Fill(FatJetSD.M()/GenJetsSD[igenSD].M(), weight)
                else:
                    h_mreco_mgen_softdrop.Fill(FatJetSD.M()/0.14, weight)
                    masslessSD += 1
                h_ptreco_ptgen_softdrop.Fill(FatJetSD.Perp()/GenJetsSD[igenSD].Perp(), weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_softdrop_pdfup.Fill( FatJetSD.Perp(), FatJetSD.M(), GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight*pdfweight_up)
                    response_softdrop_pdfdn.Fill( FatJetSD.Perp(), FatJetSD.M(), GenJetsSD[igenSD].Perp(), GenJetsSD[igenSD].M(), weight*pdfweight_dn)

                h_msd_meas.Fill( FatJetMassSoftDrop[ijet] , weight )
 #               h_2DHisto_measSD.Fill( FatJetPt[ijet], FatJetMassSoftDrop[ijet], weight )
            else:
                response_softdrop.Fake( FatJetSD.Perp() , FatJetSD.M(), weight )
                response_softdrop_jecup.Fake( FatJetSD.Perp()  * FatJetCorrUp[ijet], FatJetSD.M() * FatJetCorrUp[ijet], weight )
                response_softdrop_jecdn.Fake( FatJetSD.Perp()  * FatJetCorrDn[ijet], FatJetSD.M() * FatJetCorrDn[ijet], weight )
                response_softdrop_jerup.Fake( FatJetSD.Perp()  * smearupSD, FatJetSD.M() * smearupSD, weight )
                response_softdrop_jerdn.Fake( FatJetSD.Perp()  * smeardnSD, FatJetSD.M() * smeardnSD, weight )
                response_softdrop_jernom.Fake(FatJetSD.Perp() * smearnomSD, FatJetSD.M() * smearnomSD, weight)            
                response_softdrop_jmrnom.Fake(FatJetSD.Perp(), FatJetSD.M()*jmrnomSD, weight)
                response_softdrop_jmrup.Fake(FatJetSD.Perp(), FatJetSD.M()*jmrupSD, weight)
                response_softdrop_jmrdn.Fake(FatJetSD.Perp(), FatJetSD.M()*jmrdnSD, weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_softdrop_pdfup.Fake( FatJetSD.Perp(), FatJetSD.M(), weight*pdfweight_up)
                    response_softdrop_pdfdn.Fake( FatJetSD.Perp(), FatJetSD.M(), weight*pdfweight_dn)


                
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
                response_jernom.Miss(GenJets[igen].Perp(), GenJets[igen].M(), weight)
                response_jmrnom.Miss(GenJets[igen].Perp(), GenJets[igen].M(), weight)
                response_jmrup.Miss(GenJets[igen].Perp(), GenJets[igen].M(), weight)
                response_jmrdn.Miss(GenJets[igen].Perp(), GenJets[igen].M(), weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_pdfup.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight*pdfweight_up)
                    response_pdfdn.Miss( GenJets[igen].Perp(), GenJets[igen].M(), weight*pdfweight_dn)


            if ijetSD == None:
                response_softdrop.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jecdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jerdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jernom.Miss(GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight )
                response_softdrop_jmrnom.Miss(GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight)
                response_softdrop_jmrup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight)
                response_softdrop_jmrdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_softdrop_pdfup.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight*pdfweight_up)
                    response_softdrop_pdfdn.Miss( GenJetsSD[igen].Perp(), GenJetsSD[igen].M(), weight*pdfweight_dn)
print "Number of Massless Softdrop Jets: " + str(masslessSD)
fout.cd()
#response.Hresponse().Draw()
response.Write()
response_jecup.Write()
response_jecdn.Write()
response_jerup.Write()
response_jerdn.Write()
h_2DHisto_gen.Write()
h_2DHisto_meas.Write()
response_jmrup.Write()
response_jmrdn.Write()
response_jmrnom.Write()
response_jernom.Write()


response_pdfup.Write()
response_pdfdn.Write()
response_softdrop_pdfup.Write()
response_softdrop_pdfdn.Write()

h_mreco_mgen.Write()
h_ptreco_ptgen.Write()
h_mreco_mgen_softdrop.Write()
h_ptreco_ptgen_softdrop.Write()


h_2DHisto_measSD.Write()
h_2DHisto_genSD.Write()
response_softdrop.Write()
response_softdrop_jecup.Write()
response_softdrop_jecdn.Write()
response_softdrop_jerup.Write()
response_softdrop_jerdn.Write()
response_softdrop_jmrup.Write()
response_softdrop_jmrdn.Write()
response_softdrop_jmrnom.Write()
response_softdrop_jernom.Write()

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
