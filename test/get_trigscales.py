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



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")


f = ROOT.TFile(options.file)

h1 = f.Get('h_trig')
h2 = f.Get('h_trigraw')

trigsToGet = [
    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500' 
    ]

for ibin in xrange( 1, h1.GetNbinsX() + 1 ) :
    x1 = float(h1.GetBinContent(ibin))
    x2 = float(h2.GetBinContent(ibin))
    if x2 > 0.0 :
        prescale = x1 / x2
    else :
        prescale = 0.
    print '%13s : %10.0f %10.0f %10.2f' % ( trigsToGet[ibin-1], x1, x2, prescale )
