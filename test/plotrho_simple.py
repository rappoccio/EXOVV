#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--dataFileLo', type='string', action='store',
                  dest='dataFileLo',
                  default = 'rho_plots_pt200to350_mcut50_tau06_data.root',
                  help='Input files for Low Pt')

parser.add_option('--dataFileLoMod', type='string', action='store',
                  dest='dataFileLoMod',
                  default = 'rho_plots_pt200to350_mcut28_tau066_data.root',
                  help='Input files for Low Pt with Modified Tau')

parser.add_option('--dataFileHi', type='string', action='store',
                  dest='dataFileHi',
                  default = 'rho_plots_pt350toInf_mcut50_tau06_data.root',
                  help='Input files for High Pt')

parser.add_option('--mcFileLo', type='string', action='store',
                  dest='mcFileLo',
                  default = 'rho_plots_pt200to350_mcut50_tau06_qcdmc.root',
                  help='Input files for Low Pt')

parser.add_option('--mcFileLoMod', type='string', action='store',
                  dest='mcFileLoMod',
                  default = 'rho_plots_pt200to350_mcut28_tau066_qcdmc.root',
                  help='Input files for Low Pt with Modified Tau')

parser.add_option('--mcFileHi', type='string', action='store',
                  dest='mcFileHi',
                  default = 'rho_plots_pt350toInf_mcut50_tau06_qcdmc.root',
                  help='Input files for High Pt')


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "vv2500invpb_highpt",
                  help='Output string for output file')


parser.add_option('--modTau', type='float', action='store',
                  dest='modTau',
                  default = 0.66,
                  help='Modified tau value')



parser.add_option('--lumi', type='float', action='store',
                  dest='lumi',
                  default = 2500,
                  help='Is this simulation?')

(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)




ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetOptFit(000000)
#ROOT.gROOT.Macro("rootlogon.C")
#ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43)
#ROOT.gStyle.SetTitleFontSize(0.05)
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(30, "XYZ")
#ROOT.gStyle.SetTitleOffset(3.5, "X")
ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")

fHi_data = ROOT.TFile(options.dataFileHi )
hHi_data = fHi_data.Get("rate").Clone()
hHi_data.SetName("hHi_data")
fLo_data = ROOT.TFile(options.dataFileLo )
hLo_data = fLo_data.Get("rate").Clone()
hLo_data.SetName("hLo_data")
fLoMod_data = ROOT.TFile(options.dataFileLoMod )
hLoMod_data = fLoMod_data.Get("rate").Clone()
hLoMod_data.SetName("hLoMod_data")

fHi_mc = ROOT.TFile(options.mcFileHi )
hHi_mc = fHi_mc.Get("rate").Clone()
hHi_mc.SetName("hHi_mc")
fLo_mc = ROOT.TFile(options.mcFileLo )
hLo_mc = fLo_mc.Get("rate").Clone()
hLo_mc.SetName("hLo_mc")
fLoMod_mc = ROOT.TFile(options.mcFileLoMod )
hLoMod_mc = fLoMod_mc.Get("rate").Clone()
hLoMod_mc.SetName("hLoMod_mc")


titles = [
    '200 < p_{T} < 350 GeV, m > 50 GeV, #tau_{21} < 0.6',
    '200 < p_{T} < 350 GeV, m > 28 GeV, #tau_{21} < ' + str(options.modTau),
    'p_{T} > 350 GeV, m > 50 GeV, #tau_{21} < 0.6'
    ]

for hist in [hHi_data,hLo_data,hLoMod_data,hHi_mc,hLo_mc,hLoMod_mc] :
    hist.UseCurrentStyle()

csum = ROOT.TCanvas('csum', 'csum', 600, 600)
csum.cd()
pad1 = ROOT.TPad('p1', 'p1',0.0, 0.0, 1.0, 0.2)
pad1.SetTopMargin(0)
pad1.SetBottomMargin(0.4)
pad1.SetLeftMargin(0.15)
pad1.Draw()
pad2 = ROOT.TPad('p2', 'p2',0.0, 0.2, 1.0, 1.0)
pad2.SetBottomMargin(0)
pad2.SetLeftMargin(0.15)
pad2.Draw()
pad2.cd()
rateMetaData = [
    [24, ROOT.kRed, 2, 3004],
    [20, ROOT.kRed, 1, 3001],
    [21, ROOT.kBlack, 1, 3001],
    ]

