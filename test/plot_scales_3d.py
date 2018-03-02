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

parser.add_option('--postfix', type='string', action='store',
                  dest='postfix',
                  default = '',
                  help='Postfix for plots')

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = 'h3_mreco_mgen',
                  help='Hist to plot')

parser.add_option('--useAN', action='store_true',
                  dest='useAN',
                  default = False,
                  help='Plot everything for AN?')

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

groomstr = '_groomed' if 'softdrop' in options.hist else '_ungroomed'


ptbinstrs = ['#bf{200 < p_{T} < 260 GeV}',
                 '#bf{260 < p_{T} < 350 GeV}',
                 '#bf{350 < p_{T} < 460 GeV}',
                 '#bf{460 < p_{T} < 550 GeV}',
                 '#bf{550 < p_{T} < 650 GeV}',
                 '#bf{650 < p_{T} < 760 GeV}',
                 '#bf{760 < p_{T} < 900 GeV}',
                 '#bf{900 < p_{T} < 1000 GeV}',
                 '#bf{1000 < p_{T} < 1100 GeV}',
                 '#bf{1100 < p_{T} < 1200 GeV}',
                 '#bf{1200 < p_{T} < 1300 GeV}',
                 '#bf{p_{T} > 1300 GeV}'
                 ]

ptquickstrs = ['200-260 GeV',
                   '260-350 GeV',
                   '350-460 GeV',
                   '460-550 GeV',
                   '550-650 GeV',
                   '650-760 GeV',
                   '760-900 GeV',
                   '900-1000 GeV',
                   '1000-1100 GeV',
                   '1100-1200 GeV',
                   '1200-1300 GeV',
                   '>1300 GeV'
                   ]

if 'softdrop' in options.hist :
    maxMass = [10] * len(ptbinstrs)
else :
    #         200 260 350 460 550 650 760 900 1000 1100 1200 >1300
    maxMass = [20, 20, 20, 20, 20, 20, 40, 40,  40,  40,  40,  40]
    
histstrs = [
    options.hist,
    ]
hists = []
canvs = []
fits = []
multigraphs = []
legs = []
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

markers = [20,21,22,23,29,33,34,24,25,26,27,28]
if options.useAN:
    binsToPlot = [i for i in xrange(12)]
else : 
    binsToPlot = [1,5,7,10]
styles = dict( zip( binsToPlot, [1,2,3,4,1,2,3,4,1,2,3,4] ) )
colors = dict( zip( binsToPlot, [1,2,ROOT.kGreen+3,4,1,2,ROOT.kGreen+3,4,1,2,ROOT.kGreen+3,4] ) )

lines = []
graphs = []

import array


