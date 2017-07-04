import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
#ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(000000)

from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
from ROOT import RooUnfoldSvd
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--input', action ='store', type = 'string',
                 default ='2DData',
                 dest='input',
                 help='Input file string')
       
(options, args) = parser.parse_args()

nomfile = ROOT.TFile(options.input + '.root')
nom = nomfile.Get('massSD7')
jecupfile = ROOT.TFile(options.input + '_jecup.root')
jecup = jecupfile.Get('massSD7')
jecdnfile = ROOT.TFile(options.input + '_jecdn.root')
jecdn = jecdnfile.Get('massSD7')

nom.SetLineColor(1)
jecup.SetLineColor(2)
jecup.SetLineStyle(2)
jecdn.SetLineColor(4)
jecdn.SetLineStyle(2)

for hist in [nom,jecup,jecdn] :
    for ibin in range(1,nom.GetNbinsX()) :
        if hist.GetBinWidth(ibin) > 0. : 
            hist.SetBinContent( ibin, hist.GetBinContent(ibin) / hist.GetBinWidth(ibin) )

stack = ROOT.THStack("stack", ";Groomed jet mass (GeV)")
stack.Add( nom )
stack.Add( jecup )
stack.Add( jecdn )

stack.Draw('nostack')
