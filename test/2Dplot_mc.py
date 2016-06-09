#from ROOT import *
import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt
from optparse import OptionParser
parser = OptionParser()
                                 
(options, args) = parser.parse_args()

f = ROOT.TFile('2DClosure.root')
parton_shower = ROOT.TFile('PS_hists.root')
pdfs = ROOT.TFile('unfoldedpdf.root')

scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./9240.]


jecdna = []
jecupa = []
jerdna = []
jerupa = []
jernoma = []
jmrdna = []
jmrupa = []
jmrnoma = []


jecdnaSD = []
jecupaSD = []
jerdnaSD = []
jerupaSD = []
jernomaSD = []
jmrdnaSD = []
jmrupaSD = []
jmrnomaSD = []

ps = []
ps_softdrop = []

ps_differences = []
ps_differences_softdrop = []

jecdn = ROOT.TFile('2DClosure_jecdn.root')
jecup = ROOT.TFile('2DClosure_jecup.root')
jerdn = ROOT.TFile('2DClosure_jerdn.root')
jerup = ROOT.TFile('2DClosure_jerup.root')
jernom = ROOT.TFile('2DClosure_jernom.root')
jmrupfile = ROOT.TFile('2DClosure_jmrup.root')
jmrdnfile = ROOT.TFile('2DClosure_jmrdn.root')
jmrnomfile= ROOT.TFile('2DClosure_jmrnom.root')

##################################################################### Get uncertainty hists
for i in range(0, 7):
    jecdna.append(jecdn.Get('pythia8_mass' + str(i)))
    jecupa.append(jecup.Get('pythia8_mass' + str(i)))
    jerdna.append(jerdn.Get('pythia8_mass' + str(i)))
    jerupa.append(jerup.Get('pythia8_mass' + str(i)))
    jernoma.append(jernom.Get('pythia8_mass'+str(i)))
    jmrupa.append(jmrupfile.Get('pythia8_mass' + str(i)))
    jmrdna.append(jmrdnfile.Get('pythia8_mass' + str(i)))
    jmrnoma.append(jmrnomfile.Get('pythia8_mass' + str(i)))

    jecdnaSD.append(jecdn.Get('pythia8_massSD' + str(i)))
    jecupaSD.append(jecup.Get('pythia8_massSD' + str(i)))
    jerdnaSD.append(jerdn.Get('pythia8_massSD' + str(i)))
    jerupaSD.append(jerup.Get('pythia8_massSD' + str(i)))
    jernomaSD.append(jernom.Get('pythia8_massSD'+str(i)))
    jmrupaSD.append(jmrupfile.Get('pythia8_massSD' + str(i)))
    jmrdnaSD.append(jmrdnfile.Get('pythia8_massSD' + str(i)))
    jmrnomaSD.append(jmrnomfile.Get('pythia8_massSD' + str(i)))

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

################################################################################# generate canvases (change to loop to condense)
uc2 = TCanvas("cdist140", "cdist140")
uc3 = TCanvas("cdist200", "cdist200")
uc4 = TCanvas("cdist260", "cdist260")
uc5 = TCanvas("cdist320", "cdist320")
uc6 = TCanvas("cdist400", "cdist400")
uc7 = TCanvas("cdist450", "cdist450")
uc8 = TCanvas("cdist500", "cdist500")

ucsd2 = TCanvas("cdist140SD","cdist140SD")
ucsd3 = TCanvas("cdist200SD","cdist200SD")
ucsd4 = TCanvas("cdist260SD","cdist260SD")
ucsd5 = TCanvas("cdist320SD","cdist320SD")
ucsd6 = TCanvas("cdist400SD","cdist400SD")
ucsd7 = TCanvas("cdist450SD","cdist450SD")
ucsd8 = TCanvas("cdist500SD","cdist500SD")

datacanvasesSD = [ucsd2, ucsd3, ucsd4, ucsd5, ucsd6, ucsd7, ucsd8]
datacanvases= [uc2, uc3, uc4, uc5, uc6, uc7, uc8]



