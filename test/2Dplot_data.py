#from ROOT import *
import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout
from math import sqrt
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--plotUnc', action='store_true',
                  default= 'False',
                  dest='plotUnc',
                  help='Plot MC with systematic uncertainties added to it')                                  
(options, args) = parser.parse_args()


f = ROOT.TFile('2DData.root')
jecdna = []
jecdnaSD = []
jecupa = []
jecupaSD = []
jerdna = []
jerdnaSD = []
jerupa = []
jerupaSD = []
if options.plotUnc:
    jecdn = ROOT.TFile('2DData_jecdn.root')
    jecup = ROOT.TFile('2DData_jecup.root')
    jerdn = ROOT.TFile('2DData_jerdn.root')
    jerup = ROOT.TFile('2DData_jerup.root')
    for i in range(0, 7):
        print i 
        jecdna.append(jecdn.Get('mass' + str(i)))
        jecdnaSD.append(jecdn.Get('massSD'+ str(i)))
        jecupa.append(jecup.Get('mass' + str(i)))
        jecupaSD.append(jecup.Get('massSD'+str(i)))
        jerdna.append(jerdn.Get('mass' + str(i)))
        jerdnaSD.append(jerdn.Get('massSD'+str(i)))
        jerupa.append(jerup.Get('mass' + str(i)))
        jerupaSD.append(jerup.Get('massSD'+str(i)))


ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

# Canvases
uc2 = TCanvas("cdist140", "cdist140")
uc3 = TCanvas("cdist200", "cdist200")
uc4 = TCanvas("cdist260", "cdist260")
uc5 = TCanvas("cdist320", "cdist320")
uc6 = TCanvas("cdist400", "cdist400")
uc7 = TCanvas("cdist450", "cdist450")
uc8 = TCanvas("cdist500", "cdist500")


#qtrue140=f.Get("HLT_PFJet140mAK8Gen")
ucsd2 = TCanvas("cdist140SD","cdist140SD")
ucsd3 = TCanvas("cdist200SD","cdist200SD")
ucsd4 = TCanvas("cdist260SD","cdist260SD")
ucsd5 = TCanvas("cdist320SD","cdist320SD")
ucsd6 = TCanvas("cdist400SD","cdist400SD")
ucsd7 = TCanvas("cdist450SD","cdist450SD")
ucsd8 = TCanvas("cdist500SD","cdist500SD")

datacanvasesSD = [ucsd2, ucsd3, ucsd4, ucsd5, ucsd6, ucsd7, ucsd8]
datacanvases= [uc2, uc3, uc4, uc5, uc6, uc7, uc8]

# Variables

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
for x in range(0, 7):
    datalistSD.append(f.Get('massSD'+str(x)))
    datalist.append(f.Get('mass'+str(x)))
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
#d800 =d.Get('unfolded_6')

# Canvases
ptbins = ['#bf{p_{T} 200-240 GeV}','#bf{p_{T} 240-310 GeV}','#bf{p_{T} 310-400 GeV}','#bf{p_{T} 400-530 GeV}','#bf{p_{T} 530-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} >760 GeV}']


pads = []
padsSD = []
hRatioList = []
hRatioListSD = []

for b in atlx:
    b.SetNDC()
    b.SetTextFont(43)
    b.SetTextSize(30)
for g in atlxpt:
    g.SetNDC()
    g.SetTextFont(43)
    g.SetTextSize(25)
for leg in alegends :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for icanv,canv in enumerate ( datacanvases) :
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
    pads.append( [pad1,pad2] )
for icanv, canv in enumerate(datacanvasesSD):
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
    padsSD.append( [pad1,pad2] )
histstokeep = []

