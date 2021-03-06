#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'jetht_run2015B_newjec.root',
                  help='Input file')


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht_weighted_dataplots_otherway_repdf.root",
                  help='Output string for output file')

parser.add_option('--plotname', type='string', action='store',
                  dest='plotname',
                  default = "",
                  help='Plot name for trig eff plots')



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
#                             80   140   200   260   320   400   450
ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760.] )


trigs = [
    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    #'HLT_PFJet500' 
    ]

# Here I'm totally cheating. The first numbers are the right ones from brilcalc.
# The second products are to make sure they match, by eye. Something is completely
# wrong here with our setup, but I don't understand what that is, since this worked
# in Run 1 just fine.


scales = [
    4470.10011779109,
    812.576304821248,
    114.125335364053,
    11.3891892511202,
    5.40698304071761,
    2.38456032833827,
    1,
    ]

## scales = [
##     30000.0 * 0.045,
##     2000.0 * 0.7,
##     65.63 * 25.0,
##     11.73 * 6.6667,
##     3.97 * 2.000,
##     1.23* 3.333,
##     1.,
##     #1.
##     ]

    
def isPFJet80 ( trig ) :
    return ( int(trig) % 10 == 1 )
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
    return ( int(trig / 1000000) % 10 == 1 ) #or int(trig / 10000000) % 10 == 1)


trigfuncs = [isPFJet80, isPFJet140, isPFJet200, isPFJet260, isPFJet320, isPFJet400, isPFJet450]

def trigHelper( pt, trig ) :

    #print 'pt, trig = ', pt, ' ', trig,
    if pt < ptBinA[0] :
        return False, None
    
    nptBinA = len( ptBinA )
    ikeep = 0
    for ipt in xrange( nptBinA-1, -1, -1) :
        if pt >= ptBinA[ipt]:
            ikeep = ipt
            break
    #print ', ikeep = ', ikeep, 
    ipass = trigfuncs[ikeep](trig)
    #print ', ipass = ', ipass, 
    #if ipass == True : 
    #    print ', scale = ', scales[ikeep]
    #else: 
    #    print ''
    return ipass, ikeep
    
        
    ## selectedTrig = None
    ## if isPFJet450(trig) and pt >= ptBinA[6] :
    ##     selectedTrig = 6
    ## elif isPFJet400(trig) and ptBinA[5] <= pt and pt < ptBinA[6] :
    ##     selectedTrig = 5
    ## elif isPFJet320(trig) and ptBinA[4] <= pt  and pt < ptBinA[5] :
    ##     selectedTrig = 4
    ## elif isPFJet260(trig) and ptBinA[3] <= pt  and pt < ptBinA[4] :
    ##     selectedTrig = 3
    ## elif isPFJet200(trig) and ptBinA[2] <= pt  and pt < ptBinA[3] :
    ##     selectedTrig = 2
    ## elif isPFJet140(trig) and ptBinA[1] <= pt  and pt < ptBinA[2] :
    ##     selectedTrig = 1
    ## elif isPFJet80(trig)  and ptBinA[0] <= pt  and pt < ptBinA[1] :
    ##     selectedTrig = 0
    ## else :
    ##     selectedTrig = None

    ## if selectedTrig == None :
    ##     return None, None
    ## else:
    ##     weight = scales[selectedTrig]
    ##     return selectedTrig, weight



    
f = ROOT.TFile(options.file)
trees = [ f.Get("TreeEXOVV") ]

colors = [
    ROOT.kWhite,
    ROOT.kRed - 10,
    ROOT.kRed - 9,
    ROOT.kRed - 7,
    ROOT.kRed - 4,
    ROOT.kRed,
    ROOT.kRed + 1,
    #ROOT.kRed + 3,
    ]

mcolors = [
    ROOT.kBlack,
    ROOT.kRed,
    ROOT.kGreen + 3,
    ROOT.kBlue,
    ROOT.kOrange,
    ROOT.kMagenta,
    ROOT.kBlack,
    #ROOT.kRed,
    ]

markers =[
    24,
    20,
    21,
    22,
    23,
    29,
    33,
    #34
    ]

logy = [ True, True, False, True, True, True, True, True, True, False, False ]
palette = [0, 2]


var = 'FatJetPt'
title = ';AK8 Jet p_{T} (GeV);Number'

ROOT.gStyle.SetPadRightMargin(0.15)

pt0histspre = []
pt0hists = []
pt0histsTurnon = []
ptsd0histspre = []
ptsd0hists = []
ptsd0histsTurnon = []

#ptBinAToPlot = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 13000.])
#nbinsToPlot = len(ptBinAToPlot) - 1
#new binnings make trighelper unhappy so you need to make sure to give them a name that indicates they're to be plotted
ptBinAToPlot = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])
nbinsToPlot = len(ptBinAToPlot) - 1
mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])
nbinsm = len(mBinA) - 1