ii = 0
leg = ROOT.TLegend(0.17, 0.60, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetNColumns(3)


pad2.cd()

rates = [ hLo_data, hLoMod_data, hHi_data ]
ratemcs = [ hLo_mc, hLoMod_mc, hHi_mc ]


for irate in rates :
    for ibin in range(1,irate.GetNbinsX()) :
        val = irate.GetBinContent(ibin)
        err = 0.
        if abs(val) > 0 : 
            err1 = irate.GetBinError(ibin) / val
            err2 = 0.05
            err = math.sqrt( err1**2 + err2**2) * val
        irate.SetBinError( ibin, err )


for irate in ratemcs :
    for ibin in range(1,irate.GetNbinsX()) :
        val = irate.GetBinContent(ibin)
        err = 0.
        if abs(val) > 0 : 
            err1 = irate.GetBinError(ibin) / val
            err2 = 0.05
            err = math.sqrt( err1**2 + err2**2) * val
        irate.SetBinError( ibin, err )



closureErrors = []
prediction  = ratemcs[1]
truth = ratemcs[2]


# Get the difference in closure in MC, apply that as a systematic in data and MC
for ibin in xrange( 1, truth.GetNbinsX() ) :    
    val = prediction.GetBinContent(ibin)
    err1 = prediction.GetBinError(ibin)
    err2 = abs(prediction.GetBinContent(ibin) - truth.GetBinContent(ibin))
    prediction.SetBinError( ibin, math.sqrt(err1**2 + err2**2) )

    if val > 0.0 : 
        closureErrors.append( math.sqrt(err1**2 + err2**2) / val  )
    else :
        closureErrors.append( 0.0 )


for ival in closureErrors :
    print ' %6.4e' % (ival),
print ''

predictionData = rates[1]
for ibin in xrange( 1, predictionData.GetNbinsX() ) :
    err1 = predictionData.GetBinError(ibin)
    err2 = closureErrors[ibin-1] * predictionData.GetBinContent(ibin)
    predictionData.SetBinError( ibin, math.sqrt(err1**2 + err2**2) )    


    


for irate in xrange( len(rates) ) :
    rate = rates[irate]
    ratemc = ratemcs[irate]
    rate.SetMaximum(2)
    rate.SetMinimum(0)
    leg.AddEntry( rate, titles[irate], '')
    leg.AddEntry( rate, 'Data', 'p')
    rate.SetMarkerStyle( rateMetaData[irate][0] )
    rate.SetMarkerColor( rateMetaData[irate][1] )
    rate.SetLineColor( rateMetaData[irate][1] )
    rate.SetLineStyle( rateMetaData[irate][2] )
    rate.SetTitle(';;Rate')
    rate.SetTitleSize(30, "XYZ")

    
    if irate == 0 :
        rate.Draw("")
    else :
        if irate != 3 or not options.blind : 
            rate.Draw("same")
    ratemc.SetMarkerStyle(0)
    ratemc.SetLineColor( rateMetaData[irate][1] )
    ratemc.SetFillColor( rateMetaData[irate][1] )
    ratemc.SetLineStyle( rateMetaData[irate][2] )
    ratemc.SetFillStyle( rateMetaData[irate][3] )
    
    #ratemc.SetFillColorAlpha( rateMetaData[irate][1], 0.35 )
    ratemc.Draw("e3 same")
    leg.AddEntry( ratemc, 'MC', 'f')
    rate.GetXaxis().SetRangeUser(1e-2,0.3)

leg.Draw()

tlx2 = ROOT.TLatex()
tlx2.SetNDC()
tlx2.SetTextFont(42)
tlx2.SetTextSize(0.057)
tlx2.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(options.lumi) + " pb^{-1}")
tlx2.SetTextSize(0.025)
pad1.cd()
frac = rates[2].Clone()
den = rates[1].Clone()


frac.Divide(den)

frac.UseCurrentStyle()
frac.SetMarkerStyle(20)
frac.SetMarkerSize(1)
frac.SetTitle(';' + hHi_data.GetXaxis().GetTitle() + ';Ratio')
frac.SetTitleSize(20, "XYZ")
frac.Draw("")
frac.Fit('pol0')
frac.SetMinimum(0.)
frac.SetMaximum(2.0)
frac.GetYaxis().SetNdivisions(2,4,0,False)
frac.GetXaxis().SetNdivisions(4,8,0,False)

frac.SetTitle('')
frac.GetXaxis().SetTitle( '#rho = (m/p_{T}R)^{2}' )
frac.GetXaxis().SetTitleOffset(3.5)
frac.GetXaxis().SetRangeUser(1e-2,0.3)
csum.cd()
pad1.SetLogx()
pad2.SetLogx()
#pad2.SetLogy()

csum.Update()
csum.Print( options.outname + '_summary.png', 'png')
csum.Print( options.outname + '_summary.pdf', 'pdf')


print 'Writing output ROOT files'
fout = ROOT.TFile( options.outname + '_rate.root', 'RECREATE')
toWrite = hLoMod_data.Clone()
toWrite.SetName("rLoMod")
toWriteMC = hLoMod_mc.Clone()
toWriteMC.SetName("rLoModMC")
toWrite.Write()
toWriteMC.Write()
fout.Close()
