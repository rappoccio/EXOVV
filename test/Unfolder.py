#! /usr/bin/env python

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from HistDriver import *
import math
import pickle

class RooUnfoldUnfolder:
    def __init__(self, inputs = "2DData", useSoftDrop=False, normalizeEachPtBin=False, normalizeUnity=True, histDriver=None, lumi=2.1):

        if histDriver != None :
            self.histDriver_ = histDriver
        else :
            self.histDriver_ = HistDriver(lumi=lumi)
        self.inputs = inputs
        self.useSoftDrop = useSoftDrop                            # Use soft drop
        self.normalizeEachPtBin = normalizeEachPtBin              # Normalize each pt bin separately
        self.normalizeUnity = normalizeUnity                      # Normalize total histogram to unity (via Integral("width"))
        self.expsysnames = [ '_jer', '_jec', '_jmr', '_pu' ]      # Experimental uncertainties
        self.thsysnames = ['_pdf', '_ps']                         # Theory uncertainties
        self.sysnames = self.expsysnames + self.thsysnames        # All uncertainties
        self.files = dict()                                       # Store files
        self.responses = dict()                                   # RooUnfoldResponse objects
        self.nom = None                                           # TH2D representing central value with stat+sys uncertainties
        self.nomStat = None                                       # TH2D representing central value with ONLY stat uncertainties
        self.uncertainties = dict(                                # TH2D's representing uncertainties
            zip(self.sysnames, [None] * len(self.sysnames) )
            )

        if not self.useSoftDrop: 
            postfix1 = ''
            postfix2 = ''            
        else: 
            postfix1 = "_softdrop"
            postfix2 = "SD"
        # Nominal value :
        fnom = ROOT.TFile(self.inputs + '.root')
        self.files['nom'] = fnom
        self.responses['nom'] = fnom.Get('2d_response' + postfix1 )
        self.nom = self.responses['nom'].Hreco()


        self.nom.UseCurrentStyle()

        #ROOT.gStyle.SetTitleSize(0.04, "XYZ")

        if not self.useSoftDrop: 
            self.nom.SetTitle(";Ungroomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")
        else :
            self.nom.SetTitle(";Groomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")

        normalizeHist( self.nom, normalizeUnity = self.normalizeUnity, normalizeEachPtBin = self.normalizeEachPtBin )

        
        # Each experimental uncertainty has an "up" and a "down" variation, so
        # the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
        for sys in self.expsysnames :
            sysup = sys + 'up'
            sysdn = sys + 'dn'
            fup = ROOT.TFile( self.inputs + sysup + '.root')
            fdn = ROOT.TFile( self.inputs + sysdn + '.root')
            resup = fup.Get('2d_response' + postfix1 + sysup)
            resdn = fdn.Get('2d_response' + postfix1 + sysdn)

            self.files[sysup] = fup
            self.files[sysdn] = fdn
            self.responses[sysup] = resup
            self.responses[sysdn] = resdn

            histup = self.responses[sysup].Hreco()
            histdn = self.responses[sysdn].Hreco()
            normalizeHist( histup, normalizeUnity = self.normalizeUnity, normalizeEachPtBin = self.normalizeEachPtBin  )
            normalizeHist( histdn, normalizeUnity = self.normalizeUnity, normalizeEachPtBin = self.normalizeEachPtBin  )

            # Take difference to nominal... next step takes abs() so ignore relative sign
            histup.Add( self.nom, -1.0 )
            histdn.Add( self.nom, -1.0 )

            self.uncertainties[sys] = self.nom.Clone( self.nom.GetName() + "_" + sys )
            setToAverage( self.uncertainties[sys], histup, histdn )
            self.uncertainties[sys].Divide( self.nom )
            

        # Next : PDF and PS uncertainties
        # For the NNPDF uncertainties ("pdfup" and "pdfdn") these are
        # double sided, so (absolute) uncertainty is (up-down)/2 again (factor of 2 will come later). 
        # For the CTEQ and MSTW, the uncertainty is |sys-nom|.
        fpdf = ROOT.TFile("unfoldedpdf.root")
        self.files['_pdf'] =  fpdf 

        
        mpdfup = fpdf.Get( '2d_response' + postfix1 + '_pdfup' )
        mpdfdn  = fpdf.Get( '2d_response' + postfix1 + '_pdfdn' )
        mmstw = fpdf.Get( '2d_response' + postfix1 + '_mstw' )
        mcteq = fpdf.Get( '2d_response' + postfix1 + '_cteq' )
        
        self.responses['_pdfup'] =  mpdfup 
        self.responses['_pdfdn'] =  mpdfdn 
        self.responses['_mstw'] =  mmstw 
        self.responses['_cteq'] =  mcteq
        hpdfup = mpdfup.Hreco()
        hpdfdn = mpdfdn.Hreco()
        hmstw = mmstw.Hreco()
        hcteq = mcteq.Hreco()
        for hist in [ hpdfup, hpdfdn, hmstw, hcteq] :
            normalizeHist( hist, normalizeUnity = self.normalizeUnity, normalizeEachPtBin = self.normalizeEachPtBin  )

        
        hpdfup.Add( self.nom, -1.0 )
        hpdfdn.Add( self.nom, -1.0 )
            
        self.uncertainties['_pdf'] = hpdfup.Clone( self.nom.GetName() + "_pdf")
        setToAverage( self.uncertainties['_pdf'], hpdfup, hpdfup )    
        self.uncertainties['_pdf'].Divide( self.nom )

        #### FIXME FIXME FIXME FIXME : the uncertainties for CTEQ and MSTW still need to be included!!
        #### FIXME FIXME FIXME FIXME : the PDF up and down should be 0.5*(up-dn), not (up-dn)

        # Parton shower: Half the difference between pythia and herwig
        self.files['_ps'] = ROOT.TFile("PS_hists.root")
        self.responses['_ps'] = self.files['_ps'].Get( 'unfold_ps_data' + postfix1 + '_herwig' )
        hps = self.responses['_ps'].Hreco()
        normalizeHist( hps, normalizeUnity = self.normalizeUnity, normalizeEachPtBin = self.normalizeEachPtBin  )
        self.uncertainties['_ps'] = self.nom.Clone( self.nom.GetName() + "_ps" )
        self.uncertainties['_ps'].Add( hps, -0.5 )
        self.uncertainties['_ps'].Divide( self.nom )


        RMS_vals = pickle.load(open("ungroomeddataJackKnifeRMS.p", "rb"))         ########
        RMS_vals_softdrop = pickle.load(open("softdropdataJackKnifeRMS.p", "rb")) ########
        if not self.useSoftDrop :
            mcStatVals = RMS_vals
        else :
            mcStatVals = RMS_vals_softdrop

        
        # Set up the stat uncertainties
        self.nomStat = self.nom.Clone( self.nom.GetName() + "_stat" )
        self.mcStat = self.nom.Clone( self.nom.GetName() + "_mcstat" )        
        
        # Now sum all of the uncertainties in quadrature
        for ix in xrange(1,self.nom.GetNbinsX()+1):
            for iy in xrange(1,self.nom.GetNbinsY()+1):
                val = self.nom.GetBinContent(ix,iy)
                if val > 0.0 : 
                    mcStatVal = mcStatVals[iy-1][ix-1] / val / self.nom.GetYaxis().GetBinWidth(iy) / self.nom.GetXaxis().GetBinWidth(ix)
                else :
                    mcStatVal = 0.0
                    
                self.mcStat.SetBinContent( ix, iy, mcStatVal )
                                
                if abs(val) > 0.0 : 
                    err2 = self.nom.GetBinError(ix,iy) / val 
                    err2 = err2**2# + mcStatVal**2
                    #print 'ix,iy=', ix, ', ', iy
                    for isyst,isystval in self.uncertainties.iteritems() :
                        #print '%6s=%6.2e' % ( isyst, abs(isystval.GetBinContent(ix,iy)) ),
                        err2 += (isystval.GetBinContent(ix,iy))**2
                    #print ' totunc=%6.2e' % ( math.sqrt(err2) ),
                    self.nom.SetBinError( ix, iy, math.sqrt(err2) * val )
                    #print ' tot=%6.2e/%6.2e' % ( self.nom.GetBinError(ix,iy) , val )
                    

    def draw2D(self, postfix):
        c = ROOT.TCanvas("c" + postfix, "c" + postfix)
        c.SetLogz()
        
        self.histDriver_.canvs_.append(c)
        self.nom.Draw("colz")
        self.nom.SetMinimum(1e-12)
        self.nom.SetMaximum(1e-5)
        self.nom.GetYaxis().SetRangeUser(200, 1300)
        self.nom.GetXaxis().SetRangeUser(0, 800)
        self.histDriver_.stampCMS( c, "CMS Preliminary")
        
    def drawUncertainties(self, postfix ):
        c = ROOT.TCanvas("cunc" + postfix, "cunc" + postfix)
        c.SetLogx()
        
        self.histDriver_.canvs_.append(c)
        
        stack = ROOT.THStack( self.nom.GetName() + "_uncstack", self.nom.GetTitle() )
        iunc = 1
        for unc in self.uncertainties.itervalues() :
            setStyles( unc, lineStyle= iunc, lineColor=iunc )
            iunc += 1
            stack.Add( unc )
        stack.Draw("nostack hist")
        self.histDriver_.stampCMS( c, "CMS Preliminary")
        self.histDriver_.stacks_.append(stack)
        self.histDriver_.canvs_.append(c)
