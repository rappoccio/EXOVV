#!/usr/bin/env python
from optparse import OptionParser
import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend
from ROOT import gRandom, TH1, TH1D, cout, TFile, TH2
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TGraphErrors
from math import sqrt
from array import array

parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = "qcdsysplot_qcdsys.root",
                  help='Input file')




parser.add_option('--hist', type='string', action='store',
                  dest='hist',
                  default = "h_pt",
                  help='Histogram to plot')



parser.add_option('--sys', type='string', action='store',
                  dest='sys',
                  default = "pdf",
                  help='systematic to plot')



parser.add_option('--title', type='string', action='store',
                  dest='title',
                  default = "PDF",
                  help='Title')



(options, args) = parser.parse_args()
argv = []

import ROOT
import array
import math
import random


ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "XY")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(25,"XYZ")

g = TFile('qcdmc_stitched_qcdmc.root')


#f = ROOT.TFile(options.file)
#f.ls()

#print 'Getting ' + options.hist + "_nom"
if options.hist == "h_msd" :

    hnom1 = g.Get( "PFJet_pt_m_AK8SD" )
else:
    hnom1 = g.Get( "PFJet_pt_m_AK8" )

#print 'Getting ' + options.hist + "_" + options.sys + "nom"
#hnom1 = f.Get( options.hist + "_" + options.sys + "nom" )
#print 'Getting ' + options.hist + "_" + options.sys + "up"
#hup1 = f.Get( options.hist + "_" + options.sys + "up" )
#print 'Getting ' + options.hist + "_" + options.sys + "dn"
#hdn1 = f.Get( options.hist + "_" + options.sys + "dn" )


NomResponse = g.Get('2d_response')
NomResponseSD = g.Get('2d_response_softdrop')

if options.sys == "jes" :


    UpResponse = g.Get('2d_response_jecup')
    DnResponse = g.Get('2d_response_jecdn')

    UpResponseSD = g.Get('2d_response_softdrop_jecup')
    DnResponseSD = g.Get('2d_response_softdrop_jecdn')


else :
    
    UpResponse = g.Get('2d_response_'+ options.sys +'up')
    DnResponse = g.Get('2d_response_'+ options.sys +'dn')
    
    UpResponseSD = g.Get('2d_response_softdrop_'+ options.sys +'up')
    DnResponseSD = g.Get('2d_response_softdrop_'+ options.sys +'dn')



if options.hist == 'h_msd' :

    unfold_hnom = RooUnfoldBayes(NomResponseSD, hnom1, 4)
    unfold_hup = RooUnfoldBayes(UpResponseSD, hnom1, 4)
    unfold_hdn = RooUnfoldBayes(DnResponseSD, hnom1, 4)

else:

    unfold_hnom = RooUnfoldBayes(NomResponse, hnom1, 4)
    unfold_hup = RooUnfoldBayes(UpResponse, hnom1, 4)
    unfold_hdn = RooUnfoldBayes(DnResponse, hnom1, 4)

hnom2 = unfold_hnom.Hreco()
hup2 = unfold_hup.Hreco()
hdn2 = unfold_hdn.Hreco()

hnom = hnom2.ProjectionY()
hup = hup2.ProjectionY()
hdn = hdn2.ProjectionY()

hnom.Scale(1.0/hnom.Integral())
hup.Scale(1.0/hup.Integral())
hdn.Scale(1.0/hdn.Integral())

#hnom2.Scale(1.0/hnom2.Integral())
#hup2.Scale(1.0/hup2.Integral())
#hdn2.Scale(1.0/hdn2.Integral())


