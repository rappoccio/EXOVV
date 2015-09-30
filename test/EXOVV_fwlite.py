#! /usr/bin/env python

##################
# Editting flags
# #!!! Error or Something fishy
# #{ #} Start and stop loop (so reading indents isn't so bad
# #^ Plotting
# #@ New section (muons, electrons, AK4 jets etc.)
# #$ Cuts
##################


#@ CONFIGURATION

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', type='string', action='store',
                  default='outplots.root',
                  dest='outname',
                  help='Name of output file')

parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print debugging info')

parser.add_option('--isData', action='store_true',
                  default=False,
                  dest='isData',
                  help='Run on Data?')


parser.add_option('--deweightFlat', action='store_true',
                  default=False,
                  dest='deweightFlat',
                  help='Deweight a flat pthat sample')

parser.add_option('--selection', type='int', action='store',
                  default=-1,
                  dest='selection',
                  help='Leptonic (0), SemiLeptonic (1) or AllHadronic (2)')

parser.add_option('--maxevents', type='int', action='store',
                  default=-1,
                  dest='maxevents',
                  help='Number of events to run. -1 is all events')

parser.add_option('--maxjets', type='int', action='store',
                  default=999,
                  dest='maxjets',
                  help='Number of jets to plot. To plot all jets, set to a big number like 999')


parser.add_option('--bdisc', type='string', action='store',
                  default='combinedInclusiveSecondaryVertexV2BJetTags',
                  dest='bdisc',
                  help='Name of output file')


parser.add_option('--bDiscMin', type='float', action='store',
                  default=0.679,
                  dest='bDiscMin',
                  help='Minimum b discriminator')

parser.add_option('--minMuonPt', type='float', action='store',
                  default=20.,
                  dest='minMuonPt',
                  help='Minimum PT for muons')

parser.add_option('--maxMuonEta', type='float', action='store',
                  default=2.1,
                  dest='maxMuonEta',
                  help='Maximum muon pseudorapidity')

parser.add_option('--minElectronPt', type='float', action='store',
                  default=20.,
                  dest='minElectronPt',
                  help='Minimum PT for electrons')

parser.add_option('--maxElectronEta', type='float', action='store',
                  default=2.5,
                  dest='maxElectronEta',
                  help='Maximum electron pseudorapidity')

parser.add_option('--minZLepPt', type='float', action='store',
                  default=200.,
                  dest='minZLepPt',
                  help='Minimum PT for leptonic Z candidate')

parser.add_option('--minWLepPt', type='float', action='store',
                  default=200.,
                  dest='minWLepPt',
                  help='Minimum PT for leptonic W candidate')

parser.add_option('--minAK4Pt', type='float', action='store',
                  default=30.,
                  dest='minAK4Pt',
                  help='Minimum PT for AK4 jets')

parser.add_option('--maxAK4Rapidity', type='float', action='store',
                  default=2.4,
                  dest='maxAK4Rapidity',
                  help='Maximum AK4 rapidity')

parser.add_option('--minAK8Pt', type='float', action='store',
                  default=250.,
                  dest='minAK8Pt',
                  help='Minimum PT for AK8 jets')


parser.add_option('--maxAK8Pt', type='float', action='store',
                  default=13000.,
                  dest='maxAK8Pt',
                  help='Maximum PT for AK8 jets')

parser.add_option('--maxAK8Rapidity', type='float', action='store',
                  default=2.4,
                  dest='maxAK8Rapidity',
                  help='Maximum AK8 rapidity')


parser.add_option('--minMassCut', type='float', action='store',
                  default=50.,
                  dest='minMassCut',
                  help='Minimum Mass Pairing Cut for CMS Combined Tagger')

parser.add_option('--mAK8SoftDropCut', type='float', action='store',
                  default=50.,
                  dest='mAK8SoftDropCut',
                  help='SoftDrop mass Cut for CMS Combined Tagger')

parser.add_option('--tau21Cut', type='float', action='store',
                  default=0.6,
                  dest='tau21Cut',
                  help='Tau2 / Tau1 n-subjettiness cut')



parser.add_option('--sdmassCutLo', type='float', action='store',
                  default=60.,
                  dest='sdmassCutLo',
                  help='Lower softdrop mass cut')


parser.add_option('--sdmassCutHi', type='float', action='store',
                  default=13000.,
                  dest='sdmassCutHi',
                  help='Upper softdrop mass cut')

parser.add_option('--makeMistag', action='store_true',
                  default=False,
                  dest='makeMistag',
                  help='Create the mistag rate')

parser.add_option('--predRate', type='string', action='store',
                  default='mistagRate_mod.root',
                  dest='predRate',
                  help='Name of Predicted Distribution file')


parser.add_option('--massModMistagFile', type='string', action='store',
                  default=None,
                  dest='massModMistagFile',
                  help='Name of file for mass-modified mistag approach')

parser.add_option('--applyFilters', action='store_true',
                  default=False,
                  dest='applyFilters',
                  help='Apply MET filters')

parser.add_option('--applyHadronicTriggers', action='store_true',
                  default=False,
                  dest='applyHadronicTriggers',
                  help='Apply triggers')


parser.add_option('--applyWEleTriggers', action='store_true',
                  default=False,
                  dest='applyWEleTriggers',
                  help='Apply W electron triggers')


parser.add_option('--applyWMuoTriggers', action='store_true',
                  default=False,
                  dest='applyWMuoTriggers',
                  help='Apply W muon triggers')


parser.add_option('--applyZTriggers', action='store_true',
                  default=False,
                  dest='applyZTriggers',
                  help='Apply Z triggers')

parser.add_option('--signalTriggers', action='store_true',
                  default=False,
                  dest='signalTriggers',
                  help='Apply only "signal" triggers with prescale = 1')

parser.add_option('--useJetPtTrigs', action='store_true',
                  default=False,
                  dest='useJetPtTrigs',
                  help='Use single jet triggers instead of HT')


parser.add_option('--speedyHtMin', type='float', action='store',
                  default=None,
                  dest='speedyHtMin',
                  help='Minimum AK8 Jet HT from whatever is in the ntuple to make it faster')

parser.add_option('--htMin', type='float', action='store',
                  default=None,
                  dest='htMin',
                  help='Minimum AK8 Jet HT with right jet corrections')

parser.add_option('--puFile', type='string', action='store',
                  default=None,
                  dest='puFile',
                  help='Name of Pileup File, try "pileup_reweight.root" ')


(options, args) = parser.parse_args()
argv = []


#@ FWLITE STUFF

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gSystem.Load("libAnalysisPredictedDistribution")
import copy
import random
import array


# Old cuts : 
#pt0cuts = [150., 200., 300., 400., 500., 600., 700., 800. ]
# Updated cuts :
pt0cuts = [150., 200., 240., 320., 380., 480., 540., 600. ]
ptTrigsToGet = [
#    'HLT_PFJet60',
    'HLT_PFJet80', # 150
    'HLT_PFJet140',# 200
    'HLT_PFJet200',# 240
    'HLT_PFJet260',# 320
    'HLT_PFJet320',# 380
    'HLT_PFJet400',# 500
    'HLT_PFJet450',# 540
    'HLT_PFJet500' # 600
    ]
    
htcuts = [#200., 250., 300.,
          480., 540., 680., 750., 900.]
htcutsa = array.array('d', htcuts)
htcutsa.append( 7000. )
htTrigsToGet = [
    #'HLT_PFHT200',
    #'HLT_PFHT250',
    #'HLT_PFHT300',
    #'HLT_PFHT350',
    'HLT_PFHT400',
    'HLT_PFHT475',
    'HLT_PFHT600',
    'HLT_PFHT650',
    'HLT_PFHT800'
    ]


if not options.useJetPtTrigs :
    trigsToGet = htTrigsToGet
else :
    trigsToGet = ptTrigsToGet


    
def trigHelperPt( pt0, trigs ) :

    if pt0 < pt0cuts[0] :
        return False, None
    
    npt0cuts = len( pt0cuts )
    ipt0 = 0
    for ipt0 in xrange( npt0cuts-1, 0, -1) :
        if pt0 > pt0cuts[ipt0] :
            break
    ipass = trigs[ipt0]
    return ipass, ipt0

def trigHelperHT( ht, trigs ) :    
    nhtcuts = len( htcuts )
    iht = 0
    for iht in xrange( nhtcuts-1,0,-1) :
        if ht > htcuts[iht] :
            break
    ipass = trigs[iht]
    return ipass, iht
    
    
              
#@ Predicted distribution
if options.makeMistag == False : 
    fpreddist = ROOT.TFile(options.predRate)
    hpred = fpreddist.Get('rLoMod' )
    if options.massModMistagFile != None :
        # Get the mass-modified "prior" from QCD MC.
        # Here, we select a deviate from the QCD MC jet mass distribution
        # after the cuts are made. This is then used in the MVV calculation.        
        fmassMod = ROOT.TFile(options.massModMistagFile)
        hmassMod = fmassMod.Get("h2_msoftdropAK8").Clone()
        hmassMod.SetName('hmassMod')
        bin1 = hmassMod.GetXaxis().FindBin( 0.0 )
        bin2 = hmassMod.GetXaxis().FindBin( options.sdmassCutLo )
        bin3 = hmassMod.GetXaxis().FindBin( options.sdmassCutHi )
        for ibin in range ( bin1, bin2 ) :
            hmassMod.SetBinContent(ibin, 0.0 )
        for ibin in range ( bin3, hmassMod.GetNbinsX() ) :
            hmassMod.SetBinContent(ibin, 0.0 )
        hmassMod.Scale( 1.0 / hmassMod.Integral() )
        ROOT.SetOwnership( hmassMod, False )


#@ Labels and Handles

#generator labels and handles
h_generator = Handle("GenEventInfoProduct")
l_generator = ("generator")

#muon labels and handles
h_muPt = Handle("std::vector<float>")
l_muPt = ("muons" , "muPt")
h_muEta = Handle("std::vector<float>")
l_muEta = ("muons" , "muEta")
h_muPhi = Handle("std::vector<float>")
l_muPhi = ("muons" , "muPhi")
h_muTight = Handle("std::vector<float>")
l_muTight = ("muons" , "muIsTightMuon" )
h_muLoose = Handle("std::vector<float>")
l_muLoose = ("muons" , "muIsLooseMuon" )
h_muMass = Handle("std::vector<float>")
l_muMass = ("muons" , "muMass")
h_muDz = Handle("std::vector<float>")
l_muDz = ("muons", "muDz")
h_muCharge = Handle("std::vector<float>")
l_muCharge = ("muons", "muCharge")
h_muIso04 = Handle("std::vector<float>")
l_muIso04 = ("muons", "muIso04")

