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

parser.add_option('--lumi', action ='store', type = 'float',
                 default =2300.,
                 dest='lumi',
                 help='Luminosity')

(options, args) = parser.parse_args()
 


pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-Inf'}
nptbin = 11

pdffile = TFile('qcdmc_pythiaflat_pdf4lhc15_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')

pdfnom_response = pdffile.Get('2d_response')
pdfnom_response_softdrop = pdffile.Get('2d_response_softdrop')

pdfup_response = pdffile.Get('2d_response_pdfup')
pdfup_response_softdrop = pdffile.Get('2d_response_softdrop_pdfup')


pdfdn_response = pdffile.Get('2d_response_pdfdn')
pdfdn_response_softdrop = pdffile.Get('2d_response_softdrop_pdfdn')



# Get data hists and normalize
data_reco = datafile.Get('PFJet_pt_m_AK8')
data_reco_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

data_reco.Scale(1.0 / options.lumi)
data_reco_softdrop.Scale(1.0 / options.lumi)

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





##################################################################################################### Unfold Pythia8 with Nominal
unfold_pdfnom = RooUnfoldBayes(pdfnom_response, pdf_reco, 4)
unfold_pdfnom.SetName("unfold_pdfnom")
unfolded_pdfnom = unfold_pdfnom.Hreco().Clone("2d_response_pdfnom_mc")

canvases_nom = []
namesreco_nom = []

legends_nom = []
for x in range(0, nptbin):
    canvases_nom.append(TCanvas("canvas_pdfnom" + str(x)))
    namesreco_nom.append(None)
    legends_nom.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_nom) : 
    canvas.cd()
    namesreco_nom[i] = unfolded_pdfnom.ProjectionX('pdf_nom' + str(i), i+1, i+1)
    namesreco_nom[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_nom[i].Scale(1.0 / namesreco_nom[i].Integral() )
    namesreco_nom[i].Draw('hist')
    legends_nom[i].AddEntry(namesreco_nom[i], 'Reco_pdfnom', 'l')
    legends_nom[i].Draw()
    canvas.SaveAs('hists/pdfnom_preplot'+str(i)+'.png')

##################################################################################################### Unfold Pythia8 with Nominal for SoftDrop
unfold_pdfnom_softdrop = RooUnfoldBayes(pdfnom_response_softdrop, pdf_reco_softdrop, 4)
unfold_pdfnom_softdrop.SetName("unfold_pdfnom_softdrop")
unfolded_pdfnom_softdrop = unfold_pdfnom_softdrop.Hreco().Clone("2d_response_pdfnom_softdrop_mc")

canvases_nom_softdrop = []
namesreco_nom_softdrop = []
legends_nom_softdrop = []

for x in range(0, nptbin):
    canvases_nom_softdrop.append(TCanvas("canvas_pdfnom_softdrop"+str(x)))
    namesreco_nom_softdrop.append(None)
    legends_nom_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_nom_softdrop):
    canvas.cd()
    namesreco_nom_softdrop[i] = unfolded_pdfnom_softdrop.ProjectionX('pdf_nom_softdrop' + str(i), i+1, i+1)
    namesreco_nom_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_nom_softdrop[i].Scale( 1.0 / namesreco_nom_softdrop[i].Integral() )
    namesreco_nom_softdrop[i].Draw('hist')
    legends_nom_softdrop[i].AddEntry(namesreco_nom_softdrop[i], 'Reco_pdfnom_sd', 'l')
    legends_nom_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfnom_softdrop_preplot'+str(i)+'.png')

    

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


###################################################################################################### Unfold data with PDF-NOM
unfold_data_pdfnom = RooUnfoldBayes(pdfnom_response, data_reco, 4)
unfold_data_pdfnom.SetName("unfold_data_pdfnom")
unfolded_data_pdfnom = unfold_data_pdfnom.Hreco().Clone("2d_response_pdfnom_data")

canvases_data_nom = []
namesreco_data_nom = []

legends_data_nom = []
for x in range(0, nptbin):
    canvases_data_nom.append(TCanvas("canvas_data_pdfnom" + str(x)))
    namesreco_data_nom.append(None)
    legends_data_nom.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_nom) : 
    canvas.cd()
    namesreco_data_nom[i] = unfolded_data_pdfnom.ProjectionX('pdf_data_nom' + str(i), i+1, i+1)
    namesreco_data_nom[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_nom[i].Scale( 1.0 / namesreco_data_nom[i].Integral() )
    namesreco_data_nom[i].Draw('hist')
    legends_data_nom[i].AddEntry(namesreco_data_nom[i], 'Reco_pdfnom', 'l')
    legends_data_nom[i].Draw()
    canvas.SaveAs('hists/pdfnom_data_preplot'+str(i)+'.png')

#################################################################################################### Unfold data with PDF-NOM for SoftDrop 
unfold_data_pdfnom_softdrop = RooUnfoldBayes(pdfnom_response_softdrop, data_reco_softdrop, 4)
unfold_data_pdfnom_softdrop.SetName("unfold_data_pdfnom_softdrop")
unfolded_data_pdfnom_softdrop = unfold_data_pdfnom_softdrop.Hreco().Clone("2d_response_pdfnom_softdrop_data")

canvases_data_nom_softdrop = []
namesreco_data_nom_softdrop = []
legends_data_nom_softdrop = []
for x in range(0, nptbin):
    canvases_data_nom_softdrop.append(TCanvas("canvas_data_pdfnom_softdrop"+str(x)))
    namesreco_data_nom_softdrop.append(None)
    legends_data_nom_softdrop.append(TLegend(.7, .5, .9, .7))

for i, canvas in enumerate(canvases_data_nom_softdrop):
    canvas.cd()
    namesreco_data_nom_softdrop[i] = unfolded_data_pdfnom_softdrop.ProjectionX('pdf_data_nom_softdrop' + str(i), i+1, i+1)
    namesreco_data_nom_softdrop[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i]+ ' GeV')
    if options.scale != None and options.scale : 
        namesreco_data_nom_softdrop[i].Scale( 1.0 / namesreco_data_nom_softdrop[i].Integral() )
    namesreco_data_nom_softdrop[i].Draw('hist')
    legends_data_nom_softdrop[i].AddEntry(namesreco_data_nom_softdrop[i], 'Reco_pdfnom_sd', 'l')
    legends_data_nom_softdrop[i].Draw()
    canvas.SaveAs('hists/pdfnom_data_softdrop_preplot'+str(i)+'.png')


    
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







    
outfile = TFile("unfoldedpdf_pdf4lhc15.root", 'RECREATE')
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


unfold_pdfnom.Write()
unfold_pdfnom_softdrop.Write()
unfold_pdfup.Write()
unfold_pdfup_softdrop.Write()
unfold_pdfdn.Write()
unfold_pdfdn_softdrop.Write()
unfold_data_pdfnom.Write()
unfold_data_pdfnom_softdrop.Write()
unfold_data_pdfup.Write()
unfold_data_pdfup_softdrop.Write()
unfold_data_pdfdn.Write()
unfold_data_pdfdn_softdrop.Write()

outfile.Close()
