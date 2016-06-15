#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'jetht.root',
                  help='Input file')


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht_40pbinv_weighted_dataplots.root",
                  help='Output string for output file')

parser.add_option('--dir', type='string', action='store',
                  dest='dir',
                  default = "",
                  help='Directory containing root histograms')



parser.add_option('--rebin', type='int', action='store',
                  dest='rebin',
                  default = None,
                  help='Rebin if desired')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")

import array
from operator import itemgetter

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760.] )
scales = [
    30000.0,
    2000.0,
    65.63430429669079,
    11.732244475363055,
    3.967946158336121,
    1.2334089024152257,
    1.,
    #1.
    ]    
def isPFJet80 ( trig ) :
    return  int(trig) % 10 == 1 
def isPFJet140( trig ) :
    return ( int(trig / 10) % 10 == 1)
def isPFJet200( trig ) :
    return ( int(trig / 100) % 10 == 1)
def isPFJet260( trig ) :
    return ( int(trig / 1000) % 10 == 1)
def isPFJet320( trig ) :
    return ( int(trig / 10000) % 10 == 1)
def isPFJet400( trig ) :
    return ( int(trig / 100000) % 10 == 1)
def isPFJet450( trig ) :
    return ( int(trig / 10000000) % 10 == 1 or int(trig / 1000000) % 10 == 1)

names = [
    'PFJet80', 'PFJet140', 'PFJet200', 'PFJet260', 'PFJet320', 'PFJet400', 'PFJet450', 
    ]

trigfuncs = [isPFJet80, isPFJet140, isPFJet200, isPFJet260, isPFJet320, isPFJet400, isPFJet450]
ntrigs = len(trigfuncs)

trig1D = ROOT.TH1F("trig1D", "trig1D", ntrigs, 0, ntrigs )
trig2D = ROOT.TH2F("trig2D", "trig2D", ntrigs, 0, ntrigs, ntrigs, 0, ntrigs )

trig1Dscaled = ROOT.TH1F("trig1Dscaled", "trig1Dscaled", ntrigs, 0, ntrigs )
trig1Dscaled2 = ROOT.TH1F("trig1Dscaled2", "trig1Dscaled2", ntrigs, 0, ntrigs )

ROOT.gStyle.SetPadRightMargin(0.15)

f = ROOT.TFile(options.file)
trees = [ f.Get("TreeEXOVV") ]

for itree,t in enumerate(trees) :
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1]*5)
    Trig = array.array('i', [-1] )

    t.SetBranchStatus ('*', 0)
    #t.SetBranchStatus ('NFatJet', 1)
    #t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('Trig', 1)

    #t.SetBranchAddress ('NFatJet', NFatJet)
    #t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('Trig', Trig)
    
    entries = t.GetEntries()
    for jentry in xrange( entries ):
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break

        if jentry % 1000000 == 0 :
            print '%20d / %30d = %6.2f' % (jentry, entries, float(jentry)/entries * 100)

        if Trig[0] <= 0 :
            continue

        #print 'Trig = %10d' % (Trig[0]),
        #for itrig in xrange( len(names ) ):
        #    if trigfuncs[itrig](Trig[0]):
        #        print ' %10s' % (names[itrig]),
        #print ''
        #for ipt in xrange( NFatJet[0] ):
        #    print '%6.2f ' %( FatJetPt[ipt] ),
        #print ''
        for itrig in xrange( ntrigs-1, -1, -1):
            if trigfuncs[itrig]( Trig[0] ) :
                trig1D.Fill( itrig )
                trig1Dscaled.Fill( itrig, scales[itrig] )
                if itrig == ntrigs-1:
                    ptweight = 1.0
                else :
                    ptweight =  (ptBinA[itrig+1] - ptBinA[itrig])
                trig1Dscaled2.Fill( itrig, scales[itrig] / ptweight )
                for jtrig in xrange( ntrigs-1, -1, -1 ):
                    if jtrig != itrig and trigfuncs[jtrig](Trig[0]) :
                        trig2D.Fill( itrig, jtrig )
            

c1 = ROOT.TCanvas("c1", "c1")
trig1D.Draw()
c2 = ROOT.TCanvas("c2", "c2")
trig2D.Draw("box")
