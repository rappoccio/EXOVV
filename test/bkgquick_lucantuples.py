#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = "exovv_wv_v74x_v6_dataset6_ntuple.root",
                  help='Input file')


parser.add_option('--predFile', type='string', action='store',
                  dest='predFile',
                  default = "wv1263invpb_highpt_rate.root",
                  help='Predicted distribution file')


parser.add_option('--predHist', type='string', action='store',
                  dest='predHist',
                  default = "rLoMod",
                  help='Histogram from predFile to use as predicted rate')



parser.add_option('--modFile', type='string', action='store',
                  dest='modFile',
                  default = None,
                  help='File to get modified mass from')



parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "nom",
                  help='Label for plots')



parser.add_option('--tau21Cut', type='float', action='store',
                  default=0.6,
                  dest='tau21Cut',
                  help='Tau2 / Tau1 n-subjettiness cut')


parser.add_option('--sdmassCutLo', type='float', action='store',
                  default=50.,
                  dest='sdmassCutLo',
                  help='Lower softdrop mass cut')


parser.add_option('--sdmassCutHi', type='float', action='store',
                  default=105.,
                  dest='sdmassCutHi',
                  help='Upper softdrop mass cut')


parser.add_option('--LeptonType', type='int', action='store',
                  default=0,
                  dest='LeptonType',
                  help='Lepton type (0 = el, 1 = mu)')



parser.add_option('--weight', type='string', action='store',
                  default=None,
                  dest='weight',
                  help='Run on Data?')


