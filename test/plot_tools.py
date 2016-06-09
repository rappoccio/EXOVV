def plotter(canvas_list, pads_list, data_list, MC_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, softdrop= "", keephists=[]):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./9240.]
    for i, canv in enumerate(canvas_list):
        pads_list[i][0].cd()
        pads_list[i][0].SetLogy()
        data_list[i].UseCurrentStyle()
        MC_list[i].UseCurrentStyle()        
        data_list[i].Scale(scales[i])
        MC_list[i].Scale(scales[i])
        ########################################################################################## Get JER and JES Hists
        hReco = data_list[i]
        nom = jernom_list[i]
        jesUP  = jecup_list[i]
        jeOWN = jecdn_list[i]
        jerUP  = jerup_list[i]
        jerDOWN = jerdn_list[i]
        ########################################################################################## Get JMR hists
        jmrup = jmrup_list[i]
        jmrdn = jmrdn_list[i]
        jmrnom = jmrnom_list[i]
        ########################################################################################## Scale the hists
        jmrup.Scale(scales[i])
        jmrdn.Scale(scales[i])
        jmrnom.Scale(scales[i])
        jesUP.Scale(scales[i])
        jeOWN.Scale(scales[i])
        jerUP.Scale(scales[i])
        jerDOWN.Scale(scales[i])
        nom.Scale(scales[i])
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
            err = sqrt(err1*err1 + sys*sys + sys2*sys2)
            hReco.SetBinError(ibin, err)
        ####################################################################################### Add Jet Mass Resolution Band
        hRecoJMR = hReco.Clone()
        for ibin in xrange(1, hRecoJMR.GetNbinsX()):
            val = float(hRecoJMR.GetBinContent(ibin))
            err1 = float(hRecoJMR.GetBinError(ibin))
            upjmr = float(abs(jmrup.GetBinContent(ibin) - jmrnom.GetBinContent(ibin)))
            downjmr = float(abs(jmrnom.GetBinContent(ibin) - jmrdn.GetBinContent(ibin)))
            sys = float(((upjmr + downjmr)/2.))
            err = sqrt(err1*err1 + sys*sys)
            hRecoJMR.SetBinError(ibin, err)
        ######################################################################################## Add Parton Shower Uncertainties
        hRecoCopy = hRecoJMR.Clone()
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            temp = hRecoCopy.GetBinError(ibin)
            hRecoCopy.SetBinError(ibin, temp + psdif_list[i][ibin-1] )
        ######################################################################################## Add PDF Uncertainties
        hRecoPDF = hRecoCopy.Clone()
        for ibin in xrange(1, hRecoPDF.GetNbinsX()):
            temp = hRecoPDF.GetBinError(ibin)
            hRecoPDF.SetBinError(ibin, temp + pdfdif_list[i][ibin-1])
        ####################################################################################### PDF Drawn Here
        hRecoPDF.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
        hRecoPDF.SetMarkerStyle(20)
        hRecoPDF.SetAxisRange(1e-11, 1, "Y")
        hRecoPDF.SetFillColor(ROOT.kBlue)
        hRecoPDF.Draw("E2 same")
        hRecoPDF.Draw("E same")
        ####################################################################################### PS Drawn Here
        hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
        hRecoCopy.SetMarkerStyle(20)
        hRecoCopy.SetAxisRange(1e-11, 1, "Y")
        hRecoCopy.SetFillColor(ROOT.kGreen)
        hRecoCopy.Draw("E2 same")
        hRecoCopy.Draw("E same")
        ####################################################################################### JMR Drawn Here
        hRecoJMR.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
        hRecoJMR.SetMarkerStyle(20)
        hRecoJMR.SetAxisRange(1e-11, 1, "Y")
        hRecoJMR.SetFillColor(ROOT.kRed)
        hRecoJMR.Draw("E2")
        hRecoJMR.Draw("E same")    
        ####################################################################################### JES and JER Drawn Here
        hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
        hReco.SetMarkerStyle(20)
        hReco.SetAxisRange( 1e-11, 1, "Y")
        hReco.SetFillColor(ROOT.kYellow)
        hReco.Draw("E2 same")
        hReco.Draw("E same")
        keephists.append([hReco, hRecoPDF, hRecoCopy])
        ####################################################################################### Gen Drawn Here
        MC_list[i].SetLineColor(2)
        MC_list[i].Draw( "hist SAME" )
    
        ####################################################################################### Latex Drawn Here
        atlx[i].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
        atlxpt[i].DrawLatex(0.555, 0.559, ptbins[i])
    
        ####################################################################################### Legends Filled
        legends_list[i].AddEntry(MC_list[i], 'Pythia8'+softdrop, 'l')
        legends_list[i].AddEntry(hRecoJMR, 'JMR', 'f')
        legends_list[i].AddEntry(hRecoPDF, 'PDF', 'f')
        legends_list[i].AddEntry(hRecoCopy, 'Parton Shower', 'f')
        legends_list[i].AddEntry(hReco, 'Pythia8 Reco JES+JER+Stat' + softdrop, 'f')
        legends_list[i].Draw()
        ####################################################################################### Hists Cloned and formatted for ratios
        trueCopy = MC_list[i].Clone()
        trueCopy.SetName( trueCopy.GetName() + "_copy")
        
        datcopy = hReco.Clone()
        datcopy.SetName( datcopy.GetName() + "_copy" )
        datcopy.GetYaxis().SetTitle("Theory/Unfolded")
        datcopy.SetTitleOffset(2)
        datcopy.GetYaxis().SetTitleSize(18)
        # this stuff here is parton shower, bad name, ------------------------------------------> NEEDS REFACTORING
        datcopycopy = hRecoCopy.Clone()
        datcopycopy.SetName(hRecoCopy.GetName()+"_copyofcopy")
        datcopycopy.GetYaxis().SetTitle("Theory/Unfolded")
        datcopycopy.GetYaxis().SetTitleOffset(2)
        datcopycopy.GetYaxis().SetTitleSize(18)
        
        datPDF = hRecoPDF.Clone()
        datPDF.SetName(hRecoPDF.GetName()+"_pdfcopy")
        datPDF.GetYaxis().SetTitle("Theory/Unfolded")
        datPDF.GetYaxis().SetTitleOffset(2)
        datPDF.GetYaxis().SetTitleSize(18)
        
        datJMR = hRecoJMR.Clone()
        datJMR.SetName(hRecoJMR.GetName()+"_jmrcopy")
        datJMR.GetYaxis().SetTitle("Theory/Unfolded")
        datJMR.GetYaxis().SetTitleOffset(2)
        datJMR.GetYaxis().SetTitleSize(18)
        ##################################################################################### divide error by bin content and set to unity
        histstokeep.append( [datcopycopy,datcopy,trueCopy, datPDF, datJMR])
        for ibin in xrange(1,datcopy.GetNbinsX()):
            if datcopy.GetBinContent(ibin) > 0: 
                datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
                datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
                datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
                datJMR.SetBinError(ibin, datJMR.GetBinError(ibin)/datJMR.GetBinContent(ibin))
            else:
                datcopy.SetBinError(ibin, 0)
                datcopycopy.SetBinError(ibin, 0)
                datPDF.SetBinError(ibin, 0)
                datJMR.SetBinError(ibin, 0)
            datJMR.SetBinContent(ibin, 1.0)
            datPDF.SetBinContent(ibin, 1.0)
            datcopy.SetBinContent(ibin, 1.0)
            datcopycopy.SetBinContent(ibin, 1.0)
        ########################################################################################################## Take Ratio
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
        ########################################################################################################## change pad and set axis range
        pads_list[i][1].cd()
        trueCopy.SetTitle(";Jet Mass (GeV);Theory/Unfolded")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(2)
        
        datcopy.SetMinimum(0)
        datcopy.SetMaximum(2)
        datcopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopy.SetFillColor(ROOT.kYellow)

        datcopycopy.SetMinimum(0)
        datcopycopy.SetMaximum(2)
        datcopycopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopycopy.SetFillColor(ROOT.kGreen)
        
        datPDF.SetMinimum(0)
        datPDF.SetMaximum(2)
        datPDF.GetYaxis().SetNdivisions(2,4,0,False)
        datPDF.SetFillColor(ROOT.kBlue)
        
        datJMR.SetMinimum(0)
        datJMR.SetMaximum(2)
        datJMR.GetYaxis().SetNdivisions(2,4,0,False)
        datJMR.SetFillColor(ROOT.kRed)

        datcopy.GetYaxis().SetTitle("Theory/Unfolded")
        datcopycopy.GetYaxis().SetTitle("Theory/Unfolded")
        datPDF.GetYaxis().SetTitle("Theory/Unfolded")
        datJMR.GetYaxis().SetTitle("Theory/Unfolded")
        trueCopy.SetLineStyle(2)
        trueCopy.SetLineColor(2)
        
        ######################################################################## Draw and save
        datPDF.Draw('e2')
        datcopycopy.Draw('e2 same')
        datJMR.Draw('e2 same')
        datcopy.Draw('e2 same')
        datcopy.SetMarkerStyle(0)
        trueCopy.Draw("hist same")
        keephists.append([datcopy, datcopycopy, datPDF])
        pads_list[i][0].Update()
        pads_list[i][1].Update()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")


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
