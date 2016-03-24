﻿#! /usr/bin/env python

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

parser.add_option('--writeTree', action='store_true',
                  default=True,
                  dest='writeTree',
                  help='Write Tree?')

parser.add_option('--isMC', action='store_true',
                  default=False,
                  dest='isMC',
                  help='Is this MC?')

parser.add_option('--maxevents', type='int', action='store',
                  default=-1,
                  dest='maxevents',
                  help='Number of events to run. -1 is all events')

parser.add_option('--maxjets', type='int', action='store',
                  default=None,
                  dest='maxjets',
                  help='Max jets to plot')

parser.add_option('--deweightFlat', action='store_true',
                  default=False,
                  dest='deweightFlat',
                  help='Deweight the flat qcd sample')

parser.add_option('--applyFilters', action='store_true',
                  default=False,
                  dest='applyFilters',
                  help='Apply MET filters')

parser.add_option('--applyTriggers', action='store_true',
                  default=False,
                  dest='applyTriggers',
                  help='Apply triggers')

parser.add_option('--makeResponseMatrix', action='store_true',
                  default=False,
                  dest='makeResponseMatrix',
                  help='Make response matrix')

parser.add_option('--minAK8JetPt', type='float', action='store',
                  default=200.,
                  dest='minAK8JetPt',
                  help='Minimum AK8 Jet Pt')

parser.add_option('--speedyPtMin', type='float', action='store',
                  default=None,
                  dest='speedyPtMin',
                  help='Minimum AK8 Jet Pt for whatever is in the ntuple to make it faster')


parser.add_option('--maxTau21', type='float', action='store',
                  default=0.6,
                  dest='maxTau21',
                  help='Maximum Tau21 cut')

parser.add_option('--weightQCDSample', type='float', action='store',
                  default=None,
                  dest='weightQCDSample',
                  help='Weight the QCD samples')
                  
parser.add_option('--jecSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jecSys',
                  help='JEC systematic variation. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma). Default is None.')
                  
parser.add_option('--jerSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jerSys',
                  help='JER Systematic variation in fraction. Default is None.')

parser.add_option('--makeResponseMatrix2D', action='store_true',
                  default =False,
                  dest ='makeResponseMatrix2D',
                  help = 'Make 2D Response Matrix')

(options, args) = parser.parse_args()
argv = []


#@ FWLITE STUFF

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("rootlogon.C")

import copy
import random
from array import array
#pt0cuts = [100., 150., 200., 300., 400., 500., 600., 700., 800. ]
pt0cuts = [150., 230., 320., 410., 515., 610., 640., 700.]
trigsToGet = [
#    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500' 
    ]
if options.verbose :
    print 'start solving issues, its verbose time!'    
# Jet energy resolution (nominal, up/down) for AK8 jets
def getJER(jetEta, jerType) :

    jerSF = 1.0

    if ( (jerType==0 or jerType==-1 or jerType==1) == False):
        print "ERROR: Can't get JER! use type=0 (nom), -1 (down), +1 (up)"
        return float(jerSF)

    etamin = [0.0,0.5,1.1,1.7,2.3,2.8,3.2]
    etamax = [0.5,1.1,1.7,2.3,2.8,3.2,5.0]
    
    scale_nom = [1.079,1.099,1.121,1.208,1.254,1.395,1.056]
    scale_dn  = [1.053,1.071,1.092,1.162,1.192,1.332,0.865]
    scale_up  = [1.105,1.127,1.150,1.254,1.316,1.458,1.247]

    for iSF in range(0,len(scale_nom)) :
        if abs(jetEta) >= etamin[iSF] and abs(jetEta) < etamax[iSF] :
            if jerType < 0 :
                jerSF = scale_dn[iSF]
            elif jerType > 0 :
                jerSF = scale_up[iSF]
            else :
                jerSF = scale_nom[iSF]
            break

    return float(jerSF)
    
def getMatched( p4, coll, dRMax = 0.1) :
    if coll != None : 
        for i,c in enumerate(coll):
            if p4.DeltaR(c) < dRMax :
                return i
    return None
    

def binFinder( pt0 ) :
    if pt0 < pt0cuts[0] :
        return None
    npt0cuts = len( pt0cuts )
    ipt0 = 0
    for ipt0 in xrange( npt0cuts-1, 0, -1) :
        if pt0 > pt0cuts[ipt0] :
            break
    return ipt0

def trigHelper( pt0, trigs ) :

    if pt0 < pt0cuts[0] :
        return False, None
    
    npt0cuts = len( pt0cuts )
    ipt0 = 0
    for ipt0 in xrange( npt0cuts-1, 0, -1) :
        if pt0 > pt0cuts[ipt0] :
            break
    ipass = trigs[ipt0]
    return ipass, ipt0
