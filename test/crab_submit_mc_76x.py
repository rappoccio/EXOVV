#!/usr/bin/env python
"""
This is a small script that submits a config over many datasets
"""
import os
from optparse import OptionParser

def getOptions() :
    """
    Parse and return the arguments provided by the user.
    """
    usage = ('usage: python submit_all.py -c CONFIG -d DIR ')

    parser = OptionParser(usage=usage)    

    parser.add_option("-f", "--datasets", dest="datasets",
        help=("File listing datasets to run over"),
        metavar="FILE")
    (options, args) = parser.parse_args()


    return options
    

def main():

    options = getOptions()

    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    config.section_("General")
    #config.General.requestName = 'EXOVV_QCD_Pt_170to300'
    config.General.workArea = 'crab_smpj_76x_rejec'
    config.General.transferOutputs = True
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe = 'execute_for_crab_mc_76x.sh'
    config.JobType.outputFiles = ['outplots.root']
    config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'JetTreeDump_fwlite.py', 'JECs', 'setup_lhapdf.csh' ]

    
    config.section_("Data")
    #config.Data.inputDataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/alkahn-RunIIFall15MiniAODv2-PU25nsData2015v1_B2GAnaFW_v76x_v1p0-a5b607ee9aade77691e6d24b0736dda8/USER'
    config.Data.inputDBS = 'phys03'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1

    config.section_("Site")
    config.Site.storageSite = 'T3_US_FNALLPC'



    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute commend'
            print hte.headers

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    datasetsFile = open( options.datasets )
    jobsLines = datasetsFile.readlines()
    jobs = []
    for ijob in jobsLines :
        s = ijob.rstrip()
        jobs.append( s )
        print '  --> added ' + s

        
    for ijob, job in enumerate(jobs) :

        datasetname = job.split('/')[1]
        config.General.requestName = 'SMPJ' + datasetname
        config.Data.inputDataset = job
        print 'Submitting ' + config.General.requestName + ', dataset = ' + job
        print 'Configuration :'
        #print config
        try :
            from multiprocessing import Process
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
            #submit(config)
        except :
            print 'Not submitted.'
        





if __name__ == '__main__':
    main()            
    
