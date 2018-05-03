#!/usr/bin/env python

import glob, yoda, ROOT, subprocess, optparse


parser = optparse.OptionParser(usage=__doc__)
parser.add_option("-i", "--inputs", dest="inputs", metavar="INPUTS", 
                  help="Input files")
options, args = parser.parse_args()

files = glob.glob(options.inputs)

for ifile in files:
    print 'converting ', ifile
    subprocess.call( ["root2yoda", ifile, ifile.replace( "root", "yoda")])

    
