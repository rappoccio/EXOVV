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
jecupa = []
jerdna = []
jerupa = []
if options.plotUnc:
    jecdn = ROOT.TFile('2DData_jecdn.root')
    jecup = ROOT.TFile('2DData_jecup.root')
    jerdn = ROOT.TFile('2DData_jerdn.root')
    jerup = ROOT.TFile('2DData_jerup.root')
    for i in range(0, 7):
        print i 
        jecdna.append(jecdn.Get('mass' + str(i)))
        jecupa.append(jecup.Get('mass' + str(i)))
        jerdna.append(jerdn.Get('mass' + str(i)))
        jerupa.append(jerup.Get('mass' + str(i)))


ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

#lumi = 40.

# Variables
d100 =f.Get('mass0')
d200 =f.Get('mass1')
d300 =f.Get('mass2')
d400 =f.Get('mass3')
d500 =f.Get('mass4')
d600 =f.Get('mass5')
d700 =f.Get('mass6')
#d800 =d.Get('unfolded_6')

# Canvases
uc2 = TCanvas("cdist140", "cdist140")
uc3 = TCanvas("cdist200", "cdist200")
uc4 = TCanvas("cdist260", "cdist260")
uc5 = TCanvas("cdist320", "cdist320")
uc6 = TCanvas("cdist400", "cdist400")
uc7 = TCanvas("cdist450", "cdist450")
uc8 = TCanvas("cdist500", "cdist500")

uc2.SetLeftMargin(0.15)
uc3.SetLeftMargin(0.15)
uc4.SetLeftMargin(0.15)
uc5.SetLeftMargin(0.15)
uc6.SetLeftMargin(0.15)
uc7.SetLeftMargin(0.15)
uc8.SetLeftMargin(0.15)

#qtrue140=f.Get("HLT_PFJet140mAK8Gen")
qtrue100=f.Get("genmass0")
qtrue200=f.Get("genmass1")
qtrue260=f.Get("genmass2")
qtrue320=f.Get("genmass3")
qtrue400=f.Get("genmass4")
qtrue450=f.Get("genmass5")
qtrue500=f.Get("genmass6")

leg1 = TLegend(.5, .7, .85, .85)
leg2 = TLegend(.5, .7, .85, .85)
leg3 = TLegend(.5, .7, .85, .85)
leg4 = TLegend(.5, .7, .85, .85)
leg5 = TLegend(.5, .7, .85, .85)
leg6 = TLegend(.5, .7, .85, .85)
leg7 = TLegend(.6, .7, .95, .85)
alegends = [leg1, leg2, leg3, leg4, leg5, leg6, leg7]

tlx1 = ROOT.TLatex()
tlx2 = ROOT.TLatex()
tlx3 = ROOT.TLatex()
tlx4 = ROOT.TLatex()
tlx5 = ROOT.TLatex()
tlx6 = ROOT.TLatex()
tlx7 = ROOT.TLatex()
tlx1pt = ROOT.TLatex()
tlx2pt = ROOT.TLatex()
tlx3pt = ROOT.TLatex()
tlx4pt = ROOT.TLatex()
tlx5pt = ROOT.TLatex()
tlx6pt = ROOT.TLatex()
tlx7pt = ROOT.TLatex()
atlx = [tlx1, tlx2, tlx3, tlx4, tlx5, tlx6, tlx7]
atlxpt= [tlx1pt, tlx2pt, tlx3pt, tlx4pt, tlx5pt, tlx6pt, tlx7pt]
datacanvases= [uc2, uc3, uc4, uc5, uc6, uc7, uc8]
#pt_bin = {0: '230-320', 1: '320-410', 2: '410-515', 3: '515-610', 4: '610-640', 5: '640-700', 6: '700-Inf'}
ptbins = ['#bf{p_{T} 200-240 GeV}','#bf{p_{T} 240-310 GeV}','#bf{p_{T} 310-400 GeV}','#bf{p_{T} 400-530 GeV}','#bf{p_{T} 530-650 GeV}','#bf{p_{T} 650-760 GeV}', '#bf{p_{T} >760 GeV}']
pads = []
hRatioList = []


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

datalist = [d100, d200, d300, d400, d500, d600, d700]
MCtruth = [qtrue100, qtrue200, qtrue260, qtrue320, qtrue400, qtrue450, qtrue500]

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
    alegends[index].AddEntry(MCtruth[index], 'PYTHIA 8', 'l')
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


