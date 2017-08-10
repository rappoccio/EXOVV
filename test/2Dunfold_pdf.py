import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
ROOT.gROOT.SetBatch()

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
# dict used later for labels



from optparse import OptionParser
parser = OptionParser()

parser.add_option('--scale', action ='store_true', 
                 default =False,
                 dest='scale',
                 help='Scale hists to unity?')

(options, args) = parser.parse_args()
 


pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11

pdffile = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')


pdfup_response = pdffile.Get('2d_response_pdfup')
pdfup_response_softdrop = pdffile.Get('2d_response_softdrop_pdfup')


pdfdn_response = pdffile.Get('2d_response_pdfdn')
pdfdn_response_softdrop = pdffile.Get('2d_response_softdrop_pdfdn')


pdfcteq_response = pdffile.Get('2d_response_cteq')
pdfcteq_response_softdrop = pdffile.Get('2d_response_softdrop_cteq')

pdfmstw_response = pdffile.Get('2d_response_mstw')
pdfmstw_response_softdrop = pdffile.Get('2d_response_softdrop_mstw')



# Get data hists and normalize
data_reco = datafile.Get('PFJet_pt_m_AK8')
data_reco_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

if options.scale != None and options.scale : 
    data_reco.Scale(1./data_reco.Integral())
    data_reco_softdrop.Scale(1./data_reco_softdrop.Integral())

# get pythia 8 reco and normalize
pdf_reco = pdffile.Get('PFJet_pt_m_AK8')
pdf_reco_softdrop = pdffile.Get('PFJet_pt_m_AK8SD')

if options.scale != None and options.scale : 
    pdf_reco.Scale(1./pdf_reco.Integral())
    pdf_reco_softdrop.Scale(1./pdf_reco_softdrop.Integral())

# get truth and normalize it
pdf_gen = pdffile.Get('PFJet_pt_m_AK8Gen')
pdf_gen_softdrop = pdffile.Get('PFJet_pt_m_AK8SDgen')
if options.scale != None and options.scale : 
    pdf_gen.Scale(1./pdf_gen.Integral())
    pdf_gen_softdrop.Scale(1./pdf_gen_softdrop.Integral())