for ihist in xrange( len(histstrs) ):

    htemp = f.Get(histstrs[ihist])

    totresc = ROOT.TCanvas("totresc_" +str(ihist), "totresc_" + str(ihist) )
    totresc2 = ROOT.TCanvas("totresc2_" +str(ihist), "totresc2_" + str(ihist) )
    mg = ROOT.TMultiGraph("mg_" + str(ihist), "mg_" + str(ihist))
    rg = ROOT.TMultiGraph("rg_" + str(ihist), "rg_" + str(ihist))
    canvs.append(totresc)
    multigraphs.append([mg,rg])
    leg = ROOT.TLegend(0.5, 0.44, 0.84, 0.84)
    leg.SetHeader("p_{T} Bins")
    #leg.SetNColumns(4)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    legs.append(leg)
    leg2 = ROOT.TLegend(0.5, 0.44, 0.84, 0.84)
    leg2.SetHeader("p_{T} Bins")
    #leg2.SetNColumns(4)
    leg2.SetFillColor(0)
    leg2.SetBorderSize(0)
    legs.append(leg2)
    leg3 = ROOT.TLegend(0.5, 0.44, 0.84, 0.84)
    leg3.SetHeader("p_{T} Bins")
    #leg3.SetNColumns(4)
    leg3.SetFillColor(0)
    leg3.SetBorderSize(0)
    legs.append(leg3)

    
    for ptbin in binsToPlot: # xrange( 1, htemp.GetNbinsX() ) :

        print 'processing ptbin ', ptbin
        
        #c = ROOT.TCanvas("c" + str(ihist) + "_pt" + str(ptbin), "c" + str(ihist) + "_pt" + str(ptbin) )
        htemp.GetXaxis().SetRange(ptbin,ptbin+1)
        hist2D = htemp.Project3D("zy")
        hist2D.SetName(htemp.GetName() + "_proj_pt" + str(ptbin) )
        if hist2D.Integral() > 0 : 
            hist2D.Scale( 1.0 / hist2D.Integral() )


        
        for mbin in xrange( 1, hist2D.GetNbinsX() + 1):
            sumv = 0.0
            for vbin in xrange( 1, hist2D.GetNbinsY() + 1) :
                sumv += hist2D.GetBinContent( mbin, vbin )
            if sumv > 0.0 :
                for vbin in xrange( 1, hist2D.GetNbinsY() + 1) :
                    hist2D.SetBinContent( mbin, vbin, hist2D.GetBinContent(mbin,vbin) / sumv )
        hist2D.Draw("colz")

        
        graphX = array.array('d', [])      # Jet mass
        graphY = array.array('d', [])      # Mean of fit (jet mass scale)
        graphDX = array.array('d', [])     # Width of jet mass bin
        graphDY = array.array('d', [])     # Width of fit (jet mass resolution)
        graphdY = array.array('d', [])     # Uncertainty on mean (jms unc)
        graphdDY = array.array('d', [])    # Uncertainty on width (jmr unc)
        for mbin in xrange( 1, hist2D.GetNbinsX() + 1):
            proj = hist2D.ProjectionY(hist2D.GetName() + "_" + str(mbin), mbin, mbin+1)
            proj.SetTitle("p_{T} = " + ptbinstrs[ptbin] + ", m = " + str(hist2D.GetXaxis().GetBinLowEdge(mbin)) + "-" +str(hist2D.GetXaxis().GetBinUpEdge(mbin)) + ";m_{reco}/m_{gen}")
            cm = ROOT.TCanvas("cm" + str(ptbin) + "_" + str(mbin), "cm" + str(ptbin) + "_" + str(mbin) )
            
            #fit = ROOT.TF1("fit_pt_" + str(ptbin) + "_m_" + str(mbin) , "gaus", proj.GetMean() - proj.GetRMS(), proj.GetMean() + proj.GetRMS() )
            fit = ROOT.TF1("fit_pt_" + str(ptbin) + "_m_" + str(mbin) , "gaus", 0.5, 1.5 )
            if proj.Integral() > 0 :
                print ' low edge: ', hist2D.GetXaxis().GetBinLowEdge(mbin), ' < max mass? ', maxMass[ptbin]
                if options.useAN or hist2D.GetXaxis().GetBinLowEdge(mbin) >= maxMass[ptbin] :
                    proj.Fit(fit, "LRMQ")
                    graphX.append( hist2D.GetXaxis().GetBinLowEdge(mbin) )
                    graphDX.append( hist2D.GetXaxis().GetBinWidth(mbin) / 2.0 )
                    graphY.append( fit.GetParameter(1) )
                    graphDY.append( fit.GetParameter(2) )
                    graphdY.append( fit.GetParError(1) )
                    graphdDY.append( fit.GetParError(2) )
                    proj.SetMaximum(1.3 * proj.GetMaximum())

            else :
                proj.Draw("A")
            #canvs.append(cm)
            hists.append(proj)
            fits.append(fit)
            if 'softdrop' not in options.hist : 
                cm.Print("fits3d/mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_ungroomed" + options.postfix + ".png", "png")
                cm.Print("fits3d/mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_ungroomed" + options.postfix + ".pdf", "pdf")
            else :
                cm.Print("fits3d/mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_groomed" + options.postfix + ".png", "png")
                cm.Print("fits3d/mreco_mgen_fits_pt_" + str(ptbin) + "_m_" + str(mbin) + "_groomed" + options.postfix + ".pdf", "pdf")



        ##### Plot the jet mass scale and uncertainty.
        resc = ROOT.TCanvas("resc_" +str(ihist) + "_" + str(ptbin), "resc_" + str(ptbin) )
        #massres = ROOT.TGraphErrors( len(graphX), graphX, graphY, graphDX, graphDY )
        massres = ROOT.TGraphErrors( len(graphX), graphX, graphY, graphDX, graphdY )
        massres.SetName("massres_" + str(ptbin))
        if 'softdrop' not in options.hist : 
            massres.SetTitle(";Ungroomed jet mass (GeV);JMS")
        else :
            massres.SetTitle(";Groomed jet mass (GeV);JMS")
        leg.AddEntry( massres, ptquickstrs[ptbin], "l" )
        massres.SetFillColor(colors[ptbin])
        massres.SetLineColor(colors[ptbin])
        massres.SetLineWidth(2)
        massres.SetLineStyle(styles[ptbin])
        massres.SetFillStyle(3005)
        resc.cd()
        massres.Draw("AL3")
        resc.SetLogx()
        massres.SetMaximum(2.0)
        massres.SetMinimum(0.0)
        graphs.append(massres)
        canvs.append(resc)
        prelim.Draw()
        tlx.DrawLatex ( 0.6, 0.830, ptbinstrs[ptbin])
        prelim.DrawLatex( 0.2, 0.926, "CMS Simulation" )
        prelim.DrawLatex( 0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
        mg.Add( massres )

        if 'softdrop' not in options.hist : 
            resc.Print("fits3d/mreco_mgen_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".png", "png")
            resc.Print("fits3d/mreco_mgen_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".pdf", "pdf")
        else :
            resc.Print("fits3d/mreco_mgen_pt_" + str(ptbin) +"_groomed" + options.postfix + ".png", "png")
            resc.Print("fits3d/mreco_mgen_pt_" + str(ptbin) +"_groomed" + options.postfix + ".pdf", "pdf")




        ##### Plot the jet mass resolution and uncertainty.
        resc2 = ROOT.TCanvas("resc2_" +str(ihist) + "_" + str(ptbin), "resc2_" + str(ptbin) )
        massres2 = ROOT.TGraphErrors( len(graphX), graphX, graphDY, graphDX, graphdDY )
        massres2.SetName("massres2_" + str(ptbin))
        if 'softdrop' not in options.hist : 
            massres2.SetTitle(";Ungroomed jet mass (GeV);JMR")
        else :
            massres2.SetTitle(";Groomed jet mass (GeV);JMR")
        leg2.AddEntry( massres2, ptquickstrs[ptbin], "l" )
        massres2.SetLineColor(colors[ptbin])
        massres2.SetLineWidth(2)
        massres2.SetLineStyle(styles[ptbin])

        massres2.Draw("ALX")
        resc2.SetLogx()
        resc2.SetLogy()
        massres2.SetMinimum(1e-3)
        #massres2.SetMaximum(2.0)
        #massres2.SetMinimum(0.0)
        graphs.append(massres2)
        resc2.Draw()
        resc2.Update()
        canvs.append(resc2)
        rg.Add(massres2)
        prelim.Draw()
        tlx.DrawLatex ( 0.6, 0.830, ptbinstrs[ptbin])
        prelim.DrawLatex( 0.2, 0.926, "CMS Simulation" )
        prelim.DrawLatex( 0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
        
        if 'softdrop' not in options.hist : 
            resc2.Print("fits3d/mreco_mgen_jmr_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".png", "png")
            resc2.Print("fits3d/mreco_mgen_jmr_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".pdf", "pdf")
        else :
            resc2.Print("fits3d/mreco_mgen_jmr_pt_" + str(ptbin) +"_groomed" + options.postfix + ".png", "png")
            resc2.Print("fits3d/mreco_mgen_jmr_pt_" + str(ptbin) +"_groomed" + options.postfix + ".pdf", "pdf")



        ##### Plot the relative uncertainty on the jet mass scale.
        resc3 = ROOT.TCanvas("resc3_" +str(ihist) + "_" + str(ptbin), "resc3_" + str(ptbin) )
        fracunc = array.array( 'd', [ graphdY[igrbin] / graphY[igrbin] if graphY[igrbin] > 0.00001 else 0.0 for igrbin in xrange(len(graphY))] )
        
        massres3 = ROOT.TGraph( len(graphX), graphX, fracunc )
        massres3.SetName("massres3_" + str(ptbin))
        if 'softdrop' not in options.hist : 
            massres3.SetTitle(";Ungroomed jet mass (GeV);Uncertainty in JMS")
        else :
            massres3.SetTitle(";Groomed jet mass (GeV);Uncertainty in JMS")
        leg3.AddEntry( massres3, ptquickstrs[ptbin], "l" )
        massres3.SetLineColor(colors[ptbin])
        massres3.SetLineWidth(2)
        massres3.SetLineStyle(styles[ptbin])

        massres3.Draw("ALX")
        resc3.SetLogx()
        resc3.SetLogy()
        massres3.SetMinimum(1e-3)
        #massres3.SetMaximum(2.0)
        #massres3.SetMinimum(0.0)
        graphs.append(massres3)
        resc3.Draw()
        resc3.Update()
        canvs.append(resc3)
        line=ROOT.TLine()
        line.SetLineColor(2)
        line.DrawLine(1,0.5,400,0.5)
        lines.append(line)
        #rg.Add(massres3)
        prelim.Draw()
        tlx.DrawLatex ( 0.6, 0.830, ptbinstrs[ptbin])
        prelim.DrawLatex( 0.2, 0.926, "CMS Simulation" )
        prelim.DrawLatex( 0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
        
        if 'softdrop' not in options.hist : 
            resc3.Print("fits3d/mreco_mgen_jmsunc_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".png", "png")
            resc3.Print("fits3d/mreco_mgen_jmsunc_pt_" + str(ptbin) +"_ungroomed" + options.postfix + ".pdf", "pdf")
        else :
            resc3.Print("fits3d/mreco_mgen_jmsunc_pt_" + str(ptbin) +"_groomed" + options.postfix + ".png", "png")
            resc3.Print("fits3d/mreco_mgen_jmsunc_pt_" + str(ptbin) +"_groomed" + options.postfix + ".pdf", "pdf")

            
            
        #prof = hist2D.ProfileX("prof_" + str(ihist) + "_pt" + str(ptbin))
        #prof.SetMarkerStyle(20)
        #prof.Draw("same")
        #c.SetLogx()
        #canvs.append(c)        
        #hists.append(hist2D)
    
            
    totresc.cd()
    mg.Draw("ALX")
    if 'softdrop' not in options.hist :
        print 'UNGROOMED'
        mg.SetTitle(";Ungroomed jet mass (GeV);JMS")
        mg.SetMinimum(0.8)
        mg.SetMaximum(1.8)
        mg.GetXaxis().SetLimits(20., 1000.)
    else :
        mg.SetTitle(";Groomed jet mass (GeV);JMS")
        mg.SetMinimum(0.8)
        mg.SetMaximum(1.8)
        mg.GetXaxis().SetLimits(10., 1000.)
    mg.Draw("ALX")
    totresc.SetLogx()
    mg.GetXaxis().SetMoreLogLabels()
    mg.GetXaxis().SetNoExponent()
    #tlx.DrawLatex ( 0.6, 0.830, ptbinstrs[ptbin])
    prelim.DrawLatex( 0.2, 0.926, "CMS Simulation" )
    prelim.DrawLatex( 0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
    leg.Draw()
    
    totresc.Update()
    totresc.Print("jms" + groomstr + options.postfix + ".png", "png")
    totresc.Print("jms" + groomstr + options.postfix + ".pdf", "pdf")
    totresc.Print("jms" + groomstr + options.postfix + ".root", "root")



    totresc2.cd()
    rg.Draw("ALX")
    if "softdrop" not in options.hist :
        rg.SetTitle(";Ungroomed jet mass (GeV);JMR")
        rg.SetMinimum(0.0)
        rg.SetMaximum(0.3)
        rg.GetXaxis().SetLimits(20., 1000.)
    else : 
        rg.SetTitle(";Groomed jet mass (GeV);JMR")
        rg.SetMinimum(0.0)
        rg.SetMaximum(0.3)        
        rg.GetXaxis().SetLimits(10., 1000.)
    rg.Draw("ALX")
    totresc2.SetLogx()
    #tlx.DrawLatex ( 0.6, 0.830, ptbinstrs[ptbin])
    prelim.DrawLatex( 0.2, 0.926, "CMS Simulation" )
    prelim.DrawLatex( 0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
    leg2.Draw()
    rg.GetXaxis().SetMoreLogLabels()
    rg.GetXaxis().SetNoExponent()
    totresc2.Update()    
    totresc2.Print("jmr" + groomstr + options.postfix + ".png", "png")
    totresc2.Print("jmr" + groomstr + options.postfix + ".pdf", "pdf")
    totresc2.Print("jmr" + groomstr + options.postfix + ".root", "root")

        
print 'Done'
