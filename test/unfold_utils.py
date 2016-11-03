#! /usr/bin/env python
import ROOT

def normalize_all_pt_bins( hist ) :
    for jbin in xrange( 0, hist.GetNbinsY() + 1 ) :
        ptslice = hist.Integral( 0, hist.GetNbinsX() + 1, jbin, jbin )
        for ibin in xrange( 0, hist.GetNbinsX() + 1 ) :
            hist.SetBinContent( ibin, jbin, hist.GetBinContent(ibin, jbin) / (ptslice * hist.GetXaxis().GetBinWidth(ibin) ) )
            hist.SetBinError( ibin, jbin, hist.GetBinError(ibin, jbin) / (ptslice * hist.GetXaxis().GetBinWidth(ibin) ) )


