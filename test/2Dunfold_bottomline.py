import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
ROOT.gROOT.SetBatch()
import math

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
       
(options, args) = parser.parse_args()

mcfile = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')

response = mcfile.Get('2d_response'+ options.extension)
responseSD = mcfile.Get('2d_response_softdrop' + options.extension)

truth = mcfile.Get('PFJet_pt_m_AK8Gen')
truthSD = mcfile.Get('PFJet_pt_m_AK8SDgen')


reco = mcfile.Get('PFJet_pt_m_AK8')
recoSD = mcfile.Get('PFJet_pt_m_AK8SD')

#truth.Scale( 1./truth.Integral())
#reco.Scale( 1. / reco.Integral() )

#truthSD.Scale(1./truthSD.Integral() ) 
#recoSD.Scale( 1./recoSD.Integral() )

unfold = RooUnfoldBayes(response, reco, 4)    
reco_unfolded = unfold.Vreco()
reco_det = unfold.Vmeasured()
response = unfold.response()
mresponse = response.Mresponse()
truth = response.Vtruth()
truth_folded = ROOT.TVectorD(truth)
truth_folded *= mresponse
errs = unfold.ErecoV(2)
print errs
for ival in xrange( reco_det.GetNrows() ):
    reco_det[ival] -= truth_folded[ival]
#    reco_det[ival] /= errs[ival]
for ival in xrange( reco_unfolded.GetNrows() ):
    reco_unfolded[ival] -= truth[ival]
    if errs[ival] > 0.0 : 
        reco_unfolded[ival] /= math.sqrt(errs[ival])
print 'Ungroomed:'
print 'Chi2_folded   = ',  reco_det.Norm1()
print 'Chi2_unfolded = ', reco_unfolded.Norm1()



unfoldSD = RooUnfoldBayes(responseSD, recoSD, 4)    
reco_unfoldedSD = unfoldSD.Vreco()
reco_detSD = unfoldSD.Vmeasured()
responseSD = unfoldSD.response()
mresponseSD = responseSD.Mresponse()
truthSD = responseSD.Vtruth()
truth_foldedSD = ROOT.TVectorD(truthSD)
truth_foldedSD *= mresponseSD
errsSD = unfoldSD.ErecoV(2)

for ival in xrange( reco_detSD.GetNrows() ):
    reco_detSD[ival] -= truth_foldedSD[ival]
#    reco_det[ival] /= errs[ival]
for ival in xrange( reco_unfoldedSD.GetNrows() ):
    reco_unfoldedSD[ival] -= truthSD[ival]
    if errsSD[ival] > 0.0:
        reco_unfoldedSD[ival] /= math.sqrt(errsSD[ival])
print 'Groomed:'
print 'Chi2_folded   = ',  reco_detSD.Norm1()
print 'Chi2_unfolded = ', reco_unfoldedSD.Norm1()
