import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
#ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(000000)
import copy
from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
from ROOT import RooUnfoldSvd
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--inputs', action ='store', type = 'string',
                 default ='2DData',
                 dest='inputs',
                 help='Input file string')
       

parser.add_option('--outfile', action ='store', type = 'string',
                 default ='2DData_sum.root',
                 dest='outfile',
                 help='Output file name')
       
(options, args) = parser.parse_args()


def normalize( m ) :
    isum = 0.0
    for icol in xrange(m.GetNcols()):
        for irow in xrange(m.GetNrows() ):
            isum += m[irow][icol]
    if abs(isum) > 0.0 : 
        for icol in xrange(m.GetNcols()):
            for irow in xrange(m.GetNrows() ):
                m[irow][icol] /= isum



outfile = ROOT.TFile(options.outfile, 'RECREATE')


# Get the nominal responses and covariance matrices
responses = []
responsesSD = []
files = []

fnom = ROOT.TFile( options.inputs + '.root')

ru_nom = fnom.Get('2d_response')
ru_nomSD = fnom.Get('2d_response_softdrop')

mnom = ru_nom.response().Eresponse()
mnomSD = ru_nomSD.response().Eresponse()

responses.append( mnom )
responsesSD.append( mnomSD )
totalcov   = ru_nom.Ereco()
totalcovSD = ru_nomSD.Ereco()



                
# Now do the experimental uncertainties
sysnames = [
    ['_jerup','_jerdn'],
    ['_jecup','_jecdn'],
    ['_jmrup','_jmrdn'],
    ['_puup','_pudn'],
    ]
# Each experimental uncertainty has an "up" and a "down" variation, so
# the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
for sysup,sysdn in sysnames :
    fup = ROOT.TFile( options.inputs + sysup + '.root')
    fdn = ROOT.TFile( options.inputs + sysdn + '.root')
    res = fup.Get('2d_response' + sysup).response().Eresponse()
    resSD = fup.Get('2d_response_softdrop' + sysup).response().Eresponse()
    res -= fdn.Get('2d_response' + sysdn).response().Eresponse()
    resSD -= fdn.Get('2d_response_softdrop' + sysdn).response().Eresponse()
    files.append([fup,fdn])
    responses.append( res )
    responsesSD.append( resSD )


# Next : PDF and PS uncertainties
# For the NNPDF uncertainties ("pdfup" and "pdfdn") these are
# double sided, so (absolute) uncertainty is (up-down)/2 again (factor of 2 will come later). 
# For the CTEQ and MSTW, the uncertainty is |sys-nom|.
fpdf = ROOT.TFile("unfoldedpdf.root")
pdfsysnames = [
    '_pdfup',
    '_pdfdn',
    '_cteq',
    '_mstw',
    ]

mpdf = fpdf.Get( '2d_response_pdfup' ).response().Eresponse()
mpdf  -= fpdf.Get( '2d_response_pdfdn' ).response().Eresponse()
mmstw = fpdf.Get( '2d_response_mstw' ).response().Eresponse()
mcteq = fpdf.Get( '2d_response_cteq' ).response().Eresponse()
mmstw -= mnom
mcteq -= mnom
responses.append( mpdf )
responses.append( mmstw )
responses.append( mcteq )

mpdfSD = fpdf.Get( '2d_response_softdrop_pdfup' ).response().Eresponse()
mpdfSD  -= fpdf.Get( '2d_response_softdrop_pdfdn' ).response().Eresponse()    
mmstwSD = fpdf.Get( '2d_response_softdrop_mstw' ).response().Eresponse()
mcteqSD = fpdf.Get( '2d_response_softdrop_cteq' ).response().Eresponse()
mmstwSD -= mnomSD
mcteqSD -= mnomSD
responsesSD.append( mpdfSD )
responsesSD.append( mmstwSD )
responsesSD.append( mcteqSD )


for res in responses :
    res.Abs()
for res in [mpdf, mcteq, mmstw, mpdfSD, mmstwSD, mcteqSD] :
    res.Abs()

