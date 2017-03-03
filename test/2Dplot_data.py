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

parser.add_option('--logy', action='store_true',
                  default = False,
                  dest='logy',
                  help='plots in log y')

parser.add_option('--extension', action ='store', type = 'string',
                 default ='',
                 dest='extension',
                 help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : _jmrup : _jmrdn : _jmrnom or nothing at all to get the nominal')


(options, args) = parser.parse_args()

#from ROOT import *
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import plotter, setup, get_ptbins, plot_OneBand, PlotRatios

f = ROOT.TFile('2DData' + options.extension + '.root')
parton_shower = ROOT.TFile('PS_hists.root')
pdfs = ROOT.TFile('unfoldedpdf.root')


scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.]
nptbin = 11
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
for i in range(0, nptbin):
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
for x in range(0, nptbin):
    datalistSD.append(f.Get('massSD'+str(x)))
    datalist.append(f.Get('mass'+str(x)))
    MCtruth.append(f.Get('genmass' + str(x)))
    MCtruthSD.append(f.Get('genmassSD' + str(x)))
    atlx.append(ROOT.TLatex())
    atlxpt.append(ROOT.TLatex())
    atlxSD.append(ROOT.TLatex())
    atlxSDpt.append(ROOT.TLatex())
    
    if options.logy:
        if x > 13:
            alegends.append(TLegend(.22, .35, .37, .80))
        else:
            alegends.append(TLegend(.52, .07, .75, .50))
        if x == 0:
            alegendsSD.append(TLegend(.36, .10, .65, .450))
        elif x > 15:
            alegendsSD.append(TLegend(.33, .10, .58, .450))
        else:
            alegendsSD.append(TLegend(.36, .10, .75, .450))
        if x > 13:
            alegends_fullband.append(TLegend(.22, .65, .37, .80))
        else:
            alegends_fullband.append(TLegend(.51, .09, .75, .42))

        if x == 0:
            alegends_fullbandSD.append(TLegend(.36, .10, .65, .450))
        elif x > 15:
            alegends_fullbandSD.append(TLegend(.33, .10, .58, .450))
        else:
            alegends_fullbandSD.append(TLegend(.36, .10, .75, .450))
                
    else:

        if x > 13:
            alegends.append(TLegend(.22, .35, .37, .80))
        else:
            alegends.append(TLegend(.22, .35, .37, .80))
        if x < 4:
            alegendsSD.append(TLegend(.60, .40, .90, .80))
        else:
            alegendsSD.append(TLegend(.58, .30, .90, .80))
        if x > 13:
            alegends_fullband.append(TLegend(.25, .2, .54, .80))
        else:
            alegends_fullband.append(TLegend(.25, .2, .54, .80))
        if x == 0:
            alegends_fullbandSD.append(TLegend(.55, .29, .89, .80))
        else:
            alegends_fullbandSD.append(TLegend(.55, .29, .89, .80))

################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, nptbin):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('data_unfolded_by_herwig'+str(i)))
    ps_softdrop.append(parton_shower.Get('data_unfolded_by_herwig_softdrop'+str(i)))
      
    temp_unc = 0.5 * (ps[i] - datalist[i])
    temp_softdrop_unc = 0.5 * (ps_softdrop[i] - datalistSD[i])
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

for i in range(0, nptbin):
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
ptbins = ['#bf{200 < p_{T} < 260 GeV}','#bf{260 < p_{T} < 350 GeV}','#bf{350 < p_{T} < 460 GeV}','#bf{460 < p_{T} < 550 GeV}','#bf{550 < p_{T} < 650 GeV}','#bf{650 < p_{T} < 760 GeV}', '#bf{760 < p_{T} < 900 GeV}', '#bf{900 < p_{T} < 1000 GeV}', '#bf{1000 < p_{T} < 1100 GeV}','#bf{1100 < p_{T} < 1200 GeV}',
    '#bf{1200 < p_{T} < 1300 GeV}', '#bf{p_{T} > 1300 GeV}']


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

