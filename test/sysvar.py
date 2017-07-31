import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt
from plot_tools import unpinch_vals, smooth

import array

ptBinA = array.array('i', [  200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 13000])

mBinA = array.array('d', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])



def minmassbin_ungroomed(ibin) :
    if ptBinA[ibin] < 760:
        return 4
    else :
        return 5

def minmassbin_groomed(ibin) :
    return 3


def plot_vars(canvas_list, data_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, jmsup_list, jmsdn_list, puup_list, pudn_list,ptbins_dict, softdrop= "", keephists=[], jackknifeRMS=False, histname = "Ungroomed "):
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
        ########################################################################################## Get JMS hists
        jmsup = jmsup_list[i]
        jmsdn = jmsdn_list[i]
        ########################################################################################## Get PU hists
        puup = puup_list[i]
        pudn = pudn_list[i]
        ########################################################################################## Scale the hists for Pt bins
        jmrup.Scale(scales[i])
        jmrdn.Scale(scales[i])
        jmrnom.Scale(scales[i])
        jmsup.Scale(scales[i])
        jmsdn.Scale(scales[i])
        jesUP.Scale(scales[i])
        jeOWN.Scale(scales[i])
        jerUP.Scale(scales[i])
        jerDOWN.Scale(scales[i])
        nom.Scale(scales[i])
        puup.Scale(scales[i])
        pudn.Scale(scales[i])

        
        maxbin = hRMS.GetMaximumBin()
        
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
            jmsup.SetBinContent(ibin, jmsup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmsdn.SetBinContent(ibin, jmsdn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

            
            jesUP.SetBinContent(ibin, jesUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jeOWN.SetBinContent(ibin, jeOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerUP.SetBinContent(ibin, jerUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerDOWN.SetBinContent(ibin, jerDOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            nom.SetBinContent(ibin, nom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

        ########################################################################################## Scale the hists for mass bins
        for ibin in xrange(1, hReco.GetNbinsX()):
            puup.SetBinContent(ibin, puup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            pudn.SetBinContent(ibin, pudn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])            
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
        ####################################################################################### Get Jet mass Resolution Band
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

        ####################################################################################### Get Jet mass Resolution Band
        hRecoJMS = hRecoJMR.Clone()
        reset(hRecoJMS)
        for ibin in xrange(1, hRecoJMS.GetNbinsX()):
            val = float(hRecoJMS.GetBinContent(ibin))
            err1 = float(hRecoJMS.GetBinError(ibin))
            upjms = float(abs(jmsup.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjms = float(abs(nom.GetBinContent(ibin) - jmsdn.GetBinContent(ibin)))
            sys = float(((upjms + downjms)/2.))
            err = err1 + sys
            hRecoJMS.SetBinError(ibin, err)
        ####################################################################################### Get Jet mass Resolution Band
        hRecoPU = hRecoJMS.Clone()
        reset(hRecoPU)
        for ibin in xrange(1, hRecoPU.GetNbinsX()):
            val = float(hRecoPU.GetBinContent(ibin))
            err1 = float(hRecoPU.GetBinError(ibin))
            uppu = float(abs(puup.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downpu = float(abs(nom.GetBinContent(ibin) - pudn.GetBinContent(ibin)))
            sys = float(((uppu + downpu)/2.))
            err = err1 + sys
            hRecoPU.SetBinError(ibin, err)
            
        ######################################################################################## Get Parton Shower Uncertainties
        hRecoCopy = hRecoPU.Clone()
        reset(hRecoCopy)
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            hRecoCopy.SetBinError(ibin, (psdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1]) )
        ######################################################################################## Get PDF Uncertainties
        hRecoPDF = hRecoCopy.Clone()
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
                hRecoJMS.SetBinError(ibin, hRecoJMS.GetBinError(ibin)/hRecoJMS.GetBinContent(ibin))
                hRecoPU.SetBinError(ibin, hRecoPU.GetBinError(ibin)/hRecoPU.GetBinContent(ibin))
                hRecoPDF.SetBinError(ibin, hRecoPDF.GetBinError(ibin)/hRecoPDF.GetBinContent(ibin))
            else:
                hRMS.SetBinError(ibin, 0)
                hReco.SetBinError(ibin, 0)
                hRecoCopy.SetBinError(ibin, 0)
                hRecoJMR.SetBinError(ibin, 0)
                hRecoJMS.SetBinError(ibin, 0)
                hRecoPU.SetBinError(ibin, 0)
                hRecoPDF.SetBinError(ibin, 0)
            hRMS.SetBinContent(ibin, 1.0)
            hReco.SetBinContent(ibin, 1.0)
            hRecoCopy.SetBinContent(ibin, 1.0)
            hRecoJMR.SetBinContent(ibin, 1.0)
            hRecoJMS.SetBinContent(ibin, 1.0)
            hRecoPU.SetBinContent(ibin, 1.0)
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
        hRecoJMSup = hRecoJMS.Clone()
        hRecoJMSdn = hRecoJMS.Clone()
        hRecoPDFup = hRecoPDF.Clone()
        hRecoPDFdn = hRecoPDF.Clone()
        hRecoPUup = hRecoPU.Clone()
        hRecoPUdn = hRecoPU.Clone()

        
        for ibin in xrange(1, hRMS.GetNbinsX()):
            hRMSup.SetBinContent(ibin,  (hRMS.GetBinError(ibin) / 2.0) )
            hRMSdn.SetBinContent(ibin,  (hRMS.GetBinError(ibin) / 2.0) )
            hRecoup.SetBinContent(ibin,  (hReco.GetBinError(ibin) / 2.0) )
            hRecodn.SetBinContent(ibin,  (hReco.GetBinError(ibin) / 2.0) )
            hRecoCopyup.SetBinContent(ibin,  (hRecoCopy.GetBinError(ibin) / 2.0) )
            hRecoCopydn.SetBinContent(ibin,  (hRecoCopy.GetBinError(ibin) / 2.0) )
            hRecoJMRup.SetBinContent(ibin,  (hRecoJMR.GetBinError(ibin) / 2.0) )
            hRecoJMRdn.SetBinContent(ibin,  (hRecoJMR.GetBinError(ibin) / 2.0) )
            hRecoJMSup.SetBinContent(ibin,  (hRecoJMS.GetBinError(ibin) / 2.0) )
            hRecoJMSdn.SetBinContent(ibin,  (hRecoJMS.GetBinError(ibin) / 2.0) )
            hRecoPDFup.SetBinContent(ibin,  (hRecoPDF.GetBinError(ibin) / 2.0) )
            hRecoPDFdn.SetBinContent(ibin,  (hRecoPDF.GetBinError(ibin) / 2.0) )
            hRecoPUup.SetBinContent(ibin,  (hRecoPU.GetBinError(ibin) / 2.0) )
            hRecoPUdn.SetBinContent(ibin,  (hRecoPU.GetBinError(ibin) / 2.0) )

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

        hRecoJMSup.SetLineStyle(8)
        hRecoJMSdn.SetLineStyle(8)
        hRecoJMSup.SetLineColor(8)
        hRecoJMSdn.SetLineColor(8)
        hRecoJMSdn.SetLineWidth(3)
        hRecoJMSup.SetLineWidth(3)

        
        hRecoPUup.SetLineStyle(7)
        hRecoPUdn.SetLineStyle(7)
        hRecoPUup.SetLineColor(ROOT.kCyan + 1)
        hRecoPUdn.SetLineColor(ROOT.kCyan + 1)
        hRecoPUdn.SetLineWidth(3)
        hRecoPUup.SetLineWidth(3)

        
        hRecoPDFup.SetLineStyle(6)
        hRecoPDFdn.SetLineStyle(6)
        hRecoPDFup.SetLineColor(ROOT.kOrange+7)
        hRecoPDFdn.SetLineColor(ROOT.kOrange+7)
        hRecoPDFup.SetLineWidth(3)
        hRecoPDFdn.SetLineWidth(3)

        canvas_list[i].cd()
        hRMSup.SetTitle( '' )
        hRMSup.GetYaxis().SetTitle("Fractional Uncertainty")
        hRMSup.GetYaxis().SetTitleSize(30)
        hRMSup.GetYaxis().SetLabelSize(30)
        
        hRMSup.SetTitleSize(30)
        if histname != "Soft Drop ":
            hRMSup.GetXaxis().SetTitle("Jet mass (GeV)")
        else :
            hRMSup.GetXaxis().SetTitle("Groomed jet mass (GeV)")
        hRMSup.SetMinimum(0.0)
        hRMSup.SetMaximum(0.5)

        if histname != "Soft Drop ":
            minmassbin = minmassbin_ungroomed( i )
        else : 
            minmassbin = minmassbin_groomed( i )

        

        hRMSup.SetAxisRange(mBinA[minmassbin], 1000,"X")

        if histname != "Soft Drop " : 
            unpinch_vals( hRMSup, xval=maxbin )
            unpinch_vals( hRMSdn , xval=maxbin )
            unpinch_vals( hRecoup, xval=maxbin )
            unpinch_vals( hRecodn, xval=maxbin )
            unpinch_vals( hRecoCopyup, xval=maxbin )
            unpinch_vals( hRecoCopydn, xval=maxbin )
            unpinch_vals( hRecoJMRup, xval=maxbin )
            unpinch_vals( hRecoJMRdn, xval=maxbin )
            unpinch_vals( hRecoJMSup, xval=maxbin )
            unpinch_vals( hRecoJMSdn, xval=maxbin )            
            unpinch_vals( hRecoPUup, xval=maxbin )
            unpinch_vals( hRecoPUdn, xval=maxbin )
            unpinch_vals( hRecoPDFup, xval=maxbin )
            unpinch_vals( hRecoPDFdn, xval=maxbin )

        bin400 = hRecoCopyup.GetXaxis().FindBin(500.) - 1
        print 'smoothing '
        smooth( hRMSup, delta=2, xmin=bin400 )
        smooth( hRMSdn , delta=2, xmin=bin400 )
        smooth( hRecoup, delta=2, xmin=bin400 )
        smooth( hRecodn, delta=2, xmin=bin400 )
        #print '<<<<<<<------ this is the one we want'
        smooth( hRecoCopyup, delta=2, xmin=bin400 )
        smooth( hRecoCopydn, delta=2, xmin=bin400 )
        smooth( hRecoJMRup, delta=2, xmin=bin400 )
        smooth( hRecoJMRdn, delta=2, xmin=bin400 )
        smooth( hRecoJMSup, delta=2, xmin=bin400 )
        smooth( hRecoJMSdn, delta=2, xmin=bin400 )
        smooth( hRecoPUup, delta=2, xmin=bin400 )
        smooth( hRecoPUdn, delta=2, xmin=bin400 )
        smooth( hRecoPDFup, delta=2, xmin=bin400 )
        smooth( hRecoPDFdn, delta=2, xmin=bin400 )

        smooth( hRMSup, delta=2 )
        smooth( hRMSdn , delta=2 )
        smooth( hRecoup, delta=2 )
        smooth( hRecodn, delta=2 )
        #print '<<<<<<<------ this is the one we want'
        smooth( hRecoCopyup, delta=2 )
        smooth( hRecoCopydn, delta=2 )
        smooth( hRecoJMRup, delta=2 )
        smooth( hRecoJMRdn, delta=2 )
        smooth( hRecoJMSup, delta=2 )
        smooth( hRecoJMSdn, delta=2 )
        smooth( hRecoPUup, delta=2 )
        smooth( hRecoPUdn, delta=2 )
        smooth( hRecoPDFup, delta=2 )
        smooth( hRecoPDFdn, delta=2 )


        

        hRMSup.SetMaximum(1000)
        hRMSup.SetMinimum(1e-4)
        hRMSup.GetXaxis().SetTitleOffset(1.2)
        hRMSup.GetYaxis().SetTitleOffset(1.2)
        hRMSup.GetXaxis().SetNoExponent()
        #hRMSup.GetXaxis().SetMoreLogLabels(True)
        hRMSup.Draw('hist ][')
        #hRMSdn.Draw('hist same')
        hRecoup.Draw('hist same ][')
        #hRecodn.Draw('hist same')
        hRecoCopyup.Draw('hist same ][')
        #hRecoCopydn.Draw('hist same')
        hRecoJMRup.Draw('hist same ][')
        hRecoJMSup.Draw('hist same ][')
        hRecoPUup.Draw('hist same ][')
        #hRecoJMRdn.Draw('hist same')
        hRecoPDFup.Draw('hist same ][')
        #hRecoPDFdn.Draw('hist same')
        ####################################################################################### Legends Filled
        legends_list[i].SetNColumns(3)
        legends_list[i].AddEntry(hRecoJMRup, 'JMR', 'l')
        legends_list[i].AddEntry(hRecoJMSup, 'JMS', 'l')
        legends_list[i].AddEntry(hRecoPUup, 'PU', 'l')
        legends_list[i].AddEntry(hRecoPDFup, 'PDF', 'l')
        legends_list[i].AddEntry(hRecoCopyup, 'Physics Model', 'l')
        legends_list[i].AddEntry(hRecoup, 'JES+JER', 'l')
        legends_list[i].AddEntry(hRMSup, 'MC Stat', 'l')
        legends_list[i].Draw()

        tlx = ROOT.TLatex()
        tlx.SetNDC()
        tlx.SetTextFont(43)
        tlx.SetTextSize(24)

        tlx.DrawLatex(0.15, 0.926, "CMS Preliminary")
        tlx.DrawLatex(0.69, 0.926, "2.3 fb^{-1} (13 TeV)")

        tlx2 = ROOT.TLatex()
        tlx2.SetNDC()
        tlx2.SetTextFont(63)
        tlx2.SetTextSize(20)
        tlx2.DrawLatex(0.22, 0.830, histname + ptbins_dict[i])

        
        canvas_list[i].Draw()
        canvas_list[i].SetLogy()
        canvas_list[i].SetLogx()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")
        canvas_list[i].SaveAs(outname_str + str(i) + ".pdf")

def reset(histogram):
    for ibin in xrange(1, histogram.GetNbinsX()):
        histogram.SetBinError(ibin, 0)