######################################################################################### Get Central Value hists and generate legends etc
datalist = []
datalistSD = []
MCtruth = []
MCtruthSD = []
atlx = []
atlxpt = []
alegends = []
alegendsSD = []
atlxSD = []
atlxSDpt = []
comparisons = []
for x in range(0, 7):
    datalistSD.append(f.Get('pythia8_massSD'+str(x)))
    datalist.append(f.Get('pythia8_mass'+str(x)))
    MCtruth.append(f.Get('genmass' + str(x)))
    MCtruthSD.append(f.Get('genmassSD' + str(x)))
    atlx.append(ROOT.TLatex())
    atlxpt.append(ROOT.TLatex())
    atlxSD.append(ROOT.TLatex())
    atlxSDpt.append(ROOT.TLatex())
    alegends.append(TLegend(.5, .7, .85, .85))
    alegendsSD.append(TLegend(.5, .7, .85, .85))
    datacanvases[x].SetLeftMargin(0.15)
    datacanvasesSD[x].SetLeftMargin(0.15)
################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, 7):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('pythia8_unfolded_by_pythia6'+str(i)))
    ps_softdrop.append(parton_shower.Get('pythia8_unfolded_by_pythia6_softdrop'+str(i)))
      
    temp_unc = (ps[i] - datalist[i])
    temp_softdrop_unc = (ps_softdrop[i] - datalistSD[i])
    temp_unc.Scale(scales[i])
    temp_softdrop_unc.Scale(scales[i])
#take the differences in the bins between the pythia 8 unfolded with pythia 8 and the pythia 8 unfolded with pythia 6
    for ibin in xrange(1,temp_unc.GetNbinsX()):
        temp_diff.append(abs(temp_unc.GetBinContent(ibin)))
        temp_softdrop_diff.append(abs(temp_softdrop_unc.GetBinContent(ibin)))
    ps_differences.append(temp_diff)
    ps_differences_softdrop.append(temp_softdrop_diff)


############################################################################## PDF differences and PDF differences comparisons 
pdf_differences = []
pdf_differences_softdrop = []

pdf_up = []
pdf_dn = []

pdf_upsd = []
pdf_dnsd = []
comparisons_softdrop = []

complegends = []
complegendssd = []

for i in range(0, 7):
#    complegends.append(ROOT.TLegend(.5, .7, .85, .85))
#    complegendssd.append(ROOT.TLegend(.5, .7, .85, .85))
#    comparisons.append(ROOT.TCanvas('comp'+str(i)))
#    comparisons[i].cd()
    temp_pdf_diff = []
    temp_softdrop_pdf_diff = []
    pdf_up.append(pdfs.Get('pdf_up'+str(i)))
    pdf_dn.append(pdfs.Get('pdf_dn'+str(i)))
    pdf_upsd.append(pdfs.Get('pdf_up_softdrop'+str(i)))
    pdf_dnsd.append(pdfs.Get('pdf_dn_softdrop'+str(i)))

#####################################################################
#    pdf_up[i].Draw('hist')
#    pdf_dn[i].SetLineColor(3)
#    pdf_dn[i].Draw('same hist')
#    complegends[i].AddEntry(pdf_up[i], "Ungroomed Up", 'l')
#    complegends[i].AddEntry(pdf_dn[i], "Ungroomed Down", 'l')
#    complegends[i].Draw('same')
#    comparisons[i].SaveAs('ungroomedpdf_comp' + str(i)+'.png')
#    
#    comparisons_softdrop.append(TCanvas('compsd'+str(i)))
#    comparisons_softdrop[i].cd()    
#    pdf_upsd[i].Draw('hist')
#    pdf_dnsd[i].SetLineColor(3)
#    pdf_dnsd[i].Draw('hist same')
#    complegendssd[i].AddEntry(pdf_upsd[i], "SoftDrop Up", 'l')
#    complegendssd[i].AddEntry(pdf_dnsd[i], "SoftDrop Down", 'l')
#    complegendssd[i].Draw('same')
#    comparisons_softdrop[i].SaveAs('softdroppdf_comp'+str(i)+'.png')
#####################################################################  
     
    temp_unc = (pdf_up[i] - pdf_dn[i])
    temp_unc_softdrop = (pdf_upsd[i] - pdf_dnsd[i])
    temp_unc.Scale(scales[i])
    temp_unc_softdrop.Scale(scales[i])
    for ibin in xrange(1, temp_unc.GetNbinsX()):
        temp_pdf_diff.append(abs(temp_unc.GetBinContent(ibin)))
        temp_softdrop_pdf_diff.append(abs(temp_unc_softdrop.GetBinContent(ibin)))
    pdf_differences.append(temp_pdf_diff)
    pdf_differences_softdrop.append(temp_softdrop_pdf_diff)