(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math

ROOT.gSystem.Load("libAnalysisPredictedDistribution")

ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
#ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

lumi = 1263.88

# get the predicted distribution
predFile = ROOT.TFile( options.predFile )
hpredF = predFile.Get(options.predHist)
hpredF.SetName("junk")
hpred = ROOT.TH1D()
hpredF.Copy( hpred )
hpred.SetName("rLoMod")

if options.modFile != None : 
    fmod = ROOT.TFile( options.modFile )
    hModMassDist = fmod.Get("hModMass") # Need to run this script TWICE, first to get the MC-based mod mass, second to apply it. 
    hModMassDist.SetName("hModMassDist")
    binlo = hModMassDist.GetXaxis().FindBin( options.sdmassCutLo )
    binhi = hModMassDist.GetXaxis().FindBin( options.sdmassCutHi )
    maxbins = hModMassDist.GetNbinsX()
    for ibin in xrange(0,binlo) :
        hModMassDist.SetBinContent(ibin,0.0)
    for ibin in xrange(binhi, maxbins) :
        hModMassDist.SetBinContent(ibin,0.0)
    hModMassDist.Scale(1.0/hModMassDist.Integral())
    #modcanv = ROOT.TCanvas("modcanv", "modcanv")
    #hModMassDist.Draw()
    
f = ROOT.TFile( options.outlabel + '_predplots.root', "RECREATE")


hModMass = ROOT.TH1F("hModMass", "hModMass", 50, 0, 500.)


ROOT.SetOwnership( hpred, False )
predJetPt = ROOT.PredictedDistribution(hpred, "pred_jet_pt", "Jet p_{T} (GeV)", 30, 0, 3000.)
predJetMVV = ROOT.PredictedDistribution(hpred, "pred_mvv", "M_{VV} (GeV)", 50, 0.0, 5000.)
predJetMVVMod = ROOT.PredictedDistribution(hpred, "pred_mvvmod", "M_{VV} (GeV)", 50, 0.0, 5000.)
predJetSDMass = ROOT.PredictedDistribution(hpred, "pred_sdmass", "Soft Drop Mass", 50, 0.0, 250.)
predJetMass = ROOT.PredictedDistribution(hpred, "pred_jetmass", "Ungroomed Jet Mass", 50, 0.0, 250.)
predJetMassMod = ROOT.PredictedDistribution(hpred, "pred_jetmassmod", "Ungroomed Jet Mass", 50, 0.0, 250.)
predJetSDRho = ROOT.PredictedDistribution(hpred, "pred_sdrho", "Soft Drop Rho", 50, 0.0, 1.)

ROOT.SetOwnership( predJetPt, False )
ROOT.SetOwnership( predJetMVV, False )
ROOT.SetOwnership( predJetMVVMod, False )
ROOT.SetOwnership( predJetSDMass, False )
ROOT.SetOwnership( predJetMass, False )
ROOT.SetOwnership( predJetMassMod, False )

ROOT.SetOwnership( predJetSDRho, False )


# open the file
myfile = ROOT.TFile( options.infile )

# retrieve the ntuple of interest
t = ROOT.gDirectory.Get( 'otree' )
entries = t.GetEntriesFast()

for jentry in xrange( entries ):
    if jentry % 10000 == 0 :
        print 'processing ' + str(jentry)
    # get the next tree in the chain and verify
    ientry = t.LoadTree( jentry )
    if ientry < 0:
        break

    # copy next entry into memory and verify
    nb = t.GetEntry( jentry )
    if nb <= 0:
        continue

    FatJet = ROOT.TLorentzVector()
    FatJet.SetPtEtaPhiE( t.ungroomed_jet_pt, t.ungroomed_jet_eta, t.ungroomed_jet_phi, t.ungroomed_jet_e)
    sdm0 = t.jet_mass_so
    sdpt0 = t.jet_pt_so
    sdrho0 = -1.0
    if sdpt0 > 0. :
        sdrho0 = ( sdm0 / (sdpt0 * 0.8))**2
    Lepton = ROOT.TLorentzVector()
    Lepton.SetPtEtaPhiE( t.l_pt, t.l_eta, t.l_phi, t.l_e)
    MET = ROOT.TLorentzVector()
    MET.SetPtEtaPhiE( t.pfMET, 0., t.pfMET_Phi, t.pfMET )
    Vlep = Lepton + MET
    cut =\
      ( (options.LeptonType == 0 and Lepton.Perp() > 120. and MET.Perp() > 80.) or (options.LeptonType == 1 and Lepton.Perp() > 55. and MET.Perp() > 40.) )  and\
      Vlep.Perp() > 200. and\
      sdrho0 > 1e-3 and \
      FatJet.Perp() >   350. 


    if not cut :
        continue
    
    tau21 = t.jet_tau2tau1

    taggable = options.sdmassCutLo < sdm0 and sdm0 < options.sdmassCutHi

    if not taggable :
        continue

    if tau21 < options.tau21Cut    :
        tagged0 = True
    else :
        tagged0 = False

    hModMass.Fill( sdm0 )
    #print 'Accumulating pt = ' + str(t.FatJetPt) + ', tagged = ' + str( tagged0 )

    FatJetMod = ROOT.TLorentzVector( FatJet )
    if options.modFile != None :
        if FatJetMod.M() < options.sdmassCutLo or FatJetMod.M() > options.sdmassCutHi :
            massMod = hModMassDist.GetRandom()
        else :
            massMod = FatJetMod.M()
    else :
        massMod = FatJet.M()
    FatJetMod.SetPtEtaPhiM( FatJet.Perp(), FatJet.Eta(), FatJet.Phi(), massMod )
    vvCand = Vlep + FatJet
    vvCandMod = Vlep + FatJetMod

    weight = 1.0
    if options.weight != None :
        toks = options.weight.lstrip('(').rstrip(')').split('*')
        for tok in toks :
            weight *= getattr( t, tok )


    predJetPt.Accumulate( FatJet.Perp(), sdrho0, tagged0, weight )
    predJetMVV.Accumulate( vvCand.M(), sdrho0, tagged0, weight )
    predJetMVVMod.Accumulate( vvCandMod.M(), sdrho0, tagged0, weight )
    predJetSDMass.Accumulate( sdm0, sdrho0, tagged0, weight )
    predJetMass.Accumulate( FatJet.M(), sdrho0, tagged0, weight )
    predJetMassMod.Accumulate( FatJetMod.M(), sdrho0, tagged0, weight )
    predJetSDRho.Accumulate( sdrho0, sdrho0, tagged0, weight )



predJetPt.SetCalculatedErrors()
predJetMVV.SetCalculatedErrors()
predJetMVVMod.SetCalculatedErrors()
predJetSDMass.SetCalculatedErrors()
predJetMass.SetCalculatedErrors()
predJetMassMod.SetCalculatedErrors()
predJetSDRho.SetCalculatedErrors()


f.cd()
f.Write()

f.Close()
