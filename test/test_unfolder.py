import ROOT
from Unfolder import *

ROOT.gROOT.Macro("rootlogon.C")
ROOT.gROOT.SetBatch()

lumi = 2.3e3
driver = HistDriver(lumi=lumi)

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetTitleOffset(1.0, "Y");
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gStyle.SetTitleOffset(1.0, "X")
ROOT.gStyle.SetTitleOffset(0.8, "Y")
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(22,"XYZ")



# First absolute cross section
uu = RooUnfoldUnfolder(useSoftDrop=False,
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=False, scalePtBins=False, lumi=lumi) 
uu.plotFullXSProjections( hists=[uu.nom, uu.nomStat,uu.pythiaHist,uu.herwigHist],
                              styleNames=['nom','nomStat','pythia','herwig'],
                              postfix="absolute" )

ug = RooUnfoldUnfolder(useSoftDrop=True,
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=False, scalePtBins=False, lumi=lumi) 

ug.plotFullXSProjections( hists=[ug.nom, ug.nomStat,ug.pythiaHist,ug.herwigHist],
                              styleNames=['nom','nomStat','pythia','herwig'],
                              postfix="absolute_softdrop" )


# Plot xs wrt pt only
uu.plotPtDist( hists=[uu.nom, uu.nomStat, uu.pythiaHist, uu.herwigHist],
                   styleNames=['nom','nomStat','pythia','herwig'],
                   filename = "pt_xs", title=";Ungroomed jet p_{T} (GeV);#frac{d#sigma}{dp_{T}} (pb/GeV)" )



# Then plot uncertainties
uumc = RooUnfoldUnfolder(useSoftDrop=False,inputs='2DClosure',
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=False, scalePtBins=False, lumi=lumi)
ugmc = RooUnfoldUnfolder(useSoftDrop=True,inputs='2DClosure',
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=False, scalePtBins=False, lumi=lumi) 

uumc.plotFullUncs( hists=uu.uncertainties, postfix="ungroomed_absolute")
ugmc.plotFullUncs( hists=ug.uncertainties, postfix="softdrop_absolute")




# Now normalized cross section
uu_norm = RooUnfoldUnfolder(useSoftDrop=False,
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=True, scalePtBins=True, lumi=lumi)

uu_norm.plotFullXSProjections( hists=[uu_norm.nom, uu_norm.nomStat,uu_norm.pythiaHist,uu_norm.herwigHist],
                              styleNames=['nom','nomStat','pythia','herwig'],
                              postfix="normalized" )

ug_norm = RooUnfoldUnfolder(useSoftDrop=True,
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=True, scalePtBins=True, lumi=lumi)

ug_norm.plotFullXSProjections( hists=[ug_norm.nom, ug_norm.nomStat,ug_norm.pythiaHist,ug_norm.herwigHist],
                              styleNames=['nom','nomStat','pythia','herwig'],
                              postfix="normalized_softdrop" )


# Plot 2d cross sections
uu_norm.draw2D("absolute_ungroomed")                       
ug_norm.draw2D("absolute_groomed") 
uu_norm.draw2D("normalized_ungroomed")
ug_norm.draw2D("normalized_groomed")

# Then plot uncertainties


uumc_norm = RooUnfoldUnfolder(useSoftDrop=False, inputs="2DClosure",
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=True, scalePtBins=True, lumi=lumi)

ugmc_norm = RooUnfoldUnfolder(useSoftDrop=True, inputs="2DClosure",
                       pythiaInputs="responses_rejec_fixjmr_otherway_qcdmc_2dplots.root",
                       herwigInputs="qcdmc_herwig_otherway_rejec_fixjmr_2dplots.root",
                       powhegInputs="CMS_SMP_16_010.root",
                       normalizeUnity=True, scalePtBins=True, lumi=lumi)

uumc_norm.plotFullUncs( hists=uumc_norm.uncertainties, postfix="ungroomed")
ugmc_norm.plotFullUncs( hists=ugmc_norm.uncertainties, postfix="softdrop")
