#! /usr/bin/env python

import ROOT
import array

class HistDriver :
    def __init__( self, lumi=None ):
        self.lumi_=lumi
        self.hists_ = []  # Keep stuff around until we want them to go out of scope
        self.canvs_ = []
        self.pads_ = []
        self.stacks_ = []
        self.stampCMSVal = ROOT.TLatex()
        self.stampCMSVal.SetNDC()
        self.stampCMSVal.SetTextFont(43)
        self.stampCMSVal.SetTextSize(25)
        self.markerStyles = [20, 21, 22, 23, 33, 34, 24, 25, 26, 32, 28, 29]
        self.lineStyles = [1,2,3,4,5,6,8,9]
        self.lineColors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+3, ROOT.kViolet, ROOT.kMagenta, ROOT.kCyan+2]
        

    def plotFullXS( self, hist, postfix="" ):

        c = ROOT.TCanvas("c" + postfix, "c" + postfix)
        self.canvs_.append(c)
        stack = ROOT.THStack( hist.GetName() + "_stack", hist.GetTitle() )
        for iy in xrange(1,hist.GetNbinsY()+1):
            proj = hist.ProjectionX('proj_' + hist.GetName() + str(iy), iy,iy )
            setStyles( proj, markerStyle=self.markerStyles[iy-1], fillColor=ROOT.kGray, fillStyle=1001 )            
            stack.Add( proj )

        stack.Draw("nostack e2")
        self.stacks_.append(stack)
        self.stampCMS( c, "CMS Preliminary")
        stack.SetMinimum(1e-12)
        stack.SetMaximum(1.0)
        c.SetLogy()
        return stack

        
    def plotFullXSProjections( self, hist, histStat=None, postfix="" ):

        for iy in xrange(1,hist.GetNbinsY()+1):
            c = ROOT.TCanvas("c" + str(iy) + postfix, "c" + str(iy) + postfix)
            self.canvs_.append(c)
            
            proj = hist.ProjectionX('proj_' + hist.GetName() + str(iy), iy,iy, "e" )
            setStyles( proj, markerStyle=self.markerStyles[iy-1], fillColor=ROOT.kGray, fillStyle=1001 )            
            proj.Draw("e2")
            if histStat != None :
                projStat = histStat.ProjectionX('proj_' + histStat.GetName() + str(iy), iy,iy, "e" )
                setStyles( projStat, markerStyle=self.markerStyles[iy-1], fillColor=ROOT.kGray+3, fillStyle=1001 )
                projStat.Draw("e2 same")
            c.SetLogx()
            proj.GetXaxis().SetRangeUser(10,2000)
            proj.SetMinimum(0.0)
            self.stampCMS(c, "CMS Preliminary")
            self.hists_.append(proj)
            if histStat != None : 
                self.hists_.append(projStat)



    def plotFullUncs( self, hists, postfix="" ):

        canvs = []
        for iy in xrange(1,hists.values()[0].GetNbinsY()+1):
            c = ROOT.TCanvas("cunc" + str(iy) + postfix, "cunc" + str(iy) + postfix)
            self.canvs_.append(c)
            canvs.append(c)

            stack = ROOT.THStack( hists.values()[0].GetName() + "_uncstack" + str(iy), hists.values()[0].GetTitle() )
            for ihist,hist in enumerate(hists.values()) :
                        
                proj = hist.ProjectionX('proj_' + hist.GetName() + str(iy), iy,iy, "e" )
                setStyles( proj, lineStyle=self.lineStyles[ihist], lineColor=self.lineColors[ihist] )
                self.hists_.append(proj)
                stack.Add( proj )
                
            stack.Draw("nostack hist")
            self.stacks_.append(stack)
            c.SetLogy()
            c.SetLogx()
            self.stampCMS(c, "CMS Preliminary")
                

    def setupPads(self, canv):
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
        self.canvs_.append(canv)
        self.pads_.append( [pad1,pad2] )
        return [pad1, pad2]

    def plotHistAndRatio( pad1, pad2, hist, nominal, rationame="_ratio", option1="", option2="" ) :
        pad1.cd()
        hist.Draw(option1)
        pad2.cd()
        ratio = hist.Clone( hist.GetName() + rationame )
        ratio.Divide( nominal )
        ratio.Draw(option2)
        self.hists_.append(ratio)



    def stampCMS( self, pad, text, lumi=None ) :
        if lumi == None :
            lumi = self.lumi_
        self.stampCMSVal.DrawLatex(0.2, 0.926, text)
        self.stampCMSVal.DrawLatex(0.62, 0.926, "%3.1f fb^{-1} (13 TeV)" % (lumi) )
    
        
