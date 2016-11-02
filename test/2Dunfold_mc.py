import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
from ROOT import RooUnfoldSvd


from optparse import OptionParser
parser = OptionParser()

parser.add_option('--extension', action ='store', type = 'string',
                 default ='',
                 dest='extension',
                 help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : _jmrup : _jmrdn : _jmrnom or nothing at all to get the nominal')

                                
(options, args) = parser.parse_args()

myfile = TFile('responses_repdf_otherway_qcdmc_2dplots.root')


response = myfile.Get('2d_response' + options.extension )
outtext = options.extension
truth = myfile.Get('PFJet_pt_m_AK8Gen')
<<<<<<< HEAD
reco = myfile.Get('PFJet_pt_m_AK8')
responseSD = myfile.Get('2d_response_softdrop' + options.extension )
=======
>>>>>>> 7bff57e... Something went screwy
truthSD = myfile.Get('PFJet_pt_m_AK8SDgen')
recoSD = myfile.Get('PFJet_pt_m_AK8SD')
response.Draw('colz')

truth.Scale(1./truth.Integral())
reco.Scale(1./reco.Integral())

truthSD.Scale(1./truthSD.Integral())
recoSD.Scale(1./recoSD.Integral())

pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11
ROOT.gStyle.SetOptStat(000000)



unfold = RooUnfoldBayes(response, reco, 4)
unfoldSD = RooUnfoldBayes(responseSD, recoSD, 4)


reco_unfolded = unfold.Hreco()
span = reco_unfolded.ProjectionX()
span.SetName('pyth8_spanmass')
reco_unfoldedSD = unfoldSD.Hreco()
sdspan = reco_unfoldedSD.ProjectionX()
sdspan.SetName('pyth8_spanmassSD')

reco_unfolded.Draw()

c2=TCanvas()
c2.cd()

reco_unfoldedSD.Draw()
truth.SetLineColor(4)

truth.Draw('SAME')



################### New Correlation matrix stuff
cov = unfold.Ereco()
covSD = unfoldSD.Ereco()

nb= cov.GetNrows()
import math
cor = ROOT.TH2F("cor", "", nb, 0, nb, nb, 0, nb)
corSD = ROOT.TH2F("corSD", "", nb, 0, nb, nb, 0, nb)


for i in xrange(0,nb) :
    for j in xrange(0,nb) :
        Viijj = cov[i][i] * cov[j][j]
        if Viijj>0.0 :
            cor.SetBinContent(i+1, j+1, cov[i][j]/math.sqrt(Viijj))
        
for i in xrange(0,nb) :
    for j in xrange(0,nb) :
        Viijj = covSD[i][i] * covSD[j][j]
        if Viijj>0.0 :
            corSD.SetBinContent(i+1,j+1, covSD[i][j]/math.sqrt(Viijj) )

import array
Number = 3
Red    = array.array("d", [ 0.00, 1.00, 1.00] );
Green  = array.array("d", [ 0.00, 1.00, 140/255.] );
Blue   = array.array("d", [ 1.00, 1.00, 0.00] );
Length = array.array("d", [ 0.00, 0.51, 1.00] );
nb = 10
ROOT.TColor.CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);

#colors = array.array("i", [ROOT.kBlue, ROOT.kWhite, ROOT.kOrange + 7] )

#ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
#ROOT.gStyle.SetPalette(3, colors)#

ptbins =[  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300]

axislabels = ROOT.TH2F("axes", ";Reconstructed Bin;Generated Bin", len(ptbins), 0, cor.GetNbinsX(), len(ptbins), 0, cor.GetNbinsX() )
for ibin in xrange(len(ptbins)):
    axislabels.GetXaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )
    axislabels.GetYaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )

