import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt

def get_ptbins():
    return ['#bf{p_{T} 200-260 GeV}','#bf{p_{T} 260-350 GeV}','#bf{p_{T} 350-460 GeV}','#bf{p_{T} 460-550 GeV}','#bf{p_{T} 550-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} 760-900 GeV}', '#bf{p_{T} 900-1000 GeV}', '#bf{p_{T} 1000-1100 GeV}','#bf{p_{T} 1100-1200 GeV}',
    '#bf{p_{T} 1200-1300 GeV}', '#bf{p_{T} 1300-1400 GeV}', '#bf{p_{T} 1400-1500 GeV}', '#bf{p_{T} 1500-1600 GeV}', '#bf{p_{T} 1600-1700 GeV}', '#bf{p_{T} 1700-1800 GeV}', '#bf{p_{T} 1800-1900 GeV}', '#bf{p_{T} 1900-2000 GeV}', '#bf{p_{T} > 2000 GeV}']

def plotter(canvas_list, pads_list, data_list, MC_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, latex_list, latexpt_list, ptbins_dict, softdrop= "", keephists=[], jackknifeRMS=False):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    theoryfile = ROOT.TFile("theory_predictions.root")
    theorylist = []
    for h in xrange(0, 18):
        theorylist.append( theoryfile.Get("histSD1_"+str(h)))
    for i, canv in enumerate(canvas_list):
        pads_list[i][0].cd()
        pads_list[i][0].SetLogy()
        data_list[i].UseCurrentStyle()
        MC_list[i].UseCurrentStyle()
        data_list[i].Scale(scales[i])
        MC_list[i].Scale(scales[i])
        ########################################################################################## Get JER and JES Hists
        hRMS = data_list[i]
        nom = jernom_list[i]
        jesUP  = jecup_list[i]
        jeOWN = jecdn_list[i]
        jerUP  = jerup_list[i]
        jerDOWN = jerdn_list[i]
        ########################################################################################## Get JMR hists
        jmrup = jmrup_list[i]
        jmrdn = jmrdn_list[i]
        jmrnom = jmrnom_list[i]
        ########################################################################################## Scale the hists for Pt bins
        jmrup.Scale(scales[i])
        jmrdn.Scale(scales[i])
        jmrnom.Scale(scales[i])
        jesUP.Scale(scales[i])
        jeOWN.Scale(scales[i])
        jerUP.Scale(scales[i])
        jerDOWN.Scale(scales[i])
        nom.Scale(scales[i])
        for ibin in xrange(1, hRMS.GetNbinsX()):
            hRMS.SetBinContent(ibin, hRMS.GetBinContent(ibin) * 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, hRMS.GetBinError(ibin) * 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, hRMS.GetBinError(ibin) + ((jackknifeRMS[i][ibin-1])*scales[i]*(1./mbinwidths[ibin-1]) ) )
        hReco = hRMS.Clone()
        ########################################################################################## Scale the hists for mass bins
        for ibin in xrange(1, hReco.GetNbinsX()):
            jmrup.SetBinContent(ibin, jmrup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrdn.SetBinContent(ibin, jmrdn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrnom.SetBinContent(ibin, jmrnom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

            jesUP.SetBinContent(ibin, jesUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jeOWN.SetBinContent(ibin, jeOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerUP.SetBinContent(ibin, jerUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerDOWN.SetBinContent(ibin, jerDOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            nom.SetBinContent(ibin, nom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            MC_list[i].SetBinContent(ibin, MC_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
        ########################################################################################## Add JER and JES Uncertainties
        for ibin in xrange(1,hReco.GetNbinsX()):
            val = float(hReco.GetBinContent(ibin))
            err1 = float(hReco.GetBinError(ibin))
            upjes = float(abs(jesUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjes = float(abs(nom.GetBinContent(ibin) - jeOWN.GetBinContent(ibin)))
            sys = float(((upjes + downjes)/2.))
            upjer = float(abs(jerUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjer = float(abs(nom.GetBinContent(ibin) - jerDOWN.GetBinContent(ibin)))
            sys2 = float(((upjer + downjer )/2.))
            err = sqrt(sys*sys + sys2*sys2) + err1  
            hReco.SetBinError(ibin, err)
        ####################################################################################### Add Jet Mass Resolution Band
        hRecoJMR = hReco.Clone()
        for ibin in xrange(1, hRecoJMR.GetNbinsX()):
            val = float(hRecoJMR.GetBinContent(ibin))
            err1 = float(hRecoJMR.GetBinError(ibin))
            upjmr = float(abs(jmrup.GetBinContent(ibin) - jmrnom.GetBinContent(ibin)))
            downjmr = float(abs(jmrnom.GetBinContent(ibin) - jmrdn.GetBinContent(ibin)))
            sys = float(((upjmr + downjmr)/2.))
            err = err1 + sys
            hRecoJMR.SetBinError(ibin, err)
        ######################################################################################## Add Parton Shower Uncertainties
        hRecoCopy = hRecoJMR.Clone()
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            temp = hRecoCopy.GetBinError(ibin)
            hRecoCopy.SetBinError(ibin, temp + (psdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1]) )
        ######################################################################################## Add PDF Uncertainties
        hRecoPDF = hRecoJMR.Clone()
        for ibin in xrange(1, hRecoPDF.GetNbinsX()):
            temp = hRecoPDF.GetBinError(ibin)
            hRecoPDF.SetBinError(ibin, temp + (pdfdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1] ) )
        ####################################################################################### PDF Drawn Here
        hRecoPDF.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
        hRecoPDF.GetYaxis().SetTitleSize(30)
        hRecoPDF.GetYaxis().SetTitleOffset(1.0)
        hRecoPDF.GetYaxis().SetLabelOffset(0.0001)
        hRecoPDF.GetYaxis().SetLabelSize(20)
        hRecoPDF.SetMarkerStyle(20)
        hRecoPDF.SetFillColor(ROOT.kOrange+1)
        hRecoPDF.Scale(1.0/hRecoPDF.Integral())
        hRecoPDF.SetAxisRange(1e-5, 1, 'Y')
        hRecoPDF.Draw("E2")
        #hRecoPDF.Draw("E same")
        ####################################################################################### PS Drawn Here
        hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
        hRecoCopy.GetYaxis().SetTitleSize(30)
        hRecoCopy.GetYaxis().SetTitleOffset(1.0)
        hRecoCopy.GetYaxis().SetLabelOffset(0.0001)
        hRecoCopy.GetYaxis().SetLabelSize(20)
        hRecoCopy.SetMarkerStyle(20)
        hRecoCopy.Scale(1.0/hRecoCopy.Integral())
        hRecoCopy.SetAxisRange(1e-5, 1, 'Y')
        hRecoCopy.SetFillColor(ROOT.kAzure+2)
        hRecoCopy.Draw("E2 same")
        #hRecoCopy.Draw("E same")
        ####################################################################################### JMR Drawn Here
        hRecoJMR.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
        hRecoJMR.GetYaxis().SetTitleSize(30)
        hRecoJMR.GetYaxis().SetTitleOffset(1.0)
        hRecoJMR.GetYaxis().SetLabelOffset(0.0001)
        hRecoJMR.GetYaxis().SetLabelSize(20)
        hRecoJMR.SetMarkerStyle(20)
        hRecoJMR.Scale(1.0/hRecoJMR.Integral())
        hRecoJMR.SetAxisRange(1e-5, 1, 'Y')
        hRecoJMR.SetFillColor(ROOT.kGreen)
        hRecoJMR.Draw("E2 same")
        #hRecoJMR.Draw("E same")    
        ####################################################################################### JES and JER Drawn Here
        hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
        hReco.GetYaxis().SetTitleSize(30)
        hReco.GetYaxis().SetTitleOffset(1.0)
        hReco.GetYaxis().SetLabelOffset(0.0001)
        hReco.GetYaxis().SetLabelSize(20)
        hReco.SetMarkerStyle(20)
        hReco.SetFillColor(ROOT.kYellow)
        hReco.Scale(1.0/hReco.Integral())
        hReco.SetAxisRange( 1e-5, 1, 'Y')
        hReco.Draw("E2 same")
        hReco.Draw("E same")
        keephists.append([hReco, hRecoPDF])
        ####################################################################################### Stat Drawn Here
        hRMS.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
        hRMS.GetYaxis().SetTitleSize(30)
        hRMS.GetYaxis().SetTitleOffset(1.0)
        hRMS.GetYaxis().SetLabelOffset(0.0001)
        hRMS.GetYaxis().SetLabelSize(20)
        hRMS.SetMarkerStyle(20)
        hRMS.SetFillColor(ROOT.kMagenta + 2)
        hRMS.Scale(1.0/hRMS.Integral())
        hRMS.SetAxisRange( 1e-5, 1, 'Y')
        hRMS.Draw("E2 same")
        hRMS.Draw("E same")
        keephists.append(hRMS)
        
        ####################################################################################### Gen Drawn Here
        MC_list[i].SetLineColor(2)
        MC_list[i].SetLineWidth(3)
        MC_list[i].Scale(1.0/MC_list[i].Integral())
        MC_list[i].SetAxisRange(1e-5, 1, 'Y')
        MC_list[i].Draw( "hist SAME" )
    
        ####################################################################################### Latex Drawn Here
        latex_list[i].DrawLatex(0.131, 0.926, "CMS preliminary, 2.3 fb^{-1} (13 TeV)")
        latexpt_list[i].DrawLatex(0.250, 0.820, ptbins_dict[i])
    
        ####################################################################################### Legends Filled
        legends_list[i].AddEntry(MC_list[i], 'Pythia8'+softdrop, 'l')
        legends_list[i].AddEntry(hRecoJMR, 'JMR', 'f')
        legends_list[i].AddEntry(hRecoPDF, 'PDF', 'f')
        legends_list[i].AddEntry(hRecoCopy, 'Parton Shower', 'f')
        legends_list[i].AddEntry(hReco, 'JES+JER', 'f')
        legends_list[i].AddEntry(hRMS, 'Stat', 'f')
        legends_list[i].Draw()
        if i < 18:
            theory = theorylist[i]
            theory.Scale(1.0/theory.Integral())
            #theory.Scale(scales[i])
            theory.SetLineColor(8)
            theory.SetLineWidth(3)
            theory.SetAxisRange(1e-5, 1, "Y")
            theory.Draw("hist same")
            legends_list[i].AddEntry(theory, 'Theory Prediction', 'l')
            legends_list[i].Draw("same")
        ####################################################################################### Hists Cloned and formatted for ratios
        trueCopy = MC_list[i].Clone()
        trueCopy.SetName( trueCopy.GetName() + "_copy")
        
        datcopy = hReco.Clone()
        datcopy.SetName( datcopy.GetName() + "_copy" )
        datcopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datcopy.GetYaxis().SetTitleOffset(1.0)
        datcopy.GetYaxis().SetTitleSize(30)
        datcopy.SetMarkerStyle(0)
        # this stuff here is parton shower, bad name, ------------------------------------------> NEEDS REFACTORING
        datcopycopy = hRecoCopy.Clone()
        datcopycopy.SetName(hRecoCopy.GetName()+"_copyofcopy")
        datcopycopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datcopycopy.GetYaxis().SetTitleOffset(1.0)
        datcopycopy.GetYaxis().SetLabelOffset(0.0001)
        datcopycopy.GetYaxis().SetTitleSize(30)
        datcopycopy.SetMarkerStyle(0)
        
        datPDF = hRecoPDF.Clone()
        datPDF.SetName(hRecoPDF.GetName()+"_pdfcopy")
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datPDF.GetYaxis().SetTitleOffset(1.0)
        datPDF.GetYaxis().SetLabelOffset(0.0001)
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.SetMarkerStyle(0)
        
        datJMR = hRecoJMR.Clone()
        datJMR.SetName(hRecoJMR.GetName()+"_jmrcopy")
        datJMR.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datJMR.GetYaxis().SetTitleOffset(1.0)
        datJMR.GetYaxis().SetLabelOffset(0.0001)
        datJMR.GetYaxis().SetTitleSize(30)
        datJMR.SetMarkerStyle(0)

        datRMS = hRMS.Clone()
        datRMS.SetName(hRecoJMR.GetName()+"_jmrcopy")
        datRMS.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datRMS.GetYaxis().SetTitleOffset(1.0)
        datRMS.GetYaxis().SetLabelOffset(0.0001)
        datRMS.GetYaxis().SetTitleSize(30)
        datRMS.SetMarkerStyle(0)
        
        ##################################################################################### divide error by bin content and set to unity
        keephists.append( [datcopy,trueCopy, datPDF, datJMR])
        for ibin in xrange(1,datcopy.GetNbinsX()):
            if datcopy.GetBinContent(ibin) > 0: 
                datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
                datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
                datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
                datJMR.SetBinError(ibin, datJMR.GetBinError(ibin)/datJMR.GetBinContent(ibin))
                datRMS.SetBinError(ibin, datRMS.GetBinError(ibin)/datRMS.GetBinContent(ibin))
            else:
                datcopy.SetBinError(ibin, 0)
                datcopycopy.SetBinError(ibin, 0)
                datPDF.SetBinError(ibin, 0)
                datJMR.SetBinError(ibin, 0)
                datRMS.SetBinError(ibin, 0)
            datJMR.SetBinContent(ibin, 1.0)
            datPDF.SetBinContent(ibin, 1.0)
            datcopy.SetBinContent(ibin, 1.0)
            datcopycopy.SetBinContent(ibin, 1.0)
            datRMS.SetBinContent(ibin, 1.0)
        ########################################################################################################## Take Ratio
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
        ########################################################################################################## change pad and set axis range
        pads_list[i][1].cd()
        trueCopy.SetTitle(";Jet Mass (GeV);#frac{Theory}{Unfolded }")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(2)
        trueCopy.GetYaxis().SetTitleOffset(1.0)
        
        datcopy.SetMinimum(0)
        datcopy.SetMaximum(2)
        datcopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopy.SetFillColor(ROOT.kYellow)

        datcopycopy.SetMinimum(0)
        datcopycopy.SetMaximum(2)
        datcopycopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopycopy.SetFillColor(ROOT.kAzure+2)
        
        datPDF.SetMinimum(0)
        datPDF.SetMaximum(2)
        datPDF.GetYaxis().SetNdivisions(2,4,0,False)
        datPDF.SetFillColor(ROOT.kOrange+1)
        
        datJMR.SetMinimum(0)
        datJMR.SetMaximum(2)
        datJMR.GetYaxis().SetNdivisions(2,4,0,False)
        datJMR.SetFillColor(ROOT.kGreen)

        datRMS.SetMinimum(0)
        datRMS.SetMaximum(2)
        datRMS.GetYaxis().SetNdivisions(2,4,0,False)
        datRMS.SetFillColor(ROOT.kMagenta+2)

        datcopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datcopy.GetYaxis().SetTitleSize(30)
        datcopy.GetYaxis().SetTitleOffset(1.0)
        datcopy.GetYaxis().SetLabelOffset(0.01)
        datcopy.GetYaxis().SetLabelSize(20)
        datcopy.GetXaxis().SetLabelSize(20)
        datcopycopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datcopycopy.GetYaxis().SetTitleSize(30)
        datcopycopy.GetYaxis().SetTitleOffset(1.0)
        datcopycopy.GetYaxis().SetLabelOffset(0.01)
        datcopycopy.GetYaxis().SetLabelSize(20)
        datcopycopy.GetXaxis().SetLabelSize(20)
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.GetYaxis().SetTitleOffset(1.0)
        datPDF.GetYaxis().SetLabelOffset(0.01)
        datPDF.GetYaxis().SetLabelSize(20)
        datPDF.GetXaxis().SetLabelSize(20)
        datJMR.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datJMR.GetYaxis().SetTitleSize(30)
        datJMR.GetYaxis().SetTitleOffset(1.0)
        datJMR.GetYaxis().SetLabelOffset(0.01)
        datJMR.GetYaxis().SetLabelSize(20)
        datJMR.GetXaxis().SetLabelSize(20)
        datRMS.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        datRMS.GetYaxis().SetTitleSize(30)
        datRMS.GetYaxis().SetTitleOffset(1.0)
        datRMS.GetYaxis().SetLabelOffset(0.01)
        datRMS.GetYaxis().SetLabelSize(20)
        datRMS.GetXaxis().SetLabelSize(20)
        trueCopy.SetLineStyle(2)
        trueCopy.SetLineColor(2)
        trueCopy.SetLineWidth(3)
        
        datcopy.GetXaxis().SetTitleOffset(2.5)
        datcopycopy.GetXaxis().SetTitleOffset(2.5)
        datPDF.GetXaxis().SetTitleOffset(2.5)
        datJMR.GetXaxis().SetTitleOffset(2.5)
        datRMS.GetXaxis().SetTitleOffset(2.5)


        datcopy.GetXaxis().SetTitle("Jet Mass (GeV)")
        datcopycopy.GetXaxis().SetTitle("Jet Mass (GeV)")
        datPDF.GetXaxis().SetTitle("Jet Mass (GeV)")
        datJMR.GetXaxis().SetTitle("Jet Mass (GeV)") 
        datRMS.GetXaxis().SetTitle("Jet Mass (GeV)")


        ######################################################################## Draw and save
        datPDF.Draw('e2') 
        datcopycopy.Draw('e2 same')
        datJMR.Draw('e2 same')
        datcopy.Draw('e2 same')
        datRMS.Draw('e2 same')
        datcopy.SetMarkerStyle(0)
        trueCopy.Draw("hist same")
        keephists.append([datcopy, datPDF])
        pads_list[i][0].Update()
        pads_list[i][0].RedrawAxis()
        pads_list[i][1].Update()
        pads_list[i][1].RedrawAxis()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")
        canvas_list[i].SaveAs(outname_str + str(i) + ".pdf")

def setup(canvases_to_use, pads_to_use):
    for icanv,canv in enumerate ( canvases_to_use ) :
        canv.cd()
        pad1 = ROOT.TPad('pad' + str(icanv) + '1', 'pad' + str(icanv) + '1', 0., 0.3, 1.0, 1.0)
        pad1.SetBottomMargin(0)
        pad2 = ROOT.TPad('pad' + str(icanv) + '2', 'pad' + str(icanv) + '2', 0., 0.0, 1.0, 0.3)
        pad2.SetTopMargin(0)
        pad1.SetLeftMargin(0.15)
        pad2.SetLeftMargin(0.15)
        pad2.SetBottomMargin(0.5)
        pad1.Draw()
        pad2.Draw()
        pads_to_use.append( [pad1,pad2] )

def PlotBias(canvas_list, pads_list, gen_list, reco_list, legends_list, recolegname_str, genlegname_str, outname_str, latex_list, latexpt_list, ptbins_dict):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    for i, canvas in enumerate(canvas_list):
        pads_list[i][0].cd()
        pads_list[i][0].SetLogy()
        for ibin in xrange(1, reco_list[i].GetNbinsX()):
            reco_list[i].SetBinContent(ibin, reco_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin])
            reco_list[i].SetBinError(ibin, reco_list[i].GetBinError(ibin) * 1./mbinwidths[ibin])
            gen_list[i].SetBinContent(ibin, gen_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin])
            gen_list[i].SetBinError(ibin, gen_list[i].GetBinError(ibin) * 1./mbinwidths[ibin])
        reco_list[i].UseCurrentStyle()
        gen_list[i].UseCurrentStyle()
        reco_list[i].Scale(scales[i])
        gen_list[i].Scale(scales[i])
        reco_list[i].SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
        reco_list[i].GetYaxis().SetTitleSize(30)
        reco_list[i].SetLineColor(2)
        reco_list[i].SetAxisRange(1e-11, 1, "Y")
        reco_list[i].SetStats(0)
        reco_list[i].Draw("SAME hist")
        reco_list[i].GetXaxis().SetTitle("Mass (GeV)")
        legends_list[i].AddEntry(reco_list[i], recolegname_str, 'l')
        legends_list[i].AddEntry(gen_list[i], genlegname_str, 'pl')
        legends_list[i].Draw()
        gen_list[i].SetAxisRange(1e-11, 1, "Y")
        gen_list[i].SetMarkerStyle(8)
        #gen_list[i].SetMarkerSize(30)
        gen_list[i].Draw("SAME")
        latex_list[i].DrawLatex(0.131, 0.926, "CMS preliminary, 40 pb^{-1} (13 TeV)")
        latexpt_list[i].DrawLatex(0.200, 0.779, ptbins_dict[i])
        
        recocopy = reco_list[i].Clone()
        recocopy.SetName( recocopy.GetName() + "_copy")
        gencopy = gen_list[i].Clone()
        gencopy.SetName(gencopy.GetName() + "_copy")

        for ibin in xrange(1,recocopy.GetNbinsX()):
            if recocopy.GetBinContent(ibin) > 0: 
                recocopy.SetBinError(ibin, recocopy.GetBinError(ibin)/recocopy.GetBinContent(ibin))
            else:
                recocopy.SetBinError(ibin, 0)
            recocopy.SetBinContent(ibin, 1.0)
        gencopy.Divide(gencopy, reco_list[i], 1.0, 1.0, "B")

        pads_list[i][1].cd()
        gencopy.SetTitle(";Jet Mass (GeV); #frac{Theory}{Unfolded }")
        recocopy.SetMinimum(0)
        recocopy.SetMaximum(2)
        recocopy.GetYaxis().SetNdivisions(2,4,0,False)
        recocopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        recocopy.GetYaxis().SetTitleOffset(1.0)
        recocopy.GetYaxis().SetLabelOffset(0.01)
        recocopy.GetYaxis().SetLabelSize(20)
        recocopy.GetXaxis().SetLabelSize(20)
        recocopy.GetYaxis().SetTitleSize(30)
        recocopy.GetXaxis().SetTitleOffset(2.3)

        gencopy.SetMinimum(0)
        gencopy.SetMaximum(2)
        gencopy.GetYaxis().SetNdivisions(2,4,0,False)
        gencopy.GetYaxis().SetTitle("#frac{Theory}{Unfolded }")
        gencopy.GetYaxis().SetTitleOffset(1.0)
        gencopy.GetYaxis().SetLabelOffset(0.01)
        gencopy.GetYaxis().SetLabelSize(20)
        gencopy.GetXaxis().SetLabelSize(20)
        gencopy.GetYaxis().SetTitleSize(30)
        gencopy.GetXaxis().SetTitleOffset(2.3)
        #gencopy.SetMarkerSize(30)

        recocopy.Draw('SAME')
        gencopy.Draw("hist SAME")
        
        pads_list[i][0].Update()
        pads_list[i][0].RedrawAxis()
        pads_list[i][1].Update()
        pads_list[i][1].RedrawAxis()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str+str(i)+".png")
