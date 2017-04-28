#! /usr/bin/env python

##################
# Get purity and stability plots for 2d responses
##################

import sys
import math

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'responses_rejec_tightgen_otherway_qcdmc_2dplots.root',
                  help='Input file')

parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = '2d_response',
                  help='Response matrix')

(options, args) = parser.parse_args()
argv = []

import ROOT
#ROOT.gROOT.SetBatch()
ROOT.gSystem.Load("RooUnfold/libRooUnfold.so")
#ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)


ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)

f = ROOT.TFile(options.file)
r = f.Get(options.hist)
h2 = r.Hresponse()

h2pretty = h2.Clone("h2pretty")

title = 'Ungroomed'
if "softdrop" in options.hist :
    title = "Soft Drop"
# Make the histograms

import array

ptbins =array.array('f', [])
mbins =array.array('f', [])

ptbins =array.array('f', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000])
mbins = array.array('f', [0, 1, 5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000])

purity = ROOT.TH1F("purity", title + ";Bin;Fraction", h2.GetNbinsX(), 0, h2.GetNbinsX())
stability = ROOT.TH1F("stability", title + ";Fraction;Bin", h2.GetNbinsX(), 0, h2.GetNbinsX())

purities = []
stabilities = []

purity.GetYaxis().SetTitleOffset(0.8)

stability.SetLineColor(2)


for ipt in xrange( len(ptbins) ):
    purities.append( ROOT.TH1F("purities_" + str(ipt), "pt = " + str(ptbins[ipt]) +';Jet mass (GeV)', len(mbins)-1, mbins) )
    stabilities.append( ROOT.TH1F("stabilities_" + str(ipt), "pt = " + str(ptbins[ipt]) +';Jet mass (GeV)', len(mbins)-1, mbins) )

import array
prettybinHi = ROOT.TH2F("prettybinHi", ";Reconstructed Mass (GeV);Generated Mass (GeV)", len(mbins)-1, array.array('d', mbins ), len(mbins)-1, array.array('d', mbins ) )
prettybinLo = ROOT.TH2F("prettybinLo", ";Reconstructed Mass (GeV);Generated Mass (GeV)", len(mbins)-1, array.array('d', mbins ), len(mbins)-1, array.array('d', mbins ) )




for xbin in xrange( h2pretty.GetNbinsX() ) :
    tot = 0.
    for ybin in xrange( h2pretty.GetNbinsX() ):
        tot += h2pretty.GetBinContent( xbin, ybin )
    for ybin in xrange( h2pretty.GetNbinsX() ):
        frac = 0.
        if tot > 0.0 :
            frac = h2pretty.GetBinContent( xbin, ybin ) / tot
        h2pretty.SetBinContent( xbin, ybin, frac )
        

ibin = 0
for xbin in xrange( h2pretty.GetNbinsX() - len(mbins), h2pretty.GetNbinsX() ) :
    jbin = 0
    for ybin in xrange( h2pretty.GetNbinsY() - len(mbins), h2pretty.GetNbinsY() ) :
        prettybinHi.SetBinContent( ibin, jbin, h2pretty.GetBinContent( xbin, ybin ) )
        jbin += 1
    ibin += 1



ibin = 0
for xbin in xrange( len(mbins), 2* len(mbins) ) :
    jbin = 0
    for ybin in xrange(len(mbins), 2* len(mbins) ) :
        prettybinLo.SetBinContent( ibin, jbin, h2pretty.GetBinContent( xbin, ybin ) )
        jbin += 1
    ibin += 1



cprettyhi = ROOT.TCanvas("cprettyhi", "cprettyhi", 800, 800)
cprettyhi.SetRightMargin(0.15)
cprettyhi.SetLeftMargin(0.15)
cprettyhi.SetBottomMargin(0.15)
cprettyhi.SetTopMargin(0.15)
prettybinHi.GetYaxis().SetTitleOffset(1.5)
prettybinHi.Draw("colz")
cprettyhi.SetLogz()
tlhi = ROOT.TLatex()
tlhi.SetNDC()
tlhi.SetTextFont(43)
tlhi.SetTextSize(30)
tlhi.DrawLatex(0.14, 0.860, "CMS preliminary")
tlhi.DrawLatex(0.7, 0.860, "2.3 fb^{-1} (13 TeV)")
tlhi.SetTextSize(22)
tlhi.DrawLatex(0.2, 0.6, "p_{T} > 1300 GeV")
tlhi.DrawLatex(0.2, 0.57, title + " Jets")
cprettyhi.Update()
cprettyhi.Print("response_hi_" + options.hist + ".pdf", "pdf")
cprettyhi.Print("response_hi_" + options.hist + ".png", "png")


