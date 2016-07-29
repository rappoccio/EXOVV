#from ROOT import *
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import plotter, setup, get_ptbins, plot_OneBand
from optparse import OptionParser
import pickle
parser = OptionParser()
                                 



parser.add_option('--oneband', action='store_true',
                  default = False,
                  dest='oneband',
                  help='one band plots')


parser.add_option('--isSoftDrop', action='store_true',
                  default = False,
                  dest='isSoftDrop',
                  help='theory curves on plots')


(options, args) = parser.parse_args()

f = ROOT.TFile('2DData.root')
parton_shower = ROOT.TFile('PS_hists.root')
pdfs = ROOT.TFile('unfoldedpdf.root')


scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]

##### WARNING ### WARNING #####<----------------------------------------------
### This version of pickle  ###<----------------------------------------------
### is not secure. NEVER use###<----------------------------------------------
### it to open binary files ###<----------------------------------------------
### that you did not create ###<----------------------------------------------
###############################<----------------------------------------------
RMS_vals = pickle.load(open("ungroomeddataJackKnifeRMS.p", "rb"))         ########
RMS_vals_softdrop = pickle.load(open("softdropdataJackKnifeRMS.p", "rb")) ########
###############################<----------------------------------------------
### This version of pickle  ###<----------------------------------------------
### is not secure. NEVER use###<----------------------------------------------
### it to open binary files ###<----------------------------------------------
### that you did not create ###<----------------------------------------------
##### WARNING ### WARNING #####<----------------------------------------------

jecdnaF = []
jecupaF = []
jerdnaF = []
jerupaF = []
jernomaF = []
jmrdnaF = []
jmrupaF = []
jmrnomaF = []


jecdnaFSD = []
jecupaFSD = []
jerdnaFSD = []
jerupaFSD = []
jernomaFSD = []
jmrdnaFSD = []
jmrupaFSD = []
jmrnomaFSD = []

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

jecdn = ROOT.TFile('2DData_jecdn.root')
jecup = ROOT.TFile('2DData_jecup.root')
jerdn = ROOT.TFile('2DData_jerdn.root')
jerup = ROOT.TFile('2DData_jerup.root')
jernom = ROOT.TFile('2DData_jernom.root')
jmrupfile = ROOT.TFile('2DData_jmrup.root')
jmrdnfile = ROOT.TFile('2DData_jmrdn.root')
jmrnomfile= ROOT.TFile('2DData_jmrnom.root')

##################################################################### Get uncertainty hists
for i in range(0, 19):
    jecdna.append(jecdn.Get('mass' + str(i)))
    jecupa.append(jecup.Get('mass' + str(i)))
    jerdna.append(jerdn.Get('mass' + str(i)))
    jerupa.append(jerup.Get('mass' + str(i)))
    jernoma.append(jernom.Get('mass'+str(i)))
    jmrupa.append(jmrupfile.Get('mass' + str(i)))
    jmrdna.append(jmrdnfile.Get('mass' + str(i)))
    jmrnoma.append(jmrnomfile.Get('mass' + str(i)))

    jecdnaSD.append(jecdn.Get('massSD' + str(i)))
    jecupaSD.append(jecup.Get('massSD' + str(i)))
    jerdnaSD.append(jerdn.Get('massSD' + str(i)))
    jerupaSD.append(jerup.Get('massSD' + str(i)))
    jernomaSD.append(jernom.Get('massSD'+str(i)))
    jmrupaSD.append(jmrupfile.Get('massSD' + str(i)))
    jmrdnaSD.append(jmrdnfile.Get('massSD' + str(i)))
    jmrnomaSD.append(jmrnomfile.Get('massSD' + str(i)))
    
    jecdnaF.append(jecdn.Get('mass' + str(i)))
    jecupaF.append(jecup.Get('mass' + str(i)))
    jerdnaF.append(jerdn.Get('mass' + str(i)))
    jerupaF.append(jerup.Get('mass' + str(i)))
    jernomaF.append(jernom.Get('mass'+str(i)))
    jmrupaF.append(jmrupfile.Get('mass' + str(i)))
    jmrdnaF.append(jmrdnfile.Get('mass' + str(i)))
    jmrnomaF.append(jmrnomfile.Get('mass' + str(i)))
    
    jecdnaFSD.append(jecdn.Get('massSD' + str(i)))
    jecupaFSD.append(jecup.Get('massSD' + str(i)))
    jerdnaFSD.append(jerdn.Get('massSD' + str(i)))
    jerupaFSD.append(jerup.Get('massSD' + str(i)))
    jernomaFSD.append(jernom.Get('massSD'+str(i)))
    jmrupaFSD.append(jmrupfile.Get('massSD' + str(i)))
    jmrdnaFSD.append(jmrdnfile.Get('massSD' + str(i)))
    jmrnomaFSD.append(jmrnomfile.Get('massSD' + str(i)))

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")
datacanvasesSD = []
datacanvases= []

