#! /usr/bin/env python

##################
# Stitch together a bunch of plots for W+Jets HT binned samples
##################

from optparse import OptionParser
parser = OptionParser()


parser.add_option('--infiles', type='string', action='store',
                  dest='infiles',
                  default = 'qcd_pt*_allpt.root',
                  help='Configuration of which file belongs to which label.')



parser.add_option('--outfile', type='string', action='store',
                  dest='outfile',
                  default = 'qcd_allpt.root',
                  help='Configuration. Entries look like "filename1.root Nevents1 xs1"')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
import glob
filenames = glob.glob(options.infiles)
files = []

ROOT.gSystem.Load("RooUnfold/libRooUnfold")

for iname in filenames : 
    files.append(ROOT.TFile( iname.rstrip() ) )


fout = ROOT.TFile(options.outfile, "RECREATE")
hists ={}

index = 0
for ii, ifile in enumerate(files) :
    keys = ifile.GetListOfKeys()
    nkeys = keys.GetSize()
    for ikey in xrange(0,nkeys) :
        key = keys[ikey]
        hist = ifile.Get(key.GetName()).Clone()
        if index == 0 : # Clone the first histograms
            hists[key.GetName()] = hist.Clone()
        else :
            hists[key.GetName()].Add( hist )
    index += 1

fout.cd()
for key,val in hists.items() :
    val.Write()
fout.Close()
print 'Done'
