#!/usr/bin/env bash

export PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf6/6.1.5-cms/bin/:$PATH
export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf6/6.1.5-cms/lib/:$LD_LIBRARY_PATH
export PYTHONPATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf6/6.1.5-cms/lib/python2.7/site-packages/:$PYTHONPATH

python execute_for_crab.py --makeResponseMatrix2D --isMC --doPDFs --xrootd root://cmsxrootd.fnal.gov/ --applyTriggers --deweightFlat
