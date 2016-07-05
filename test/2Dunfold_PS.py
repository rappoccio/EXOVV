import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
# dict used later for labels

pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-Inf'}


pythia6file = TFile('qcdmc_stitched_pythia6.root')
pythia8file = TFile('qcdmc_stitched_qcdmc.root')
datafile = TFile('jetht_run2015B_weighted_plots.root')


pythia6_response = pythia6file.Get('2d_response')
pythia6_response_softdrop = pythia6file.Get('2d_response_softdrop')

pythia8_response = pythia8file.Get('2d_response')
pythia8_response_softdrop = pythia8file.Get('2d_response_softdrop')

# Get data hists and normalize
data_reco = datafile.Get('PFJet_pt_m_AK8')
data_reco_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

data_reco.Scale(1./data_reco.Integral())
data_reco_softdrop.Scale(1./data_reco_softdrop.Integral())

# get pythia 8 reco and normalize
pythia8_reco = pythia8file.Get('PFJet_pt_m_AK8')
pythia8_reco_softdrop = pythia8file.Get('PFJet_pt_m_AK8SD')
pythia8_reco.Scale(1./pythia8_reco.Integral())
pythia8_reco_softdrop.Scale(1./pythia8_reco_softdrop.Integral())

# get pythia6 reco and normalize
pythia6_reco = pythia6file.Get('PFJet_pt_m_AK8')
pythia6_reco_softdrop = pythia6file.Get('PFJet_pt_m_AK8SD')
pythia6_reco.Scale(1./pythia6_reco.Integral())
pythia6_reco_softdrop.Scale(1./pythia6_reco_softdrop.Integral())

# get truth and normalize it
pythia8_gen = pythia8file.Get('PFJet_pt_m_AK8Gen')
pythia8_gen_softdrop = pythia8file.Get('PFJet_pt_m_AK8SDgen')
pythia8_gen.Scale(1./pythia8_gen.Integral())
pythia8_gen_softdrop.Scale(1./pythia8_gen_softdrop.Integral())

pythia6_gen = pythia6file.Get('PFJet_pt_m_AK8Gen')
pythia6_gen_softdrop = pythia6file.Get('PFJet_pt_m_AK8SDgen')
pythia6_gen.Scale(1./pythia6_gen.Integral())
pythia6_gen_softdrop.Scale(1./pythia6_gen_softdrop.Integral())

# unfold the UNGROOMED pythia8 reco with pythia6 response matrix and partition into pt bins
unfold_ps = RooUnfoldBayes(pythia6_response, pythia8_reco, 3)
unfolded_ps = unfold_ps.Hreco()

canvases = []
namesreco = []
namesgen = []
legends = []
for x in range(0, 7):
    canvases.append(TCanvas("canvas" + str(x)))
    namesreco.append(None)
    namesgen.append(None)
    legends.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases) : 
    canvas.cd()
    namesreco[i] = unfolded_ps.ProjectionY('pythia8_unfolded_by_pythia6' + str(i), i+1, i+1)
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = pythia8_gen.ProjectionY('pythia8_gen' + str(i), i+1, i+1)
    namesgen[i].SetLineColor(4)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('partonshower_unc_test'+str(i)+'.png')

# unfold the SoftDrop pythia8 reco with pythia6 response matrix and partition into pt bins

unfold_ps_softdrop = RooUnfoldBayes(pythia6_response_softdrop, pythia8_reco_softdrop, 3)
unfolded_ps_softdrop = unfold_ps_softdrop.Hreco()

canvases_softdrop = []
namesreco_softdrop = []
namesgen_softdrop = []
legends_softdrop = []

for x in range(0, 7):
    canvases_softdrop.append(TCanvas("canvas_softdrop" + str(x)))
    namesreco_softdrop.append(None)
    namesgen_softdrop.append(None)
    legends_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_softdrop) : 
    canvas.cd()
    namesreco_softdrop[i] = unfolded_ps_softdrop.ProjectionY('pythia8_unfolded_by_pythia6_softdrop' + str(i), i+1, i+1)
    namesreco_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_softdrop[i].Draw('hist')
    namesgen_softdrop[i] = pythia8_gen_softdrop.ProjectionY('pythia8_gen' + str(i), i+1, i+1)
    namesgen_softdrop[i].SetLineColor(4)
    namesgen_softdrop[i].Draw('same hist')
    legends_softdrop[i].AddEntry(namesreco_softdrop[i], 'Reco', 'l')
    legends_softdrop[i].AddEntry(namesgen_softdrop[i], 'Gen', 'l')
    legends_softdrop[i].Draw()
    canvas.SaveAs('partonshower_unc_test_softdrop'+str(i)+'.png')
# unfold data with pythia 6
unfold_ps_data = RooUnfoldBayes(pythia6_response, data_reco, 3)
unfolded_ps_data = unfold_ps_data.Hreco()

canvases_data = []
namesreco_data = []
namesgen_data = []
legends_data = []

for x in range(0, 7):
    canvases_data.append(TCanvas("canvas_data" + str(x)))
    legends_data.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data) : 
    canvas.cd()
    namesreco_data.append(unfolded_ps_data.ProjectionY('data_unfolded_by_pythia6' + str(i), i+1, i+1))
    namesreco_data[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data[i].Draw('hist')
    legends_data[i].AddEntry(namesreco_data[i], 'Reco', 'l')
    legends_data[i].Draw()
    canvas.SaveAs('partonshower_unc_data'+str(i)+'.png')
    
# unfold softdrop data with pythia 6
unfold_ps_data_softdrop = RooUnfoldBayes(pythia6_response_softdrop, data_reco_softdrop, 3)
unfolded_ps_data_softdrop = unfold_ps_data_softdrop.Hreco()

canvases_data_softdrop = []
namesreco_data_softdrop = []
legends_data_softdrop = []

for x in range(0, 7):
    canvases_data_softdrop.append(TCanvas("canvas_data_softdrop" + str(x)))
    legends_data_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_softdrop) : 
    canvas.cd()
    namesreco_data_softdrop.append(unfolded_ps_data_softdrop.ProjectionY('data_unfolded_by_pythia6_softdrop' + str(i), i+1, i+1))
    namesreco_data_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_softdrop[i].Draw('hist')
    legends_data_softdrop[i].AddEntry(namesreco_data_softdrop[i], 'Reco', 'l')
    legends_data_softdrop[i].Draw()
    canvas.SaveAs('partonshower_unc_data_softdrop'+str(i)+'.png')
outfile = TFile('PS_hists.root', 'RECREATE')
outfile.cd()
for i in range(0, 7):
    namesreco[i].Write()
    namesreco_softdrop[i].Write()
    namesreco_data[i].Write()
    namesreco_data_softdrop[i].Write()
