import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
# dict used later for labels
pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11

pdffile = TFile('responses_repdf_otherway_qcdmc.root')
datafile = TFile('jetht_weighted_dataplots_otherway_repdf.root')


pdfup_response = pdffile.Get('2d_response_pdfup')
pdfup_response_softdrop = pdffile.Get('2d_response_softdrop_pdfup')


pdfdn_response = pdffile.Get('2d_response_pdfdn')
pdfdn_response_softdrop = pdffile.Get('2d_response_softdrop_pdfdn')

# Get data hists and normalize
data_reco = datafile.Get('PFJet_pt_m_AK8')
data_reco_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

data_reco.Scale(1./data_reco.Integral())
data_reco_softdrop.Scale(1./data_reco_softdrop.Integral())

# get pythia 8 reco and normalize
pdf_reco = pdffile.Get('PFJet_pt_m_AK8')
pdf_reco_softdrop = pdffile.Get('PFJet_pt_m_AK8SD')

pdf_reco.Scale(1./pdf_reco.Integral())
pdf_reco_softdrop.Scale(1./pdf_reco_softdrop.Integral())

# get truth and normalize it
pdf_gen = pdffile.Get('PFJet_pt_m_AK8Gen')
pdf_gen_softdrop = pdffile.Get('PFJet_pt_m_AK8SDgen')
pdf_gen.Scale(1./pdf_gen.Integral())
pdf_gen_softdrop.Scale(1./pdf_gen_softdrop.Integral())

##################################################################################################### Unfold Pythia8 with PDF-UP
unfold_pdfup = RooUnfoldBayes(pdfup_response, pdf_reco, 4)
unfolded_pdfup = unfold_pdfup.Hreco()

canvases_up = []
namesreco_up = []