def setStyles( hist,
               lineColor=None, fillColor=None, markerColor=None, 
               lineStyle=None, fillStyle=None, markerStyle=None, 
               lineWidth=None,
               xaxisTitleSize = None, yaxisTitleSize = None,
               xaxisLabelSize = None, yaxisLabelSize = None, ) :
    if lineStyle != None : hist.SetLineStyle(lineStyle)
    if fillStyle != None : hist.SetFillStyle(fillStyle)
    if markerStyle != None : hist.SetMarkerStyle(markerStyle)    
    if lineColor != None : hist.SetLineColor(lineColor)
    if fillColor != None : hist.SetFillColor(fillColor)
    if markerColor != None : hist.SetMarkerColor(markerColor)
    if lineWidth != None : hist.SetLineWidth(lineWidth)
    if xaxisTitleSize != None: hist.GetXaxis().SetTitleSize( xaxisTitleSize )
    if yaxisTitleSize != None: hist.GetYaxis().SetTitleSize( yaxisTitleSize )
    if xaxisLabelSize != None: hist.GetXaxis().SetLabelSize( xaxisLabelSize )
    if yaxisLabelSize != None: hist.GetYaxis().SetLabelSize( yaxisLabelSize )
    

# Turn a histogram into a graph
def getGraph( hist, width=None, minmassbin=None ) :
    x = array.array("d", [] )
    y = array.array("d", [] )
    dx = array.array("d", [] )
    dy = array.array("d", [] )
    if minmassbin == None :
        imin = 1
    else :
        imin = minmassbin
    for ibin in xrange( imin, hist.GetNbinsX() + 1):
        val = hist.GetBinContent(ibin) 
        if val > 0. :
            x.append( hist.GetXaxis().GetBinCenter(ibin) )
            dx.append( hist.GetXaxis().GetBinWidth(ibin) / 2. )
            y.append( val )
            dy.append( hist.GetBinError(ibin) )
    graph =TGraphErrors( len(x), x, y, dx, dy )
    graph.SetName( hist.GetName() + "_graph")
    graph.SetLineColor( hist.GetLineColor() )
    graph.SetLineStyle( hist.GetLineStyle() )
    if width == None :
        graph.SetLineWidth( hist.GetLineWidth() )
    else : 
        graph.SetLineWidth( width )
    graph.SetFillColor( hist.GetFillColor() )
    graph.SetFillStyle( hist.GetFillStyle() )
    return graph

def normalizeHist(hist, normalizeUnity=True, normalizeEachPtBin=False):
    '''
      1. Normalize to unity if desired.
      2. Divide all bins by bin width.
      3. Normalize pt bins to unity if desired.
    '''
    if normalizeUnity and hist.Integral("width") > 0.0 :
        hist.Scale( 1.0 / hist.Integral("width") )
    divideByBinWidthsXY( hist )
    if normalizeEachPtBin :
        normalizeYSlices( hist )

def setToAverage(hist, up, dn ):
    '''
    Set the values of "hist" to the average of the absolute values of "up" and "dn"
    '''
    for ix in xrange(hist.GetNbinsX()+2) :
        for iy in xrange(hist.GetNbinsY()+2):
            value = 0.5 * ( abs( up.GetBinContent(ix,iy) ) + abs(dn.GetBinContent(ix,iy)) )
            hist.SetBinContent(ix,iy, value )




