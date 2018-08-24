import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
ROOT.gROOT.SetBatch()

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


parser.add_option('--scale', action ='store_true', 
                 default =False,
                 dest='scale',
                 help='Scale hists to unity?')

parser.add_option('--lumi', action ='store', type = 'float',
                 default =2300.,
                 dest='lumi',
                 help='Luminosity')


       
(options, args) = parser.parse_args()

mcfile = TFile('responses_jecsrcs_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')

pt_bin = {0: '200 < p_{T} < 260', 1: '260 < p_{T} < 350', 2: '350 < p_{T} < 460', 3: '460 < p_{T} < 550', 4: '550 < p_{T} < 650', 5: '650 < p_{T} < 760', 6: '760 < p_{T} < 900', 7: '900 < p_{T} < 1000', 8: '1000 < p_{T} < 1100', 9:'1100 < p_{T} < 1200', 10:'1200 < p_{T} < 1300', 11:'1300 < p_{T} < Inf'}
nptbin = len(pt_bin)

if options.extension == "": 
    outfile = TFile('2DData_expunc.root', 'RECREATE')
    outfile2 = TFile('2DData.root', 'RECREATE')
else :
    outfile = TFile('2DData_expunc.root', 'UPDATE')
    outfile2 = TFile('2DData' + options.extension + '.root', 'RECREATE')
outtext = options.extension

response = mcfile.Get('2d_response'+ options.extension)
responseSD = mcfile.Get('2d_response_softdrop' + options.extension)

truth = mcfile.Get('PFJet_pt_m_AK8Gen')
truthSD = mcfile.Get('PFJet_pt_m_AK8SDgen')


reco = datafile.Get('PFJet_pt_m_AK8')
recoSD = datafile.Get('PFJet_pt_m_AK8SD')

reco.Scale(1.0 / options.lumi )
recoSD.Scale(1.0 / options.lumi )

if options.scale != None and options.scale :     
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

hists = []
for i in xrange(0, nptbin  ):
    h = reco_unfolded.ProjectionX('mass' + str(i), i+1, i+1)
    hsd = recoSD_unfolded.ProjectionX('massSD' + str(i), i+1, i+1)
    t = truth.ProjectionX('genmass' + str(i), i+1, i+1)
    tsd = truthSD.ProjectionX('genmassSD' + str(i), i+1, i+1)
    for hist in [h,hsd,t,tsd]:
        hists.append(hist)


    
outfile.cd()
for h in hists:
    if h.Integral() > 0.0:
        h.Scale(1.0 / h.Integral() )
    h.Write()
unfold.Write()
unfoldSD.Write()
outfile.Close()
outfile2.cd()
for h in hists:
    if h.Integral() > 0.0:
        h.Scale(1.0 / h.Integral() )
    h.Write()
outfile2.Close()
