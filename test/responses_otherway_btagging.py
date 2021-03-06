#!/usr/bin/env python
from optparse import OptionParser
from jettools import getJER
from math import sqrt

parser = OptionParser()


parser.add_option('--outlabel', type='string', action='store',
                  dest='outlabel',
                  default = "responses_otherway_btagged",
                  help='Label for plots')


parser.add_option('--maxEvents', type='int', action='store',
                  dest='maxEvents',
                  default = None,
                  help='Max events')


parser.add_option('--ptMin', type='float', action='store',
                  dest='ptMin',
                  default = 220.,
                  help='Max events')

parser.add_option('--bdisc', type='float', action='store',
                  dest='bdisc',
                  default = 0.6,
                  help='b discriminator cut')

parser.add_option('--herwigFlat', action='store_true',
                  dest='herwigFlat',
                  default = False,
                  help='Max events')



parser.add_option('--verbose', action='store_true',
                  dest='verbose',
                  default = False,
                  help='Verbosity')




parser.add_option('--split', type='int', action='store',
                  dest='split',
                  default = None,
                  help='Split section')


(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math
import random

ROOT.gSystem.Load("RooUnfold/libRooUnfold")

ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])
nbinsPt = len(ptBinA) - 1
mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])
nbinsm = len(mBinA) - 1

trueVarHist = ROOT.TH2F('truehist2d', 'truehist2D', nbinsm, mBinA, nbinsPt, ptBinA)
measVarHist = ROOT.TH2F('meashist2d', 'meashist2D', nbinsm, mBinA, nbinsPt, ptBinA)

response = ROOT.RooUnfoldResponse()
response.SetName("2d_response")
response.Setup(measVarHist, trueVarHist)

response_pdfup = ROOT.RooUnfoldResponse()
response_pdfup.SetName("2d_response_pdfup")
response_pdfup.Setup(measVarHist, trueVarHist)

response_pdfdn = ROOT.RooUnfoldResponse()
response_pdfdn.SetName("2d_response_pdfdn")
response_pdfdn.Setup(measVarHist, trueVarHist)

response_softdrop_pdfup = ROOT.RooUnfoldResponse()
response_softdrop_pdfup.SetName("2d_response_softdrop_pdfup")
response_softdrop_pdfup.Setup(measVarHist, trueVarHist)

response_softdrop_pdfdn = ROOT.RooUnfoldResponse()
response_softdrop_pdfdn.SetName("2d_response_softdrop_pdfdn")
response_softdrop_pdfdn.Setup(measVarHist, trueVarHist)

response_cteq = ROOT.RooUnfoldResponse()
response_cteq.SetName("2d_response_cteq")
response_cteq.Setup(measVarHist, trueVarHist)

response_softdrop_cteq = ROOT.RooUnfoldResponse()
response_softdrop_cteq.SetName("2d_response_softdrop_cteq")
response_softdrop_cteq.Setup(measVarHist, trueVarHist)

response_mstw = ROOT.RooUnfoldResponse()
response_mstw.SetName("2d_response_mstw")
response_mstw.Setup(measVarHist, trueVarHist)

response_softdrop_mstw = ROOT.RooUnfoldResponse()
response_softdrop_mstw.SetName("2d_response_softdrop_mstw")
response_softdrop_mstw.Setup(measVarHist, trueVarHist)

response_jecup = ROOT.RooUnfoldResponse()
response_jecup.SetName("2d_response_jecup")
response_jecup.Setup(measVarHist, trueVarHist)

response_jecdn = ROOT.RooUnfoldResponse()
response_jecdn.SetName("2d_response_jecdn")
response_jecdn.Setup(measVarHist, trueVarHist)

response_jerup = ROOT.RooUnfoldResponse()
response_jerup.SetName("2d_response_jerup")
response_jerup.Setup(measVarHist, trueVarHist)

response_jerdn = ROOT.RooUnfoldResponse()
response_jerdn.SetName("2d_response_jerdn")
response_jerdn.Setup(measVarHist, trueVarHist)

response_jernom = ROOT.RooUnfoldResponse()
response_jernom.SetName("2d_response_jernom")
response_jernom.Setup(measVarHist, trueVarHist)

response_jmrup = ROOT.RooUnfoldResponse()
response_jmrup.SetName("2d_response_jmrup")
response_jmrup.Setup(measVarHist, trueVarHist)

response_jmrdn = ROOT.RooUnfoldResponse()
response_jmrdn.SetName("2d_response_jmrdn")
response_jmrdn.Setup(measVarHist, trueVarHist)

response_jmrnom = ROOT.RooUnfoldResponse()
response_jmrnom.SetName("2d_response_jmrnom")
response_jmrnom.Setup(measVarHist, trueVarHist)

response_nomnom = ROOT.RooUnfoldResponse()
response_nomnom.SetName("2d_response_nomnom")
response_nomnom.Setup(measVarHist, trueVarHist)



response_softdrop = ROOT.RooUnfoldResponse()
response_softdrop.SetName("2d_response_softdrop")
response_softdrop.Setup(measVarHist, trueVarHist)


response_softdrop_jecup = ROOT.RooUnfoldResponse()
response_softdrop_jecup.SetName("2d_response_softdrop_jecup")
response_softdrop_jecup.Setup(measVarHist, trueVarHist)

response_softdrop_jecdn = ROOT.RooUnfoldResponse()
response_softdrop_jecdn.SetName("2d_response_softdrop_jecdn")
response_softdrop_jecdn.Setup(measVarHist, trueVarHist)

response_softdrop_jerup = ROOT.RooUnfoldResponse()
response_softdrop_jerup.SetName("2d_response_softdrop_jerup")
response_softdrop_jerup.Setup(measVarHist, trueVarHist)

response_softdrop_jerdn = ROOT.RooUnfoldResponse()
response_softdrop_jerdn.SetName("2d_response_softdrop_jerdn")
response_softdrop_jerdn.Setup(measVarHist, trueVarHist)

response_softdrop_jernom = ROOT.RooUnfoldResponse()
response_softdrop_jernom.SetName("2d_response_softdrop_jernom")
response_softdrop_jernom.Setup(measVarHist, trueVarHist)

response_softdrop_jmrup = ROOT.RooUnfoldResponse()
response_softdrop_jmrup.SetName("2d_response_softdrop_jmrup")
response_softdrop_jmrup.Setup(measVarHist, trueVarHist)

response_softdrop_jmrdn = ROOT.RooUnfoldResponse()
response_softdrop_jmrdn.SetName("2d_response_softdrop_jmrdn")
response_softdrop_jmrdn.Setup(measVarHist, trueVarHist)

response_softdrop_jmrnom = ROOT.RooUnfoldResponse()
response_softdrop_jmrnom.SetName("2d_response_softdrop_jmrnom")
response_softdrop_jmrnom.Setup(measVarHist, trueVarHist)

response_softdrop_nomnom = ROOT.RooUnfoldResponse()
response_softdrop_nomnom.SetName("2d_response_softdrop_nomnom")
response_softdrop_nomnom.Setup(measVarHist, trueVarHist)