# Smooth histograms :
#   - Loop through bins
#   - Take the median value above and below "this" bin
#   - If the current value is below the median above AND below, replace with average of medians
def smooth( hist, delta = 2, xmin = None, xmax = None, reverse=True, verbose=False) :
    newvalues = {}
    if hist.GetNbinsX() >= 2 * delta :
        if xmin == None :
            xmin = 1
        if xmax == None :
            xmax = hist.GetNbinsX() + 1
        for ibin in xrange(xmin, xmax ) :
            val = hist.GetBinContent( ibin )

            if val == 0.0 :
                continue

            vals = []
            binlo = ibin - delta
            if binlo < 0 : binlo = 0
            binhi = ibin + delta + 1

            if binhi > hist.GetNbinsX()+1 : binhi = hist.GetNbinsX()+1
            for jbin in xrange( binlo, binhi ) :
                vals.append( hist.GetBinContent( jbin ) )

            svals = sorted( vals, reverse=reverse)


            if len( vals ) == 0 :
                median = 0.
            else : 
                median = svals[ len(svals) / 2 ]

            newvalues[ibin] = median



            if verbose: 
                print '-----------'
                for ival in svals :
                    print '%6.2f' % ( ival ),
                print ''
                print median

        for ibin in xrange(xmin, xmax) :
            if ibin in newvalues : 
                hist.SetBinContent( ibin, newvalues[ibin] )



# "Unpinch" histograms :
#   - Average the uncertainties at the "peak" by averaging uncertainties from "peak +- delta"
def unpinch( hist, delta = 2, xval = None ) :
    newxvals = []

    if xval == None :
        xval = hist.GetMaximumBin()
    if hist.GetNbinsX() >= 2 * delta  :
        binlo = max( 0, xval - delta)
        binhi = min( xval + delta, hist.GetNbinsX() )
        avg = 0.0
        navg = 0
        for ibin in xrange(binlo, binhi) :
            val = hist.GetBinContent( ibin )
            err = hist.GetBinError( ibin )
            if val > 0.0 :
                avg += err/val
                navg += 1
        avg = avg / navg
        for ibin in xrange(binlo, binhi) :
            val = hist.GetBinContent( ibin )
            err = hist.GetBinError( ibin )
            if err < avg * val : 
                hist.SetBinError( ibin, avg * val )

def unpinch_vals( hist, delta = 2, xval = None ) :
    newxvals = []

    if xval == None :
        xval = hist.GetMaximumBin()
    if hist.GetNbinsX() >= 2 * delta  :
        binlo = max( 0, xval - delta)
        binhi = min( xval + delta, hist.GetNbinsX() )
        avg = 0.0
        navg = 0
        for ibin in xrange(binlo, binhi) :
            val = hist.GetBinContent( ibin )
            avg += val
            navg += 1
        avg = avg / navg
        for ibin in xrange(binlo, binhi) :
            val = hist.GetBinContent( ibin )
            if (val < 1.0 and val > avg) or (val > 1.0 and val < avg) : 
                hist.SetBinContent( ibin, avg )


def divideByBinWidthsXY( hist ) :
    for ix in xrange(1,hist.GetNbinsX()+1):
        for iy in xrange(1,hist.GetNbinsY()+1):
            prod = hist.GetXaxis().GetBinWidth(ix) * hist.GetYaxis().GetBinWidth(iy)
            if prod > 0.0 :
                hist.SetBinContent(ix,iy, hist.GetBinContent(ix,iy) / prod )
                hist.SetBinError(ix,iy, hist.GetBinError(ix,iy) / prod )
        


def normalizeYSlices( hist ) :
    for iy in xrange(1,hist.GetNbinsY()+1 ) :
        binsum = 0.0
        for ix in xrange(1,hist.GetNbinsX()+1 ) :
            binsum += hist.GetBinContent( ix, iy )
        if binsum > 0.0 : 
            for ix in xrange(1,hist.GetNbinsX()+1 ) :
                hist.SetBinContent( ix, iy, hist.GetBinContent(ix,iy) / binsum )
                hist.SetBinError( ix, iy, hist.GetBinError(ix,iy) / binsum )
            
def normalizeXSlices( hist ) :
    for ix in xrange(1,hist.GetNbinsX()+1 ) :
        binsum = 0.0
        for iy in xrange(1,hist.GetNbinsY()+1 ) :
            binsum += hist.GetBinContent( ix, iy )
        if binsum > 0.0 : 
            for iy in xrange(1,hist.GetNbinsY()+1 ) :
                hist.SetBinContent( ix, iy, hist.GetBinContent(ix,iy) / binsum )
                hist.SetBinError( ix, iy, hist.GetBinError(ix,iy) / binsum )
            
                        
                
def printHist( hist ) :
    for ix in xrange(1,hist.GetNbinsX()+1):
        for iy in xrange(1,hist.GetNbinsY()+1):
            print '%7.2e +- %7.2e' % ( hist.GetBinContent(ix,iy), hist.GetBinError(ix,iy) ),
        print ''