h_muKey = Handle("std::vector<float>")
l_muKey = ("muons", "muKey")

#electron label and handles
h_elPt = Handle("std::vector<float>")
l_elPt = ("electrons" , "elPt")
h_elEta = Handle("std::vector<float>")
l_elEta = ("electrons" , "elEta")
h_elPhi = Handle("std::vector<float>")
l_elPhi = ("electrons" , "elPhi")
h_elTight = Handle("std::vector<float>")
l_elTight = ("electrons" , "elisTight" )
h_elLoose = Handle("std::vector<float>")
l_elLoose = ("electrons" , "elisLoose" )
h_eldEtaIn = Handle("std::vector<float>")
l_eldEtaIn = ( "electrons" , "eldEtaIn" )
h_eldPhiIn = Handle("std::vector<float>")
l_eldPhiIn = ( "electrons" , "eldPhiIn" )
h_elHoE = Handle("std::vector<float>")
l_elHoE = ( "electrons" , "elHoE" )
h_elfull5x5siee = Handle("std::vector<float>")
l_elfull5x5siee = ( "electrons" , "elfull5x5siee")
h_elE = Handle("std::vector<float>")
l_elE = ( "electrons" , "elE" )
h_elD0 = Handle("std::vector<float>")
l_elD0 = ( "electrons" , "elD0" )
h_elDz = Handle("std::vector<float>")
l_elDz = ( "electrons" , "elDz")
h_elIso03 = Handle("std::vector<float>")
l_elIso03 = ( "electrons" , "elIso03" )
h_elisVeto = Handle("std::vector<float>")
l_elisVeto = ( "electrons" , "elisVeto" )
h_elhasMatchedConVeto = Handle("std::vector<float>")
l_elhasMatchedConVeto = ( "electrons" , "elhasMatchedConVeto" )
h_elooEmooP = Handle("std::vector<float>")
l_elooEmooP = ( "electrons" , "elooEmooP" )
h_elMass = Handle("std::vector<float>")
l_elMass = ( "electrons" , "elMass" )
h_elscEta = Handle("std::vector<float>")
l_elscEta = ( "electrons" , "elscEta" )
h_elCharge = Handle("std::vector<float>")
l_elCharge = ( "electrons" , "elCharge" )
h_elmissHits = Handle("std::vector<float>")
l_elmissHits = ( "electrons" , "elmissHits" )

h_elKey = Handle("std::vector<float>")
l_elKey = ( "electrons" , "elKey" )

#AK4 Jet Label and Handles
h_jetsAK4Pt = Handle("std::vector<float>")
l_jetsAK4Pt = ("jetsAK4" , "jetAK4Pt") #
h_jetsAK4Eta = Handle("std::vector<float>")
l_jetsAK4Eta = ("jetsAK4" , "jetAK4Eta")
h_jetsAK4Phi = Handle("std::vector<float>")
l_jetsAK4Phi = ("jetsAK4" , "jetAK4Phi")
h_jetsAK4Mass = Handle("std::vector<float>")
l_jetsAK4Mass = ("jetsAK4" , "jetAK4Mass")
h_jetsAK4Energy = Handle("std::vector<float>")
l_jetsAK4Energy = ("jetsAK4" , "jetAK4E") #check! is this energy?
h_jetsAK4JEC = Handle("std::vector<float>")
l_jetsAK4JEC = ("jetsAK4" , "jetAK4jecFactor0") 
h_jetsAK4CSV = Handle("std::vector<float>")
l_jetsAK4CSV = ("jetsAK4" , "jetAK4CSV")
h_jetsAK4NumDaughters = Handle("std::vector<float>")
l_jetsAK4NumDaughters = ( "jetsAK4" , "jetAK4numberOfDaughters" )
h_jetsAK4Area = Handle("std::vector<float>")
l_jetsAK4Area = ( "jetsAK4" , "jetAK4jetArea" )


h_pv_chi = Handle("std::vector<float>")
l_pv_chi = ( "vertexInfo", "chi" )
h_pv_rho = Handle("std::vector<float>")
l_pv_rho = ( "vertexInfo", "rho" )
h_pv_z = Handle("std::vector<float>")
l_pv_z = ( "vertexInfo", "z" )
h_pv_ndof = Handle("std::vector<std::int>")
l_pv_ndof = ( "vertexInfo", "ndof" )

h_puNtrueInt = Handle("std::int")
l_puNtrueInt = ( "eventUserData" , "puNtrueInt" )

h_NPV = Handle("std::int")
l_NPV = ( "eventUserData" , "npv" )

h_jetsAK4Keys = Handle("std::vector<std::vector<int> >")
l_jetsAK4Keys = ( "jetKeysAK4" , "" )

h_jetsAK4nHadEnergy = Handle("std::vector<float>")
l_jetsAK4nHadEnergy = ("jetsAK4" , "jetAK4neutralHadronEnergy")
h_jetsAK4nEMEnergy = Handle("std::vector<float>")
l_jetsAK4nEMEnergy = ("jetsAK4" , "jetAK4neutralEmEnergy")
h_jetsAK4HFHadronEnergy = Handle("std::vector<float>")
l_jetsAK4HFHadronEnergy = ("jetsAK4" , "jetAK4HFHadronEnergy")
h_jetsAK4cHadEnergy = Handle("std::vector<float>")
l_jetsAK4cHadEnergy = ("jetsAK4" , "jetAK4chargedHadronEnergy")
h_jetsAK4cEMEnergy = Handle("std::vector<float>")
l_jetsAK4cEMEnergy = ("jetsAK4" , "jetAK4chargedEmEnergy")
h_jetsAK4numDaughters = Handle("std::vector<float>")
l_jetsAK4numDaughters = ("jetsAK4" , "jetAK4numberOfDaughters")
h_jetsAK4cMultip = Handle("std::vector<float>")
l_jetsAK4cMultip = ("jetsAK4" , "jetAK4chargedMultiplicity")
h_jetsAK4Y = Handle("std::vector<float>")
l_jetsAK4Y = ("jetsAK4" , "jetAK4Y")

#Rho
h_rho = Handle("double")
l_rho = ("fixedGridRhoFastjetAll", "")

#MET label and Handles
h_metPt = Handle("std::vector<float>")
l_metPt = ("met" , "metPt")
h_metPx = Handle("std::vector<float>")
l_metPx = ("met" , "metPx")
h_metPy = Handle("std::vector<float>")
l_metPy = ("met" , "metPy")
h_metPhi = Handle("std::vector<float>")
l_metPhi = ("met" , "metPhi")

#AK8 Jets label and Handles
h_jetsAK8Pt = Handle("std::vector<float>")
l_jetsAK8Pt = ("jetsAK8" , "jetAK8Pt") #
h_jetsAK8Eta = Handle("std::vector<float>")
l_jetsAK8Eta = ("jetsAK8" , "jetAK8Eta")
h_jetsAK8Phi = Handle("std::vector<float>")
l_jetsAK8Phi = ("jetsAK8" , "jetAK8Phi")
h_jetsAK8Mass = Handle("std::vector<float>")
l_jetsAK8Mass = ("jetsAK8" , "jetAK8Mass")
h_jetsAK8Energy = Handle("std::vector<float>")
l_jetsAK8Energy = ("jetsAK8" , "jetAK8E") #check! is this energy?
h_jetsAK8JEC = Handle("std::vector<float>")
l_jetsAK8JEC = ("jetsAK8" , "jetAK8jecFactor0")
h_jetsAK8Y = Handle("std::vector<float>")
l_jetsAK8Y = ("jetsAK8" , "jetAK8Y")

h_jetsAK8nHadEnergy = Handle("std::vector<float>")
l_jetsAK8nHadEnergy = ("jetsAK8" , "jetAK8neutralHadronEnergy")
h_jetsAK8nEMEnergy = Handle("std::vector<float>")
l_jetsAK8nEMEnergy = ("jetsAK8" , "jetAK8neutralEmEnergy")
h_jetsAK8HFHadronEnergy = Handle("std::vector<float>")
l_jetsAK8HFHadronEnergy = ("jetsAK8" , "jetAK8HFHadronEnergy")
h_jetsAK8cHadEnergy = Handle("std::vector<float>")
l_jetsAK8cHadEnergy = ("jetsAK8" , "jetAK8chargedHadronEnergy")
h_jetsAK8cEMEnergy = Handle("std::vector<float>")
l_jetsAK8cEMEnergy = ("jetsAK8" , "jetAK8chargedEmEnergy")
h_jetsAK8numDaughters = Handle("std::vector<float>")
l_jetsAK8numDaughters = ("jetsAK8" , "jetAK8numberOfDaughters")
h_jetsAK8cMultip = Handle("std::vector<float>")
l_jetsAK8cMultip = ("jetsAK8" , "jetAK8chargedMultiplicity")
h_jetsAK8Y = Handle("std::vector<float>")
l_jetsAK8Y = ("jetsAK8" , "jetAK8Y")

h_jetsAK8Keys = Handle("std::vector<std::vector<int> >")
l_jetsAK8Keys = ( "jetKeysAK8" , "" )

h_jetsAK8SoftDropMass = Handle("std::vector<float>")
l_jetsAK8SoftDropMass = ("jetsAK8", "jetAK8softDropMass" )
h_jetsAK8TrimMass = Handle("std::vector<float>")
l_jetsAK8TrimMass = ("jetsAK8", "jetAK8trimmedMass" )
h_jetsAK8PrunMass = Handle("std::vector<float>")
l_jetsAK8PrunMass = ("jetsAK8", "jetAK8prunedMass" )
h_jetsAK8FiltMass = Handle("std::vector<float>")
l_jetsAK8FiltMass = ("jetsAK8", "jetAK8filteredMass" )
h_jetsAK8Tau1 = Handle("std::vector<float>")
l_jetsAK8Tau1 = ("jetsAK8", "jetAK8tau1" )
h_jetsAK8Tau2 = Handle("std::vector<float>")
l_jetsAK8Tau2 = ("jetsAK8", "jetAK8tau2" )
h_jetsAK8Tau3 = Handle("std::vector<float>")
l_jetsAK8Tau3 = ("jetsAK8", "jetAK8tau3" )
h_jetsAK8nSubJets = Handle("std::vector<float>")
l_jetsAK8nSubJets = ("jetsAK8", "jetAK8nSubJets" )
h_jetsAK8minmass = Handle("std::vector<float>")
l_jetsAK8minmass = ("jetsAK8", "jetAK8minmass" )
h_jetsAK8Area = Handle("std::vector<float>")
l_jetsAK8Area = ( "jetsAK8" , "jetAK8jetArea" )


