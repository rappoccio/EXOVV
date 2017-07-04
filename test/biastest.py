import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, TFile, TH2
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TGraph, TMatrixD, TMatrix
from math import sqrt
from array import array
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--extension', action ='store', type = 'string',
                  default ='',
                  dest='extension',
                  help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : or nothing at all to get the nominal')


parser.add_option('--softdrop', action ='store_true',
                  default =False,
                  dest='softdrop',
                  help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : or nothing at all to get the nominal')

parser.add_option('--isBottomLine', action='store_true',
                  default= False,
                  dest='isBottomLine',
                  help='Flag true to run bottom line test on data')


(options, args) = parser.parse_args()
argv = []

myfile = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datfile = TFile('jetht_weighted_dataplots_otherway_rejec.root')
outtext = ''
outfile = None

if options.softdrop == False : 
    response = myfile.Get('2d_response_softdrop' + options.extension)
    if options.isBottomLine:
        reco = datfile.Get('PFJet_pt_m_AK8SD')
        outfile = TFile('2DBottomLine_softdrop' + options.extension + '.root', 'RECREATE')
        outtext = 'BottomLine' + options.extension
    else:
        reco = myfile.Get('PFJet_pt_m_AK8SD')
        outfile = TFile('2DClosure_softdrop' + options.extension + '.root', 'RECREATE')
        outtext = options.extension

    truth = myfile.Get('PFJet_pt_m_AK8SDgen')
else :
    response = myfile.Get('2d_response' + options.extension)
    if options.isBottomLine:
        reco = datfile.Get('PFJet_pt_m_AK8')
        outfile = TFile('2DBottomLine' + options.extension + '.root', 'RECREATE')
        outtext = 'BottomLine' + options.extension
    else:
        reco = myfile.Get('PFJet_pt_m_AK8')
        outfile = TFile('2DClosure' + options.extension + '.root', 'RECREATE')
        outtext = options.extension
    
    truth = myfile.Get('PFJet_pt_m_AK8Gen')
        
c_reco = ROOT.TCanvas("c_reco", "c_reco")
reco.Draw("colz")

#####################

pvalues = array('f', [])
n_iterations = array('f', [])

y_error = array('f', [])
x_error = array('f', [])

c_refoldeds = []
refolded_hists = []
c_sanitys = []
sanity_hists = []
for i in range(1,6,1) :
    print '--------- i = ', i
    unfoldreco = RooUnfoldBayes(response, reco, i)
    reco_unfolded = unfoldreco.Vreco()
    reco_asvector = unfoldreco.Vmeasured()
    m = response.Mresponse()
    print 'response : ', m.GetNrows(), ' x ', m.GetNcols()
    refolded = ROOT.TVectorD(reco_unfolded)
    refolded *= m #TMatrixD(m,TMatrixD.kMult,reco_unfolded)
    print 'refolded : ', refolded.GetNrows()
    refolded_hist = ROOT.TH1D("refolded_hist_" + str(i), "refolded_hist_" + str(i), reco.GetNbinsX()*reco.GetNbinsY(), 0, reco.GetNbinsX()*reco.GetNbinsY() )
    sanity_hist = ROOT.TH1D("sanity_hist_" + str(i), "sanity_hist_" + str(i), reco.GetNbinsX()*reco.GetNbinsY(), 0, reco.GetNbinsX()*reco.GetNbinsY() )
    for ibin in xrange(0, refolded.GetNrows() ) :
        refolded_hist.SetBinContent( ibin+1, refolded[ibin] )
    for ibin in xrange(0, reco_asvector.GetNrows() ) :
        sanity_hist.SetBinContent( ibin+1, reco_asvector[ibin] )        
    refolded_hists.append( refolded_hist )
    sanity_hists.append( sanity_hist )
    #c_refolded = ROOT.TCanvas("c_refolded_" + str(i), "c_refolded_" + str(i))
    #refolded_hist.Draw()
    #c_refoldeds.append(c_refolded)
    #c_sanity = ROOT.TCanvas("c_sanity_" + str(i), "c_sanity_" + str(i))
    #sanity_hist.Draw()
    #c_sanitys.append(c_sanity)    
    

    pvalue = sanity_hist.Chi2Test( refolded_hist)
    pvalues.append( pvalue )
    n_iterations.append( i )
    print 'pvalue = ', pvalue

canvas3 = TCanvas("Pvalue vs n_iterations", "Pvalue vs n_iterations")
canvas3.cd()

plot3 = TGraph( len(n_iterations), n_iterations, pvalues )
plot3.SetMarkerStyle(21)

plot3.SetTitle("Probability vs Number of Iterations; Number of Iterations ; Probability ")
plot3.Draw("AL")
if options.isBottomLine:
    outname = "BottomLine"
else:
    outname = "niteration_optimize"

canvas3.Print(outname+ ".png", "png")
canvas3.Print(outname+ ".pdf", "pdf")