legends_up = []
for x in range(0, nptbin):
    canvases_up.append(TCanvas("canvas_pdfup" + str(x)))
    namesreco_up.append(None)
    legends_up.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_up) : 
    canvas.cd()
    namesreco_up[i] = unfolded_pdfup.ProjectionX('pdf_up' + str(i), i+1, i+1)
    namesreco_up[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_up[i].Draw('hist')
    legends_up[i].AddEntry(namesreco_up[i], 'Reco_pdfup', 'l')
    legends_up[i].Draw()
    canvas.SaveAs('hists/pdfup_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-UP for SoftDrop
unfold_pdfup_softdrop = RooUnfoldBayes(pdfup_response_softdrop, pdf_reco_softdrop, 4)
unfolded_pdfup_softdrop = unfold_pdfup_softdrop.Hreco()

canvases_up_softdrop = []
namesreco_up_softdrop = []
legends_up_softdrop = []

for x in range(0, nptbin):
    canvases_up_softdrop.append(TCanvas("canvas_pdfup_softdrop"+str(x)))
    namesreco_up_softdrop.append(None)
    legends_up_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_up_softdrop):
    canvas.cd()
    namesreco_up_softdrop[i] = unfolded_pdfup_softdrop.ProjectionX('pdf_up_softdrop' + str(i), i+1, i+1)
    namesreco_up_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_up_softdrop[i].Draw('hist')
    legends_up_softdrop[i].AddEntry(namesreco_up_softdrop[i], 'Reco_pdfup_sd', 'l')
    legends_up_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfup_softdrop_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-Down 
unfold_pdfdn = RooUnfoldBayes(pdfdn_response, pdf_reco, 4)
unfolded_pdfdn = unfold_pdfdn.Hreco()

canvases_dn = []
namesreco_dn = []
namesgen_dn = []
legends_dn = []

for x in range(0, nptbin):
    canvases_dn.append(TCanvas("canvas_pdfdn"+str(x)))
    namesreco_dn.append(None)
    legends_dn.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_dn):
    canvas.cd()
    namesreco_dn[i] = unfolded_pdfdn.ProjectionX('pdf_dn' + str(i), i+1, i+1)
    namesreco_dn[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_dn[i].Draw('hist')
    legends_dn[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn', 'l')
    legends_dn[i].Draw()
    canvas.SaveAs('hists/pdfdn_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-Down for SoftDrop
unfold_pdfdn_softdrop = RooUnfoldBayes(pdfdn_response_softdrop, pdf_reco_softdrop, 4)
unfolded_pdfdn_softdrop = unfold_pdfdn_softdrop.Hreco()

canvases_dn_softdrop = []
namesreco_dn_softdrop = []
legends_dn_softdrop = []

for x in range(0, nptbin):
    canvases_dn_softdrop.append(TCanvas("canvas_pdfdn_softdrop"+str(x)))
    namesreco_dn_softdrop.append(None)
    legends_dn_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_dn):
    canvas.cd()
    namesreco_dn_softdrop[i] = unfolded_pdfdn_softdrop.ProjectionX('pdf_dn_softdrop' + str(i), i+1, i+1)
    namesreco_dn_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_dn_softdrop[i].Draw('hist')
    legends_dn_softdrop[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn_sd', 'l')
    legends_dn_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfdn_preplot_softdrop'+str(i)+'.png')

###################################################################################################### Unfold data with PDF-UP
unfold_data_pdfup = RooUnfoldBayes(pdfup_response, data_reco, 4)
unfolded_data_pdfup = unfold_data_pdfup.Hreco()

canvases_data_up = []
namesreco_data_up = []

legends_data_up = []
for x in range(0, nptbin):
    canvases_data_up.append(TCanvas("canvas_data_pdfup" + str(x)))
    namesreco_data_up.append(None)
    legends_data_up.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_up) : 
    canvas.cd()
    namesreco_data_up[i] = unfolded_data_pdfup.ProjectionX('pdf_data_up' + str(i), i+1, i+1)
    namesreco_data_up[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_up[i].Draw('hist')
    legends_data_up[i].AddEntry(namesreco_data_up[i], 'Reco_pdfup', 'l')
    legends_data_up[i].Draw()
    canvas.SaveAs('hists/pdfup_data_preplot'+str(i)+'.png')

#################################################################################################### Unfold data with PDF-UP for SoftDrop 
unfold_data_pdfup_softdrop = RooUnfoldBayes(pdfup_response_softdrop, data_reco_softdrop, 4)
unfolded_data_pdfup_softdrop = unfold_data_pdfup_softdrop.Hreco()

canvases_data_up_softdrop = []
namesreco_data_up_softdrop = []
legends_data_up_softdrop = []
for x in range(0, nptbin):
    canvases_data_up_softdrop.append(TCanvas("canvas_data_pdfup_softdrop"+str(x)))
    namesreco_data_up_softdrop.append(None)
    legends_data_up_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_up_softdrop):
    canvas.cd()
    namesreco_data_up_softdrop[i] = unfolded_data_pdfup_softdrop.ProjectionX('pdf_data_up_softdrop' + str(i), i+1, i+1)
    namesreco_data_up_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_up_softdrop[i].Draw('hist')
    legends_data_up_softdrop[i].AddEntry(namesreco_data_up_softdrop[i], 'Reco_pdfup_sd', 'l')
    legends_data_up_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfup_data_softdrop_preplot'+str(i)+'.png')

################################################################################################### Unfold data with PDF-DOWN
unfold_data_pdfdn = RooUnfoldBayes(pdfdn_response, data_reco, 4)
unfolded_data_pdfdn = unfold_data_pdfdn.Hreco()

canvases_data_dn = []
namesreco_data_dn = []
namesgen_data_dn = []
legends_data_dn = []

for x in range(0, nptbin):
    canvases_data_dn.append(TCanvas("canvas_data_pdfdn"+str(x)))
    namesreco_data_dn.append(None)
    legends_data_dn.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_dn):
    canvas.cd()
    namesreco_data_dn[i] = unfolded_data_pdfdn.ProjectionX('pdf_data_dn' + str(i), i+1, i+1)
    namesreco_data_dn[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_dn[i].Draw('hist')
    legends_data_dn[i].AddEntry(namesreco_data_dn[i], 'Reco_pdfdn', 'l')
    legends_data_dn[i].Draw()
    canvas.SaveAs('hists/pdfdn_data_preplot'+str(i)+'.png')


################################################################################################## Unfold data with PDF-Down for SoftDrop
unfold_data_pdfdn_softdrop = RooUnfoldBayes(pdfdn_response_softdrop, data_reco_softdrop, 4)
unfolded_data_pdfdn_softdrop = unfold_data_pdfdn_softdrop.Hreco()

canvases_data_dn_softdrop = []
namesreco_data_dn_softdrop = []
legends_data_dn_softdrop = []

for x in range(0, nptbin):
    canvases_data_dn_softdrop.append(TCanvas("canvas_data_pdfdn_softdrop"+str(x)))
    namesreco_data_dn_softdrop.append(None)
    legends_data_dn_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_dn_softdrop):
    canvas.cd()
    namesreco_data_dn_softdrop[i] = unfolded_data_pdfdn_softdrop.ProjectionX('pdf_data_dn_softdrop' + str(i), i+1, i+1)
    namesreco_data_dn_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_data_dn_softdrop[i].Draw('hist')
    legends_data_dn_softdrop[i].AddEntry(namesreco_data_dn_softdrop[i], 'Reco_pdfdn_sd', 'l')
    legends_data_dn_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfdn_data_preplot_softdrop'+str(i)+'.png')


outfile = TFile("unfoldedpdf.root", 'RECREATE')
outfile.cd()
for i in range(0, nptbin):
    namesreco_up[i].Write()
    namesreco_up_softdrop[i].Write()
    namesreco_dn[i].Write()
    namesreco_dn_softdrop[i].Write()
    namesreco_data_up[i].Write()
    namesreco_data_up_softdrop[i].Write()
    namesreco_data_dn[i].Write()
    namesreco_data_dn_softdrop[i].Write()
outfile.Close()
