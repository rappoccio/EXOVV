#! /usr/bin/env python
import ROOT
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--isSoftDrop', action='store_true',
                  default = False,
                  dest='isSoftDrop',
                  help='theory curves on plots')


parser.add_option('--hist', action='store', type='string',
                  default = 'pythia8_mass',
                  dest='hist',
                  help='histogram')



(options, args) = parser.parse_args()




f1 = ROOT.TFile("2DClosure.root")
f2 = ROOT.TFile("old_2DClosure.root")

hists1 = []
hists2 = []

canvs = []
stacks = []
legs = []

typestr = "RECO"
if "gen" in options.hist :
    typestr = "GEN"

sdstr = ""
sdtitle = typestr + ' Ungroomed jets'
outstr = typestr + "_ungroomed"
if options.isSoftDrop :
    sdstr = "SD"
    sdtitle = typestr + ' Groomed jets'
    outstr = typestr + "_groomed"

for i in xrange(10):
    stack = ROOT.THStack("stack_" + str(i), sdtitle + ";Jet mass (GeV)")
    hist1 = f1.Get(options.hist + sdstr + str(i)).Clone("hist1_" + str(i))
    hist2 = f2.Get(options.hist + sdstr + str(i)).Clone("hist2_" + str(i))
    leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    leg.AddEntry( hist1, "Gen p_{T} Asym.", "p")
    leg.AddEntry( hist2, "No Gen p_{T} Asym.", "p")
    hist1.Scale(1.0/hist1.Integral("width"))
    hist2.Scale(1.0/hist2.Integral("width"))

    for ix in range( 1,hist1.GetNbinsX()+1):
        hist1.SetBinContent( ix, hist1.GetBinContent(ix) / hist1.GetBinWidth(ix) )
        hist2.SetBinContent( ix, hist2.GetBinContent(ix) / hist2.GetBinWidth(ix) )
        hist1.SetBinError( ix, hist1.GetBinError(ix) / hist1.GetBinWidth(ix) )
        hist2.SetBinError( ix, hist2.GetBinError(ix) / hist2.GetBinWidth(ix) )
        
    c = ROOT.TCanvas("c" + str(i), "c" + str(i))
    hist1.GetXaxis().SetRangeUser(1, 2000)    
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerColor(1)
    hist2.SetMarkerStyle(21)
    hist2.SetMarkerColor(2)
    stack.Add( hist1 )
    stack.Add( hist2 )
    stack.Draw("nostack")
    leg.Draw()
    c.SetLogx()
    stacks.append(stack)
    canvs.append(c)
    hists1.append(hist1)
    hists2.append(hist2)
    legs.append(leg)
    c.Print("compare_genmatch_" + outstr + str(i) +".png", "png")
    c.Print("compare_genmatch_" + outstr + str(i) +".pdf", "pdf")