canvs = []
for ires,res in enumerate(responses) :
    c = ROOT.TCanvas("c" + str(ires), "c" + str(ires) )
    res.Draw("colz")
    canvs.append(c)


# For the parton shower uncertainty, we need normalized response matrices
# to check the effects. For the previous ones, we need unnormalized
# response matrices, so first get the errors from previous ones,
# then do parton shower.

# For exp unc as well as PDF, take 0.5*(up-down) (already took the diff above).
for iresp in xrange(1,6):
    for irow in xrange( totalcov.GetNrows() ) :
        for jcol in xrange( totalcov.GetNcols() ):
            if abs( mnom[irow][jcol] ) > 0. :
                #if irow < 20 and jcol < 20 :
                #    print '%6d %6d %6d : %6.2e' % (iresp, irow, jcol, responses[iresp][irow][jcol])
                totalcov[irow][jcol] += ( 0.5 * responses[iresp][irow][jcol] )**2
            if abs( mnomSD[irow][jcol] ) > 0. :
                totalcovSD[irow][jcol] += ( 0.5 * responsesSD[iresp][irow][jcol])**2

# For MSTW and CTEQ, take (weighted-nom) (already took the diff above)
for irow in xrange( totalcov.GetNrows() ) :
    for jcol in xrange( totalcov.GetNcols() ):
        if abs( mnom[irow][jcol] ) > 0. :
            totalcov[irow][jcol] += ( responses[iresp][irow][jcol] )**2
        if abs( mnomSD[irow][jcol] ) > 0. :
            totalcovSD[irow][jcol] += ( responsesSD[iresp][irow][jcol] )**2

            
# Now we need the PS uncertainty itself.
# Now we need to normalize the response matrices for the nominal and PS cases.
# Then the uncertainty is 0.5 * |scalednom-scaledps|*nom (where nom is unscaled)
fps = ROOT.TFile("PS_hists.root")
mps = fps.Get("unfold_ps_data_herwig").response().Eresponse()
mpsSD = fps.Get("unfold_ps_data_softdrop_herwig").response().Eresponse()

mnomNorm = copy.copy( mnom )
mnomNormSD = copy.copy( mnomSD )
for im in [ mnomNorm, mps, mnomNormSD, mpsSD ] :
    normalize (im)
mps -= mnomNorm
mpsSD -= mnomNormSD

print '---- These are the PS uncertainties:'
for irow in xrange( totalcov.GetNrows() ) :
    for jcol in xrange( totalcov.GetNcols() ):
        if abs( mnom[irow][jcol] ) > 0. :
            totalcov[irow][jcol] += (0.5*mps[irow][jcol] * mnom[irow][jcol] )**2
        if abs( mnomSD[irow][jcol] ) > 0. :
            totalcovSD[irow][jcol] += (0.5*mpsSD[irow][jcol] * mnom[irow][jcol] )**2


responses.append( mps )
responsesSD.append( mpsSD )

import math

nb= totalcov.GetNrows()
cor = ROOT.TH2F("cor", "", nb, 0, nb, nb, 0, nb)
corSD = ROOT.TH2F("corSD", "", nb, 0, nb, nb, 0, nb)


for i in xrange(0,nb) :
    for j in xrange(0,nb) :
        Viijj = totalcov[i][i] * totalcov[j][j]
        if Viijj>0.0 :
            cor.SetBinContent(i+1, j+1, totalcov[i][j]/math.sqrt(Viijj))
        
for i in xrange(0,nb) :
    for j in xrange(0,nb) :
        Viijj = totalcovSD[i][i] * totalcovSD[j][j]
        if Viijj>0.0 :
            corSD.SetBinContent(i+1,j+1, totalcovSD[i][j]/math.sqrt(Viijj) )




ptbins =[  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300]

axislabels = ROOT.TH2F("axes", ";Reconstructed Bin;Generated Bin", len(ptbins), 0, cor.GetNbinsX(), len(ptbins), 0, cor.GetNbinsX() )
for ibin in xrange(len(ptbins)):
    axislabels.GetXaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )
    axislabels.GetYaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)



