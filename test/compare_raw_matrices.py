import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")
#ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(000000)
#ROOT.gROOT.Macro("rootlogon.C")

ROOT.gStyle.SetLabelFont(43, "XYZ")
ROOT.gStyle.SetLabelSize(24, "XYZ")
ROOT.gStyle.SetTitleFont(43, "XYZ")
ROOT.gStyle.SetTitleSize(28, "XYZ")
ROOT.gStyle.SetTitleOffset(2.0, "Y")
ROOT.gStyle.SetTitleOffset(4.0, "X")


from ROOT import gRandom, TH1, cout, TH2, TLegend, TFile
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import TCanvas
from ROOT import RooUnfoldSvd
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--syst', action ='store', type = 'string',
                 default ='jec',
                 dest='syst',
                 help='Systematic to vary')
       
(options, args) = parser.parse_args()


def setupPads(canv, pads):
    canv.cd()
    pad1 = ROOT.TPad('pad' + canv.GetName() + '1', 'pad' + canv.GetName() + '1', 0., 0.3, 1.0, 1.0)
    pad1.SetBottomMargin(0.022)
    pad2 = ROOT.TPad('pad' + canv.GetName() + '2', 'pad' + canv.GetName() + '2', 0., 0.0, 1.0, 0.3)
    pad2.SetTopMargin(0.05)
    pad1.SetLeftMargin(0.20)
    pad2.SetLeftMargin(0.20)
    pad2.SetBottomMargin(0.5)
    pad1.Draw()
    pad2.Draw()
    pads.append( [pad1,pad2] )
    return [pad1, pad2]
 

ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)

mcfile = TFile('responses_rejec_tightgen_otherway_qcdmc_2dplots.root')
datafile = TFile('jetht_weighted_dataplots_otherway_rejec.root')


data = datafile.Get('PFJet_pt_m_AK8SD')
nomM = mcfile.Get('2d_response_softdrop')
jecupM = mcfile.Get('2d_response_softdrop_' + options.syst + 'up')
jecdnM = mcfile.Get('2d_response_softdrop_' + options.syst + 'dn')

nomU = RooUnfoldBayes(nomM, data, 4)
jecupU = RooUnfoldBayes(jecupM, data, 4)
jecdnU = RooUnfoldBayes(jecdnM, data, 4)


hnom = nomU.Hreco()
hjecup = jecupU.Hreco()
hjecdn = jecdnU.Hreco()

for hist in [hnom, hjecup, hjecdn] :
    hist.UseCurrentStyle()