if options.verbose :
    print 'definitions made for everything'

ptBinA = array('d', [150., 230., 320., 410., 515., 610., 640., 700])
nbinsPt = len(ptBinA) - 1



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
l_jetsAK8Energy = ("jetsAK8" , "jetAK8E")
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



h_genJetsAK8Pt = Handle("std::vector<float>")
l_genJetsAK8Pt = ("genJetsAK8" , "genJetsAK8Pt")
h_genJetsAK8Eta = Handle("std::vector<float>")
l_genJetsAK8Eta = ("genJetsAK8" , "genJetsAK8Eta")
h_genJetsAK8Phi = Handle("std::vector<float>")
l_genJetsAK8Phi = ("genJetsAK8" , "genJetsAK8Phi")
h_genJetsAK8Mass = Handle("std::vector<float>")
l_genJetsAK8Mass = ("genJetsAK8" , "genJetsAK8Mass")
h_genJetsAK8SoftDropMass = Handle("std::vector<float>")
l_genJetsAK8SoftDropMass = ("genJetsAK8SoftDrop" , "genJetsAK8SoftDropMass")
h_genJetsAK8SoftDropPt = Handle("std::vector<float>")
l_genJetsAK8SoftDropPt = ("genJetsAK8SoftDrop" , "genJetsAK8SoftDropPt")
h_genJetsAK8SoftDropPhi = Handle("std::vector<float>")
l_genJetsAK8SoftDropPhi = ("genJetsAK8SoftDrop" , "genJetsAK8SoftDropPhi")
h_genJetsAK8SoftDropEta = Handle("std::vector<float>")
l_genJetsAK8SoftDropEta = ("genJetsAK8SoftDrop" , "genJetsAK8SoftDropEta")


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




f = ROOT.TFile(options.outname, "RECREATE")
f.cd()


