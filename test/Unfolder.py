#! /usr/bin/env python

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from HistDriver import *
import math
import pickle

class RooUnfoldUnfolder:
    def __init__(self, inputs = "2DData",
                     pythiaInputs=None, herwigInputs=None, powhegInputs=None,
                     theoryInputs1=None, theoryInputs2=None,
                     useSoftDrop=False, normalizeUnity=True, scalePtBins=False, useUncSrcs=True,
                     lumi=2.3e3, dlumi=0.027, postfix=''):

        self.maxunc = 0.6                                            # Zero bins with frac. unc. larger than maxunc
        self.histDriver_ = HistDriver(lumi=lumi, dlumi=dlumi)        # Creates and stores histograms so they don't go out of scope
        self.inputs = inputs                                         # String for inputs to use
        self.pythiaInputs=pythiaInputs                               # String for pythia filename
        self.herwigInputs=herwigInputs                               # String for herwig filename
        self.powhegInputs=powhegInputs                               # String for powheg filename
        self.theoryInputs1=theoryInputs1                             # String for theory1 filename
        self.theoryInputs2=theoryInputs2                             # String for theory2 filename
        self.pythiaHist = None                                       # Pythia histogram(s) 
        self.herwigHist = None                                       # Herwig histogram(s)
        self.powhegHist = None                                       # Powheg histogram(s)
        self.pythiaFile = None                                       # Pythia file
        self.herwigFile = None                                       # Herwig file 
        self.powhegFile = None                                       # Powheg file
        self.theoryfile1= None                                       # Theory 1 file
        self.theoryfile2= None                                       # Theory 2 file
        self.theorylist1 = []
        self.theorylist2 = []
        self.theorygraphs1 = []
        self.theorygraphs2 = []
        self.theorylist = [ self.theorylist1, self.theorylist2]
        self.theorygraphs = [self.theorygraphs1, self.theorygraphs2]
        self.useSoftDrop = useSoftDrop                               # Use soft drop
        self.normalizeUnity = normalizeUnity                         # Normalize total histogram to unity (via Integral("width"))
        self.scalePtBins = scalePtBins                               # Scale each pt bin separately
        self.useUncSrcs = useUncSrcs                                 # Use JEC uncertainty sources? 
        self.expsysnames = [ '_jec', '_jer', '_jmr', '_jms', '_pu' ] # Experimental uncertainties EXCEPT for jec
        self.thsysnames = ['_pdf', '_ps', '_mcStat']                 # Theory uncertainties
        self.flatsysnames = ['_lum']                                 # Flat uncertainties
        if not self.normalizeUnity:
            self.allsysts = self.expsysnames + self.thsysnames + self.flatsysnames 
            self.sysnames = self.allsysts + ['_totunc']              # All uncertainties
        else :
            self.allsysts = self.expsysnames + self.thsysnames
            self.sysnames = self.allsysts + ['_totunc']              # All uncertainties
        self.responses = dict()                                      # RooUnfoldResponse objects
        self.nom = None                                              # TH2D representing central value with stat+sys uncertainties
        self.jernom = None                                           # TH2D representing central value in JER
        self.jmrnom = None                                           # TH2D representing central value in JMR
        self.nomStat = None                                          # TH2D representing central value with ONLY stat uncertainties
        self.nomNorm = None                                          # Normalization of the nominal. If we don't normalize to unity, we normalize Herwig to this. 
        self.postfix = postfix
        self.files = {}
        self.extraHists = []
        
        # All jet energy uncertainty sources
        self.allJecUncSrcNames = [
            "AbsoluteStat","AbsoluteScale","AbsoluteFlavMap","AbsoluteMPFBias",
            "Fragmentation",
            "SinglePionECAL","SinglePionHCAL",
            "FlavorQCD",
            "TimeEta","TimePt",
            "RelativeJEREC1","RelativeJEREC2","RelativeJERHF","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeFSR","RelativeStatFSR","RelativeStatEC","RelativeStatHF",
            "PileUpDataMC","PileUpPtRef","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpMuZero","PileUpEnvelope",
            "SubTotalPileUp","SubTotalRelative","SubTotalPt","SubTotalScale","SubTotalAbsolute","SubTotalMC",
            "Total","TotalNoFlavor","TotalNoTime","TotalNoFlavorNoTime",
            "FlavorZJet","FlavorPhotonJet","FlavorPureGluon","FlavorPureQuark","FlavorPureCharm","FlavorPureBottom",
            "TimeRunA","TimeRunB","TimeRunC","TimeRunD",
            "CorrelationGroupMPFInSitu","CorrelationGroupIntercalibration","CorrelationGroupbJES","CorrelationGroupFlavor","CorrelationGroupUncorrelated",
            ]
        self.allJecUncSrcs = dict(
            zip( self.allJecUncSrcNames, [i for i in xrange( len(self.allJecUncSrcNames) )] )
            )

        # Jet energy uncertainty sources to use
        self.jecUncSrcs = [
            "AbsoluteStat","AbsoluteScale","AbsoluteFlavMap","AbsoluteMPFBias",
            "Fragmentation",
            "SinglePionECAL","SinglePionHCAL",
            "FlavorQCD",   # Would double count pythia-vs-herwig
            "TimeEta","TimePt",
            "RelativeJEREC1","RelativeJEREC2","RelativeJERHF","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeFSR","RelativeStatFSR","RelativeStatEC","RelativeStatHF",
            "PileUpDataMC","PileUpPtRef","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpMuZero","PileUpEnvelope",
            ]
        
            
        self.uncertainties = dict(                                   # TH2D's representing uncertainties
            zip(self.sysnames, [None] * len(self.sysnames) )
            )

        if not self.normalizeUnity:
            unctitles = ['JEC', 'JER', 'JMR', 'JMS', 'PU', 'PDF', 'Physics model', 'Stat. unc.', 'Lumi', 'Total']
        else :
            unctitles = ['JEC', 'JER', 'JMR', 'JMS', 'PU', 'PDF', 'Physics model', 'Stat. unc.', 'Total']
        self.uncertaintyNames = dict( zip( self.sysnames, unctitles ) )

        self.theorydict = dict( zip(['theory1', 'theory2'], [i for i in xrange(2)]  ) )
        
        
        self.ptBinNames = [    '200 < p_{T} < 260 GeV',
                               '260 < p_{T} < 350 GeV',
                               '350 < p_{T} < 460 GeV',
                               '460 < p_{T} < 550 GeV',
                               '550 < p_{T} < 650 GeV',
                               '650 < p_{T} < 760 GeV',
                               '760 < p_{T} < 900 GeV',
                               '900 < p_{T} < 1000 GeV',
                               '1000 < p_{T} < 1100 GeV',
                               '1100 < p_{T} < 1200 GeV',
                               '1200 < p_{T} < 1300 GeV',
                               'p_{T} > 1300 GeV'          ]
        if self.useSoftDrop == False : 
            self.xAxisRanges = [
                [20,1000],    #'200 < p_{T} < 260 GeV',    
                [20,1000],    #'260 < p_{T} < 350 GeV',    
                [20,1000],    #'350 < p_{T} < 460 GeV',    
                [20,1000],    #'460 < p_{T} < 550 GeV',    
                [20,1000],    #'550 < p_{T} < 650 GeV',    
                [20,1000],    #'650 < p_{T} < 760 GeV',    
                [40,1000],    #'760 < p_{T} < 900 GeV',    
                [40,1000],    #'900 < p_{T} < 1000 GeV',   
                [40,1000],    #'1000 < p_{T} < 1100 GeV',  
                [40,1000],    #'1100 < p_{T} < 1200 GeV',  
                [40,1000],    #'1200 < p_{T} < 1300 GeV',  
                [40,1000],    #'p_{T} > 1300 GeV'          
                [40,1000],    #
                [40,1000],    #
                ]
        else :
            self.xAxisRanges = [
                [10,1000],    #'200 < p_{T} < 260 GeV',    
                [10,1000],    #'260 < p_{T} < 350 GeV',    
                [10,1000],    #'350 < p_{T} < 460 GeV',    
                [10,1000],    #'460 < p_{T} < 550 GeV',    
                [10,1000],    #'550 < p_{T} < 650 GeV',    
                [10,1000],    #'650 < p_{T} < 760 GeV',    
                [10,1000],    #'760 < p_{T} < 900 GeV',    
                [10,1000],    #'900 < p_{T} < 1000 GeV',   
                [10,1000],    #'1000 < p_{T} < 1100 GeV',  
                [10,1000],    #'1100 < p_{T} < 1200 GeV',  
                [10,1000],    #'1200 < p_{T} < 1300 GeV',  
                [10,1000],    #'p_{T} > 1300 GeV'          
                [10,1000],    #
                [10,1000],    #
                ]

        if not self.useSoftDrop: 
            self.postfix1 = ''
            self.postfix2 = ''
            self.subscript= '_{u}'
        else: 
            self.postfix1 = "_softdrop"
            self.postfix2 = "SD"
            self.subscript= '_{g}'

        self.readExp()

        if self.pythiaInputs != None :
            self.readPythia()
        if self.herwigInputs != None :
            self.readHerwig()
        if self.powhegInputs != None :
            self.readPowheg()
        if self.theoryInputs1 != None:
            self.readTheory1()
        if self.theoryInputs2 != None:
            self.readTheory2()            
            
    def readExp(self) :
        # Nominal value :
        fnom = ROOT.TFile(self.inputs + '_expunc.root')
        self.files['nom'] = fnom
        self.responses['nom'] = fnom.Get('2d_response' + self.postfix1 + '_nomnom' )
        self.responses['jernom'] = fnom.Get('2d_response' + self.postfix1 + '_jernom' )
        self.responses['jmrnom'] = fnom.Get('2d_response' + self.postfix1 + '_jmrnom' )
        self.responses['unsmeared'] = fnom.Get('2d_response' + self.postfix1 )

        self.nom = self.responses['nom'].Hreco()
        self.raw = self.nom.Clone(self.nom.GetName() + "_unscaled")
        self.jernom = self.responses['jernom'].Hreco()
        self.jmrnom = self.responses['jmrnom'].Hreco()

        self.unsmeared = self.responses['unsmeared'].Hreco()
        self.unsmearedForPS = self.unsmeared.Clone( self.nom.GetName() + "_normalizingPS")
        self.rawForStat = self.raw.Clone( self.raw.GetName() + "_forstats")
        self.histDriver_.normalizeHist( self.unsmearedForPS, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True)
        self.histDriver_.normalizeHist( self.rawForStat, normalizeUnity = self.normalizeUnity, divideByBinWidths=True, scalePtBins = True)
        #self.histDriver_.normalizeHist( self.unsmeared, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True)
        
        self.nom.UseCurrentStyle()

        #ROOT.gStyle.SetTitleSize(0.04, "XYZ")
        ROOT.TGaxis.SetExponentOffset(-0.06, 0.00, "y")

        if not self.useSoftDrop: 
            self.nom.SetTitle(";Ungroomed jet mass m_{u} (GeV);Ungroomed jet p_{T} (GeV)")
        else :
            self.nom.SetTitle(";Groomed jet mass m_{g} (GeV);Ungroomed jet p_{T} (GeV)")

        self.histDriver_.normalizeHist( self.nom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.jernom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.jmrnom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.unsmeared, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )

        self.nomNorm = self.nom.Integral("width")
        
        # Each experimental uncertainty has an "up" and a "down" variation, so
        # the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
        for sys in self.expsysnames :
            inom = self.jernom
            if sys == '_jmr' :
                inom = self.jmrnom            
            histup, histdn = self.getUpAndDown( fnom, sys )
            self.uncertainties[sys] = inom.Clone( inom.GetName() + "_" + sys )                
            self.getRelative( inom, self.uncertainties[sys], histup, histdn )
                
        # If desired, replace the JEC with the sources:
        if self.useUncSrcs :
            for ix in xrange(1,self.nom.GetNbinsX()+1):
                for iy in xrange(1,self.nom.GetNbinsY()+1):
                    self.uncertainties['_jec'].SetBinContent(ix,iy, 0.0)
                    
            for jecUncSrc in self.jecUncSrcs:
                index = self.allJecUncSrcs[jecUncSrc]
                sys = '_jecsrc' + str(index)
                histup, histdn = self.getUpAndDown( fnom, sys )
                havg = self.unsmeared.Clone( self.nom.GetName() + "_" + sys )
                self.getRelative( self.unsmeared, havg, histup, histdn)
                for ix in xrange(1,self.nom.GetNbinsX()+1):
                    for iy in xrange(1,self.nom.GetNbinsY()+1):
                        val1 = self.uncertainties['_jec'].GetBinContent(ix,iy)
                        val2 = havg.GetBinContent(ix,iy)
                        val = val1**1 + val2**2          # NOTE: KEEPING SUM OF SQUARES HERE, TAKE SQRT LATER
                        self.uncertainties['_jec'].SetBinContent(ix,iy, val)
            for ix in xrange(1,self.nom.GetNbinsX()+1):
                for iy in xrange(1,self.nom.GetNbinsY()+1):
                    val = self.uncertainties['_jec'].GetBinContent(ix,iy)
                    self.uncertainties['_jec'].SetBinContent(ix,iy, math.sqrt(val) )
                
        # Now get the luminosity uncertainty
        if not self.normalizeUnity : 
            self.uncertainties['_lum'] = self.nom.Clone( self.nom.GetName() + "_lum" )
            for ix in xrange(0, self.unsmeared.GetXaxis().FindBin( self.nom.GetXaxis().GetXmax() ) ):
                for iy in xrange(0, self.unsmeared.GetNbinsY()+2):
                    if self.unsmeared.GetBinContent(ix,iy) > 0.0 :
                        if self.normalizeUnity == False : 
                            self.uncertainties['_lum'].SetBinContent( ix, iy, math.sqrt( self.histDriver_.dlumi2_ )  )
                        else :
                            self.uncertainties['_lum'].SetBinContent( ix, iy, 0.0 )

        # Next : PDF uncertainties from PDF4LHC15 meta-pdf
        fpdf = ROOT.TFile("unfoldedpdf_pdf4lhc15.root")
        self.files['pdf'] = fpdf
        pdfpostfix = ''
        if "Data" in self.inputs :
            pdfpostfix = '_data'
        mpdfup = fpdf.Get( 'unfold' + pdfpostfix + '_pdfup' + self.postfix1 )
        mpdfdn = fpdf.Get( 'unfold' + pdfpostfix + '_pdfdn' + self.postfix1 )
        mpdfnom = fpdf.Get( 'unfold' + pdfpostfix + '_pdfnom' + self.postfix1 )
        
        
        self.responses['_pdfup'] =  mpdfup 
        self.responses['_pdfdn'] =  mpdfdn
        self.responses['_pdfnom'] =  mpdfnom
        hpdfup = mpdfup.Hreco()
        hpdfdn = mpdfdn.Hreco()
        hpdfnom = mpdfnom.Hreco()
        self.histDriver_.normalizeHist( hpdfnom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        for hist in [ hpdfup, hpdfdn] :
            self.histDriver_.normalizeHist( hist, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
            hist.Add( hpdfnom, -1.0 )
            ensureAbs( hist )
            hist.Divide( hpdfnom )
        self.uncertainties['_pdf'] = self.raw.Clone( self.nom.GetName() + "_pdf")
        setToAverage( self.uncertainties['_pdf'], hpdfup, hpdfdn)        
        

        # Parton shower: Half the difference between pythia and herwig
        # However : There is a different pt spectrum, so need to correct per pt bin to
        # just get the mass differences
        psfile = ROOT.TFile("PS_hists.root")
        self.files['ps'] = psfile
        if "Data" in self.inputs : 
            self.responses['_ps'] = psfile.Get( 'unfold_ps_data' + self.postfix1 + '_herwig' )
        else :
            self.responses['_ps'] = psfile.Get( 'unfold_ps' + self.postfix1 + '_herwig' )
        hps = self.responses['_ps'].Hreco()
        self.histDriver_.normalizeHist( hps, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True  )      
        # This holds [ (dsigma/dm)_pythia - (dsigma/dm)_herwig ]        
        hps.Add( self.unsmearedForPS, -1.0 )
        ensureAbs( hps )
        hps.Scale(0.5)        
        hps.Divide(self.unsmearedForPS)
        hps.Scale(2.0)
        # Now set up the PS uncertainties themselves:
        self.uncertainties['_ps'] = hps.Clone( self.nom.GetName() + "_ps" )


        # Now for the MC stat uncertainty
        picklePostfix = ""
        if "Data" in self.inputs :
            picklePostfix = "data"
        if self.normalizeUnity : 
            RMS_vals = pickle.load(open("ungroomed" + picklePostfix +"JackKnifeRMS.p", "rb"))         ########
            RMS_vals_softdrop = pickle.load(open("softdrop" + picklePostfix +"JackKnifeRMS.p", "rb")) ########
        else :
            RMS_vals = pickle.load(open("ungroomed" + picklePostfix +"JackKnifeRMS_absolute.p", "rb"))         ########
            RMS_vals_softdrop = pickle.load(open("softdrop" + picklePostfix +"JackKnifeRMS_absolute.p", "rb")) ########

        if not self.useSoftDrop :
            mcStatVals = RMS_vals
        else :
            mcStatVals = RMS_vals_softdrop

        
        # Set up the stat uncertainties and fill styles
        self.nomStat = self.nom.Clone( self.nom.GetName() + "_stat" )
        self.mcStat = self.nom.Clone( self.nom.GetName() + "_mcstat" )
        setStyles( self.nom, fillStyle=1001, fillColor=ROOT.kGray, markerStyle=20)
        setStyles( self.nomStat, fillStyle=1001, fillColor=ROOT.kGray+2)
        for ix in xrange(1,self.raw.GetNbinsX()+1):
            for iy in xrange(1,self.raw.GetNbinsY()):
                val = self.raw.GetBinContent(ix,iy)
                staterr = self.raw.GetBinError(ix,iy)
                biny = self.raw.GetYaxis().GetBinWidth(iy)
                binx = self.raw.GetXaxis().GetBinWidth(ix)
                if val > 0.0 : 
                    #mcStatVal = math.sqrt( staterr/binx/biny + mcStatVals[iy-1][ix-1]/binx/biny)
                    mcStatVal = math.sqrt( (staterr/val)**2 + (mcStatVals[iy-1][ix-1]/val/binx/biny)**2)
                else :
                    mcStatVal = 0.0                    
                self.mcStat.SetBinContent( ix, iy, mcStatVal )
        self.uncertainties['_mcStat'] = self.mcStat.Clone( self.nom.GetName() + "_mcStat")


        # Unpinch and smear out the uncertainties
        print self.uncertainties
        for iunc,unc in self.uncertainties.iteritems():
            if not unc:
                continue
            if not self.useSoftDrop :
                unpinch_vals( unc, xval=unc.GetXaxis().FindBin(self.xAxisRanges[iy-1][0]) )
            smooth( unc, delta=2, xmin = unc.GetXaxis().FindBin(500)-1)
            smooth( unc, delta=2 )
                
        # Now sum all of the uncertainties in quadrature
        self.totunc = self.nom.Clone( self.nom.GetName() + '_totunc')
        for ix in xrange(1,self.nom.GetNbinsX()+1):
            for iy in xrange(1,self.nom.GetNbinsY()+1):
                val = self.nom.GetBinContent(ix,iy)

                if abs(val) > 0.0 : 
                    err2 = self.nom.GetBinError(ix,iy) / val 
                    err2 = err2**2
                    for isystname in self.allsysts :
                        #print '%6s=%6.2e' % ( isyst, abs(isystval.GetBinContent(ix,iy)) ),
                        isystval = self.uncertainties[isystname]
                        err2 += (isystval.GetBinContent(ix,iy))**2
                    #print ' totunc=%6.2e' % ( math.sqrt(err2) ),
                    self.nom.SetBinError( ix, iy, math.sqrt(err2) * val )
                    self.totunc.SetBinContent( ix, iy, math.sqrt(err2) )
                    #print ' tot=%6.2e/%6.2e' % ( self.nom.GetBinError(ix,iy) , val )
        self.uncertainties["_totunc"] = self.totunc
        for ihist in self.uncertainties.itervalues() :
            ensureAbs(ihist)


        

    def readPythia(self):
        self.pythiaFile = ROOT.TFile( self.pythiaInputs )
        if self.useSoftDrop :
            self.pythiaHist = self.pythiaFile.Get("PFJet_pt_m_AK8SDgen").Clone( "pythia" + "PFJet_pt_m_AK8SDgen")
        else :
            self.pythiaHist = self.pythiaFile.Get("PFJet_pt_m_AK8Gen").Clone( "pythia" + "PFJet_pt_m_AK8gen")
        setStylesClass( hist=self.pythiaHist, istyle=self.histDriver_.styles['pythia'] )
        self.histDriver_.normalizeHist( self.pythiaHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
        if not self.normalizeUnity : 
            self.pythiaHist.Scale( self.nomNorm )

    def readHerwig(self):
        self.herwigFile = ROOT.TFile( self.herwigInputs )
        if self.useSoftDrop :
            self.herwigHist = self.herwigFile.Get("PFJet_pt_m_AK8SDgen").Clone( "herwig" + "PFJet_pt_m_AK8SDgen")
        else :
            self.herwigHist = self.herwigFile.Get("PFJet_pt_m_AK8Gen").Clone( "herwig" + "PFJet_pt_m_AK8gen")
        setStylesClass( hist=self.herwigHist, istyle=self.histDriver_.styles['herwig'] )
        self.histDriver_.normalizeHist( self.herwigHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
        if not self.normalizeUnity : 
            self.herwigHist.Scale( self.nomNorm )

    def readPowheg(self):
        powhegnorms = {
             9:2.1193569211303091e-06,
            24:6.6484332012113942e-06,
            17:4.4307535721251039e-08,
            05:4.4307535721251039e-08,
            12:6.6484332012113942e-06,
             6:1.1595650952686315e-07,
             2:9.0217025937519018e-10,
             3:3.3673066950289893e-09,
            14:9.0217025937519018e-10,
            22:4.2934493898958184e-06,
            20:1.0286268859966279e-06,
             4:1.6570917349274774e-08,
            16:1.6570917349274774e-08,
            19:2.7358869330354964e-07,
             7:2.7358869330354964e-07,
             1:4.5617935030748854e-10,
            15:3.3673066950289893e-09,
            13:4.5617935030748854e-10,
            11:8.0892638225999357e-06,
             8:1.0286268859966279e-06,
            23:8.0892638225999357e-06,
            10:4.2934493898958184e-06,
            21:2.1193569211303091e-06,
            18:1.1595650952686315e-07
            }

        
        self.powhegFile = ROOT.TFile( self.powhegInputs )

        self.powhegHist = self.pythiaHist.Clone( "powheg")
        powheghists = []
        if not self.useSoftDrop :            
            for h in [1,2,3,4,5,6,7,8,9]:
                ih = self.powhegFile.Get("CMS_SMP_16_010/d0"+str(h)+"-x01-y01")
                ih.Scale( 1.0 / powhegnorms[h] )
                powheghists.append( ih )
            for h in [10,11,12]:
                ih = self.powhegFile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01")
                ih.Scale( 1.0 / powhegnorms[h] )
                powheghists.append( ih )
        else : 
            for h in [13,14,15,16,17,18,19,20,21,22,23,24]:
                ih = self.powhegFile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01")
                ih.Scale( 1.0 / powhegnorms[h] )
                powheghists.append( ih )

        # Don't forget off-by-one from ROOT
        for iy,hist in enumerate(powheghists):
            for ix in xrange(1,hist.GetNbinsX()) :
                self.powhegHist.SetBinContent( ix, iy+1, hist.GetBinContent(ix) )
                self.powhegHist.SetBinError( ix, iy+1, hist.GetBinError(ix) )            
            
        setStylesClass( hist=self.powhegHist, istyle=self.histDriver_.styles['powheg'] )
        self.histDriver_.normalizeHist( self.powhegHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
        if not self.normalizeUnity : 
            self.powhegHist.Scale( self.nomNorm )

    def readTheory1(self):
        self.theoryfile1 = ROOT.TFile(self.theoryInputs1)
        for h in xrange(0, 12):
            self.theorylist1.append( self.theoryfile1.Get("histSD_"+str(h)+"_ours"))
            if self.theorylist1[h].Integral("width") > 0.0 : 
                self.theorylist1[h].Scale(1.0 / self.theorylist1[h].Integral("width") )
            binx = self.nom.GetXaxis().FindBin(50.)
            biny = h + 1
            ratio_bin = float(self.nom.GetBinContent( binx,biny )/self.theorylist1[h].GetBinContent( self.theorylist1[h].GetXaxis().FindBin(50.)))
            self.theorylist1[h].Scale(ratio_bin)
            setStylesClass( hist=self.theorylist1[h], istyle=self.histDriver_.styles['theory1'] )
            self.theorygraphs1.append( getGraph( self.theorylist1[h], width=3, minmassbin=0 ) )
            
        
    def readTheory2(self):
        self.theoryfile2 = ROOT.TFile(self.theoryInputs2)
        for h in xrange(0, 12):            
            self.theorylist2.append( self.theoryfile2.Get("hist_marzani_SD_"+str(h)))
            if self.scalePtBins :
                self.theorylist2[h].Scale(1.0 / self.theorylist2[h].Integral("width") )
            setStylesClass( hist=self.theorylist2[h], istyle=self.histDriver_.styles['theory2'] )
            self.theorygraphs2.append( getGraph( self.theorylist2[h], width=3, minmassbin=0 ) )
            
    def draw2D(self, postfix):
        c = ROOT.TCanvas("c" + postfix, "c" + postfix)
        c.SetLogz()
        
        self.histDriver_.canvs_.append(c)
        self.nom.Draw("colz")
        self.nom.SetMinimum(1e-12)
        self.nom.SetMaximum(1e-5)
        #self.nom.GetYaxis().SetRangeUser(200, 1300)
        #self.nom.GetXaxis().SetRangeUser(0, 800)
        self.histDriver_.stampCMS( c, "CMS")


    def printUnc( self ) :
        print '--------'
        for iy in xrange(1,5): 
            for n,v in self.uncertainties.iteritems() :
                print '%3d %8s: ' % (iy, n ),
                for ix in xrange(1,5):
                    print ' %6.1e ' % ( v.GetBinContent(ix,iy) ),
                print ''
                    
        
    def plotPtDist( self, hists, styleNames, title=None, filename = None) :

        c = ROOT.TCanvas("c" + hists[0].GetName() + "_ptcanvas", "c" + hists[0].GetName() + "_ptcanvas", 800, 600 )
        pad1,pad2 = self.histDriver_.setupPads( c )
        leg = ROOT.TLegend(0.6, 0.4, 0.83, 0.83)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetTextFont(43)
        self.histDriver_.legs_.append(leg)

        projs = []
        leg.AddEntry( hists[0], 'Data', 'p')
        for ihist, hist in enumerate( hists ):
            if ihist == 0 :
                leg.AddEntry( hist, 'Stat. + syst. unc.', 'f')
            elif ihist == 1 :
                leg.AddEntry( hist, 'Stat. unc.', 'f')
            else :
                legstyle = 'l'
                leg.AddEntry( hist, self.histDriver_.titles[styleNames[ihist]], legstyle)


            ##### Here, need to project sum( val * width )
            projy = None
            for im in xrange( 1, hist.GetNbinsX()) :
                proji = hist.ProjectionY(hist.GetName() + "_ptplot", im, im, "e")
                proji.Scale( hist.GetXaxis().GetBinWidth(im) )                
                if im == 1 :
                    projy = proji.Clone(hist.GetName() + "_ptplot")
                else :
                    #projy.Add( proji )
                    self.histDriver_.addCorrelated1D( projy, proji )
            projs.append(projy)
            self.histDriver_.hists_.append(projy)
            if title != None :
                projy.SetTitle( title )

            if ihist != 1 :
                ratioval = projs[0]
            else : 
                ratioval = projs[1]

            if ihist == 0 :
                option = "e2"
            elif ihist == 1 :
                option = "e2 same"
            else :
                option = "hist same"
            projy.GetXaxis().SetRangeUser(200,1300)

            self.histDriver_.plotHistAndRatio( pad1=pad1, pad2=pad2, hist=projy, nominal=ratioval,
                                option1=option, option2=option,
                                ratiotitle=";"+projy.GetXaxis().GetTitle()+";#frac{Theory}{Data}", logy=True, ratiorange=[0.,2.])

        pad1.cd()
        leg.Draw()
        projs[0].GetXaxis().SetLabelSize(0)
        projs[0].GetXaxis().SetTitleSize(0)

        
            
        self.histDriver_.stampCMS(pad1, "CMS", self.histDriver_.lumi_)
        if filename == None : 
            c.Print( projy.GetName() + ".png", "png")
            c.Print( projy.GetName() + ".pdf", "pdf")
            c.Print( projy.GetName() + ".root", "root")
        else :
            c.Print( filename + ".png", "png")
            c.Print( filename + ".pdf", "pdf")
            c.Print( filename + ".root", "root")
        c.Draw()
        self.histDriver_.canvs_.append(c)
        

                        

        
    def plotFullXSProjections( self, hists, styleNames, xAxisRange = None, theorycurves=None, plotlogm=False, legendpos = "right"):

        # First check pt,m bins that have large uncertainties and keep a record of them.
        # They will be used below to zero out bins in the plots.
        zerobins = []
        for iy in xrange(1,hists[0].GetNbinsY()+1):
            lowuncs = True
            for ix in xrange(hists[0].GetNbinsX() / 5, hists[0].GetNbinsX()+1):
                val = hists[0].GetBinContent(ix,iy)
                err = hists[0].GetBinError(ix,iy)
                if lowuncs and abs(val) > 0.0 and abs(err/val) > self.maxunc:
                    lowuncs = False
                if not lowuncs:
                    for ihist in hists :
                        ihist.SetBinContent(ix,iy,0.0)
                        ihist.SetBinError(ix,iy,0.0)

        for iy in xrange(1,hists[0].GetNbinsY()+1):
            if plotlogm : 
                c = ROOT.TCanvas("c" + str(iy) + self.postfix + '_logm', "c" + str(iy) + self.postfix, 800, 600)
            else:
                c = ROOT.TCanvas("c" + str(iy) + self.postfix, "c" + str(iy) + self.postfix, 800, 600)
            pad1,pad2 = self.histDriver_.setupPads( c )

            if legendpos == "right" :
                leg = ROOT.TLegend(0.53, 0.3, 0.84, 0.86, self.ptBinNames[iy-1] )
            else:
                leg = ROOT.TLegend(0.2, 0.46, 0.53, 0.89, self.ptBinNames[iy-1] )
            leg.SetBorderSize(0)
            leg.SetFillColor(0)
            leg.SetTextFont(43)
            self.histDriver_.legs_.append(leg)

            
            projs = []
            maxval = 0.0

            for ihist, hist in enumerate( hists ):

                if not plotlogm: 
                    projx = hist.ProjectionX('proj_' + hist.GetName() + self.postfix + str(iy), iy,iy, "e" )
                else :
                    projx = hist.ProjectionX('proj_' + hist.GetName() + self.postfix + str(iy) + "_dlogm", iy,iy, "e" )

                # Unpinch the uncertainties
                if not self.useSoftDrop :
                    unpinch( projx )#, xval=projx.GetXaxis().FindBin(self.xAxisRanges[iy-1][0]) )

                if plotlogm :
                    for ix in xrange( projx.GetNbinsX() ):
                        xval = projx.GetBinCenter(ix)
                        yval = projx.GetBinContent(ix)
                        yerr = projx.GetBinError(ix)
                        projx.SetBinContent( ix, xval * yval )
                        projx.SetBinError( ix, xval * yerr )
                
                setStylesClass( projx,istyle=self.histDriver_.styles[styleNames[ihist]] )
                projs.append(projx)
                self.extraHists.append(projx)

                if ihist != 1 :
                    ratioval = projs[0]
                else : 
                    ratioval = projs[1]
                
                if xAxisRange != None :
                    projx.GetXaxis().SetRangeUser( xAxisRange[0], xAxisRange[1] )
                
                if ihist == 0 :
                    leg.AddEntry( projx, 'Data', 'p')
                    leg.AddEntry( projx, 'Stat. + syst. unc.', 'f')
                elif ihist == 1 :
                    leg.AddEntry( projx, 'Stat. unc.', 'f')
                else :
                    legstyle = 'l'
                    leg.AddEntry( projx, self.histDriver_.titles[styleNames[ihist]], legstyle)

                if self.useSoftDrop == False :                    
                    if projx.GetMaximum() * 1.2 > maxval :
                        maxval = projx.GetMaximum() * 1.2
                elif plotlogm :
                    if projx.GetMaximum() * 2.0 > maxval :
                        maxval = projx.GetMaximum() * 2.0
                else :
                    if projx.GetBinContent( projx.GetXaxis().FindBin(10.0) ) * 1.2 > maxval :
                        maxval = projx.GetBinContent(projx.GetXaxis().FindBin(10.0)) * 1.2
                if not self.normalizeUnity : 
                    projx.GetYaxis().SetTitle("#frac{d^{2}#sigma}{dm" + self.subscript + " dp_{T}} (pb/GeV^{2})")
                elif plotlogm : 
                    projx.GetYaxis().SetTitle("#frac{m" + self.subscript + "}{d#sigma/dp_{T}} #frac{d^{2}#sigma}{dm" + self.subscript + " dp_{T}}")
                else:
                    projx.GetYaxis().SetTitle("#frac{1}{d#sigma/dp_{T}} #frac{d^{2}#sigma}{dm" + self.subscript + " dp_{T}} (1/GeV)")

                
                self.histDriver_.hists_.append(projx)
                #if title != None :
                #    projx.SetTitle( title )

                if ihist == 0 :
                    option = "e2 ]["
                elif ihist == 1 :
                    option = "e2 same ]["
                else :
                    option = "hist same ]["
                #projx.GetXaxis().SetRangeUser(00,1300)
                #print projx.GetName()
                #print 'Integral() = ', projx.Integral(), ', Integral(width) = ', projx.Integral('width')


                self.histDriver_.plotHistAndRatio( pad1=pad1, pad2=pad2, hist=projx, nominal=ratioval,
                                       option1=option, option2=option,
                                       ratiotitle=";"+projx.GetXaxis().GetTitle()+";#frac{Theory}{Data}", logy=False, logx=True, ratiorange=[0.,2.],xAxisRange=self.xAxisRanges[iy-1])

                pad1.cd()
                projs[0].SetMaximum(maxval)
                projs[0].SetMinimum(0.0)
                projs[0].GetXaxis().SetLabelSize(0)
                projs[0].GetXaxis().SetTitleSize(0)
                projs[0].GetYaxis().SetTitleSize( 25 )
                projs[0].GetYaxis().SetLabelSize( 19 )
                projs[0].GetYaxis().SetTitleOffset( 1.5 )                
            if theorycurves != None: 
                for theory in theorycurves :
                    if not plotlogm: 
                        hist=self.theorylist[ self.theorydict[theory] ] [iy-1]
                    else:
                        hist=self.theorylist[ self.theorydict[theory] ] [iy-1].Clone( self.theorylist[ self.theorydict[theory] ] [iy-1].GetName() + "_dlogm")
                        self.extraHists.append( hist )
                    for ix in xrange(hist.GetNbinsX()):
                        val = hist.GetBinContent(ix)
                        err = hist.GetBinError(ix)
                        if val > 0 and abs(err/val) > 1.0:
                            hist.SetBinError(ix, hist.GetBinError(ix-1))
                    if plotlogm :
                        for ix in xrange( hist.GetNbinsX() ):
                            xval = hist.GetBinCenter(ix)
                            yval = hist.GetBinContent(ix)
                            yerr = hist.GetBinError(ix)
                            hist.SetBinContent( ix, xval * yval )
                            hist.SetBinError( ix, xval * yerr )
                    legstyle = 'l'
                    leg.AddEntry( hist, self.histDriver_.titles[theory], "p")
                    self.histDriver_.plotHistAndRatio( pad1=pad1, pad2=pad2, hist=hist , nominal=projs[0],
                                                           option1="e1 x0 same ][", option2="e1 x0 same ][",
                                                           ratiotitle=";",
                                                           logy=False, logx=True, ratiorange=[0.,2.],xAxisRange=self.xAxisRanges[iy-1] ) 
                    #leg.AddEntry( g11, self.histDriver_.titles[theory], 'f')
                    
            pad1.cd()
            leg.Draw()

            
                    
            self.histDriver_.stampCMS(pad1, "CMS", self.histDriver_.lumi_)
            self.histDriver_.canvs_.append(c)

            # Write the histograms in a flat ROOT tree for conversion to YAML and YODA and whatever else theorists want instead of using ROOT
            fout = ROOT.TFile("rawout_fullxs_" + self.postfix + str(iy) + ".root", "RECREATE")
            for proj in projs :
                proj.Write()
            fout.Close()
            if plotlogm == False:
                c.Print("fullxs_" + self.postfix + str(iy) + ".png", "png")
                c.Print("fullxs_" + self.postfix + str(iy) + ".pdf", "pdf")
                c.Print("fullxs_" + self.postfix + str(iy) + ".root", "root")
            else:
                c.Print("fullxs_" + self.postfix + str(iy) + "_mdsigmadm.png", "png")
                c.Print("fullxs_" + self.postfix + str(iy) + "_mdsigmadm.pdf", "pdf")
                c.Print("fullxs_" + self.postfix + str(iy) + "_mdsigmadm.root", "root")
            c.Draw()



    def plotFullUncs( self, hists ):

        canvs = []
        for iy in xrange(1,hists.values()[0].GetNbinsY()+1):
            c = ROOT.TCanvas("cunc" + str(iy) + self.postfix, "cunc" + str(iy) + self.postfix, 800, 600)
            self.histDriver_.canvs_.append(c)
            canvs.append(c)
            leg= ROOT.TLegend( 0.2, 0.54, 0.84, 0.89, self.ptBinNames[iy-1])
            leg.SetEntrySeparation( 2.0 * leg.GetEntrySeparation() )
            leg.SetBorderSize(0)
            leg.SetFillColor(0)
            leg.SetNColumns(2)
            leg.SetTextFont(43)
            if self.useSoftDrop :
                stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), ";Groomed jet mass m_{g} (GeV);Fractional uncertainty" )
            else :
                stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), ";Ungroomed jet mass m_{u} (GeV);Fractional uncertainty" )



            for key in self.sysnames :
                hist = hists[key]

                proj = hist.ProjectionX('proj_' + hist.GetName()+ self.postfix + str(iy), iy,iy, "e" )
                leg.AddEntry( proj, self.uncertaintyNames[key] , "l")

                
                if not self.useSoftDrop :
                    unpinch_vals( proj, xval=proj.GetXaxis().FindBin(self.xAxisRanges[iy-1][0]) )
                smooth( proj, delta=2, xmin = proj.GetXaxis().FindBin(500)-1)
                smooth( proj, delta=2 )
                    
                setStylesClass( proj, self.histDriver_.sysStyles[key] )
                self.histDriver_.hists_.append(proj)
                stack.Add( proj, "hist ][" )


                
            stack.Draw("nostack hist ][")
            stack.SetMinimum(1e-4)
            stack.SetMaximum(1e3)
            stack.GetXaxis().SetRangeUser( self.xAxisRanges[iy-1][0], self.xAxisRanges[iy-1][1] )
            stack.GetXaxis().SetLabelFont(42)
            stack.GetXaxis().SetLabelSize(0.05)
            stack.GetXaxis().SetNoExponent()
            stack.GetXaxis().SetMoreLogLabels()
            stack.GetYaxis().SetTitleOffset(1.2)
            leg.Draw()
            self.histDriver_.stacks_.append(stack)
            self.histDriver_.legs_.append(leg)
            c.SetLogy()
            c.SetLogx()
            self.histDriver_.stampCMS(c, "CMS")
            c.Print("uncertainties_" + self.postfix + str(iy) + ".png", "png")
            c.Print("uncertainties_" + self.postfix + str(iy) + ".pdf", "pdf")
            c.Print("uncertainties_" + self.postfix + str(iy) + ".root", "root")
            c.Draw()


    def getRelative(self, histnom, histavg, histup, histdn ):
        histup.Add( histnom, -1.0 )
        histdn.Add( histnom, -1.0 )
        setToAverage( histavg, histup, histdn )
        histavg.Divide( histnom )
        
    def getUpAndDown(self, fnom, sys ):
        sysup = sys + 'up'
        sysdn = sys + 'dn'
        resup = fnom.Get('2d_response' + self.postfix1 + sysup)
        resdn = fnom.Get('2d_response' + self.postfix1 + sysdn)

        self.responses[sysup] = resup
        self.responses[sysdn] = resdn

        histup = self.responses[sysup].Hreco()
        histdn = self.responses[sysdn].Hreco()
        self.histDriver_.normalizeHist( histup, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( histdn, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        
        return histup, histdn
