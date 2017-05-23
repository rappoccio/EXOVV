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


def normalize(vec):
    norm = 0.
    for i in range(vec.GetNrows() ):
        norm += vec[i]
    if abs(norm) > 0.0 : 
        for i in range(vec.GetNrows() ):
            vec[i] /= norm

parser.add_option('--input', action ='store', type = 'string',
                 default ='2DData_sum.root',
                 dest='input',
                 help='Input file string')
       
(options, args) = parser.parse_args()

f = ROOT.TFile(options.input)

totalcov   = f.Get("totalcovRooUnfold")
totalcovSD = f.Get("totalcovSDRooUnfold")
c= ROOT.TCanvas("c", "c")
totalcov.Draw("colz")
c.SetLogz()


totalcovinv = totalcov.Wreco() #ROOT.TDecompSVD( totalcov ).Invert()
totalcovinvSD = totalcovSD.Wreco() #ROOT.TDecompSVD( totalcovSD ).Invert()


# For the theory predictions.
pythiahists = []
herwighists = []

pythiahistsSD = []
herwighistsSD = []
fryehistsSD = []
marzanihistsSD = []

pythiavector = ROOT.TVectorD( totalcovinv.GetNrows() )
herwigvector = ROOT.TVectorD( totalcovinv.GetNrows() )
pythiavectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
herwigvectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
fryevectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
marzanivectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )

dpythiavector = ROOT.TVectorD( totalcovinv.GetNrows() )
dherwigvector = ROOT.TVectorD( totalcovinv.GetNrows() )
dpythiavectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
dherwigvectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
dfryevectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )
dmarzanivectorSD = ROOT.TVectorD( totalcovinv.GetNrows() )



obshists = []
obshistsSD = []
obsvec = ROOT.TVectorD( totalcovinv.GetNrows() )
obsvecSD = ROOT.TVectorD( totalcovinv.GetNrows() )
dobsvec = ROOT.TVectorD( totalcovinv.GetNrows() )
dobsvecSD = ROOT.TVectorD( totalcovinv.GetNrows() )


predvecs = [ obsvec, obsvecSD, pythiavector, herwigvector,  pythiavectorSD, herwigvectorSD, fryevectorSD, marzanivectorSD]
dpredvecs = [ dobsvec, dobsvecSD, dpythiavector, dherwigvector, dpythiavectorSD, dherwigvectorSD, dfryevectorSD, dmarzanivectorSD]

chi2vectors = [] 

# Next : PDF and PS uncertainties

fdef = ROOT.TFile("2DData.root")
fpdf = ROOT.TFile("unfoldedpdf.root")
fps = ROOT.TFile("PS_hists.root")
ffrye = ROOT.TFile("theory_predictions.root")
fmarzani = ROOT.TFile("theory_predictions_marzani_newpred.root")

# Get the theory predictions
for iptbin in xrange(11):
    obshists.append( fdef.Get('mass' + str(iptbin) ) )
    obshistsSD.append( fdef.Get('massSD' + str(iptbin) ) )
    pythiahists.append( fdef.Get('genmass' + str(iptbin)) )
    pythiahistsSD.append( fdef.Get('genmassSD' + str(iptbin)) )
    herwighists.append( fps.Get("herwig_gen" + str(iptbin)) )
    herwighistsSD.append( fps.Get("herwig_gen_softdrop" + str(iptbin)) )
    fryehistsSD.append( ffrye.Get("histSD_" + str(iptbin) + "_ours") )
    marzanihistsSD.append( fmarzani.Get("hist_marzani_SD_" + str(iptbin)) )


nmassbins = pythiahists[0].GetNbinsX()

