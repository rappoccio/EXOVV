#from ROOT import *
import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt
from plot_tools import plotter, setup
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

setup(datacanvases, pads)
setup(datacanvasesSD, padsSD)

histstokeep = []

plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldedclosure_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, ptbins, keephists=histstokeep)
plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldedclosure_softdrop_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, ptbins, softdrop="MMDT Beta=0", keephists=histstokeep)
