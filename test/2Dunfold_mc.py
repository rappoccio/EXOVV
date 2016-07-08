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


myfile = TFile('qcdmc_stitched_qcdmc.root')

response = myfile.Get('2d_response' + options.extension )
outtext = options.extension
truth = myfile.Get('PFJet_pt_m_AK8Gen')
reco = myfile.Get('PFJet_pt_m_AK8')
responseSD = myfile.Get('2d_response_softdrop' + options.extension )
truthSD = myfile.Get('PFJet_pt_m_AK8SDgen')
recoSD = myfile.Get('PFJet_pt_m_AK8SD')
response.Draw('colz')

truth.Scale(1./truth.Integral())
reco.Scale(1./reco.Integral())

truthSD.Scale(1./truthSD.Integral())
recoSD.Scale(1./recoSD.Integral())

pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-1400', 12:'1400-1500', 13:'1500-1600', 14:'1600-1700', 15:'1700-1800', 16:'1800-1900', 17:'1900-2000', 18:'2000-Inf'}




unfold = RooUnfoldBayes(response, reco, 4)
unfoldSD = RooUnfoldBayes(responseSD, recoSD, 4)


reco_unfolded = unfold.Hreco()
reco_unfoldedSD = unfoldSD.Hreco()

reco_unfolded.Draw()

c2=TCanvas()
c2.cd()

reco_unfoldedSD.Draw()
truth.SetLineColor(4)

truth.Draw('SAME')


canvases = []
namesreco = []
namesgen = []
legends = []
canvasesSD = []
legendsSD = []
namesrecoSD = []
namesgenSD = []
keepHists = []
for i in range(0, 19):
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
    ihist = namesreco[i] = reco_unfolded.ProjectionY('pythia8_mass' + str(i), i+1, i+1)
    keepHists.append( ihist )
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesreco[i].Draw('hist')
    ihist = namesgen[i] = truth.ProjectionY('genmass' + str(i), i+1 , i+1)
    keepHists.append( ihist) 
    namesgen[i].SetLineColor(2)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('unfolded_closure_preplotter_'+pt_bin[i] + options.extension + '.png')

for i, canvas in enumerate(canvasesSD):
    canvas.cd()
    ihist = namesrecoSD[i] = reco_unfoldedSD.ProjectionY('pythia8_massSD' + str(i), i+1, i+1)
    keepHists.append(ihist)
    namesrecoSD[i].SetTitle('SD Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesrecoSD[i].Draw('hist')
    ihist = namesgenSD[i] = truthSD.ProjectionY('genmassSD' + str(i), i+1, i+1)
    keepHists.append(ihist)
    namesgenSD[i].SetLineColor(2)
    namesgenSD[i].Draw('same hist')
    legendsSD[i].AddEntry(namesrecoSD[i], 'SD Reco', 'l')
    legendsSD[i].AddEntry(namesgenSD[i], 'SD Gen', 'l')
    legendsSD[i].Draw()
    canvas.SaveAs('unfolded_closure_softdrop_preplotter_' + pt_bin[i] + options.extension + '.png')    


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
outfile.Write()
outfile.Close()