h_jetsAK8vSubjetIndex0 = Handle("std::vector<float>")
l_jetsAK8vSubjetIndex0 = ("jetsAK8", "jetAK8vSubjetIndex0")
h_jetsAK8vSubjetIndex1 = Handle("std::vector<float>")
l_jetsAK8vSubjetIndex1 = ("jetsAK8", "jetAK8vSubjetIndex1")

h_subjetsAK8Pt = Handle( "std::vector<float>")
l_subjetsAK8Pt = ("subjetsAK8", "subjetAK8Pt")
h_subjetsAK8Eta = Handle( "std::vector<float>")
l_subjetsAK8Eta = ("subjetsAK8", "subjetAK8Eta")
h_subjetsAK8Phi = Handle( "std::vector<float>")
l_subjetsAK8Phi = ("subjetsAK8", "subjetAK8Phi")
h_subjetsAK8Mass = Handle( "std::vector<float>")
l_subjetsAK8Mass = ("subjetsAK8", "subjetAK8Mass")
h_subjetsAK8BDisc = Handle( "std::vector<float>")
l_subjetsAK8BDisc = ("subjetsAK8", "subjetAK8CSV")


# MET and HCAL Filter handles
h_filterNameStrings = Handle( "std::vector<std::string>")
l_filterNameStrings = ("METUserData", "triggerNameTree")
h_filterBits = Handle( "std::vector<float>")
l_filterBits = ("METUserData", "triggerBitTree")
h_filterPrescales = Handle( "std::vector<int>")
l_filterPrescales = ("METUserData", "triggerPrescaleTree")
h_HBHEfilter = Handle("bool")
l_HBHEfilter = ("HBHENoiseFilterResultProducer", "HBHENoiseFilterResultRun1")

# Triggers
h_triggerNameStrings = Handle( "std::vector<std::string>")
l_triggerNameStrings = ("TriggerUserData", "triggerNameTree")
h_triggerBits = Handle( "std::vector<float>")
l_triggerBits = ("TriggerUserData", "triggerBitTree")
h_triggerPrescales = Handle( "std::vector<int>")
l_triggerPrescales = ("TriggerUserData", "triggerPrescaleTree")


#@ Pileup reweighting
if not options.isData and options.puFile != None :
    fPU = ROOT.TFile(options.puFile)
    hPU = fPU.Get("h_NPVert")


f = ROOT.TFile(options.outname, "RECREATE")
f.cd()

#^ Plot initialization


h_NPVert         = ROOT.TH1D("h_NPVert"        , "", 200,0,200 )
h_NtrueIntPU     = ROOT.TH1D("h_NtrueIntPU"    , "", 200,0,200 )


h_ptLep = [ ROOT.TH1F("h0_ptLep", "Lepton p_{T}, Dilepton Channel;p_{T} (GeV)", 100, 0, 1000),
            ROOT.TH1F("h1_ptLep", "Lepton p_{T}, Leptonic Channel;p_{T} (GeV)", 100, 0, 1000),
            ROOT.TH1F("h2_ptLep", "Lepton p_{T}, Hadronic Channel;p_{T} (GeV)", 100, 0, 1000),
            ]
h_etaLep = [ROOT.TH1F("h0_etaLep", "Lepton #eta, Dilepton Channel;#eta", 100, 0, ROOT.TMath.TwoPi() ),
            ROOT.TH1F("h1_etaLep", "Lepton #eta, Leptonic Channel;#eta", 100, 0, ROOT.TMath.TwoPi() ),
            ROOT.TH1F("h2_etaLep", "Lepton #eta, Hadronic Channel;#eta", 100, 0, ROOT.TMath.TwoPi() ),
            ]
h_met = [ ROOT.TH1F("h0_met", "Missing p_{T}, Dilepton Channel;p_{T} (GeV)", 100, 0, 1000),
          ROOT.TH1F("h1_met", "Missing p_{T}, Leptonic Channel;p_{T} (GeV)", 100, 0, 1000),
          ROOT.TH1F("h2_met", "Missing p_{T}, Hadronic Channel;p_{T} (GeV)", 100, 0, 1000),
          ]

h_vPt = [ ROOT.TH1F("h0_vPt", "Boson p_{T}, Dilepton Channel;p_{T} (GeV)", 100, 0, 1000),
          ROOT.TH1F("h1_vPt", "Boson p_{T}, Leptonic Channel;p_{T} (GeV)", 100, 0, 1000),
          ROOT.TH1F("h2_vPt", "Boson p_{T}, Hadronic Channel;p_{T} (GeV)", 100, 0, 1000),
          ]



h_htAK4 = ROOT.TH1D("h2_htAK4", "H_{T}, AK4 jets, Hadronic Channel;H_{T} (GeV)", 100, 0, 1000)
        
h_ptAK8 = [ ROOT.TH1F("h0_ptAK8", "AK8 Jet p_{T}, Dilepton Channel;p_{T} (GeV)", 300, 0, 3000),
            ROOT.TH1F("h1_ptAK8", "AK8 Jet p_{T}, Leptonic Channel;p_{T} (GeV)", 300, 0, 3000),
            ROOT.TH1F("h2_ptAK8", "AK8 Jet p_{T}, Hadronic Channel;p_{T} (GeV)", 300, 0, 3000),
            ]
h_yAK8 = [ROOT.TH1F("h0_yAK8", "AK8 Jet Rapidity, Dilepton Channel;y", 120, -6, 6),
          ROOT.TH1F("h1_yAK8", "AK8 Jet Rapidity, Leptonic Channel;y", 120, -6, 6),
          ROOT.TH1F("h2_yAK8", "AK8 Jet Rapidity, Hadronic Channel;y", 120, -6, 6),
          ]
h_phiAK8 = [ROOT.TH1F("h0_phiAK8", "AK8 Jet #phi, Dilepton Channel;#phi (radians)",100,-ROOT.Math.Pi(),ROOT.Math.Pi()),
            ROOT.TH1F("h1_phiAK8", "AK8 Jet #phi, Leptonic Channel;#phi (radians)",100,-ROOT.Math.Pi(),ROOT.Math.Pi()),
            ROOT.TH1F("h2_phiAK8", "AK8 Jet #phi, Hadronic Channel;#phi (radians)",100,-ROOT.Math.Pi(),ROOT.Math.Pi()),
            ]
h_mAK8 = [ROOT.TH1F("h0_mAK8", "AK8 Jet Mass, Dilepton Channel;Mass (GeV)", 100, 0, 1000),
          ROOT.TH1F("h1_mAK8", "AK8 Jet Mass, Leptonic Channel;Mass (GeV)", 100, 0, 1000),
          ROOT.TH1F("h2_mAK8", "AK8 Jet Mass, Hadronic Channel;Mass (GeV)", 100, 0, 1000),
          ]
h_msoftdropAK8 = [ROOT.TH1F("h0_msoftdropAK8", "AK8 Softdrop Jet Mass, Dilepton Channel;Mass (GeV)", 100, 0, 1000),
                  ROOT.TH1F("h1_msoftdropAK8", "AK8 Softdrop Jet Mass, Leptonic Channel;Mass (GeV)", 100, 0, 1000),
                  ROOT.TH1F("h2_msoftdropAK8", "AK8 Softdrop Jet Mass, Hadronic Channel;Mass (GeV)", 100, 0, 1000),
                  ]
h_tau21AK8 = [ROOT.TH1F("h0_tau21AK8", "AK8 Jet #tau_{2} / #tau_{1}, Dilepton Channel;#tau_{21}", 100, 0, 1.0),
              ROOT.TH1F("h1_tau21AK8", "AK8 Jet #tau_{2} / #tau_{1}, Leptonic Channel;#tau_{21}", 100, 0, 1.0),
              ROOT.TH1F("h2_tau21AK8", "AK8 Jet #tau_{2} / #tau_{1}, Hadronic Channel;#tau_{21}", 100, 0, 1.0),
              ]


h_jetrhoAK8 = [ROOT.TH1F("h0_jetrhoAK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Dilepton Channel;Jet #rho", 100, 0, 1.0),
               ROOT.TH1F("h1_jetrhoAK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Leptonic Channel;Jet #rho", 100, 0, 1.0),
               ROOT.TH1F("h2_jetrhoAK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Hadronic Channel;Jet #rho", 100, 0, 1.0),
              ]


h_jetrho_vs_tau21AK8 = [
    ROOT.TH2F("h0_jetrho_vs_tau21AK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Dilepton Channel;Jet #rho; Jet #tau_{21}", 50, 0, 1.0, 25, 0, 1.0),
    ROOT.TH2F("h1_jetrho_vs_tau21AK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Leptonic Channel;Jet #rho; Jet #tau_{21}", 50, 0, 1.0, 25, 0, 1.0),
    ROOT.TH2F("h2_jetrho_vs_tau21AK8", "AK8 Jet #rho=#frac{m}{p_{T} R}, Hadronic Channel;Jet #rho; Jet #tau_{21}", 50, 0, 1.0, 25, 0, 1.0),
              ]

    
h_mvv = [
    ROOT.TH1D("h0_mvv", "m_{VV}, Dilepton Channel;m_{VV} (GeV)", 50, 0, 5000.),
    ROOT.TH1D("h1_mvv", "m_{VV}, Leptonic Channel;m_{VV} (GeV)", 50, 0, 5000.),
    ROOT.TH1D("h2_mvv", "m_{VV}, Hadronic Channel;m_{VV} (GeV)", 50, 0, 5000.),
              ]

h_rho_all      =[
    ROOT.TH1D("h0_rho_all",      "Dilepton Channel;Jet #rho", 50, 0.0, 1.0),
    ROOT.TH1D("h1_rho_all",      "Leptonic Channel;Jet #rho", 50, 0.0, 1.0),
    ROOT.TH1D("h2_rho_all",      "Hadronic Channel;Jet #rho", 50, 0.0, 1.0),
    ]
h_rho_tau21cut      =[
    ROOT.TH1D("h0_rho_tau21cut",      "Dilepton Channel;Jet #rho", 50, 0.0, 1.0),
    ROOT.TH1D("h1_rho_tau21cut",      "Leptonic Channel;Jet #rho", 50, 0.0, 1.0),
    ROOT.TH1D("h2_rho_tau21cut",      "Hadronic Channel;Jet #rho", 50, 0.0, 1.0),
    ]    

