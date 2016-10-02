import FWCore.ParameterSet.Config as cms

process = cms.Process('NoSplit')

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring([
'/store/user/lpctlbsm/B2GAnaFW_76X_V2p2/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/QCDPt470to600TuneCUETP8M113TeVpythia8RunIIFall15MiniAODv2-PU25nsData2015v176XmcRun2_B2GAnaFW_76X_V1p2/160624_161658/0000/B2GEDMNtuple_87.root'
    ]))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
