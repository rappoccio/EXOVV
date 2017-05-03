#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = 'responses_rejec_tightgen_otherway_qcdmc_2dplots.root',
                  help='String to append to MC names')


(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gROOT.SetBatch()
#ROOT.gSystem.Load("libRooFitCore")

f = ROOT.TFile(options.infile)

ptbinstrs = ['#bf{200 < p_{T} < 260 GeV}','#bf{260 < p_{T} < 350 GeV}','#bf{350 < p_{T} < 460 GeV}','#bf{460 < p_{T} < 550 GeV}','#bf{550 < p_{T} < 650 GeV}','#bf{650 < p_{T} < 760 GeV}', '#bf{760 < p_{T} < 900 GeV}', '#bf{900 < p_{T} < 1000 GeV}', '#bf{1000 < p_{T} < 1100 GeV}','#bf{1100 < p_{T} < 1200 GeV}',
    '#bf{1200 < p_{T} < 1300 GeV}', '#bf{p_{T} > 1300 GeV}']

histstrs = [
    'h3_mreco_mgen',
    'h3_mreco_mgen_softdrop_nomnom',
    #'h2_ptreco_ptgen',
    #'h2_ptreco_ptgen_softdrop',
    ]
hists = []
canvs = []
fits = []
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kBlackBody)
ROOT.gStyle.SetTitleOffset( 1.0, "Y" )

prelim = ROOT.TLatex()
prelim.SetNDC()
prelim.SetTextFont(43)
prelim.SetTextSize(30)

tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(25)


graphs = []

import array

for ihist in xrange( len(histstrs) ):

    htemp = f.Get(histstrs[ihist])



    for ptbin in xrange( 1, htemp.GetNbinsX() ) :
        
        c = ROOT.TCanvas("c" + str(ihist) + "_pt" + str(ptbin), "c" + str(ihist) + "_pt" + str(ptbin) )
        htemp.GetXaxis().SetRange(ptbin,ptbin+1)
        hist2D = htemp.Project3D("zy")
        hist2D.SetName(htemp.GetName() + "_proj_pt" + str(ptbin) )
        hist2D.Scale( 1.0 / hist2D.Integral() )


        
        for mbin in xrange( 1, hist2D.GetNbinsX() + 1):
            sumv = 0.0
            for vbin in xrange( 1, hist2D.GetNbinsY() + 1) :
                sumv += hist2D.GetBinContent( mbin, vbin )
            if sumv > 0.0 :
                for vbin in xrange( 1, hist2D.GetNbinsY() + 1) :
                    hist2D.SetBinContent( mbin, vbin, hist2D.GetBinContent(mbin,vbin) / sumv )
        hist2D.Draw("colz")

        
        graphX = array.array('d', [])
        graphY = array.array('d', [])
        graphDX = array.array('d', [])
        graphDY = array.array('d', [])
        for mbin in xrange( 1, hist2D.GetNbinsX() + 1):
            proj = hist2D.ProjectionY(hist2D.GetName() + "_" + str(mbin), mbin, mbin+1)
            proj.SetTitle("p_{T} = " + ptbinstrs[ptbin] + ", m = " + str(hist2D.GetXaxis().GetBinLowEdge(mbin)) + "-" +str(hist2D.GetXaxis().GetBinUpEdge(mbin)) + ";m_{reco}/m_{gen}")
            cm = ROOT.TCanvas("cm" + str(ptbin) + "_" + str(mbin), "cm" + str(ptbin) + "_" + str(mbin) )
            if proj.Integral() > 0 :
                fit = ROOT.TF1("fit_pt_" + str(ptbin) + "_m_" + str(mbin) , "gaus", proj.GetMean() - proj.GetRMS(), proj.GetMean() + proj.GetRMS() )
                proj.Fit(fit, "LRM")
                canvs.append(cm)
                hists.append(proj)
                fits.append(fit)
                graphX.append( hist2D.GetXaxis().GetBinLowEdge(mbin) )
                graphDX.append( hist2D.GetXaxis().GetBinWidth(mbin) / 2.0 )
                graphY.append( fit.GetParameter(1) )
                graphDY.append( fit.GetParError(1) )
                proj.SetMaximum(1.3 * proj.GetMaximum())
                if ihist == 0 : 
                    cm.Print("mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_ungroomed.png", "png")
                    cm.Print("mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_ungroomed.pdf", "pdf")
                else :
                    cm.Print("mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_groomed.png", "png")
                    cm.Print("mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_groomed.pdf", "pdf")


        resc = ROOT.TCanvas("resc_" +str(ihist) + "_" + str(ptbin), "resc_" + str(ptbin) )
        massres = ROOT.TGraphErrors( len(graphX), graphX, graphY, graphDX, graphDY )
        massres.SetName("massres_" + str(ptbin))
        massres.SetTitle("p_{T} = " + ptbinstrs[ptbin] +"-" + ptbinstrs[ptbin] + ";Jet mass (GeV);Fitted m_{reco}/m_{gen}")
        massres.SetFillColor(ROOT.kBlue)
        massres.SetLineColor(ROOT.kBlue)
        massres.SetLineWidth(3)
        massres.SetFillStyle(3005)
        massres.Draw("AL3")        
        resc.SetLogx()
        massres.SetMaximum(2.0)
        massres.SetMinimum(0.0)
        graphs.append(massres)
        canvs.append(resc)
        if ihist == 0 : 
            resc.Print("mreco_mgen_pt_" + str(ptbin) +"_ungroomed.png", "png")
            resc.Print("mreco_mgen_pt_" + str(ptbin) +"_ungroomed.pdf", "pdf")
        else :
            resc.Print("mreco_mgen_pt_" + str(ptbin) +"_groomed.png", "png")
            resc.Print("mreco_mgen_pt_" + str(ptbin) +"_groomed.pdf", "pdf")

            
        #prof = hist2D.ProfileX("prof_" + str(ihist) + "_pt" + str(ptbin))
        #prof.SetMarkerStyle(20)
        #prof.Draw("same")
        #c.SetLogx()
        #canvs.append(c)        
        #hists.append(hist2D)
