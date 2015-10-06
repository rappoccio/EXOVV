#! /usr/bin/env python

##################
# Stitch together a bunch of plots for W+Jets HT binned samples
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--config', type='string', action='store',
                  dest='config',
                  default = 'wjets_stitch_config.txt',
                  help='Configuration. Entries look like "label1 Nevents1 xs1"')

parser.add_option('--fileLabels', type='string', action='store',
                  dest='fileLabels',
                  default = 'wjets_pthi_labels.txt',
                  help='Configuration of which file belongs to which label.')



parser.add_option('--outfile', type='string', action='store',
                  dest='outfile',
                  default = 'wjets_stitched.root',
                  help='Configuration. Entries look like "filename1.root Nevents1 xs1"')


parser.add_option('--lum', type='float', action='store',
                  dest='lum',
                  default = 40.03,
                  help='Luminosity in pb')

parser.add_option('--withRooUnfold', action='store_true',
                  dest='withRooUnfold',
                  default = False,
                  help='load RooUnfold lib')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys


if options.withRooUnfold :
    ROOT.gSystem.Load("RooUnfold/libRooUnfold")

hists = {}
files = {}
nev = {}
xs = {}


print 'Getting file map'
infile1 = file( options.fileLabels )
lines = infile1.readlines()
for iline,line in enumerate(lines) :
    tokens = line.rstrip().split()
    #print tokens
    files[ tokens[0] ] = ROOT.TFile( tokens[1] )


print 'Getting weight map'
infile2 = file( options.config )
lines2 = infile2.readlines()
for iline2,line2 in enumerate(lines2) :
    tokens2 = line2.rstrip().split()
    #print tokens2
    key = tokens2[0]    
    nev[key] = float(tokens2[1] )
    xs[key]  = float(tokens2[2] )

#print files
#print nev
#print xs


fout = ROOT.TFile(options.outfile, "RECREATE")
hists ={}

index = 0
for ii in files.iterkeys() :
    ifile = files[ii]
    inev = nev[ii]
    ixs = xs[ii]    
    keys = ifile.GetListOfKeys()
    nkeys = keys.GetSize()
    for ikey in xrange(0,nkeys) :
        key = keys[ikey]
        print 'Getting ' + key.GetName()
        hist = ifile.Get(key.GetName()).Clone()
        hist.Sumw2()
        hist.Scale( ixs * options.lum / inev )
        if index == 0 : # Clone the first histograms
            hists[key.GetName()] = hist.Clone()
            print 'index = 0, cloned'
        else :
            hists[key.GetName()].Add( hist )
            print 'index = ' + str(index) + ', added'
    index += 1

fout.cd()
for key,val in hists.items() :
    val.Write()
fout.Close()
print 'Done'