#    print "ungroomed"
#    print temp_pdf_diff
#    print "softdrop now"
#    print  temp_softdrop_pdf_diff

# Canvases
ptbins = ['#bf{p_{T} 200-260 GeV}','#bf{p_{T} 260-350 GeV}','#bf{p_{T} 350-460 GeV}','#bf{p_{T} 460-550 GeV}','#bf{p_{T} 550-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} >760 GeV}']


pads = []
padsSD = []
hRatioList = []
hRatioListSD = []

for b in atlx:
    b.SetNDC()
    b.SetTextFont(43)
    b.SetTextSize(30)
for b in atlxSD:
    b.SetNDC()
    b.SetTextFont(43)
    b.SetTextSize(30)
for g in atlxpt:
    g.SetNDC()
    g.SetTextFont(43)
    g.SetTextSize(25)
for g in atlxSDpt:
    g.SetNDC()
    g.SetTextFont(43)
    g.SetTextSize(25)
for leg in alegends :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in alegendsSD :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

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

setup(datacanvases, pads)
setup(datacanvasesSD, padsSD)

histstokeep = []

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
    
plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldedclosure_", jmrupa, jmrdna, jmrnoma, keephists=histstokeep)
plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldedclosure_softdrop_", jmrupaSD, jmrdnaSD, jmrnomaSD, softdrop="MMDT Beta=0", keephists=histstokeep)