projsnom = []
projsjecup = []
projsjecdn = []
normprojsnom = []
normprojsjecup = []
normprojsjecdn = []
canvs = []
canvsnorm = []
stacks = []
stacksnorm = []
pads = []
ratios = []
for ipt in xrange(1,hnom.GetNbinsY()):
    projsnom.append( hnom.ProjectionX("hnom_" + str(ipt), ipt,ipt) )
    projsjecup.append( hjecup.ProjectionX("hjecup_" + str(ipt), ipt,ipt) )
    projsjecdn.append( hjecdn.ProjectionX("hjecdn_" + str(ipt), ipt,ipt) )
    projsnom[ipt-1].SetLineStyle(1)
    projsnom[ipt-1].SetLineWidth(2)
    projsjecup[ipt-1].SetLineStyle(2)
    projsjecdn[ipt-1].SetLineStyle(2)
    for iproj in [ projsnom[ipt-1], projsjecup[ipt-1], projsjecdn[ipt-1] ] :
        iproj.GetXaxis().SetRangeUser(1,500)
        for im in xrange(1,iproj.GetNbinsX() ) : 
            if  iproj.GetBinContent(im) > 0.0 :
                iproj.SetBinContent(im, iproj.GetBinContent(im)/iproj.GetBinWidth(im) )


    normprojsnom.append( projsnom[ipt-1].Clone("hnormnom_" + str(ipt) ) )
    normprojsjecup.append( projsjecup[ipt-1].Clone("hnormjecup_" + str(ipt) ) )
    normprojsjecdn.append( projsjecdn[ipt-1].Clone("hnormjecdn_" + str(ipt) ) )
    normprojsnom[ipt-1].Scale( 1.0 / normprojsnom[ipt-1].Integral() )
    normprojsjecup[ipt-1].Scale( 1.0 / normprojsjecup[ipt-1].Integral() )
    normprojsjecdn[ipt-1].Scale( 1.0 / normprojsjecdn[ipt-1].Integral() )

    stack = ROOT.THStack( "h_" + str(ipt), ";;Number")
    stack.Add( projsnom[ipt-1] )
    stack.Add( projsjecup[ipt-1] )
    stack.Add( projsjecdn[ipt-1] )    
    cpt = ROOT.TCanvas( "cpt" + str(ipt), "cpt" + str(ipt), 800, 800 )
    p1,p2 = setupPads(cpt, pads)
    p1.cd()
    p1.SetLogx()
    stack.Draw("nostack hist")
    stacks.append(stack)
    p1.Update()
    p2.cd()
    p2.SetLogx()
    ratioup = projsjecup[ipt-1].Clone("ratioup_" + str(ipt))
    ratioup.Divide(projsnom[ipt-1])
    ratiodn = projsjecdn[ipt-1].Clone("ratiodn_" + str(ipt))
    ratiodn.Divide(projsnom[ipt-1])
    ratioup.Draw("hist")
    ratiodn.Draw("hist same")
    ratioup.SetTitle(';Groomed jet mass (GeV);Ratio')
    ratioup.GetYaxis().SetNdivisions(2,4,0,False)
    ratioup.GetYaxis().SetRangeUser(0.9,1.1)
    ratioup.GetXaxis().SetNoExponent()
    ratios.append( [ratioup,ratiodn])
    cpt.Update()
    cpt.Print("compare_" + options.syst + "_" + str(ipt) + ".png")
    cpt.Print("compare_" + options.syst + "_" + str(ipt) + ".pdf")
                        
    stacknorm = ROOT.THStack( "hnorm_" + str(ipt), ";;Fraction")
    stacknorm.Add( normprojsnom[ipt-1] )
    stacknorm.Add( normprojsjecup[ipt-1] )
    stacknorm.Add( normprojsjecdn[ipt-1] )    
    cptnorm = ROOT.TCanvas( "cptnorm" + str(ipt), "cptnorm" + str(ipt), 800, 800 )
    pn1,pn2 = setupPads(cptnorm, pads)
    pn1.cd()
    pn1.SetLogx()
    stacknorm.Draw("nostack hist")
    pn1.Update()
    pn2.cd()
    pn2.SetLogx()
    normratioup = normprojsjecup[ipt-1].Clone("normratioup_" + str(ipt))
    normratioup.Divide(normprojsnom[ipt-1])
    normratiodn = normprojsjecdn[ipt-1].Clone("ratiodn_" + str(ipt))
    normratiodn.Divide(normprojsnom[ipt-1])
    normratioup.Draw("hist")
    normratiodn.Draw("hist same")
    normratioup.SetTitle(';Groomed jet mass (GeV);Ratio')
    normratioup.GetYaxis().SetNdivisions(2,4,0,False)
    normratioup.GetYaxis().SetRangeUser(0.99,1.01)
    normratioup.GetXaxis().SetNoExponent()
    ratios.append( [normratioup,normratiodn])
    pn2.Update()
    cptnorm.Update()
    cptnorm.Print("compare_" + options.syst + "_norm_" + str(ipt) + ".png")
    cptnorm.Print("compare_" + options.syst + "_norm_" + str(ipt) + ".pdf")
    stacksnorm.append(stacknorm)
    canvsnorm.append(cptnorm)
    


hjecup.Divide( hnom )

hjecup.SetTitle("Unfolded " + options.syst.upper() + " Up / Unfolded Nominal;Groomed jet mass (GeV);Jet p_{T} (GeV)")

c = ROOT.TCanvas("c","c", 800, 800)
hjecup.GetXaxis().SetTitleOffset(1.0)
hjecup.GetYaxis().SetTitleOffset(1.0)
hjecup.Draw("colz")
hjecup.GetXaxis().SetRangeUser(0,600)
hjecup.GetYaxis().SetRangeUser(200,1000)
hjecup.SetMaximum(1.1)
hjecup.SetMinimum(0.9)
c.SetLogx()

c.Print("absolute_unfolded_ratio_" + options.syst + ".png", "png")
c.Print("absolute_unfolded_ratio_" + options.syst + ".pdf", "pdf")
