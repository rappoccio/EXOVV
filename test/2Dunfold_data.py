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
       
(options, args) = parser.parse_args()

mcfile = TFile('responses_rejec_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')


outfile = TFile('2DData' + options.extension + '.root', 'RECREATE')
outtext = options.extension

response = mcfile.Get('2d_response'+ options.extension)
responseSD = mcfile.Get('2d_response_softdrop' + options.extension)

truth = mcfile.Get('PFJet_pt_m_AK8Gen')
truthSD = mcfile.Get('PFJet_pt_m_AK8SDgen')


if 'nomnom' in options.extension :
    reco = datafile.Get('PFJet_pt_m_AK8_nomnom')
    recoSD = datafile.Get('PFJet_pt_m_AK8SD_nomnom')
else : 
    reco = datafile.Get('PFJet_pt_m_AK8')
    recoSD = datafile.Get('PFJet_pt_m_AK8SD')
    
truth.Scale( 1./truth.Integral())
reco.Scale( 1. / reco.Integral() )

truthSD.Scale(1./truthSD.Integral() ) 
recoSD.Scale( 1./recoSD.Integral() )

response.Draw('colz')
unfold = RooUnfoldBayes(response, reco, 4)
unfoldSD = RooUnfoldBayes(responseSD, recoSD, 4)

reco_unfolded = unfold.Hreco()
recoSD_unfolded = unfoldSD.Hreco()

reco_unfolded.Draw()

truth.SetLineColor(4)

truth.Draw('SAME')

pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11


canvases = []
canvasesSD = []
namesreco = []
namesrecoSD = []
namesgen = []
namesgenSD = []
legends = []
legendsSD = []
for x in range(0, nptbin):
    canvases.append(TCanvas("canvas" + str(x)))
    canvasesSD.append(TCanvas("canvasSD" + str(x)))
    namesreco.append(None)
    namesrecoSD.append(None)
    namesgen.append(None)
    namesgenSD.append(None)
    legends.append(TLegend(.7, .5, .9, .7))
    legendsSD.append(TLegend(.7, .5, .9, .7))


for i, canvas in enumerate(canvases) : 
    canvas.cd()
    namesreco[i] = reco_unfolded.ProjectionX('mass' + str(i), i+1, i+1)
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = truth.ProjectionX('genmass' + str(i), i+1, i+1)
    namesgen[i].SetLineColor(4)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('hists/unfolded_results_preplotter_'+ outtext +str(i)+'.png')

for i, canvas in enumerate(canvasesSD) : 
    canvas.cd()
    namesrecoSD[i] = recoSD_unfolded.ProjectionX('massSD' + str(i), i+1, i+1)
    namesrecoSD[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesrecoSD[i].Draw('hist')
    namesgenSD[i] = truthSD.ProjectionX('genmassSD' + str(i), i+1, i+1)
    namesgenSD[i].SetLineColor(2)
    namesgenSD[i].Draw('same hist')
    legendsSD[i].AddEntry(namesrecoSD[i], 'SD Reco', 'l')
    legendsSD[i].AddEntry(namesgenSD[i], 'SD Gen', 'l')
    legendsSD[i].Draw()
    canvas.SaveAs('hists/unfolded_results_softdrop_preplotter_'+ outtext +str(i)+'.png')
    
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
