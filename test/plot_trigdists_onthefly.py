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

#                             80   140   200   260   320   400   450
ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760.])
nbinsPt = len(ptBinA) - 1


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
    30000.0,
    2000.0,
    65.63430429669079,
    11.732244475363055,
    3.967946158336121,
    1.2334089024152257,
    1.,
    #1.
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
    return  trig == 1
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


trigfuncs = [isPFJet80, isPFJet140, isPFJet200, isPFJet260, isPFJet320, isPFJet400, isPFJet450]

def trigHelper( pt, trig ) :


    if pt < ptBinA[0] :
        return False, None
    
    nptBinA = len( ptBinA )
    ipt = 0
    for ipt in xrange( nptBinA-1, 0, -1) :
        if pt > ptBinA[ipt] :
            break
    ipass = trigfuncs[ipt](trig)
    return ipass, ipt
    
        
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

ptBinAToPlot = array.array('d', [  200., 240., 310., 460., 530., 650., 760., 13000.])
nbinsToPlot = len(ptBinAToPlot) - 1

h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsToPlot, ptBinAToPlot, 50, 0, 1000)
h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsToPlot, ptBinAToPlot, 50, 0, 1000)

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
    
    
stack = ROOT.THStack(var + '_stack', title)
canv = ROOT.TCanvas(var + '_stackcanv', var +'_stackcanv')
stackpre = ROOT.THStack(var + '_stackpre', title)
canvpre = ROOT.TCanvas(var + '_stackcanvpre', var +'_stackcanvpre')

for itree,t in enumerate(trees) :
    FatJetPt = array.array('f', [-1,-1])
    FatJetRap = array.array('f', [-1,-1])
    FatJetPhi = array.array('f', [-1,-1])
    FatJetMass = array.array('f', [-1,-1])
    FatJetMassSoftDrop = array.array('f', [-1,-1])
    FatJetRhoRatio = array.array('f', [-1,-1])
    FatJetTau21 = array.array('f', [-1,-1])
    FatJetTau32 = array.array('f', [-1,-1])
    METpt = array.array('f', [-1])
    Trig = array.array('i', [-1] )

    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetRap', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus( 'FatJetRhoRatio', 1)
    t.SetBranchStatus( 'FatJetTau21', 1)
    t.SetBranchStatus( 'FatJetTau32', 1)
    t.SetBranchStatus( 'METpt', 1)
    t.SetBranchStatus ('Trig', 1)

    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetRap', FatJetRap)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress( 'FatJetRhoRatio', FatJetRhoRatio)
    t.SetBranchAddress( 'FatJetTau21', FatJetTau21)
    t.SetBranchAddress( 'FatJetTau32', FatJetTau32)
    t.SetBranchAddress( 'METpt', METpt)    
    t.SetBranchAddress ('Trig', Trig)
    
    entries = t.GetEntriesFast()
    for jentry in xrange( entries ):
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break
        if Trig[0] == None or Trig[0] < 0 :
            continue

        maxjet = 0
        minjet = 1
        if FatJetPt[0] < FatJetPt[1] :
            maxjet = 1
            minjet = 0
        pt0 = FatJetPt[maxjet]


        if isPFJet450( Trig[0] ) :
            pt0histspre[6].Fill( pt0, scales[6] )

            
        if isPFJet400( Trig[0] )  :
            pt0histspre[5].Fill( pt0, scales[5] )
            if isPFJet450( Trig[0] ) :
                pt0histsTurnon[5].Fill( pt0, scales[5] )


            
        if isPFJet320( Trig[0] )  :
            pt0histspre[4].Fill( pt0, scales[4] )
            if isPFJet400( Trig[0] ) :
                pt0histsTurnon[4].Fill( pt0, scales[4] )


            
        if isPFJet260( Trig[0] )  :
            pt0histspre[3].Fill( pt0, scales[3] )
            if isPFJet320( Trig[0] ) :
                pt0histsTurnon[3].Fill( pt0, scales[3] )

            
        if isPFJet200( Trig[0] )  :
            pt0histspre[2].Fill( pt0, scales[2] )
            if isPFJet260( Trig[0] ) :
                pt0histsTurnon[2].Fill( pt0, scales[2] )

            
        if isPFJet140( Trig[0] ) :
            pt0histspre[1].Fill( pt0, scales[1] )
            if isPFJet200( Trig[0] ) :
                pt0histsTurnon[1].Fill( pt0, scales[1] )

                        
        if isPFJet80( Trig[0] ) :
            pt0histspre[0].Fill( pt0, scales[0] )
            if isPFJet140( Trig[0] ) :
                pt0histsTurnon[0].Fill( pt0, scales[0] )

                

        ipass, trigbin = trigHelper( pt0, Trig[0] )
        weight = scales[trigbin]


        if trigbin == None or ipass == False :
            continue


        ptasym = (FatJetPt[maxjet] - FatJetPt[minjet])/(FatJetPt[maxjet] + FatJetPt[minjet])
        dphi = ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[minjet] )

                
        if dphi > 2.0 :
            h_ptasym_meas.Fill( ptasym, weight )
        if ptasym < 0.3 :
            h_dphi_meas.Fill( dphi, weight )

        passkin = ptasym < 0.3 and dphi > 2.0
        if not passkin :
            continue


        #print 'pt0 = %6.2f, trigbin = %6d, weight = %8.2f' % (pt0, trigbin, weight )

        #print '   %10.2f, %6d, %6d, %30s, %6.2f' % (FatJetPt[0], Trig[0], trigbin, trigs[trigbin], scales[trigbin] )
        
        #print ' %8.2f %6d %30s %9.2f' % (FatJetPt[maxjet], trigbin, trigs[trigbin], scales[trigbin] )
        
        pt0hists[trigbin].Fill( pt0, weight )
        
        for ijet in [0,1] :
            h_2DHisto_meas.Fill( FatJetPt[ijet], FatJetMass[ijet], weight )
            h_2DHisto_measSD.Fill( FatJetPt[ijet], FatJetMassSoftDrop[ijet], weight )
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


