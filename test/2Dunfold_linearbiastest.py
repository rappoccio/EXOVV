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
                 help='Runs jec for data, correct options are _jecup : _jecdn : _jerup : _jerdn : or nothing at all to get the nominal')
       
(options, args) = parser.parse_args()


ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetTitleOffset(2.0, "Y")

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

niterations = 4

reconom = reco.Clone("recobiased_nom")
unfoldnom = RooUnfoldBayes(response, reconom, niterations)
reconom_unfolded = unfoldnom.Hreco()

reconomSD = recoSD.Clone("recobiasedSD_nom")
unfoldnomSD = RooUnfoldBayes(responseSD, reconomSD, niterations)
reconomSD_unfolded = unfoldnomSD.Hreco()

unfolded = []
unfoldedSD = []

hists = [reco, recoSD]
noms = [ reconom_unfolded, reconomSD_unfolded ]
biased = [ unfolded, unfoldedSD]
names = ['Ungroomed', 'Groomed']
responses = [response, responseSD]

canvs = []
funcs = []

fits2d = []

Nbias = 10
dbias = 0.01

biashist = ROOT.TH1F("biashist", ";Input Slope (1/GeV);Output Slope - Input Slope  (1/GeV)", Nbias, 0, Nbias * dbias )
biashistSD = ROOT.TH1F("biashistSD", ";Input Slope (1/GeV);Output Slope - Input Slope  (1/GeV)", Nbias, 0, Nbias * dbias )
biashists = [biashist, biashistSD]


leg = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.AddEntry( biashist, 'Ungroomed', 'p')
leg.AddEntry( biashistSD, 'Groomed', 'p')

for i in xrange(2) : 
    for j in xrange(0,Nbias+1):

        recobiased = hists[i].Clone("recobiased" + names[i] + "_" + str(i))
        slopex = dbias * j



        for ybin in xrange(1,recobiased.GetNbinsY() ) :
            for xbin in xrange(1,recobiased.GetNbinsX() ) :
                x = recobiased.GetXaxis().GetBinLowEdge(xbin)
                xval = recobiased.GetBinContent(xbin,ybin)
                #print 'x = ', x, ', xval = ', xval
                #print 'changing : ', xval, ' --> ', slopex * x + xval
                recobiased.SetBinContent(xbin,ybin, (1 + slopex * x) * xval )



        unfold = RooUnfoldBayes(responses[i], recobiased, niterations)
        reco_unfolded = unfold.Hreco()
        reco_unfolded.SetName("recoratio" + names[i] + "_" + str(i) )
        reco_unfolded.Divide( noms[i] )
        #reco_unfolded.Draw("colz")

        aSlices = ROOT.TObjArray()
        func = ROOT.TF1("func_" + str(i) + "_" + str(j), "pol1", 0, 2000)
        funcs.append(func)
        reco_unfolded.GetYaxis().SetRangeUser(200.,1300.)

        fit2d = ROOT.TF2("fit2d_" + str(i) + "_" + str(j), "[0]*x + [1]*y + [2]", 0, 2000, 220, 1300)        
        reco_unfolded.Fit( fit2d )
        #fit2d.Print()
        biashists[i].SetBinContent( j, fit2d.GetParameter(0) - slopex )
        biashists[i].SetBinError( j, fit2d.GetParError(0) )
        fits2d.append(fit2d)
        biased[i].append( reco_unfolded )
        

biashists[0].SetMarkerStyle(20)
biashists[1].SetMarkerStyle(21)

biashists[0].Draw("e")
biashists[1].Draw("e same")
leg.Draw()
biashists[0].SetMinimum(-1.0 * dbias * Nbias)
biashists[0].SetMaximum(       dbias * Nbias)

outfile = ROOT.TFile("2Dunfold_linearbiastest.root", "RECREATE")
for xhist in biased :
    for yhist in xhist :
        yhist.Write()
for hist in biashists :
    hist.Write()
outfile.Close()

