import csv
from ROOT import *
import array

'''

binning = array.array('d',[0, 1, 5., 10., 20., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000. ])
mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]



ptbins = [200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
fout = TFile('theory_predictions.root', 'RECREATE')
fout.cd()

for j, jbin in enumerate(ptbins):
    #for k in xrange(1,4):
    
    Bincontent = [0., 0.]  # These have to be added because the calculation
    Binerrors = [0., 0.]   # only goes down to 5 GeV but our histograms
    Xvalues = [0., 1.]     # extend down to zero. 
    with open('theory/histogram_NNLL_pt'+str(jbin)+'._beta0._rebinned.dat') as f:
        i = 0
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            i += 1
            if i > 9:
                xvalue =  float(line[0].split(' ')[0])
                central = float(line[1])
                lower = float(line[2])
                upper = float(line[3].split('#')[0])
                unc1 = abs(central - lower)
                unc2 = abs(upper - central)
                unc = (unc1 + unc2) * 0.5
                Bincontent.append( central )
                Binerrors.append( unc)
                Xvalues.append( xvalue )
                print line
                #print 'xval = ', xvalue, ' yval = ', central, ' +- ', unc
                #if k == 3:
                    #Uppervalues = line[k].split("#")
                    #Bincontent.append(float(Uppervalues[0]))
                #else:
                    #Bincontent.append(float(line[k]))
                    

        nextx = Xvalues[ len(Xvalues) - 1 ]
        while nextx <= 2000. :
                Xvalues.append( nextx )
                Bincontent.append( 0 )
                Binerrors.append( 0 )
                nextx += 50.0
        aXvalues = array.array('f', Xvalues)
        hist = TH1F('histSD_'+str(j), 'Mass Distributions', len(Xvalues)-1, aXvalues)
        for ixval in Xvalues[0:len(Xvalues)-1] :
            histbin = hist.GetXaxis().FindBin( ixval )
            hist.SetBinContent( histbin, Bincontent[Xvalues.index(ixval)] )
            hist.SetBinError( histbin, Binerrors[Xvalues.index(ixval)] )
        ourhist = hist.Rebin( len(binning) - 1, hist.GetName() + '_ours', binning )

        #for ibin in xrange(1, ourhist.GetNbinsX()+1):
        #    ourhist.SetBinContent(ibin, ourhist.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
        #    ourhist.SetBinError(ibin, ourhist.GetBinError(ibin) * 1./mbinwidths[ibin-1])
        ourhist.Write()
fout.Close()



##### OLD Marzani et al prediction:

fout = TFile('theory_predictions_marzani.root', 'RECREATE')
fout.cd()
binstart = [2, 51, 100, 149, 198, 247, 296, 345, 394, 443, 492, 541, 590, 639, 688, 737, 786, 835, 884 ]

for j, jbin in enumerate(ptbins):
    i = 0
    Bincontent = []
    Binerrors = []

    with open('theory/matched-ll_lo-cms.res.txt') as f:
        reader = csv.reader(f, delimiter=" ")
        for line in reader:
            print line
            
            if i > (binstart[j]-1) and i < (binstart[j+1]-4):
                central = float(line[3])
                Bincontent.append( central )
                lower = float(line[4])
                upper = float(line[5])
                unc1 = abs(central - lower)
                unc2 = abs(upper - central)
                unc = (unc1 + unc2) * 0.5
                Binerrors.append( unc)
            elif i == (binstart[j+1]-4):
                break
            i += 1

        hist = TH1F('hist_marzani_SD_'+str(j), 'Mass Distributions', len(binning)-1, binning)
        
        for xval in binning[1:len(binning)-1] :
            histbin = hist.GetXaxis().FindBin( xval )
            hist.SetBinContent( histbin, Bincontent[binning.index(xval)-1] )
            hist.SetBinError( histbin, Binerrors[binning.index(xval)-1] )

        hist.Write()

fout.Close()
'''




binning = array.array('d',[0, 1, 5., 10., 20., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000. ])

ptbins = [200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 13000]

fout = TFile('theory_predictions_marzani_newpred.root', 'RECREATE')
fout.cd()

f = open('theory/mmdt-mass-lhc13-NLO+LL-MSS.res')
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
            for massbin in xrange( len(binning)-2 ):
                    
                line = f.readline()
                toks = line.rstrip().split(' ')

                if j == 0 :
                    Bincontent[massbin+1] = float(toks[25])
                    vallo = float(toks[24])
                    valhi = float(toks[26])
                else : 
                    Bincontent[massbin+1] = float(toks[13])
                    vallo = float(toks[12])
                    valhi = float(toks[14])
                baderrors = vallo < 0.
                if (vallo < 0. ) :
                    vallo = 0.
                if ( valhi < 0. ) :
                    valhi = 0.
                BinerrorsLo = abs( Bincontent[massbin+1] - vallo)
                BinerrorsHi = abs( valhi - Bincontent[massbin+1] )
                if baderrors : 
                    Binerrors[massbin+1] = ( BinerrorsLo + BinerrorsHi ) * 0.5
                else :
                    Binerrors[massbin+1] = BinerrorsHi
                ## if Bincontent[massbin+1] < 0.:
                ##     Bincontent[massbin+1] = 0.
                ##     Binerrors[massbin+1] = 0.
                print ' --- %6.0f : %8.3e +- %8.3e' % ( binning[massbin], Bincontent[massbin+1], Binerrors[massbin+1] )

                    

            break




    hist = TH1F('hist_marzani_SD_'+str(j), 'Mass Distributions', len(binning)-1, binning)
    for ibin in xrange(len(binning)) :
        hist.SetBinContent( ibin + 1, Bincontent[ibin])
        hist.SetBinError( ibin + 1, Binerrors[ibin])


    hist.Write()

fout.Close()