cprettylo = ROOT.TCanvas("cprettylo", "cprettylo", 800, 800)
cprettylo.SetRightMargin(0.15)
cprettylo.SetLeftMargin(0.15)
cprettylo.SetBottomMargin(0.15)
cprettylo.SetTopMargin(0.15)
prettybinLo.GetYaxis().SetTitleOffset(1.5)
prettybinLo.GetXaxis().SetRangeUser(0, 150)
prettybinLo.GetYaxis().SetRangeUser(0, 150)
prettybinLo.Draw("colz")
cprettylo.SetLogz()
tllo = ROOT.TLatex()
tllo.SetNDC()
tllo.SetTextFont(43)
tllo.SetTextSize(30)
tllo.DrawLatex(0.14, 0.860, "CMS preliminary")
tllo.DrawLatex(0.7, 0.860, "2.3 fb^{-1} (13 TeV)")
tllo.SetTextSize(22)
tllo.DrawLatex(0.2, 0.6, "260 < p_{T} < 350 GeV")
tllo.DrawLatex(0.2, 0.57, title + " Jets")
cprettylo.Update()
cprettylo.Print("response_lo_" + options.hist + ".pdf", "pdf")
cprettylo.Print("response_lo_" + options.hist + ".png", "png")




        
for irecopt in xrange(len(ptbins) ):
    for irecom in xrange(len(mbins) ):
        diag = 0
        tot = 0
        recopt = ptbins[irecopt]
        recom = mbins[irecom]
        recobin = irecom + ( len(mbins)-1) * irecopt
        #print 'reco pt: %6d (%6.0f), m: %6d (%6.0f), rbin: %6d' % ( irecopt, recopt, irecom, recom, recobin)
        for igenpt in xrange( len(ptbins) ):
            for igenm in xrange( len(mbins) ):
                genpt = ptbins[igenpt]
                genm = mbins[igenm]
                genbin = igenm + ( len(mbins)-1) * igenpt
                #print 'gen  pt: %6d (%6.0f), m: %6d (%6.0f), gbin: %6d' % ( igenpt, genpt, igenm, genm, genbin),
                #if genm < genpt * 0.8 / math.sqrt(2.0) and recom < recopt * 0.8 / math.sqrt(2.0) :
                if genbin == recobin :
                    #print "THESE BINS MATCH"
                    diag += h2.GetBinContent(recobin, genbin)
                tot += h2.GetBinContent(recobin, genbin)
        if tot > 0.0001 :
            frac = diag / tot
        else :
            frac = 0
        #print '----> frac = %6.4f' % (frac)
        purity.SetBinContent( recobin + 1, frac )
        purities[irecopt].Fill( recom, frac )
        

# Stability
for igenpt in xrange(len(ptbins) ):
    for igenm in xrange(len(mbins) ):
        diag = 0
        tot = 0
        genpt = ptbins[igenpt]
        genm = mbins[igenm]
        genbin = igenm + ( len(mbins)-1) * igenpt
        for irecopt in xrange( len(ptbins) ):
            for irecom in xrange( len(mbins) ):
                recopt = ptbins[irecopt]
                recom = mbins[irecom]                
                recobin = irecom + ( len(mbins)-1) * irecopt
                #if recom < recopt * 0.8 / math.sqrt(2.0) and genm < genpt * 0.8 / math.sqrt(2.0) :
                if recobin == genbin :
                    diag += h2.GetBinContent(recobin, genbin)                
                tot += h2.GetBinContent(recobin, genbin)
        if tot > 0.0001 :
            frac = diag / tot
        else :
            frac = 0
        stability.SetBinContent( genbin + 1, frac )
        stabilities[igenpt].Fill( genm, frac )

print 'Purity: ', purity.Integral()
print 'Stability: ', stability.Integral()




#for ibin in xrange(0, len(ptbins) ) :
#    h2pretty.GetXaxis().SetBinLabel( ibin * ( len(mbins)) + 1, str( int(ptbins[ibin] )) )
#    h2pretty.GetYaxis().SetBinLabel( ibin * ( len(mbins)) + 1, str( int(ptbins[ibin] )) )


axislabels = ROOT.TH2F("axes", ";Reconstructed Bin;Generated Bin", len(ptbins), 0, h2pretty.GetNbinsX(), len(ptbins), 0, h2pretty.GetNbinsX() )
for ibin in xrange(len(ptbins)):
    axislabels.GetXaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )
    axislabels.GetYaxis().SetBinLabel( ibin+1, str( int(ptbins[ibin])) )

c0 = ROOT.TCanvas("c0", "response", 800, 800)
c0.SetRightMargin(0.15)
c0.SetLeftMargin(0.15)
c0.SetBottomMargin(0.15)
c0.SetTopMargin(0.15)
c0.SetGrid()
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.SetTitle(';Response Matrix Reconstructed p_{T} Bins (GeV);Response Matrix Generated p_{T} Bins (GeV)')
axislabels.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetXaxis().SetTitleOffset(1.5)
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.Draw("axis")
h2pretty.GetYaxis().SetTitleOffset(1.5)
h2pretty.GetXaxis().SetLabelSize(0)
h2pretty.GetYaxis().SetLabelSize(0)
h2pretty.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
h2pretty.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
h2pretty.GetXaxis().SetTitleOffset(1.5)
h2pretty.GetYaxis().SetTitleOffset(1.5)
h2pretty.Draw("colz same")