h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_gen = ROOT.TH2F('PFJet_pt_m_AK8Gen', 'Generator Mass vs. P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)

h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_genSD = ROOT.TH2F('PFJet_pt_m_AK8SDgen', 'Generator Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)


h_2DHisto_nomnom_meas = ROOT.TH2F('PFJet_pt_m_AK8_nomnom', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_nomnom_gen = ROOT.TH2F('PFJet_pt_m_AK8Gen_nomnom', 'Generator Mass vs. P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)

h_2DHisto_nomnom_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD_nomnom', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)
h_2DHisto_nomnom_genSD = ROOT.TH2F('PFJet_pt_m_AK8SDgen_nomnom', 'Generator Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA)


h_pt_meas = ROOT.TH1F("h_pt_meas", ";Jet p_{T} (GeV); Number", 150, 0, 3000)
h_y_meas = ROOT.TH1F("h_y_meas", ";Jet Rapidity; Number", 50, -2.5, 2.5 )
h_phi_meas = ROOT.TH1F("h_phi_meas", ";Jet #phi (radians); Number", 50, -ROOT.TMath.Pi(), ROOT.TMath.Pi() )
h_m_meas = ROOT.TH1F("h_m_meas", ";Jet Mass (GeV); Number", 50, 0, 500 )
h_msd_meas = ROOT.TH1F("h_msd_meas", ";Jet Soft Drop Mass (GeV); Number", 50, 0, 500 )
h_rho_meas = ROOT.TH1F("h_rho_meas", ";Jet (m/p_{T}R)^{2}; Number", 100, 0, 1.0 )
h_tau21_meas = ROOT.TH1F("h_tau21_meas", ";Jet #tau_{2}/#tau_{1}; Number", 50, 0, 1.0 )
h_dphi_meas = ROOT.TH1F("h_dphi_meas", ";Jet #phi (radians); Number", 50, 0, ROOT.TMath.TwoPi() )
h_ptasym_meas = ROOT.TH1F("h_ptasym_meas", ";Jet (p_{T1} - p_{T2}) / (p_{T1} + p_{T2}); Number", 50, 0, 1.0 )
h_rho_vs_tau_meas = ROOT.TH2F("h_rho_vs_tau21_meas", ";Jet (m/p_{T}R)^{2};Jet #tau_{2}/#tau_{1}", 100, 0, 1.0, 50, 0, 1.0 )

h_massup = ROOT.TH1F("h_massup", "JMR Up Variation", nbinsm, mBinA)
h_massdn = ROOT.TH1F("h_massdn", "JMR Down Variation", nbinsm, mBinA)
h_massnom = ROOT.TH1F("h_massnom", "JMR Nominal", nbinsm, mBinA)

h_massup_softdrop = ROOT.TH1F("h_massup_softdrop", "JMR Up Softdrop", nbinsm, mBinA)
h_massdn_softdrop = ROOT.TH1F("h_massdn_softdrop", "JMR Down Softdrop", nbinsm, mBinA)
h_massnom_softdrop = ROOT.TH1F("h_massnom_softdrop", "JMR Nominal Softdrop", nbinsm, mBinA)

h_mreco_mgen = ROOT.TH1F("h_mreco_mgen", "Reco Mass/Gen Mass", 1000, 0, 2)
h_ptreco_ptgen = ROOT.TH1F("h_ptreco_ptgen", "Reco Pt/Gen Pt", 1000, 0, 2)
h_mreco_mgen_softdrop = ROOT.TH1F("h_mreco_mgen_softdrop", "Reco Mass/Gen Mass Softdrop", 1000, 0, 2)
h_ptreco_ptgen_softdrop = ROOT.TH1F("h_ptreco_ptgen_softdrop", "Reco Pt/Gen Pt Softdrop", 1000, 0, 2)

h_mreco_mgen_nomnom = ROOT.TH1F("h_mreco_mgen_nomnom", "Reco Mass/Gen Mass", 1000, 0, 2)
h_ptreco_ptgen_nomnom = ROOT.TH1F("h_ptreco_ptgen_nomnom", "Reco Pt/Gen Pt", 1000, 0, 2)
h_mreco_mgen_softdrop_nomnom = ROOT.TH1F("h_mreco_mgen_softdrop_nomnom", "Reco Mass/Gen Mass Softdrop", 1000, 0, 2)
h_ptreco_ptgen_softdrop_nomnom = ROOT.TH1F("h_ptreco_ptgen_softdrop_nomnom", "Reco Pt/Gen Pt Softdrop", 1000, 0, 2)



h2_y_meas = ROOT.TH2F("h2_y_meas", ";Jet Rapidity; Number", nbinsPt, ptBinA, 50, -2.5, 2.5 )
h2_phi_meas = ROOT.TH2F("h2_phi_meas", ";Jet #phi (radians); Number", nbinsPt, ptBinA, 50, -ROOT.TMath.Pi(), ROOT.TMath.Pi() )
h2_m_meas = ROOT.TH2F("h2_m_meas", ";Jet Mass (GeV); Number", nbinsPt, ptBinA, 50, 0, 500 )
h2_msd_meas = ROOT.TH2F("h2_msd_meas", ";Jet Soft Drop Mass (GeV); Number", nbinsPt, ptBinA, 50, 0, 500 )
h2_rho_meas = ROOT.TH2F("h2_rho_meas", ";Jet (m/p_{T}R)^{2}; Number", nbinsPt, ptBinA, 100, 0, 1.0 )
h2_tau21_meas = ROOT.TH2F("h2_tau21_meas", ";Jet #tau_{2}/#tau_{1}; Number", nbinsPt, ptBinA, 50, 0, 1.0 )
h2_dphi_meas = ROOT.TH2F("h2_dphi_meas", ";Jet #phi (radians); Number", nbinsPt, ptBinA, 50, 0, ROOT.TMath.TwoPi() )
h2_ptasym_meas = ROOT.TH2F("h2_ptasym_meas", ";Jet (p_{T1} - p_{T2}) / (p_{T1} + p_{T2}); Number", nbinsPt, ptBinA, 50, 0, 1.0 )

h2_massup = ROOT.TH2F("h2_massup", "JMR Up Variation", nbinsPt, ptBinA, nbinsm, mBinA)
h2_massdn = ROOT.TH2F("h2_massdn", "JMR Down Variation", nbinsPt, ptBinA, nbinsm, mBinA)
h2_massnom = ROOT.TH2F("h2_massnom", "JMR Nominal", nbinsPt, ptBinA, nbinsm, mBinA)

h2_massup_softdrop = ROOT.TH2F("h2_massup_softdrop", "JMR Up Softdrop", nbinsPt, ptBinA, nbinsm, mBinA)
h2_massdn_softdrop = ROOT.TH2F("h2_massdn_softdrop", "JMR Down Softdrop", nbinsPt, ptBinA, nbinsm, mBinA)
h2_massnom_softdrop = ROOT.TH2F("h2_massnom_softdrop", "JMR Nominal Softdrop", nbinsPt, ptBinA, nbinsm, mBinA)

h2_mreco_mgen = ROOT.TH2F("h2_mreco_mgen", "Reco Mass/Gen Mass", nbinsPt, ptBinA, 1000, 0, 2)
h2_ptreco_ptgen = ROOT.TH2F("h2_ptreco_ptgen", "Reco Pt/Gen Pt", nbinsPt, ptBinA, 1000, 0, 2)
h2_mreco_mgen_softdrop = ROOT.TH2F("h2_mreco_mgen_softdrop", "Reco Mass/Gen Mass Softdrop", nbinsPt, ptBinA, 1000, 0, 2)
h2_ptreco_ptgen_softdrop = ROOT.TH2F("h2_ptreco_ptgen_softdrop", "Reco Pt/Gen Pt Softdrop", nbinsPt, ptBinA, 1000, 0, 2)

h2_mreco_mgen_nomnom = ROOT.TH2F("h2_mreco_mgen_nomnom", "Reco Mass/Gen Mass", nbinsPt, ptBinA, 1000, 0, 2)
h2_ptreco_ptgen_nomnom = ROOT.TH2F("h2_ptreco_ptgen_nomnom", "Reco Pt/Gen Pt", nbinsPt, ptBinA, 1000, 0, 2)
h2_mreco_mgen_softdrop_nomnom = ROOT.TH2F("h2_mreco_mgen_softdrop_nomnom", "Reco Mass/Gen Mass Softdrop", nbinsPt, ptBinA, 1000, 0, 2)
h2_ptreco_ptgen_softdrop_nomnom = ROOT.TH2F("h2_ptreco_ptgen_softdrop_nomnom", "Reco Pt/Gen Pt Softdrop", nbinsPt, ptBinA, 1000, 0, 2)



sysvarstr = ['jecup', 'jecdn', 'jerup', 'jerdn', 'jmrup', 'jmrdn', 'pdfup', 'pdfdn', 'cteq', 'mstw' ]
jecup_ndx = sysvarstr.index('jecup')
jecdn_ndx = sysvarstr.index('jecdn')
jerup_ndx = sysvarstr.index('jerup')
jerdn_ndx = sysvarstr.index('jerdn')
jmrup_ndx = sysvarstr.index('jmrup')
jmrdn_ndx = sysvarstr.index('jmrdn')
pdfup_ndx = sysvarstr.index('pdfup')
pdfdn_ndx = sysvarstr.index('pdfdn')
cteq_ndx  = sysvarstr.index('cteq')
mstw_ndx  = sysvarstr.index('mstw')

h2_y_meas_sys      = []
h2_phi_meas_sys    = []
h2_m_meas_sys      = []
h2_msd_meas_sys    = []
h2_rho_meas_sys    = []
h2_tau21_meas_sys  = []
h2_dphi_meas_sys   = []
h2_ptasym_meas_sys = []
h_2DHisto_meas_sys= []
h_2DHisto_measSD_sys = []

for isys in sysvarstr : 
    h2_y_meas_sys      .append(  ROOT.TH2F("h2_y_meas_sys" + isys, ";Jet Rapidity; Number", nbinsPt, ptBinA, 50, -2.5, 2.5 ))
    h2_phi_meas_sys    .append(  ROOT.TH2F("h2_phi_meas_sys" + isys, ";Jet #phi (radians); Number", nbinsPt, ptBinA, 50, -ROOT.TMath.Pi(), ROOT.TMath.Pi()) )
    h2_m_meas_sys      .append(  ROOT.TH2F("h2_m_meas_sys" + isys, ";Jet Mass (GeV); Number", nbinsPt, ptBinA, 50, 0, 500 ))
    h2_msd_meas_sys    .append(  ROOT.TH2F("h2_msd_meas_sys" + isys, ";Jet Soft Drop Mass (GeV); Number", nbinsPt, ptBinA, 50, 0, 500 ))
    h2_rho_meas_sys    .append(  ROOT.TH2F("h2_rho_meas_sys" + isys, ";Jet (m/p_{T}R))^{2}; Number", nbinsPt, ptBinA, 100, 0, 1.0 ))
    h2_tau21_meas_sys  .append(  ROOT.TH2F("h2_tau21_meas_sys" + isys, ";Jet #tau_{2}/#tau_{1}; Number", nbinsPt, ptBinA, 50, 0, 1.0 ))
    h2_dphi_meas_sys   .append(  ROOT.TH2F("h2_dphi_meas_sys" + isys, ";Jet #phi (radians); Number", nbinsPt, ptBinA, 50, 0, ROOT.TMath.TwoPi()) )
    h2_ptasym_meas_sys .append(  ROOT.TH2F("h2_ptasym_meas_sys" + isys, ";Jet (p_{T1} - p_{T2})) / (p_{T1} + p_{T2}); Number", nbinsPt, ptBinA, 50, 0, 1.0 ))
    h_2DHisto_meas_sys.append( ROOT.TH2F('PFJet_pt_m_AK8_sys'+isys, 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA) )
    h_2DHisto_measSD_sys.append( ROOT.TH2F('PFJet_pt_m_AK8SD_sys'+isys, 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsPt, ptBinA) )






def getMatched( p4, coll, dRMax = 0.4) :
    if coll != None : 
        for i,c in enumerate(coll):
            if p4.DeltaR(c) < dRMax :
                return i
    return None



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


deweightFlat = False


if not options.herwigFlat :
    input_names_file = open("outplots_names.txt", "r")
    qcdIn = []
    for line in input_names_file:
        print 'adding ' + line
        qcdIn.append(ROOT.TFile.Open(line.rstrip() ))
        #qcdIn =[
        #ROOT.TFile('qcdpy8_170to300_rejec.root'),
        #ROOT.TFile('qcdpy8_300to470_rejec.root'),
        #ROOT.TFile('qcdpy8_470to600_rejec.root'),
        #ROOT.TFile('qcdpy8_600to800_rejec.root'),
        #ROOT.TFile('qcdpy8_800to1000_rejec.root'),
        #ROOT.TFile('qcdpy8_1000to1400_rejec.root'),
        #ROOT.TFile('qcdpy8_1400to1800_rejec.root'),
        #ROOT.TFile('qcdpy8_1800to2400_rejec.root'),
        #ROOT.TFile('qcdpy8_2400to3200_rejec.root'),
        #ROOT.TFile('qcdpy8_3200toinf_rejec.root'),
        #]
        #qcdWeights =[
        #117276.      / 6918748.,  #170to300
        #7823.        / 5968960.,  #300to470
        #648.2        / 3977770.,  #470to600
        #186.9        / 3979884.,  #600to800
        #32.293       / 3973224.,  #800to1000
        #9.4183       / 2953982.,  #1000to1400
        #0.84265      / 395725. ,  #1400to1800
        #0.114943     / 393760. ,  #1800to2400
        #0.00682981   / 398452. ,  #2400to3200
        #0.000165445  / 391108. ,  #3200toInf
        #]
    qcdWeights =      [117276.      / 6918748.]*165  #170to300
    qcdWeights.extend([7823.        / 5968960.]*144) #300to470
    qcdWeights.extend([648.2        / 3977770.]*89)  #470to600
    qcdWeights.extend([186.9        / 3979884.]*91)  #600to800
    qcdWeights.extend([32.293       / 3973224.]*98)  #800to1000
    qcdWeights.extend([9.4183       / 2953982.]*89)  #1000to1400
    qcdWeights.extend([0.84265      / 395725. ]*9)   #1400to1800
    qcdWeights.extend([0.114943     / 393760. ]*9)   #1800to2400
    qcdWeights.extend([0.00682981   / 398452. ]*9)   #2400to3200
    qcdWeights.extend([0.000165445  / 391108. ]*9)   #3200toInf

else :
    qcdIn =[
        ROOT.TFile('qcdherwig_flat_rejec.root'),
        ]
    qcdWeights =[
        1.0
        ]
    deweightFlat = True
        
masslessSD = 0


trees = []
# Append the actual TTrees
if options.split == None : 
    for iq in qcdIn:
        trees.append( iq.Get("TreeEXOVV") )
	print 'tree found for '+ str(iq)
else : 
    trees.append( qcdIn[options.split].Get("TreeEXOVV") )
    
if options.split != None : 
    fout = ROOT.TFile(options.outlabel +'_' + str(options.split), 'RECREATE')
else : 
    fout = ROOT.TFile(options.outlabel, 'RECREATE')

for itree,t in enumerate(trees) :
    Weight = array.array('f', [-1])    
    NFatJet = array.array('i', [0] )
    
    NNPDF3weight_CorrDn = array.array('f', [-1.])
    NNPDF3weight_CorrUp = array.array('f', [-1.])


    CTEQweight_Central = array.array('f', [-1.])
    MSTWweight_Central = array.array('f', [-1.])

    
    FatJetPt = array.array('f', [-1]*5)
    FatJetEta = array.array('f', [-1]*5)
    FatJetRap = array.array('f', [-1]*5)
    FatJetPhi = array.array('f', [-1]*5)
    FatJetMass = array.array('f', [-1]*5)
    FatJetMassSoftDrop = array.array('f', [-1]*5)
    FatJetTau21 = array.array('f', [-1]*5)
    FatJetCorrUp = array.array('f', [-1]*5)
    FatJetCorrDn = array.array('f', [-1]*5)
    FatJetRhoRatio = array.array('f', [-1]*5)
    FatJetBDisc = array.array('f', [-1]*5)
    NGenJet = array.array('i', [0] )
    GenJetPt = array.array('f', [-1]*5)
    GenJetEta = array.array('f', [-1]*5)
    GenJetPhi = array.array('f', [-1]*5)
    GenJetMass = array.array('f', [-1]*5)
    GenJetMassSoftDrop = array.array('f', [-1]*5)
    GenJetRhoRatio = array.array('f', [-1]*5)
    FatJetPtSoftDrop = array.array('f', [-1]*5)
    GenJetPtSoftDrop = array.array('f', [-1]*5)
    NGenPart = array.array('i', [0] )
    GenPartID = array.array('f', [-1]*20)
    GenPartMom0ID = array.array('f', [-1]*20)
    GenPartPt = array.array('f', [-1]*20)
    GenPartEta = array.array('f', [-1]*20)
    GenPartPhi = array.array('f', [-1]*20)
    GenPartMass = array.array('f', [-1]*20)
    
    
    
    Trig = array.array('i', [-1] )
    
    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('Weight', 1)
    t.SetBranchStatus ('NFatJet', 1)
    t.SetBranchStatus ('NGenJet', 1)
    t.SetBranchStatus ('NGenPart', 1)
    t.SetBranchStatus ('GenPartID'  , 1)
    t.SetBranchStatus ('GenPartMom0ID'  , 1)
    t.SetBranchStatus ('GenPartPt'  , 1)
    t.SetBranchStatus ('GenPartEta' , 1)
    t.SetBranchStatus ('GenPartPhi' , 1)
    t.SetBranchStatus ('GenPartMass', 1)

    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetEta', 1)
    t.SetBranchStatus ('FatJetRap', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetBDisc', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus ('GenJetPt', 1)
    t.SetBranchStatus ('GenJetEta', 1)
    t.SetBranchStatus ('GenJetPhi', 1)
    t.SetBranchStatus ('GenJetMass', 1)
    t.SetBranchStatus ('GenJetMassSoftDrop', 1)    
    t.SetBranchStatus ('FatJetRhoRatio', 1)
    t.SetBranchStatus ('FatJetTau21', 1)
    t.SetBranchStatus ('FatJetCorrUp', 1)
    t.SetBranchStatus ('FatJetCorrDn', 1)
    t.SetBranchStatus ('Trig', 1)
    t.SetBranchStatus ('GenJetRhoRatio', 1)
    t.SetBranchStatus ('GenJetPtSoftDrop', 1)
    t.SetBranchStatus ('FatJetPtSoftDrop', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrDn', 1)
    t.SetBranchStatus ('NNPDF3weight_CorrUp', 1)
    t.SetBranchStatus ('FatJetSDmaxbdisc', 1)

    t.SetBranchStatus ('CTEQweight_Central', 1)
    t.SetBranchStatus ('MSTWweight_Central', 1)


    t.SetBranchAddress ('NNPDF3weight_CorrDn', NNPDF3weight_CorrDn)
    t.SetBranchAddress ('NNPDF3weight_CorrUp', NNPDF3weight_CorrUp)
    t.SetBranchAddress ('CTEQweight_Central', CTEQweight_Central)
    t.SetBranchAddress ('MSTWweight_Central', MSTWweight_Central)
    t.SetBranchAddress ('Weight', Weight)
    t.SetBranchAddress ('NFatJet', NFatJet)
    t.SetBranchAddress ('NGenJet', NGenJet)
    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetEta', FatJetEta)
    t.SetBranchAddress ('FatJetRap', FatJetRap)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress ('FatJetCorrUp', FatJetCorrUp)
    t.SetBranchAddress ('FatJetCorrDn', FatJetCorrDn)
    t.SetBranchAddress ('GenJetPt', GenJetPt)
    t.SetBranchAddress ('GenJetEta', GenJetEta)
    t.SetBranchAddress ('GenJetPhi', GenJetPhi)
    t.SetBranchAddress ('GenJetMass', GenJetMass)
    t.SetBranchAddress ('GenJetMassSoftDrop', GenJetMassSoftDrop)
    t.SetBranchAddress ('FatJetRhoRatio', FatJetRhoRatio)
    t.SetBranchAddress ('FatJetTau21', FatJetTau21)
    t.SetBranchAddress ('Trig', Trig)
    t.SetBranchAddress ('GenJetRhoRatio', GenJetRhoRatio)
    t.SetBranchAddress ('FatJetPtSoftDrop', FatJetPtSoftDrop)
    t.SetBranchAddress ('GenJetPtSoftDrop', GenJetPtSoftDrop)
    t.SetBranchAddress ('FatJetBDisc', FatJetBDisc)
    t.SetBranchAddress ('NGenPart', NGenPart)
    t.SetBranchAddress ('GenPartID', GenPartID)
    t.SetBranchAddress ('GenPartMom0ID', GenPartMom0ID)
    t.SetBranchAddress ('GenPartPt', GenPartPt)
    t.SetBranchAddress ('GenPartEta', GenPartEta)
    t.SetBranchAddress ('GenPartPhi', GenPartPhi)
    t.SetBranchAddress ('GenPartMass', GenPartMass)
    entries = t.GetEntriesFast()
    print 'Processing tree ' + str(itree)
    

    if options.maxEvents != None :
        eventsToRun = options.maxEvents
    else :
        eventsToRun = entries
    for jentry in xrange( eventsToRun ):
        if jentry % 10000 == 0 or options.verbose :
            print '======================== processing ' + str(jentry)
        # get the next tree in the chain and verify
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break

        # Speed this up : only look at events with at least two btags
        nbtags = 0
        for bdisc in FatJetBDisc : 
            if bdisc > options.bdisc : 
                nbtags += 1

        if nbtags < 2 : 
            continue
        
        GenJets = []
        FatJets = []
        GenJetsMassSD = []
        FatJetsMassSD = []        
        GenJetsSD = []
        FatJetsSD = []
        GenJets_UDSG = []
        GenJetsSD_UDSG = []
        weight = qcdWeights[itree]

        ThirdGenJet = None
        ThirdGenJetSD = None
        pdfweight_up = NNPDF3weight_CorrUp[0]
        pdfweight_dn = NNPDF3weight_CorrDn[0]
        cteqweight = CTEQweight_Central[0]
        mstwweight = MSTWweight_Central[0]
        #print "pdfweight up: " + str(pdfweight_up)
        #print "pdfweight down: " + str(pdfweight_dn)
        #print 'cteq weight: ' + str(cteqweight)
        #print 'mstw weight: ' + str(mstwweight)


        if deweightFlat != None and deweightFlat :
            weight *= Weight[0]
            if options.verbose :
                print 'Deweighting flat tree, weight = ', weight

            if NGenJet[0] < 3 or 5e-6 < weight/(GenJetPt[0]+GenJetPt[1]):
                if options.verbose : print 'Weight is outside bounds, skipping'
                continue

        bdisccut = options.bdisc
        # First get the generator level jets. If there are at least two,
        # this part is "good". (Changed to three now, with two bjets and one non-b jet)
        ngen = 0
        ngenSD = 0
        #genIDlist = []
        bjetlist = []
        cjetlist = []
        gluonjetlist = []
        bjetlistSD = []
        cjetlistSD = []
        gluonjetlistSD = []


        bquarklist = []
        cquarklist = []
        udsglist = []


        if options.verbose :
            print '--------- Gen Jets -----------'
        for ijet in xrange(  int(NGenJet[0]) ):
            genjet = ROOT.TLorentzVector()
            genjet.SetPtEtaPhiM( GenJetPt[ijet], GenJetEta[ijet], GenJetPhi[ijet], GenJetMass[ijet])
            GenJet = ROOT.TLorentzVector()
            GenJet.SetPtEtaPhiM( GenJetPt[ijet], GenJetEta[ijet], GenJetPhi[ijet], GenJetMass[ijet])
            GenJetSD = ROOT.TLorentzVector()
            GenJetSD.SetPtEtaPhiM( GenJetPtSoftDrop[ijet], GenJetEta[ijet], GenJetPhi[ijet], GenJetMassSoftDrop[ijet] )
            GenJets.append(GenJet)
            GenJetsSD.append(GenJetSD)
            GenJetsMassSD.append( GenJetMassSoftDrop[ijet] )
            if options.verbose :
                print '  ungroomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( ijet, GenJet.Perp(), GenJet.Eta(), GenJet.Phi(), GenJet.M() )
                print '    groomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( ijet, GenJetSD.Perp(), GenJetSD.Eta(), GenJetSD.Phi(), GenJetSD.M() )
            

        genIDlist = []
        for part in xrange( int(NGenPart[0])):
            genIDlist.append( GenPartID[part] )
            for ipart, ipartID in enumerate(genIDlist):
                if GenPartPt[ipart] < 1.0 : 
                    continue
                if abs(ipartID) == 5:
                    BQuark = ROOT.TLorentzVector()
                    BQuark.SetPtEtaPhiM( GenPartPt[ipart], GenPartEta[ipart], GenPartPhi[ipart], GenPartMass[ipart])
                    bquarklist.append(BQuark)
                elif abs(ipartID) == 4:
                    CQuark = ROOT.TLorentzVector()
                    CQuark.SetPtEtaPhiM( GenPartPt[ipart], GenPartEta[ipart], GenPartPhi[ipart], GenPartMass[ipart])
                    cquarklist.append(CQuark)
                else: 
                    udsg = ROOT.TLorentzVector()
                    udsg.SetPtEtaPhiM( GenPartPt[ipart], GenPartEta[ipart], GenPartPhi[ipart], GenPartMass[ipart])
                    udsglist.append(udsg)

        #if options.verbose:
        #    print 'bquarks : ' 
        #    for bquark in bquarklist: 
        #        print '  %6.2f %4.3f %4.3f %6.2f' % ( bquark.Perp(), bquark.Eta(), bquark.Phi(), bquark.M() )


        for ijet,genjet in enumerate(GenJets):
            bindex = getMatched(genjet, bquarklist )
            cindex = getMatched(genjet, cquarklist)
            if bindex != None:
                bjetlist.append(ijet)
            elif cindex  != None:
                cjetlist.append(ijet)
            else:
                GenJets_UDSG.append( genjet )
                gluonjetlist.append(ijet)

        for ijet,genjet in enumerate(GenJetsSD):
            bindex = getMatched(genjet, bquarklist )
            cindex = getMatched(genjet, cquarklist)
            if bindex != None:
                bjetlistSD.append(ijet)
            elif cindex  != None:
                cjetlistSD.append(ijet)
            else:
                GenJetsSD_UDSG.append( genjet )
                gluonjetlistSD.append(ijet)

        if options.verbose: 
            print 'bjets : ', len(bjetlist)
            print 'gjets : ', len(gluonjetlist)
        if len(bjetlist) >= 2 and len(gluonjetlist) >= 1:
            ThirdGenJet = gluonjetlist[0]
            if GenJetPt[ThirdGenJet] > 0. :
                h_2DHisto_gen.Fill( GenJets[ThirdGenJet].M(), GenJets[ThirdGenJet].Perp(), weight )

        if ThirdGenJet != None : 
            if len(bjetlistSD) >= 2 and len(gluonjetlistSD) >= 1:
                ThirdGenJetSD = gluonjetlistSD[0]
                if GenJetPtSoftDrop[ThirdGenJetSD] > 0. :
                    h_2DHisto_genSD.Fill( GenJetsSD[ThirdGenJetSD].M(), GenJets[ThirdGenJet].Perp(), weight)

        if options.verbose:
            print 'UDSG Jets:'
            for ijet,GenJet in enumerate(GenJets_UDSG) :
                GenJetSD = GenJetsSD_UDSG[ijet]
                print '  ungroomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( ijet, GenJet.Perp(), GenJet.Eta(), GenJet.Phi(), GenJet.M() )
                print '    groomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( ijet, GenJetSD.Perp(), GenJetSD.Eta(), GenJetSD.Phi(), GenJetSD.M() )
                


                
        # Next get the reco level jets. If there are at least two
        # AND at least two gen jets, then we can "fill".
        # If there are fewer than two gen jets, it is a "fake".
        #passkinloose = False   # Does it have two jets that pass the ptasym and dphi cuts?
        passkinfull = False    # Do the 2 jets pass the pt cuts?
        passkinfullsoftdrop = False  # Do the 2 groomed jets pass the pt cuts?


        if options.verbose : print '---------- Reco Jets-----------'

        bdisctuple = [] # Store the indices of the jets sorted by b discriminator.

        Bjet1 = None
        Bjet2 = None
        ThirdJet = None
        
        for ijet in xrange(NFatJet[0]):
            bdisctuple.append( [ijet, FatJetBDisc[ijet] ] )
            if options.verbose :
                print '  ungroomed  %6d : pt,eta,phi,m,bdisc = %6.2f, %8.3f, %8.3f, %6.2f, %6.2f, ' % ( ijet, FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet], FatJetBDisc[ijet] )
                print '    groomed  %6d : pt,eta,phi,m,bdisc = %6.2f, %8.3f, %8.3f, %6.2f, %6.2f, ' % ( ijet, FatJetPtSoftDrop[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMassSoftDrop[ijet], FatJetBDisc[ijet] )
        if NFatJet[0] >= 3 :
            bdiscsorted = sorted(bdisctuple, key=lambda bdiscsort : bdiscsort[1], reverse=True )
            if options.verbose :
                print bdiscsorted
            if (bdiscsorted[0][1] >= bdisccut and bdiscsorted[1][1] >= bdisccut):
                ThirdJet = bdiscsorted[2][0]
                Bjet1 = bdiscsorted[0][0]
                Bjet2 = bdiscsorted[1][0]
            if options.verbose :
                print 'Sorted by bdisc:'
                print bdiscsorted
                print ', third jet = ', ThirdJet

            if ThirdJet == None :
                if options.verbose : 
                    print 'No third jet!'
                continue

            passkinfull = FatJetPt[ThirdJet] > options.ptMin
            passkinfullsoftdrop = passkinfull #and FatJetPtSoftDrop[maxjet] > options.ptMin and FatJetPtSoftDrop[minjet] > options.ptMin #and FatJetPtSoftDrop[maxjet] <= FatJetPt[maxjet] and FatJetPtSoftDrop[minjet] <= FatJetPt[minjet]


            # First get the "Fills" and "Fakes" (i.e. we at least have a RECO jet)
            for ijet in [ThirdJet]:
                if not ( passkinfull ) :
                    if options.verbose : print 'Skipping ungroomed jet, kin loose or kin full failed'                    
                    continue 
                FatJet = ROOT.TLorentzVector()
                FatJet.SetPtEtaPhiM( FatJetPt[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMass[ijet])
                FatJets.append(FatJet)
                igen = getMatched( FatJet, GenJets_UDSG )            

                if options.verbose : 
                    print 'Found igen!'
                    print igen
                    print 'ngen = ', ngen

                h_2DHisto_meas.Fill( FatJet.M(), FatJet.Perp(),  weight )
                if igen != None :  # Here we have a "Fill"
                    if options.verbose : 
                        print ' reco   %6d --> gen   %6d' % ( ijet, igen )


                    valup = getJER(FatJet.Eta(), +1) #JER nominal=0, up=+1, down=-1
                    recopt = FatJet.Perp()
                    genpt = GenJets_UDSG[igen].Perp()
                    deltapt = (recopt-genpt)*(valup-1.0)
                    if abs(recopt) > 0.0 : smearup = max(0.0, (recopt+deltapt)/recopt)
                    else : smearup = 0.0

                    valdn = getJER(FatJet.Eta(), -1) #JER nominal=0, dn=+1, down=-1
                    recopt = FatJet.Perp()
                    genpt = GenJets_UDSG[igen].Perp()
                    deltapt = (recopt-genpt)*(valdn-1.0)
                    if abs(recopt) > 0.0 : smeardn = max(0.0, (recopt+deltapt)/recopt)
                    else : smeardn = 0.0

                    valnom = getJER(FatJet.Eta(), 0)
                    recopt = FatJet.Perp()
                    genpt = GenJets_UDSG[igen].Perp()
                    deltapt = (recopt-genpt)*(valnom-1.0)
                    if abs(recopt) > 0.0 : smearnom = max(0.0, (recopt+deltapt)/recopt)
                    else : smearnom = 0.

                    jmrvalup = 1.2
                    recomass = FatJet.M()
                    genmass = GenJets_UDSG[igen].M()
                    deltamass = (recomass-genmass)*(jmrvalup-1.0)
                    if abs(recomass) > 0.0 : jmrup = max(0.0, (recomass+deltamass)/recomass)
                    else : jmrup = 0.

                    jmrvaldn = 1.0
                    recomass = FatJet.M()
                    genmass = GenJets_UDSG[igen].M()
                    deltamass = (recomass-genmass)*(jmrvaldn-1.0)
                    if abs(recomass) > 0.0 : jmrdn = max(0.0, (recomass+deltamass)/recomass)
                    else : jmrdn = 0.

                    jmrvalnom = 1.1
                    recomass = FatJet.M()
                    genmass = GenJets_UDSG[igen].M()
                    deltamass = (recomass-genmass)*(jmrvalnom-1.0)
                    if abs(recomass) > 0.0 : jmrnom = max(0.0, (recomass+deltamass)/recomass)
                    else : jmrnom = 0.

                    h_2DHisto_nomnom_meas.Fill( FatJet.M()*jmrnom*smearnom, FatJet.Perp()*smearnom,  weight )
                    

                    if options.verbose :
                        print '     smearnom,jmrnom = %6.3f, %6.3f', smearnom, jmrnom

                    response.Fill( FatJet.M(), FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_jecup.Fill( FatJet.M() * FatJetCorrUp[ijet], FatJet.Perp()* FatJetCorrUp[ijet], GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_jecdn.Fill( FatJet.M() * FatJetCorrDn[ijet], FatJet.Perp()* FatJetCorrDn[ijet], GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_jerup.Fill( FatJet.M() * smearup, FatJet.Perp()* smearup, GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_jerdn.Fill( FatJet.M() * smeardn, FatJet.Perp()* smeardn, GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_jernom.Fill(FatJet.M() * smearnom, FatJet.Perp()*smearnom, GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)

                    response_jmrup.Fill( FatJet.M()*jmrup , FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_jmrdn.Fill( FatJet.M()*jmrdn , FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_jmrnom.Fill(FatJet.M()*jmrnom, FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)

                    response_nomnom.Fill(FatJet.M()*jmrnom*smearnom, FatJet.Perp()*smearnom, GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)

                    h_massup.Fill(FatJet.M()*jmrup, weight)
                    h_massdn.Fill(FatJet.M()*jmrdn, weight)
                    h_massnom.Fill(FatJet.M()*jmrnom, weight)

                    h2_massup.Fill(FatJet.Perp(), FatJet.M()*jmrup, weight)
                    h2_massdn.Fill(FatJet.Perp(), FatJet.M()*jmrdn, weight)
                    h2_massnom.Fill(FatJet.Perp(), FatJet.M()*jmrnom, weight)


                    if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                        pass
                    else:
                        response_pdfup.Fill( FatJet.M(), FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_up)
                        response_pdfdn.Fill( FatJet.M(), FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_dn)

                    if cteqweight > 1.2 or cteqweight < 0.8:
                        pass
                    else:
                        response_cteq.Fill( FatJet.M(), FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*cteqweight)

                    if mstwweight > 1.2 or mstwweight < 0.8:
                        pass
                    else:
                        response_mstw.Fill( FatJet.M(), FatJet.Perp(), GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*mstwweight)


                    # Make some data-to-MC plots

                    #                h_2DHisto_meas.Fill( FatJetPt[ijet], FatJetMass[ijet], weight )


                    h_pt_meas.Fill( FatJetPt[ijet] , weight )
                    h_y_meas.Fill( FatJetRap[ijet] , weight )
                    h_phi_meas.Fill( FatJetPhi[ijet] , weight )
                    h_m_meas.Fill( FatJetMass[ijet] , weight )
                    h_rho_meas.Fill( FatJetRhoRatio[ijet] , weight )
                    h_tau21_meas.Fill( FatJetTau21[ijet] , weight )
                    h_rho_vs_tau_meas.Fill( FatJetRhoRatio[ijet], FatJetTau21[ijet] , weight )
                    if GenJets_UDSG[igen].M() != 0:
                        h_mreco_mgen.Fill(FatJet.M()/GenJets_UDSG[igen].M(), weight)
                        h_mreco_mgen_nomnom.Fill(FatJet.M() * smearnom * jmrnom/GenJets_UDSG[igen].M(), weight)
                    else:
                        h_mreco_mgen.Fill(FatJet.M() * smearnom * jmrnom/0.140, weight)
                    h_ptreco_ptgen.Fill(FatJet.Perp()/GenJets_UDSG[igen].Perp(), weight)
                    h_ptreco_ptgen.Fill(FatJet.Perp() * smearnom /GenJets_UDSG[igen].Perp(), weight)        


                    h2_y_meas.Fill( FatJet.Perp(), FatJetRap[ijet] , weight )
                    h2_phi_meas.Fill( FatJet.Perp(), FatJetPhi[ijet] , weight )
                    h2_m_meas.Fill( FatJet.Perp(), FatJetMass[ijet] , weight )
                    h2_msd_meas.Fill( FatJet.Perp(), FatJetMassSoftDrop[ijet] , weight )
                    h2_rho_meas.Fill( FatJet.Perp(), FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas.Fill( FatJet.Perp(), FatJetTau21[ijet] , weight )
                    if GenJets_UDSG[igen].M() != 0:
                        h2_mreco_mgen.Fill(GenJets_UDSG[igen].Perp(), FatJet.M()/GenJets_UDSG[igen].M(), weight)
                        h2_mreco_mgen_nomnom.Fill(GenJets_UDSG[igen].Perp(), FatJet.M() * smearnom * jmrnom/GenJets_UDSG[igen].M(), weight)
                    else:
                        h2_mreco_mgen.Fill(GenJets_UDSG[igen].Perp(), FatJet.M()/0.140, weight)
                        h2_mreco_mgen_nomnom.Fill(GenJets_UDSG[igen].Perp()* smearnom * jmrnom, FatJet.M()/0.140, weight)
                    h2_ptreco_ptgen.Fill(FatJet.Perp(), FatJet.Perp()/GenJets_UDSG[igen].Perp(), weight)
                    h2_ptreco_ptgen_nomnom.Fill(FatJet.Perp(), FatJet.Perp() * smearnom/GenJets_UDSG[igen].Perp(), weight)


                    h2_y_meas_sys    [jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetMassSoftDrop[ijet] * FatJetCorrUp[ijet], weight )
                    h2_rho_meas_sys  [jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jecup_ndx].Fill( FatJet.Perp() * FatJetCorrUp[ijet], FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jecup_ndx].Fill( FatJet.M(), FatJet.Perp()* FatJetCorrUp[ijet],  weight )
                    h_2DHisto_meas_sys[jecup_ndx].Fill( FatJet.M(), FatJet.Perp()* FatJetCorrUp[ijet],  weight )
                    h_2DHisto_measSD_sys[jecup_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp()* FatJetCorrUp[ijet],  weight)
                    
                    h2_y_meas_sys    [jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetMassSoftDrop[ijet] * FatJetCorrDn[ijet], weight )
                    h2_rho_meas_sys  [jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jecdn_ndx].Fill( FatJet.Perp() * FatJetCorrDn[ijet], FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jecdn_ndx].Fill( FatJet.M(), FatJet.Perp()* FatJetCorrDn[ijet],  weight )
                    h_2DHisto_measSD_sys[jecdn_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp()* FatJetCorrDn[ijet],  weight)

                    h2_y_meas_sys    [jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetMassSoftDrop[ijet] * smearup, weight )
                    h2_rho_meas_sys  [jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jerup_ndx].Fill( FatJet.Perp() * smearup, FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jerup_ndx].Fill( FatJet.M()* smearup, FatJet.Perp()* smearup,  weight )
                    h_2DHisto_measSD_sys[jerup_ndx].Fill( FatJetMassSoftDrop[ijet]*smearup, FatJet.Perp()* smearup,  weight)

                    h2_y_meas_sys    [jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetMassSoftDrop[ijet] * smeardn, weight )
                    h2_rho_meas_sys  [jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jerdn_ndx].Fill( FatJet.Perp() * smeardn, FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jerdn_ndx].Fill( FatJet.M()* smeardn, FatJet.Perp()* smeardn,  weight )
                    h_2DHisto_measSD_sys[jerdn_ndx].Fill( FatJetMassSoftDrop[ijet]*smeardn, FatJet.Perp()* smeardn,  weight)

                    h2_y_meas_sys    [jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetMassSoftDrop[ijet] * jmrup, weight )
                    h2_rho_meas_sys  [jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jmrup_ndx].Fill( FatJet.Perp() * jmrup, FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jmrup_ndx].Fill( FatJet.M()* jmrup, FatJet.Perp()* jmrup,  weight )
                    h_2DHisto_measSD_sys[jmrup_ndx].Fill( FatJetMassSoftDrop[ijet]*jmrup, FatJet.Perp(),  weight)

                    h2_y_meas_sys    [jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetRap[ijet] , weight )
                    h2_phi_meas_sys  [jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetPhi[ijet] , weight )
                    h2_m_meas_sys    [jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetMass[ijet] , weight )
                    h2_msd_meas_sys  [jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetMassSoftDrop[ijet] * jmrdn, weight )
                    h2_rho_meas_sys  [jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetRhoRatio[ijet] , weight )
                    h2_tau21_meas_sys[jmrdn_ndx].Fill( FatJet.Perp() * jmrdn, FatJetTau21[ijet] , weight )
                    h_2DHisto_meas_sys[jmrdn_ndx].Fill( FatJet.M()* jmrdn, FatJet.Perp()* jmrdn,  weight )
                    h_2DHisto_measSD_sys[jmrdn_ndx].Fill( FatJetMassSoftDrop[ijet]*jmrdn, FatJet.Perp(),  weight)

                    h2_y_meas_sys    [pdfup_ndx].Fill( FatJet.Perp(), FatJetRap[ijet] , weight*pdfweight_up )
                    h2_phi_meas_sys  [pdfup_ndx].Fill( FatJet.Perp(), FatJetPhi[ijet] , weight*pdfweight_up )
                    h2_m_meas_sys    [pdfup_ndx].Fill( FatJet.Perp(), FatJetMass[ijet] , weight*pdfweight_up )
                    h2_msd_meas_sys  [pdfup_ndx].Fill( FatJet.Perp(), FatJetMassSoftDrop[ijet], weight*pdfweight_up )
                    h2_rho_meas_sys  [pdfup_ndx].Fill( FatJet.Perp(), FatJetRhoRatio[ijet] , weight*pdfweight_up )
                    h2_tau21_meas_sys[pdfup_ndx].Fill( FatJet.Perp(), FatJetTau21[ijet] , weight*pdfweight_up )
                    h_2DHisto_meas_sys[pdfup_ndx].Fill( FatJet.M(), FatJet.Perp(),  weight*pdfweight_up )
                    h_2DHisto_measSD_sys[pdfup_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp(),  weight*pdfweight_up)

                    h2_y_meas_sys    [pdfdn_ndx].Fill( FatJet.Perp(), FatJetRap[ijet] , weight*pdfweight_dn )
                    h2_phi_meas_sys  [pdfdn_ndx].Fill( FatJet.Perp(), FatJetPhi[ijet] , weight*pdfweight_dn )
                    h2_m_meas_sys    [pdfdn_ndx].Fill( FatJet.Perp(), FatJetMass[ijet] , weight*pdfweight_dn )
                    h2_msd_meas_sys  [pdfdn_ndx].Fill( FatJet.Perp(), FatJetMassSoftDrop[ijet], weight*pdfweight_dn )
                    h2_rho_meas_sys  [pdfdn_ndx].Fill( FatJet.Perp(), FatJetRhoRatio[ijet] , weight*pdfweight_dn )
                    h2_tau21_meas_sys[pdfdn_ndx].Fill( FatJet.Perp(), FatJetTau21[ijet] , weight*pdfweight_dn )
                    h_2DHisto_meas_sys[pdfdn_ndx].Fill( FatJet.M(), FatJet.Perp(),  weight*pdfweight_dn )
                    h_2DHisto_measSD_sys[pdfdn_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp(),  weight*pdfweight_dn)

                    h2_y_meas_sys    [cteq_ndx].Fill( FatJet.Perp(), FatJetRap[ijet] , weight*cteqweight )
                    h2_phi_meas_sys  [cteq_ndx].Fill( FatJet.Perp(), FatJetPhi[ijet] , weight*cteqweight )
                    h2_m_meas_sys    [cteq_ndx].Fill( FatJet.Perp(), FatJetMass[ijet] , weight*cteqweight )
                    h2_msd_meas_sys  [cteq_ndx].Fill( FatJet.Perp(), FatJetMassSoftDrop[ijet], weight*cteqweight )
                    h2_rho_meas_sys  [cteq_ndx].Fill( FatJet.Perp(), FatJetRhoRatio[ijet] , weight*cteqweight )
                    h2_tau21_meas_sys[cteq_ndx].Fill( FatJet.Perp(), FatJetTau21[ijet] , weight*cteqweight )
                    h_2DHisto_meas_sys[cteq_ndx].Fill( FatJet.M(), FatJet.Perp(),  weight*cteqweight )
                    h_2DHisto_measSD_sys[cteq_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp(),  weight*cteqweight)

                    h2_y_meas_sys    [mstw_ndx].Fill( FatJet.Perp(), FatJetRap[ijet] , weight*mstwweight )
                    h2_phi_meas_sys  [mstw_ndx].Fill( FatJet.Perp(), FatJetPhi[ijet] , weight*mstwweight )
                    h2_m_meas_sys    [mstw_ndx].Fill( FatJet.Perp(), FatJetMass[ijet] , weight*mstwweight )
                    h2_msd_meas_sys  [mstw_ndx].Fill( FatJet.Perp(), FatJetMassSoftDrop[ijet], weight*mstwweight )
                    h2_rho_meas_sys  [mstw_ndx].Fill( FatJet.Perp(), FatJetRhoRatio[ijet] , weight*mstwweight )
                    h2_tau21_meas_sys[mstw_ndx].Fill( FatJet.Perp(), FatJetTau21[ijet] , weight*mstwweight )
                    h_2DHisto_meas_sys[mstw_ndx].Fill( FatJet.M(), FatJet.Perp(),  weight*mstwweight )
                    h_2DHisto_measSD_sys[mstw_ndx].Fill( FatJetMassSoftDrop[ijet], FatJet.Perp(),  weight*mstwweight)

                    
                                        
                                        
                else : # Here we have a "Fake", i.e. fewer than 2 gen jets matched to 2 reco jets

                    if options.verbose : print 'Fake ungroomed jet'                    
                    response.Fake( FatJet.M(), FatJet.Perp(), weight )
                    response_jecup.Fake( FatJet.M() * FatJetCorrUp[ijet], FatJet.Perp()* FatJetCorrUp[ijet], weight )
                    response_jecdn.Fake( FatJet.M() * FatJetCorrDn[ijet], FatJet.Perp()* FatJetCorrDn[ijet], weight )
                    response_jerup.Fake( FatJet.M(), FatJet.Perp(), weight )
                    response_jerdn.Fake( FatJet.M(), FatJet.Perp(), weight ) 
                    response_jernom.Fake(FatJet.M(), FatJet.Perp(),weight)
                    response_jmrup.Fake( FatJet.M(), FatJet.Perp(), weight)
                    response_jmrdn.Fake( FatJet.M(), FatJet.Perp(), weight)
                    response_jmrnom.Fake(FatJet.M(), FatJet.Perp(), weight)
                    response_nomnom.Fake(FatJet.M(), FatJet.Perp(), weight)

                    if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                        pass
                    else:
                        response_pdfup.Fake(FatJet.M(), FatJet.Perp(), weight*pdfweight_up)
                        response_pdfdn.Fake(FatJet.M(), FatJet.Perp(), weight*pdfweight_dn)

                    if cteqweight > 1.2 or cteqweight < 0.8:
                        pass
                    else:
                        response_cteq.Fake( FatJet.M(), FatJet.Perp(), weight*cteqweight)

                    if mstwweight > 1.2 or mstwweight < 0.8:
                        pass
                    else:
                        response_mstw.Fake( FatJet.M(), FatJet.Perp(), weight*mstwweight)


            # Now get the "Fills" and "Fakes" for soft drop (i.e. we at least have a RECO jet)
            for ijet in [ThirdJet]:
                if not ( passkinfullsoftdrop ) :
                    if options.verbose : print 'Skipping soft drop jet, kin loose or kin full failed'                    
                    continue 

                FatJetSD = ROOT.TLorentzVector()
                FatJetSD.SetPtEtaPhiM( FatJetPtSoftDrop[ijet], FatJetEta[ijet], FatJetPhi[ijet], FatJetMassSoftDrop[ijet]  )            
                FatJetsSD.append(FatJetSD)
                igenSD = getMatched(FatJetSD, GenJetsSD_UDSG, dRMax=0.3)
                igen = getMatched(FatJetSD, GenJets_UDSG, dRMax=0.3)


                h_2DHisto_measSD.Fill( FatJetSD.M(), FatJetPt[ijet],  weight)
                if  igenSD != None and igen != None  :
                    if options.verbose : 
                        print ' recoSD %6d --> genSD %6d' % ( ijet, igenSD )

                    #### be less conservative, define jes and jer for SD now
                    valupSD = getJER(FatJetSD.Eta(), +1)
                    recoptSD = FatJetPt[ijet]
                    genptSD = GenJets_UDSG[igen].Perp()
                    deltaptSD = (recoptSD-genptSD)*(valupSD-1.0)
                    if abs(recoptSD) > 0.0 : smearupSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)
                    else : smearupSD = 0.

                    valdnSD = getJER(FatJetSD.Eta(), -1)
                    recoptSD = FatJetPt[ijet]
                    genptSD = GenJets_UDSG[igen].Perp()
                    deltaptSD = (recoptSD-genptSD)*(valdnSD-1.0)
                    if abs(recoptSD) > 0.0 : smeardnSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)
                    else : smeardnSD = 0.

                    valnomSD = getJER(FatJetSD.Eta(), 0)
                    recoptSD = FatJetPt[ijet]
                    genptSD = GenJets_UDSG[igen].Perp()
                    deltaptSD = (recoptSD-genptSD)*(valnomSD-1.0)
                    if abs(recoptSD) > 0.0 : smearnomSD = max(0.0, (recoptSD+deltaptSD)/recoptSD)
                    else : smearnomSD = 0.

                    jmrvalnomSD = 1.1
                    recomassSD = FatJetSD.M()
                    genmassSD = GenJetsSD_UDSG[igenSD].M()
                    deltamassSD = (recomassSD-genmassSD)*(jmrvalnomSD-1.0)
                    if abs(recomassSD) > 0.0 : jmrnomSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)
                    else : jmrnomSD = 0.

                    jmrvalupSD = 1.2
                    recomassSD = FatJetSD.M()
                    genmassSD = GenJetsSD_UDSG[igenSD].M()
                    deltamassSD = (recomassSD-genmassSD)*(jmrvalupSD-1.0)
                    if abs(recomassSD) > 0.0 : jmrupSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)
                    else : jmrupSD = 0.

                    jmrvaldnSD = 1.0
                    recomassSD = FatJetSD.M()
                    genmassSD = GenJetsSD_UDSG[igenSD].M()
                    deltamassSD = (recomassSD-genmassSD)*(jmrvaldnSD-1.0)
                    if abs(recomassSD) > 0.0 : jmrdnSD = max(0.0, (recomassSD+deltamassSD)/recomassSD)
                    else : jmrdnSD = 0.

                    if options.verbose :
                        print '     smearnom,jmrnom = %6.3f, %6.3f', smearnomSD, jmrnomSD
                        

                    h_2DHisto_nomnom_measSD.Fill( FatJetSD.M()*jmrnomSD*smearnomSD, FatJetPt[ijet]*smearnomSD,  weight)
                    response_softdrop.Fill( FatJetSD.M() , FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_softdrop_jecup.Fill( FatJetSD.M()  * FatJetCorrUp[ijet], FatJetPt[ijet] * FatJetCorrUp[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_softdrop_jecdn.Fill( FatJetSD.M()  * FatJetCorrDn[ijet], FatJetPt[ijet] * FatJetCorrDn[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_softdrop_jerup.Fill( FatJetSD.M()  * smearupSD, FatJetPt[ijet] * smearupSD, GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_softdrop_jerdn.Fill( FatJetSD.M()  * smeardnSD, FatJetPt[ijet] * smeardnSD, GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                    response_softdrop_jernom.Fill(FatJetSD.M() * smearnomSD, FatJetPt[ijet] * smearnomSD, GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_softdrop_jmrnom.Fill(FatJetSD.M()*jmrnomSD, FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_softdrop_jmrup.Fill(FatJetSD.M() *jmrupSD , FatJetPt[ijet] , GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_softdrop_jmrdn.Fill(FatJetSD.M() *jmrdnSD , FatJetPt[ijet] , GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                    response_softdrop_nomnom.Fill(FatJetSD.M()*jmrnomSD*smearnomSD, FatJetPt[ijet]*smearnomSD, GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)

                    h_massup_softdrop.Fill(FatJetSD.M()*jmrupSD, weight)
                    h_massdn_softdrop.Fill(FatJetSD.M()*jmrdnSD, weight)
                    h_massnom_softdrop.Fill(FatJetSD.M()*jmrnomSD, weight)
                    if GenJetsSD_UDSG[igenSD].M() != 0:
                        h_mreco_mgen_softdrop.Fill(FatJetSD.M()/GenJetsSD_UDSG[igenSD].M(), weight)
                        h2_mreco_mgen_softdrop.Fill(GenJets_UDSG[igen].Perp(), FatJetSD.M()/GenJetsSD_UDSG[igenSD].M(), weight)
                        h_mreco_mgen_softdrop_nomnom.Fill(FatJetSD.M() *jmrnomSD*smearnomSD /GenJetsSD_UDSG[igenSD].M(), weight)
                        h2_mreco_mgen_softdrop_nomnom.Fill(GenJets_UDSG[igen].Perp(), FatJetSD.M()*jmrnomSD*smearnomSD/GenJetsSD_UDSG[igenSD].M(), weight)
                    else:
                        h_mreco_mgen_softdrop.Fill(FatJetSD.M()/0.14, weight)
                        h2_mreco_mgen_softdrop.Fill(GenJets_UDSG[igen].Perp(), FatJetSD.M()/0.140, weight)
                        h_mreco_mgen_softdrop_nomnom.Fill(FatJetSD.M() *jmrnomSD*smearnomSD/0.14, weight)
                        h2_mreco_mgen_softdrop_nomnom.Fill(GenJets_UDSG[igen].Perp(), FatJetSD.M() *jmrnomSD*smearnomSD/0.140, weight)
                        masslessSD += 1
                    h_ptreco_ptgen_softdrop.Fill(FatJetPt[ijet]/GenJets_UDSG[igen].Perp(), weight)
                    h2_ptreco_ptgen_softdrop.Fill(GenJets_UDSG[igen].Perp(), FatJetPt[ijet]/GenJets_UDSG[igen].Perp(), weight)
                    h_ptreco_ptgen_softdrop.Fill(FatJetPt[ijet]*smearnomSD/GenJets_UDSG[igen].Perp(), weight)
                    h2_ptreco_ptgen_softdrop.Fill(GenJets_UDSG[igen].Perp(), FatJetPt[ijet]*smearnomSD/GenJets_UDSG[igen].Perp(), weight)

                    if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                        pass
                    else:
                        response_softdrop_pdfup.Fill( FatJetSD.M(), FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_up)
                        response_softdrop_pdfdn.Fill( FatJetSD.M(), FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_dn)


                    if cteqweight > 1.2 or cteqweight < 0.8:
                        pass
                    else:
                        response_softdrop_cteq.Fill( FatJetSD.M(), FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*cteqweight)

                    if mstwweight > 1.2 or mstwweight < 0.8:
                        pass
                    else:
                        response_softdrop_mstw.Fill( FatJetSD.M(), FatJetPt[ijet], GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*mstwweight)

                        

                    if ( FatJetPt[ijet] > 1300. and FatJetSD.M() > 800 and GenJetsSD_UDSG[igenSD].M() < 500 ) or (igen != igenSD) :
                    #if ( FatJetPt[ijet]/GenJetPt[igenSD] > 1.1 ) :

                        if igen != igenSD :
                            print '#'
                            print '#'
                            print '#==========> This is very, very wrong <============'
                            print '#'
                            print '#'
                        
                        print '<<<<<<<<<<<<<<<< Something screwy >>>>>>>>>>>>>>>>'
                        print 'ijet = ', ijet, ' igenSD = ', igenSD
                        print '--------- Gen Jets -----------'
                        for igenDebug in xrange( len(GenJets) ):
                                print '  ungroomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( igenDebug, GenJets[igenDebug].Perp(), GenJets[igenDebug].Eta(), GenJets[igenDebug].Phi(), GenJets[igenDebug].M() )
                        for igenDebug in xrange( len(GenJetsSD_UDSG) ):
                                print '    groomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f' % ( igenDebug, GenJetsSD_UDSG[igenDebug].Perp(), GenJetsSD_UDSG[igenDebug].Eta(), GenJetsSD_UDSG[igenDebug].Phi(), GenJetsSD_UDSG[igenDebug].M() )

                        print '---------- Reco Jets-----------'
                        for ijetDebug in xrange( NFatJet[0] ) : 
                            print '  ungroomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f, ' % ( ijetDebug, FatJetPt[ijetDebug], FatJetEta[ijetDebug], FatJetPhi[ijetDebug], FatJetMass[ijetDebug] )
                        for ijetDebug in xrange( NFatJet[0] ) : 
                            print '    groomed  %6d : pt,eta,phi,m = %6.2f, %8.3f, %8.3f, %6.2f, ' % ( ijetDebug, FatJetPtSoftDrop[ijetDebug], FatJetEta[ijetDebug], FatJetPhi[ijetDebug], FatJetMassSoftDrop[ijetDebug] )


                        

                        

                    h_msd_meas.Fill( FatJetMassSoftDrop[ijet] , weight )
     #               h_2DHisto_measSD.Fill( FatJetPt[ijet], FatJetMassSoftDrop[ijet], weight )
                else:
                    if options.verbose : print 'Fake groomed jet'
                    h_2DHisto_nomnom_measSD.Fill( FatJetSD.M(), FatJetPt[ijet],  weight)
                    response_softdrop.Fake( FatJetSD.M() , FatJetPt[ijet], weight )
                    response_softdrop_jecup.Fake( FatJetSD.M()  * FatJetCorrUp[ijet], FatJetPt[ijet] * FatJetCorrUp[ijet], weight )
                    response_softdrop_jecdn.Fake( FatJetSD.M()  * FatJetCorrDn[ijet], FatJetPt[ijet] * FatJetCorrDn[ijet], weight )
                    response_softdrop_jerup.Fake( FatJetSD.M(), FatJetPt[ijet], weight )
                    response_softdrop_jerdn.Fake( FatJetSD.M(), FatJetPt[ijet], weight )
                    response_softdrop_jernom.Fake(FatJetSD.M(), FatJetPt[ijet], weight)            
                    response_softdrop_jmrnom.Fake(FatJetSD.M(), FatJetPt[ijet], weight)
                    response_softdrop_jmrup.Fake(FatJetSD.M() , FatJetPt[ijet] , weight)
                    response_softdrop_jmrdn.Fake(FatJetSD.M() , FatJetPt[ijet] , weight)
                    response_softdrop_nomnom.Fake(FatJetSD.M(), FatJetPt[ijet], weight)
                    if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                        pass
                    else:
                        response_softdrop_pdfup.Fake( FatJetSD.M(), FatJetPt[ijet], weight*pdfweight_up)
                        response_softdrop_pdfdn.Fake( FatJetSD.M(), FatJetPt[ijet], weight*pdfweight_dn)


                    if cteqweight > 1.2 or cteqweight < 0.8:
                        pass
                    else:
                        response_softdrop_cteq.Fake( FatJetSD.M(), FatJetPt[ijet], weight*cteqweight)

                    if mstwweight > 1.2 or mstwweight < 0.8:
                        pass
                    else:
                        response_softdrop_mstw.Fake( FatJetSD.M(), FatJetPt[ijet], weight*mstwweight)


        if ngen >= 3 and len(GenJets_UDSG) > 0 and not ( passkinfull ) :
            # Now get the "Misses" (i.e. we have no RECO jet)
            for igen in xrange( 0 ):
                if options.verbose :
                    print 'Missed ungroomed gen jet: ', igen
                response.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                response_jecup.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                response_jecdn.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                response_jerup.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                response_jerdn.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight )
                response_jernom.Miss(GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                response_jmrnom.Miss(GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                response_jmrup.Miss(GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                response_jmrdn.Miss(GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                response_nomnom.Miss(GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_pdfup.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_up)
                    response_pdfdn.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_dn)


                if cteqweight > 1.2 or cteqweight < 0.8:
                    pass
                else:
                    response_cteq.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*cteqweight)

                if mstwweight > 1.2 or mstwweight < 0.8:
                    pass
                else:
                    response_mstw.Miss( GenJets_UDSG[igen].M(), GenJets_UDSG[igen].Perp(), weight*mstwweight)


        if ngen >= 3 and ngenSD >= 3 and len(GenJetsSD_UDSG) > 0 and not ( passkinfullsoftdrop ):
            # Now get the "Misses" (i.e. we have no RECO jet)
            for igenSD in xrange( 0 ):
                igen = getMatched( GenJetsSD_UDSG[igenSD], GenJets, dRMax=0.3 )
                if options.verbose :
                    print 'Missed   groomed gen jet: ', igenSD
                response_softdrop.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jecup.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jecdn.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jerup.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jerdn.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jernom.Miss(GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight )
                response_softdrop_jmrnom.Miss(GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                response_softdrop_jmrup.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                response_softdrop_jmrdn.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                response_softdrop_nomnom.Miss(GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight)
                if pdfweight_up > 1.2 or pdfweight_dn < 0.8:
                    pass
                else:
                    response_softdrop_pdfup.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_up)
                    response_softdrop_pdfdn.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*pdfweight_dn)

                if cteqweight > 1.2 or cteqweight < 0.8:
                    pass
                else:
                    response_softdrop_cteq.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*cteqweight)

                if mstwweight > 1.2 or mstwweight < 0.8:
                    pass
                else:
                    response_softdrop_mstw.Miss( GenJetsSD_UDSG[igenSD].M(), GenJets_UDSG[igen].Perp(), weight*mstwweight)


                    
print "Number of Massless Softdrop Jets: " + str(masslessSD)
fout.cd()
#response.Hresponse().Draw()
response.Write()
response_jecup.Write()
response_jecdn.Write()
response_jerup.Write()
response_jerdn.Write()
h_2DHisto_gen.Write()
h_2DHisto_meas.Write()
response_jmrup.Write()
response_jmrdn.Write()
response_jmrnom.Write()
response_jernom.Write()
response_nomnom.Write()

response_pdfup.Write()
response_pdfdn.Write()
response_softdrop_pdfup.Write()
response_softdrop_pdfdn.Write()

response_cteq.Write()
response_softdrop_cteq.Write()

response_mstw.Write()
response_softdrop_mstw.Write()

h_mreco_mgen.Write()
h_ptreco_ptgen.Write()
h_mreco_mgen_softdrop.Write()
h_ptreco_ptgen_softdrop.Write()

h_mreco_mgen_nomnom.Write()
h_ptreco_ptgen_nomnom.Write()
h_mreco_mgen_softdrop_nomnom.Write()
h_ptreco_ptgen_softdrop_nomnom.Write()

h_2DHisto_measSD.Write()
h_2DHisto_genSD.Write()
h_2DHisto_nomnom_measSD.Write()
h_2DHisto_nomnom_genSD.Write()

response_softdrop.Write()
response_softdrop_jecup.Write()
response_softdrop_jecdn.Write()
response_softdrop_jerup.Write()
response_softdrop_jerdn.Write()
response_softdrop_jmrup.Write()
response_softdrop_jmrdn.Write()
response_softdrop_jmrnom.Write()
response_softdrop_jernom.Write()
response_softdrop_nomnom.Write()
h_pt_meas.Write()
h_y_meas.Write()
h_phi_meas.Write()
h_m_meas.Write()
h_msd_meas.Write()
h_rho_meas.Write()
h_tau21_meas.Write()
h_dphi_meas.Write()
h_ptasym_meas.Write()
h_rho_vs_tau_meas.Write()


h2_y_meas.Write()
h2_phi_meas.Write()
h2_m_meas.Write()
h2_msd_meas.Write()
h2_rho_meas.Write()
h2_tau21_meas.Write()
h2_dphi_meas.Write()
h2_ptasym_meas.Write()
h2_mreco_mgen.Write()
h2_ptreco_ptgen.Write()
h2_mreco_mgen_softdrop.Write()
h2_ptreco_ptgen_softdrop.Write()
h2_mreco_mgen_nomnom.Write()
h2_ptreco_ptgen_nomnom.Write()
h2_mreco_mgen_softdrop_nomnom.Write()
h2_ptreco_ptgen_softdrop_nomnom.Write()

for isys in xrange( len(sysvarstr) ) : 
    h2_y_meas_sys[isys].Write()
    h2_phi_meas_sys[isys].Write()
    h2_m_meas_sys[isys].Write()
    h2_msd_meas_sys[isys].Write()
    h2_rho_meas_sys[isys].Write()
    h2_tau21_meas_sys[isys].Write()
    h2_dphi_meas_sys[isys].Write()
    h2_ptasym_meas_sys[isys].Write()
    h_2DHisto_meas_sys[isys].Write()
    h_2DHisto_measSD_sys[isys].Write()

fout.Close()