h_rhostar_all      =[
    ROOT.TH1D("h0_rhostar_all",      "Dilepton Channel;Jet #rho", 50, 0.0, 0.01),
    ROOT.TH1D("h1_rhostar_all",      "Leptonic Channel;Jet #rho", 50, 0.0, 0.01),
    ROOT.TH1D("h2_rhostar_all",      "Hadronic Channel;Jet #rho", 50, 0.0, 0.01),
    ]
h_rhostar_tau21cut      =[
    ROOT.TH1D("h0_rhostar_tau21cut",      "Dilepton Channel;Jet #rho", 50, 0.0, 0.01),
    ROOT.TH1D("h1_rhostar_tau21cut",      "Leptonic Channel;Jet #rho", 50, 0.0, 0.01),
    ROOT.TH1D("h2_rhostar_tau21cut",      "Hadronic Channel;Jet #rho", 50, 0.0, 0.01),
    ]    

    
ha_ptAK8 = []
ha_yAK8 = []
ha_mAK8 = []
ha_msoftdropAK8 = []
ha_rho_all = []
ha_htAK8 = []
ha_pt0 = []
for itrig,trig in enumerate(trigsToGet) :
    ha_htAK8.append( ROOT.TH1D("h2_htAK8_" + trig, "H_{T}, AK4 jets, Hadronic Channel, " + trig + ";H_{T} (GeV)", 100, 0, 1000))
    ha_pt0.append( ROOT.TH1F("h2_pt0_" + trig, "Leading AK8 Jet p_{T}, Hadronic Channel, " + trig + ";p_{T} (GeV)", 300, 0, 3000) )
    ha_ptAK8.append( ROOT.TH1F("h2_ptAK8_" + trig, "AK8 Jet p_{T}, Hadronic Channel, " + trig + ";p_{T} (GeV)", 300, 0, 3000) )
    ha_yAK8.append( ROOT.TH1F("h2_yAK8_" + trig, "AK8 Jet Rapidity, Hadronic Channel, " + trig + ";y", 120, -6, 6) )
    ha_mAK8.append( ROOT.TH1F("h2_mAK8_" + trig, "AK8 Jet Mass, Hadronic Channel, " + trig + ";Mass (GeV)", 100, 0, 1000) )
    ha_msoftdropAK8.append( ROOT.TH1F("h2_msoftdropAK8_" + trig, "AK8 Softdrop Jet Mass, Hadronic Channel, " + trig + ";Mass (GeV)", 100, 0, 1000) )
    ha_rho_all.append( ROOT.TH1F("h2_rho_all_" + trig, "AK8 Jet #rho = (m/p_{T}R)^{2}, Hadronic Channel, " + trig + ";#rho", 100, 0, 1.0) )


if options.makeMistag == False : 
    #^ Predicted distributions
    ROOT.SetOwnership( hpred, False )
    predJetRho = ROOT.PredictedDistribution(hpred, "pred_jet_rho", "Jet #rho", 50, 0.0, 1.0)
    predJetPt = ROOT.PredictedDistribution(hpred, "pred_jet_pt", "Jet p_{T} (GeV)", 30, 0, 3000.)
    predJetMVV = ROOT.PredictedDistribution(hpred, "pred_mvv", "M_{VV} (GeV)", 50, 0.0, 5000.)
    predJetMVVMod = ROOT.PredictedDistribution(hpred, "pred_mvvmod", "M_{VV} (GeV)", 50, 0.0, 5000.)

    ROOT.SetOwnership( predJetRho, False )
    ROOT.SetOwnership( predJetPt, False )
    ROOT.SetOwnership( predJetMVV, False )
    ROOT.SetOwnership( predJetMVVMod, False )



#@ JET CORRECTIONS

ROOT.gSystem.Load('libCondFormatsJetMETObjects')
#jecParStrAK4 = ROOT.std.string('JECs/PHYS14_25_V2_AK4PFchs.txt')
#jecUncAK4 = ROOT.JetCorrectionUncertainty( jecParStrAK4 )
#jecParStrAK8 = ROOT.std.string('JECs/PHYS14_25_V2_AK8PFchs.txt')
#jecUncAK8 = ROOT.JetCorrectionUncertainty( jecParStrAK8 )



if options.isData :
    print 'Getting L3 for AK4'
    L3JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L3Absolute_AK4PFchs.txt");
    print 'Getting L2 for AK4'
    L2JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L2Relative_AK4PFchs.txt");
    print 'Getting L1 for AK4'
    L1JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L1FastJet_AK4PFchs.txt");
    # for data only :
    ResJetParAK4 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L2L3Residual_AK4PFchs.txt");

    print 'Getting L3 for AK8'
    L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L3Absolute_AK8PFchs.txt");
    print 'Getting L2 for AK8'
    L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L2Relative_AK8PFchs.txt");
    print 'Getting L1 for AK8'
    L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L1FastJet_AK8PFchs.txt");
    # for data only :
    ResJetParAK8 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_DATA_L2L3Residual_AK8PFchs.txt"); 

    #  Load the JetCorrectorParameter objects into a vector, IMPORTANT: THE ORDER MATTERS HERE !!!! 
    vParJecAK4 = ROOT.vector('JetCorrectorParameters')()
    vParJecAK4.push_back(L1JetParAK4)
    vParJecAK4.push_back(L2JetParAK4)
    vParJecAK4.push_back(L3JetParAK4)
    vParJecAK4.push_back(ResJetParAK4)

    vParJecAK4ForMass = ROOT.vector('JetCorrectorParameters')()
    vParJecAK4ForMass.push_back(L2JetParAK4)
    vParJecAK4ForMass.push_back(L3JetParAK4)
    vParJecAK4ForMass.push_back(ResJetParAK4)
    

    ak4JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK4)
    ak4JetCorrectorForMass = ROOT.FactorizedJetCorrector(vParJecAK4ForMass)

    vParJecAK8 = ROOT.vector('JetCorrectorParameters')()
    vParJecAK8.push_back(L1JetParAK8)
    vParJecAK8.push_back(L2JetParAK8)
    vParJecAK8.push_back(L3JetParAK8)
    vParJecAK8.push_back(ResJetParAK8)

    ak8JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK8)

else : 
    print 'Getting L3 for AK4'
    L3JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L3Absolute_AK4PFchs.txt");
    print 'Getting L2 for AK4'
    L2JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L2Relative_AK4PFchs.txt");
    print 'Getting L1 for AK4'
    L1JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L1FastJet_AK4PFchs.txt");
    # for data only :
    #ResJetParAK4 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L2L3Residual_AK4PFchs.txt");

    print 'Getting L3 for AK8'
    L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L3Absolute_AK8PFchs.txt");
    print 'Getting L2 for AK8'
    L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L2Relative_AK8PFchs.txt");
    print 'Getting L1 for AK8'
    L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L1FastJet_AK8PFchs.txt");
    # for data only :
    #ResJetParAK8 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV4_MC_L2L3Residual_AK8PFchs.txt"); 

    #  Load the JetCorrectorParameter objects into a vector, IMPORTANT: THE ORDER MATTERS HERE !!!! 
    vParJecAK4 = ROOT.vector('JetCorrectorParameters')()
    vParJecAK4.push_back(L1JetParAK4)
    vParJecAK4.push_back(L2JetParAK4)
    vParJecAK4.push_back(L3JetParAK4)

    vParJecAK4ForMass = ROOT.vector('JetCorrectorParameters')()
    vParJecAK4ForMass.push_back(L2JetParAK4)
    vParJecAK4ForMass.push_back(L3JetParAK4)
    
    ak4JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK4)
    ak4JetCorrectorForMass = ROOT.FactorizedJetCorrector(vParJecAK4ForMass)

    vParJecAK8 = ROOT.vector('JetCorrectorParameters')()
    vParJecAK8.push_back(L1JetParAK8)
    vParJecAK8.push_back(L2JetParAK8)
    vParJecAK8.push_back(L3JetParAK8)


    ak8JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK8)


#@ EVENT LOOP

#Tracker variables
DimuonEvents = 0
DieleEvents = 0
muoneleEvents = 0
muonJetsEvents = 0
eleJetsEvents = 0
AllHadronicEvents = 0

cutflow = [0]*13
cutflownames = [
    'Inclusive',
    '>=1 PV',
    '>=1 lepton',
    'V lep pt',
    '>= 1 AK8 jets',
    '>= 2 AK8 jets',
    'VlepVhad',
    'VlepVhad : taggable',
    'VlepVhad : tagged',
    'VhadVhad',
    'VhadVhad : single tag',
    'VhadVhad : taggable',
    'VhadVhad : tagged'
    ]
    
filelist = file( options.files )
filesraw = filelist.readlines()
files = []
nevents = 0
for ifile in filesraw : #{ Loop over text file and find root files linked
    if len( ifile ) > 2 : 
        #s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
        s = ifile.rstrip()
        files.append( s )
        print 'Added ' + s
        #} End loop over txt file