cov_canvas = ROOT.TCanvas("cov_canvas", "response", 800, 800)
cov_canvas.SetRightMargin(0.15)
cov_canvas.SetLeftMargin(0.15)
cov_canvas.SetBottomMargin(0.15)
cov_canvas.SetTopMargin(0.15)
cov_canvas.SetGrid()
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.SetTitle(';Response Matrix Reconstructed p_{T} Bins (GeV);Response Matrix Generated p_{T} Bins (GeV)')
axislabels.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetXaxis().SetTitleOffset(1.5)
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.Draw("axis")
cor.SetMinimum(-1.0)
cor.SetMaximum(1.0)
cor.SetTitle(';Reconstructed bin;Generated bin')
cor.Draw("colz same")
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Ungroomed Jets")
cov_canvas.Update()
cov_canvas.Print("CovarianceMatrix.png", "png")
cov_canvas.Print("CovarianceMatrix.pdf", "pdf")

covSD_canvas=TCanvas("covSDcanvas", "covSDcanvas", 800, 800)
covSD_canvas.SetRightMargin(0.15)
covSD_canvas.SetLeftMargin(0.15)
covSD_canvas.SetBottomMargin(0.15)
covSD_canvas.SetTopMargin(0.15)
covSD_canvas.SetGrid()
covSD_canvas.cd()
axislabels.Draw("axis")
corSD.SetMinimum(-1.0)
corSD.SetMaximum(1.0)
corSD.SetTitle(';Reconstructed bin;Generated bin')
corSD.Draw("colz same")
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Soft Drop Jets")

covSD_canvas.Update()
covSD_canvas.Print("CovarianceMatrixSD.png", "png")
covSD_canvas.Print("CovarianceMatrixSD.pdf", "pdf")
###################





canvases = []
namesreco = []
namesgen = []
legends = []
canvasesSD = []
legendsSD = []
namesrecoSD = []
namesgenSD = []
keepHists = []
for i in range(0, nptbin):
    namesreco.append(None)
    namesgen.append(None)
    legends.append(TLegend(.7, .5, .9, .7))
    canvases.append(TCanvas())
    canvasesSD.append(TCanvas())
    legendsSD.append(TLegend(.7, .5, .9, .7))
    namesrecoSD.append(None)
    namesgenSD.append(None)

for i, canvas in enumerate(canvases) : 
    canvas.cd()
    ihist = namesreco[i] = reco_unfolded.ProjectionX('pythia8_mass' + str(i), i+1, i+1)
    keepHists.append( ihist )
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesreco[i].Draw('hist')
    ihist = namesgen[i] = truth.ProjectionX('genmass' + str(i), i+1 , i+1)
    keepHists.append( ihist) 
    namesgen[i].SetLineColor(2)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('hists/unfolded_closure_preplotter_'+pt_bin[i] + options.extension + '.png')

for i, canvas in enumerate(canvasesSD):
    canvas.cd()
    ihist = namesrecoSD[i] = reco_unfoldedSD.ProjectionX('pythia8_massSD' + str(i), i+1, i+1)
    keepHists.append(ihist)
    namesrecoSD[i].SetTitle('SD Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesrecoSD[i].Draw('hist')
    ihist = namesgenSD[i] = truthSD.ProjectionX('genmassSD' + str(i), i+1, i+1)
    keepHists.append(ihist)
    namesgenSD[i].SetLineColor(2)
    namesgenSD[i].Draw('same hist')
    legendsSD[i].AddEntry(namesrecoSD[i], 'SD Reco', 'l')
    legendsSD[i].AddEntry(namesgenSD[i], 'SD Gen', 'l')
    legendsSD[i].Draw()
    canvas.SaveAs('hists/unfolded_closure_softdrop_preplotter_' + pt_bin[i] + options.extension + '.png')    


outfile = TFile('2DClosure' + options.extension + '.root', 'RECREATE')
outfile.cd()
for hists in namesreco:
    hists.Write()
for stuff in namesgen:
    stuff.Write()
for morestuff in namesrecoSD:
    morestuff.Write()
for evenmore in namesgenSD:
    evenmore.Write()
span.Write()
sdspan.Write()
outfile.Write()
outfile.Close()