for jhist, hists in enumerate ([ obshists, obshistsSD, pythiahists, pythiahistsSD, herwighists, herwighistsSD, fryehistsSD, marzanihistsSD ]):
    
    vecbin = 0
    for iptbin in xrange(11) :
        hist = hists[iptbin]
        #if ( hist.Integral() > 0.0 ):
        #    hist.Scale(1.0 / hist.Integral() )
        for mval in range( 1, hist.GetNbinsX() + 1 ) :
            predvecs[jhist][vecbin] = hist.GetBinContent( mval )
            dpredvecs[jhist][vecbin] = hist.GetBinError( mval )
            vecbin += 1

#for ivec in [obsvec, obsvecSD, pythiavector, herwigvector, pythiavectorSD, herwigvectorSD, fryevectorSD, marzanivectorSD] :
#    normalize(ivec)

            
import copy

pythiavector    -= obsvec
herwigvector    -= obsvec
pythiavectorSD  -= obsvecSD
herwigvectorSD  -= obsvecSD
fryevectorSD    -= obsvecSD
marzanivectorSD -= obsvecSD

Lpythiavector    = copy.copy( pythiavector )
Lherwigvector    = copy.copy( herwigvector )
LpythiavectorSD  = copy.copy( pythiavectorSD )
LherwigvectorSD  = copy.copy( herwigvectorSD )
LfryevectorSD    = copy.copy( fryevectorSD )
LmarzanivectorSD = copy.copy( marzanivectorSD )
            
pythiavector    *= totalcovinv
herwigvector    *= totalcovinv
pythiavectorSD  *= totalcovinvSD
herwigvectorSD  *= totalcovinvSD
fryevectorSD    *= totalcovinvSD
marzanivectorSD *= totalcovinvSD

pythiachi2 = [ 0.0 ] * 11
herwigchi2 = [ 0.0 ] * 11
pythiachi2SD = [ 0.0 ] * 11
herwigchi2SD = [ 0.0 ] * 11
fryechi2SD = [ 0.0 ] * 11
marzanichi2SD = [ 0.0 ] * 11

for iptbin in xrange(11):
    chi2pythia = 0.0
    chi2herwig = 0.0
    chi2pythiaSD = 0.0
    chi2herwigSD = 0.0
    chi2fryeSD = 0.0
    chi2marzaniSD = 0.0
    for im in xrange( nmassbins ) :
        ibin = im + iptbin * nmassbins
        chi2pythia += abs( Lpythiavector[ ibin ] * pythiavector[ibin] )
        chi2herwig += abs( Lherwigvector[ ibin ] * herwigvector[ibin] )
        chi2pythiaSD += abs( LpythiavectorSD[ ibin ] * pythiavectorSD[ibin] )
        chi2herwigSD += abs( LherwigvectorSD[ ibin ] * herwigvectorSD[ibin] )
        chi2fryeSD += abs( LfryevectorSD[ ibin ] * fryevectorSD[ibin] )
        chi2marzaniSD += abs( LmarzanivectorSD[ ibin ] * marzanivectorSD[ibin] )
    pchi2pythia = ROOT.TMath.Prob( chi2pythia, nmassbins )
    pchi2herwig = ROOT.TMath.Prob( chi2herwig, nmassbins )
    pchi2pythiaSD = ROOT.TMath.Prob( chi2pythiaSD, nmassbins )
    pchi2herwigSD = ROOT.TMath.Prob( chi2herwigSD, nmassbins )
    pchi2fryeSD = ROOT.TMath.Prob( chi2fryeSD, nmassbins )
    pchi2marzaniSD = ROOT.TMath.Prob( chi2marzaniSD, nmassbins )
    print ' %6d & %12.3e & %12.3e & %12.3e & %12.3e & %12.3e & %12.3e \\\\' % ( iptbin, pchi2pythia, pchi2herwig, pchi2pythiaSD, pchi2herwigSD, pchi2fryeSD, pchi2marzaniSD )
    
# Now calculate the chi2 per pt bin. The individual values are stored as elements in a vector
#pyval = totalcovinv * pythiavector
#print pyval
