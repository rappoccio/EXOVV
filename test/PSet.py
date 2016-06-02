import FWCore.ParameterSet.Config as cms

process = cms.Process('NoSplit')

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring([
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_1.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_10.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_100.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_102.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_103.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_104.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_105.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_106.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_107.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_108.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_109.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_110.root',
    '/store/user/rappocc/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_b2ganafw74xV5_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/160601_023457/0000/B2GEDMNtuple_111.root',
    ]))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
