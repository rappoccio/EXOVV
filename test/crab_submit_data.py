from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EXOVV_JetHT_2015D'
config.General.workArea = 'crab_tightmatch'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = '/JetHT/algomez-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-f22ee4b431887aefaa4bd1ff29f8ab62/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data.sh'

config.JobType.outputFiles = ['outplots.root']
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'JetTreeDump_fwlite.py', 'JECs', 'purw.root' ]
