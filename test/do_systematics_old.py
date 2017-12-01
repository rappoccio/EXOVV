#from ROOT import *
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import setup, get_ptbins, smooth
from optparse import OptionParser
from sysvar_old import plot_vars, reset
import pickle
parser = OptionParser()
                                 
(options, args) = parser.parse_args()

f = ROOT.TFile('PASStage/2DClosure_nomnom.root')
parton_shower = ROOT.TFile('PASStage/PS_hists.root')
pdfs = ROOT.TFile('PASStage/unfoldedpdf.root')
bins = ['200 < p_{T} < 260 GeV','260 < p_{T} < 350 GeV','350 < p_{T} < 460 GeV','460 < p_{T} < 550 GeV','550 < p_{T} < 650 GeV','650 < p_{T} < 760 GeV', '760 < p_{T} < 900 GeV', '900 < p_{T} < 1000 GeV', '1000 < p_{T} < 1100 GeV','1100 < p_{T} < 1200 GeV',
    '1200 < p_{T} < 1300 GeV', 'p_{T} > 1300 GeV']
scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100.]
nptbins = 11
##### WARNING ### WARNING #####<----------------------------------------------
### This version of pickle  ###<----------------------------------------------
### is not secure. NEVER use###<----------------------------------------------
### it to open binary files ###<----------------------------------------------
### that you did not create ###<----------------------------------------------
###############################<----------------------------------------------
RMS_vals = pickle.load(open("ungroomedJackKnifeRMS.p", "rb"))         ########
RMS_vals_softdrop = pickle.load(open("softdropJackKnifeRMS.p", "rb")) ########
###############################<----------------------------------------------
### This version of pickle  ###<----------------------------------------------
### is not secure. NEVER use###<----------------------------------------------
### it to open binary files ###<----------------------------------------------
### that you did not create ###<----------------------------------------------
##### WARNING ### WARNING #####<----------------------------------------------

jecdna = []
jecupa = []
jerdna = []
jerupa = []
jernoma = []
jmrdna = []
jmrupa = []
jmrnoma = []
pudna = []
puupa = []


jecdnaSD = []
jecupaSD = []
jerdnaSD = []
jerupaSD = []
jernomaSD = []
jmrdnaSD = []
jmrupaSD = []
jmrnomaSD = []
pudnaSD = []
puupaSD = []

ps = []
ps_softdrop = []

ps_differences = []
ps_differences_softdrop = []

jecdn = ROOT.TFile('PASStage/2DClosure_jecdn.root')
jecup = ROOT.TFile('PASStage/2DClosure_jecup.root')
jerdn = ROOT.TFile('PASStage/2DClosure_jerdn.root')
jerup = ROOT.TFile('PASStage/2DClosure_jerup.root')
jernom = ROOT.TFile('PASStage/2DClosure_jernom.root')
jmrupfile = ROOT.TFile('PASStage/2DClosure_jmrup.root')
jmrdnfile = ROOT.TFile('PASStage/2DClosure_jmrdn.root')
jmrnomfile= ROOT.TFile('PASStage/2DClosure_jmrnom.root')
puupfile = ROOT.TFile('PASStage/2DClosure_puup.root')
pudnfile = ROOT.TFile('PASStage/2DClosure_pudn.root')

##################################################################### Get uncertainty hists
for i in range(0, nptbins):
    jecdna.append(jecdn.Get('pythia8_mass' + str(i)))
    jecupa.append(jecup.Get('pythia8_mass' + str(i)))
    jerdna.append(jerdn.Get('pythia8_mass' + str(i)))
    jerupa.append(jerup.Get('pythia8_mass' + str(i)))
    jernoma.append(jernom.Get('pythia8_mass'+str(i)))
    jmrupa.append(jmrupfile.Get('pythia8_mass' + str(i)))
    jmrdna.append(jmrdnfile.Get('pythia8_mass' + str(i)))
    jmrnoma.append(jmrnomfile.Get('pythia8_mass' + str(i)))
    puupa.append(puupfile.Get('pythia8_mass' + str(i)))
    pudna.append(pudnfile.Get('pythia8_mass' + str(i)))

    
    jecdnaSD.append(jecdn.Get('pythia8_massSD' + str(i)))
    jecupaSD.append(jecup.Get('pythia8_massSD' + str(i)))
    jerdnaSD.append(jerdn.Get('pythia8_massSD' + str(i)))
    jerupaSD.append(jerup.Get('pythia8_massSD' + str(i)))
    jernomaSD.append(jernom.Get('pythia8_massSD'+str(i)))
    jmrupaSD.append(jmrupfile.Get('pythia8_massSD' + str(i)))
    jmrdnaSD.append(jmrdnfile.Get('pythia8_massSD' + str(i)))
    jmrnomaSD.append(jmrnomfile.Get('pythia8_massSD' + str(i)))
    puupaSD.append(puupfile.Get('pythia8_massSD' + str(i)))
    pudnaSD.append(pudnfile.Get('pythia8_massSD' + str(i)))

    
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")
datacanvasesSD = []
datacanvases= []