# loop over files
for ifile in files : #{ Loop over root files
    print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break

    # loop over events in this file
    i = 0

    # Make sure the handles we want are in the files so we can
    # avoid leaking memory
    readFilters = True
    readTriggers = True

    
    for event in events: #{ Loop over events in root files
        if options.maxevents > 0 and nevents > options.maxevents :
            break
        i += 1
        nevents += 1
        cutflow[0] += 1
        
        evWeight = 1.0
            
        
        #@ VERTEX SETS
        event.getByLabel( l_pv_chi, h_pv_chi )
        event.getByLabel( l_pv_rho, h_pv_rho )
        event.getByLabel( l_pv_z, h_pv_z )
        event.getByLabel( l_pv_ndof, h_pv_ndof )

        pv_chi = h_pv_chi.product()
        pv_rho = h_pv_rho.product()
        pv_z = h_pv_z.product()
        pv_ndof = h_pv_ndof.product()
        NPV = 0

        for ivtx in xrange( len(pv_chi) ) :
            if abs(pv_z[ivtx]) < 24. and pv_ndof[ivtx] > 4 and abs(pv_rho[ivtx]) < 2.0 :
                NPV += 1
        if NPV < 1 :
            if options.verbose :
                print 'Event has no primary vertex'
            continue
        cutflow[1] += 1
            
        #@ RHO VALUE        
        gotrho = event.getByLabel( l_rho, h_rho )
        if gotrho == False : 
            print "Event has no rho values."
            continue
        if len(h_rho.product()) == 0 :
            print "Event has no rho values."
            continue
        else:
            rho = h_rho.product()[0]
            if options.verbose :
                print 'rho = {0:6.2f}'.format( rho )


        pvWeight = 1.0
        if not options.isData : 
            #@ PU interactions
            event.getByLabel(l_puNtrueInt, h_puNtrueInt)
            puNTrueInt = h_puNtrueInt.product()[0]
            h_NtrueIntPU.Fill( puNTrueInt )

            if options.puFile != None : 
                pvWeight = hPU.GetBinContent( hPU.GetXaxis().FindBin( NPV) )
                evWeight *= pvWeight
            
        h_NPVert.Fill( NPV, evWeight )
                

        # Speedy cuts. Make things go faster.
        event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )
        event.getByLabel ( l_jetsAK8Eta, h_jetsAK8Eta )
        event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )
        event.getByLabel ( l_jetsAK8Phi, h_jetsAK8Phi )
        event.getByLabel ( l_jetsAK8Mass, h_jetsAK8Mass )
        event.getByLabel ( l_jetsAK8Energy, h_jetsAK8Energy )
        event.getByLabel ( l_jetsAK8JEC, h_jetsAK8JEC )
        event.getByLabel ( l_jetsAK8Area, h_jetsAK8Area )
        AK8Pt = h_jetsAK8Pt.product()
        AK8Eta = h_jetsAK8Eta.product()
        AK8Phi = h_jetsAK8Phi.product()
        AK8Mass = h_jetsAK8Mass.product()
        AK8Energy = h_jetsAK8Energy.product()
        AK8JEC = h_jetsAK8JEC.product()
        AK8Area = h_jetsAK8Area.product()

        ak8JetsP4Corr = []
        ak8JetsP4Raw = []
        
        ht = 0.
        # Need to uncorrect and re-correct the jets with latest/greatest
        # JEC's. This almost always has to be done so might as well just always do it. 
        for ipt,pt in enumerate(AK8Pt) :

            AK8JECFromB2GAnaFW = AK8JEC[ipt]   
            AK8P4Raw = ROOT.TLorentzVector()
            AK8P4Raw.SetPtEtaPhiM( AK8Pt[ipt] , AK8Eta[ipt], AK8Phi[ipt], AK8Mass[ipt])
            # Remove the old JEC's to get raw energy
            AK8P4Raw *= AK8JECFromB2GAnaFW            
            ak8JetsP4Raw.append( AK8P4Raw )


            #@ JEC Scaling for AK8 Jets
            ak8JetCorrector.setJetEta( AK8P4Raw.Eta() )
            ak8JetCorrector.setJetPt ( AK8P4Raw.Perp() )
            ak8JetCorrector.setJetE  ( AK8P4Raw.E() )
            ak8JetCorrector.setJetA  ( AK8Area[ipt] )
            ak8JetCorrector.setRho   ( rho )
            ak8JetCorrector.setNPV   ( NPV )
            newJEC = ak8JetCorrector.getCorrection()
            AK8P4Corr = AK8P4Raw*newJEC
            ak8JetsP4Corr.append( AK8P4Corr )                        
            ht += pt
            
        if options.speedyHtMin != None :
            if ht < options.speedyHtMin :
                continue

        if len(ak8JetsP4Corr) < 1 :
            continue
        pt0 = ak8JetsP4Corr[0].Perp()
            

        ###################################################################
        # Event quantities.
        ###################################################################

        
        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)




        
        lastRun = 1
        currRun = 1
        trigMap = {}

        if options.applyFilters and readFilters :
            cscFilt = False
            vertexFilt = False
            hbheFilt = False

            
            gotit1 = event.getByLabel( l_filterNameStrings, h_filterNameStrings )
            gotit2 = event.getByLabel( l_filterBits, h_filterBits )
            #gotit3 = event.getByLabel( l_filterPrescales, h_filterPrescales )
            #gotit4 = event.getByLabel( l_HBHEfilter, h_HBHEfilter )


            if options.verbose :
                print 'Filter string names?  ' + str(gotit1)
                print 'Filter bits?          ' + str(gotit2)

            if gotit1 == False or gotit2 == False  :
                readFilters = False

            filterNameStrings = h_filterNameStrings.product()
            filterBits = h_filterBits.product()
            
            for itrig in xrange(0, len(filterNameStrings) ) :
                if options.verbose :
                    print 'Filter name = ' + filterNameStrings[itrig]
                    print 'Filter bit  = ' + str(filterBits[itrig])
                if "CSC" in filterNameStrings[itrig] :
                    if filterBits[itrig] == 1 :
                        cscFilt = True
                #if "goodVer" in filterNameStrings[itrig] :
                #    if filterBits[itrig] == 1 :
                #        vertexFilt = True
                #if "HBHE" in filterNameStrings[itrig] :
                #    if filterBits[itrig] == 1 :
                #        hbheFilt = True


            if cscFilt == False :
                if options.verbose :
                    print 'Found filters, but they failed'
                continue

        if not readFilters :
            if options.verbose :
                print 'Did not find filters'
            continue



        if (options.applyWEleTriggers or options.applyWMuoTriggers ) and readTriggers :

            passTrig = False
            prescale = 1.0
            unprescaled = False
            gotit1 = event.getByLabel( l_triggerNameStrings, h_triggerNameStrings )
            gotit2 = event.getByLabel( l_triggerBits, h_triggerBits )
            gotit3 = event.getByLabel( l_triggerPrescales, h_triggerPrescales )                        
            if options.verbose :
                print 'Trigger string names? ' + str(gotit1)
                print 'Trigger bits?         ' + str(gotit2)
            
            if gotit1 == False or gotit2 == False or gotit3 == False :
                readTriggers = False            

            triggerNameStrings = h_triggerNameStrings.product()
            triggerBits = h_triggerBits.product()
            triggerPrescales = h_triggerPrescales.product()            

            nSelectedTriggersPassed = 0
            for itrig in xrange(0, len(triggerNameStrings) ) :

                if options.applyWEleTriggers and \
                  ("HLT_Ele23_WPLoose_Gsf" in triggerNameStrings[itrig] or
                   "HLT_Ele32_eta2p1_WPLoose_Gsf" in triggerNameStrings[itrig] ) :
                    if triggerBits[itrig] == 1 :
                        nSelectedTriggersPassed += 1
                        passTrig = True

                if options.applyWMuoTriggers and "HLT_IsoMu24_eta2p1" in triggerNameStrings[itrig]  :  
                    if triggerBits[itrig] == 1 :
                        nSelectedTriggersPassed += 1
                        passTrig = True
        
        if options.applyHadronicTriggers and readTriggers :

            passTrig = False
            prescale = 1.0
            unprescaled = False
            
            gotit1 = event.getByLabel( l_triggerNameStrings, h_triggerNameStrings )
            gotit2 = event.getByLabel( l_triggerBits, h_triggerBits )
            gotit3 = event.getByLabel( l_triggerPrescales, h_triggerPrescales )

            
            
            if options.verbose :
                print 'Trigger string names? ' + str(gotit1)
                print 'Trigger bits?         ' + str(gotit2)
            
            if gotit1 == False or gotit2 == False or gotit3 == False :
                readTriggers = False            

            triggerNameStrings = h_triggerNameStrings.product()
            triggerBits = h_triggerBits.product()
            triggerPrescales = h_triggerPrescales.product()            

            nSelectedTriggersPassed = 0
            for itrig in xrange(0, len(triggerNameStrings) ) :

                if not options.useJetPtTrigs : 
                    # Our triggers are named "PFHT", but there are other "PFHT" triggers that have Jet requirements.
                    # We don't want those, so we veto them. 
                    if "HLT_PFHT" in triggerNameStrings[itrig] and 'Jet' not in triggerNameStrings[itrig] :  
                        for itrigToGet, trigToGet in enumerate(trigsToGet) : 
                            if trigToGet in triggerNameStrings[itrig] :
                                trigIndex = itrigToGet
                                trigMap[ itrigToGet ] = int(triggerBits[itrig])
                                if triggerBits[itrig] == 1 :
                                    nSelectedTriggersPassed += 1
                                    ha_htAK8[itrigToGet].Fill( ht, pvWeight )


                        if triggerBits[itrig] == 1 :

                            if options.verbose : 
                                print '    Passed trigger                : ' + triggerNameStrings[itrig]
                            if triggerPrescales[itrig] == 1.0 :
                                unprescaled = True
                            prescale = prescale * triggerPrescales[itrig]
                        else :
                            if options.verbose :
                                print '    found trigger name but failed : ' + triggerNameStrings[itrig]

                else :
                    if "HLT_PFJet" in triggerNameStrings[itrig] :  
                        for itrigToGet, trigToGet in enumerate(trigsToGet) : 
                            if trigToGet in triggerNameStrings[itrig] :
                                trigIndex = itrigToGet
                                trigMap[ itrigToGet ] = int(triggerBits[itrig])
                                if triggerBits[itrig] == 1 :
                                    nSelectedTriggersPassed += 1
                                    ha_pt0[itrigToGet].Fill( pt0, pvWeight )


                        if triggerBits[itrig] == 1 :

                            if options.verbose : 
                                print '    Passed trigger                : ' + triggerNameStrings[itrig]
                            if triggerPrescales[itrig] == 1.0 :
                                unprescaled = True
                            prescale = prescale * triggerPrescales[itrig]
                        else :
                            if options.verbose :
                                print '    found trigger name but failed : ' + triggerNameStrings[itrig]

                                                            
            if not readTriggers :
                if options.verbose :
                    print 'Did not find triggers'
                continue

            if nSelectedTriggersPassed == 0 :
                if options.verbose :
                    print 'No selected triggers passed'
                continue

            if not options.useJetPtTrigs :
                passTrig,iht = trigHelperHT( ht, trigMap )
                if options.verbose : 
                    print 'Check : ht = ' + str(ht) + ', iht = ' + str(iht) + ', pass = ' + str(passTrig)
            else :
                passTrig,iht = trigHelperPt( pt0, trigMap )
                if options.verbose : 
                    print 'Check : pt0 = ' + str(pt0) + ', iht = ' + str(iht) + ', pass = ' + str(passTrig)


            if not passTrig :
                continue

                        

            if unprescaled :
                prescale = 1.0
            if options.verbose :
                print 'Prescale = ' + str(prescale)

            if options.signalTriggers != None and options.signalTriggers == True :
                if not unprescaled :
                    continue
                
            evWeight = evWeight * prescale
            if passTrig == False :
                continue

        if options.deweightFlat : 
            #@ Event weights
            gotGenerator = event.getByLabel( l_generator, h_generator )
            if gotGenerator :
                #evWeight = evWeight * h_generator.product().weight()
                pthat = 0.0
                if h_generator.product().hasBinningValues() :
                    pthat = h_generator.product().binningValues()[0]
                    evWeight = evWeight * 1/pow(pthat/15.,4.5)
                if options.verbose :
                    print 'Event weight = ' + str( evWeight )
                    print 'pthat = ' + str(pthat)




        ###################################################################
        # Lepton quantities
        ###################################################################
                
        #EVENT MUON HANDLE FILLING
        event.getByLabel ( l_muPt, h_muPt )
        event.getByLabel ( l_muEta, h_muEta )
        event.getByLabel ( l_muPhi, h_muPhi )
        event.getByLabel ( l_muTight, h_muTight )
        event.getByLabel ( l_muLoose, h_muLoose )
        event.getByLabel ( l_muDz, h_muDz )
        event.getByLabel ( l_muCharge, h_muCharge )
        event.getByLabel ( l_muIso04, h_muIso04 )
        event.getByLabel ( l_muKey, h_muKey )

        #@ Muon Selection
        muonsP4 = []
        goodMuonIndices = []
        if len(h_muPt.product()) > 0:
            muonPt = h_muPt.product()
            muonEta = h_muEta.product()
            muonPhi = h_muPhi.product()
            muonTight = h_muTight.product()
            muonLoose = h_muLoose.product()
            muonDz = h_muDz.product()
            muKey = h_muKey.product()
            muCharge = h_muCharge.product()
            muIso = h_muIso04.product()
            for imuon, muon in enumerate(muonPt): #{ Loop over all muons in event
                imuonP4 = ROOT.TLorentzVector()
                imuonP4.SetPtEtaPhiM( muonPt[imuon], muonEta[imuon], muonPhi[imuon], 0.00051)
                muonsP4.append( imuonP4 )
                if options.verbose :
                    print 'muon pt = {0:8.2f}, eta = {1:6.2f}, phi = {2:6.2f}, Dz = {3:6.2f}, tight = {4:6.0f}, iso = {5:6.2f}'.format (
                        imuonP4.Perp(), imuonP4.Eta(), imuonP4.Phi(), muonDz[imuon], muonTight[imuon], muIso[imuon]
                    ),
                if muonPt[imuon] > options.minMuonPt and abs(muonEta[imuon]) < options.maxMuonEta and \
                  muonDz[imuon] < 5.0 and muonTight[imuon] and muIso[imuon] < 0.2 : #$ Muon Cuts
                        goodMuonIndices.append( imuon )
                        if options.verbose : 
                                print ' <-- good'
                elif options.verbose : 
                    print ''
                        
        event.getByLabel ( l_elPt, h_elPt )
        event.getByLabel ( l_elEta, h_elEta )
        event.getByLabel ( l_elPhi, h_elPhi )
        event.getByLabel ( l_elTight, h_elTight )
        event.getByLabel ( l_elLoose, h_elLoose )
        event.getByLabel ( l_elCharge, h_elCharge )
        event.getByLabel ( l_elIso03, h_elIso03 )
        event.getByLabel ( l_eldEtaIn, h_eldEtaIn )
        event.getByLabel ( l_eldPhiIn, h_eldPhiIn )
        event.getByLabel ( l_elHoE, h_elHoE )
        event.getByLabel ( l_elfull5x5siee, h_elfull5x5siee )
        event.getByLabel ( l_elD0, h_elD0 )
        event.getByLabel ( l_elDz, h_elDz )
        event.getByLabel ( l_elhasMatchedConVeto, h_elhasMatchedConVeto )
        event.getByLabel ( l_elooEmooP, h_elooEmooP )
        event.getByLabel ( l_elscEta, h_elscEta )
        event.getByLabel ( l_elmissHits, h_elmissHits )
                
        #@ Electron Selection
        electronsP4 = []
        goodElectronIndices = []
        if len(h_elPt.product()) > 0:
            electronPt = h_elPt.product()
            electronEta = h_elEta.product()
            electronPhi = h_elPhi.product()
            electronTight = h_elTight.product()
            electronLoose = h_elLoose.product()
            electronabsiso = h_elIso03.product()
            electronCharge = h_elCharge.product()
            electrondEtaIn = h_eldEtaIn.product()
            electrondPhiIn = h_eldPhiIn.product()
            electronHoE = h_elHoE.product()
            electronfull5x5siee = h_elfull5x5siee.product()
            electronD0 = h_elD0.product()
            electronDz = h_elDz.product()
            electronhasMatchedConVeto = h_elhasMatchedConVeto.product()
            electronooEmooP = h_elooEmooP.product()
            electronscEta = h_elscEta.product()
            electronmissHits = h_elmissHits.product()

            for ielectron, electron in enumerate(electronPt): #{ Loop over all electrons in event
                iePt = electronPt[ielectron]   
                ieEta = electronEta[ielectron]
                iePhi = electronPhi[ielectron]
                ieCharge = electronCharge[ielectron]
                ielectronP4 = ROOT.TLorentzVector()
                ielectronP4.SetPtEtaPhiM( iePt, ieEta, iePhi, 0.00051)
                electronsP4.append( ielectronP4 )
                goodElectron = False
                if iePt < iePt and abs(ieEta) < options.maxElectronEta : #$ Electron eta cut (based on options)
                    continue

                if abs(electronscEta[ielectron]) < 1.479 :
                    goodElectron = \
                      abs(electrondEtaIn[ielectron]) < 0.006046 and \
                      abs(electrondPhiIn[ielectron]) < 0.028092 and \
                      electronfull5x5siee[ielectron] < 0.009947 and \
                      electronHoE[ielectron] < 0.045772 and \
                      abs(electronD0[ielectron]) < 0.008790 and \
                      abs(electronDz[ielectron]) < 0.021226 and \
                      electronooEmooP[ielectron] < 0.020118 and \
                      electronmissHits[ielectron] <= 1 and \
                      electronhasMatchedConVeto[ielectron] == 1
                      
                elif abs(electronscEta[ielectron]) < 2.5 :
                    goodElectron = \
                      abs(electrondEtaIn[ielectron]) < 0.007057 and \
                      abs(electrondPhiIn[ielectron]) < 0.030159 and \
                      electronfull5x5siee[ielectron] < 0.028237 and \
                      electronHoE[ielectron] < 0.067778 and \
                      abs(electronD0[ielectron]) < 0.027984 and \
                      abs(electronDz[ielectron]) < 0.133431 and \
                      electronooEmooP[ielectron] < 0.098919 and \
                      electronmissHits[ielectron] <= 1 and \
                      electronhasMatchedConVeto[ielectron] == 1
                else :
                    goodElectron = False

                if options.verbose :
                    print 'elec pt = {0:8.2f}, eta = {1:6.2f}, phi = {2:6.2f}, sceta={3:6.2f}, dEta={4:6.2f}, dPhi={5:6.2f}'.format (
                        ielectronP4.Perp(), ielectronP4.Eta(), ielectronP4.Phi(), electronscEta[ielectron],
                        electrondEtaIn[ielectron], electrondPhiIn[ielectron]
                    ),
                    
                if goodElectron == True and electronabsiso[ielectron] < 0.2 :
                    goodElectronIndices.append( ielectron )
                    if options.verbose :
                        print ' <-- good'
                elif options.verbose :
                    print ''
                                             



        if len(goodElectronIndices) > 0 or len(goodMuonIndices) > 0 :
            cutflow[2] += 1

        ###################################################################
        # MET quantities
        ###################################################################


        #Get MET HERE
        event.getByLabel ( l_metPt, h_metPt )
        event.getByLabel ( l_metPx, h_metPx )
        event.getByLabel ( l_metPy, h_metPy )
        event.getByLabel ( l_metPhi, h_metPhi )

        metPx = h_metPx.product()[0]
        metPy = h_metPy.product()[0]
        metPhi = h_metPhi.product()[0]
        metPt = h_metPt.product()[0]
        metP4 = ROOT.TLorentzVector()
        metP4.SetPtEtaPhiM( metPt, 0.0, metPhi, 0.0)

        ###################################################################
        # Jet quantities
        ###################################################################

        #EVENT AK8 HANDLES

        #event.getByLabel ( l_jetsAK8Eta, h_jetsAK8Eta )
        #event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )   # Got this above. Don't get it twice. 
        #event.getByLabel ( l_jetsAK8Phi, h_jetsAK8Phi )
        #event.getByLabel ( l_jetsAK8Mass, h_jetsAK8Mass )
        #event.getByLabel ( l_jetsAK8Energy, h_jetsAK8Energy )
        #event.getByLabel ( l_jetsAK8JEC, h_jetsAK8JEC )
        event.getByLabel ( l_jetsAK8Y, h_jetsAK8Y )
        #event.getByLabel ( l_jetsAK8Area, h_jetsAK8Area )
        event.getByLabel ( l_jetsAK8nHadEnergy, h_jetsAK8nHadEnergy)
        event.getByLabel ( l_jetsAK8nEMEnergy, h_jetsAK8nEMEnergy )
        event.getByLabel ( l_jetsAK8cHadEnergy, h_jetsAK8cHadEnergy )
        event.getByLabel ( l_jetsAK8HFHadronEnergy, h_jetsAK8HFHadronEnergy )
        event.getByLabel ( l_jetsAK8cEMEnergy, h_jetsAK8cEMEnergy )
        event.getByLabel ( l_jetsAK8numDaughters, h_jetsAK8numDaughters )
        event.getByLabel ( l_jetsAK8cMultip, h_jetsAK8cMultip )

        event.getByLabel ( l_jetsAK8Keys, h_jetsAK8Keys )

        event.getByLabel ( l_jetsAK8SoftDropMass, h_jetsAK8SoftDropMass )
        event.getByLabel ( l_jetsAK8TrimMass, h_jetsAK8TrimMass )
        event.getByLabel ( l_jetsAK8PrunMass, h_jetsAK8PrunMass )
        event.getByLabel ( l_jetsAK8FiltMass, h_jetsAK8FiltMass )
        event.getByLabel ( l_jetsAK8Tau1, h_jetsAK8Tau1 )
        event.getByLabel ( l_jetsAK8Tau2, h_jetsAK8Tau2 )
        event.getByLabel ( l_jetsAK8Tau3, h_jetsAK8Tau3 )
        event.getByLabel ( l_jetsAK8nSubJets, h_jetsAK8nSubJets )
        event.getByLabel ( l_jetsAK8minmass, h_jetsAK8minmass )

        event.getByLabel ( l_jetsAK8vSubjetIndex0, h_jetsAK8vSubjetIndex0 )
        event.getByLabel ( l_jetsAK8vSubjetIndex1, h_jetsAK8vSubjetIndex1 )

        
        event.getByLabel ( l_subjetsAK8BDisc, h_subjetsAK8BDisc)
        event.getByLabel ( l_subjetsAK8Pt, h_subjetsAK8Pt)
        event.getByLabel ( l_subjetsAK8Eta, h_subjetsAK8Eta)
        event.getByLabel ( l_subjetsAK8Phi, h_subjetsAK8Phi)
        event.getByLabel ( l_subjetsAK8Mass, h_subjetsAK8Mass)



        
        ak8JetsPassID = []
        ak8JetsPassKin = []
        ak8JetsPassTag = []
        AK8Rho = []
        AK8SoftDropM = []

        if len( h_jetsAK8Pt.product()) > 0 : 
            #AK8Pt = h_jetsAK8Pt.product()   # Got this earlier, don't get it twice. 
            #AK8Eta = h_jetsAK8Eta.product()
            #AK8Phi = h_jetsAK8Phi.product()
            #AK8Mass = h_jetsAK8Mass.product()
            #AK8Energy = h_jetsAK8Energy.product()
            AK8Y = h_jetsAK8Y.product()

            #AK8JEC = h_jetsAK8JEC.product()
            #AK8Area = h_jetsAK8Area.product()
            #AK8SoftDropM = h_jetsAK8SoftDropMass.product()
            AK8TrimmedM = h_jetsAK8TrimMass.product()
            AK8TrimmedM = h_jetsAK8TrimMass.product()
            AK8PrunedM = h_jetsAK8PrunMass.product()
            AK8FilteredM = h_jetsAK8FiltMass.product()
            AK8Tau1 = h_jetsAK8Tau1.product()
            AK8Tau2 = h_jetsAK8Tau2.product()
            AK8Tau3 = h_jetsAK8Tau3.product()
            AK8nSubJets = h_jetsAK8nSubJets.product()
            AK8minmass = h_jetsAK8minmass.product()
            AK8vSubjetIndex0 = h_jetsAK8vSubjetIndex0.product()
            AK8vSubjetIndex1 = h_jetsAK8vSubjetIndex1.product()
            AK8Keys = h_jetsAK8Keys.product()

            AK8nHadE = h_jetsAK8nHadEnergy.product()
            AK8nEME = h_jetsAK8nEMEnergy.product()
            AK8cHadE =  h_jetsAK8cHadEnergy.product()
            AK8HFHadE = h_jetsAK8HFHadronEnergy.product()
            AK8cEME =  h_jetsAK8cEMEnergy.product()
            AK8numDaughters = h_jetsAK8numDaughters.product()
            AK8cMultip =  h_jetsAK8cMultip.product()            
        
        if len( h_subjetsAK8BDisc.product() ) > 0 : 
            AK8SubJetsBDisc = h_subjetsAK8BDisc.product()
            AK8SubJetsPt = h_subjetsAK8Pt.product()
            AK8SubJetsEta = h_subjetsAK8Eta.product()
            AK8SubJetsPhi = h_subjetsAK8Phi.product()
            AK8SubJetsMass = h_subjetsAK8Mass.product()


        htCorr = 0.
        for i,AK8P4Corr in enumerate(ak8JetsP4Corr):#{ Loop over AK8 Jets, corrected above

            if options.verbose :
                print 'AK8 jet ' + str(i)
                
            AK8P4Raw = ak8JetsP4Raw[i]
            
                
            ##### To do : Type 1 MET corrections, JER propagation

            #$ Get Jet Rho and softdrop mass
            sp4_0 = None
            sp4_1 = None
            ival = int(AK8vSubjetIndex0[i])            
            if ival > -1 :
                spt0    = AK8SubJetsPt[ival]
                seta0   = AK8SubJetsEta[ival]
                sphi0   = AK8SubJetsPhi[ival]
                sm0   = AK8SubJetsMass[ival]
                sp4_0Raw = ROOT.TLorentzVector()
                sp4_0Raw.SetPtEtaPhiM( spt0, seta0, sphi0, sm0 )

                ak4JetCorrectorForMass.setJetEta( sp4_0Raw.Eta() )
                ak4JetCorrectorForMass.setJetPt ( sp4_0Raw.Perp() )
                ak4JetCorrectorForMass.setJetE  ( sp4_0Raw.E() )
                ak4JetCorrectorForMass.setRho   ( rho )
                ak4JetCorrectorForMass.setNPV   ( NPV )
                subjetJEC = ak4JetCorrectorForMass.getCorrection()
                sp4_0 = sp4_0Raw * subjetJEC
                
            ival = int(AK8vSubjetIndex1[i])
            if ival > -1 :
                spt1    = AK8SubJetsPt[ival]
                seta1   = AK8SubJetsEta[ival]
                sphi1   = AK8SubJetsPhi[ival]
                sm1   = AK8SubJetsMass[ival]
                sp4_1Raw = ROOT.TLorentzVector()
                sp4_1Raw.SetPtEtaPhiM( spt1, seta1, sphi1, sm1 )

                ak4JetCorrectorForMass.setJetEta( sp4_1Raw.Eta() )
                ak4JetCorrectorForMass.setJetPt ( sp4_1Raw.Perp() )
                ak4JetCorrectorForMass.setJetE  ( sp4_1Raw.E() )
                ak4JetCorrectorForMass.setRho   ( rho )
                ak4JetCorrectorForMass.setNPV   ( NPV )
                subjetJEC = ak4JetCorrectorForMass.getCorrection()
                sp4_1 = sp4_1Raw * subjetJEC


            if sp4_0 == None or sp4_1 == None :
                jetrho = -1.0
                AK8SoftDropM.append( -1.0 )
                AK8Rho.append(-1.0)
            else : 
                softdrop_p4 = sp4_0 + sp4_1
                jetR = 0.8
                jetrho = softdrop_p4.M() / (softdrop_p4.Perp() * jetR)
                jetrho *= jetrho
                AK8SoftDropM.append( softdrop_p4.M() )
                AK8Rho.append( jetrho )

            
            #$ Jet ID for AK8 jets
            nhf = AK8nHadE[i] / AK8P4Raw.E()
            nef = AK8nEME[i] / AK8P4Raw.E()
            chf = AK8cHadE[i] / AK8P4Raw.E()
            cef = AK8cEME[i] / AK8P4Raw.E()
            nconstituents = AK8numDaughters[i]
            nch = AK8cMultip[i] 
            goodJet = \
              nhf < 0.99 and \
              nef < 0.99 and \
              chf > 0.00 and \
              cef < 0.99 and \
              nconstituents > 1 and \
              nch > 0

            if options.verbose :
                print '   raw jet pt = {0:8.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}'.format (
                    AK8P4Raw.Perp(), AK8P4Raw.Rapidity(), AK8P4Raw.Phi(), AK8P4Raw.M()
                    )

            tau21 = None
            if AK8Tau1[i] > 0.0 :
                tau21 = AK8Tau2[i] / AK8Tau1[i]
                
            if options.verbose : 
                print '  corr jet pt = {0:8.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, m_sd = {4:6.2f}, tau21 = {5:6.2f}, jetrho = {6:10.2e}'.format (
                    AK8P4Corr.Perp(), AK8P4Corr.Rapidity(), AK8P4Corr.Phi(), AK8P4Corr.M(), AK8SoftDropM[i], tau21, jetrho
                )

            if not goodJet :
                ak8JetsPassID.append(False)
                
            else :
                ak8JetsPassID.append(True)
                htCorr += AK8P4Corr.Perp()
                                
            passTaggable = False
            # Separately test whether the jet passes kinematics and if the jet passes substructure cuts
            if  options.minAK8Pt < AK8P4Corr.Perp() and AK8P4Corr.Perp() < options.maxAK8Pt and abs( AK8P4Corr.Rapidity() ) < 2.4 and \
              options.sdmassCutLo < AK8SoftDropM[i] and AK8SoftDropM[i] < options.sdmassCutHi :
                passTaggable = True
                ak8JetsPassKin.append( True )
            else :
                ak8JetsPassKin.append( False )
                
            if options.verbose :
                print '    pass kin = ' + str(ak8JetsPassKin[len(ak8JetsPassKin)-1])

            passTagged = False
            if tau21 < options.tau21Cut and options.sdmassCutLo < AK8SoftDropM[i] and AK8SoftDropM[i] < options.sdmassCutHi :
                passTagged = True
                ak8JetsPassTag.append( True )

            else :
                ak8JetsPassTag.append( False )

            if options.verbose :
                print '    pass tag = ' + str(ak8JetsPassTag[len(ak8JetsPassTag)-1])

            if passTaggable and options.verbose : 
                print '  tgb  jet pt = {0:8.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, m_sd = {4:6.2f}, tau21 = {5:6.2f}, jetrho = {6:10.2e}, tag = {7:3.0f}'.format (
                    AK8P4Corr.Perp(), AK8P4Corr.Rapidity(), AK8P4Corr.Phi(), AK8P4Corr.M(), AK8SoftDropM[i], tau21, jetrho, passTagged
                )

        if options.htMin != None and htCorr < options.htMin :
            continue
        ###################################################################
        # Leptonic boson selection
        ###################################################################
        wLepCand = None
        zLepCand = None
        hLepCand = None
        leptons = []
        if len(goodMuonIndices) == 1 :
            leptons.append( muonsP4[goodMuonIndices[0]] )
            wLepCand = muonsP4[goodMuonIndices[0]] + metP4
        elif len(goodElectronIndices) == 1 :
            leptons.append( electronsP4[goodElectronIndices[0]] )
            wLepCand = electronsP4[goodElectronIndices[0]] + metP4
        elif len( goodMuonIndices) == 2 :
            leptons.append( muonsP4[goodMuonIndices[0]] )
            leptons.append( muonsP4[goodMuonIndices[1]] )
            zLepCand = muonsP4[goodMuonIndices[0]] + muonsP4[goodMuonIndices[1]]
        elif len( goodElectronIndices) == 2 :
            leptons.append( electronsP4[goodElectronIndices[0]] )
            leptons.append( electronsP4[goodElectronIndices[1]] )
            zLepCand = electronsP4[goodElectronIndices[0]] + electronsP4[goodElectronIndices[1]]

        # Define selection based on number of boosted leptonic bosons

        if zLepCand != None and zLepCand.Perp() > options.minZLepPt :
            selection = 0
        elif wLepCand != None and wLepCand.Perp() > options.minWLepPt :
            selection = 1
        else :
            selection = 2



        if selection != options.selection :
            continue
        cutflow[3] += 1
        if options.verbose :
            print 'Selection = ' + str(selection)
                
        for ilepton, lepton in enumerate( leptons) :
            h_ptLep[selection].Fill( lepton.Perp(), evWeight )
            h_etaLep[selection].Fill( lepton.Eta(), evWeight )
            h_met[selection].Fill( metPt, evWeight )

            

        # boson and diboson plots
        vLep = None
        vHad0 = None
        vHad1 = None
        eventTagged = False

        if zLepCand != None :
            vLep = zLepCand
        elif wLepCand != None :
            vLep = wLepCand


        if len(ak8JetsP4Corr) > 0 :

            cutflow[4] += 1
            vHad0 = ak8JetsP4Corr[0]
            taggable0 = ak8JetsPassKin[0]
            tagged0 = ak8JetsPassTag[0]
            sdm0 = AK8SoftDropM[0]
            sdrho0 = AK8Rho[0]
            tau21_0 = 0.0
            if AK8Tau1[0] > 0.0 :
                tau21_0 = AK8Tau2[0] / AK8Tau1[0]
            if sdm0 > 0.0 : 
                sdrhostar0 = sdrho0 / sdm0 * tau21_0
            else :
                sdrhostar0 = 0.0

            if len( ak8JetsP4Corr ) > 1 :
                cutflow[5] += 1
                vHad1 = ak8JetsP4Corr[1]
                taggable1 = ak8JetsPassKin[1]
                tagged1 = ak8JetsPassTag[1]
                sdm1 = AK8SoftDropM[1]
                sdrho1 = AK8Rho[1]
                tau21_1 = 0.0
                if AK8Tau1[1] > 0.0 :
                    tau21_1 = AK8Tau2[1] / AK8Tau1[1]
                if sdm1 > 0.0 :
                    sdrhostar1 = sdrho1 / sdm1* tau21_1
                else :
                    sdrhostar1 = 0.0

        if selection < 2 and vLep != None and vHad0 != None :
            cutflow[6] += 1
            vvCand = vLep + vHad0
            h_vPt[selection].Fill( vLep.Perp(), evWeight )
            printString = 'V lep + V had'
            if taggable0 :
                cutflow[7] += 1                
                h_jetrho_vs_tau21AK8[selection].Fill( sdrho0, tau21_0, evWeight )                
                h_ptAK8[selection].Fill( vHad0.Perp(), evWeight  )
                h_yAK8[selection].Fill( vHad0.Rapidity(), evWeight  )
                h_phiAK8[selection].Fill( vHad0.Phi(), evWeight  )
                h_mAK8[selection].Fill( vHad0.M(), evWeight  )
                h_msoftdropAK8[selection].Fill( sdm0, evWeight  )
                h_rho_all[selection].Fill( sdrho0, evWeight )
                h_rhostar_all[selection].Fill( sdrhostar0, evWeight )
                printString += ', taggable'
                if options.makeMistag == False : 
                    predJetRho.Accumulate( sdrho0, sdrho0, tagged0, evWeight )
                    predJetPt.Accumulate( vHad0.Perp(), sdrho0, tagged0, evWeight )
                    predJetMVV.Accumulate( vvCand.M(), sdrho0, tagged0, evWeight )
                if tagged0 :
                    cutflow[8] += 1
                    eventTagged = True
                    h_rho_tau21cut[selection].Fill( sdrho0, evWeight )
                    h_rhostar_tau21cut[selection].Fill( sdrhostar0, evWeight )
                    printString += ', tagged'
            if options.verbose :
                print printString
                     
           

        elif selection == 2 and vHad0 != None and vHad1 != None :




            if vHad0.DeltaPhi(vHad1) < 2.1 :
                continue


            
            # Get the "mass modified" four-vectors
            # taking the three-vector from the original
            # jet, and setting the mass from a distribution
            # based on MC. 
            vHad0Mod = copy.copy ( vHad0 )
            vHad1Mod = copy.copy ( vHad1 )

            if options.massModMistagFile != None : 
                randM0 = hmassMod.GetRandom()
                randM1 = hmassMod.GetRandom()

                if vHad0Mod.M() < options.sdmassCutLo or vHad0Mod.M() > options.sdmassCutHi : 
                    vHad0Mod.SetPtEtaPhiM( vHad0Mod.Perp(), vHad0Mod.Eta(), vHad0Mod.Phi(), randM0 )
                if vHad1Mod.M() < options.sdmassCutLo or vHad1Mod.M() > options.sdmassCutHi : 
                    vHad1Mod.SetPtEtaPhiM( vHad1Mod.Perp(), vHad1Mod.Eta(), vHad1Mod.Phi(), randM1 )

            vvCand = vHad0 + vHad1

            
            printString = 'V had + V had'
            cutflow[9] += 1

            # Here we select double tagged events.
            # We simultaneously derive a mistage rate from
            # "tag and probe" events at lower pt, and
            # then apply it for events at higher pt. 
            iprobe = random.randint(0,1)
            
            if iprobe == 0 and taggable1 and tagged1 :
                printString += ', 1 tagged, using 0 as probe : '
                cutflow[10] += 1
                if taggable0 :
                    cutflow[11] += 1
                    vvCandMod = vHad0Mod + vHad1
                    h_ptAK8[selection].Fill( vHad0.Perp(), evWeight  )
                    h_yAK8[selection].Fill( vHad0.Rapidity(), evWeight  )
                    h_phiAK8[selection].Fill( vHad0.Phi(), evWeight  )
                    h_mAK8[selection].Fill( vHad0.M(), evWeight  )
                    h_msoftdropAK8[selection].Fill( sdm0, evWeight  )
                    h_rho_all[selection].Fill( sdrho0, evWeight )
                    h_rhostar_all[selection].Fill( sdrhostar0, evWeight )
                    h_jetrho_vs_tau21AK8[selection].Fill( sdrho0, tau21_0, evWeight )
                    
                    if options.applyHadronicTriggers :
                        ha_ptAK8[iht].Fill( vHad0.Perp(), pvWeight  )
                        ha_yAK8[iht].Fill( vHad0.Rapidity(), pvWeight  )
                        ha_mAK8[iht].Fill( vHad0.M(), pvWeight  )
                        ha_msoftdropAK8[iht].Fill( sdm0, pvWeight  )
                        ha_rho_all[iht].Fill( sdrho0, pvWeight )
                    
                    printString += 'taggable 0'
                    if options.makeMistag == False : 
                        predJetRho.Accumulate( sdrho1, sdrho0, tagged0, evWeight )
                        predJetPt.Accumulate( vHad0.Perp(), sdrho0, tagged0, evWeight )
                        predJetMVV.Accumulate( vvCand.M(), sdrho0, tagged0, evWeight )
                        predJetMVVMod.Accumulate( vvCandMod.M(), sdrho0, tagged0, evWeight )
                    
                    if tagged0 :
                        cutflow[12] += 1
                        eventTagged = True
                        h_rho_tau21cut[selection].Fill( sdrho0, evWeight )
                        h_rhostar_tau21cut[selection].Fill( sdrhostar0, evWeight )
                        printString += ', tagged 0... SUCCESS'
            if iprobe == 1 and taggable0 and tagged0 :
                printString += ', 0 tagged, using 1 as probe : '
                cutflow[10] += 1
                if taggable1 :
                    cutflow[11] += 1
                    vvCandMod = vHad0 + vHad1Mod
                    h_ptAK8[selection].Fill( vHad1.Perp(), evWeight  )
                    h_yAK8[selection].Fill( vHad1.Rapidity(), evWeight  )
                    h_phiAK8[selection].Fill( vHad1.Phi(), evWeight  )
                    h_mAK8[selection].Fill( vHad1.M(), evWeight  )
                    h_msoftdropAK8[selection].Fill( sdm1, evWeight  )
                    h_rho_all[selection].Fill( sdrho1, evWeight )
                    h_rhostar_all[selection].Fill( sdrhostar1, evWeight )
                    h_jetrho_vs_tau21AK8[selection].Fill( sdrho1, tau21_1, evWeight )

                    if options.applyHadronicTriggers : 
                        ha_ptAK8[iht].Fill( vHad1.Perp(), pvWeight )
                        ha_yAK8[iht].Fill( vHad1.Rapidity(), pvWeight )
                        ha_mAK8[iht].Fill( vHad1.M(), pvWeight )
                        ha_msoftdropAK8[iht].Fill( sdm1, pvWeight )
                        ha_rho_all[iht].Fill( sdrho1, pvWeight )
                                        
                    printString += 'taggable 1'
                    if options.makeMistag == False : 
                        predJetRho.Accumulate( sdrho0, sdrho1, tagged1, evWeight )
                        predJetPt.Accumulate( vHad1.Perp(), sdrho1, tagged1, evWeight )
                        predJetMVV.Accumulate( vvCand.M(), sdrho1, tagged1, evWeight )
                        predJetMVVMod.Accumulate( vvCandMod.M(), sdrho1, tagged1, evWeight )
                    if tagged1 :
                        cutflow[12] += 1
                        eventTagged = True
                        h_rho_tau21cut[selection].Fill( sdrho1, evWeight )
                        h_rhostar_tau21cut[selection].Fill( sdrhostar1, evWeight )
                        printString += ', tagged 1... SUCCESS'                        
            if options.verbose :
                print printString
        else :
            if options.verbose :
                print "event failed VV selection"
            continue

        if eventTagged : 
            h_mvv[selection].Fill( vvCand.M(), evWeight )
        
        
            
#@ CLEANUP
if options.makeMistag == False : 
    predJetRho.SetCalculatedErrors()
    predJetPt.SetCalculatedErrors()
    predJetMVV.SetCalculatedErrors()

f.cd()
f.Write()

f.Close()


for istage,stage in enumerate(cutflow) :
    print 'Stage %6d %-20s : %8d' % (istage, cutflownames[istage], stage)
