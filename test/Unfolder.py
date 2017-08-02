#! /usr/bin/env python

import ROOT
ROOT.gSystem.Load("RooUnfold/libRooUnfold")

from HistDriver import *
import math
import pickle

class RooUnfoldUnfolder:
    def __init__(self, inputs = "2DData", pythiaInputs=None, herwigInputs=None, powhegInputs=None,
                 useSoftDrop=False, normalizeUnity=True, scalePtBins=False, lumi=2.3e3, dlumi=0.027):

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
        self.expsysnames = [ '_jer', '_jec', '_jmr', '_jms', '_pu' ] # Experimental uncertainties
        self.thsysnames = ['_pdf', '_ps']                            # Theory uncertainties
        self.sysnames = self.expsysnames + self.thsysnames           # All uncertainties
        self.files = dict()                                          # Store files
        self.responses = dict()                                      # RooUnfoldResponse objects
        self.nom = None                                              # TH2D representing central value with stat+sys uncertainties
        self.nomStat = None                                          # TH2D representing central value with ONLY stat uncertainties
        self.nomNorm = None                                          # Normalization of the nominal. If we don't normalize to unity, we normalize Herwig to this. 

        self.uncertainties = dict(                                   # TH2D's representing uncertainties
            zip(self.sysnames, [None] * len(self.sysnames) )
            )

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
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
                [40,1000],
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
        fnom = ROOT.TFile(self.inputs + '.root')
        self.files['nom'] = fnom
        self.responses['nom'] = fnom.Get('2d_response' + self.postfix1 )
        self.nom = self.responses['nom'].Hreco()
        
        
        self.nom.UseCurrentStyle()

        #ROOT.gStyle.SetTitleSize(0.04, "XYZ")

        if not self.useSoftDrop: 
            self.nom.SetTitle(";Ungroomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")
        else :
            self.nom.SetTitle(";Groomed jet mass (GeV);Ungroomed jet p_{T} (GeV)")

        self.histDriver_.normalizeHist( self.nom, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )

        self.nomNorm = self.nom.Integral("width")
        
        # Each experimental uncertainty has an "up" and a "down" variation, so
        # the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
        for sys in self.expsysnames :
            sysup = sys + 'up'
            sysdn = sys + 'dn'
            fup = ROOT.TFile( self.inputs + sysup + '.root')
            fdn = ROOT.TFile( self.inputs + sysdn + '.root')
            resup = fup.Get('2d_response' + self.postfix1 + sysup)
            resdn = fdn.Get('2d_response' + self.postfix1 + sysdn)

            self.files[sysup] = fup
            self.files[sysdn] = fdn
            self.responses[sysup] = resup
            self.responses[sysdn] = resdn

            histup = self.responses[sysup].Hreco()
            histdn = self.responses[sysdn].Hreco()
            self.histDriver_.normalizeHist( histup, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )
            self.histDriver_.normalizeHist( histdn, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )

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

        
        mpdfup = fpdf.Get( '2d_response' + self.postfix1 + '_pdfup' )
        mpdfdn  = fpdf.Get( '2d_response' + self.postfix1 + '_pdfdn' )
        mmstw = fpdf.Get( '2d_response' + self.postfix1 + '_mstw' )
        mcteq = fpdf.Get( '2d_response' + self.postfix1 + '_cteq' )
        
        self.responses['_pdfup'] =  mpdfup 
        self.responses['_pdfdn'] =  mpdfdn 
        self.responses['_mstw'] =  mmstw 
        self.responses['_cteq'] =  mcteq
        hpdfup = mpdfup.Hreco()
        hpdfdn = mpdfdn.Hreco()
        hmstw = mmstw.Hreco()
        hcteq = mcteq.Hreco()
        for hist in [ hpdfup, hpdfdn, hmstw, hcteq] :
            self.histDriver_.normalizeHist( hist, normalizeUnity = self.normalizeUnity, scalePtBins = self.scalePtBins )

        
        hpdfup.Add( self.nom, -1.0 )
        hpdfdn.Add( self.nom, -1.0 )
            
        self.uncertainties['_pdf'] = hpdfup.Clone( self.nom.GetName() + "_pdf")
        setToAverage( self.uncertainties['_pdf'], hpdfup, hpdfup )    
        self.uncertainties['_pdf'].Divide( self.nom )

        #### FIXME FIXME FIXME FIXME : the uncertainties for CTEQ and MSTW still need to be included!!
        #### FIXME FIXME FIXME FIXME : the PDF up and down should be 0.5*(up-dn), not (up-dn)

        # Parton shower: Half the difference between pythia and herwig
        # However : There is a different pt spectrum, so need to correct per pt bin to
        # just get the mass differences
        self.files['_ps'] = ROOT.TFile("PS_hists.root")
        self.responses['_ps'] = self.files['_ps'].Get( 'unfold_ps_data' + self.postfix1 + '_herwig' )
        hps = self.responses['_ps'].Hreco()
        
        # HAVE to normalize a pythia clone and the herwig to unity per pt bin regardless for systematic
        # uncertainty estimation. 
        self.histDriver_.normalizeHist( hps, normalizeUnity = True, scalePtBins = True  )
        nomForPS = self.nom.Clone( self.nom.GetName() + "_normalizingPS")
        self.histDriver_.normalizeHist( nomForPS, normalizeUnity = True, scalePtBins = True) # Normalization to unity already done
        
        # This holds 0.5 * [ (dsigma/dm)_pythia - (dsigma/dm)_herwig ]
        hps.Add( nomForPS, -1.0 )
        hps.Scale(0.5)
        #for ix in xrange(1,10) :
        #    print " %8.1e" % ( hps.GetBinContent(ix, 2) ),
        #print ''

        # Now set up the PS uncertainties themselves:
        self.uncertainties['_ps'] = self.nom.Clone( self.nom.GetName() + "_ps" )
        for ix in xrange(1,self.nom.GetNbinsX()+1) :
            for iy in xrange(1,self.nom.GetNbinsY()+1) :
                value = abs(hps.GetBinContent(ix,iy))
                self.uncertainties['_ps'].SetBinContent(ix,iy,value)

                
                
        #self.uncertainties['_ps'].Add( hps, -0.5 )
        #self.uncertainties['_ps'].Divide( self.nom )


        RMS_vals = pickle.load(open("ungroomeddataJackKnifeRMS.p", "rb"))         ########
        RMS_vals_softdrop = pickle.load(open("softdropdataJackKnifeRMS.p", "rb")) ########
        if not self.useSoftDrop :
            mcStatVals = RMS_vals
        else :
            mcStatVals = RMS_vals_softdrop

        
        # Set up the stat uncertainties
        self.nomStat = self.nom.Clone( self.nom.GetName() + "_stat" )
        self.mcStat = self.nom.Clone( self.nom.GetName() + "_mcstat" )


        setStyles( self.nom, fillStyle=1001, fillColor=ROOT.kGray, markerStyle=20)
        setStyles( self.nomStat, fillStyle=1001, fillColor=ROOT.kGray+2)
        
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


    def readPythia(self):
        self.pythiaFile = ROOT.TFile( self.pythiaInputs )
        if self.useSoftDrop :
            self.pythiaHist = self.pythiaFile.Get("PFJet_pt_m_AK8SDgen").Clone( "pythia" + "PFJet_pt_m_AK8SDgen")
        else :
            self.pythiaHist = self.pythiaFile.Get("PFJet_pt_m_AK8Gen").Clone( "pythia" + "PFJet_pt_m_AK8gen")
        setStylesClass( hist=self.pythiaHist, istyle=self.histDriver_.styles['pythia'] )
        self.histDriver_.normalizeHist( self.pythiaHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
        self.pythiaHist.Scale( self.nomNorm )

    def readHerwig(self):
        self.herwigFile = ROOT.TFile( self.herwigInputs )
        if self.useSoftDrop :
            self.herwigHist = self.herwigFile.Get("PFJet_pt_m_AK8SDgen").Clone( "herwig" + "PFJet_pt_m_AK8SDgen")
        else :
            self.herwigHist = self.herwigFile.Get("PFJet_pt_m_AK8Gen").Clone( "herwig" + "PFJet_pt_m_AK8gen")
        setStylesClass( hist=self.herwigHist, istyle=self.histDriver_.styles['herwig'] )
        self.histDriver_.normalizeHist( self.herwigHist, normalizeUnity = True, scalePtBins = self.scalePtBins )
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


        
    def plotPtDist( self, hists, styleNames, title=None, filename = None) :

        c = ROOT.TCanvas("c" + hists[0].GetName() + "_ptcanvas", "c" + hists[0].GetName() + "_ptcanvas", 800, 600 )
        pad1,pad2 = self.histDriver_.setupPads( c )
        leg = ROOT.TLegend(0.6, 0.4, 0.83, 0.83)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
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
            projy = hist.ProjectionY(hist.GetName() + "_ptplot")
            setStylesClass( projy, istyle=self.histDriver_.styles[styleNames[ihist]] )
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
        else :
            c.Print( filename + ".png", "png")
            c.Print( filename + ".pdf", "pdf")
        self.histDriver_.canvs_.append(c)
        

                        

        
    def plotFullXSProjections( self, hists, styleNames, postfix="", xAxisRange = None):


        for iy in xrange(1,hists[0].GetNbinsY()+1):
            c = ROOT.TCanvas("c" + str(iy) + postfix, "c" + str(iy) + postfix)
            pad1,pad2 = self.histDriver_.setupPads( c )

            leg = ROOT.TLegend(0.6, 0.4, 0.83, 0.83)
            leg.SetBorderSize(0)
            leg.SetFillColor(0)
            self.histDriver_.legs_.append(leg)

            
            projs = []
            maxval = 0.0

            for ihist, hist in enumerate( hists ):
                
                    

                projx = hist.ProjectionX('proj_' + hist.GetName() + postfix + str(iy), iy,iy, "e" )
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
                    if projx.GetBinContent(4) * 1.4 > maxval :
                        maxval = projx.GetBinContent(4) * 1.4
                projx.GetYaxis().SetTitle("#frac{d^{2}#sigma}{dm dp_{T}} (pb/GeV^{2})")

                
                self.histDriver_.hists_.append(projx)
                #if title != None :
                #    projx.SetTitle( title )

                if ihist == 0 :
                    option = "e2"
                elif ihist == 1 :
                    option = "e2 same"
                else :
                    option = "hist same"
                #projx.GetXaxis().SetRangeUser(00,1300)
    
                self.histDriver_.plotHistAndRatio( pad1=pad1, pad2=pad2, hist=projx, nominal=ratioval,
                                       option1=option, option2=option,
                                       ratiotitle=";"+projx.GetXaxis().GetTitle()+";#frac{Theory}{Data}", logy=False, logx=True, ratiorange=[0.,2.],xAxisRange=self.xAxisRanges[iy])

                pad1.cd()
                projs[0].SetMaximum(maxval)
                projs[0].SetMinimum(0.0)
                projs[0].SetLabelSize(0)
                projs[0].SetTitleSize(0)
                leg.Draw()
            
            
            self.histDriver_.stampCMS(pad1, "CMS", self.histDriver_.lumi_)
            self.histDriver_.canvs_.append(c)
            c.Print("fullxs_" + postfix + str(iy) + ".png", "png")
            c.Print("fullxs_" + postfix + str(iy) + ".pdf", "pdf")



    def plotFullUncs( self, hists, postfix="" ):

        canvs = []
        for iy in xrange(1,hists.values()[0].GetNbinsY()+1):
            c = ROOT.TCanvas("cunc" + str(iy) + postfix, "cunc" + str(iy) + postfix)
            self.histDriver_.canvs_.append(c)
            canvs.append(c)

            stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), hists.values()[0].GetTitle() )
            for ihist,hist in enumerate(hists.values()) :

                proj = hist.ProjectionX('proj_' + hist.GetName()+ postfix + str(iy), iy,iy, "e" )
                setStyles( proj, lineWidth=3, lineStyle=self.histDriver_.lineStyles[ihist], lineColor=self.histDriver_.lineColors[ihist] )
                self.histDriver_.hists_.append(proj)
                stack.Add( proj )
                
            stack.Draw("nostack hist")
            stack.SetMinimum(1e-4)
            stack.SetMaximum(1e3)
            self.histDriver_.stacks_.append(stack)
            c.SetLogy()
            c.SetLogx()
            self.histDriver_.stampCMS(c, "CMS")