for i in datacanvases:
    index = datacanvases.index(i)
    pads[index][0].cd()
    pads[index][0].SetLogy()
    datalist[index].UseCurrentStyle()
    MCtruth[index].UseCurrentStyle()
    ################################## Uncertainties
    hReco = datalist[index]
    nom = datalist[index]
    jesUP  = jecupa[index]
    jesDOWN = jecdna[index]
    jerUP  = jerupa[index]
    jerDOWN = jerdna[index]
    if options.plotUnc:
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

    ################################## Make top plot nice
    hReco.SetTitle(";; #frac{d#sigma}{dmdp_{T}} (#frac{1}{GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( 1e-8, 1e+3, "Y")
    hReco.SetFillColor(ROOT.kYellow)
    hReco.Draw("E2")
    hReco.Draw("E same")
    MCtruth[index].SetLineColor(2)
    #MCtruth[index].Scale(lumi)
    MCtruth[index].Draw( "hist SAME" )
    atlx[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
    atlxpt[index].DrawLatex(0.555, 0.559, ptbins[index])
    ################################## legends
    alegends[index].AddEntry(MCtruth[index], 'Data', 'l')
    alegends[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
    alegends[index].Draw()
    #################################### ratio plot stuff
    trueCopy = MCtruth[index].Clone()
    trueCopy.SetName( trueCopy.GetName() + "_copy")
    datcopy = hReco.Clone()
    datcopy.SetName( datcopy.GetName() + "_copy" )
    datcopy.GetYaxis().SetTitle("Theory/Data")
    histstokeep.append( [datcopy,trueCopy])
    for ibin in xrange(1,datcopy.GetNbinsX()):
        if datcopy.GetBinContent(ibin) > 0: 
            datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
        else:
            datcopy.SetBinError(ibin, 0)
        datcopy.SetBinContent(ibin, 1.0)
        
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    pads[index][1].cd()
    trueCopy.SetTitle(";Jet Mass (GeV);Theory/Data")
    trueCopy.UseCurrentStyle()
    trueCopy.GetXaxis().SetTitleOffset(3)
    datcopy.SetMinimum(0)
    datcopy.SetMaximum(2)
    datcopy.GetYaxis().SetNdivisions(2,4,0,False)
    trueCopy.SetLineStyle(2)
    trueCopy.SetLineColor(2)
    datcopy.SetFillColor(ROOT.kYellow)
    datcopy.Draw('e2')
    datcopy.SetMarkerStyle(0)
    trueCopy.Draw("hist same")
    
    hRatioList.append( trueCopy)
    pads[index][0].Update()
    pads[index][1].Update()
    datacanvases[index].Draw()
    datacanvases[index].SaveAs("unfoldedresults_" + str(index) + ".png")

for i in datacanvasesSD:
    index = datacanvasesSD.index(i)
    padsSD[index][0].cd()
    padsSD[index][0].SetLogy()
    datalistSD[index].UseCurrentStyle()
    MCtruthSD[index].UseCurrentStyle()
    ################################## Uncertainties
    hReco = datalistSD[index]
    nom = datalistSD[index]
    jesUP  = jecupaSD[index]
    jesDOWN = jecdnaSD[index]
    jerUP  = jerupaSD[index]
    jerDOWN = jerdnaSD[index]
    if options.plotUnc:
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
    ################################## Make top plot nice
    hReco.SetTitle(";; #frac{d#sigma}{dmdp_{T}} (#frac{pb}{GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( .0001, 1000000, "Y")
    hReco.SetFillStyle(1001)
    hReco.SetFillColor(ROOT.kYellow)
    hReco.Draw("E2")
    hReco.Draw("E same")
    MCtruthSD[index].SetLineColor(2)
    #MCtruth[index].Scale(lumi)
    MCtruthSD[index].Draw( "hist SAME" )
    atlxSD[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
    atlxSDpt[index].DrawLatex(0.555, 0.559, ptbins[index])
    ################################## legends
    alegendsSD[index].AddEntry(MCtruth[index], 'Data w/ MMDT Beta = 0', 'l')
    alegendsSD[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
    alegendsSD[index].Draw()
    #################################### ratio plot stuff
    trueCopy = MCtruthSD[index].Clone()
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    padsSD[index][1].cd()
    trueCopy.SetTitle(";Jet Mass (GeV);Theory/Data")
    trueCopy.UseCurrentStyle()
    trueCopy.GetXaxis().SetTitleOffset(3)
    trueCopy.SetMinimum(0)
    trueCopy.SetMaximum(2)
    trueCopy.GetYaxis().SetNdivisions(2,4,0,False)
    trueCopy.SetFillStyle(1001)
    trueCopy.SetFillColor(ROOT.kYellow)
    trueCopy.Draw("E2")
    hRatioListSD.append( trueCopy)
    padsSD[index][0].Update()
    padsSD[index][1].Update()
    datacanvasesSD[index].Draw()
    datacanvasesSD[index].SaveAs("unfoldedresultsSD_" + str(index) + ".png")

