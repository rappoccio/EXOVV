
import ROOT
f1 = ROOT.TFile("theory_predictions_marzani.root")
f2 = ROOT.TFile("theory_predictions_marzani_newpred.root")
h1 = f1.Get("histSD_5_ours")
h2 = f2.Get("hist_marzani_SD_5")
h1.Draw()
h2.SetLineColor(2)
h2.Draw("same")