if options.writeTree : 
    TreeEXOVV = ROOT.TTree("TreeEXOVV", "TreeEXOVV")
    Trig        = array('i', [0]  )
    Weight      = array('f', [0.] )

    NFatJet             = array('i', [0] )
    FatJetPt            = array('f', [-1., -1.])
    FatJetEta           = array('f', [-1., -1.])
    FatJetPhi           = array('f', [-1., -1.])
    FatJetRap           = array('f', [-1., -1.])
    FatJetBDisc         = array('f', [-1., -1.])
    FatJetRhoRatio      = array('f', [-1., -1.])
    FatJetMass          = array('f', [-1., -1.])
    FatJetMassSoftDrop  = array('f', [-1., -1.])
    FatJetMassPruned    = array('f', [-1., -1.])
    FatJetMassFiltered  = array('f', [-1., -1.])
    FatJetMassTrimmed   = array('f', [-1., -1.])
    FatJetTau1          = array('f', [-1., -1.]) 
    FatJetTau2          = array('f', [-1., -1.]) 
    FatJetTau3          = array('f', [-1., -1.]) 
    FatJetTau32         = array('f', [-1., -1.])
    FatJetTau21         = array('f', [-1., -1.]) 
    FatJetSDnsubjets    = array('f', [-1., -1.])
    FatJetSDbdisc0      = array('f', [-1., -1.])
    FatJetSDbdisc1      = array('f', [-1., -1.])
    FatJetSDmaxbdisc    = array('f', [-1., -1.])
    FatJetSDsubjetWpt   = array('f', [-1., -1.])
    FatJetSDsubjetWmass = array('f', [-1., -1.])
    FatJetSDsubjetWp4   = array('f', [-1., -1.])
    FatJetSDsubjetBpt   = array('f', [-1., -1.])
    FatJetSDsubjetBmass = array('f', [-1., -1.])
    FatJetSDsubjetBp4   = array('f', [-1., -1.])
    FatJetCorrUp        = array('f', [-1., -1.])
    FatJetCorrDn        = array('f', [-1., -1.])
    


    NGenJet             = array('i', [0] )
    GenJetPt            = array('f', [-1., -1.])
    GenJetEta           = array('f', [-1., -1.])
    GenJetPhi           = array('f', [-1., -1.])
    GenJetRap           = array('f', [-1., -1.])
    GenJetBDisc         = array('f', [-1., -1.])
    GenJetRhoRatio      = array('f', [-1., -1.])
    GenJetMass          = array('f', [-1., -1.])
    GenJetMassSoftDrop  = array('f', [-1., -1.])
    GenJetMassPruned    = array('f', [-1., -1.])
    GenJetMassFiltered  = array('f', [-1., -1.])
    GenJetMassTrimmed   = array('f', [-1., -1.])
    GenJetTau1          = array('f', [-1., -1.]) 
    GenJetTau2          = array('f', [-1., -1.]) 
    GenJetTau3          = array('f', [-1., -1.]) 
    GenJetTau32         = array('f', [-1., -1.])
    GenJetTau21         = array('f', [-1., -1.]) 
    GenJetSDnsubjets    = array('f', [-1., -1.])
    GenJetSDbdisc0      = array('f', [-1., -1.])
    GenJetSDbdisc1      = array('f', [-1., -1.])
    GenJetSDmaxbdisc    = array('f', [-1., -1.])
    GenJetSDsubjetWpt   = array('f', [-1., -1.])
    GenJetSDsubjetWmass = array('f', [-1., -1.])
    GenJetSDsubjetWp4   = array('f', [-1., -1.])
    GenJetSDsubjetBpt   = array('f', [-1., -1.])
    GenJetSDsubjetBmass = array('f', [-1., -1.])
    GenJetSDsubjetBp4   = array('f', [-1., -1.])
    
    METpx        = array('f', [-1.])
    METpy        = array('f', [-1.])
    METpt        = array('f', [-1.])
    METphi       = array('f', [-1.])
    Nvtx         = array('f', [-1.])



    TreeEXOVV.Branch('Trig'                , Trig                ,  'Trig/I'        )
    TreeEXOVV.Branch('Weight'              , Weight              ,  'Weight/F'      )
    TreeEXOVV.Branch('NFatJet'             , NFatJet             ,  'NFatJet/I'        )
    TreeEXOVV.Branch('FatJetPt'            , FatJetPt            ,  'FatJetPt[NFatJet]/F'            )
    TreeEXOVV.Branch('FatJetEta'           , FatJetEta           ,  'FatJetEta[NFatJet]/F'           )
    TreeEXOVV.Branch('FatJetPhi'           , FatJetPhi           ,  'FatJetPhi[NFatJet]/F'           )
    TreeEXOVV.Branch('FatJetRap'           , FatJetRap           ,  'FatJetRap[NFatJet]/F'           )
    TreeEXOVV.Branch('FatJetBDisc'         , FatJetBDisc         ,  'FatJetBDisc[NFatJet]/F'         )
    TreeEXOVV.Branch('FatJetRhoRatio'      , FatJetRhoRatio      ,  'FatJetRhoRatio[NFatJet]/F'      )
    TreeEXOVV.Branch('FatJetMass'          , FatJetMass          ,  'FatJetMass[NFatJet]/F'          )
    TreeEXOVV.Branch('FatJetMassSoftDrop'  , FatJetMassSoftDrop  ,  'FatJetMassSoftDrop[NFatJet]/F'  )
    TreeEXOVV.Branch('FatJetMassPruned'    , FatJetMassPruned    ,  'FatJetMassPruned[NFatJet]/F'    )
    TreeEXOVV.Branch('FatJetMassFiltered'  , FatJetMassFiltered  ,  'FatJetMassFiltered[NFatJet]/F'  )
    TreeEXOVV.Branch('FatJetMassTrimmed'   , FatJetMassTrimmed   ,  'FatJetMassTrimmed[NFatJet]/F'   )
    TreeEXOVV.Branch('FatJetTau1'          , FatJetTau1          ,  'FatJetTau1[NFatJet]/F'          )
    TreeEXOVV.Branch('FatJetTau2'          , FatJetTau2          ,  'FatJetTau2[NFatJet]/F'          )
    TreeEXOVV.Branch('FatJetTau3'          , FatJetTau3          ,  'FatJetTau3[NFatJet]/F'          )
    TreeEXOVV.Branch('FatJetTau32'         , FatJetTau32         ,  'FatJetTau32[NFatJet]/F'         )
    TreeEXOVV.Branch('FatJetTau21'         , FatJetTau21         ,  'FatJetTau21[NFatJet]/F'         )
    TreeEXOVV.Branch('FatJetSDnsubjets'    , FatJetSDnsubjets    ,  'FatJetSDnsubjets[NFatJet]/F'    )
    TreeEXOVV.Branch('FatJetSDbdisc0'      , FatJetSDbdisc0      ,  'FatJetSDbdisc0[NFatJet]/F'      )
    TreeEXOVV.Branch('FatJetSDbdisc1'      , FatJetSDbdisc1      ,  'FatJetSDbdisc1[NFatJet]/F'      )
    TreeEXOVV.Branch('FatJetSDmaxbdisc'    , FatJetSDmaxbdisc    ,  'FatJetSDmaxbdisc[NFatJet]/F'    )
    TreeEXOVV.Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   ,  'FatJetSDsubjetWpt[NFatJet]/F'   )
    TreeEXOVV.Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass ,  'FatJetSDsubjetWmass[NFatJet]/F' )
    TreeEXOVV.Branch('FatJetSDsubjetWp4'   , FatJetSDsubjetWp4   ,  'FatJetSDsubjetWp4[NFatJet]/F'   )
    TreeEXOVV.Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   ,  'FatJetSDsubjetBpt[NFatJet]/F'   )
    TreeEXOVV.Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass ,  'FatJetSDsubjetBmass[NFatJet]/F' )
    TreeEXOVV.Branch('FatJetSDsubjetBp4'   , FatJetSDsubjetBp4   ,  'FatJetSDsubjetBp4[NFatJet]/F'   )
    TreeEXOVV.Branch('FatJetCorrUp'        , FatJetCorrUp        ,  'FatJetCorrUp[NFatJet]/F'        )
    TreeEXOVV.Branch('FatJetCorrDn'        , FatJetCorrDn        ,  'FatJetCorrDn[NFatJet]/F'        )


    TreeEXOVV.Branch('NGenJet'             , NGenJet             ,  'NGenJet/I'        )
    TreeEXOVV.Branch('GenJetPt'            , GenJetPt            ,  'GenJetPt[NGenJet]/F'            )
    TreeEXOVV.Branch('GenJetEta'           , GenJetEta           ,  'GenJetEta[NGenJet]/F'           )
    TreeEXOVV.Branch('GenJetPhi'           , GenJetPhi           ,  'GenJetPhi[NGenJet]/F'           )
    TreeEXOVV.Branch('GenJetRap'           , GenJetRap           ,  'GenJetRap[NGenJet]/F'           )
    TreeEXOVV.Branch('GenJetBDisc'         , GenJetBDisc         ,  'GenJetBDisc[NGenJet]/F'         )
    TreeEXOVV.Branch('GenJetRhoRatio'      , GenJetRhoRatio      ,  'GenJetRhoRatio[NGenJet]/F'      )
    TreeEXOVV.Branch('GenJetMass'          , GenJetMass          ,  'GenJetMass[NGenJet]/F'          )
    TreeEXOVV.Branch('GenJetMassSoftDrop'  , GenJetMassSoftDrop  ,  'GenJetMassSoftDrop[NGenJet]/F'  )

    

    TreeEXOVV.Branch('METpx'        , METpx        ,  'METpx/F'        )
    TreeEXOVV.Branch('METpy'        , METpy        ,  'METpy/F'        )
    TreeEXOVV.Branch('METpt'        , METpt        ,  'METpt/F'        )
    TreeEXOVV.Branch('METphi'       , METphi       ,  'METphi/F'       )
    TreeEXOVV.Branch('Nvtx'         , Nvtx         ,  'Nvtx/F'         )






