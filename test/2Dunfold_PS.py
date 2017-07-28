import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
ROOT.gROOT.SetBatch()

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
# dict used later for labels

pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11

herwigfile = TFile('qcdmc_herwig_otherway_rejec_tightgen_2dplots.root')
pythia8file = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')


herwig_response = herwigfile.Get('2d_response')
herwig_response_softdrop = herwigfile.Get('2d_response_softdrop_nomnom')

pythia8_response = pythia8file.Get('2d_response')
pythia8_response_softdrop = pythia8file.Get('2d_response_softdrop_nomnom')

# Get data hists and normalize
data_reco = datafile.Get('PFJet_pt_m_AK8')
data_reco_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

data_reco.Scale(1./data_reco.Integral("width"))
data_reco_softdrop.Scale(1./data_reco_softdrop.Integral("width"))

# get pythia 8 reco and normalize
pythia8_reco = pythia8file.Get('PFJet_pt_m_AK8')
pythia8_reco_softdrop = pythia8file.Get('PFJet_pt_m_AK8SD_nomnom')
pythia8_reco.Scale(1./pythia8_reco.Integral("width"))
pythia8_reco_softdrop.Scale(1./pythia8_reco_softdrop.Integral("width"))

# get herwig reco and normalize
herwig_reco = herwigfile.Get('PFJet_pt_m_AK8')
herwig_reco_softdrop = herwigfile.Get('PFJet_pt_m_AK8SD_nomnom')
herwig_reco.Scale(1./herwig_reco.Integral("width"))
herwig_reco_softdrop.Scale(1./herwig_reco_softdrop.Integral("width"))

# get truth and normalize it
pythia8_gen = pythia8file.Get('PFJet_pt_m_AK8Gen')
pythia8_gen_softdrop = pythia8file.Get('PFJet_pt_m_AK8SDgen')
pythia8_gen.Scale(1./pythia8_gen.Integral("width"))
pythia8_gen_softdrop.Scale(1./pythia8_gen_softdrop.Integral("width"))

herwig_gen = herwigfile.Get('PFJet_pt_m_AK8Gen')
herwig_gen_softdrop = herwigfile.Get('PFJet_pt_m_AK8SDgen')
herwig_gen.Scale(1./herwig_gen.Integral("width"))
herwig_gen_softdrop.Scale(1./herwig_gen_softdrop.Integral("width"))

########################################################################################################### Unfold ungroomed pythia  8 with herwig
unfold_ps = RooUnfoldBayes(herwig_response, pythia8_reco, 4)
unfolded_ps = unfold_ps.Hreco()
pyth8_uherwig = unfolded_ps.ProjectionX()
pyth8_uherwig.Scale( 1.0 / pyth8_uherwig.Integral("width") )
pyth8_uherwig.SetName("pyth8_uherwig")
canvases = []
namesreco = []
namesgen = []
legends = []
for x in range(0, nptbin):
    canvases.append(TCanvas("canvas" + str(x)))
    namesreco.append(None)
    namesgen.append(None)
    legends.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases) : 
    canvas.cd()
    namesreco[i] = unfolded_ps.ProjectionX('pythia8_unfolded_by_herwig' + str(i), i+1, i+1)
    namesreco[i].Scale( 1.0 / namesreco[i].Integral("width") )
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = pythia8_gen.ProjectionX('pythia8_gen' + str(i), i+1, i+1)
    namesgen[i].Scale(1.0 / namesgen[i].Integral("width") )
    namesgen[i].SetLineColor(4)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('hists/partonshower_unc_test'+str(i)+'.png')

########################################################################################################### Unfold softdrop pythia 8 with herwig

unfold_ps_softdrop = RooUnfoldBayes(herwig_response_softdrop, pythia8_reco_softdrop, 4)
unfolded_ps_softdrop = unfold_ps_softdrop.Hreco()
pyth8_uherwig_softdrop = unfolded_ps_softdrop.ProjectionX()
pyth8_uherwig_softdrop.Scale(1.0 / pyth8_uherwig_softdrop.Integral("width") )
pyth8_uherwig_softdrop.SetName('pyth8_uherwig_softdrop')


canvases_softdrop = []
namesreco_softdrop = []
namesgen_softdrop = []
legends_softdrop = []

