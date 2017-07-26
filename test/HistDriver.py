#! /usr/bin/env python

import ROOT

class HistDriver :
    def __init__( self ):
        self.hists_ = []  # Keep stuff around until we want them to go out of scope
        self.canvs_ = []
        self.pads_ = []

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
