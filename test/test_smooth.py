#from ROOT import *
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import plotter, setup, get_ptbins, smooth
from optparse import OptionParser
from sysvar import plot_vars, reset
import pickle
parser = OptionParser()
                                 
(options, args) = parser.parse_args()

parton_shower = ROOT.TFile('PS_hists.root')

ps = parton_shower.Get('pythia8_unfolded_by_herwig'+str(4))
ps.SetLineColor(1)
psclone = ps.Clone("psclone")
smooth(psclone, delta = 5)
psclone.SetLineColor(2)

c1 = ROOT.TCanvas("c1", "c1")
ps.Draw()
psclone.Draw("same")
