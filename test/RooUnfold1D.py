#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas
from ROOT import gRandom, TH1, TH1D, cout
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
# from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold

f = ROOT.TFile("qcd_allpt_fixedresponses.root")

#h150 =f.Get("m_response_150")
h230 =f.Get("m_response_230")
h320 =f.Get("m_response_320")
h410 =f.Get("m_response_410")
h515 =f.Get("m_response_515")
h610 =f.Get("m_response_610")
h640 =f.Get("m_response_640")
h700 =f.Get("m_response_700")
#q80 =f.Get("HLT_PFJet80_mAK8")
q140 =f.Get("HLT_PFJet140_mAK8")
q200 =f.Get("HLT_PFJet200_mAK8")
q260 =f.Get("HLT_PFJet260_mAK8")
q320 =f.Get("HLT_PFJet320_mAK8")
q400 =f.Get("HLT_PFJet400_mAK8")
q450 =f.Get("HLT_PFJet450_mAK8")
q500 =f.Get("HLT_PFJet500_mAK8")
#qtrue80 =f.Get("HLT_PFJet80mAK8Gen")
qtrue140=f.Get("HLT_PFJet140mAK8Gen")
qtrue200=f.Get("HLT_PFJet200mAK8Gen")
qtrue260=f.Get("HLT_PFJet260mAK8Gen")
qtrue320=f.Get("HLT_PFJet320mAK8Gen")
qtrue400=f.Get("HLT_PFJet400mAK8Gen")
qtrue450=f.Get("HLT_PFJet450mAK8Gen")
qtrue500=f.Get("HLT_PFJet500mAK8Gen")
#uc1 = TCanvas("cdist80", "cdist80")
uc2 = TCanvas("cdist140", "cdist140")
uc3 = TCanvas("cdist200", "cdist200")
uc4 = TCanvas("cdist260", "cdist260")
uc5 = TCanvas("cdist320", "cdist320")
uc6 = TCanvas("cdist400", "cdist400")
uc7 = TCanvas("cdist450", "cdist450")
uc8 = TCanvas("cdist500", "cdist500")
#rc1 = TCanvas("cresponse150","cresponse150")
rc2 = TCanvas("cresponse200","cresponse200")
rc3 = TCanvas("cresponse300","cresponse300")
rc4 = TCanvas("cresponse400","cresponse400")
rc5 = TCanvas("cresponse500","cresponse500")
rc6 = TCanvas("cresponse600","cresponse600")
rc7 = TCanvas("cresponse700","cresponse700")
rc8 = TCanvas("cresponse800","cresponse800")
#c1 = TCanvas("ratio80", "ratio80")
c2 = TCanvas("ratio140", "ratio140")
c3 = TCanvas("ratio200", "ratio200")
c4 = TCanvas("ratio260", "ratio260")
c5 = TCanvas("ratio320", "ratio320")
c6 = TCanvas("ratio400", "ratio400")
c7 = TCanvas("ratio450", "ratio450")
c8 = TCanvas("ratio500", "ratio500")



responselist= [h230, h320, h410, h515, h610, h640, h700]
hMeaslist= [q140, q200, q260, q320, q400, q450, q500]
hTruelist= [qtrue140, qtrue200, qtrue260, qtrue320, qtrue400, qtrue450, qtrue500]
responsecanvases= [rc2, rc3, rc4, rc5, rc6, rc7, rc8]
unfoldingcanvases= [uc2, uc3, uc4, uc5, uc6, uc7, uc8]
ratiocanvases= [c2, c3, c4, c5, c6, c7, c8]
hRatioList = []

for i in responselist:

    index = responselist.index(i)
    print 'Using ' + str(index)
    correspondinghMeas = hMeaslist[index]
    correspondinghTrue = hTruelist[index]
    response = i
    responsecanvases[index].cd()
    response.Hresponse().Draw( "colz" )
    unfoldingcanvases[index].cd()
    hTrue= correspondinghTrue
    hMeas= correspondinghMeas
    unfold= RooUnfoldBayes( response, hMeas, 4 )
    hReco= unfold.Hreco()
    unfold.PrintTable ( cout, hTrue )
    hReco.SetMarkerStyle( 20 )
    hMeas.SetMarkerStyle( 21 )
    hMeas.SetMarkerColor( 2 )
    hReco.Draw()
    hMeas.Draw( "SAME" )
    hTrue.SetLineColor( 8 )
    hTrue.Draw( "hist SAME" )
    ratiocanvases[index].cd()
    #trueCopy = ROOT.TH1F()
    trueCopy = hTrue.Clone() # make a copy of hTrue? Thought something weird was happening with this becuase when it was acted on with division it changed in the previous plots.... strange
    trueCopy.SetName( 'ratio_' + str(index) )
    trueCopy.Divide( hReco ) # using the copy made it okay in previous plots, but these don't appear to make sense, they are not even close to one, at least they're not 10^9 anymore
    trueCopy.Draw("e")
    hRatioList.append( trueCopy) 
    ratiocanvases[index].Update()

#below was just checking that the plots were working correctly, division is weird, cant do h1/h2, not the same number of bins, have to do this for errors as well.

    #trueCopy.Divide(hTrue, hReco, 1, 1)
    #trueCopy.Divide(hReco)
    #trueCopy.Draw()
    #print "The division passes " + str(value)
    #hTrue.Divide(hTrue, hReco, 1, 1)
    #hTrue.Draw()
    #canvas5 = TCanvas('testingbefore', 'testingbefore')
    #canvas5.cd()
    #hTrue.Draw()
    #hReco.Draw("SAME")
    #canvas4 = TCanvas('testing', 'testingdivide')
    #canvas4.cd()


