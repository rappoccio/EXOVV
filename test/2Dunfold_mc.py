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


response = myfile.Get('2d_response' + options.extension)
outfile = TFile('2DClosure' + options.extension + '.root', 'RECREATE')
outtext = options.extension

truth = myfile.Get('PFJet_pt_m_AK8Gen')
reco = myfile.Get('PFJet_pt_m_AK8')

response.Draw('colz')


unfold = RooUnfoldBayes(response, reco, 6)
#unfold= RooUnfoldSvd(response, reco, 5);

reco_unfolded = unfold.Hreco()

reco_unfolded.Draw()

truth.SetLineColor(4)

truth.Draw('SAME')

c2 = TCanvas()
c3 = TCanvas()
c4 = TCanvas()
c5 = TCanvas()
c6 = TCanvas()
c7 = TCanvas()
c8 = TCanvas()

canvases = {c2, c3, c4, c5, c6, c7, c8}

pt_bins = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6}

pt_bin = {0: '200-240', 1: '240-310', 2: '310-400', 3: '400-530', 4: '530-650', 5: '650-760', 6: '760-Inf'}

bin1 = None
bin2 = None
bin3 = None
bin4 = None
bin5 = None
bin6 = None
bin7 = None

namesreco = [ bin1, bin2, bin3, bin4, bin5, bin6, bin7 ]

genbin1 = None
genbin2 = None
genbin3 = None
genbin4 = None
genbin5 = None
genbin6 = None
genbin7 = None

namesgen = [ genbin1, genbin2, genbin3, genbin4, genbin5, genbin6, genbin7 ]

leg1 = TLegend(.7, .5, .9, .7)
leg2 = TLegend(.7, .5, .9, .7)
leg3 = TLegend(.7, .5, .9, .7)
leg4 = TLegend(.7, .5, .9, .7)
leg5 = TLegend(.7, .5, .9, .7)
leg6 = TLegend(.7, .5, .9, .7)
leg7 = TLegend(.7, .5, .9, .7)

legends = [leg1, leg2, leg3, leg4, leg5, leg6, leg7]

for i, canvas in enumerate(canvases) : 
    canvas.cd()
    namesreco[i] = reco_unfolded.ProjectionY('mass' + str(i), i, pt_bins[i])
    namesreco[i].SetTitle('Mass Projection for P_{T} ' + pt_bin[i] + ' GeV')
    namesreco[i].Draw('hist')
    namesgen[i] = truth.ProjectionY('genmass' + str(i), i, pt_bins[i])
    namesgen[i].SetLineColor(4)
    namesgen[i].Draw('same hist')
    legends[i].AddEntry(namesreco[i], 'Reco', 'l')
    legends[i].AddEntry(namesgen[i], 'Gen', 'l')
    legends[i].Draw()
    canvas.SaveAs('unfolded_closure_preplotter_'+pt_bin[i] + options.extension + '.png')
    
outfile.cd()
for hists in namesreco:
    hists.Write()
for stuff in namesgen:
    stuff.Write()
outfile.Write()
outfile.Close()
