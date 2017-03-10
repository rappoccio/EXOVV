#!/usr/bin/env python
from optparse import OptionParser
from math import sqrt

parser = OptionParser()


parser.add_option('--datafiles', type='string', action='store',
                  dest='datafiles',
                  default = "MyDataPileupHistogram",
                  help='Data file plots')


parser.add_option('--mcfile', type='string', action='store',
                  dest='mcfile',
                  default = "responses_rejec_otherway_qcdmc_2dplots.root",
                  help='MC file plots')


parser.add_option('--outfile', type='string', action='store',
                  dest='outfile',
                  default = "purw.root",
                  help='PU reweight')


(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

fnom = ROOT.TFile(options.datafiles + '.root')
fup = ROOT.TFile(options.datafiles + 'Up.root')
fdn = ROOT.TFile(options.datafiles + 'Dn.root')

fmc = ROOT.TFile(options.mcfile)

hnom = fnom.Get("pileup")
hup = fup.Get("pileup")
hdn = fdn.Get("pileup")
hmc = fmc.Get("h_nvtx")

for hist in [hnom,hup,hdn,hmc]:
    hist.Sumw2()
    hist.Scale(1.0/hist.Integral())

    
for hist in [hnom,hup,hdn]:    
    hist.Divide( hmc )
    hist.Draw("same")

fout = ROOT.TFile(options.outfile, 'RECREATE')
for hist in [hnom,hup,hdn]:
    hist.Write()