h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsToPlot, ptBinAToPlot)
h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsm, mBinA, nbinsToPlot, ptBinAToPlot)

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

h_nvtx = ROOT.TH1F("h_nvtx", ";N_{PV};Number", 100,0,100)

for itrig,trig in enumerate(trigs) :
    pt0histpre = ROOT.TH1F(var + "_" + trig + "_pre", var + "_" + trig + "_pre", 200, 0, 2000)
    pt0histpre.SetMarkerStyle(markers[itrig])
    pt0histpre.SetMarkerColor(mcolors[itrig])
    pt0histspre.append(pt0histpre)

    
    pt0hist = ROOT.TH1F(var + "_" + trig, var + "_" + trig, 200, 0, 2000)
    pt0hist.SetFillColor( colors[itrig] )
    pt0hists.append(pt0hist)

    pt0histTurnon = ROOT.TH1F(var + "_" + trig + "_turnon", var + "_" + trig + "_turnon", 200, 0, 2000)
    pt0histTurnon.SetMarkerColor( colors[itrig] )
    pt0histsTurnon.append(pt0histTurnon)


    ptsd0histpre = ROOT.TH1F(var + "sd_" + trig + "_pre", var + "sd_" + trig + "_pre", 200, 0, 2000)
    ptsd0histpre.SetMarkerStyle(markers[itrig])
    ptsd0histpre.SetMarkerColor(mcolors[itrig])
    ptsd0histspre.append(ptsd0histpre)

    
    ptsd0hist = ROOT.TH1F(var + "sd_" + trig, var + "sd_" + trig, 200, 0, 2000)
    ptsd0hist.SetFillColor( colors[itrig] )
    ptsd0hists.append(ptsd0hist)

    ptsd0histTurnon = ROOT.TH1F(var + "sd_" + trig + "_turnon", var + "sd_" + trig + "_turnon", 200, 0, 2000)
    ptsd0histTurnon.SetMarkerColor( colors[itrig] )
    ptsd0histsTurnon.append(ptsd0histTurnon)


        
    
stack = ROOT.THStack(var + '_stack', title)
canv = ROOT.TCanvas(var + '_stackcanv', var +'_stackcanv')
stackpre = ROOT.THStack(var + '_stackpre', title)
canvpre = ROOT.TCanvas(var + '_stackcanvpre', var +'_stackcanvpre')