for x in range(0, nptbin):
    canvases_softdrop.append(TCanvas("canvas_softdrop" + str(x)))
    namesreco_softdrop.append(None)
    namesgen_softdrop.append(None)
    legends_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_softdrop) : 
    canvas.cd()
    namesreco_softdrop[i] = unfolded_ps_softdrop.ProjectionX('pythia8_unfolded_by_herwig_softdrop' + str(i), i+1, i+1)
    namesreco_softdrop[i].Scale(1.0 / namesreco_softdrop[i].Integral("width") )
    namesreco_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_softdrop[i].Draw('hist')
    namesgen_softdrop[i] = pythia8_gen_softdrop.ProjectionX('pythia8_gen' + str(i), i+1, i+1)
    namesgen_softdrop[i].Scale( 1.0 / namesgen_softdrop[i].Integral("width") )
    namesgen_softdrop[i].SetLineColor(4)
    namesgen_softdrop[i].Draw('same hist')
    legends_softdrop[i].AddEntry(namesreco_softdrop[i], 'Reco', 'l')
    legends_softdrop[i].AddEntry(namesgen_softdrop[i], 'Gen', 'l')
    legends_softdrop[i].Draw()
    canvas.SaveAs('hists/partonshower_unc_test_softdrop'+str(i)+'.png')
############################################################################################################ Unfold data with herwig
unfold_ps_data = RooUnfoldBayes(herwig_response, data_reco, 4)
unfolded_ps_data = unfold_ps_data.Hreco()

data_uherwig = unfolded_ps_data.ProjectionX()
data_uherwig.Scale(1.0 / data_uherwig.Integral("width") )
data_uherwig.SetName('data_uherwig')

canvases_data = []
namesreco_data = []
namesgen_data = []
legends_data = []
for x in range(0, nptbin):
    canvases_data.append(TCanvas("canvas_data" + str(x)))
    legends_data.append(TLegend(.7, .5, .9, .7))
for i, canvas in enumerate(canvases_data) : 
    canvas.cd()
    namesreco_data.append(unfolded_ps_data.ProjectionX('data_unfolded_by_herwig' + str(i), i+1, i+1))
    namesreco_data[i].Scale(1.0 / namesreco_data[i].Integral("width") )
    namesreco_data[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data[i].Draw('hist')
    legends_data[i].AddEntry(namesreco_data[i], 'Reco', 'l')
    legends_data[i].Draw()
    canvas.SaveAs('hists/partonshower_unc_data'+str(i)+'.png')
    
########################################################################################################### Unfold softdrop data with herwig

unfold_ps_data_softdrop = RooUnfoldBayes(herwig_response_softdrop, data_reco_softdrop, 4)
unfolded_ps_data_softdrop = unfold_ps_data_softdrop.Hreco()

data_uherwig_softdrop = unfolded_ps_data_softdrop.ProjectionX()
data_uherwig_softdrop.Scale( 1.0 / data_uherwig_softdrop.Integral("width") )
data_uherwig_softdrop.SetName('data_uherwig_softdrop')

canvases_data_softdrop = []
namesreco_data_softdrop = []
legends_data_softdrop = []

for x in range(0, nptbin):
    canvases_data_softdrop.append(TCanvas("canvas_data_softdrop" + str(x)))
    legends_data_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_softdrop) : 
    canvas.cd()
    namesreco_data_softdrop.append(unfolded_ps_data_softdrop.ProjectionX('data_unfolded_by_herwig_softdrop' + str(i), i+1, i+1))
    namesreco_data_softdrop[i].Scale( 1.0 / namesreco_data_softdrop[i].Integral("width") )
    namesreco_data_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_softdrop[i].Draw('hist')
    legends_data_softdrop[i].AddEntry(namesreco_data_softdrop[i], 'Reco', 'l')
    legends_data_softdrop[i].Draw()
    canvas.SaveAs('hists/partonshower_unc_data_softdrop'+str(i)+'.png')

########################################################################################################## Ungroomed herwig unfolded with the pythia 8
unfold_bias = RooUnfoldBayes(pythia8_response, herwig_reco, 4)
unfolded_bias = unfold_bias.Hreco()

