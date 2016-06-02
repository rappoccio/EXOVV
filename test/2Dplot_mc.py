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
parser.add_option('--pythia6', action ='store_true', default=False, dest='pythia6')
                                 
(options, args) = parser.parse_args()


f = ROOT.TFile('2DClosure.root')
jecdna = []
jecupa = []
jerdna = []
jerupa = []
jecdnSDa = []
jecupSDa = []
jerdnSDa = []
jerupSDa = []

pythia6jecdna = []
pythia6jecupa = []
pythia6jerdna = []
pythia6jerupa = []
pythia6jecdnSDa = []
pythia6jecupSDa = []
pythia6jerdnSDa = []
pythia6jerupSDa = []


if options.plotUnc:
    jecdn = ROOT.TFile('2DClosure_jecdn.root')
    jecup = ROOT.TFile('2DClosure_jecup.root')
    jerdn = ROOT.TFile('2DClosure_jerdn.root')
    jerup = ROOT.TFile('2DClosure_jerup.root')
    for i in range(0, 7):
         
        jecdna.append(jecdn.Get('mass' + str(i)))
        jecupa.append(jecup.Get('mass' + str(i)))
        jerdna.append(jerdn.Get('mass' + str(i)))
        jerupa.append(jerup.Get('mass' + str(i)))
        jecdnSDa.append(jecdn.Get('massSD' + str(i)))
        jecupSDa.append(jecup.Get('massSD' + str(i)))
        jerdnSDa.append(jerdn.Get('massSD' + str(i)))
        jerupSDa.append(jerup.Get('massSD' + str(i)))
    if options.pythia6:
        for i in range(0, 7):
            pythia6jecdna.append(jecdn.Get('pythia6mass' + str(i)))
            pythia6jecupa.append(jecup.Get('pythia6mass' + str(i)))
            pythia6jerdna.append(jerdn.Get('pythia6mass' + str(i)))
            pythia6jerupa.append(jerup.Get('pythia6mass' + str(i)))
            pythia6jecdnSDa.append(jecdn.Get('pythia6massSD' + str(i)))
            pythia6jecupSDa.append(jecup.Get('pythia6massSD' + str(i)))
            pythia6jerdnSDa.append(jerdn.Get('pythia6massSD' + str(i)))
            pythia6jerupSDa.append(jerup.Get('pythia6massSD' + str(i)))
        
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

#lumi = 40.
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


pythia6uc2 = TCanvas("pythia6cdist140", "pythia6cdist140")
pythia6uc3 = TCanvas("pythia6cdist200", "pythia6cdist200")
pythia6uc4 = TCanvas("pythia6cdist260", "pythia6cdist260")
pythia6uc5 = TCanvas("pythia6cdist320", "pythia6cdist320")
pythia6uc6 = TCanvas("pythia6cdist400", "pythia6cdist400")
pythia6uc7 = TCanvas("pythia6cdist450", "pythia6cdist450")
pythia6uc8 = TCanvas("pythia6cdist500", "pythia6cdist500")

pythia6ucsd2 = TCanvas("pythia6cdist140SD","pythia6cdist140SD")
pythia6ucsd3 = TCanvas("pythia6cdist200SD","pythia6cdist200SD")
pythia6ucsd4 = TCanvas("pythia6cdist260SD","pythia6cdist260SD")
pythia6ucsd5 = TCanvas("pythia6cdist320SD","pythia6cdist320SD")
pythia6ucsd6 = TCanvas("pythia6cdist400SD","pythia6cdist400SD")
pythia6ucsd7 = TCanvas("pythia6cdist450SD","pythia6cdist450SD")
pythia6ucsd8 = TCanvas("pythia6cdist500SD","pythia6cdist500SD")


pythia6datacanvasesSD = [pythia6ucsd2, pythia6ucsd3, pythia6ucsd4, pythia6ucsd5, pythia6ucsd6, pythia6ucsd7, pythia6ucsd8]
pythia6datacanvases= [pythia6uc2, pythia6uc3, pythia6uc4, pythia6uc5, pythia6uc6, pythia6uc7, pythia6uc8]


# Variables

datalist = []
datalistSD = []
pythia6datalist = []
pythia6datalistSD = []

MCtruth = []
MCtruthSD = []
pythia6MCtruth = []
pythia6MCtruthSD = []

atlx = []
atlxpt = []
alegends = []
alegendsSD = []
atlxSD = []
atlxSDpt = []
pythia6atlx = []
pythia6atlxpt = []
pythia6alegends = []
pythia6alegendsSD = []
pythia6atlxSD = []
pythia6atlxSDpt = []

