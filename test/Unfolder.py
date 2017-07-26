#! /usr/bin/env python

import ROOT

class Unfolder:
    def __init__(self, inputs = "2DData"):
        # Experimental uncertainties
        self.sysnames = [
            ['_jerup','_jerdn'],
            ['_jecup','_jecdn'],
            ['_jmrup','_jmrdn'],
            ['_puup','_pudn'],
            ]
        self.pdfsysnames = [
            '_pdfup',
            '_pdfdn',
            '_cteq',
            '_mstw',
            ]
        self.files = []
        self.responses = []
        self.responsesSD = []
        
        # Each experimental uncertainty has an "up" and a "down" variation, so
        # the (absolute) uncertainty is (up-down)/2   (factor of 2 will come later)
        for sysup,sysdn in self.sysnames :
            fup = ROOT.TFile( options.inputs + sysup + '.root')
            fdn = ROOT.TFile( options.inputs + sysdn + '.root')
            resup = fup.Get('2d_response' + sysup)
            resupSD = fup.Get('2d_response_softdrop' + sysup)
            resdn = fdn.Get('2d_response' + sysdn)
            resdnSD = fdn.Get('2d_response_softdrop' + sysdn)
            self.files.append([fup,fdn])
            self.responses.append( [resup,resdn] )
            self.responsesSD.append( [resupSD,resdnSD] )


        # Next : PDF and PS uncertainties
        # For the NNPDF uncertainties ("pdfup" and "pdfdn") these are
        # double sided, so (absolute) uncertainty is (up-down)/2 again (factor of 2 will come later). 
        # For the CTEQ and MSTW, the uncertainty is |sys-nom|.
        fpdf = ROOT.TFile("unfoldedpdf.root")
        self.files.append(fpdf)

        
        mpdf = fpdf.Get( '2d_response_pdfup' ).response().Eresponse()
        mpdf  -= fpdf.Get( '2d_response_pdfdn' ).response().Eresponse()
        mmstw = fpdf.Get( '2d_response_mstw' ).response().Eresponse()
        mcteq = fpdf.Get( '2d_response_cteq' ).response().Eresponse()
        mmstw -= mnom
        mcteq -= mnom
        responses.append( mpdf )
        responses.append( mmstw )
        responses.append( mcteq )

        mpdfSD = fpdf.Get( '2d_response_softdrop_pdfup' ).response().Eresponse()
        mpdfSD  -= fpdf.Get( '2d_response_softdrop_pdfdn' ).response().Eresponse()    
        mmstwSD = fpdf.Get( '2d_response_softdrop_mstw' ).response().Eresponse()
        mcteqSD = fpdf.Get( '2d_response_softdrop_cteq' ).response().Eresponse()
        mmstwSD -= mnomSD
        mcteqSD -= mnomSD
        responsesSD.append( mpdfSD )
        responsesSD.append( mmstwSD )
        responsesSD.append( mcteqSD )

