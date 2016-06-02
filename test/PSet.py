import FWCore.ParameterSet.Config as cms

process = cms.Process('NoSplit')

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring([
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_1.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_10.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_100.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_101.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_102.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_103.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_104.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_105.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_106.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_107.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_108.root',
    '/store/user/alkahn/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0/160307_165107/0000/B2GEDMNtuple_109.root',
    ]))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