canvases_bias = []
namesreco_bias = []
namesgen_bias = []
legends_bias = []
for x in range(0, nptbin):
    canvases_bias.append(TCanvas("canvas_bias" + str(x)))
    namesreco_bias.append(None)
    namesgen_bias.append(None)
    legends_bias.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_bias) : 
    canvas.cd()
    namesreco_bias[i] = unfolded_bias.ProjectionX('herwig_unfolded_by_pythia8' + str(i), i+1, i+1)
    namesreco_bias[i].Scale( 1.0 / namesreco_bias[i].Integral("width") )
    namesreco_bias[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_bias[i].Draw('hist')
    namesgen_bias[i] = herwig_gen.ProjectionX('herwig_gen' + str(i), i+1, i+1)
    namesgen_bias[i].Scale( 1.0 / namesgen_bias[i].Integral("width") )
    namesgen_bias[i].SetLineColor(4)
    namesgen_bias[i].Draw('same hist')
    legends_bias[i].AddEntry(namesreco_bias[i], 'Pyth6 Unfolded by Pythia8', 'l')
    legends_bias[i].AddEntry(namesgen_bias[i], 'herwig Gen', 'l')
    legends_bias[i].Draw()
    canvas.SaveAs('hists/ungroomed_bias'+str(i)+'.png')

########################################################################################################### unfold the SoftDrop herwig reco with pythia8 response matrix and partition into pt bins

unfold_bias_softdrop = RooUnfoldBayes(pythia8_response_softdrop, herwig_reco_softdrop, 4)
unfolded_bias_softdrop = unfold_bias_softdrop.Hreco()

canvases_bias_softdrop = []
namesreco_bias_softdrop = []
namesgen_bias_softdrop = []
legends_bias_softdrop = []

for x in range(0, nptbin):
    canvases_bias_softdrop.append(TCanvas("canvas_bias_softdrop" + str(x)))
    namesreco_bias_softdrop.append(None)
    namesgen_bias_softdrop.append(None)
    legends_bias_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_bias_softdrop) : 
    canvas.cd()
    namesreco_bias_softdrop[i] = unfolded_bias_softdrop.ProjectionX('herwig_unfolded_by_pythia8_softdrop' + str(i), i+1, i+1)
    namesreco_bias_softdrop[i].Scale( 1.0 / namesreco_bias_softdrop[i].Integral("width") )
    namesreco_bias_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_bias_softdrop[i].Draw('hist')
    namesgen_bias_softdrop[i] = herwig_gen_softdrop.ProjectionX('herwig_gen_softdrop' + str(i), i+1, i+1)
    namesgen_bias_softdrop[i].Scale( 1.0 / namesgen_bias_softdrop[i].Integral("width") )
    namesgen_bias_softdrop[i].SetLineColor(4)
    namesgen_bias_softdrop[i].Draw('same hist')
    legends_bias_softdrop[i].AddEntry(namesreco_bias_softdrop[i], 'Reco', 'l')
    legends_bias_softdrop[i].AddEntry(namesgen_bias_softdrop[i], 'Gen', 'l')
    legends_bias_softdrop[i].Draw()
    canvas.SaveAs('hists/softdrop_bias'+str(i)+'.png')

########################################################################################################### Save it all
outfile = TFile('PS_hists.root', 'RECREATE')
outfile.cd()

for i in range(0, nptbin):
    namesreco[i].Write()
    namesreco_softdrop[i].Write()
    namesreco_data[i].Write()
    namesreco_data_softdrop[i].Write()
    namesreco_bias_softdrop[i].Write()
    namesreco_bias[i].Write()
    namesgen_bias_softdrop[i].Write()
    namesgen_bias[i].Write()
    pyth8_uherwig.Write()
    pyth8_uherwig_softdrop.Write()
    data_uherwig.Write()
    data_uherwig_softdrop.Write()
unfold_ps.SetName("unfold_ps_herwig")
unfold_ps.Write()
unfold_ps_softdrop.SetName("unfold_ps_softdrop_herwig")
unfold_ps_softdrop.Write()
unfold_ps_data.SetName("unfold_ps_data_herwig")
unfold_ps_data.Write()
unfold_ps_data_softdrop.SetName("unfold_ps_data_softdrop_herwig")
unfold_ps_data_softdrop.Write()
unfold_bias.SetName("unfold_bias")
unfold_bias.Write()
unfold_bias_softdrop.SetName("unfold_bias_softdrop")
unfold_bias_softdrop.Write()
herwig_response.SetName("herwig_response")
herwig_response.Write()
herwig_response_softdrop.SetName("herwig_response_softdrop")
herwig_response_softdrop.Write()
outfile.Close()
