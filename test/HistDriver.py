#! /usr/bin/env python

import ROOT
import array
import math

class StyleDriver :
    def __init__(self, name,
                lineColor=None, fillColor=None, markerColor=None, 
                lineStyle=None, fillStyle=None, markerStyle=None, 
                lineWidth=None):
        self.name        = name
        self.lineColor   = lineColor   
        self.fillColor   = fillColor   
        self.markerColor = markerColor 
        self.lineStyle   = lineStyle   
        self.fillStyle   = fillStyle   
        self.markerStyle = markerStyle 
        self.lineWidth   = lineWidth   
        
class HistDriver :
    def __init__( self, lumi=None, dlumi=None ):
        self.lumi_=lumi
        if dlumi != None :
            self.dlumi2_ = dlumi**2
        else :
            self.dlumi2_ = None
        self.hists_ = []  # Keep stuff around until we want them to go out of scope
        self.canvs_ = []
        self.pads_ = []
        self.stacks_ = []
        self.legs_ = []
        self.stampCMSVal = ROOT.TLatex()
        self.stampCMSVal.SetNDC()
        self.stampCMSVal.SetTextFont(43)
        self.stampCMSVal.SetTextSize(25)
        self.styles = {
            'nom':StyleDriver(name="nom",markerStyle=20,lineStyle=1,lineColor=ROOT.kBlack,fillStyle=1001,fillColor=ROOT.kGray),
            'nomStat':StyleDriver(name="nomStat",markerStyle=20,lineStyle=1,lineColor=ROOT.kBlack,fillStyle=1001,fillColor=ROOT.kGray+2),
            'pythia':StyleDriver(name="pythia",markerStyle=0,lineStyle=2,lineColor=ROOT.kBlack,lineWidth=3),
            'herwig':StyleDriver(name="herwig",markerStyle=0,lineStyle=8,lineColor=ROOT.kMagenta+1,lineWidth=3),
            'powheg':StyleDriver(name="powheg",markerStyle=0,lineStyle=4,lineColor=ROOT.kGreen+2,lineWidth=3),
            'theory1':StyleDriver(name="theory1",markerStyle=0,fillStyle=3004,fillColor=ROOT.kBlue,lineColor=ROOT.kBlue,lineWidth=3),
            'theory2':StyleDriver(name="theory2",markerStyle=0,fillStyle=3005,fillColor=ROOT.kOrange+7,lineColor=ROOT.kOrange+7,lineWidth=3)
            }

        self.titles = {
            'pythia':'PYTHIA8', 'herwig':'HERWIG++', 'powheg':'POWHEG+PYTHIA8', 'theory1':'Frye et al', 'theory2':'Marzani et al'
            }
        self.sysStyles = {'_jer'   :StyleDriver(name="_jer",   lineWidth=3,lineStyle=8,lineColor=ROOT.kRed),
                          '_jec'   :StyleDriver(name="_jec",   lineWidth=3,lineStyle=3,lineColor=ROOT.kRed),
                          '_jmr'   :StyleDriver(name="_jmr",   lineWidth=3,lineStyle=5,lineColor=ROOT.kBlue),
                          '_jms'   :StyleDriver(name="_jms",   lineWidth=3,lineStyle=8,lineColor=ROOT.kBlue),
                          '_pu'    :StyleDriver(name="_pu",    lineWidth=3,lineStyle=7,lineColor=ROOT.kCyan+1),
                          '_lum'   :StyleDriver(name="_lum",   lineWidth=3,lineStyle=4,lineColor=ROOT.kOrange+1),
                          '_pdf'   :StyleDriver(name="_pdf",   lineWidth=3,lineStyle=6,lineColor=ROOT.kMagenta),
                          '_ps'    :StyleDriver(name="_ps",    lineWidth=3,lineStyle=4,lineColor=ROOT.kGreen+2),
                          '_mcStat':StyleDriver(name="_mcStat",lineWidth=3,lineStyle=2,lineColor=ROOT.kBlack),
                          '_totunc':StyleDriver(name="_totunc",lineWidth=3,lineStyle=1,lineColor=ROOT.kBlack, fillStyle=0),
                        }
        for i in xrange(53) :
            self.sysStyles[ '_jecsrc' + str(i) ] = StyleDriver(name="_jecsrc" + str(i), lineWidth=3,lineStyle=3,lineColor=ROOT.kRed)
        self.lineStyles = [3,8,5,9,7,4,6,4,2,1,1,1,1]
        self.lineColors = [ROOT.kRed, ROOT.kRed, ROOT.kBlue, ROOT.kBlue, ROOT.kCyan+1, ROOT.kOrange+1, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack]

        
        
    def setupPads(self, canv):
        canv.cd()
        pad1 = ROOT.TPad('pad' + canv.GetName() + '1', 'pad' + canv.GetName() + '1', 0., 0.3, 1.0, 1.0)
        pad1.SetBottomMargin(0.05)
        pad2 = ROOT.TPad('pad' + canv.GetName() + '2', 'pad' + canv.GetName() + '2', 0., 0.0, 1.0, 0.3)
        pad2.SetTopMargin(0.05)
        pad1.SetLeftMargin(0.15)
        pad2.SetLeftMargin(0.15)
        pad1.SetRightMargin(0.15)
        pad2.SetRightMargin(0.15)
        pad2.SetBottomMargin(0.5)
        pad1.Draw()
        pad2.Draw()
        self.pads_.append([pad1,pad2])
        
        
        self.canvs_.append(canv)
        self.pads_.append( [pad1,pad2] )
        return [pad1, pad2]

    def plotHistAndRatio(self, pad1, pad2, hist, nominal, rationame="_ratio", option1="", option2="", ratiotitle=None, logy=False, logx=False, ratiorange=None, xAxisRange=None ) :

        if xAxisRange != None :
            hist.GetXaxis().SetRangeUser(xAxisRange[0],xAxisRange[1])
            
        pad1.cd()
        hist.GetYaxis().SetTitleOffset(1.2)
        hist.Draw(option1)
        pad1.SetLogy(logy)
        pad1.SetLogx(logx)
        pad2.cd()
        pad2.SetLogx(logx)
        ratio = hist.Clone( hist.GetName() + rationame )
        ratio.SetMarkerStyle(0)
        ratio.GetXaxis().SetTickLength(0.07)
        ratio.GetYaxis().SetNdivisions(2,4,0,False)
        ratio.GetYaxis().SetTitleOffset(1.2)
        ratio.GetXaxis().SetTitleOffset(3.5)
        if logx :
            ratio.GetXaxis().SetNoExponent()
        if ratiotitle != None :
            ratio.SetTitle(ratiotitle)
        ratio.Divide( nominal )
        ratio.Draw(option2)
        if ratiorange != None :
            ratio.SetMinimum( ratiorange[0] )
            ratio.SetMaximum( ratiorange[1] )
        self.hists_.append(ratio)



    def plotGraphAndRatio(self, pad1, pad2, hist, nominal, rationame="_ratio", option1="", option2="", ratiotitle=None, logy=False, logx=False, ratiorange=None, xAxisRange=None ) :

        if xAxisRange != None :
            hist.GetXaxis().SetRangeUser(xAxisRange[0],xAxisRange[1])
            
        ratio = hist.Clone( hist.GetName() + rationame )
        ratio.Divide( nominal )
        ratio.SetMarkerStyle(0)
        ratio.GetXaxis().SetTickLength(0.07)
        ratio.GetYaxis().SetNdivisions(2,4,0,False)
        ratio.GetYaxis().SetTitleOffset(1.2)
        ratio.GetXaxis().SetTitleOffset(3.5)
            
        graph1 = getGraph( hist, minmassbin=hist.GetXaxis().FindBin(xAxisRange[0]) )
        graph2 = getGraph( ratio, minmassbin=hist.GetXaxis().FindBin(xAxisRange[0]) )
        pad1.cd()
        hist.GetYaxis().SetTitleOffset(1.2)
        graph1.Draw(option1)
        pad1.SetLogy(logy)
        pad1.SetLogx(logx)
        pad2.cd()
        pad2.SetLogx(logx)        
        graph2.Draw(option2)
        self.hists_.append(graph1)
        self.hists_.append(graph2)
        return graph1,graph2
    

    def divide1D( self, hist1, hist2 ) :
        for ix in xrange(0, hist1.GetNbinsX()+2) :
            val1 = hist1.GetBinContent(ix)
            err1 = hist1.GetBinError(ix)
            val2 = hist2.GetBinContent(ix)
            err2 = hist2.GetBinError(ix)
            if abs(val2) > 0.0 and abs(val1) > 0.0 :
                hist1.SetBinContent( ix, val1/val2 )
                errtot = math.sqrt( (err1/val1)**2 + (err2/val2)**2)
                hist1.SetBinError( ix, val1/val2 * errtot )
            else :
                hist1.SetBinContent(ix,0.0)
                hist1.SetBinError(ix,0.0)
                

    def addCorrelated1D(self, hist1, hist2 ):
        for ix in xrange(1,hist1.GetNbinsX() ):
            val1 = hist1.GetBinContent(ix)
            val2 = hist2.GetBinContent(ix)
            err1 =  hist1.GetBinError(ix) if abs(val1) > 0 else 0.
            err2 =  hist2.GetBinError(ix) if abs(val2) > 0 else 0.

            
            hist1.SetBinContent( ix, val1 + val2 )
            hist1.SetBinError( ix, err1 + err2 )

    def normalizeHist(self, hist, normalizeUnity=True, divideByBinWidths=True, scalePtBins = False):
        '''
          1. Normalize to unity if desired.
          2. Divide all bins by bin width.
          3. Normalize pt bins to unity if desired.
        '''
        if normalizeUnity and hist.Integral() > 0.0 :
            hist.Scale( 1.0 / hist.Integral() )
            


        ## elif normalizeUnity == False and self.lumi_ > 0.0 :
        ##     #hist.Scale( 1.0 / self.lumi_ )
        ##     for ix in xrange(1,hist.GetNbinsX()+1) :
        ##         for iy in xrange(1,hist.GetNbinsY()+1):
        ##             val = hist.GetBinContent(ix,iy)
        ##             err = hist.GetBinError(ix,iy)
        ##             if val > 0.0 :
        ##                 errtot = math.sqrt( (err/val)**2 + self.dlumi2_ ) * val
        ##                 hist.SetBinError(ix,iy,errtot)
        ## else :
        ##     raise ValueError("Normalizing histogram is not valid.")
        if divideByBinWidths : 
            divideByBinWidthsXY( hist )
        if scalePtBins :
            normalizeYSlices(hist)


    def stampCMS( self, pad, text, lumi=None ) :
        pad.cd()
        if lumi == None :
            lumi = self.lumi_ 
        self.stampCMSVal.DrawLatex(0.15, 0.926, text)
        self.stampCMSVal.DrawLatex(0.64, 0.926, "%3.1f fb^{-1} (13 TeV)" % (lumi / 1e3) )
    


