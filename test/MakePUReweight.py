import ROOT


fData = ROOT.TFile("exovvhists/exovv_jetht_dataset4_pthi_taucut6_mcut50.root")
fMC = ROOT.TFile("exovvhists/qcd_pthi_taucut6_mcut50.root")

hData = fData.Get("h_NPVert")
hMC = fMC.Get("h_NPVert")

hData.Sumw2()
hMC.Sumw2()

hData.Scale( 1.0 / hData.Integral() )
hMC.Scale( 1.0 / hMC.Integral() )

hData.Divide( hMC )

hData.Draw("e")

fOut = ROOT.TFile("pileup_reweight.root", "RECREATE")
hData.Write()
fOut.Close()
