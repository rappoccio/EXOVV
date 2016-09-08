import csv
from ROOT import *
import array


binning = array.array('d',[ 0., 1., 5., 10., 20., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000. ])


ptbins = [200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]

fout = TFile('theory_predictions.root', 'RECREATE')
fout.cd()

for j, jbin in enumerate(ptbins):
    #for k in xrange(1,4):
    
    Bincontent = []
    Binerrors = []
    Xvalues = []
    with open('histogram_NNLL_pt'+str(jbin)+'._beta0._norm.dat') as f:
        i = 0
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            i += 1
            if i > 6:
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
                    

        Xvalues.append(2000)
        aXvalues = array.array('f', Xvalues)
        hist = TH1F('histSD_'+str(j), 'Mass Distributions', len(Xvalues)-1, aXvalues)
        for ixval in Xvalues[0:len(Xvalues)-1] :
            histbin = hist.GetXaxis().FindBin( ixval )
            hist.SetBinContent( histbin, Bincontent[Xvalues.index(ixval)] )
            hist.SetBinError( histbin, Binerrors[Xvalues.index(ixval)] )
        ourhist = hist.Rebin( len(binning) - 1, hist.GetName() + '_ours', binning )
        ourhist.Write()

fout.Close()