datacanvases_fullband = []
datacanvases_fullbandSD = []
################################################################################# generate canvases 



######################################################################################### Get Central Value hists and generate legends etc

datalist = []
datalistSD = []
MCtruth = []
MCtruthSD = []
atlx = []
atlxpt = []
alegends = []
alegendsSD = []
alegends_fullband = []
alegends_fullbandSD = []
atlxSD = []
atlxSDpt = []
comparisons = []
for x in range(0, 19):
    datalistSD.append(f.Get('massSD'+str(x)))
    datalist.append(f.Get('mass'+str(x)))
    MCtruth.append(f.Get('genmass' + str(x)))
    MCtruthSD.append(f.Get('genmassSD' + str(x)))
    atlx.append(ROOT.TLatex())
    atlxpt.append(ROOT.TLatex())
    atlxSD.append(ROOT.TLatex())
    atlxSDpt.append(ROOT.TLatex())
    alegends.append(TLegend(.25, .35, .45, .80))
    alegendsSD.append(TLegend(.61, .35, .9, .80))
    alegends_fullband.append(TLegend(.18, .45, .51, .80))
    if x == 0:
        alegends_fullbandSD.append(TLegend(.55, .40, .9, .80))
    else:
        alegends_fullbandSD.append(TLegend(.55, .35, .9, .80))


################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, 19):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('data_unfolded_by_pythia6'+str(i)))
    ps_softdrop.append(parton_shower.Get('data_unfolded_by_pythia6_softdrop'+str(i)))
      
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

for i in range(0, 19):
#    complegends.append(ROOT.TLegend(.5, .7, .85, .85))
#    complegendssd.append(ROOT.TLegend(.5, .7, .85, .85))
#    comparisons.append(ROOT.TCanvas('comp'+str(i)))
#    comparisons[i].cd()
    temp_pdf_diff = []
    temp_softdrop_pdf_diff = []
    pdf_up.append(pdfs.Get('pdf_data_up'+str(i)))
    pdf_dn.append(pdfs.Get('pdf_data_dn'+str(i)))
    pdf_upsd.append(pdfs.Get('pdf_data_up_softdrop'+str(i)))
    pdf_dnsd.append(pdfs.Get('pdf_data_dn_softdrop'+str(i)))

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
pads_fullband = []
pads_fullbandSD = []
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
for leg in alegends_fullband :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in alegends_fullbandSD :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)


if options.oneband:
    
    for x in range(0, 19):
        datacanvases_fullband.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x)))
        datacanvases_fullbandSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD"))
    for x in range(0, 19):
        datacanvases_fullband[x].SetLeftMargin(0.15)
        datacanvases_fullbandSD[x].SetLeftMargin(0.15)
    
    setup(datacanvases_fullband, pads_fullband)
    setup(datacanvases_fullbandSD, pads_fullbandSD)
    

    histstokeep = []

    plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, ps_differences, pdf_differences, alegends_fullband, "unfoldeddata_fullband_", jmrupaF, jmrdnaF, jmrnomaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)
    plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldeddata_softdrop_fullband_", jmrupaFSD, jmrdnaFSD, jmrnomaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)

    del histstokeep[:]

else:
    
    for x in range(0, 19):
        datacanvases.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x)))
        datacanvasesSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD"))
    for x in range(0, 19):
        datacanvases[x].SetLeftMargin(0.15)
        datacanvasesSD[x].SetLeftMargin(0.15)


    setup(datacanvases, pads)
    setup(datacanvasesSD, padsSD)

    histstokeep = []

    plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldeddata_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)
    plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldeddata_softdrop_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)


