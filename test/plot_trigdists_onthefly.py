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
ptBinA = array.array('d', [  200., 240., 310., 400., 530., 650., 760.])
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
    30000.0 * 0.045,
    2000.0 * 0.7,
    65.63 * 25.0,
    11.73 * 6.6667,
    3.97 * 2.000,
    1.23* 3.333,
    1.,
    #1.
    ]

def trigHelper( pt, trig ) :
    selectedTrig = None
    if ( (trig % 10000000) / 1000000 == 1 or (trig % 1000000) / 100000 == 1) and pt >= ptBinA[6] :
        selectedTrig = 6
    elif ((trig % 100000) / 10000 == 1) and ptBinA[5] <= pt and pt < ptBinA[6] :
        selectedTrig = 5
    elif ((trig % 10000) / 1000 == 1) and ptBinA[4] <= pt  and pt < ptBinA[5] :
        selectedTrig = 4
    elif ((trig % 1000) / 100 == 1) and ptBinA[3] <= pt  and pt < ptBinA[4] :
        selectedTrig = 3
    elif ((trig % 100) / 10 == 1) and ptBinA[2] <= pt  and pt < ptBinA[3] :
        selectedTrig = 2
    elif ((trig % 10) / 1 == 1) and ptBinA[1] <= pt  and pt < ptBinA[2] :
        selectedTrig = 1
    elif ( trig == 1) and ptBinA[0] <= pt  and pt < ptBinA[1] :
        selectedTrig = 0
    else :
        selectedTrig = None

    if selectedTrig == None :
        return None, None
    else:
        weight = scales[selectedTrig]
        return selectedTrig, weight

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

ptBinAToPlot = array.array('d', [  200., 240., 310., 400., 530., 650., 760., 13000.])
nbinsToPlot = len(ptBinAToPlot) - 1

h_2DHisto_meas = ROOT.TH2F('PFJet_pt_m_AK8', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsToPlot, ptBinAToPlot, 50, 0, 1000)
h_2DHisto_measSD = ROOT.TH2F('PFJet_pt_m_AK8SD', 'HLT Binned Mass and P_{T}; P_{T} (GeV); Mass (GeV)', nbinsToPlot, ptBinAToPlot, 50, 0, 1000)



for itrig,trig in enumerate(trigs) :
    pt0histpre = ROOT.TH1F(var + "_" + trig + "_pre", var + "_" + trig + "_pre", 200, 0, 2000)
    pt0histpre.SetMarkerStyle(markers[itrig])
    pt0histpre.SetMarkerColor(mcolors[itrig])
    pt0histspre.append(pt0histpre)

    
    pt0hist = ROOT.TH1F(var + "_" + trig, var + "_" + trig, 200, 0, 2000)
    pt0hist.SetFillColor( colors[itrig] )
    pt0hists.append(pt0hist)


    
    
stack = ROOT.THStack(var + '_stack', title)
canv = ROOT.TCanvas(var + '_stackcanv', var +'_stackcanv')
stackpre = ROOT.THStack(var + '_stackpre', title)
canvpre = ROOT.TCanvas(var + '_stackcanvpre', var +'_stackcanvpre')

for itree,t in enumerate(trees) :
    FatJetPt = array.array('f', [-1,-1])
    FatJetPhi = array.array('f', [-1,-1])
    FatJetMass = array.array('f', [-1,-1])
    FatJetMassSoftDrop = array.array('f', [-1,-1])
    Trig = array.array('i', [-1] )

    t.SetBranchStatus ('*', 0)
    t.SetBranchStatus ('FatJetPt', 1)
    t.SetBranchStatus ('FatJetPhi', 1)
    t.SetBranchStatus ('FatJetMass', 1)
    t.SetBranchStatus ('FatJetMassSoftDrop', 1)
    t.SetBranchStatus ('Trig', 1)

    t.SetBranchAddress ('FatJetPt', FatJetPt)
    t.SetBranchAddress ('FatJetPhi', FatJetPhi)
    t.SetBranchAddress ('FatJetMass', FatJetMass)
    t.SetBranchAddress ('FatJetMassSoftDrop', FatJetMassSoftDrop)
    t.SetBranchAddress ('Trig', Trig)
    
    entries = t.GetEntriesFast()
    for jentry in xrange( entries ):
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break
        if Trig[0] == None or Trig[0] < 0 :
            continue


        maxjet = 0
        if FatJetPt[0] < FatJetPt[1] :
            maxjet = 1

        passkin = (FatJetPt[maxjet] - FatJetPt[1])/(FatJetPt[maxjet] + FatJetPt[1]) < 0.3 and ROOT.TVector2.Phi_0_2pi( FatJetPhi[maxjet] - FatJetPhi[1] ) > 2.0
        if not passkin :
            continue


        
        pt0 = FatJetPt[maxjet]
        trigbin, weight = trigHelper( pt0, Trig[0] )



        if ( (Trig[0] % 10000000) / 1000000 == 1 or (Trig[0] % 1000000) / 100000 == 1) :
            pt0histspre[6].Fill( pt0, scales[6] )
        if ((Trig[0] % 100000) / 10000 == 1)  :
            pt0histspre[5].Fill( pt0, scales[5] )
        if ((Trig[0] % 10000) / 1000 == 1)  :
            pt0histspre[4].Fill( pt0, scales[4] )
        if ((Trig[0] % 1000) / 100 == 1)  :
            pt0histspre[3].Fill( pt0, scales[3] )
        if ((Trig[0] % 100) / 10 == 1)  :
            pt0histspre[2].Fill( pt0, scales[2] )
        if ((Trig[0] % 10) / 1 == 1) :
            pt0histspre[1].Fill( pt0, scales[1] )
        if ( Trig[0] == 1)  :
            pt0histspre[0].Fill( pt0, scales[0] )

        
        #print '   %10.2f, %6d, %6d, %30s, %6.2f' % (FatJetPt[0], Trig[0], trigbin, trigs[trigbin], scales[trigbin] )
        
        if trigbin == None :
            continue

        #print ' %8.2f %6d %30s %9.2f' % (FatJetPt[maxjet], trigbin, trigs[trigbin], scales[trigbin] )
        
        pt0hists[trigbin].Fill( pt0, weight )

        for ijet in [0,1] :
            h_2DHisto_meas.Fill( FatJetPt[ijet], FatJetMass[ijet], weight )
            h_2DHisto_measSD.Fill( FatJetPt[ijet], FatJetMassSoftDrop[ijet], weight )


    
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


fout = ROOT.TFile(options.outname, 'RECREATE')
fout.cd()
h_2DHisto_meas.Write()
h_2DHisto_measSD.Write()
fout.Close()
