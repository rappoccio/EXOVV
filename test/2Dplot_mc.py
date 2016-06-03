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

scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./9240.]


jecdna = []
jecupa = []
jerdna = []
jerupa = []
jecdnaSD = []
jecupaSD = []
jerdnaSD = []
jerupaSD = []
ps = []
ps_softdrop = []
ps_differences = []
ps_differences_softdrop = []
jecdn = ROOT.TFile('2DClosure_jecdn.root')
jecup = ROOT.TFile('2DClosure_jecup.root')
jerdn = ROOT.TFile('2DClosure_jerdn.root')
jerup = ROOT.TFile('2DClosure_jerup.root')
for i in range(0, 7):
    jecdna.append(jecdn.Get('pythia8_mass' + str(i)))
    jecupa.append(jecup.Get('pythia8_mass' + str(i)))
    jerdna.append(jerdn.Get('pythia8_mass' + str(i)))
    jerupa.append(jerup.Get('pythia8_mass' + str(i)))
    jecdnaSD.append(jecdn.Get('pythia8_massSD' + str(i)))
    jecupaSD.append(jecup.Get('pythia8_massSD' + str(i)))
    jerdnaSD.append(jerdn.Get('pythia8_massSD' + str(i)))
    jerupaSD.append(jerup.Get('pythia8_massSD' + str(i)))
    
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
#d800 =d.Get('unfolded_6')
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
for i in datacanvases:
    index = datacanvases.index(i)
    pads[index][0].cd()
    pads[index][0].SetLogy()
    datalist[index].UseCurrentStyle()
    MCtruth[index].UseCurrentStyle()
    
    datalist[index].Scale(scales[index])
    MCtruth[index].Scale(scales[index])
    ################################## Uncertainties
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
    hRecoCopy = hReco.Clone()
    for ibin in xrange(1, hRecoCopy.GetNbinsX()):
        temp = hRecoCopy.GetBinError(ibin)
        hRecoCopy.SetBinError(ibin, temp + ps_differences[index][ibin-1] )
    ################################## Make top plot nice
    hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoCopy.SetMarkerStyle(20)
    hRecoCopy.SetAxisRange(1e-11, 1, "Y")
    hRecoCopy.SetFillColor(ROOT.kGreen)
    hRecoCopy.Draw("E2")
    hRecoCopy.Draw("E same")
    hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( 1e-11, 1, "Y")
    hReco.SetFillColor(ROOT.kYellow)
    hReco.Draw("E2 same")
    hReco.Draw("E same")
    MCtruth[index].SetLineColor(2)
    #MCtruth[index].Scale(lumi)
    MCtruth[index].Draw( "hist SAME" )
    atlx[index].DrawLatex(0.131, 0.926, "CMS Preliminary #sqrt{s}=13 TeV, 40 pb^{-1}")
    atlxpt[index].DrawLatex(0.555, 0.559, ptbins[index])
    ################################## legends
    alegends[index].AddEntry(MCtruth[index], 'Pythia8', 'l')
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
    histstokeep.append( [datcopycopy,datcopy,trueCopy])
    for ibin in xrange(1,datcopy.GetNbinsX()):
        if datcopy.GetBinContent(ibin) > 0: 
            datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
            datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
        else:
            datcopy.SetBinError(ibin, 0)
            datcopycopy.SetBinError(ibin, 0)
        datcopy.SetBinContent(ibin, 1.0)
        datcopycopy.SetBinContent(ibin, 1.0)
    trueCopy.Divide( trueCopy, hReco, 1.0, 1.0, "B" )
    pads[index][1].cd()
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
    datcopy.GetYaxis().SetTitle("Theory/Unfolded")
    datcopycopy.GetYaxis().SetTitle("Theory/Unfolded")
    trueCopy.SetLineStyle(2)
    trueCopy.SetLineColor(2)
    datcopy.SetFillColor(ROOT.kYellow)
    datcopycopy.Draw('e2')
    datcopy.Draw('e2 same')
    datcopy.SetMarkerStyle(0)
    trueCopy.Draw("hist same")
    
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
    hRecoCopy.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{1}{20GeV^{2}})")
    hRecoCopy.SetMarkerStyle(20)
    hRecoCopy.SetAxisRange(1e-11, 1, "Y")
    hRecoCopy.SetFillColor(ROOT.kGreen)
    hRecoCopy.Draw("E2")
    hRecoCopy.Draw("E same")
    ################################## Make top plot nice
    hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dmdp_{T}} (#frac{pb}{20GeV^{2}})")
    hReco.SetMarkerStyle(20)
    hReco.SetAxisRange( 1e-11, 1, "Y")
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
    alegendsSD[index].AddEntry(MCtruth[index], 'Pythia8 SoftDrop', 'l')
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
    histstokeep.append( [datcopycopy,datcopy,trueCopy])
    for ibin in xrange(1,datcopy.GetNbinsX()):
        if datcopy.GetBinContent(ibin) > 0: 
            datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
            datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
        else:
            datcopy.SetBinError(ibin, 0)
            datcopycopy.SetBinError(ibin, 0)
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
    trueCopy.SetLineStyle(2)
    trueCopy.SetLineColor(2)
    datcopy.SetFillColor(ROOT.kYellow)
    datcopycopy.Draw('e2')
    datcopy.Draw('e2 same')
    datcopy.SetMarkerStyle(0)
    trueCopy.Draw("hist same")    
    hRatioListSD.append( trueCopy)
    padsSD[index][0].Update()
    padsSD[index][1].Update()
    datacanvasesSD[index].Draw()
    datacanvasesSD[index].SaveAs("unfoldedclosure_softdrop_" + str(index) + ".png")












'''

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
'''
