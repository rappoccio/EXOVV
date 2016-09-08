import ROOT
from ROOT import TCanvas, TLegend
from ROOT import TH1, TH1D, cout, TFile, TH2

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

actualfile = TFile("2DClosure.root")
theoryfile = TFile("theory_predictions.root")

fout = TFile('theory_predictions_normalized.root', 'RECREATE')
fout.cd()


resultbinwidths = [1., 4., 5., 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]

theorybinwidths = [ 1., 4., 5., 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]

legends = []
canvases = []
for j in xrange(0,18):
    legends.append(TLegend(.6, .5, .85, .7))
    canvases.append(TCanvas("theory_SD"+str(j),"theory_SD"+str(j)))
                    
                    

for jbin in xrange(0, 18):
    result = actualfile.Get("pythia8_massSD"+str(jbin))
    theory = theoryfile.Get("histSD1_"+str(jbin))
    theoryU = theoryfile.Get("histSD3_"+str(jbin))
    theoryL = theoryfile.Get("histSD2_"+str(jbin))
    truth = actualfile.Get("genmassSD"+str(jbin))

    leg = legends[jbin]
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    theory.Scale(1.0/theory.Integral())
    theoryU.Scale(1.0/theoryU.Integral())
    theoryL.Scale(1.0/theoryL.Integral())
    result.Scale(1.0/result.Integral())
    truth.Scale(1.0/truth.Integral())

    for ibin in xrange(1, result.GetNbinsX()+1):
        result.SetBinContent(ibin, result.GetBinContent(ibin) * 1./resultbinwidths[ibin-1])
        result.SetBinError(ibin, result.GetBinError(ibin) * 1./resultbinwidths[ibin-1])
        truth.SetBinContent(ibin, truth.GetBinContent(ibin) * 1./resultbinwidths[ibin-1])
        truth.SetBinError(ibin, truth.GetBinError(ibin) * 1./resultbinwidths[ibin-1])

    for ibin in xrange(1, theory.GetNbinsX()+1):
        theory.SetBinContent(ibin, theory.GetBinContent(ibin) * 1./theorybinwidths[ibin-1])
        theory.SetBinError(ibin, theory.GetBinError(ibin) * 1./theorybinwidths[ibin-1])
        theoryU.SetBinContent(ibin, theoryU.GetBinContent(ibin) * 1./theorybinwidths[ibin-1])
        theoryU.SetBinError(ibin, theoryU.GetBinError(ibin) * 1./theorybinwidths[ibin-1])
        theoryL.SetBinContent(ibin, theoryL.GetBinContent(ibin) * 1./theorybinwidths[ibin-1])
        theoryL.SetBinError(ibin, theoryL.GetBinError(ibin) * 1./theorybinwidths[ibin-1])


    theory.SetLineColor(2)
    theoryU.SetLineColor(2)
    theoryU.SetLineStyle(6)
    theoryL.SetLineColor(2)
    theoryL.SetLineStyle(2)
    truth.SetLineColor(4)
    result.SetXTitle("Mass (GeV)")

    canvas = canvases[jbin]
    canvas.SetLogy()

    leg.AddEntry(result, 'Unfolded MC', 'p')
    leg.AddEntry(theory, 'Theory Central Values', 'l')
    leg.AddEntry(theoryU, 'Theory Upper Values', 'l')
    leg.AddEntry(theoryL, 'Theory Lower Values', 'l')
    leg.AddEntry(truth, 'MC Truth', 'l')

    result.GetXaxis().SetRangeUser(0,2000)
    result.SetMarkerStyle(20)
    result.SetMarkerSize(0.5)

    result.Draw()
    theory.Draw("hist SAME")
    theoryU.Draw("hist SAME")
    theoryL.Draw("hist SAME")
    truth.Draw("hist SAME")
    leg.Draw()
    theory.Write()
    theoryU.Write()
    theoryL.Write()

    canvas.SaveAs("TheoryComparison_SD_"+str(jbin)+".png")
    canvas.SaveAs("TheoryComparison_SD_"+str(jbin)+".pdf")
    canvas.Update()

fout.Close()