'''
hnom_1 = hnom2.ProjectionY("200-260GeV", 1, 1)
hnom_2 = hnom2.ProjectionY("260-350GeV", 2, 2)
hnom_3 = hnom2.ProjectionY("350-460GeV", 3, 3)
hnom_4 = hnom2.ProjectionY("460-550GeV", 4, 4)
hnom_5 = hnom2.ProjectionY("550-650GeV", 5, 5)
hnom_6 = hnom2.ProjectionY("650-760GeV", 6, 6)
hnom_7 = hnom2.ProjectionY("760GeV", 7, 7)

hup_1 = hup2.ProjectionY("up200-260GeV", 1, 1)
hup_2 = hup2.ProjectionY("up260-350GeV", 2, 2)
hup_3 = hup2.ProjectionY("up350-460GeV", 3, 3)
hup_4 = hup2.ProjectionY("up460-550GeV", 4, 4)
hup_5 = hup2.ProjectionY("up550-650GeV", 5, 5)
hup_6 = hup2.ProjectionY("up650-760GeV", 6, 6)
hup_7 = hup2.ProjectionY("up760GeV", 7, 7)

hdn_1 = hdn2.ProjectionY("dn200-260GeV", 1, 1)
hdn_2 = hdn2.ProjectionY("dn260-350GeV", 2, 2)
hdn_3 = hdn2.ProjectionY("dn350-460GeV", 3, 3)
hdn_4 = hdn2.ProjectionY("dn460-550GeV", 4, 4)
hdn_5 = hdn2.ProjectionY("dn550-650GeV", 5, 5)
hdn_6 = hdn2.ProjectionY("dn650-760GeV", 6, 6)
hdn_7 = hdn2.ProjectionY("dn760GeV", 7, 7)

c1 = ROOT.TCanvas("c1", "c1")
c2 = ROOT.TCanvas("c2", "c2")
c3 = ROOT.TCanvas("c3", "c3")
c4 = ROOT.TCanvas("c4", "c4")
c5 = ROOT.TCanvas("c5", "c5")
c6 = ROOT.TCanvas("c6", "c6")
c7 = ROOT.TCanvas("c7", "c7")

tlx1 = ROOT.TLatex()
tlx2 = ROOT.TLatex()
tlx3 = ROOT.TLatex()
tlx4 = ROOT.TLatex()
tlx5 = ROOT.TLatex()
tlx6 = ROOT.TLatex()
tlx7 = ROOT.TLatex()

atlx = [tlx1, tlx2, tlx3, tlx4, tlx5, tlx6, tlx7]

ptbins = ['#bf{p_{T} 200-260 GeV}','#bf{p_{T} 260-350 GeV}','#bf{p_{T} 350-460 GeV}','#bf{p_{T} 460-550 GeV}','#bf{p_{T} 550-650 GeV}','#bf{p_{T} 650-760 GeV}','#bf{p_{T} >760 GeV}']

hnomlist = [hnom_1, hnom_2, hnom_3, hnom_4, hnom_5, hnom_6, hnom_7]
huplist = [hup_1, hup_2, hup_3, hup_4, hup_5, hup_6, hup_7]
hdownlist = [hdn_1, hdn_2, hdn_3, hdn_4, hdn_5, hdn_6, hdn_7]
clist = [c1, c2, c3, c4, c5, c6, c7]

for i, nom in enumerate(hnomlist):
    up = huplist[i]
    dn = hdownlist[i]
    up.Divide(nom)
    dn.Divide(nom)
    
    reachedSmoothUP = False
    for ibin in xrange(0,up.GetNbinsX()+1):
        print ibin
        val = float(up.GetBinContent(ibin))
        print val
        err = float(abs((up.GetBinContent(ibin)-nom.GetBinContent(ibin))))
        print err
        if val != 0.0 :
            reachedSmoothUP = True
        else:
            reachedSmoothUP = False
        if reachedSmoothUP and err/val > 1.0 :
            up.SetBinContent(ibin, 0.)
            up.SetBinError( ibin, 0.)

    reachedSmoothDN = False
    for ibin in xrange(0,dn.GetNbinsX()+1):
        print ibin
        val = float(dn.GetBinContent(ibin))
        print val
        err = float(abs((dn.GetBinContent(ibin)-nom.GetBinContent(ibin))))
        print err
        if val != 0.0 :
            reachedSmoothDN = True
        else:
            reachedSmoothDN = False
        if reachedSmoothDN and err/val > 1.0 :
            dn.SetBinContent(ibin, 0.)
            dn.SetBinError( ibin, 0.)


    clist[i].cd()
    up.SetLineStyle(2)
    dn.SetLineStyle(3)
    up.Draw("hist")
    dn.Draw("hist same")
    up.GetYaxis().SetTitle(options.title + " Variation")
    up.GetYaxis().SetTitleSize(15)
    up.GetYaxis().SetLabelSize(15)
    up.SetTitle(options.title + " Variation Unfolded")
    up.GetXaxis().SetTitle("Jet Mass (GeV)")
    up.SetMinimum(0.0)
    up.SetMaximum(2.0)
    atlx[i].DrawLatex(679.598 , 1.28602 , ptbins[i])
    if options.hist == "h_msd" :
        clist[i].SaveAs(options.sys+"UnfoldedSD_"+str(i)+".png")
    else:
        clist[i].SaveAs(options.sys+"Unfolded_"+str(i)+".png")
    clist[i].Update()
'''

hup.Divide(hnom)
hdn.Divide(hnom)

reachedSmoothUP = False
for ibin in xrange(0,hup.GetNbinsX()+1):
    #print ibin
    val = float(hup.GetBinContent(ibin))
    #print val
    err = float(abs((hup.GetBinContent(ibin)-hnom.GetBinContent(ibin))))
    #print err
    if val != 0.0 :
        reachedSmoothUP = True
    else:
        reachedSmoothUP = False
    if reachedSmoothUP and err/val > 1.0 :
        hup.SetBinContent(ibin, 0.)
        hup.SetBinError( ibin, 0.)

reachedSmoothDN = False
for ibin in xrange(0,hdn.GetNbinsX()+1):
    #print ibin
    val = float(hdn.GetBinContent(ibin))
    #print val
    err = float(abs((hdn.GetBinContent(ibin)-hnom.GetBinContent(ibin))))
    #print err
    if val != 0.0 :
        reachedSmoothDN = True
    else:
        reachedSmoothDN = False
    if reachedSmoothDN and err/val > 1.0 :
        hdn.SetBinContent(ibin, 0.)
        hdn.SetBinError( ibin, 0.)

c = ROOT.TCanvas("c", "c")
hup.SetLineStyle(2)
hdn.SetLineStyle(3)

hup.Draw("hist")
hdn.Draw("hist same")

hup.GetYaxis().SetTitle(options.title + " Variation")
hup.GetYaxis().SetTitleSize(15)
hup.GetYaxis().SetLabelSize(15)
hup.SetTitle(options.title + " Variation Unfolded")
hup.GetXaxis().SetTitle("Jet Mass (GeV)")

hup.SetMinimum(0.0)
hup.SetMaximum(2.0)
hdn.Draw("hist same")
if options.hist == "h_msd" :
    c.SaveAs(options.sys+"UnfoldedSD.png")
else:
    c.SaveAs(options.sys+"Unfolded.png")
c.Update()

