import csv
from ROOT import *
import array



binning = array.array('d',[0, 1, 5., 10., 20., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000. ])

ptbins = [200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 13000]


f = open('mmdt-mass-lhc13-NLO+LL-MSS.res.txt')
for j in xrange(len( ptbins) - 1):
    bin_header = '# pt_' + str(ptbins[j]) + '_' + str(ptbins[j+1])    
    print 'processing pt bin ', bin_header
    jbin = ptbins[j]
    Bincontent = array.array('d',  [0.0] * len(binning) )
    Binerrors = array.array( 'd', [0.0] * len(binning) )


    while True :
        line = f.readline()

        if not line :
            break
    
        if line.rstrip() == bin_header : 
            line = f.readline()
            for massbin in xrange(0,len(binning)-1):
                if massbin == 0 :
                    Bincontent[massbin] = 0.
                    Binerrors[massbin] = 0.
                else : 
                    
                    line = f.readline()
                    toks = line.rstrip().split(' ')
                    ftoks = [ float(itok) for itok in toks]

                    Bincontent[massbin] = float(toks[4])                        
                    BinerrorsLo = abs( Bincontent[massbin] - float(toks[3]))
                    BinerrorsHi = abs( float(toks[5]) - Bincontent[massbin] )
                    Binerrors[massbin] = ( BinerrorsLo + BinerrorsHi ) * 0.5
                    if Bincontent[massbin] < 0.:
                        Bincontent[massbin] = 0.
                        Binerrors[massbin] = 0.

                    print '%6.0f : %9.3e %9.3e %9.3e %9.3e' % ( ftoks[0], ftoks[4], ftoks[7], ftoks[10], ftoks[13] )

                    

            break

