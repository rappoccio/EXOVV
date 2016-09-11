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



parser.add_option('--logy', action='store_true',
                  default = False,
                  dest='logy',
                  help='plots in log y')

                                 
(options, args) = parser.parse_args()

f = ROOT.TFile('2DClosure.root')
parton_shower = ROOT.TFile('PS_hists.root')
pdfs = ROOT.TFile('unfoldedpdf.root')


scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]

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


jecdnaSD = []
jecupaSD = []
jerdnaSD = []
jerupaSD = []
jernomaSD = []
jmrdnaSD = []
jmrupaSD = []
jmrnomaSD = []


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
for i in range(0, 19):
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

    jecdnaF.append(jecdn.Get('pythia8_mass'  + str(i)))
    jecupaF.append(jecup.Get('pythia8_mass'  + str(i)))
    jerdnaF.append(jerdn.Get('pythia8_mass'  + str(i)))
    jerupaF.append(jerup.Get('pythia8_mass'  + str(i)))
    jernomaF.append(jernom.Get('pythia8_mass' +str(i)))
    jmrupaF.append(jmrupfile.Get('pythia8_mass'  + str(i)))
    jmrdnaF.append(jmrdnfile.Get('pythia8_mass'  + str(i)))
    jmrnomaF.append(jmrnomfile.Get('pythia8_mass'  + str(i)))
    
    jecdnaFSD.append(jecdn.Get('pythia8_mass'  + str(i)))
    jecupaFSD.append(jecup.Get('pythia8_mass'  + str(i)))
    jerdnaFSD.append(jerdn.Get('pythia8_mass'  + str(i)))
    jerupaFSD.append(jerup.Get('pythia8_mass'  + str(i)))
    jernomaFSD.append(jernom.Get('pythia8_mass' +str(i)))
    jmrupaFSD.append(jmrupfile.Get('pythia8_mass'  + str(i)))
    jmrdnaFSD.append(jmrdnfile.Get('pythia8_mass'  + str(i)))
    jmrnomaFSD.append(jmrnomfile.Get('pythia8_mass'  + str(i)))


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
    datalistSD.append(f.Get('pythia8_massSD'+str(x)))
    datalist.append(f.Get('pythia8_mass'+str(x)))
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
            alegends_fullband.append(TLegend(.22, .55, .47, .80))
        else:
            alegends_fullband.append(TLegend(.22, .55, .47, .80))
        if x == 0:
            alegends_fullbandSD.append(TLegend(.60, .50, .90, .80))
        else:
            alegends_fullbandSD.append(TLegend(.58, .30, .90, .80))
################################################################################################################# Get Parton Showering Unc.
ps_differences = []
ps_differences_softdrop = []
for i in range(0, 19):
    temp_diff = []
    temp_softdrop_diff = []
    ps.append(parton_shower.Get('pythia8_unfolded_by_herwig'+str(i)))
    ps_softdrop.append(parton_shower.Get('pythia8_unfolded_by_herwig_softdrop'+str(i)))
      
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

for i in range(0, 19):
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

if options.logy:
    if options.oneband:
        
        for x in range(0, 19):
            datacanvases_fullband.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvases_fullbandSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, 19):
            datacanvases_fullband[x].SetLeftMargin(0.15)
            datacanvases_fullbandSD[x].SetLeftMargin(0.15)
    
        setup(datacanvases_fullband, pads_fullband)
        setup(datacanvases_fullbandSD, pads_fullbandSD)
        
        
        histstokeep = []
        if options.isSoftDrop:
            plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldedclosure_softdrop_fullband_logy_", jmrupaFSD, jmrdnaFSD, jmrnomaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=False)
        else:
            plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, ps_differences, pdf_differences, alegends_fullband, "unfoldedclosure_fullband_logy_", jmrupaF, jmrdnaF, jmrnomaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=False)
        del histstokeep[:]
    
    else:
        
        for x in range(0, 19):
            datacanvases.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvasesSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, 19):
            datacanvases[x].SetLeftMargin(0.15)
            datacanvasesSD[x].SetLeftMargin(0.15)
    
    
        setup(datacanvases, pads)
        setup(datacanvasesSD, padsSD)
        
        histstokeep = []
        if options.isSoftDrop:
            plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldedclosure_softdrop_logy_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=False)

        else:
            plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldedclosure_logy_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=False)

else:
    if options.oneband:
        
        for x in range(0, 19):
            datacanvases_fullband.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvases_fullbandSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD", 800, 600))
        for x in range(0, 19):
            datacanvases_fullband[x].SetLeftMargin(0.15)
            datacanvases_fullbandSD[x].SetLeftMargin(0.15)
        
        setup(datacanvases_fullband, pads_fullband)
        setup(datacanvases_fullbandSD, pads_fullbandSD)
        
        
        histstokeep = []
        
        if options.isSoftDrop:
            plot_OneBand(datacanvases_fullbandSD, pads_fullbandSD, datalistSD, MCtruthSD, jecupaFSD, jecdnaFSD, jerupaFSD, jerdnaFSD, jernomaFSD, ps_differences_softdrop, pdf_differences_softdrop, alegends_fullbandSD, "unfoldedclosure_softdrop_fullband_", jmrupaFSD, jmrdnaFSD, jmrnomaFSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=False)
        else:
            plot_OneBand(datacanvases_fullband, pads_fullband, datalist, MCtruth, jecupaF, jecdnaF, jerupaF, jerdnaF, jernomaF, ps_differences, pdf_differences, alegends_fullband, "unfoldedclosure_fullband_", jmrupaF, jmrdnaF, jmrnomaF, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=False)
        del histstokeep[:]

    else:
        
        for x in range(0, 19):
            datacanvases.append(TCanvas("ddist_full"+str(x), "ddist_full"+str(x), 800, 600))
            datacanvasesSD.append(TCanvas("ddist_full" + str(x) + "SD", "ddist_full"+str(x)+"SD"), 800, 600)
        for x in range(0, 19):
            datacanvases[x].SetLeftMargin(0.15)
            datacanvasesSD[x].SetLeftMargin(0.15)
        
        
        setup(datacanvases, pads)
        setup(datacanvasesSD, padsSD)
        
        histstokeep = []
        
        if options.isSoftDrop:
            plotter(datacanvasesSD, padsSD, datalistSD, MCtruthSD, jecupaSD, jecdnaSD, jerupaSD, jerdnaSD, jernomaSD, ps_differences_softdrop, pdf_differences_softdrop, alegendsSD, "unfoldedclosure_softdrop_", jmrupaSD, jmrdnaSD, jmrnomaSD, atlxSD, atlxSDpt, get_ptbins(), softdrop="MMDT Beta=0", keephists=histstokeep, jackknifeRMS=RMS_vals_softdrop, isData=False)
        else:
            plotter(datacanvases, pads, datalist, MCtruth, jecupa, jecdna, jerupa, jerdna, jernoma, ps_differences, pdf_differences, alegends, "unfoldedclosure_", jmrupa, jmrdna, jmrnoma, atlx, atlxpt, get_ptbins(), keephists=histstokeep, jackknifeRMS=RMS_vals, isData=False)