##################################################################################################### Unfold Pythia8 with PDF-UP
unfold_pdfup = RooUnfoldBayes(pdfup_response, pdf_reco, 4)
unfold_pdfup.SetName("unfold_pdfup")
unfolded_pdfup = unfold_pdfup.Hreco().Clone("2d_response_pdfup_mc")

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
    if options.scale != None and options.scale : 
        namesreco_up[i].Scale(1.0 / namesreco_up[i].Integral() )
    namesreco_up[i].Draw('hist')
    legends_up[i].AddEntry(namesreco_up[i], 'Reco_pdfup', 'l')
    legends_up[i].Draw()
    canvas.SaveAs('hists/pdfup_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-UP for SoftDrop
unfold_pdfup_softdrop = RooUnfoldBayes(pdfup_response_softdrop, pdf_reco_softdrop, 4)
unfold_pdfup_softdrop.SetName("unfold_pdfup_softdrop")
unfolded_pdfup_softdrop = unfold_pdfup_softdrop.Hreco().Clone("2d_response_pdfup_softdrop_mc")

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
    if options.scale != None and options.scale : 
        namesreco_up_softdrop[i].Scale( 1.0 / namesreco_up_softdrop[i].Integral() )
    namesreco_up_softdrop[i].Draw('hist')
    legends_up_softdrop[i].AddEntry(namesreco_up_softdrop[i], 'Reco_pdfup_sd', 'l')
    legends_up_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfup_softdrop_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-Down 
unfold_pdfdn = RooUnfoldBayes(pdfdn_response, pdf_reco, 4)
unfold_pdfdn.SetName("unfold_pdfdn")
unfolded_pdfdn = unfold_pdfdn.Hreco().Clone("2d_response_pdfdn_mc")

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
    if options.scale != None and options.scale : 
        namesreco_dn[i].Scale(1.0 / namesreco_dn[i].Integral() )
    namesreco_dn[i].Draw('hist')
    legends_dn[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn', 'l')
    legends_dn[i].Draw()
    canvas.SaveAs('hists/pdfdn_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-Down for SoftDrop
unfold_pdfdn_softdrop = RooUnfoldBayes(pdfdn_response_softdrop, pdf_reco_softdrop, 4)
unfold_pdfdn_softdrop.SetName("unfold_pdfdn_softdrop")
unfolded_pdfdn_softdrop = unfold_pdfdn_softdrop.Hreco().Clone("2d_response_pdfdn_softdrop_mc")

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
    if options.scale != None and options.scale : 
        namesreco_dn_softdrop[i].Scale( 1.0 / namesreco_dn_softdrop[i].Integral() )
    namesreco_dn_softdrop[i].Draw('hist')
    legends_dn_softdrop[i].AddEntry(namesreco_dn[i], 'Reco_pdfdn_sd', 'l')
    legends_dn_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfdn_preplot_softdrop'+str(i)+'.png')

###################################################################################################### Unfold data with PDF-UP
unfold_data_pdfup = RooUnfoldBayes(pdfup_response, data_reco, 4)
unfold_data_pdfup.SetName("unfold_data_pdfup")
unfolded_data_pdfup = unfold_data_pdfup.Hreco().Clone("2d_response_pdfup_data")

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
    if options.scale != None and options.scale : 
        namesreco_data_up[i].Scale( 1.0 / namesreco_data_up[i].Integral() )
    namesreco_data_up[i].Draw('hist')
    legends_data_up[i].AddEntry(namesreco_data_up[i], 'Reco_pdfup', 'l')
    legends_data_up[i].Draw()
    canvas.SaveAs('hists/pdfup_data_preplot'+str(i)+'.png')

#################################################################################################### Unfold data with PDF-UP for SoftDrop 
unfold_data_pdfup_softdrop = RooUnfoldBayes(pdfup_response_softdrop, data_reco_softdrop, 4)
unfold_data_pdfup_softdrop.SetName("unfold_data_pdfup_softdrop")
unfolded_data_pdfup_softdrop = unfold_data_pdfup_softdrop.Hreco().Clone("2d_response_pdfup_softdrop_data")

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
    if options.scale != None and options.scale : 
        namesreco_data_up_softdrop[i].Scale( 1.0 / namesreco_data_up_softdrop[i].Integral() )
    namesreco_data_up_softdrop[i].Draw('hist')
    legends_data_up_softdrop[i].AddEntry(namesreco_data_up_softdrop[i], 'Reco_pdfup_sd', 'l')
    legends_data_up_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfup_data_softdrop_preplot'+str(i)+'.png')

################################################################################################### Unfold data with PDF-DOWN
unfold_data_pdfdn = RooUnfoldBayes(pdfdn_response, data_reco, 4)
unfold_data_pdfdn.SetName("unfold_data_pdfdn")
unfolded_data_pdfdn = unfold_data_pdfdn.Hreco().Clone("2d_response_pdfdn_data")

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
    if options.scale != None and options.scale : 
        namesreco_data_dn[i].Scale(1.0 / namesreco_data_dn[i].Integral() )
    namesreco_data_dn[i].Draw('hist')
    legends_data_dn[i].AddEntry(namesreco_data_dn[i], 'Reco_pdfdn', 'l')
    legends_data_dn[i].Draw()
    canvas.SaveAs('hists/pdfdn_data_preplot'+str(i)+'.png')


################################################################################################## Unfold data with PDF-Down for SoftDrop
unfold_data_pdfdn_softdrop = RooUnfoldBayes(pdfdn_response_softdrop, data_reco_softdrop, 4)
unfold_data_pdfdn_softdrop.SetName("unfold_data_pdfdn_softdrop")
unfolded_data_pdfdn_softdrop = unfold_data_pdfdn_softdrop.Hreco().Clone("2d_response_pdfdn_softdrop_data")

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
    if options.scale != None and options.scale : 
        namesreco_data_dn_softdrop[i].Scale( 1.0 / namesreco_data_dn_softdrop[i].Integral() )
    namesreco_data_dn_softdrop[i].Draw('hist')
    legends_data_dn_softdrop[i].AddEntry(namesreco_data_dn_softdrop[i], 'Reco_pdfdn_sd', 'l')
    legends_data_dn_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfdn_data_preplot_softdrop'+str(i)+'.png')






##################################################################################################### Unfold Pythia8 with PDF-CTEQ
unfold_pdfcteq = RooUnfoldBayes(pdfcteq_response, pdf_reco, 4)
unfold_pdfcteq.SetName("unfold_pdfcteq")
unfolded_pdfcteq = unfold_pdfcteq.Hreco().Clone("2d_response_cteq_mc")

canvases_cteq = []
namesreco_cteq = []

legends_cteq = []
for x in range(0, nptbin):
    canvases_cteq.append(TCanvas("canvas_pdfcteq" + str(x)))
    namesreco_cteq.append(None)
    legends_cteq.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_cteq) : 
    canvas.cd()
    namesreco_cteq[i] = unfolded_pdfcteq.ProjectionX('pdf_cteq' + str(i), i+1, i+1)
    namesreco_cteq[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_cteq[i].Scale( 1.0 / namesreco_cteq[i].Integral() )
    namesreco_cteq[i].Draw('hist')
    legends_cteq[i].AddEntry(namesreco_cteq[i], 'Reco_pdfcteq', 'l')
    legends_cteq[i].Draw()
    canvas.SaveAs('hists/pdfcteq_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-CTEQ for SoftDrop
unfold_pdfcteq_softdrop = RooUnfoldBayes(pdfcteq_response_softdrop, pdf_reco_softdrop, 4)
unfold_pdfcteq_softdrop.SetName("unfold_pdfcteq_softdrop")
unfolded_pdfcteq_softdrop = unfold_pdfcteq_softdrop.Hreco().Clone("2d_response_cteq_softdrop_mc")

canvases_cteq_softdrop = []
namesreco_cteq_softdrop = []
legends_cteq_softdrop = []

for x in range(0, nptbin):
    canvases_cteq_softdrop.append(TCanvas("canvas_pdfcteq_softdrop"+str(x)))
    namesreco_cteq_softdrop.append(None)
    legends_cteq_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_cteq_softdrop):
    canvas.cd()
    namesreco_cteq_softdrop[i] = unfolded_pdfcteq_softdrop.ProjectionX('pdf_cteq_softdrop' + str(i), i+1, i+1)
    namesreco_cteq_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_cteq_softdrop[i].Scale( 1.0 / namesreco_cteq_softdrop[i].Integral() )
    namesreco_cteq_softdrop[i].Draw('hist')
    legends_cteq_softdrop[i].AddEntry(namesreco_cteq_softdrop[i], 'Reco_pdfcteq_sd', 'l')
    legends_cteq_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfcteq_softdrop_preplot'+str(i)+'.png')





##################################################################################################### Unfold Pythia8 with PDF-MSTW
unfold_pdfmstw = RooUnfoldBayes(pdfmstw_response, pdf_reco, 4)
unfold_pdfmstw.SetName("unfold_pdfmstw")
unfolded_pdfmstw = unfold_pdfmstw.Hreco().Clone("2d_response_mstw_mc")

canvases_mstw = []
namesreco_mstw = []

legends_mstw = []
for x in range(0, nptbin):
    canvases_mstw.append(TCanvas("canvas_pdfmstw" + str(x)))
    namesreco_mstw.append(None)
    legends_mstw.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_mstw) : 
    canvas.cd()
    namesreco_mstw[i] = unfolded_pdfmstw.ProjectionX('pdf_mstw' + str(i), i+1, i+1)
    namesreco_mstw[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_mstw[i].Scale(1.0 / namesreco_mstw[i].Integral() )
    namesreco_mstw[i].Draw('hist')
    legends_mstw[i].AddEntry(namesreco_mstw[i], 'Reco_pdfmstw', 'l')
    legends_mstw[i].Draw()
    canvas.SaveAs('hists/pdfmstw_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with PDF-MSTW for SoftDrop
unfold_pdfmstw_softdrop = RooUnfoldBayes(pdfmstw_response_softdrop, pdf_reco_softdrop, 4)
unfold_pdfmstw_softdrop.SetName("unfold_pdfmstw_softdrop")
unfolded_pdfmstw_softdrop = unfold_pdfmstw_softdrop.Hreco().Clone("2d_response_mstw_softdrop_mc")

canvases_mstw_softdrop = []
namesreco_mstw_softdrop = []
legends_mstw_softdrop = []

for x in range(0, nptbin):
    canvases_mstw_softdrop.append(TCanvas("canvas_pdfmstw_softdrop"+str(x)))
    namesreco_mstw_softdrop.append(None)
    legends_mstw_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_mstw_softdrop):
    canvas.cd()
    namesreco_mstw_softdrop[i] = unfolded_pdfmstw_softdrop.ProjectionX('pdf_mstw_softdrop' + str(i), i+1, i+1)
    namesreco_mstw_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_mstw_softdrop[i].Scale( 1.0 / namesreco_mstw_softdrop[i].Integral() )
    namesreco_mstw_softdrop[i].Draw('hist')
    legends_mstw_softdrop[i].AddEntry(namesreco_mstw_softdrop[i], 'Reco_pdfmstw_sd', 'l')
    legends_mstw_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfmstw_softdrop_preplot'+str(i)+'.png')





###################################################################################################### Unfold data with PDF-CTEQ
unfold_data_pdfcteq = RooUnfoldBayes(pdfcteq_response, data_reco, 4)
unfold_data_pdfcteq.SetName("unfold_data_pdfcteq")
unfolded_data_pdfcteq = unfold_data_pdfcteq.Hreco().Clone("2d_response_cteq_data")

canvases_data_cteq = []
namesreco_data_cteq = []

legends_data_cteq = []
for x in range(0, nptbin):
    canvases_data_cteq.append(TCanvas("canvas_data_pdfcteq" + str(x)))
    namesreco_data_cteq.append(None)
    legends_data_cteq.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_cteq) : 
    canvas.cd()
    namesreco_data_cteq[i] = unfolded_data_pdfcteq.ProjectionX('pdf_data_cteq' + str(i), i+1, i+1)
    namesreco_data_cteq[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_cteq[i].Scale( 1.0 / namesreco_data_cteq[i].Integral() )
    namesreco_data_cteq[i].Draw('hist')
    legends_data_cteq[i].AddEntry(namesreco_data_cteq[i], 'Reco_pdfcteq', 'l')
    legends_data_cteq[i].Draw()
    canvas.SaveAs('hists/pdfcteq_data_preplot'+str(i)+'.png')

#################################################################################################### Unfold data with PDF-CTEQ for SoftDrop 
unfold_data_pdfcteq_softdrop = RooUnfoldBayes(pdfcteq_response_softdrop, data_reco_softdrop, 4)
unfold_data_pdfcteq_softdrop.SetName("unfold_data_pdfcteq_softdrop")
unfolded_data_pdfcteq_softdrop = unfold_data_pdfcteq_softdrop.Hreco().Clone("2d_response_cteq_softdrop_data")

canvases_data_cteq_softdrop = []
namesreco_data_cteq_softdrop = []
legends_data_cteq_softdrop = []
for x in range(0, nptbin):
    canvases_data_cteq_softdrop.append(TCanvas("canvas_data_pdfcteq_softdrop"+str(x)))
    namesreco_data_cteq_softdrop.append(None)
    legends_data_cteq_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_cteq_softdrop):
    canvas.cd()
    namesreco_data_cteq_softdrop[i] = unfolded_data_pdfcteq_softdrop.ProjectionX('pdf_data_cteq_softdrop' + str(i), i+1, i+1)
    namesreco_data_cteq_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_cteq_softdrop[i].Scale( 1.0 / namesreco_data_cteq_softdrop[i].Integral() )
    namesreco_data_cteq_softdrop[i].Draw('hist')
    legends_data_cteq_softdrop[i].AddEntry(namesreco_data_cteq_softdrop[i], 'Reco_pdfcteq_sd', 'l')
    legends_data_cteq_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfcteq_data_softdrop_preplot'+str(i)+'.png')
    


###################################################################################################### Unfold data with PDF-MSTW
unfold_data_pdfmstw = RooUnfoldBayes(pdfmstw_response, data_reco, 4)
unfold_data_pdfmstw.SetName("unfold_data_pdfmstw")
unfolded_data_pdfmstw = unfold_data_pdfmstw.Hreco().Clone("2d_response_mstw_data")

canvases_data_mstw = []
namesreco_data_mstw = []

legends_data_mstw = []
for x in range(0, nptbin):
    canvases_data_mstw.append(TCanvas("canvas_data_pdfmstw" + str(x)))
    namesreco_data_mstw.append(None)
    legends_data_mstw.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_mstw) : 
    canvas.cd()
    namesreco_data_mstw[i] = unfolded_data_pdfmstw.ProjectionX('pdf_data_mstw' + str(i), i+1, i+1)
    namesreco_data_mstw[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_mstw[i].Scale( 1.0 / namesreco_data_mstw[i].Integral() )
    namesreco_data_mstw[i].Draw('hist')
    legends_data_mstw[i].AddEntry(namesreco_data_mstw[i], 'Reco_pdfmstw', 'l')
    legends_data_mstw[i].Draw()
    canvas.SaveAs('hists/pdfmstw_data_preplot'+str(i)+'.png')

#################################################################################################### Unfold data with PDF-MSTW for SoftDrop 
unfold_data_pdfmstw_softdrop = RooUnfoldBayes(pdfmstw_response_softdrop, data_reco_softdrop, 4)
unfold_data_pdfmstw_softdrop.SetName("unfold_data_pdfmstw_softdrop")
unfolded_data_pdfmstw_softdrop = unfold_data_pdfmstw_softdrop.Hreco().Clone("2d_response_mstw_softdrop_data")

canvases_data_mstw_softdrop = []
namesreco_data_mstw_softdrop = []
legends_data_mstw_softdrop = []
for x in range(0, nptbin):
    canvases_data_mstw_softdrop.append(TCanvas("canvas_data_pdfmstw_softdrop"+str(x)))
    namesreco_data_mstw_softdrop.append(None)
    legends_data_mstw_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_mstw_softdrop):
    canvas.cd()
    namesreco_data_mstw_softdrop[i] = unfolded_data_pdfmstw_softdrop.ProjectionX('pdf_data_mstw_softdrop' + str(i), i+1, i+1)
    namesreco_data_mstw_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_mstw_softdrop[i].Scale( 1.0 / namesreco_data_mstw_softdrop[i].Integral() )
    namesreco_data_mstw_softdrop[i].Draw('hist')
    legends_data_mstw_softdrop[i].AddEntry(namesreco_data_mstw_softdrop[i], 'Reco_pdfmstw_sd', 'l')
    legends_data_mstw_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfmstw_data_softdrop_preplot'+str(i)+'.png')
    


    
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


    namesreco_cteq[i].Write()
    namesreco_cteq_softdrop[i].Write()
    namesreco_mstw[i].Write()
    namesreco_mstw_softdrop[i].Write()
    namesreco_data_cteq[i].Write()
    namesreco_data_cteq_softdrop[i].Write()
    namesreco_data_mstw[i].Write()
    namesreco_data_mstw_softdrop[i].Write()

unfold_pdfup.Write()
unfold_pdfup_softdrop.Write()
unfold_pdfdn.Write()
unfold_pdfdn_softdrop.Write()
unfold_data_pdfup.Write()
unfold_data_pdfup_softdrop.Write()
unfold_data_pdfdn.Write()
unfold_data_pdfdn_softdrop.Write()
unfold_pdfcteq.Write()
unfold_pdfcteq_softdrop.Write()
unfold_pdfmstw.Write()
unfold_pdfmstw_softdrop.Write()
unfold_data_pdfcteq.Write()
unfold_data_pdfcteq_softdrop.Write()
unfold_data_pdfmstw.Write()
unfold_data_pdfmstw_softdrop.Write()

outfile.Close()
