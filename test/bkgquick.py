#!/usr/bin/env python
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = "exovv_wv_v74x_v6_dataset6_ntuple.root",
                  help='Input file')


parser.add_option('--predFile', type='string', action='store',
                  dest='predFile',
                  default = "wv1263invpb_nomass_highpt_rate.root",
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


parser.add_option('--weight', type='float', action='store',
                  default=None,
                  dest='weight',
                  help='Weight for sample')


parser.add_option('--isData', action='store_true',
                  default=False,
                  dest='isData',
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
ROOT.SetOwnership( predJetPt, False )
ROOT.SetOwnership( predJetMVV, False )
ROOT.SetOwnership( predJetMVVMod, False )

# open the file
myfile = ROOT.TFile( options.infile )

# retrieve the ntuple of interest
t = ROOT.gDirectory.Get( 'TreeEXOVV' )
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
    FatJet.SetPtEtaPhiM( t.FatJetPt, t.FatJetEta, t.FatJetPhi, t.FatJetMass)
    Lepton = ROOT.TLorentzVector()
    Lepton.SetPtEtaPhiE( t.LeptonPt, t.LeptonEta, t.LeptonPhi, t.LeptonEnergy)
    Vlep = ROOT.TLorentzVector()
    Vlep.SetPtEtaPhiE( t.VlepPt, t.VlepEta, t.VlepPhi, t.VlepEnergy)
    cut =\
      ( (t.LeptonType == 0 and t.LeptonPt > 120. and t.METpt > 80.) or (t.LeptonType == 1 and t.LeptonPt > 55. and t.METpt > 40.) )  and\
      t.VlepPt > 200. and\
      t.FatJetRhoRatio > 1e-3 and\
      t.LeptonIso / t.LeptonPt < 0.10  and \
      t.FatJetPt >   350. and \
      FatJet.DeltaR(Lepton) > ROOT.TMath.PiOver2()  and  \
      ROOT.TVector2.Phi_0_2pi( t.FatJetPhi - t.METphi) > ROOT.TMath.PiOver2()  and  \
      ROOT.TVector2.Phi_0_2pi( t.FatJetPhi - t.VlepPhi) > ROOT.TMath.PiOver2()  and  \
      t.MaxBDisc < 0.6
    trig =  ((t.LeptonType == 0 and t.Trig >= 7 ) or (t.LeptonType == 1 and t.Trig <= 2))


    

    if not cut :
        continue
    if options.isData and not trig :
        continue 
    
    tau21 = t.FatJetTau21
    sdrho0 = t.FatJetRhoRatio
    sdm0 = t.FatJetMassSoftDrop

    taggable = 15. < sdm0 

    if not taggable :
        continue


    hModMass.Fill( t.FatJetMass )
    
    if tau21 < options.tau21Cut and options.sdmassCutLo < sdm0  :
        tagged0 = True
    else :
        tagged0 = False

    #print 'Accumulating pt = ' + str(t.FatJetPt) + ', tagged = ' + str( tagged0 )

    vvCand = Vlep + FatJet

    FatJetMod = ROOT.TLorentzVector( FatJet )
    if options.modFile != None :
        if FatJetMod.M() < options.sdmassCutLo or FatJetMod.M() > options.sdmassCutHi :
            massMod = hModMassDist.GetRandom()
        else :
            massMod = FatJetMod.M()
    else :
        massMod = FatJet.M()
    FatJetMod.SetPtEtaPhiM( FatJet.Perp(), FatJet.Eta(), FatJet.Phi(), massMod )

    vvCandMod = Vlep + FatJetMod

    weight = 1.0

    if options.weight != None :
        weight = options.weight * lumi

    predJetPt.Accumulate( FatJet.Perp(), sdrho0, tagged0, weight )
    predJetMVV.Accumulate( vvCand.M(), sdrho0, tagged0, weight )
    predJetMVVMod.Accumulate( vvCandMod.M(), sdrho0, tagged0, weight )



predJetPt.SetCalculatedErrors()
predJetMVV.SetCalculatedErrors()
predJetMVVMod.SetCalculatedErrors()

f.cd()
f.Write()

f.Close()