#@ JET CORRECTIONS

ROOT.gSystem.Load('libCondFormatsJetMETObjects')

#Left out AK4 for now

#jecParStrAK4 = ROOT.std.string('JECs/PHYS14_25_V2_AK4PFchs.txt')
#jecUncAK4 = ROOT.JetCorrectionUncertainty( jecParStrAK4 )


if options.isMC : 
    print 'Getting L3 for AK4'
    L3JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L3Absolute_AK4PFchs.txt");
    print 'Getting L2 for AK4'
    L2JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L2Relative_AK4PFchs.txt");## USE 50 NS CORRECTIONS BUT THE UNCERTAINTY IS FOR 25
    print 'Getting L1 for AK4'
    L1JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L1FastJet_AK4PFchs.txt");


    print 'Getting L3 for AK8'
    L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L3Absolute_AK8PFchs.txt");
    print 'Getting L2 for AK8'
    L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L2Relative_AK8PFchs.txt");
    print 'Getting L1 for AK8'
    L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_MC_L1FastJet_AK8PFchs.txt");


    jecParStrAK8 = ROOT.std.string('JECs/Summer15_25nsV5_DATA_Uncertainty_AK8PFchs.txt')
    jecUncAK8 = ROOT.JetCorrectionUncertainty( jecParStrAK8 )

    
else :
    print 'Getting L3 for AK4'
    L3JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L3Absolute_AK4PFchs.txt");## same deal as above
    print 'Getting L2 for AK4'
    L2JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L2Relative_AK4PFchs.txt");
    print 'Getting L1 for AK4'
    L1JetParAK4  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L1FastJet_AK4PFchs.txt");
    # for data only :
    ResJetParAK4 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L2L3Residual_AK4PFchs.txt");

    print 'Getting L3 for AK8'
    L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L3Absolute_AK8PFchs.txt");
    print 'Getting L2 for AK8'
    L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L2Relative_AK8PFchs.txt");
    print 'Getting L1 for AK8'
    L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L1FastJet_AK8PFchs.txt");
    # for data only :
    ResJetParAK8 = ROOT.JetCorrectorParameters("JECs/Summer15_50nsV5_DATA_L2L3Residual_AK8PFchs.txt");


    
