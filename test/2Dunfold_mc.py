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
                 help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : or nothing at all to get the nominal')
                                
(options, args) = parser.parse_args()


myfile = TFile('qcdmc_stitched_qcdmc.root')

outtext = ''
outfile = None


response = myfile.Get('2d_response' + options.extension )
outfile = TFile('2DClosure' + options.extension + '.root', 'RECREATE')
outtext = options.extension
truth = myfile.Get('PFJet_pt_m_AK8Gen')
reco = myfile.Get('PFJet_pt_m_AK8')

responseSD = myfile.Get('2d_response_softdrop' + options.extension )
truthSD = myfile.Get('PFJet_pt_m_AK8SDgen')
recoSD = myfile.Get('PFJet_pt_m_AK8SD')

response.Draw('colz')


unfold = RooUnfoldBayes(response, reco, 6)
unfoldSD = RooUnfoldBayes(responseSD, recoSD, 6)
#unfold= RooUnfoldSvd(response, reco, 5);

reco_unfolded = unfold.Hreco()
reco_unfoldedSD = unfoldSD.Hreco()

reco_unfolded.Draw()

c2=TCanvas()
c2.cd()

reco_unfoldedSD.Draw()
truth.SetLineColor(4)

truth.Draw('SAME')

pt_bin = {0: '200-240', 1: '240-310', 2: '310-400', 3: '400-530', 4: '530-650', 5: '650-760', 6: '760-Inf'}

canvases = []
namesreco = []
namesgen = []
legends = []
canvasesSD = []
legendsSD = []
namesrecoSD = []
namesgenSD = []
for i in range(0, 7):
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
    namesreco[i] = reco_unfolded.ProjectionY('mass' + str(i), i+1, i+1)
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = truth.ProjectionY('genmass' + str(i), i+1 , i+1)
    namesgen[i].SetLineColor(2)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('unfolded_closure_preplotter_'+pt_bin[i] + options.extension + '.png')

for i, canvas in enumerate(canvasesSD):
    canvas.cd()
    namesrecoSD[i] =  reco_unfoldedSD.ProjectionY('massSD' + str(i), i+1, i+1)
    namesrecoSD[i].SetTitle('SD Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesreco[i].Draw('hist')
    namesgenSD[i] = truthSD.ProjectionY('genmassSD' + str(i), i+1, i+1)
    namesgenSD[i].SetLineColor(2)
    namesgenSD[i].Draw('same hist')
    legendsSD[i].AddEntry(namesrecoSD[i], 'SD Reco', 'l')
    legendsSD[i].AddEntry(namesgenSD[i], 'SD Gen', 'l')
    legendsSD[i].Draw()
    canvas.SaveAs('unfolded_closure_softdrop_preplotter_'+pt_bin[i]+options.extension + '.png')    



outfile.cd()
for hists in namesreco:
    hists.Write()
for stuff in namesgen:
    stuff.Write()
for morestuff in namesrecoSD:
    morestuff.Write()
for evenmore in namesgenSD:
    evenmore.Write()
outfile.Write()
outfile.Close()