for x in range(0, 7):
    if options.pythia6:
        pythia6datalist.append(f.Get('pythia6mass' + str(x)))
        pythia6datalistSD.append(f.Get('pythia6massSD'+str(x)))
        pythia6MCtruth.append(f.Get('pythia6genmass'+str(x)))
        pythia6MCtruthSD.append(f.Get('pythia6genmassSD'+str(x)))
    datalistSD.append(f.Get('massSD'+str(x)))
    datalist.append(f.Get('mass'+str(x)))
    MCtruth.append(f.Get('genmass' + str(x)))
    MCtruthSD.append(f.Get('genmassSD' + str(x)))
    atlx.append(ROOT.TLatex())
    pythia6atlx.append(ROOT.TLatex())
    atlxpt.append(ROOT.TLatex())
    pythia6atlxpt.append(ROOT.TLatex())
    atlxSD.append(ROOT.TLatex())
    pythia6atlxSD.append(ROOT.TLatex())
    atlxSDpt.append(ROOT.TLatex())
    pythia6atlxSDpt.append(ROOT.TLatex())
    alegends.append(TLegend(.5, .7, .85, .85))
    pythia6alegends.append(TLegend(.5, .7, .85, .85))
    alegendsSD.append(TLegend(.5, .7, .85, .85))
    pythia6alegendsSD.append(TLegend(.5, .7, .85, .85))
    datacanvases[x].SetLeftMargin(0.15)
    pythia6datacanvases[x].SetLeftMargin(0.15)
    datacanvasesSD[x].SetLeftMargin(0.15)
    pythia6datacanvasesSD[x].SetLeftMargin(0.15)
#d800 =d.Get('unfolded_6')

# Canvases
ptbins = ['#bf{p_{T} 200-240 GeV}','#bf{p_{T} 240-310 GeV}','#bf{p_{T} 310-400 GeV}','#bf{p_{T} 400-530 GeV}','#bf{p_{T} 530-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} >760 GeV}']


pads = []
padsSD = []
hRatioList = []
hRatioListSD = []

pythia6pads = []
pythia6padsSD = []
pythia6hRatioList = []
pythia6hRatioListSD = []


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

for b in pythia6atlx:
    b.SetNDC()
    b.SetTextFont(43)
    b.SetTextSize(30)
for b in pythia6atlxSD:
    b.SetNDC()
    b.SetTextFont(43)
    b.SetTextSize(30)
for g in pythia6atlxpt:
    g.SetNDC()
    g.SetTextFont(43)
    g.SetTextSize(25)
for g in pythia6atlxSDpt:
    g.SetNDC()
    g.SetTextFont(43)
    g.SetTextSize(25)
for leg in pythia6alegends :
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
for leg in pythia6alegendsSD :
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
setup(pythia6datacanvases, pythia6pads)
setup(pythia6datacanvasesSD, pythia6padsSD)