for ipt0hist,pt0hist in enumerate(pt0hists):
    stack.Add( pt0hist )
    stackpre.Add( pt0histspre[ipt0hist] )
    leg.AddEntry(pt0hist, trigs[ipt0hist], 'f')
    legpre.AddEntry(pt0histspre[ipt0hist], trigs[ipt0hist], 'p')    
    
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

ptBinB = [ 0.]
for ival in ptBinA : ptBinB.append( ival )

for ihist, hist in enumerate(pt0histspre) :
    print '%30s : %10d : ' % (hist.GetName(), hist.GetEntries()),
    for iptbin in xrange( 0, len(ptBinB) ) :
        bin1 = hist.GetXaxis().FindBin( ptBinB[iptbin] )
        bin2 = hist.GetXaxis().FindBin( ptBinB[iptbin] + 1 )
        bin3 = hist.GetXaxis().FindBin( 10000. )
        nbin = hist.Integral(bin1, bin2) 
        nover= hist.Integral(bin2, bin3 )
        ntot = hist.Integral()
        print ' %8.4f ' % ( nbin / ntot ),
    print ''
        

turnoncanvs = []
for itrig, trig in enumerate(trigs):
    pt0histsTurnon[itrig].Sumw2()
    pt0histsTurnon[itrig].Divide( pt0histspre[itrig] )
    turnoncanv = ROOT.TCanvas("cturnon" + str(itrig), "cturnon" + str(itrig) )
    pt0histsTurnon[itrig].Draw('e')
    turnoncanvs.append(turnoncanv)


fout = ROOT.TFile(options.outname, 'RECREATE')
fout.cd()
h_2DHisto_meas.Write()
h_2DHisto_measSD.Write()
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
