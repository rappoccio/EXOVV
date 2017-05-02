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

                
# First do the experimental uncertainties
sysnames = [
    '',
    '_jerup',
    '_jerdn',
    '_jernom',
    '_jecup',
    '_jecdn',
    '_jmrnom',
    '_jmrup',
    '_jmrdn',
    '_puup',
    '_pudn',
    ]

covs = []
covsSD = []
files = []

for sysname in sysnames :
    f = ROOT.TFile( options.inputs + sysname + '.root')
    cov = f.Get('2d_response' + sysname)
    covSD = f.Get('2d_response_softdrop' + sysname)

    files.append(f)
    covs.append( cov )
    covsSD.append( covSD )


totalcov   = covs[0].Ereco()
totalcovSD = covsSD[0].Ereco()

for ival in range(1,len(covs)):
    totalcov += covs[ival].Ereco()
    totalcovSD += covsSD[ival].Ereco()    

# Next : PDF and PS uncertainties

addTh = True 
if addTh : 
    fpdf = ROOT.TFile("unfoldedpdf.root")
    fps = ROOT.TFile("PS_hists.root")    

    pdfsysnames = [
        '_pdfup',
        '_pdfdn',
        '_cteq',
        '_mstw',
        ]
    mnom = covs[0].response().Eresponse()
    mnomSD = covsSD[0].response().Eresponse()

    mpdf = fpdf.Get( '2d_response_pdfup' ).response().Eresponse()
    mdn  = fpdf.Get( '2d_response_pdfdn' ).response().Eresponse()
    mmstw = fpdf.Get( '2d_response_mstw' ).response().Eresponse()
    mcteq = fpdf.Get( '2d_response_cteq' ).response().Eresponse()
    mpdfSD = fpdf.Get( '2d_response_softdrop_pdfup' ).response().Eresponse()
    mdnSD  = fpdf.Get( '2d_response_softdrop_pdfdn' ).response().Eresponse()
    mmstwSD = fpdf.Get( '2d_response_softdrop_mstw' ).response().Eresponse()
    mcteqSD = fpdf.Get( '2d_response_softdrop_cteq' ).response().Eresponse()
    ps = fps.Get("2d_response").response().Eresponse()
    psSD = fps.Get("2d_response_softdrop_nomnom").response().Eresponse()

    for imat in [mnom, mpdf, mdn, mmstw, mcteq, ps, mnomSD, mpdfSD, mdnSD, mmstwSD, mcteqSD, psSD] :
        normalize( imat )


    mpdf -= mdn
    mmstw -= mnom
    mcteq -= mnom
    mpdfSD -= mdnSD
    mmstwSD -= mnomSD
    mcteqSD -= mnomSD    
    ps -= mnom
    psSD -= mnomSD



    for irow in xrange( totalcov.GetNrows() ) :
        for jcol in xrange( totalcov.GetNcols() ):
            if abs( mnom[irow][jcol] ) > 0. :
                totalcov[irow][jcol] += mpdf[irow][jcol]**2 + mcteq[irow][jcol]**2 + mmstw[irow][jcol]**2 + 0.25*ps[irow][jcol]**2
            if abs( mnomSD[irow][jcol] ) > 0. :
                totalcovSD[irow][jcol] += mpdfSD[irow][jcol]**2 + mcteqSD[irow][jcol]**2 + mmstwSD[irow][jcol]**2 + 0.25*psSD[irow][jcol]**2



covs[0].SetMeasuredCov( totalcov )
covsSD[0].SetMeasuredCov( totalcovSD )

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


import array
Number = 3
Red    = array.array("d", [ 0.00, 1.00, 1.00] );
Green  = array.array("d", [ 0.00, 1.00, 140/255.] );
Blue   = array.array("d", [ 1.00, 1.00, 0.00] );
Length = array.array("d", [ 0.00, 0.51, 1.00] );
nb = 10
ROOT.TColor.CreateGradientColorTable(Number,Length,Red,Green,Blue,nb);



ptbins =[  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300]

axislabels = ROOT.TH2F("axes", ";Reconstructed Bin;Generated Bin", len(ptbins), 0, cor.GetNbinsX(), len(ptbins), 0, cor.GetNbinsX() )
for ibin in xrange(len(ptbins)):
    axislabels.GetXaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )
    axislabels.GetYaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )




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

covSD_canvas.Update()
covSD_canvas.Print("CovarianceMatrixSD_Total.png", "png")
covSD_canvas.Print("CovarianceMatrixSD_Total.pdf", "pdf")
###################



outfile.cd()

totalcov.Write("totalcov")
totalcovSD.Write("totalcovSD")
covs[0].Write("totalcovRooUnfold")
covsSD[0].Write("totalcovSDRooUnfold")
outfile.Close()
