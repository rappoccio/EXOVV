#! /usr/bin/env python

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from HistDriver import *
import math
import pickle

class RooUnfoldUnfolder:
    def __init__(self, inputs = "2DData", pythiaInputs=None, herwigInputs=None, powhegInputs=None,
                 useSoftDrop=False, normalizeUnity=True, scalePtBins=False, lumi=2.3e3, dlumi=0.027, postfix=''):

        self.histDriver_ = HistDriver(lumi=lumi, dlumi=dlumi)        # Creates and stores histograms so they don't go out of scope
        self.inputs = inputs                                         # String for inputs to use
        self.pythiaInputs=pythiaInputs                               # String for pythia filename
        self.herwigInputs=herwigInputs                               # String for herwig filename
        self.powhegInputs=powhegInputs                               # String for powheg filename
        self.pythiaHist = None                                       # Pythia histogram(s) 
        self.herwigHist = None                                       # Herwig histogram(s)
        self.powhegHist = None                                       # Powheg histogram(s)
        self.pythiaFile = None                                       # Pythia file
        self.herwigFile = None                                       # Herwig file 
        self.powhegFile = None                                       # Powheg file
        self.useSoftDrop = useSoftDrop                               # Use soft drop
        self.normalizeUnity = normalizeUnity                         # Normalize total histogram to unity (via Integral("width"))
        self.scalePtBins = scalePtBins                               # Scale each pt bin separately
        self.expsysnames = [ '_jec', '_jer', '_jmr', '_jms', '_pu' ] # Experimental uncertainties EXCEPT for jec
        self.thsysnames = ['_pdf', '_ps', '_mcStat']                 # Theory uncertainties
        self.flatsysnames = ['_lum']                                 # Flat uncertainties
        self.sysnames = self.expsysnames + self.flatsysnames + self.thsysnames + ['_totunc'] # All uncertainties
        self.responses = dict()                                      # RooUnfoldResponse objects
        self.nom = None                                              # TH2D representing central value with stat+sys uncertainties
        self.jernom = None                                           # TH2D representing central value in JER
        self.jmrnom = None                                           # TH2D representing central value in JMR
        self.nomStat = None                                          # TH2D representing central value with ONLY stat uncertainties
        self.nomNorm = None                                          # Normalization of the nominal. If we don't normalize to unity, we normalize Herwig to this. 
        self.postfix = postfix
        self.files = {}
        
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
        unctitles = ['JEC', 'JER', 'JMR', 'JMS', 'PU', 'Lumi', 'PDF', 'Physics Model', 'Stat. Unc.', 'Total']
        for i in xrange(53) :
            unctitles += 'JEC' + str(i)
        self.uncertaintyNames = dict( zip( self.sysnames, unctitles ) )

        self.ptBinNames = ['200 < p_{T} < 260 GeV','260 < p_{T} < 350 GeV','350 < p_{T} < 460 GeV','460 < p_{T} < 550 GeV','550 < p_{T} < 650 GeV','650 < p_{T} < 760 GeV', '760 < p_{T} < 900 GeV', '900 < p_{T} < 1000 GeV', '1000 < p_{T} < 1100 GeV','1100 < p_{T} < 1200 GeV',
    '1200 < p_{T} < 1300 GeV', 'p_{T} > 1300 GeV']
        if self.useSoftDrop == False : 
            self.xAxisRanges = [
                [20,1000],
                [20,1000],
                [20,1000],
                [20,1000],
                [20,1000],
                [20,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                ]
        else :
            self.xAxisRanges = [
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                [10,1000],
                ]

        if not self.useSoftDrop: 
            self.postfix1 = ''
            self.postfix2 = ''            
        else: 
            self.postfix1 = "_softdrop"
            self.postfix2 = "SD"

        self.readExp()

        if self.pythiaInputs != None :
            self.readPythia()
        if self.herwigInputs != None :
            self.readHerwig()
        if self.powhegInputs != None :
            self.readPowheg()
            
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

        print self.nom.Integral()
        self.unsmeared = self.responses['unsmeared'].Hreco()
        self.unsmearedForPS = self.unsmeared.Clone( self.nom.GetName() + "_normalizingPS")
        self.rawForStat = self.raw.Clone( self.raw.GetName() + "_forstats")
        self.histDriver_.normalizeHist( self.unsmearedForPS, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True)
        self.histDriver_.normalizeHist( self.rawForStat, normalizeUnity = self.normalizeUnity, divideByBinWidths=True, scalePtBins = True)
        #self.histDriver_.normalizeHist( self.unsmeared, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True)
        
        self.nom.UseCurrentStyle()

        #ROOT.gStyle.SetTitleSize(0.04, "XYZ")

        if not self.useSoftDrop: 
            self.nom.SetTitle(";Ungroomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")
        else :
            self.nom.SetTitle(";Groomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")

        self.histDriver_.normalizeHist( self.nom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.jernom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.jmrnom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
        self.histDriver_.normalizeHist( self.unsmeared, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )

        self.nomNorm = self.nom.Integral("width")
        
        # Each experimental uncertainty has an "up" and a "down" variation, so
        # the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
        for sys in self.expsysnames :
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

            # Take difference to nominal... next step takes abs() so ignore relative sign
            if sys in ['_jec', '_jer', '_jms', '_pu' ] : 
                histup.Add( self.jernom, -1.0 )
                histdn.Add( self.jernom, -1.0 )
                self.uncertainties[sys] = self.jernom.Clone( self.nom.GetName() + "_" + sys )
                setToAverage( self.uncertainties[sys], histup, histdn )
                self.uncertainties[sys].Divide( self.jernom )
            elif sys in ['_jmr']:
                histup.Add( self.jmrnom, -1.0 )
                histdn.Add( self.jmrnom, -1.0 )
                self.uncertainties[sys] = self.jmrnom.Clone( self.jmrnom.GetName() + "_" + sys )
                setToAverage( self.uncertainties[sys], histup, histdn )
                self.uncertainties[sys].Divide( self.jmrnom )                

        self.uncertainties['_lum'] = self.nom.Clone( self.nom.GetName() + "_lum" )
        for ix in xrange(0, self.unsmeared.GetXaxis().FindBin( self.nom.GetXaxis().GetXmax() ) ):
            for iy in xrange(0, self.unsmeared.GetNbinsY()+2):
                if self.unsmeared.GetBinContent(ix,iy) > 0.0 :
                    if self.normalizeUnity == False : 
                        self.uncertainties['_lum'].SetBinContent( ix, iy, math.sqrt( self.histDriver_.dlumi2_ )  )
                    else :
                        self.uncertainties['_lum'].SetBinContent( ix, iy, 0.0 )

        # Next : PDF and PS uncertainties
        fpdf = ROOT.TFile("unfoldedpdf_pdf4lhc15.root")
        self.files['pdf'] = fpdf

        pdfpostfix = ''
        if "Data" in self.inputs :
            pdfpostfix = '_data'


        #print 'Getting PDFs:'
        #print 'unfold' + pdfpostfix + '_mstw' + self.postfix1 
        mpdfup = fpdf.Get( 'unfold' + pdfpostfix + '_pdfup' + self.postfix1 )
        mpdfdn = fpdf.Get( 'unfold' + pdfpostfix + '_pdfdn' + self.postfix1 )
        
        self.responses['_pdfup'] =  mpdfup 
        self.responses['_pdfdn'] =  mpdfdn
        hpdfup = mpdfup.Hreco()
        hpdfdn = mpdfdn.Hreco()

        
        for hist in [ hpdfup, hpdfdn] :
            self.histDriver_.normalizeHist( hist, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True )


        hpdfdiff = hpdfup.Clone(hpdfup.GetName() + "_difftodn")
        hpdfdiff.Add( hpdfdn, -1.0 )
        hpdfdiff.Scale(0.5)

        #hmstw.Add( self.unsmearedForPS, -1.0 )
        #hcteq.Add( self.unsmearedForPS, -1.0 )

        
        self.uncertainties['_pdf'] = hpdfdiff.Clone( self.unsmeared.GetName() + "_pdf")
        
        
        for iy in xrange(0,hpdfdiff.GetNbinsY()+2) :
            for ix in xrange(0,hpdfup.GetNbinsX()+2) :
                diff1 = abs(hpdfdiff.GetBinContent(ix,iy))
                self.uncertainties['_pdf'].SetBinContent(ix,iy,diff1)                

        self.uncertainties['_pdf'].Divide( self.unsmearedForPS )
        
                                               
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
        
        # HAVE to normalize a pythia clone and the herwig to unity per pt bin regardless for systematic
        # uncertainty estimation. 
        #self.histDriver_.normalizeHist( hps, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins  )
        #self.histDriver_.normalizeHist( self.unsmearedForPS, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins)
        self.histDriver_.normalizeHist( hps, normalizeUnity = True, divideByBinWidths=True, scalePtBins = True  )

      
        # This holds [ (dsigma/dm)_pythia - (dsigma/dm)_herwig ]
        
        hps.Add( self.unsmearedForPS, -1.0 )
        ensureAbs( hps )
        hps.Scale(0.5)
        
        #hps.Divide(self.unsmearedForPS)
        hps.Divide(self.unsmearedForPS)
        # Now set up the PS uncertainties themselves:
        self.uncertainties['_ps'] = hps.Clone( self.nom.GetName() + "_ps" )

        picklePostfix = ""
        if "Data" in self.inputs :
            picklePostfix = "data"
        #RMS_vals = pickle.load(open("ungroomed" + picklePostfix +"JackKnifeRMS.p", "rb"))         ########
        #RMS_vals_softdrop = pickle.load(open("softdrop" + picklePostfix +"JackKnifeRMS.p", "rb")) ########

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

        
        # Set up the stat uncertainties
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

        #self.mcStat.Divide( self.nomForPS )
        #printHist( self.mcStat, maxx=5,maxy=3 )
        self.uncertainties['_mcStat'] = self.mcStat.Clone( self.nom.GetName() + "_mcStat")
        
        # Now sum all of the uncertainties in quadrature
        self.totunc = self.nom.Clone( self.nom.GetName() + '_totunc')
        for ix in xrange(1,self.nom.GetNbinsX()+1):
            for iy in xrange(1,self.nom.GetNbinsY()+1):
                val = self.nom.GetBinContent(ix,iy)

                if abs(val) > 0.0 : 
                    err2 = self.nom.GetBinError(ix,iy) / val 
                    err2 = err2**2
                    for isystname in self.expsysnames + self.flatsysnames + self.thsysnames :
                        #print '%6s=%6.2e' % ( isyst, abs(isystval.GetBinContent(ix,iy)) ),
                        isystval = self.uncertainties[isystname]
                        err2 += (isystval.GetBinContent(ix,iy))**2
                    #print ' totunc=%6.2e' % ( math.sqrt(err2) ),
                    self.nom.SetBinError( ix, iy, math.sqrt(err2) * val )
                    self.totunc.SetBinContent( ix, iy, math.sqrt(err2) )
                    #print ' tot=%6.2e/%6.2e' % ( self.nom.GetBinError(ix,iy) , val )

        #self.printUnc()
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
        self.powhegFile = ROOT.TFile( self.powhegInputs )

        self.powhegHist = self.pythiaHist.Clone( "powheg")
        powheghists = []
        if not self.useSoftDrop :            
            for h in [1,2,3,4,5,6,7,8,9]:
                powheghists.append( self.powhegFile.Get("CMS_SMP_16_010/d0"+str(h)+"-x01-y01"))
            for h in [10,11,12]:
                powheghists.append( self.powhegFile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))
        else : 
            for h in [13,14,15,16,17,18,19,20,21,22,23,24]:
                powheghists.append( self.powhegFile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))

        # Don't forget off-by-one from ROOT
        for iy,hist in enumerate(powheghists):
            for ix in xrange(1,hist.GetNbinsX()) :
                self.powhegHist.SetBinContent( ix, iy+1, hist.GetBinContent(ix) )
                self.powhegHist.SetBinError( ix, iy+1, hist.GetBinError(ix) )            
            
        setStylesClass( hist=self.powhegHist, istyle=self.histDriver_.styles['powheg'] )
        self.histDriver_.normalizeHist( self.powhegHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
        if not self.normalizeUnity : 
            self.powhegHist.Scale( self.nomNorm )
        
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
                leg.AddEntry( hist, 'Stat. + Syst. Unc.', 'f')
            elif ihist == 1 :
                leg.AddEntry( hist, 'Stat. Unc.', 'f')
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
        

                        

        
    def plotFullXSProjections( self, hists, styleNames, xAxisRange = None):


        for iy in xrange(1,hists[0].GetNbinsY()+1):
            c = ROOT.TCanvas("c" + str(iy) + self.postfix, "c" + str(iy) + self.postfix, 800, 600)
            pad1,pad2 = self.histDriver_.setupPads( c )

            leg = ROOT.TLegend(0.5, 0.4, 0.83, 0.83, self.ptBinNames[iy-1] )
            leg.SetBorderSize(0)
            leg.SetFillColor(0)
            leg.SetTextFont(43)
            self.histDriver_.legs_.append(leg)

            
            projs = []
            maxval = 0.0

            for ihist, hist in enumerate( hists ):
                
                    

                projx = hist.ProjectionX('proj_' + hist.GetName() + self.postfix + str(iy), iy,iy, "e" )
                setStylesClass( projx,istyle=self.histDriver_.styles[styleNames[ihist]] )
                projs.append(projx)

                if ihist != 1 :
                    ratioval = projs[0]
                else : 
                    ratioval = projs[1]
                
                if xAxisRange != None :
                    projx.GetXaxis().SetRangeUser( xAxisRange[0], xAxisRange[1] )
                
                if ihist == 0 :
                    leg.AddEntry( projx, 'Data', 'p')
                    leg.AddEntry( projx, 'Stat. + Syst. Unc.', 'f')
                elif ihist == 1 :
                    leg.AddEntry( projx, 'Stat. Unc.', 'f')
                else :
                    legstyle = 'l'
                    leg.AddEntry( projx, self.histDriver_.titles[styleNames[ihist]], legstyle)

                if self.useSoftDrop == False :                    
                    if projx.GetMaximum() * 1.2 > maxval :
                        maxval = projx.GetMaximum() * 1.2
                else :
                    if projx.GetBinContent( projx.GetXaxis().FindBin(10.0) ) * 1.2 > maxval :
                        maxval = projx.GetBinContent(projx.GetXaxis().FindBin(10.0)) * 1.2
                if not self.normalizeUnity : 
                    projx.GetYaxis().SetTitle("#frac{d^{2}#sigma}{dm dp_{T}} (pb/GeV^{2})")
                else : 
                    projx.GetYaxis().SetTitle("Normalized cross section (1/GeV)")

                
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

    
                self.histDriver_.plotHistAndRatio( pad1=pad1, pad2=pad2, hist=projx, nominal=ratioval,
                                       option1=option, option2=option,
                                       ratiotitle=";"+projx.GetXaxis().GetTitle()+";#frac{Theory}{Data}", logy=False, logx=True, ratiorange=[0.,2.],xAxisRange=self.xAxisRanges[iy])

                pad1.cd()
                projs[0].SetMaximum(maxval)
                projs[0].SetMinimum(0.0)
                projs[0].GetXaxis().SetLabelSize(0)
                projs[0].GetXaxis().SetTitleSize(0)
                projs[0].GetYaxis().SetTitleSize( 25 )
                projs[0].GetYaxis().SetLabelSize( 19 )
                projs[0].GetYaxis().SetTitleOffset( 1.5 )                
                leg.Draw()
            
            
            self.histDriver_.stampCMS(pad1, "CMS", self.histDriver_.lumi_)
            self.histDriver_.canvs_.append(c)
            c.Print("fullxs_" + self.postfix + str(iy) + ".png", "png")
            c.Print("fullxs_" + self.postfix + str(iy) + ".pdf", "pdf")
            c.Draw()



    def plotFullUncs( self, hists ):

        canvs = []
        for iy in xrange(1,hists.values()[0].GetNbinsY()+1):
            c = ROOT.TCanvas("cunc" + str(iy) + self.postfix, "cunc" + str(iy) + self.postfix, 800, 600)
            self.histDriver_.canvs_.append(c)
            canvs.append(c)
            leg= ROOT.TLegend( 0.2, 0.54, 0.84, 0.84, self.ptBinNames[iy-1])
            leg.SetBorderSize(0)
            leg.SetFillColor(0)
            leg.SetNColumns(2)
            leg.SetTextFont(43)
            if self.useSoftDrop :
                stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), ";Groomed jet mass (GeV);Fractional Uncertainty" )
            else :
                stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), ";Jet mass (GeV);Fractional Uncertainty" )



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
            stack.GetXaxis().SetNoExponent()
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
