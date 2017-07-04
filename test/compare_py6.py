import ROOT
ROOT.gROOT.SetBatch()

#Files are:
# /uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_5_patch1/src/Analysis/EXOVV/test/qcd_ptflat_pythia6.root
# /uscms_data/d2/rappocc/analysis/EXOVV/CMSSW_7_6_5_patch1/src/Analysis/EXOVV/test/qcd_ptflat_newjec.root



f1 = ROOT.TFile("qcd_ptflat_pythia6.root")
f2 = ROOT.TFile("qcd_ptflat_newjec.root") 
t1 = f1.Get("TreeEXOVV")
t2 = f2.Get("TreeEXOVV")
t1.Draw("FatJetPt[0] >> pt_py6(130, 0, 1300)")
t2.Draw("FatJetPt[0] >> pt_py8(130, 0, 1300)")
t1.Draw("FatJetMass[0] >> m_py6(100, 0, 1000)")
t2.Draw("FatJetMass[0] >> m_py8(100, 0, 1000)")

pt_py6 = ROOT.gDirectory.Get("pt_py6")
pt_py8 = ROOT.gDirectory.Get("pt_py8")
m_py6 = ROOT.gDirectory.Get("m_py6")
m_py8 = ROOT.gDirectory.Get("m_py8")

outfile = ROOT.TFile("py6_vs_py8_bias.root", "RECREATE")
for hist in [pt_py6,pt_py8,m_py6,m_py8] :
    hist.Write()
outfile.Close()
