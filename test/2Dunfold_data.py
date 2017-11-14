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

if options.extension == "": 
    outfile = TFile('2DData_expunc.root', 'RECREATE')
else :
    outfile = TFile('2DData_expunc.root', 'UPDATE')
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


    
outfile.cd()
unfold.Write()
unfoldSD.Write()
outfile.Close()