'''
for i in datacanvases:
    index = datacanvases.index(i)
    pads[index][0].cd()
    pads[index][0].SetLogy()
    datalist[index].UseCurrentStyle()
    MCtruth[index].UseCurrentStyle()
    
    datalist[index].Scale(scales[index])
    MCtruth[index].Scale(scales[index])
    ########################################################################################## Add JER and JES Uncertainties
    hReco = datalist[index]
    nom = datalist[index]
    jesUP  = jecupa[index]
    jesDOWN = jecdna[index]
    jerUP  = jerupa[index]
    jerDOWN = jerdna[index]
    jesUP.Scale(scales[index])
    jesDOWN.Scale(scales[index])
    jerUP.Scale(scales[index])
    jerDOWN.Scale(scales[index])
    for ibin in xrange(1,hReco.GetNbinsX()):
        val = float(hReco.GetBinContent(ibin))
        err1 = float(hReco.GetBinError(ibin))
        upjes = float(abs(jesUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
        downjes = float(abs(nom.GetBinContent(ibin) - jesDOWN.GetBinContent(ibin)))
        sys = float(((upjes + downjes)/2.))
        upjer = float(abs(jerUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
        downjer = float(abs(nom.GetBinContent(ibin) - jerDOWN.GetBinContent(ibin)))
        sys2 = float(((upjer + downjer )/2.))
        err = sqrt(err1*err1 + sys*sys + sys2*sys2)
        hReco.SetBinError(ibin, err)
    ######################################################################################## Add Parton Shower Uncertainties
    hRecoCopy = hReco.Clone()
    for ibin in xrange(1, hRecoCopy.GetNbinsX()):
        temp = hRecoCopy.GetBinError(ibin)
        hRecoCopy.SetBinError(ibin, temp + ps_differences[index][ibin-1] )
    ######################################################################################## Add PDF Uncertainties
    hRecoPDF = hRecoCopy.Clone()
    for ibin in xrange(1, hRecoPDF.GetNbinsX()):
        temp = hRecoPDF.GetBinError(ibin)
        hRecoPDF.SetBinError(ibin, temp + pdf_differences[index][ibin-1])

    ####################################################################################### PDF Drawn Here
    hRecoPDF.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoPDF.SetMarkerStyle(20)
    hRecoPDF.SetAxisRange(1e-11, 1, "Y")
    hRecoPDF.SetFillColor(ROOT.kBlue)
    hRecoPDF.Draw("E2")
    hRecoPDF.Draw("E same")

    ####################################################################################### PS Drawn Here
    hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoCopy.SetMarkerStyle(20)
    hRecoCopy.SetAxisRange(1e-11, 1, "Y")
    hRecoCopy.SetFillColor(ROOT.kGreen)
    hRecoCopy.Draw("E2 same")
    hRecoCopy.Draw("E same")

    ####################################################################################### JES and JER Drawn Here
    hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( 1e-11, 1, "Y")
    hReco.SetFillColor(ROOT.kYellow)
    hReco.Draw("E2 same")
    hReco.Draw("E same")

    ####################################################################################### Gen Drawn Here
    MCtruth[index].SetLineColor(2)
    MCtruth[index].Draw( "hist SAME" )

    ####################################################################################### Latex Drawn Here
    atlx[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
    atlxpt[index].DrawLatex(0.555, 0.559, ptbins[index])

    ################################## legends
    alegends[index].AddEntry(MCtruth[index], 'Pythia8', 'l')
    alegends[index].AddEntry(hRecoPDF, 'PDF', 'f')
    alegends[index].AddEntry(hRecoCopy, 'Parton Shower', 'f')
    alegends[index].AddEntry(hReco, 'Pythia8 Reco JES+JER+Stat', 'f')
    alegends[index].Draw()

    #################################### ratio plot stuff
    trueCopy = MCtruthSD[index].Clone()
    trueCopy.SetName( trueCopy.GetName() + "_copy")
    
    datcopy = hReco.Clone()
    datcopy.SetName( datcopy.GetName() + "_copy" )
    datcopy.GetYaxis().SetTitle("Theory/Unfolded")
    datcopy.SetTitleOffset(2)
    datcopy.GetYaxis().SetTitleSize(18)
    
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
    
    histstokeep.append( [datcopycopy,datcopy,trueCopy])
    for ibin in xrange(1,datcopy.GetNbinsX()):
        if datcopy.GetBinContent(ibin) > 0: 
            datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
            datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
            datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
        else:
            datcopy.SetBinError(ibin, 0)
            datcopycopy.SetBinError(ibin, 0)
            datPDF.SetBinError(ibin, 0)
        datPDF.SetBinContent(ibin, 1.0)
        datcopy.SetBinContent(ibin, 1.0)
        datcopycopy.SetBinContent(ibin, 1.0)
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    pads[index][1].cd()
    trueCopy.SetTitle(";Jet Mass (GeV);Theory/Unfolded")
    trueCopy.UseCurrentStyle()
    trueCopy.GetXaxis().SetTitleOffset(2)
    datcopy.SetMinimum(0)
    datcopy.SetMaximum(2)
    datcopy.GetYaxis().SetNdivisions(2,4,0,False)

    datcopycopy.SetMinimum(0)
    datcopycopy.SetMaximum(2)
    datcopycopy.GetYaxis().SetNdivisions(2,4,0,False)
    datcopycopy.SetFillColor(ROOT.kGreen)
    
    datPDF.SetMinimum(0)
    datPDF.SetMaximum(2)
    datPDF.GetYaxis().SetNdivisions(2,4,0,False)
    datPDF.SetFillColor(ROOT.kBlue)
    
    datcopy.GetYaxis().SetTitle("Theory/Unfolded")
    datcopycopy.GetYaxis().SetTitle("Theory/Unfolded")
    datPDF.GetYaxis().SetTitle("Theory/Unfolded")
    
    trueCopy.SetLineStyle(2)
    trueCopy.SetLineColor(2)
    datcopy.SetFillColor(ROOT.kYellow)
    datPDF.Draw('e2')
    
    datcopycopy.Draw('e2 same')
    
    datcopy.Draw('e2 same')
    datcopy.SetMarkerStyle(0)
    trueCopy.Draw("hist same")
    
    hRatioList.append([trueCopy, datcopy, datcopycopy, datPDF])
    pads[index][0].Update()
    pads[index][1].Update()
    datacanvases[index].Draw()
    datacanvases[index].SaveAs("unfoldedclosure_" + str(index) + ".png")







for i in datacanvasesSD:
    index = datacanvasesSD.index(i)
    padsSD[index][0].cd()
    padsSD[index][0].SetLogy()
    datalistSD[index].UseCurrentStyle()
    MCtruthSD[index].UseCurrentStyle()
    datalistSD[index].Scale(scales[index])
    MCtruthSD[index].Scale(scales[index])
    ################################## Uncertainties
    hReco = datalistSD[index]
    nom = datalistSD[index]
    jesUP  = jecupaSD[index]
    jesDOWN = jecdnaSD[index]
    jerUP  = jerupaSD[index]
    jerDOWN = jerdnaSD[index]
    jesUP.Scale(scales[index])
    jesDOWN.Scale(scales[index])
    jerUP.Scale(scales[index])
    jerDOWN.Scale(scales[index])
    for ibin in xrange(1,hReco.GetNbinsX()):
        val = float(hReco.GetBinContent(ibin))
        err1 = float(hReco.GetBinError(ibin))
        upjes = float(abs(jesUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
        downjes = float(abs(nom.GetBinContent(ibin) - jesDOWN.GetBinContent(ibin)))
        sys = float(((upjes + downjes)/2.))
        upjer = float(abs(jerUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
        downjer = float(abs(nom.GetBinContent(ibin) - jerDOWN.GetBinContent(ibin)))
        sys2 = float(((upjer + downjer )/2.))
        err = sqrt(err1*err1 + sys*sys + sys2*sys2)
        hReco.SetBinError(ibin, err)
    hRecoCopy = hReco.Clone()
    for ibin in xrange(1, hRecoCopy.GetNbinsX()):
        temp = hRecoCopy.GetBinError(ibin)
        hRecoCopy.SetBinError(ibin, temp + ps_differences_softdrop[index][ibin-1] )
    ############################################################################################ Add PDF Uncertainties
    hRecoPDF = hRecoCopy.Clone()
    for ibin in xrange(1, hRecoPDF.GetNbinsX()):
        temp = hRecoPDF.GetBinError(ibin)
        hRecoPDF.SetBinError(ibin, temp + pdf_differences_softdrop[index][ibin-1])

    ############################################################################################ Draw PDFs
    hRecoPDF.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoPDF.SetMarkerStyle(20)
    hRecoPDF.SetAxisRange(1e-11, 1, "Y")
    hRecoPDF.SetFillColor(ROOT.kBlue)
    hRecoPDF.Draw("E2")
    hRecoPDF.Draw("E same")
    ########################################################################################### Draw Parton Shower
    hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoCopy.SetMarkerStyle(20)
    hRecoCopy.SetAxisRange(1e-11, 1, "Y")
    hRecoCopy.SetFillColor(ROOT.kGreen)
    hRecoCopy.Draw("E2 same")
    hRecoCopy.Draw("E same")

    ########################################################################################### Draw JES and JER
    hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{pb}{20GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( 1e-11, 1, "Y")
    hReco.SetFillColor(ROOT.kYellow)
    hReco.Draw("E2 same")
    hReco.Draw("E same")
    ########################################################################################### Draw Gen
    MCtruthSD[index].SetLineColor(2)
    MCtruthSD[index].Draw( "hist SAME" )
    ########################################################################################### Draw Latex
    atlxSD[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
    atlxSDpt[index].DrawLatex(0.555, 0.559, ptbins[index])
    ########################################################################################### Draw legends
    alegendsSD[index].AddEntry(MCtruthSD[index], 'Pythia8 SoftDrop', 'l')
    alegendsSD[index].AddEntry(hRecoPDF, 'PDF', 'f')
    alegendsSD[index].AddEntry(hRecoCopy, 'Parton Shower', 'f')
    alegendsSD[index].AddEntry(hReco, 'Pythia8 Reco JES+JER+Stat-MMDT Beta = 0', 'f')
    alegendsSD[index].Draw()
    #################################### ratio plot stuff
    trueCopy = MCtruthSD[index].Clone()
    trueCopy.SetName( trueCopy.GetName() + "_copy")
    
    datcopy = hReco.Clone()
    datcopy.SetName( datcopy.GetName() + "_copy" )
    datcopy.GetYaxis().SetTitle("Theory/Unfolded")
    datcopy.SetTitleOffset(2)
    datcopy.GetYaxis().SetTitleSize(18)
    
    datcopycopy = hRecoCopy.Clone()
    datcopycopy.SetName(hRecoCopy.GetName()+"_copyofcopy")
    datcopycopy.GetYaxis().SetTitle("Theory/Unfolded")
    datcopycopy.GetYaxis().SetTitleOffset(2)
    datcopycopy.GetYaxis().SetTitleSize(18)
    
    datPDF = hRecoPDF.Clone()
    datPDF.SetName(datPDF.GetName() + '_pdfcopy')
    datPDF.GetYaxis().SetTitle('Theory/Unfolded')
    datPDF.GetYaxis().SetTitleOffset(2)
    datPDF.GetYaxis().SetTitleSize(18)
    
    histstokeep.append( [datcopycopy,datcopy,trueCopy,datPDF])
    for ibin in xrange(1,datcopy.GetNbinsX()):
        if datcopy.GetBinContent(ibin) > 0: 
            datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
            datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
            datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
        else:
            datcopy.SetBinError(ibin, 0)
            datcopycopy.SetBinError(ibin, 0)
            datPDF.SetBinError(ibin, 0)
        
        datPDF.SetBinContent(ibin, 1.0)
        datcopy.SetBinContent(ibin, 1.0)
        datcopycopy.SetBinContent(ibin, 1.0)
        
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    padsSD[index][1].cd()
    trueCopy.SetTitle(";Jet Mass (GeV);Theory/Unfolded")
    trueCopy.UseCurrentStyle()
    trueCopy.GetXaxis().SetTitleOffset(3)
    
    datcopy.SetMinimum(0)
    datcopy.SetMaximum(2)
    datcopy.GetYaxis().SetNdivisions(2,4,0,False)
    
    datcopycopy.SetMinimum(0)
    datcopycopy.SetMaximum(2)
    datcopycopy.GetYaxis().SetNdivisions(2,4,0,False)
    datcopycopy.SetFillColor(ROOT.kGreen)
    
    datPDF.SetMinimum(0)
    datPDF.SetMaximum(2)
    datPDF.GetYaxis().SetNdivisions(2,4,0,False)
    
    trueCopy.SetLineStyle(2)
    trueCopy.SetLineColor(2)
    datcopy.SetFillColor(ROOT.kYellow)

    datcopy.SetMarkerStyle(0)
    
    datPDF.Draw('e2')
    datcopycopy.Draw('e2 same')
    datcopy.Draw('e2 same')
    trueCopy.Draw("hist same")    
    hRatioListSD.append([trueCopy, datcopy, datcopycopy, datPDF])
    padsSD[index][0].Update()
    padsSD[index][1].Update()
    datacanvasesSD[index].Draw()
    datacanvasesSD[index].SaveAs("unfoldedclosure_softdrop_" + str(index) + ".png")
'''