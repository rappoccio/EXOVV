import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
ROOT.gROOT.SetBatch()
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, RooUnfoldBayes
from math import sqrt
from plot_tools import setup, get_ptbins
import pickle


from optparse import OptionParser

############################################################################
############################################################################
####################CALCULATE JACKKNIFE UNCERTAINTY#########################
############################################################################
############################################################################

parser = OptionParser()

parser.add_option('--scale', action='store_true',
                  default = False,
                  dest='scale',
                  help='Scale to unity')


(options, args) = parser.parse_args()
 


pt_bin = {0: '200-260', 1: '260-350', 2: '350-460', 3: '460-550', 4: '550-650', 5: '650-760', 6: '760-900', 7: '900-1000', 8: '1000-1100', 9:'1100-1200', 10:'1200-1300', 11:'1300-1400', 12:'1400-1500', 13:'1500-1600', 14:'1600-1700', 15:'1700-1800', 16:'1800-1900', 17:'1900-2000', 18:'2000-Inf'}

jackknife_mc = ROOT.TFile('jackknife_otherway_repdf.root')
supplementaryMC = ROOT.TFile('responses_rejec_fixjmr_otherway_qcdmc_2dplots.root')
datafile = ROOT.TFile('jetht_weighted_dataplots_otherway_rejec.root')
responses = []
unfolded = []

unfolded_data = []
unfolded_data_softdrop = []

data_hist = datafile.Get('PFJet_pt_m_AK8')
data_hist_softdrop = datafile.Get('PFJet_pt_m_AK8SD')

if options.scale != None and options.scale : 
    data_hist.Scale(1./data_hist.Integral())
    data_hist_softdrop.Scale(1./data_hist_softdrop.Integral())

mc_hist = supplementaryMC.Get('PFJet_pt_m_AK8')
if options.scale != None and options.scale : 
    mc_hist.Scale(1./mc_hist.Integral())

responses_softdrop = []
unfolded_softdrop = []
mc_hist_softdrop = supplementaryMC.Get('PFJet_pt_m_AK8SD')
if options.scale != None and options.scale : 
    mc_hist_softdrop.Scale(1./mc_hist_softdrop.Integral())


for i in range(0, 10):
    responses_softdrop.append(jackknife_mc.Get('2d_response_softdrop'+str(i)))
    responses.append(jackknife_mc.Get('2d_response'+str(i)))

    unfolded_softdrop.append(RooUnfoldBayes(responses_softdrop[i], mc_hist_softdrop, 4).Hreco())
    unfolded.append(RooUnfoldBayes(responses[i], mc_hist, 4).Hreco())

    unfolded_data.append(RooUnfoldBayes(responses[i], data_hist, 4).Hreco())
    unfolded_data_softdrop.append(RooUnfoldBayes(responses_softdrop[i], data_hist_softdrop, 4).Hreco())

    if options.scale != None and options.scale : 
        unfolded_data[i].Scale(1./ unfolded_data[i].Integral())
        unfolded_data_softdrop[i].Scale(1./unfolded_data_softdrop[i].Integral())

        unfolded_softdrop[i].Scale( 1. / unfolded_softdrop[i].Integral())
        unfolded[i].Scale( 1. / unfolded[i].Integral() )
    
    



del responses[:]
del responses_softdrop[:]




def unfold_jackknife( unfoldedlist, pickleoutputname):
    pt_projections = [[] for i in range(0, 10)]
    for i, hist in enumerate(unfoldedlist):
        for j in range(0, 19):
            pt_projections[i].append(hist.ProjectionX('jackknifesample'+str(i)+str(j), j+1, j+1))
    del unfoldedlist[:]
    ### Take the RMS of every mass bin and scale it by 9/10
    massnums = [[[] for i in range(0, 19)] for i in range(0, 10)] 
    for y in range(0, 19):
        for x in range(0, 10):
            for ibin in range(1, pt_projections[x][y].GetNbinsX()):
                massnums[x][y].append(pt_projections[x][y].GetBinContent(ibin))
    # throw away the monstrous list of lists of lists of numbers and make a list of lists of numbers... yep
    RMS_vals = [[] for j in range(0, 19)]
    for y in range(0, 19):
        for numbers in range(0, len(massnums[0][y])):
            mu = 1./10. * ((massnums[0][y][numbers]) + (massnums[1][y][numbers]) + (massnums[2][y][numbers]) + (massnums[3][y][numbers]) + (massnums[4][y][numbers]) + (massnums[5][y][numbers]) + (massnums[6][y][numbers]) + (massnums[7][y][numbers]) + (massnums[8][y][numbers]) + (massnums[9][y][numbers])    )
            RMS_vals[y].append(9./10.*sqrt(1./10. * ((massnums[0][y][numbers] - mu)**2 + (massnums[1][y][numbers]- mu)**2 + (massnums[2][y][numbers]- mu)**2 + (massnums[3][y][numbers]- mu)**2 + (massnums[4][y][numbers]- mu)**2 + (massnums[5][y][numbers]- mu)**2 + (massnums[6][y][numbers]- mu)**2 +     (massnums[7][y][numbers]- mu)**2 + (massnums[8][y][numbers]- mu)**2 + (massnums[9][y][numbers]- mu)**2)))
    ### serialize in binary format with pickle
    pickle.dump(RMS_vals, open(pickleoutputname+".p", "wb"))


postfix = ''
if not options.scale :
    postfix += "_absolute"
unfold_jackknife(unfolded, "ungroomedJackKnifeRMS" + postfix)
unfold_jackknife(unfolded_softdrop, "softdropJackKnifeRMS" + postfix)

unfold_jackknife(unfolded_data, "ungroomeddataJackKnifeRMS" + postfix)
unfold_jackknife(unfolded_data_softdrop, "softdropdataJackKnifeRMS" + postfix)
