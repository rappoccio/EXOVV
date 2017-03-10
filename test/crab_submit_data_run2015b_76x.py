from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EXOVV_JetHT_2015B'
config.General.workArea = 'crab_2015B_76x_22nov'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = '/JetHT/srappocc-JetHT_Run2015B-16Dec2015-v1_B2GAnaFW_76X_V1p2-bc790ca2c39fc80d2d155816f7f6a0a6/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data_76x.sh'

config.JobType.outputFiles = ['outplots.root']
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'JetTreeDump_fwlite.py', 'JECs']
