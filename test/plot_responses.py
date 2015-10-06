#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = "qcd_allpt_withresponse.root",
                  help='Input file, without the .root')



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")

ROOT.gSystem.Load("RooUnfold/libRooUnfold")

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetPadBottomMargin(0.15)
ROOT.gStyle.SetPadTopMargin(0.15)
ROOT.gStyle.SetTitleOffset( 1.2, 'y')

f = ROOT.TFile(options.file )
responses = []
canvs = []
ptBins = [150., 200., 300., 400., 500., 600., 700., 800. ]
for ibin, inum in enumerate( ptBins ) :
    response = f.Get( "m_response_" + str( int(inum) ) )
    c = ROOT.TCanvas("c" + str(ibin), "c" + str(ibin), 600, 600 )
    hist = response.Hresponse()
    hist.UseCurrentStyle()
    hist.GetXaxis().SetRangeUser(0,400)
    hist.GetYaxis().SetRangeUser(0,400)
    if ibin < len(ptBins) - 1: 
        hist.SetTitle( 'p_{T} = ' + str(inum) + '-' + str(ptBins[ibin+1]) + ' GeV;m_{RECO} (GeV);m_{TRUE} (GeV)')
    elif ibin == len(ptBins) - 1 :
        hist.SetTitle( 'p_{T} > ' + str(inum) + ' GeV;m_{RECO} (GeV);m_{TRUE} (GeV)')
    hist.Draw("colz")
    responses.append(response)
    canvs.append(c)
    c.Print( 'response_' + str( int(inum) ) + '.png', 'png')
    c.Print( 'response_' + str( int(inum) ) + '.pdf', 'pdf')
