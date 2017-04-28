#! /usr/bin/env python


import ROOT

f1 = ROOT.TFile("responses_rejec_tightgen_otherway_qcdmc_2dplots.root")
f2 = ROOT.TFile("responses_rejec_otherway_qcdmc_2dplots.root")

hist1 = f1.Get("PFJet_pt_m_AK8Gen").Clone("hist1")
hist2 = f2.Get("PFJet_pt_m_AK8Gen").Clone("hist2")

hists1 = []
hists2 = []

canvs = []
stacks = []

for iy in range( 1, hist1.GetNbinsY()+1):
    stack = ROOT.THStack("stack_" + str(iy), ";Jet mass (GeV)")
    proj1 = hist1.ProjectionX("hist1_p" + str(iy), iy, iy+1)
    proj2 = hist2.ProjectionX("hist2_p" + str(iy), iy, iy+1)
    proj1.Scale(1.0/proj1.Integral("width"))
    proj2.Scale(1.0/proj2.Integral("width"))

    for ix in range( 1,proj1.GetNbinsX()+1):
        proj1.SetBinContent( ix, proj1.GetBinContent(ix) / proj1.GetBinWidth(ix) )
        proj2.SetBinContent( ix, proj2.GetBinContent(ix) / proj2.GetBinWidth(ix) )
        proj1.SetBinError( ix, proj1.GetBinError(ix) / proj1.GetBinWidth(ix) )
        proj2.SetBinError( ix, proj2.GetBinError(ix) / proj2.GetBinWidth(ix) )
        
    c = ROOT.TCanvas("c" + str(iy), "c" + str(iy))
    proj1.GetXaxis().SetRangeUser(1, 2000)    
    proj1.SetMarkerStyle(20)
    proj1.SetMarkerColor(1)
    proj2.SetMarkerStyle(21)
    proj2.SetMarkerColor(2)
    stack.Add( proj1 )
    stack.Add( proj2 )
    stack.Draw("nostack")
    stacks.append(stack)
    c.SetLogx()
    canvs.append(c)
    hists1.append(proj1)
    hists2.append(proj2)

    