def closure_plot(data_canvases_to_plot, jec_up, jec_down, jer_up, jer_down):
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
        hReco.SetTitle(";; #frac{d#sigma}{dmdp_{T}} (#frac{pb}{GeV^{2}})")
        hReco.SetMarkerStyle(20)
        hReco.SetAxisRange( .0001, 1000000, "Y")
        hReco.SetFillStyle(1001)
        hReco.SetFillColor(ROOT.kYellow)
        hReco.Draw("E2")
        hReco.Draw("E same")
        MCtruth[index].SetLineColor(2)
        #MCtruth[index].Scale(lumi)
        MCtruth[index].Draw( "hist SAME" )
        atlx[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
        atlxpt[index].DrawLatex(0.555, 0.559, ptbins[index])
        ################################## legends
        alegends[index].AddEntry(MCtruth[index], 'PYTHIA 8', 'l')
        alegends[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
        alegends[index].Draw()
        #################################### ratio plot stuff
        trueCopy = MCtruth[index].Clone()
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
        pads[index][1].cd()
        trueCopy.SetTitle(";Jet Mass (GeV);Theory/Reco")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(3)
        trueCopy.SetMinimum(0)
        trueCopy.SetMaximum(2)
        trueCopy.GetYaxis().SetNdivisions(2,4,0,False)
        trueCopy.SetFillStyle(1001)
        trueCopy.SetFillColor(ROOT.kYellow)
        trueCopy.Draw("E2")
        hRatioList.append( trueCopy)
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
    ################################## Uncertainties
    hReco = datalistSD[index]
    nom = datalistSD[index]
    jesUP  = jecupSDa[index]
    jesDOWN = jecdnSDa[index]
    jerUP  = jerupSDa[index]
    jerDOWN = jerdnSDa[index]
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
    alegendsSD[index].AddEntry(MCtruth[index], 'PYTHIA 8 w/ MMDT Beta = 0', 'l')
    alegendsSD[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
    alegendsSD[index].Draw()
    #################################### ratio plot stuff
    trueCopy = MCtruthSD[index].Clone()
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    padsSD[index][1].cd()
    trueCopy.SetTitle(";Jet Mass (GeV);Theory/Reco")
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
    datacanvasesSD[index].SaveAs("unfoldedclosureSD_" + str(index) + ".png")

if options.pythia6:
    for i in pythia6datacanvases:
        index = pythia6datacanvases.index(i)
        pythia6pads[index][0].cd()
        pythia6pads[index][0].SetLogy()
        pythia6datalist[index].UseCurrentStyle()
        pythia6MCtruth[index].UseCurrentStyle()
        ################################## Uncertainties
        hReco = pythia6datalist[index]
        nom = pythia6datalist[index]
        jesUP  = pythia6jecupa[index]
        jesDOWN = pythia6jecdna[index]
        jerUP  = pythia6jerupa[index]
        jerDOWN = pythia6jerdna[index]
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
        pythia6MCtruth[index].SetLineColor(2)
        #MCtruth[index].Scale(lumi)
        pythia6MCtruth[index].Draw( "hist SAME" )
        pythia6atlx[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
        pythia6atlxpt[index].DrawLatex(0.555, 0.559, ptbins[index])
        ################################## legends
        pythia6alegends[index].AddEntry(pythia6MCtruth[index], 'PYTHIA 8 w/ Pythia 6', 'l')
        pythia6alegends[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
        pythia6alegends[index].Draw()
        #################################### ratio plot stuff
        trueCopy = pythia6MCtruth[index].Clone()
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
        pads[index][1].cd()
        trueCopy.SetTitle(";Jet Mass (GeV);Theory/Data")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(3)
        trueCopy.SetMinimum(0)
        trueCopy.SetMaximum(2)
        trueCopy.GetYaxis().SetNdivisions(2,4,0,False)
        trueCopy.SetFillStyle(1001)
        trueCopy.SetFillColor(ROOT.kYellow)
        trueCopy.Draw("E2")
        hRatioList.append( trueCopy)
        pythia6pads[index][0].Update()
        pythia6pads[index][1].Update()
        pythia6datacanvases[index].Draw()
        pythia6datacanvases[index].SaveAs("unfoldeduncertainty_pythia6_" + str(index) + ".png")

    for i in pythia6datacanvasesSD:
        index = pythia6datacanvasesSD.index(i)
        pythia6padsSD[index][0].cd()
        pythia6padsSD[index][0].SetLogy()
        pythia6datalistSD[index].UseCurrentStyle()
        pythia6MCtruthSD[index].UseCurrentStyle()
        ################################## Uncertainties
        hReco = pythia6datalistSD[index]
        nom = pythia6datalistSD[index]
        jesUP  = pythia6jecupSDa[index]
        jesDOWN = pythia6jecdnSDa[index]
        jerUP  = pythia6jerupSDa[index]
        jerDOWN = pythia6jerdnSDa[index]
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
        pythia6MCtruthSD[index].SetLineColor(2)
        #MCtruth[index].Scale(lumi)
        pythia6MCtruthSD[index].Draw( "hist SAME" )
        pythia6atlxSD[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
        pythia6atlxSDpt[index].DrawLatex(0.555, 0.559, ptbins[index])
        ################################## legends
        pythia6alegendsSD[index].AddEntry(pythia6MCtruth[index], 'PYTHIA 8 w/ Pythia6 & MMDT Beta = 0', 'l')
        pythia6alegendsSD[index].AddEntry(hReco, 'Exp + Stat Uncertainty', 'f')
        pythia6alegendsSD[index].Draw()
        #################################### ratio plot stuff
        trueCopy = pythia6MCtruthSD[index].Clone()
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
        pythia6padsSD[index][1].cd()
        trueCopy.SetTitle(";Jet Mass (GeV);Theory/Reco")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(3)
        trueCopy.SetMinimum(0)
        trueCopy.SetMaximum(2)
        trueCopy.GetYaxis().SetNdivisions(2,4,0,False)
        trueCopy.SetFillStyle(1001)
        trueCopy.SetFillColor(ROOT.kYellow)
        trueCopy.Draw("E2")
        hRatioListSD.append( trueCopy)
        pythia6padsSD[index][0].Update()
        pythia6padsSD[index][1].Update()
        pythia6datacanvasesSD[index].Draw()
        pythia6datacanvasesSD[index].SaveAs("unfoldeduncertaintySD_pythia6_" + str(index) + ".png")