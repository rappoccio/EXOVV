from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EXOVV_JetHT_2016B'
config.General.workArea = 'crab_2016B_80x_'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = '/JetHT/srappocc-RunIISpring16MiniAODv2_B2GAnaFW_80x_V1p0-c9ad27f972ae59d36cd924fb5f87408c/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = 'Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt'
config.Data.unitsPerJob = 50


config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data_80x.sh'

config.JobType.outputFiles = ['outplots.root']
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'JetTreeDump_fwlite.py', 'JECs']