################################################################################# generate canvases 
for x in range(0, nptbins):
    datacanvases.append(TCanvas("cdist"+str(x), "cdist"+str(x), 800, 600))
    datacanvasesSD.append(TCanvas("cdist" + str(x) + "SD", "cdist"+str(x)+"SD", 800, 600))
for canv in datacanvases:
    canv.SetBottomMargin(0.15)
for canv in datacanvasesSD:
    canv.SetBottomMargin(0.15)
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
for x in range(0, nptbins):
    datalistSD.append(f.Get('pythia8_massSD'+str(x)))
    datalist.append(f.Get('pythia8_mass'+str(x)))
    MCtruth.append(f.Get('genmass' + str(x)))
    MCtruthSD.append(f.Get('genmassSD' + str(x)))
    atlx.append(ROOT.TLatex())
    atlxpt.append(ROOT.TLatex())
    atlxSD.append(ROOT.TLatex())
    atlxSDpt.append(ROOT.TLatex())
    alegends.append(TLegend(.2, .6, .89, .80))
    alegendsSD.append(TLegend(.2, .6, .89, .80))
    datacanvases[x].SetLeftMargin(0.15)
    datacanvasesSD[x].SetLeftMargin(0.15)
################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, nptbins):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('pythia8_unfolded_by_herwig'+str(i)))
    ps_softdrop.append(parton_shower.Get('pythia8_unfolded_by_herwig_softdrop'+str(i)))
    
    temp_unc = (ps[i] - datalist[i])
    temp_softdrop_unc = (ps_softdrop[i] - datalistSD[i])
    temp_unc.Scale(scales[i])
    temp_softdrop_unc.Scale(scales[i])
    
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

pdf_cteq = []
pdf_mstw = []

pdf_cteqsd = []
pdf_mstwsd = []

complegends = []
complegendssd = []

for i in range(0, nptbins):
    temp_pdf_diff = []
    temp_softdrop_pdf_diff = []
    pdf_up.append(pdfs.Get('pdf_up'+str(i)))
    pdf_dn.append(pdfs.Get('pdf_dn'+str(i)))
    pdf_upsd.append(pdfs.Get('pdf_up_softdrop'+str(i)))
    pdf_dnsd.append(pdfs.Get('pdf_dn_softdrop'+str(i)))

    pdf_cteq.append(pdfs.Get('pdf_cteq'+str(i)))
    pdf_mstw.append(pdfs.Get('pdf_mstw'+str(i)))
    pdf_cteqsd.append(pdfs.Get('pdf_cteq_softdrop'+str(i)))
    pdf_mstwsd.append(pdfs.Get('pdf_mstw_softdrop'+str(i)))
         
    temp_unc = (pdf_up[i] - pdf_dn[i])
    temp_unc_softdrop = (pdf_upsd[i] - pdf_dnsd[i])
    temp_unc2 = (pdf_cteq[i] - datalist[i])
    temp_unc2_softdrop = (pdf_cteqsd[i] - datalistSD[i])
    temp_unc3 = (pdf_mstw[i] - datalist[i])
    temp_unc3_softdrop = (pdf_mstwsd[i] - datalistSD[i])
    
    temp_unc.Scale(scales[i])
    temp_unc_softdrop.Scale(scales[i])
    temp_unc2.Scale(scales[i])
    temp_unc2_softdrop.Scale(scales[i])
    temp_unc3.Scale(scales[i])
    temp_unc3_softdrop.Scale(scales[i])
                
    for ibin in xrange(1, temp_unc.GetNbinsX()):
        val_ungroomed = (temp_unc.GetBinContent(ibin))**2 + (temp_unc2.GetBinContent(ibin))**2 + (temp_unc3.GetBinContent(ibin))**2
        val_groomed = (temp_unc_softdrop.GetBinContent(ibin))**2 + (temp_unc2_softdrop.GetBinContent(ibin))**2 + (temp_unc3_softdrop.GetBinContent(ibin))**2
        temp_pdf_diff.append(sqrt(val_ungroomed))
        temp_softdrop_pdf_diff.append( sqrt(val_groomed) )


    pdf_differences.append(temp_pdf_diff)
    pdf_differences_softdrop.append(temp_softdrop_pdf_diff)

# Canvases
ptbins = ['#{p_{T} 200-260 GeV}','#{p_{T} 260-350 GeV}','#{p_{T} 350-460 GeV}','#{p_{T} 460-550 GeV}','#{p_{T} 550-650 GeV}','#{p_{T} 650-760 GeV}', '#{p_{T} >760 GeV}']

for leg in alegends :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in alegendsSD :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

histstokeep = []

plot_vars(datacanvases, datalist, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "mcvariations_PAS_", jmrupa, jmrdna, jmrnoma, puupa, pudna, bins, keephists=histstokeep, jackknifeRMS=RMS_vals)
plot_vars(datacanvasesSD, datalistSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "mcvariations_softdrop_PAS_", jmrupaSD, jmrdnaSD, jmrnomaSD, puupaSD, pudnaSD, bins, softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, histname="Soft Drop ")