for itree,t in enumerate(trees) :
    NFatJet = array.array('i', [0] )
    FatJetPt = array.array('f', [-1]*5)
    FatJetRap = array.array('f', [-1]*5)
    FatJetEta = array.array('f', [-1]*5)
    FatJetPhi = array.array('f', [-1]*5)
    FatJetMass = array.array('f', [-1]*5)
    FatJetMassSoftDrop = array.array('f', [-1]*5)
    FatJetPtSoftDrop = array.array('f', [-1]*5 )
    FatJetRhoRatio = array.array('f', [-1]*5)
    FatJetTau21 = array.array('f', [-1]*5)
    FatJetTau32 = array.array('f', [-1]*5)
    METpt = array.array('f', [-1])
    Trig = array.array('i', [-1] )
    Nvtx = array.array('f', [-1.0] )

    t.SetBranchStatus('*', 0)
    t.SetBranchStatus('NFatJet', 1)
    t.SetBranchStatus('FatJetPt', 1)
    t.SetBranchStatus('FatJetRap', 1)
    t.SetBranchStatus('FatJetEta', 1)
    t.SetBranchStatus('FatJetPhi', 1)
    t.SetBranchStatus('FatJetMass', 1)
    t.SetBranchStatus('FatJetMassSoftDrop', 1)
    t.SetBranchStatus('FatJetPtSoftDrop', 1)
    t.SetBranchStatus( 'FatJetRhoRatio', 1)
    t.SetBranchStatus( 'FatJetTau21', 1)
    t.SetBranchStatus( 'FatJetTau32', 1)
    t.SetBranchStatus( 'METpt', 1)
    t.SetBranchStatus('Trig', 1)
    t.SetBranchStatus('Nvtx', 1)

    t.SetBranchAddress('NFatJet', NFatJet)
    t.SetBranchAddress('FatJetPt', FatJetPt)
    t.SetBranchAddress('FatJetRap', FatJetRap)
    t.SetBranchAddress('FatJetEta', FatJetEta)
    t.SetBranchAddress('FatJetPhi', FatJetPhi)
    t.SetBranchAddress('FatJetMass', FatJetMass)
    t.SetBranchAddress('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress('FatJetPtSoftDrop', FatJetPtSoftDrop)
    t.SetBranchAddress( 'FatJetRhoRatio', FatJetRhoRatio)
    t.SetBranchAddress( 'FatJetTau21', FatJetTau21)
    t.SetBranchAddress( 'FatJetTau32', FatJetTau32)
    t.SetBranchAddress( 'METpt', METpt)    
    t.SetBranchAddress('Trig', Trig)
    t.SetBranchAddress('Nvtx', Nvtx)
    
    entries = t.GetEntriesFast()
    #entries = 10000
    for jentry in xrange( entries ):
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break
        if Trig[0] == None or Trig[0] <= 0 :
            continue
        if FatJetPt[0] < 220. :
            continue
        if jentry % 100000 == 0 : 
            print '%15d / %20d = %6.2f' % (jentry, entries, float(jentry)/float(entries) )



        h_nvtx.Fill( Nvtx[0] )

        if NFatJet[0] < 2 :
            continue

        ptToSort = [ ]
        for ijet in xrange(NFatJet[0]):
            ptToSort.append( (ijet, FatJetPt[ijet] ) )

        ptSorted = sorted( ptToSort, key=itemgetter(1), reverse=True)

        indices = [ index[0] for index in ptSorted ]
        
        maxjet = indices[0]
        minjet = indices[1]
        pt0 = FatJetPt[maxjet]
        ptsd0 = FatJetPtSoftDrop[maxjet]

        if pt0 > 13000. : # Sanity check
            continue
        if FatJetPt[minjet] < 220. : # require both jets to be >= 200 GeV
            continue
        
        ptasym = (FatJetPt[maxjet] - FatJetPt[minjet])/(FatJetPt[maxjet] + FatJetPt[minjet])
        dphi = ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[minjet] )

        ipass, trigbin = trigHelper( pt0, Trig[0] )

        if trigbin != None and trigbin >= 0 : 
            weight = scales[trigbin]
        else :
            weight = 0.0

                        
        if dphi > 1.57 and dphi < 4.71:
            h_ptasym_meas.Fill( ptasym, weight )
        if ptasym < 0.3 :
            h_dphi_meas.Fill( dphi, weight )

        passkin = ptasym < 0.3 and dphi > 1.57 and dphi < 4.71
        if not passkin :
            continue


        if isPFJet450( Trig[0] ) :
            pt0histspre[6].Fill( pt0 )
            ptsd0histspre[6].Fill( ptsd0 )

            
        if isPFJet400( Trig[0] )  :
            pt0histspre[5].Fill( pt0 )
            ptsd0histspre[5].Fill( ptsd0 )
            if isPFJet450( Trig[0] ) :
                pt0histsTurnon[5].Fill( pt0 )
                ptsd0histsTurnon[5].Fill( ptsd0 )


            
        if isPFJet320( Trig[0] )  :
            pt0histspre[4].Fill( pt0 )
            ptsd0histspre[4].Fill( ptsd0 )
            if isPFJet400( Trig[0] ) :
                pt0histsTurnon[4].Fill( pt0 )
                ptsd0histsTurnon[4].Fill( ptsd0 )


            
        if isPFJet260( Trig[0] )  :
            pt0histspre[3].Fill( pt0 )
            ptsd0histspre[3].Fill( ptsd0 )
            if isPFJet320( Trig[0] ) :
                pt0histsTurnon[3].Fill( pt0 )
                ptsd0histsTurnon[3].Fill( ptsd0 )

            
        if isPFJet200( Trig[0] )  :
            pt0histspre[2].Fill( pt0 )
            ptsd0histspre[2].Fill( ptsd0 )
            if isPFJet260( Trig[0] ) :
                pt0histsTurnon[2].Fill( pt0 )
                ptsd0histsTurnon[2].Fill( ptsd0 )

            
        if isPFJet140( Trig[0] ) :
            pt0histspre[1].Fill( pt0 )
            ptsd0histspre[1].Fill( ptsd0 )
            if isPFJet200( Trig[0] ) :
                pt0histsTurnon[1].Fill( pt0 )
                ptsd0histsTurnon[1].Fill( ptsd0 )

                        
        if isPFJet80( Trig[0] ) :
            pt0histspre[0].Fill( pt0 )
            ptsd0histspre[0].Fill( ptsd0 )
            if isPFJet140( Trig[0] ) :
                pt0histsTurnon[0].Fill( pt0 )
                ptsd0histsTurnon[0].Fill( ptsd0 )

                

        
        #print 'ipass, trigbin, trig, pt0 = ', ipass, ' ', trigbin, ' ', Trig[0], ' ', pt0
        if trigbin == None or ipass == False :
            continue


        #print 'pt0 = %6.2f, trigbin = %6d, weight = %8.2f' % (pt0, trigbin, weight )

        #print '   %10.2f, %6d, %6d, %30s, %6.2f' % (FatJetPt[0], Trig[0], trigbin, trigs[trigbin], scales[trigbin] )
        
        #print ' %8.2f %6d %30s %9.2f' % (FatJetPt[maxjet], trigbin, trigs[trigbin], scales[trigbin] )
        
        pt0hists[trigbin].Fill( pt0, weight )
        
        for ijet in [ indices[0], indices[1] ] :
            if abs(FatJetEta[ijet]) < 2.4 : 
                h_2DHisto_meas.Fill( FatJetMass[ijet], FatJetPt[ijet], weight )
                h_2DHisto_measSD.Fill( FatJetMassSoftDrop[ijet], FatJetPt[ijet], weight )
                h_pt_meas.Fill( FatJetPt[ijet] , weight )
                h_y_meas.Fill( FatJetRap[ijet] , weight )
                h_phi_meas.Fill( FatJetPhi[ijet] , weight )
                h_m_meas.Fill( FatJetMass[ijet] , weight )
                h_msd_meas.Fill( FatJetMassSoftDrop[ijet] , weight )
                h_rho_meas.Fill( FatJetRhoRatio[ijet] , weight )
                h_tau21_meas.Fill( FatJetTau21[ijet] , weight )
                h_rho_vs_tau_meas.Fill( FatJetRhoRatio[ijet], FatJetTau21[ijet] , weight )
    
leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)
legpre = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
legpre.SetFillColor(0)
legpre.SetBorderSize(0)

fout = ROOT.TFile(options.outname, 'RECREATE')
fout.cd()


for ipt0hist,pt0hist in enumerate(pt0hists):
    stack.Add( pt0hist )
    stackpre.Add( pt0histspre[ipt0hist] )
    leg.AddEntry(pt0hist, trigs[ipt0hist], 'f')
    legpre.AddEntry(pt0histspre[ipt0hist], trigs[ipt0hist], 'p')    
    pt0hist.Write()
    pt0histspre[ipt0hist].Write()
    
canv.cd()
stack.Draw('hist')
stack.Draw('e same')
if logy[ipt0hist] : 
    canv.SetLogy()
    stack.SetMinimum(0.1)
leg.Draw()
canv.Update()
canv.Print( 'trigplots_' + var + '.png', 'png')
canv.Print( 'trigplots_' + var + '.pdf', 'pdf')


canvpre.cd()
stackpre.Draw('nostack e')
legpre.Draw()
if logy[ipt0hist] : 
    canvpre.SetLogy()
    stackpre.SetMinimum(0.1)

canvpre.Update()
canvpre.Print( 'trigplots_pre_' + var + '.png', 'png')
canvpre.Print( 'trigplots_pre_' + var + '.pdf', 'pdf')


turnoncanvs = []
efficiencies = []
for itrig in xrange(len(trigs) - 1):
    trig = trigs[itrig]
    pt0histsTurnon[itrig].Sumw2()
    efficiency = ROOT.TEfficiency( pt0histsTurnon[itrig], pt0histspre[itrig] )
    efficiency.SetTitle("Trigger Turnon, " + trigs[itrig + 1] )
    turnoncanv = ROOT.TCanvas("cturnon" + str(itrig), "cturnon" + str(itrig) )
    efficiency.Draw('ap')
    turnoncanvs.append(turnoncanv)
    turnoncanv.Print( 'trigplots_turnon_' + var + '_' + str(itrig) + options.plotname +  '.png', 'png')
    turnoncanv.Print( 'trigplots_turnon_' + var + '_' + str(itrig) + options.plotname +  '.pdf', 'pdf')
    efficiency.Write()

    ptsd0histsTurnon[itrig].Sumw2()
    efficiencySD = ROOT.TEfficiency( ptsd0histsTurnon[itrig], ptsd0histspre[itrig] )
    efficiencySD.SetTitle("Trigger Turnon, " + trigs[itrig + 1] )

    turnoncanv = ROOT.TCanvas("cturnonsd" + str(itrig), "cturnonsd" + str(itrig) )
    efficiencySD.Draw('ap')
    turnoncanvs.append(turnoncanv)
    turnoncanv.Print( 'trigplots_turnon_' + var + 'sd_' + str(itrig) + options.plotname + '.png', 'png')
    turnoncanv.Print( 'trigplots_turnon_' + var + 'sd_' + str(itrig) + options.plotname + '.pdf', 'pdf')
    efficiencySD.Write()

    efficiencies.append( efficiency )
    efficiencies.append( efficiencySD )

h_2DHisto_meas.Write()
h_2DHisto_measSD.Write()
h_nvtx.Write()
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
fout.Close()
