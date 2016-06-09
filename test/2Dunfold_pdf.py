import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
# dict used later for labels
pt_bin = {0: '200-240', 1: '240-310', 2: '310-400', 3: '400-530', 4: '530-650', 5: '650-760', 6: '760-Inf'}


pdffile = TFile('qcdmc_stitched_pdf_qcdmc.root')
datafile = TFile('jetht_40pbinv_weighted_dataplots.root')


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

# unfold the reco with pdf up response matrix

unfold_pdfup = RooUnfoldBayes(pdfup_response, pdf_reco, 3)
unfolded_pdfup = unfold_pdfup.Hreco()

canvases_up = []
namesreco_up = []

legends_up = []
for x in range(0, 7):
    canvases_up.append(TCanvas("canvas_pdfup" + str(x)))
    namesreco_up.append(None)
    legends_up.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_up) : 
    canvas.cd()
    namesreco_up[i] = unfolded_pdfup.ProjectionY('pdf_up' + str(i), i+1, i+1)
    namesreco_up[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_up[i].Draw('hist')
    legends_up[i].AddEntry(namesreco_up[i], 'Reco_pdfup', 'l')
    legends_up[i].Draw()
    canvas.SaveAs('pdfup_preplot'+str(i)+'.png')
# now softdrop

unfold_pdfup_softdrop = RooUnfoldBayes(pdfup_response_softdrop, pdf_reco_softdrop, 3)
unfolded_pdfup_softdrop = unfold_pdfup_softdrop.Hreco()

canvases_up_softdrop = []
namesreco_up_softdrop = []
legends_up_softdrop = []

for x in range(0, 7):
    canvases_up_softdrop.append(TCanvas("canvas_pdfup_softdrop"+str(x)))
    namesreco_up_softdrop.append(None)
    legends_up_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_up_softdrop):
    canvas.cd()
    namesreco_up_softdrop[i] = unfolded_pdfup_softdrop.ProjectionY('pdf_up_softdrop' + str(i), i+1, i+1)
    namesreco_up_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_up_softdrop[i].Draw('hist')
    legends_up_softdrop[i].AddEntry(namesreco_up_softdrop[i], 'Reco_pdfup_sd', 'l')
    legends_up_softdrop[i].Draw()
    canvas.SaveAs('pdfup_softdrop_preplot'+str(i)+'.png')
# pdf down
unfold_pdfdn = RooUnfoldBayes(pdfdn_response, pdf_reco, 3)
unfolded_pdfdn = unfold_pdfdn.Hreco()

canvases_dn = []
namesreco_dn = []
namesgen_dn = []
legends_dn = []

for x in range(0, 7):
    canvases_dn.append(TCanvas("canvas_pdfdn"+str(x)))
    namesreco_dn.append(None)
    legends_dn.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_dn):
    canvas.cd()
    namesreco_dn[i] = unfolded_pdfdn.ProjectionY('pdf_dn' + str(i), i+1, i+1)
    namesreco_dn[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_dn[i].Draw('hist')
    legends_dn[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn', 'l')
    legends_dn[i].Draw()
    canvas.SaveAs('pdfdn_preplot'+str(i)+'.png')


# pdf down softdrop
unfold_pdfdn_softdrop = RooUnfoldBayes(pdfdn_response_softdrop, pdf_reco_softdrop, 3)
unfolded_pdfdn_softdrop = unfold_pdfdn_softdrop.Hreco()

canvases_dn_softdrop = []
namesreco_dn_softdrop = []
legends_dn_softdrop = []

for x in range(0, 7):
    canvases_dn_softdrop.append(TCanvas("canvas_pdfdn_softdrop"+str(x)))
    namesreco_dn_softdrop.append(None)
    legends_dn_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_dn):
    canvas.cd()
    namesreco_dn_softdrop[i] = unfolded_pdfdn_softdrop.ProjectionY('pdf_dn_softdrop' + str(i), i+1, i+1)
    namesreco_dn_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    namesreco_dn_softdrop[i].Draw('hist')
    legends_dn_softdrop[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn_sd', 'l')
    legends_dn_softdrop[i].Draw()
    canvas.SaveAs('pdfdn_preplot_softdrop'+str(i)+'.png')




# data


outfile = TFile("unfoldedpdf.root", 'RECREATE')
outfile.cd()
for i in range(0, 7):
    namesreco_up[i].Write()
    namesreco_up_softdrop[i].Write()
    namesreco_dn[i].Write()
    namesreco_dn_softdrop[i].Write()
outfile.Close()