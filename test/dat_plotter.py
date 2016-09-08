import csv
from ROOT import *
import array

i = 0;
binning = array.array('d',[ 0., 1., 5., 10., 20., 40., 60., 80., 100., 150., 200., 250., 300., 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 850., 900., 950., 1000., 1050., 1100., 1150., 1200., 1250., 1300., 1350., 1400., 1450., 1500., 1550., 1600., 1650., 1700., 1750., 1800., 1850., 1900., 1950., 2000. ])
mlen = len( binning ) - 1

ptbins = [200, 260, 350, 460, 550, 650, 760, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]

fout = TFile('theory_predictions.root', 'RECREATE')
fout.cd()



for j, jbin in enumerate(ptbins):
    for k in xrange(1,4):
        hist = TH1F('histSD'+str(k)+'_'+str(j), 'Mass Distributions', mlen, binning)
        Bincontent = []
        with open('histogram_NNLL_pt'+str(jbin)+'._beta0._norm.dat') as f:

            reader = csv.reader(f, delimiter="\t")
            for line in reader:
                i += 1
                if i > 6:
                    if k == 3:
                        Uppervalues = line[k].split("#")
                        Bincontent.append(float(Uppervalues[0]))
                    else:
                        Bincontent.append(float(line[k]))
        i = 0
        
        for m in xrange(1,201):
            Bincontent.append(0.0)
        hist.Fill(0., 0.0)
        hist.Fill(1., 0.0)
        hist.Fill(5., float(Bincontent[0]))
        hist.Fill(10, float( Bincontent[1]+Bincontent[2]))
        hist.Fill(20., float( Bincontent[3]+Bincontent[4]+Bincontent[5]+Bincontent[6] ))
        hist.Fill(40., float( Bincontent[7]+Bincontent[8]+Bincontent[9]+Bincontent[10] ))
        hist.Fill(60., float( Bincontent[11]+Bincontent[12]+Bincontent[13]+Bincontent[14] ))
        hist.Fill(80., float( Bincontent[15]+Bincontent[16]+Bincontent[17]+Bincontent[18] ))
        hist.Fill(100., float( Bincontent[19]+Bincontent[20]+Bincontent[21]+Bincontent[22]+Bincontent[23]+Bincontent[24]+Bincontent[25]+Bincontent[26]+Bincontent[27]+Bincontent[28] ))
        hist.Fill(150., float( Bincontent[29]+Bincontent[30]+Bincontent[31]+Bincontent[32]+Bincontent[33]+Bincontent[34]+Bincontent[35]+Bincontent[36]+Bincontent[37]+Bincontent[38] ))
        hist.Fill(200., float( Bincontent[39]+Bincontent[40]+Bincontent[41]+Bincontent[42]+Bincontent[43]+Bincontent[44]+Bincontent[45]+Bincontent[46]+Bincontent[47]+Bincontent[48] ))
        hist.Fill(250., float( Bincontent[49]+Bincontent[50]+Bincontent[51]+Bincontent[52]+Bincontent[53]+Bincontent[54]+Bincontent[55]+Bincontent[56]+Bincontent[57]+Bincontent[58] ))
        hist.Fill(300., float( Bincontent[59]+Bincontent[60]+Bincontent[61]+Bincontent[62]+Bincontent[63]+Bincontent[64]+Bincontent[65]+Bincontent[66]+Bincontent[67]+Bincontent[68] ))
        hist.Fill(350., float( Bincontent[69]+Bincontent[70]+Bincontent[71]+Bincontent[72]+Bincontent[73]+Bincontent[74]+Bincontent[75]+Bincontent[76]+Bincontent[77]+Bincontent[78] ))
        hist.Fill(400., float( Bincontent[79]+Bincontent[80]+Bincontent[81]+Bincontent[82]+Bincontent[83]+Bincontent[84]+Bincontent[85]+Bincontent[86]+Bincontent[87]+Bincontent[88] ))
        hist.Fill(450., float( Bincontent[89]+Bincontent[90]+Bincontent[91]+Bincontent[92]+Bincontent[93]+Bincontent[94]+Bincontent[95]+Bincontent[96]+Bincontent[97]+Bincontent[98] ))
        hist.Fill(500., float( Bincontent[99]+Bincontent[100]+Bincontent[101]+Bincontent[102]+Bincontent[103]+Bincontent[104]+Bincontent[105]+Bincontent[106]+Bincontent[107]+Bincontent[108] ))
        hist.Fill(550., float( Bincontent[109]+Bincontent[110]+Bincontent[111]+Bincontent[112]+Bincontent[113]+Bincontent[114]+Bincontent[115]+Bincontent[116]+Bincontent[117]+Bincontent[118] ))
        hist.Fill(600., float( Bincontent[119]+Bincontent[120]+Bincontent[121]+Bincontent[122]+Bincontent[123]+Bincontent[124]+Bincontent[125]+Bincontent[126]+Bincontent[127]+Bincontent[128] ))
        hist.Fill(650., float( Bincontent[129]+Bincontent[130]+Bincontent[131]+Bincontent[132]+Bincontent[133]+Bincontent[134]+Bincontent[135]+Bincontent[136]+Bincontent[137]+Bincontent[138] ))
        hist.Fill(700., float( Bincontent[139]+Bincontent[140]+Bincontent[141]+Bincontent[142]+Bincontent[143]+Bincontent[144]+Bincontent[145]+Bincontent[146]+Bincontent[147]+Bincontent[148] ))
        hist.Fill(750., float( Bincontent[149]+Bincontent[150]+Bincontent[151]+Bincontent[152]+Bincontent[153]+Bincontent[154]+Bincontent[155]+Bincontent[156]+Bincontent[157]+Bincontent[158] ))
        hist.Fill(800., float( Bincontent[159]+Bincontent[160]+Bincontent[161]+Bincontent[162]+Bincontent[163]+Bincontent[164]+Bincontent[165]+Bincontent[166]+Bincontent[167]+Bincontent[168] ))
        hist.Write()

fout.Close()







