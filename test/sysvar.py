import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt

def plot_vars(canvas_list, data_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, ptbins_dict, softdrop= "", keephists=[], jackknifeRMS=False, histname = "Ungroomed "):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]

    for i, canv in enumerate(canvas_list):
        data_list[i].UseCurrentStyle()
        data_list[i].Scale(scales[i])
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
        reset(hReco)
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
        ########################################################################################## Get JER and JES Uncertainties
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
        ####################################################################################### Get Jet Mass Resolution Band
        hRecoJMR = hReco.Clone()
        reset(hRecoJMR)
        for ibin in xrange(1, hRecoJMR.GetNbinsX()):
            val = float(hRecoJMR.GetBinContent(ibin))
            err1 = float(hRecoJMR.GetBinError(ibin))
            upjmr = float(abs(jmrup.GetBinContent(ibin) - jmrnom.GetBinContent(ibin)))
            downjmr = float(abs(jmrnom.GetBinContent(ibin) - jmrdn.GetBinContent(ibin)))
            sys = float(((upjmr + downjmr)/2.))
            err = err1 + sys
            hRecoJMR.SetBinError(ibin, err)
        ######################################################################################## Get Parton Shower Uncertainties
        hRecoCopy = hRecoJMR.Clone()
        reset(hRecoCopy)
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            hRecoCopy.SetBinError(ibin, (psdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1]) )
        ######################################################################################## Get PDF Uncertainties
        hRecoPDF = hRecoJMR.Clone()
        reset(hRecoPDF)
        for ibin in xrange(1, hRecoPDF.GetNbinsX()):
            hRecoPDF.SetBinError(ibin, (pdfdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1] ) )

        ##################################################################################### divide error by bin content and set to unity
        for ibin in xrange(1,hRMS.GetNbinsX()):
            if hRMS.GetBinContent(ibin) > 0: 
                hRMS.SetBinError(ibin, hRMS.GetBinError(ibin)/hRMS.GetBinContent(ibin))
                hReco.SetBinError(ibin, hReco.GetBinError(ibin)/hReco.GetBinContent(ibin))
                hRecoCopy.SetBinError(ibin, hRecoCopy.GetBinError(ibin)/hRecoCopy.GetBinContent(ibin))
                hRecoJMR.SetBinError(ibin, hRecoJMR.GetBinError(ibin)/hRecoJMR.GetBinContent(ibin))
                hRecoPDF.SetBinError(ibin, hRecoPDF.GetBinError(ibin)/hRecoPDF.GetBinContent(ibin))
            else:
                hRMS.SetBinError(ibin, 0)
                hReco.SetBinError(ibin, 0)
                hRecoCopy.SetBinError(ibin, 0)
                hRecoJMR.SetBinError(ibin, 0)
                hRecoPDF.SetBinError(ibin, 0)
            hRMS.SetBinContent(ibin, 1.0)
            hReco.SetBinContent(ibin, 1.0)
            hRecoCopy.SetBinContent(ibin, 1.0)
            hRecoJMR.SetBinContent(ibin, 1.0)
            hRecoPDF.SetBinContent(ibin, 1.0)

        ######################################################################## Clone em all
        hRMSup = hRMS.Clone()
        hRMSdn = hRMS.Clone()
        hRecoup = hReco.Clone()
        hRecodn = hReco.Clone()
        hRecoCopyup = hRecoCopy.Clone()
        hRecoCopydn = hRecoCopy.Clone()
        hRecoJMRup = hRecoJMR.Clone()
        hRecoJMRdn = hRecoJMR.Clone()
        hRecoPDFup = hRecoPDF.Clone()
        hRecoPDFdn = hRecoPDF.Clone()

        for ibin in xrange(1, hRMS.GetNbinsX()):
            hRMSup.SetBinContent(ibin, 1 + (hRMS.GetBinError(ibin) / 2.0) )
            hRMSdn.SetBinContent(ibin, 1 - (hRMS.GetBinError(ibin) / 2.0) )
            hRecoup.SetBinContent(ibin, 1 + (hReco.GetBinError(ibin) / 2.0) )
            hRecodn.SetBinContent(ibin, 1 - (hReco.GetBinError(ibin) / 2.0) )
            hRecoCopyup.SetBinContent(ibin, 1 + (hRecoCopy.GetBinError(ibin) / 2.0) )
            hRecoCopydn.SetBinContent(ibin, 1 - (hRecoCopy.GetBinError(ibin) / 2.0) )
            hRecoJMRup.SetBinContent(ibin, 1 + (hRecoJMR.GetBinError(ibin) / 2.0) )
            hRecoJMRdn.SetBinContent(ibin, 1 - (hRecoJMR.GetBinError(ibin) / 2.0) )
            hRecoPDFup.SetBinContent(ibin, 1 + (hRecoPDF.GetBinError(ibin) / 2.0) )
            hRecoPDFdn.SetBinContent(ibin, 1 - (hRecoPDF.GetBinError(ibin) / 2.0) )

        ######################################################################## Format, Draw, and save

        hRMSup.SetLineStyle(2)
        hRMSdn.SetLineStyle(2)
        hRMSup.SetLineColor(1)
        hRMSdn.SetLineWidth(3)
        hRMSdn.SetLineColor(1)
        hRMSup.SetLineWidth(3)
        hRMSup.GetXaxis().SetTitleSize(30)
        hRMSup.GetXaxis().SetTitleOffset(.72)
        hRMSup.GetYaxis().SetLabelSize(10)


        hRecoup.SetLineStyle(3)
        hRecodn.SetLineStyle(3)
        hRecoup.SetLineColor(2)
        hRecodn.SetLineColor(2)
        hRecoup.SetLineWidth(3)
        hRecodn.SetLineWidth(3)

        hRecoCopyup.SetLineStyle(4)
        hRecoCopydn.SetLineStyle(4)
        hRecoCopyup.SetLineColor(ROOT.kGreen+2)
        hRecoCopydn.SetLineColor(ROOT.kGreen+2)
        hRecoCopyup.SetLineWidth(3)
        hRecoCopydn.SetLineWidth(3)

        hRecoJMRup.SetLineStyle(5)
        hRecoJMRdn.SetLineStyle(5)
        hRecoJMRup.SetLineColor(4)
        hRecoJMRdn.SetLineColor(4)
        hRecoJMRdn.SetLineWidth(3)
        hRecoJMRup.SetLineWidth(3)

        hRecoPDFup.SetLineStyle(6)
        hRecoPDFdn.SetLineStyle(6)
        hRecoPDFup.SetLineColor(6)
        hRecoPDFdn.SetLineColor(6)
        hRecoPDFup.SetLineWidth(3)
        hRecoPDFdn.SetLineWidth(3)

        canvas_list[i].cd()
        hRMSup.GetYaxis().SetTitle("Variation")
        hRMSup.GetYaxis().SetTitleSize(30)
        hRMSup.GetYaxis().SetLabelSize(30)
        hRMSup.SetTitle( histname + "Uncertainty Variations Unfolded for " +ptbins_dict[i] )
        hRMSup.SetTitleSize(30)
        hRMSup.GetXaxis().SetTitle("Jet Mass (GeV)")
        hRMSup.SetMinimum(0.0)
        hRMSup.SetMaximum(2.0)
        if i == 18:
            hRMSup.SetAxisRange(1, 1900,"X")
        elif i >= 15 and i < 18:
            hRMSup.SetAxisRange(1, 1000, "X")
        elif i >= 11 and i < 15:
            hRMSup.SetAxisRange(1, 900, "X")
        elif i >= 9 and i < 11:
            hRMSup.SetAxisRange(1, 800, "X")
        elif i >= 7 and i < 9:
            hRMSup.SetAxisRange(1, 700, "X")
        elif i >= 6 and i < 7:
            hRMSup.SetAxisRange(1, 600, "X")
        elif i >= 5 and i < 6:
            hRMSup.SetAxisRange(1, 500, "X")
        elif i >= 3 and i < 5:
            hRMSup.SetAxisRange(1, 400, "X")
        elif i >= 2 and i < 3 :
            hRMSup.SetAxisRange(1, 300,"X")
        elif i < 2:
            hRMSup.SetAxisRange(1, 200,"X")
        hRMSup.Draw('hist')
        hRMSdn.Draw('hist same')
        hRecoup.Draw('hist same')
        hRecodn.Draw('hist same')
        hRecoCopyup.Draw('hist same')
        hRecoCopydn.Draw('hist same')
        hRecoJMRup.Draw('hist same')
        hRecoJMRdn.Draw('hist same')
        hRecoPDFup.Draw('hist same')
        hRecoPDFdn.Draw('hist same')
        ####################################################################################### Legends Filled
        legends_list[i].AddEntry(hRecoJMRup, 'JMR', 'l')
        legends_list[i].AddEntry(hRecoPDFup, 'PDF', 'l')
        legends_list[i].AddEntry(hRecoCopyup, 'Parton Shower', 'l')
        legends_list[i].AddEntry(hRecoup, 'JES+JER', 'l')
        legends_list[i].AddEntry(hRMSup, 'Stat', 'l')
        legends_list[i].Draw()

        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")
        canvas_list[i].SaveAs(outname_str + str(i) + ".pdf")

def reset(histogram):
    for ibin in xrange(1, histogram.GetNbinsX()):
        histogram.SetBinError(ibin, 0)