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
       
(options, args) = parser.parse_args()

mcfile = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')

response = mcfile.Get('2d_response'+ options.extension)
responseSD = mcfile.Get('2d_response_softdrop' + options.extension)

truth = mcfile.Get('PFJet_pt_m_AK8Gen')
truthSD = mcfile.Get('PFJet_pt_m_AK8SDgen')


reco = datafile.Get('PFJet_pt_m_AK8')
recoSD = datafile.Get('PFJet_pt_m_AK8SD')

truth.Scale( 1./truth.Integral())
reco.Scale( 1. / reco.Integral() )

truthSD.Scale(1./truthSD.Integral() ) 
recoSD.Scale( 1./recoSD.Integral() )

recos = []
recosSD = []


cu = ROOT.TCanvas("cu", "cu")
for i in xrange(1,6): 
    unfold = RooUnfoldBayes(response, reco, i)


    reco_unfolded = unfold.Hreco()
    reco_unfolded.SetName("recoratio_" + str(i) )

    
    recos.append( reco_unfolded )
    
    if i == 1 : 
        reco_unfolded.Draw("l")
    else :
        reco_unfolded.Draw("l same")
cu.Print("biastest_ungroomed.png", "png")




cg = ROOT.TCanvas("cg", "cg")
for i in xrange(1,6): 
    unfoldSD = RooUnfoldBayes(responseSD, recoSD, i)


    recoSD_unfolded = unfoldSD.Hreco()

    recoSD_unfolded.SetName("recoratioSD_" + str(i) )
    
    recosSD.append( recoSD_unfolded )
    
    if i == 1 : 
        recoSD_unfolded.Draw("l")
    else :
        recoSD_unfolded.Draw("l same")

uncs = []
uncsSD = []
                
for i in xrange(1,len(recos)) :
    unc = recos[i].Clone("unc" + str(i))
    uncSD = recosSD[i].Clone("uncSD" + str(i))
    for x in xrange(1,recos[i].GetNbinsX() +1 ) :
        for y in xrange(1,recos[i].GetNbinsY() +1 ) :
                if recos[i-1].GetBinError(x,y) > 1e-12 :
                        unc.SetBinContent( x, y, recos[i].GetBinError(x,y) / recos[i-1].GetBinError(x,y) )
                if recosSD[i-1].GetBinError(x,y) > 1e-12 :
                        uncSD.SetBinContent( x, y, recosSD[i].GetBinError(x,y) / recosSD[i-1].GetBinError(x,y) )
    uncs.append(unc)
    uncsSD.append(uncSD)

cu.Print("biastest_groomed.png", "png")

fout = ROOT.TFile("biastest_plots.root", "RECREATE")
for i in recos : i.Write()
for i in recosSD : i.Write()
for i in uncs : i.Write()
for i in uncsSD : i.Write()
fout.Close()