#  Load the JetCorrectorParameter objects into a vector, IMPORTANT: THE ORDER MATTERS HERE !!!! 
vParJecAK4 = ROOT.vector('JetCorrectorParameters')()
vParJecAK4.push_back(L1JetParAK4)
vParJecAK4.push_back(L2JetParAK4)
vParJecAK4.push_back(L3JetParAK4)
# for data only :
if not options.isMC : 
    vParJecAK4.push_back(ResJetParAK4)

ak4JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK4)

vParJecAK8 = ROOT.vector('JetCorrectorParameters')()
vParJecAK8.push_back(L1JetParAK8)
vParJecAK8.push_back(L2JetParAK8)
vParJecAK8.push_back(L3JetParAK8)
# for data only :
if not options.isMC : 
    vParJecAK8.push_back(ResJetParAK8)

ak8JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK8)

#@ EVENT LOOP

if options.verbose :
     print 'handles gotten, start event loop'    
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
    if options.verbose :
        print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break
    if options.verbose :
        print 'begin looping events'
    # loop over events in this file
    i = 0

    # Make sure the handles we want are in the files so we can
    # avoid leaking memory
    readFilters = True
    readTriggers = True

    
    for event in events: #{ Loop over events in root files
        if options.maxevents > 0 and nevents > options.maxevents :
            if options.verbose : 
                print 'breaking for max events'
            break
            
        i += 1
        nevents += 1


        ###################################################################
        # Event quantities.
        ###################################################################

        
        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)


        evWeight = 1.0

        
        lastRun = 1
        currRun = 1
        trigMap = {}
        ipt0 = -1

        # Speed up processing by preselecting an AK8 jet with high pt
        gotAK8 = event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )

        if gotAK8 == False :
            continue
        jetPtAK8 = h_jetsAK8Pt.product()
        if len( jetPtAK8) < 1 :
            continue
        if options.speedyPtMin != None : 
            if jetPtAK8[0] < options.speedyPtMin :
                continue


            
        
        #@ VERTEX SETS
        event.getByLabel( l_NPV, h_NPV )
        NPV = h_NPV.product()[0]
        if len(h_NPV.product()) == 0 :
            if options.verbose :
                print "Event has no good primary vertex."
            continue

            
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

                
        if options.applyFilters and readFilters :
            cscFilt = False
            vertexFilt = False
            hbheFilt = False

            
            gotit1 = event.getByLabel( l_filterNameStrings, h_filterNameStrings )
            gotit2 = event.getByLabel( l_filterBits, h_filterBits )
            #gotit3 = event.getByLabel( l_filterPrescales, h_filterPrescales )
            gotit4 = event.getByLabel( l_HBHEfilter, h_HBHEfilter )


            if options.verbose :
                print 'Filter string names?  ' + str(gotit1)
                print 'Filter bits?          ' + str(gotit2)

            if gotit1 == False or gotit2 == False  :
                readFilters = False

            filterNameStrings = h_filterNameStrings.product()
            filterBits = h_filterBits.product()

            hbheFilt = h_HBHEfilter.product()[0]
            
            for itrig in xrange(0, len(filterNameStrings) ) :
                if options.verbose :
                    print 'Filter name = ' + filterNameStrings[itrig]
                    print 'Filter bit  = ' + str(filterBits[itrig])
                if "CSC" in filterNameStrings[itrig] :
                    if filterBits[itrig] == 1 :
                        cscFilt = True
                # (Apply vertex filter later)
                #if "goodVer" in filterNameStrings[itrig] :
                #    if filterBits[itrig] == 1 :
                #        vertexFilt = True
                # (For now turn off HBHE filter, needs re-miniaod)
                #if "HBHE" in filterNameStrings[itrig] :
                #    if filterBits[itrig] == 1 :
                #        hbheFilt = True


            if cscFilt == False or hbheFilt == False :
                if options.verbose :
                    print 'Found filters, but they failed'
                continue

        if not readFilters :
            if options.verbose :
                print 'Did not find filters'
            continue




        if options.isMC and options.deweightFlat  : 
            #@ Event weights
            gotGenerator = event.getByLabel( l_generator, h_generator )
            if gotGenerator :

                if options.deweightFlat : 
                    #evWeight = evWeight * h_generator.product().weight()
                    pthat = 0.0
                    if h_generator.product().hasBinningValues() :
                        pthat = h_generator.product().binningValues()[0]
                        evWeight = evWeight * 1/pow(pthat/15.,4.5)
                    if options.verbose :
                        print 'Event weight = ' + str( evWeight )
                        print 'pthat = ' + str(pthat)
        if options.weightQCDSample != None :
            evWeight = evWeight * options.weightQCDSample
            if options.verbose :
                print 'Event weight = ' + str( evWeight )

        if options.verbose:
            print 'pre-hist fill event weight: ' + str(evWeight)
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

        if options.isMC : 
            event.getByLabel ( l_genJetsAK8Pt, h_genJetsAK8Pt )
            event.getByLabel ( l_genJetsAK8Eta, h_genJetsAK8Eta )
            event.getByLabel ( l_genJetsAK8Phi, h_genJetsAK8Phi )
            event.getByLabel ( l_genJetsAK8Mass, h_genJetsAK8Mass )
            event.getByLabel ( l_genJetsAK8SoftDropMass, h_genJetsAK8SoftDropMass )
            event.getByLabel ( l_genJetsAK8SoftDropPt, h_genJetsAK8SoftDropPt )
            event.getByLabel ( l_genJetsAK8SoftDropPhi, h_genJetsAK8SoftDropPhi )
            event.getByLabel ( l_genJetsAK8SoftDropEta, h_genJetsAK8SoftDropEta )
        
        
        # event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt ) got this above to speed things up
        event.getByLabel ( l_jetsAK8Eta, h_jetsAK8Eta )
        event.getByLabel ( l_jetsAK8Phi, h_jetsAK8Phi )
        event.getByLabel ( l_jetsAK8Mass, h_jetsAK8Mass )
        event.getByLabel ( l_jetsAK8Energy, h_jetsAK8Energy )
        event.getByLabel ( l_jetsAK8JEC, h_jetsAK8JEC )
        event.getByLabel ( l_jetsAK8Y, h_jetsAK8Y )
        event.getByLabel ( l_jetsAK8Area, h_jetsAK8Area )
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



        ak8JetsP4Corr = []
        ak8JetsCorrUp = []
        ak8JetsCorrDn = []
        ak8JetsP4SoftDropCorr = []
        ak8JetsPassID = []
        AK8SoftDropM = []
        AK8Tau21 = []
        AK8JetRho = []
        AK8JetZ = []

        AK8nhf = []
        AK8chf = []
        AK8nef = []
        AK8cef = []
        AK8nconstituents = []
        AK8nch = []
        AK8subjetDR = []
        AK8isFake = []
        if len( h_jetsAK8Pt.product()) > 0 : 
            AK8Pt = h_jetsAK8Pt.product()
            AK8Eta = h_jetsAK8Eta.product()
            AK8Phi = h_jetsAK8Phi.product()
            AK8Mass = h_jetsAK8Mass.product()
            AK8Energy = h_jetsAK8Energy.product()
            AK8Y = h_jetsAK8Y.product()

            AK8OldJEC = h_jetsAK8JEC.product()
            AK8Area = h_jetsAK8Area.product()
            AK8SoftDropM = h_jetsAK8SoftDropMass.product()
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




        if options.isMC : 
            if len( h_genJetsAK8Pt.product()) > 0 :
                GenAK8Pt = h_genJetsAK8Pt.product()
                GenAK8Eta = h_genJetsAK8Eta.product()
                GenAK8Phi = h_genJetsAK8Phi.product()
                GenAK8Mass = h_genJetsAK8Mass.product()
                GenAK8SoftDropPt = h_genJetsAK8SoftDropPt.product()
                GenAK8SoftDropEta = h_genJetsAK8SoftDropEta.product()
                GenAK8SoftDropPhi = h_genJetsAK8SoftDropPhi.product()
                GenAK8SoftDropMass = h_genJetsAK8SoftDropMass.product()
        

        njets = len(h_jetsAK8Pt.product())
        if options.maxjets == None :
            maxjets = njets            
        else :
            maxjets = min( njets, options.maxjets)
                          
        for i in range(0,maxjets):#{ Loop over AK8 Jets

            if options.verbose :
                print 'AK8 jet ' + str(i)


            AK8JECFromB2GAnaFW = AK8OldJEC[i]   
            AK8P4Raw = ROOT.TLorentzVector()
            AK8P4Raw.SetPtEtaPhiM( AK8Pt[i] , AK8Eta[i], AK8Phi[i], AK8Mass[i])
            # Remove the old JEC's to get raw energy
            AK8P4Raw *= AK8JECFromB2GAnaFW            
            
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

            ak8JetsPassID.append( goodJet )
            AK8nhf.append( nhf )
            AK8chf.append( chf )
            AK8nef.append( nef )
            AK8cef.append( cef )
            AK8nconstituents.append( nconstituents)
            AK8nch.append( nch )
            

            if options.verbose :
                print 'Good jet? ' + str(goodJet)
                    
            ak8JetCorrector.setJetEta( AK8P4Raw.Eta() )
            ak8JetCorrector.setJetPt ( AK8P4Raw.Perp() )
            ak8JetCorrector.setJetE  ( AK8P4Raw.E() )
            ak8JetCorrector.setJetA  ( AK8Area[i] )
            ak8JetCorrector.setRho   ( rho )
            ak8JetCorrector.setNPV   ( NPV )
            newJEC = ak8JetCorrector.getCorrection()
            AK8P4Corr = AK8P4Raw*newJEC
                                                    
            # Gen Jets
            if options.isMC:
                ak8GenJetsP4 = []
                ak8GenJetsSoftDropP4 = []
                if len( GenAK8Pt ) > 0 :
                    for igen in range(0, len( GenAK8Pt ) ):

                        genpt = GenAK8Pt[igen]
                        geneta = GenAK8Eta[igen]
                        genphi = GenAK8Phi[igen]
                        genmass = GenAK8Mass[igen]
                        gensoftdroppt = GenAK8SoftDropPt[igen]
                        gensoftdropeta = GenAK8SoftDropEta[igen]
                        gensoftdropphi = GenAK8SoftDropPhi[igen]
                        gensoftdropmass = GenAK8SoftDropMass[igen]

                        genp4 = ROOT.TLorentzVector()
                        genp4.SetPtEtaPhiM( genpt, geneta, genphi, genmass )
                        gensoftdropp4 = ROOT.TLorentzVector()
                        gensoftdropp4.SetPtEtaPhiM( gensoftdroppt, gensoftdropeta, gensoftdropphi, gensoftdropmass )
                        
                        ak8GenJetsP4.append( genp4 )
                        ak8GenJetsSoftDropP4.append( gensoftdropp4 )
            
                
            #@ JEC Scaling for AK8 Jets
            ak8JetsP4Corr.append( AK8P4Corr )
            if options.isMC  :
                jecUncAK8.setJetEta( AK8P4Corr.Eta() )
                jecUncAK8.setJetPt( AK8P4Corr.Perp() )
                ak8JetsCorrUp.append( 1. + jecUncAK8.getUncertainty(1) )
                jecUncAK8.setJetEta( AK8P4Corr.Eta() )
                jecUncAK8.setJetPt( AK8P4Corr.Perp() )
                ak8JetsCorrDn.append( 1. - jecUncAK8.getUncertainty(0) )
            else :
                ak8JetsCorrUp.append( -1.0 )
                ak8JetsCorrDn.append( -1.0 )

            tau21 = -1.0
            if AK8Tau1[i] > 0.0 :
                tau21 = AK8Tau2[i] / AK8Tau1[i]
            AK8Tau21.append( tau21 )

            if options.verbose :
                print 'tau21 = ' + str(tau21)

            #$ Get Jet Rho
            sp4_0 = None
            sp4_1 = None
            ival = int(AK8vSubjetIndex0[i])
            if options.verbose :
                print 'subjet index 0 = ' + str(ival)
            
            if ival > -1 :
                spt0    = AK8SubJetsPt[ival]
                seta0   = AK8SubJetsEta[ival]
                sphi0   = AK8SubJetsPhi[ival]
                sm0   = AK8SubJetsMass[ival]
                sp4_0 = ROOT.TLorentzVector()
                sp4_0.SetPtEtaPhiM( spt0, seta0, sphi0, sm0 )
            ival = int(AK8vSubjetIndex1[i])
            if options.verbose :
                print 'subjet index 1 = ' + str(ival)
            if ival > -1 :
                spt1    = AK8SubJetsPt[ival]
                seta1   = AK8SubJetsEta[ival]
                sphi1   = AK8SubJetsPhi[ival]
                sm1   = AK8SubJetsMass[ival]
                sp4_1 = ROOT.TLorentzVector()
                sp4_1.SetPtEtaPhiM( spt1, seta1, sphi1, sm1 )              
                                
            if sp4_0 == None or sp4_1 == None :
                if options.verbose :
                    print 'Did not find subjets'
                ak8JetsP4SoftDropCorr.append( None )
                AK8JetRho.append( None )
                AK8JetZ.append( None )
                AK8subjetDR.append( None )
            else :

                softdrop_p4 = sp4_0 + sp4_1
                ak8JetsP4SoftDropCorr.append( softdrop_p4 )
                jetR = 0.8
                jetrho = softdrop_p4.M() / (softdrop_p4.Perp() * jetR)
                jetrho *= jetrho
                jetz = 0.0                
                if sp4_0.Perp() > sp4_1.Perp() :
                    jetz = (sp4_1.Perp()) / ( sp4_0 + sp4_1).Perp()
                else :
                    jetz = (sp4_0.Perp()) / ( sp4_0 + sp4_1).Perp()

                AK8JetRho.append( jetrho )
                AK8JetZ.append( jetz )
                AK8subjetDR.append( sp4_0.DeltaR( sp4_1 ) )

                if options.verbose :
                    print "Corrected pt = " + str(AK8P4Corr.Perp())




        pt0 = ak8JetsP4Corr[0].Perp()
        if options.isMC :
            ipt0 = binFinder( pt0  )
            if options.verbose :
                print 'For MC : bin is ' + str(ipt0)
        elif options.applyTriggers and readTriggers :

            passTrig = False
            prescale = 1.0
            unprescaled = False
            
            gotit1 = event.getByLabel( l_triggerNameStrings, h_triggerNameStrings )
            gotit2 = event.getByLabel( l_triggerBits, h_triggerBits )
            gotit3 = event.getByLabel( l_triggerPrescales, h_triggerPrescales )

            
            ## if currRun != lastRun :
            ##     lastRun = currRun
            ##     fixTrigMap( trigMap, h_filterNameStrings )
            
            
            if options.verbose :
                print 'Trigger string names? ' + str(gotit1)
                print 'Trigger bits?         ' + str(gotit2)
            
            if gotit1 == False or gotit2 == False or gotit3 == False :
                readTriggers = False            

            triggerNameStrings = h_triggerNameStrings.product()
            triggerBits = h_triggerBits.product()
            triggerPrescales = h_triggerPrescales.product()            

            for itrig in xrange(0, len(triggerNameStrings) ) :
                if "HLT_PFJet" in triggerNameStrings[itrig] : #\
                  #or "HLT_PFHT" in triggerNameStrings[itrig] \
                  #or "HLT_HT" in triggerNameStrings[itrig] :
                    for itrigToGet, trigToGet in enumerate(trigsToGet) : 
                        if trigToGet in triggerNameStrings[itrig] :
                            trigIndex = itrigToGet
                            trigMap[ itrigToGet ] = int(triggerBits[itrig])                                          



            if options.writeTree and not options.isMC : 
                Trig[0] = 0
                for itrigForWrite in xrange( len(trigsToGet) - 1, -1, -1) :
                    if trigMap[itrigForWrite] > 0 :
                        Trig[0] += pow( 10, itrigForWrite)


        if options.writeTree :
            if options.verbose :
                print 'Writing hadronic tree'

            Weight              [0] = evWeight
            
            NFatJet             [0] = min( 2, len(ak8JetsP4Corr))
            for ifatjet in xrange( int(NFatJet[0]) ) :
                jetP4 = ak8JetsP4Corr[ifatjet]
                FatJetPt            [ifatjet] = jetP4.Perp()
                FatJetEta           [ifatjet] = jetP4.Eta()
                FatJetPhi           [ifatjet] = jetP4.Phi()
                FatJetRap           [ifatjet] = jetP4.Rapidity()
                if AK8JetRho[ifatjet] != None : 
                    FatJetRhoRatio      [ifatjet] = AK8JetRho[ifatjet]
                else :
                    FatJetRhoRatio      [ifatjet] = -1.
                if ak8JetsP4SoftDropCorr[ifatjet] != None : 
                    FatJetMassSoftDrop  [ifatjet] = ak8JetsP4SoftDropCorr[ifatjet].M()
                else :
                    FatJetMassSoftDrop  [ifatjet] = -1.0
                FatJetMass          [ifatjet] = jetP4.M()
                FatJetTau1          [ifatjet] = AK8Tau1[ifatjet]
                FatJetTau2          [ifatjet] = AK8Tau2[ifatjet]
                FatJetTau3          [ifatjet] = AK8Tau3[ifatjet]
                FatJetTau21         [ifatjet] = AK8Tau21[ifatjet]
                FatJetCorrUp        [ifatjet] = ak8JetsCorrUp[ifatjet]
                FatJetCorrDn        [ifatjet] = ak8JetsCorrDn[ifatjet]

            if options.isMC : 
                NGenJet             [0] = min( 2, len(ak8GenJetsP4))
                for igenjet in xrange( int(NGenJet[0]) ) :
                    jetP4 = ak8GenJetsP4[igenjet]
                    GenJetPt            [igenjet] = jetP4.Perp()
                    GenJetEta           [igenjet] = jetP4.Eta()
                    GenJetPhi           [igenjet] = jetP4.Phi()
                    GenJetRap           [igenjet] = jetP4.Rapidity()
                    GenJetMassSoftDrop  [igenjet] = ak8GenJetsSoftDropP4[igenjet].M()
                    GenJetMass          [igenjet] = jetP4.M()

                
            METpx               [0] = metPx
            METpy               [0] = metPy
            METpt               [0] = metPt
            METphi              [0] = metPhi     
            Nvtx                [0] = NPV
            TreeEXOVV.Fill()



f.cd()
TreeEXOVV.Write()
f.Close()