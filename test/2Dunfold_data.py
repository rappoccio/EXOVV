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
                 help='Runs jec for data, correct options are _jecup : _jecdn : _jerup : _jerdn : or nothing at all to get the nominal')
parser.add_option('--pythia6', action ='store_true', default=False, dest='pythia6')
       
(options, args) = parser.parse_args()

mcfile = TFile('qcdmc_stitched_qcdmc.root')
datafile = TFile('jetht_40pbinv_weighted_dataplots.root')


outfile = TFile('2DData' + options.extension + '.root', 'RECREATE')
outtext = options.extension

response = mcfile.Get('2d_response'+ options.extension)
responseSD = mcfile.Get('2d_response_softdrop' + options.extension)

truth = mcfile.Get('PFJet_pt_m_AK8Gen')
reco = datafile.Get('PFJet_pt_m_AK8')

truthSD = mcfile.Get('PFJet_pt_m_AK8SDgen')
recoSD = datafile.Get('PFJet_pt_m_AK8SD')

truth.Scale( 1./truth.Integral())
reco.Scale( 1. / reco.Integral() )

truthSD.Scale(1./truthSD.Integral() ) 
recoSD.Scale( 1./recoSD.Integral() )

response.Draw('colz')
unfold = RooUnfoldBayes(response, reco, 6)
unfoldSD = RooUnfoldBayes(responseSD, recoSD, 6)
#unfold= RooUnfoldSvd(response, reco, 5);

reco_unfolded = unfold.Hreco()
recoSD_unfolded = unfoldSD.Hreco()

reco_unfolded.Draw()

truth.SetLineColor(4)

truth.Draw('SAME')

canvases = []
canvasesSD = []
namesreco = []
namesrecoSD = []
namesgen = []
namesgenSD = []
legends = []
legendsSD = []
for x in range(0, 7):
    canvases.append(TCanvas("canvas" + str(x)))
    canvasesSD.append(TCanvas("canvasSD" + str(x)))
    namesreco.append(None)
    namesrecoSD.append(None)
    namesgen.append(None)
    namesgenSD.append(None)
    legends.append(TLegend(.7, .5, .9, .7))
    legendsSD.append(TLegend(.7, .5, .9, .7))
pt_bin = {0: '200-240', 1: '240-310', 2: '310-400', 3: '400-530', 4: '530-650', 5: '650-760', 6: '760-Inf'}


for i, canvas in enumerate(canvases) : 
    canvas.cd()
    namesreco[i] = reco_unfolded.ProjectionY('mass' + str(i), i+1, i+1)
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = truth.ProjectionY('genmass' + str(i), i+1, i+1)
    namesgen[i].SetLineColor(4)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('unfolded_results_preplotter_'+ outtext +str(i)+'.png')

for i, canvas in enumerate(canvasesSD) : 
    canvas.cd()
    namesrecoSD[i] = recoSD_unfolded.ProjectionY('massSD' + str(i), i+1, i+1)
    namesrecoSD[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesrecoSD[i].Draw('hist')
    namesgenSD[i] = truthSD.ProjectionY('genmassSD' + str(i), i+1, i+1)
    namesgenSD[i].SetLineColor(2)
    namesgenSD[i].Draw('same hist')
    legendsSD[i].AddEntry(namesrecoSD[i], 'SD Reco', 'l')
    legendsSD[i].AddEntry(namesgenSD[i], 'SD Gen', 'l')
    legendsSD[i].Draw()
    canvas.SaveAs('unfolded_results_softdrop_preplotter_'+ outtext +str(i)+'.png')

canvasespythia6 = []
canvasespythia6SD = []
namegenpythia6 = []
namesgenpythia6SD = []
namesrecopythia6 = []
namesrecopythia6SD = []
legendspythia6 = []
legendspythia6SD = []
for x in range(0, 7):
    canvasespythia6.append(TCanvas("pythia6canvas" + str(x)))
    canvasespythia6SD.append(TCanvas("pythia6canvasSD" + str(x)))
    namesrecopythia6.append(None)
    namesrecopythia6SD.append(None)
    namesgenpythia6SD.append(None)
    namesgenpythia6SD.append(None)
    legendspythia6.append(TLegend(.7, .5, .9, .7))
    legendspythia6SD.append(TLegend(.7, .5, .9, .7))
if options.pythia6:
    pythia6file = TFile('qcdmc_stitched_pythia6.root')
    pythia6truth = pythia6file.Get('PFJet_pt_m_AK8Gen')
    pythia6truthSD = pythia6file.Get('PFJet_pt_m_AK8SDgen')
    unfoldpyth6 = RooUnfoldBayes(pythia6response, reco, 6)
    unfoldpyth6SD = RooUnfoldBayes(pythia6responseSD, recoSD, 6)
    reco_unfolded_pythia6 = unfoldpyth6.HReco()
    reco_unfoldedSD_pythia6 = unfoldpyth6SD.HReco()
    for i, canvas in enumerate(canvasespythia6) : 
        canvas.cd()
        namesrecopythia6[i] = reco_unfolded_pythia6.ProjectionY('pythia6mass' + str(i), i+1, i+1)
        namesrecopythia6[i].SetTitle('Pythia6 Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
        namesrecopythia6[i].Draw('hist')
        namesgenpythia6[i] = pythia6truth.ProjectionY('pythia6genmass' + str(i), i+1, i+1)
        namesgenpythia6[i].SetLineColor(4)
        namesgenpythia6[i].Draw('same hist')
        legendspythia6[i].AddEntry(namesrecopythia6[i], 'Reco', 'l')
        legendspythia6[i].AddEntry(namesgenpythia6[i], 'Gen', 'l')
        legendspythia6[i].Draw()
        canvas.SaveAs('unfolded_results_preplotter_pythia6_'+ outtext +str(i)+'.png')

    for i, canvas in enumerate(canvasespythia6SD) : 
        canvas.cd()
        namesrecopythia6SD[i] = reco_unfoldedSD_pythia6.ProjectionY('pythia6massSD' + str(i), i+1, i+1)
        namesrecopythia6SD[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
        namesrecopythia6SD[i].Draw('hist')
        namesgenpythia6SD[i] = pythia6truthSD.ProjectionY('pythia6genmassSD' + str(i), i+1, i+1)
        namesgenpythia6SD[i].SetLineColor(2)
        namesgenpythia6SD[i].Draw('same hist')
        legendspythia6SD[i].AddEntry(namesrecopythia6SD[i], 'SD Reco', 'l')
        legendspythia6SD[i].AddEntry(namesgenpythia6SD[i], 'SD Gen', 'l')
        legendspythia6SD[i].Draw()
        canvas.SaveAs('unfolded_results_softdrop_preplotter_pythia6_'+ outtext +str(i)+'.png')
    




    
outfile.cd()
for hists in namesreco:
    hists.Write()
for stuff in namesgen:
    stuff.Write()
for more in namesgenSD:
    more.Write()
for evenmore in namesrecoSD:
    evenmore.Write()
outfile.Close()