cov_canvas = ROOT.TCanvas("cov_canvas", "response", 800, 800)
cov_canvas.SetRightMargin(0.15)
cov_canvas.SetLeftMargin(0.15)
cov_canvas.SetBottomMargin(0.15)
cov_canvas.SetTopMargin(0.15)
cov_canvas.SetGrid()
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.SetTitle(';Response Matrix Reconstructed p_{T} Bins (GeV);Response Matrix Generated p_{T} Bins (GeV)')
axislabels.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetXaxis().SetTitleOffset(1.5)
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.Draw("axis")
axislabels.SetTitle(';Reconstructed bin;Generated bin')
totalcov.Draw("colz same")
cov_canvas.SetLogz()
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Ungroomed Jets")
cov_canvas.Update()
cov_canvas.Print("CovarianceMatrix_Total.png", "png")
cov_canvas.Print("CovarianceMatrix_Total.pdf", "pdf")

covSD_canvas=TCanvas("covSDcanvas", "covSDcanvas", 800, 800)
covSD_canvas.SetRightMargin(0.15)
covSD_canvas.SetLeftMargin(0.15)
covSD_canvas.SetBottomMargin(0.15)
covSD_canvas.SetTopMargin(0.15)
covSD_canvas.SetGrid()
covSD_canvas.cd()
axislabels.Draw("axis")
axislabels.SetTitle(';Reconstructed bin;Generated bin')
totalcovSD.Draw("colz same")
covSD_canvas.SetLogz()
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Soft Drop Jets")

covSD_canvas.Update()
covSD_canvas.Print("CovarianceMatrixSD_Total.png", "png")
covSD_canvas.Print("CovarianceMatrixSD_Total.pdf", "pdf")
###################

import array
Number = 3
Red    = array.array("d", [ 0.00, 1.00, 1.00] );
Green  = array.array("d", [ 0.00, 1.00, 140/255.] );
Blue   = array.array("d", [ 1.00, 1.00, 0.00] );
Length = array.array("d", [ 0.00, 0.51, 1.00] );
nb = 10
ROOT.TColor.CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);



cor_canvas = ROOT.TCanvas("cor_canvas", "response", 800, 800)
cor_canvas.SetRightMargin(0.15)
cor_canvas.SetLeftMargin(0.15)
cor_canvas.SetBottomMargin(0.15)
cor_canvas.SetTopMargin(0.15)
cor_canvas.SetGrid()
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.SetTitle(';Response Matrix Reconstructed p_{T} Bins (GeV);Response Matrix Generated p_{T} Bins (GeV)')
axislabels.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetXaxis().SetTitleOffset(1.5)
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.Draw("axis")
cor.SetMinimum(-1.0)
cor.SetMaximum(1.0)
cor.SetTitle(';Reconstructed bin;Generated bin')
cor.Draw("colz same")
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Ungroomed Jets")
cor_canvas.Update()
cor_canvas.Print("CorrelationMatrix_Total.png", "png")
cor_canvas.Print("CorrelationMatrix_Total.pdf", "pdf")

corSD_canvas=TCanvas("corSDcanvas", "corSDcanvas", 800, 800)
corSD_canvas.SetRightMargin(0.15)
corSD_canvas.SetLeftMargin(0.15)
corSD_canvas.SetBottomMargin(0.15)
corSD_canvas.SetTopMargin(0.15)
corSD_canvas.SetGrid()
corSD_canvas.cd()
axislabels.Draw("axis")
corSD.SetMinimum(-1.0)
corSD.SetMaximum(1.0)
corSD.SetTitle(';Reconstructed bin;Generated bin')
corSD.Draw("colz same")
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.86, "CMS preliminary")
tlx.DrawLatex(0.7, 0.86, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, "Soft Drop Jets")

corSD_canvas.Update()
corSD_canvas.Print("CorrelationMatrixSD_Total.png", "png")
corSD_canvas.Print("CorrelationMatrixSD_Total.pdf", "pdf")
###################



outfile.cd()

totalcov.Write("totalcov")
totalcovSD.Write("totalcovSD")
ru_nom.Write()
ru_nomSD.Write()
outfile.Close()
