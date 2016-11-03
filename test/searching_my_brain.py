#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = 'responses_rejec_otherway_qcdmc_2dplots.root',
                  help='String to append to MC names')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from unfold_utils import normalize_all_pt_bins

f = ROOT.TFile(options.infile)


truth1 = f.Get("PFJet_pt_m_AK8SDgen")
matrix = f.Get("2d_response_softdrop")
truth2 = matrix.Htruth()

normalize_all_pt_bins( truth1 )
normalize_all_pt_bins( truth2 )
projs = []

for ptbin in xrange( 1, truth1.GetNbinsY() + 1 ) :

    proj1 = truth1.ProjectionX("proj1_" + str(ptbin), ptbin, ptbin )
    proj2 = truth2.ProjectionX("proj2_" + str(ptbin), ptbin, ptbin )
    proj1.SetMarkerStyle(20)
    proj2.SetMarkerStyle(25)
    c = ROOT.TCanvas("c" + str(ptbin), "c" + str(ptbin) )
    proj1.Draw()
    proj2.Draw("same")
        
    projs.append ( [c, proj1, proj2] )
