#!/usr/bin/env python

import glob
import string
import shutil
import ROOT

def main():

    from optparse import OptionParser

    parser = OptionParser()


    parser.add_option('--files', type='string', action='store',
                          dest='files',
                          default = None,
                          help='Input files to glob')


    parser.add_option('--xmin', type='float', action='store',
                  dest='xmin',
                  default = None,
                  help='Min x value')

    parser.add_option('--xmax', type='float', action='store',
                  dest='xmax',
                  default = None,
                  help='Max x value')

    
    (options, args) = parser.parse_args()
    argv = []

    infiles = glob.glob(options.files)

    for i,infile in enumerate(infiles):
        
        tfile = ROOT.TFile( infile )
        name = infile.replace( "raw", "zoomed")
        ofile = ROOT.TFile( name, "RECREATE")
        objs = tfile.GetListOfKeys()

        for iobj,obj in enumerate(objs):
            h = obj.ReadObj()
            if "TH1" in h.ClassName():
                for ix in xrange(0, h.GetXaxis().FindBin(options.xmin) ):
                    h.SetBinContent(ix,0.0)
                    h.SetBinError(ix,0.0)
                for ix in xrange( h.GetXaxis().FindBin(options.xmax), h.GetNbinsX()+1):
                    h.SetBinContent(ix,0.0)
                    h.SetBinError(ix,0.0)                    
                h.Write()
        ofile.Close()
        tfile.Close()
    
if __name__ == "__main__":    
    main()
    
