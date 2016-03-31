from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'EXOVV_QCD_Pt_170to300'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab.sh'

config.JobType.outputFiles = ['outplots.root']
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'JetTreeDump_fwlite.py', 'JECs', 'purw.root' ]
