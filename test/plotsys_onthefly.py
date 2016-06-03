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

h_pt = []
h_m = []
h_msd = []

systs = [
    'nom', 'jesup', 'jesdn', 'jerup', 'jerdn', 'pdfup', 'pdfdn'
    ]
NOM=systs.index('nom')
JESUP=systs.index('jesup')
JESDN=systs.index('jesdn')
JERUP=systs.index('jerup')
JERDN=systs.index('jerdn')
PDFUP=systs.index('pdfup')
PDFDN=systs.index('pdfdn')

for isyst, syst in enumerate( systs) : 
    h_pt.append( ROOT.TH1F("h_pt_" + syst, ";Jet p_{T} (GeV); Number", 150, 0, 3000) )
    h_m.append( ROOT.TH1F("h_m_" + syst, ";Jet Mass (GeV); Number", 50, 0, 500 ) )
    h_msd.append( ROOT.TH1F("h_msd_" + syst, ";Jet Soft Drop Mass (GeV); Number", 50, 0, 500 ) )



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
fout = ROOT.TFile(options.outlabel + '_qcdmcsys.root', 'RECREATE')


for itree,t in enumerate(trees) :
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1,-1])
    FatJetPhi = array.array('f', [-1,-1])
    FatJetMass = array.array('f', [-1,-1])
    FatJetMassSoftDrop = array.array('f', [-1,-1])
    FatJetCorrUp = array.array('f', [-1,-1])
    FatJetCorrDn = array.array('f', [-1,-1])    
    NNPDF3weight_CorrDn = array.array('f', [-1])
    NNPDF3weight_CorrUp = array.array('f', [-1])
    NGenJet = array.array('i', [0] )
    GenJetPt = array.array('f', [-1,-1])
    GenJetMass = array.array('f', [-1,-1])
    GenJetMassSoftDrop = array.array('f', [-1,-1])
    
    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('NFatJet', 1)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus ('FatJetCorrUp', 1)
    t.SetBranchStatus ('FatJetCorrDn', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrDn', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrUp', 1)
    t.SetBranchStatus ('NGenJet', 1)
    t.SetBranchStatus ('GenJetPt', 1)
    t.SetBranchStatus ('GenJetMass', 1)
    t.SetBranchStatus ('GenJetMassSoftDrop', 1)
            
    t.SetBranchAddress ('NFatJet', NFatJet)
    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress ('FatJetCorrUp', FatJetCorrUp)
    t.SetBranchAddress ('FatJetCorrDn', FatJetCorrDn)
    t.SetBranchAddress ('NNPDF3weight_CorrUp', NNPDF3weight_CorrUp)
    t.SetBranchAddress ('NNPDF3weight_CorrDn', NNPDF3weight_CorrDn)
    t.SetBranchAddress ('NGenJet', NGenJet)
    t.SetBranchAddress ('GenJetPt', GenJetPt)
    t.SetBranchAddress ('GenJetMass', GenJetMass)
    t.SetBranchAddress ('GenJetMassSoftDrop', GenJetMassSoftDrop)    
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


        if NFatJet[0] < 2 :
            continue
        
        weight = qcdWeights[itree]

        maxjet = 0
        minjet = 1
        if FatJetPt[0] < FatJetPt[1] :
            maxjet = 1
            minjet = 0


        ptasym = (FatJetPt[maxjet] - FatJetPt[minjet])/(FatJetPt[maxjet] + FatJetPt[minjet])
        dphi = ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[minjet] )

        passkin = ptasym < 0.3 and dphi > 2.0
        if not passkin :
            continue

        
        h_pt[NOM].Fill( FatJetPt[0], weight )
        h_pt[NOM].Fill( FatJetPt[1], weight )
        h_m[NOM].Fill( FatJetMass[0], weight )
        h_m[NOM].Fill( FatJetMass[1], weight )
        h_msd[NOM].Fill( FatJetMassSoftDrop[0], weight )
        h_msd[NOM].Fill( FatJetMassSoftDrop[1], weight )

        h_pt[JESUP].Fill( FatJetPt[0] * FatJetCorrUp[0], weight )
        h_pt[JESUP].Fill( FatJetPt[1] * FatJetCorrUp[1], weight )
        h_m[JESUP].Fill( FatJetMass[0] * FatJetCorrUp[0], weight )
        h_m[JESUP].Fill( FatJetMass[1] * FatJetCorrUp[1], weight )
        h_msd[JESUP].Fill( FatJetMassSoftDrop[0] * FatJetCorrUp[0], weight )
        h_msd[JESUP].Fill( FatJetMassSoftDrop[1] * FatJetCorrUp[1], weight )
        
        h_pt[JESDN].Fill( FatJetPt[0] * FatJetCorrDn[0], weight )
        h_pt[JESDN].Fill( FatJetPt[1] * FatJetCorrDn[1], weight )
        h_m[JESDN].Fill( FatJetMass[0] * FatJetCorrDn[0], weight )
        h_m[JESDN].Fill( FatJetMass[1] * FatJetCorrDn[1], weight )
        h_msd[JESDN].Fill( FatJetMassSoftDrop[0] * FatJetCorrDn[0], weight )
        h_msd[JESDN].Fill( FatJetMassSoftDrop[1] * FatJetCorrDn[1], weight )

        h_pt[PDFUP].Fill( FatJetPt[0] , NNPDF3weight_CorrUp[0] * weight * weight )
        h_pt[PDFUP].Fill( FatJetPt[1] , NNPDF3weight_CorrUp[0] * weight )
        h_m[PDFUP].Fill( FatJetMass[0] , NNPDF3weight_CorrUp[0] * weight )
        h_m[PDFUP].Fill( FatJetMass[1] , NNPDF3weight_CorrUp[0] * weight )
        h_msd[PDFUP].Fill( FatJetMassSoftDrop[0] , NNPDF3weight_CorrUp[0] * weight )
        h_msd[PDFUP].Fill( FatJetMassSoftDrop[1] , NNPDF3weight_CorrUp[0] * weight )
        
        h_pt[PDFDN].Fill( FatJetPt[0] , NNPDF3weight_CorrDn[0] * weight )
        h_pt[PDFDN].Fill( FatJetPt[1] , NNPDF3weight_CorrDn[0] * weight )
        h_m[PDFDN].Fill( FatJetMass[0] , NNPDF3weight_CorrDn[0] * weight )
        h_m[PDFDN].Fill( FatJetMass[1] , NNPDF3weight_CorrDn[0] * weight )
        h_msd[PDFDN].Fill( FatJetMassSoftDrop[0] , NNPDF3weight_CorrDn[0] * weight )
        h_msd[PDFDN].Fill( FatJetMassSoftDrop[1] , NNPDF3weight_CorrDn[0] * weight )





        
fout.cd()
for ihist in xrange(0,len(h_pt)):
    h_pt[ihist].Write()
    h_m[ihist].Write()
    h_msd[ihist].Write()

fout.Close()