c0.SetLogz()
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.860, "CMS preliminary")
tlx.DrawLatex(0.7, 0.860, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, title + " Jets")
#xaxis1.Draw()
c0.Update()
c0.Print("response_" + options.hist + ".pdf", "pdf")
c0.Print("response_" + options.hist + ".png", "png")



c1 = ROOT.TCanvas("c1", "xpurity")
leg = ROOT.TLegend(0.7, 0.7, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.AddEntry( purity, 'Purity', 'l')
leg.AddEntry( stability, 'Stability', 'l')
purity.Draw()
stability.Draw("same")
purity.SetMaximum(1.0)
#purity.GetXaxis().SetRangeUser(0,400)
purity.GetXaxis().SetNdivisions( len(ptbins), False)
leg.Draw()
c1.Update()
outstr = "ungroomed"
c1.Print("purity_stability_" + options.hist + ".pdf", "pdf")
c1.Print("purity_stability_" + options.hist + ".png", "png")






h2pretty_ptonly = h2pretty.Clone("h2pretty_ptonly")
h2pretty_ptonly.Rebin2D(len(mbins)-1,len(mbins)-1)


c2 = ROOT.TCanvas("c2", "response", 800, 800)
c2.SetRightMargin(0.15)
c2.SetLeftMargin(0.15)
c2.SetBottomMargin(0.15)
c2.SetTopMargin(0.15)
c2.SetGrid()
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.SetTitle(';Response Matrix Reconstructed p_{T} Bins (GeV);Response Matrix Generated p_{T} Bins (GeV)')
axislabels.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
axislabels.GetXaxis().SetTitleOffset(1.5)
axislabels.GetYaxis().SetTitleOffset(1.5)
axislabels.Draw("axis")
h2pretty_ptonly.GetYaxis().SetTitleOffset(1.5)
h2pretty_ptonly.GetXaxis().SetLabelSize(0)
h2pretty_ptonly.GetYaxis().SetLabelSize(0)
h2pretty_ptonly.GetXaxis().SetNdivisions( 400 + len(ptbins), False)
h2pretty_ptonly.GetYaxis().SetNdivisions( 400 + len(ptbins), False)
h2pretty_ptonly.GetXaxis().SetTitleOffset(1.5)
h2pretty_ptonly.GetYaxis().SetTitleOffset(1.5)
h2pretty_ptonly.Draw("colz same")





c2.SetLogz()
tlx = ROOT.TLatex()
tlx.SetNDC()
tlx.SetTextFont(43)
tlx.SetTextSize(30)
tlx.DrawLatex(0.14, 0.860, "CMS preliminary")
tlx.DrawLatex(0.7, 0.860, "2.3 fb^{-1} (13 TeV)")
tlx.SetTextSize(22)
tlx.DrawLatex(0.2, 0.6, title + " Jets")
#xaxis1.Draw()
c2.Update()
c2.Print("responsept_" + options.hist + ".pdf", "pdf")
c2.Print("responsept_" + options.hist + ".png", "png")

canvs = []
prettylegs = []
for ipt in xrange( len(ptbins) ):
    verbosecanv = ROOT.TCanvas("vc" + str(ipt), "vc" + str(ipt) )    
    prettyleg = ROOT.TLegend( 0.7, 0.7, 0.9, 0.9)
    prettyleg.SetFillColor(0)
    prettyleg.SetBorderSize(0)
    prettyleg.AddEntry( purities[ipt], "Purity", 'l')
    prettyleg.AddEntry( stabilities[ipt], "Stability", 'l')
    purities[ipt].Draw("hist")
    purities[ipt].SetMaximum(1.0)
    stabilities[ipt].SetLineStyle(2)
    stabilities[ipt].SetLineColor(2)
    stabilities[ipt].Draw("hist same")    
    prettyleg.Draw()
    verbosecanv.SetLogx()
    prettylegs.append(prettyleg)
    canvs.append(verbosecanv)
    if "softdrop" in options.hist :
        verbosecanv.Print( 'purity_stability_pt_' + str(ipt) + '_groomed.png', 'png' )
        verbosecanv.Print( 'purity_stability_pt_' + str(ipt) + '_groomed.pdf', 'pdf' )
    else:
        verbosecanv.Print( 'purity_stability_pt_' + str(ipt) + '_ugroomed.png', 'png' )
        verbosecanv.Print( 'purity_stability_pt_' + str(ipt) + '_ugroomed.pdf', 'pdf' )