def setStylesClass( hist, istyle ) :
    setStyles(hist, lineColor=istyle.lineColor, fillColor=istyle.fillColor, markerColor=istyle.markerColor, 
               lineStyle=istyle.lineStyle, fillStyle=istyle.fillStyle, markerStyle=istyle.markerStyle, 
               lineWidth=istyle.lineWidth )


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
    graph =ROOT.TGraphErrors( len(x), x, y, dx, dy )
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


def normalizeYSlices(hist):

    for iy in xrange(0,hist.GetNbinsY()+2):
        proj = hist.ProjectionX("proj_" + str(iy), iy, iy, "e")
        if proj.Integral() > 0.0 : 
            proj.Scale(1.0 / proj.Integral('width') )
            for ix in xrange(0, hist.GetNbinsX()+2):
                hist.SetBinContent( ix,iy, proj.GetBinContent(ix,iy) )
                hist.SetBinError( ix,iy, proj.GetBinError(ix,iy) )

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



            #if verbose: 
            #    print '-----------'
            #    for ival in svals :
            #        print '%6.2f' % ( ival ),
            #    print ''
            #    print median

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
        

def printHist( hist, maxx = None, maxy = None ) :
    xmax = hist.GetNbinsX()+1
    if maxx != None :
        xmax = maxx
    ymax = hist.GetNbinsY()+1
    if maxy != None :
        ymax = maxy
    for ix in xrange(1,xmax):
        for iy in xrange(1,ymax):
            print '%7.2e +- %7.2e' % ( hist.GetBinContent(ix,iy), hist.GetBinError(ix,iy) ),
        print ''

        
def printHist1D( hist, maxx = None ) :
    if maxx == None : 
        for ix in xrange(1,hist.GetNbinsX()+1):
            print ' %8.2e' % ( hist.GetBinContent(ix) ),
        print ''
    else : 
        for ix in xrange(1,maxx):
            print ' %8.2e' % ( hist.GetBinContent(ix) ),
        print ''

        
def printHist1DErrs( hist, maxx = None ) :
    if maxx == None : 
        for ix in xrange(1,hist.GetNbinsX()+1):
            print ' %8.2e' % ( hist.GetBinError(ix) ),
        print ''
    else : 
        for ix in xrange(1,maxx):
            print ' %8.2e' % ( hist.GetBinError(ix) ),
        print ''

def ensureAbs(hist):
    for ix in xrange(0,hist.GetNbinsX()+2):
        for iy in xrange(0,hist.GetNbinsY()+2):
            if hist.GetBinContent(ix,iy) < 0.0 :
                hist.SetBinContent(ix,iy, -1*hist.GetBinContent(ix,iy) )
            
