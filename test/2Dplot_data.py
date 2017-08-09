from optparse import OptionParser
import pickle
parser = OptionParser()

parser.add_option('--extra_massy', action='store_true',
                  default = False,
                  dest='extra_massy',
                  help='multiply by m of each bin')

parser.add_option('--isSoftDrop', action='store_true',
                  default = False,
                  dest='isSoftDrop',
                  help='theory curves on plots')

parser.add_option('--plotTheoryAndMC', action='store', type = 'int',
                  default = 0, # 0 = plot both, 1 = plot only MC, 2 = plot only theory
                  dest='plotTheoryAndMC',
                  help='Plot theory and MC (0), just MC (1), or just theory (2)')


parser.add_option('--extension', action ='store', type = 'string',
                 default ='',
                 dest='extension',
                 help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : _jmrup : _jmrdn : _jmrnom : _jmsup : _jmsdn : _puup : _pudn or nothing at all to get the nominal')


parser.add_option('--unrestrictedChi2', action='store_true',
                  default = False,
                  dest='unrestrictedChi2',
                  help='If true, do not restrict range in chi2 calculation')


(options, args) = parser.parse_args()

#from ROOT import *
import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import setup, get_ptbins, plot_OneBand, PlotRatios

f = ROOT.TFile('2DData' + options.extension + '.root')
parton_shower = ROOT.TFile('PS_hists.root')
pdfs = ROOT.TFile('unfoldedpdf.root')

if not options.extra_massy :
    mstr = ''
else : 
    mstr = 'mdsigmadm_'
    
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
jmsdnaF = []
jmsupaF = []
pudnaF = []
puupaF = []

jecdnaFSD = []
jecupaFSD = []
jerdnaFSD = []
jerupaFSD = []
jernomaFSD = []
jmrdnaFSD = []
jmrupaFSD = []
jmrnomaFSD = []
jmsdnaFSD = []
jmsupaFSD = []
pudnaFSD = []
puupaFSD = []

jecdna = []
jecupa = []
jerdna = []
jerupa = []
jernoma = []
jmrdna = []
jmrupa = []
jmrnoma = []
jmsdna = []
jmsupa = []
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
jmsdnaSD = []
jmsupaSD = []
pudnaSD = []
puupaSD = []

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
jmsupfile = ROOT.TFile('2DData_jmsup.root')
jmsdnfile = ROOT.TFile('2DData_jmsdn.root')
pudn = ROOT.TFile('2DData_pudn.root')
puup = ROOT.TFile('2DData_puup.root')

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
    jmsupa.append(jmsupfile.Get('mass' + str(i)))
    jmsdna.append(jmsdnfile.Get('mass' + str(i)))
    pudna.append(pudn.Get('mass' + str(i)))
    puupa.append(puup.Get('mass' + str(i)))

    
    jecdnaSD.append(jecdn.Get('massSD' + str(i)))
    jecupaSD.append(jecup.Get('massSD' + str(i)))
    jerdnaSD.append(jerdn.Get('massSD' + str(i)))
    jerupaSD.append(jerup.Get('massSD' + str(i)))
    jernomaSD.append(jernom.Get('massSD'+str(i)))
    jmrupaSD.append(jmrupfile.Get('massSD' + str(i)))
    jmrdnaSD.append(jmrdnfile.Get('massSD' + str(i)))
    jmrnomaSD.append(jmrnomfile.Get('massSD' + str(i)))
    jmsupaSD.append(jmsupfile.Get('massSD' + str(i)))
    jmsdnaSD.append(jmsdnfile.Get('massSD' + str(i)))
    pudnaSD.append(pudn.Get('massSD' + str(i)))
    puupaSD.append(puup.Get('massSD' + str(i)))

        
    jecdnaF.append(jecdn.Get('mass' + str(i)))
    jecupaF.append(jecup.Get('mass' + str(i)))
    jerdnaF.append(jerdn.Get('mass' + str(i)))
    jerupaF.append(jerup.Get('mass' + str(i)))
    jernomaF.append(jernom.Get('mass'+str(i)))
    jmrupaF.append(jmrupfile.Get('mass' + str(i)))
    jmrdnaF.append(jmrdnfile.Get('mass' + str(i)))
    jmrnomaF.append(jmrnomfile.Get('mass' + str(i)))
    jmsupaF.append(jmsupfile.Get('mass' + str(i)))
    jmsdnaF.append(jmsdnfile.Get('mass' + str(i)))
    pudnaF.append(pudn.Get('mass' + str(i)))
    puupaF.append(puup.Get('mass' + str(i)))
        
    jecdnaFSD.append(jecdn.Get('massSD' + str(i)))
    jecupaFSD.append(jecup.Get('massSD' + str(i)))
    jerdnaFSD.append(jerdn.Get('massSD' + str(i)))
    jerupaFSD.append(jerup.Get('massSD' + str(i)))
    jernomaFSD.append(jernom.Get('massSD'+str(i)))
    jmrupaFSD.append(jmrupfile.Get('massSD' + str(i)))
    jmrdnaFSD.append(jmrdnfile.Get('massSD' + str(i)))
    jmrnomaFSD.append(jmrnomfile.Get('massSD' + str(i)))
    jmsupaFSD.append(jmsupfile.Get('massSD' + str(i)))
    jmsdnaFSD.append(jmsdnfile.Get('massSD' + str(i)))
    pudnaFSD.append(pudn.Get('massSD' + str(i)))
    puupaFSD.append(puup.Get('massSD' + str(i)))
    
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

for hists in [
    jecdnaF, jecupaF, jerdnaF, jerupaF, jernomaF, jmrdnaF, jmrupaF, jmrnomaF, jmsdnaF, jmsupaF, pudnaF, puupaF, 
    jecdnaFSD, jecupaFSD, jerdnaFSD, jerupaFSD, jernomaFSD, jmrdnaFSD, jmrupaFSD, jmrnomaFSD, jmsdnaFSD, jmsupaFSD, pudnaFSD, puupaFSD, 
    jecdna, jecupa, jerdna, jerupa, jernoma, jmrdna, jmrupa, jmrnoma, jmsdna, jmsupa, pudna, puupa, 
    jecdnaSD, jecupaSD, jerdnaSD, jerupaSD, jernomaSD, jmrdnaSD, jmrupaSD, jmrnomaSD, jmsdnaSD, jmsupaSD, pudnaSD, puupaSD ] :
    for hist in hists:
        if hist.Integral() > 0 :
            hist.Scale(1.0 / hist.Integral() )

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
    
    if not options.extra_massy : 
        if x < 4:
            alegends.append(TLegend(.58, .30, .88, .80))
            alegendsSD.append(TLegend(.58, .40, .88, .80))
        else:
            alegends.append(TLegend(.58, .30, .88, .80))
            alegendsSD.append(TLegend(.58, .30, .88, .80))
        if x == 0:
            alegends_fullband.append(TLegend(.58, .30, .88, .80))
            alegends_fullbandSD.append(TLegend(.55, .29, .88, .80))
        else:
            alegends_fullband.append(TLegend(.58, .30, .88, .80))
            alegends_fullbandSD.append(TLegend(.55, .29, .88, .80))
    else : 

        alegends_fullband.append(TLegend(0.64, 0.5, 0.89, 0.89))        
        alegends_fullbandSD.append(TLegend(0.25, 0.5, 0.5, 0.89))
            
for hists in [datalistSD,datalist,MCtruth,MCtruthSD] :
    for hist in hists:
        if hist.Integral() > 0 :
            hist.Scale(1.0 / hist.Integral() )
################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, nptbin):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('data_unfolded_by_herwig'+str(i)))
    ps_softdrop.append(parton_shower.Get('data_unfolded_by_herwig_softdrop'+str(i)))

    if ps[i].Integral() > 0.0 : 
        ps[i].Scale(1.0 / ps[i].Integral() )
    if ps_softdrop[i].Integral() > 0.0 : 
        ps_softdrop[i].Scale(1.0 / ps_softdrop[i].Integral() )
    
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
pdf_cteq = []
pdf_mstw = []

pdf_upsd = []
pdf_dnsd = []
pdf_cteqsd = []
pdf_mstwsd = []
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
    pdf_cteq.append(pdfs.Get('pdf_data_cteq'+str(i)))
    pdf_cteqsd.append(pdfs.Get('pdf_data_cteq_softdrop'+str(i)))
    pdf_mstw.append(pdfs.Get('pdf_data_mstw'+str(i)))
    pdf_mstwsd.append(pdfs.Get('pdf_data_mstw_softdrop'+str(i)))

    for hist in [pdf_up[i], pdf_dn[i], pdf_upsd[i], pdf_dnsd[i], pdf_cteq[i], pdf_cteqsd[i], pdf_mstw[i], pdf_mstwsd[i]]:
        if hist.Integral() > 0:
            hist.Scale(1.0 / hist.Integral() )
    

    temp_diffcteq = (pdf_cteq[i] - MCtruth[i])
    temp_diffmstw = (pdf_mstw[i] - MCtruth[i])
    temp_diffcteqsd = (pdf_cteqsd[i] - MCtruthSD[i])
    temp_diffmstwsd = (pdf_mstwsd[i] - MCtruthSD[i])

    
    temp_unc = (pdf_up[i] - pdf_dn[i]) 
    temp_unc_softdrop = (pdf_upsd[i] - pdf_dnsd[i])
    #temp_unc.Scale( 0.5 )
    #temp_unc_softdrop.Scale(0.5)

    temp_unc.Scale(scales[i])
    temp_unc_softdrop.Scale(scales[i])
    temp_diffcteq.Scale(scales[i])
    temp_diffmstw.Scale(scales[i])
    temp_diffcteqsd.Scale(scales[i])
    temp_diffmstwsd.Scale(scales[i])
    for ibin in xrange(1, temp_unc.GetNbinsX()):
        diff1 = abs(temp_unc.GetBinContent(ibin))
        diff2 = abs(temp_diffcteq.GetBinContent(ibin))
        diff3 = abs(temp_diffmstw.GetBinContent(ibin))
        if diff1 > diff2 and diff1 > diff3 : 
            temp_pdf_diff.append(diff1)
        elif diff2 > diff1 and diff2 > diff3 :
            temp_pdf_diff.append(diff2)
        else :
            temp_pdf_diff.append(diff3)

        diffSD1 = abs(temp_unc_softdrop.GetBinContent(ibin))
        diffSD2 = abs(temp_diffcteqsd.GetBinContent(ibin))
        diffSD3 = abs(temp_diffmstwsd.GetBinContent(ibin))
        if diffSD1 > diffSD2 and diffSD1 > diffSD3 : 
            temp_softdrop_pdf_diff.append(diffSD1)
        elif diffSD2 > diffSD1 and diffSD2 > diffSD3 :
            temp_softdrop_pdf_diff.append(diffSD2)
        else :
            temp_softdrop_pdf_diff.append(diffSD3)
                        
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
    plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, puupaFSD, pudnaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldeddata_softdrop_fullband_" + mstr, jmrupaFSD, jmrdnaFSD, jmrnomaFSD, jmsupaFSD, jmsdnaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=True)
else:
    plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, puupaF, pudnaF, ps_differences, pdf_differences, alegends_fullband, "unfoldeddata_fullband_" + mstr, jmrupaF, jmrdnaF, jmrnomaF, jmsupaF, jmsdnaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=True)
del histstokeep[:]