##############################################################
'''
pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
#### Bring in post-unfolded MC and store in lists
MCfile = ROOT.TFile('2DClosure.root')
MClistSD = []
MClist = []
for x in range(0, 19):
    MClistSD.append(MCfile.Get('pythia8_massSD'+str(x)))
    MClist.append(MCfile.Get('pythia8_mass'+str(x)))

##### Get pre-unfolded distributions and slice them
pre_datafile = ROOT.TFile('jetht_40pbinv_weighted_dataplots_otherway.root')
pre_MCfile = ROOT.TFile('responses_otherway_qcdmc.root')
preunfoldedMC = pre_MCfile.Get('PFJet_pt_m_AK8')
preunfoldedMCSD = pre_MCfile.Get('PFJet_pt_m_AK8SD')
preunfolded = pre_datafile.Get('PFJet_pt_m_AK8')
preunfoldedSD = pre_datafile.Get('PFJet_pt_m_AK8SD')

preunfolded_datalist = []
preunfolded_datalistSD = []
preunfolded_MClist = []
preunfolded_MClistSD = []

for i in range(0, 19):
    preunfolded_datalist.append(preunfolded.ProjectionX('pre_mass' + str(i), i+1, i+1))
    preunfolded_datalist[i].SetTitle('Preunfolded Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    preunfolded_datalistSD.append(preunfoldedSD.ProjectionX('pre_mass' + str(i), i+1, i+1))
    preunfolded_datalistSD[i].SetTitle('Preunfolded Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    preunfolded_MClist.append(preunfoldedMC.ProjectionX('pre_mass_MC' + str(i), i+1, i+1))
    preunfolded_MClist[i].SetTitle('Preunfolded MC Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    preunfolded_MClistSD.append(preunfoldedMCSD.ProjectionX('pre_mass_MC' + str(i), i+1, i+1))
    preunfolded_MClistSD[i].SetTitle('Preunfolded MC Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
#### prepare ratio canvases and legends
ratiocanvases = []
ratiocanvasesSD = []
ratiocanvases2 = []
ratiocanvasesSD2 = []
ratioLeg = []
ratioLegSD = []
ratioLeg2 = []
ratioLegSD2 = []
for x in range(0,19):
    ratiocanvases.append(TCanvas("ratio_"+str(x), "ratio_"+str(x)))
    ratiocanvasesSD.append(TCanvas("ratio_" + str(x) + "SD", "ratio_"+str(x)+"SD"))
    ratiocanvases2.append(TCanvas("ratio2_"+str(x), "ratio2_"+str(x)))
    ratiocanvasesSD2.append(TCanvas("ratio2_" + str(x) + "SD", "ratio2_"+str(x)+"SD"))
    if x ==18:
        ratioLeg.append(TLegend(.30, .70, .70, .80))
        ratioLegSD.append(TLegend(.27, .70, .70, .80))
    else:
        ratioLeg.append(TLegend(.50, .70, .90, .80))
        ratioLegSD.append(TLegend(.50, .70, .95, .80))
    if x == 18:
        ratioLeg2.append(TLegend(.110, .80, .48, .90))
        ratioLegSD2.append(TLegend(.50, .70, .90, .80))
    else:
        ratioLeg2.append(TLegend(.50, .70, .90, .80))
        ratioLegSD2.append(TLegend(.50, .70, .90, .80))
for leg in ratioLeg :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in ratioLegSD :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in ratioLeg2 :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in ratioLegSD2 :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

PlotRatios( ratiocanvasesSD,  datalistSD, MClistSD, preunfolded_datalistSD, preunfolded_MClistSD, ratioLegSD, get_ptbins(), atlxSD, atlxSDpt, "ratio_SD_", MCtruthSD, ratiocanvasesSD2, ratioLegSD2, softdrop="MMDT Beta=0")
PlotRatios( ratiocanvases,  datalist, MClist, preunfolded_datalist, preunfolded_MClist, ratioLeg, get_ptbins(), atlx, atlxpt, "ratio_", MCtruth,  ratiocanvases2, ratioLeg2 )

'''
####################################################################
if options.logy:
    if options.oneband:
    
        for x in range(0, nptbin):
            datacanvases_fullband.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvases_fullbandSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, nptbin):
            datacanvases_fullband[x].SetLeftMargin(0.15)
            datacanvases_fullbandSD[x].SetLeftMargin(0.15)
    
        setup(datacanvases_fullband, pads_fullband)
        setup(datacanvases_fullbandSD, pads_fullbandSD)
    

        histstokeep = []
        if options.isSoftDrop:
            plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldeddata_softdrop_fullband_logy_", jmrupaFSD, jmrdnaFSD, jmrnomaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)
        else:
            plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, ps_differences, pdf_differences, alegends_fullband, "unfoldeddata_fullband_logy_", jmrupaF, jmrdnaF, jmrnomaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)
        del histstokeep[:]

    else:
    
        for x in range(0, nptbin):
            datacanvases.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvasesSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, nptbin):
            datacanvases[x].SetLeftMargin(0.15)
            datacanvasesSD[x].SetLeftMargin(0.15)


        setup(datacanvases, pads)
        setup(datacanvasesSD, padsSD)
    
        histstokeep = []
        if options.isSoftDrop:
            plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldeddata_softdrop_logy_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)

        else:
            plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldeddata_logy_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)

else:
    if options.oneband:
        
        for x in range(0, nptbin):
            datacanvases_fullband.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvases_fullbandSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, nptbin):
            datacanvases_fullband[x].SetLeftMargin(0.15)
            datacanvases_fullbandSD[x].SetLeftMargin(0.15)
    
        setup(datacanvases_fullband, pads_fullband)
        setup(datacanvases_fullbandSD, pads_fullbandSD)
        
        
        histstokeep = []
        
        if options.isSoftDrop:
            plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldeddata_softdrop_fullband_", jmrupaFSD, jmrdnaFSD, jmrnomaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)
        else:
            plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, ps_differences, pdf_differences, alegends_fullband, "unfoldeddata_fullband_", jmrupaF, jmrdnaF, jmrnomaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)
        del histstokeep[:]

    else:
    
        for x in range(0, nptbin):
            datacanvases.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvasesSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, nptbin):
            datacanvases[x].SetLeftMargin(0.15)
            datacanvasesSD[x].SetLeftMargin(0.15)


        setup(datacanvases, pads)
        setup(datacanvasesSD, padsSD)
        
        histstokeep = []
        
        if options.isSoftDrop:
            plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldeddata_softdrop_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)
        else:
            plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldeddata_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)



