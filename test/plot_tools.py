import ROOT
ROOT.gSystem.Load("../libRooUnfold")
from ROOT import TCanvas, TLegend, THStack, gRandom, TH1, TH1D, cout, TGraphErrors
from math import sqrt
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--oneband', action='store_true',
                  default = False,
                  dest='oneband',
                  help='one band plots')


parser.add_option('--isSoftDrop', action='store_true',
                  default = False,
                  dest='isSoftDrop',
                  help='theory curves on plots')

parser.add_option('--logy', action='store_true',
                  default = False,
                  dest='logy',
                  help='plots in log y')

parser.add_option('--extension', action ='store', type = 'string',
                 default ='',
                 dest='extension',
                 help='Runs jec, correct options are _jecup : _jecdn : _jerup : _jerdn : _jmrup : _jmrdn : _jmrnom or nothing at all to get the nominal')

parser.add_option('--unrestrictedChi2', action='store_true',
                  default = False,
                  dest='unrestrictedChi2',
                  help='If true, do not restrict range in chi2 calculation')


(options, args) = parser.parse_args()

def get_pt_bin_vals() :
    return array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900, 1000, 1100, 1200, 1300, 13000.])


def minmassbin_ungroomed(ibin) :
    return 5

def minmassbin_groomed(ibin) :
    ptbins_here = get_pt_bin_vals()
    if ptbins_here[ibin] < 550:
        return 2
    elif ptbins_here[ibin] < 900:
        return 3
    else :
        return 4

def add_quadrature( a ):
    sumit = 0
    for ia in a: sumit += ia**2
    return sqrt( sumit )


def zero_hist_bins( bin1, bin2, hists ):
    for hist in hists:
        for ibin in xrange(bin1,bin2) :
            hist.SetBinContent(ibin, 0.0)
        hist.GetXaxis().SetRange(bin2,hist.GetNbinsX()+1)

def get_ptbins_std():
    return ['200-260 GeV #times 10^{0}','260-350 GeV #times 10^{1}','350-460 GeV #times 10^{2}','460-550 GeV #times 10^{3}','550-650 GeV #times 10^{4}','650-760 GeV #times 10^{5}', '760-900 GeV #times 10^{6}', '900-1000 GeV #times 10^{7}', '1000-1100 GeV #times 10^{8}','1100-1200 GeV #times 10^{9}',
    '1200-1300 GeV #times 10^{10}', '> 1300 GeV']


if options.unrestrictedChi2 :    
    def expected_agreement():
        return [[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000],[0,13000] ]
else :
    def expected_agreement():
        return [[20,50], [20,70], [20,100], [20,100], [30,100], [40,100], [40,200], [40, 200], [50,300], [50, 300], [50,300], [50,300] ]


    
def get_markers() :
    return [ 20, 21, 22, 23, 33, 34, 24, 25, 26, 32, 28  ]

def get_ptbins():
    return ['#bf{200 < p_{T} < 260 GeV}','#bf{260 < p_{T} < 350 GeV}','#bf{350 < p_{T} < 460 GeV}','#bf{460 < p_{T} < 550 GeV}','#bf{550 < p_{T} < 650 GeV}','#bf{650 < p_{T} < 760 GeV}', '#bf{760 < p_{T} < 900 GeV}', '#bf{900 < p_{T} < 1000 GeV}', '#bf{1000 < p_{T} < 1100 GeV}','#bf{1100 < p_{T} < 1200 GeV}',
    '#bf{1200 < p_{T} < 1300 GeV}', '#bf{p_{T} > 1300 GeV}']


import array
# Turn a histogram into a graph
def getGraph( hist, width=None ) :
    x = array.array("d", [] )
    y = array.array("d", [] )
    dx = array.array("d", [] )
    dy = array.array("d", [] )
    for ibin in xrange( 1, hist.GetNbinsX() + 1):
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
                

            

def plotter(canvas_list, pads_list, data_list, MC_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, puup_list, pudn_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, latex_list, latexpt_list, ptbins_dict, softdrop= "", keephists=[], jackknifeRMS=False, isData = False):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100.]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    theoryfile = ROOT.TFile("theory_predictions.root")
    theorylist = []
    theoryfile2 = ROOT.TFile("theory_predictions_marzani_newpred.root")
    theorylist2 = []
    chi2_pythia = []
    chi2_herwig = []
    chi2_marzani = []
    chi2_harvard = []

    graphs = []

    herwig_genfile = ROOT.TFile("PS_hists.root")
    herwig_genlist = []
    herwig_genlistSD = []
    for h in xrange(0, 19):
        herwig_genlist.append(herwig_genfile.Get("herwig_gen"+str(h)))
        herwig_genlistSD.append(herwig_genfile.Get("herwig_gen_softdrop"+str(h)))
    
    powhegfile = ROOT.TFile("CMS_SMP_16_010.root")
    powheglist = []
    powheglistSD = []
    for h in [1,2,3,4,5,6,7,8,9]:
        powheglist.append( powhegfile.Get("CMS_SMP_16_010/d0"+str(h)+"-x01-y01"))
    for h in [10,11]:
        powheglist.append( powhegfile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))
    for h in [12,13,14,15,16,17,18,19,20,21,22]:
        powheglistSD.append( powhegfile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))
    
    for h in xrange(0, 12):
        theorylist.append( theoryfile.Get("histSD_"+str(h)+"_ours"))
        theorylist2.append( theoryfile2.Get("hist_marzani_SD_"+str(h)))

    for i, canv in enumerate(canvas_list):
        pads_list[i][0].cd()
        #pads_list[i][0].SetLogy()
        pads_list[i][0].SetLogx()
        if options.logy:
            pads_list[i][0].SetLogy()
        data_list[i].UseCurrentStyle()
        MC_list[i].UseCurrentStyle()
        data_list[i].Scale(scales[i])
        MC_list[i].Scale(scales[i])
        ########################################################################################## Get JER and JES Hists
        hRMS = data_list[i]
        nom = jernom_list[i]
        jesUP  = jecup_list[i]
        jeOWN = jecdn_list[i]
        jerUP  = jerup_list[i]
        jerDOWN = jerdn_list[i]
        puUP  = puup_list[i]
        puDOWN = pudn_list[i]
        ########################################################################################## Get JMR hists
        jmrup = jmrup_list[i]
        jmrdn = jmrdn_list[i]
        jmrnom = jmrnom_list[i]
        ########################################################################################## Scale the hists for Pt bins
        jmrup.Scale(scales[i])
        jmrdn.Scale(scales[i])
        jmrnom.Scale(scales[i])
        jesUP.Scale(scales[i])
        jeOWN.Scale(scales[i])
        jerUP.Scale(scales[i])
        jerDOWN.Scale(scales[i])
        puUP.Scale(scales[i])
        puDOWN.Scale(scales[i])
        nom.Scale(scales[i])
        


        for ibin in xrange(1, hRMS.GetNbinsX()):
            hRMS.SetBinContent(ibin, hRMS.GetBinContent(ibin) * 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, hRMS.GetBinError(ibin) * 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, add_quadrature( [hRMS.GetBinError(ibin), ((jackknifeRMS[i][ibin-1])*scales[i]*(1./mbinwidths[ibin-1]) ) ]) )
        hReco = hRMS.Clone()
        ########################################################################################## Scale the hists for mass bins
        for ibin in xrange(1, hReco.GetNbinsX()):
            jmrup.SetBinContent(ibin, jmrup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrdn.SetBinContent(ibin, jmrdn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrnom.SetBinContent(ibin, jmrnom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

            jesUP.SetBinContent(ibin, jesUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jeOWN.SetBinContent(ibin, jeOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerUP.SetBinContent(ibin, jerUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerDOWN.SetBinContent(ibin, jerDOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            puUP.SetBinContent(ibin, puUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            puDOWN.SetBinContent(ibin, puDOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])            
            nom.SetBinContent(ibin, nom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            MC_list[i].SetBinContent(ibin, MC_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            
            herwig_genlist[i].SetBinContent(ibin, herwig_genlist[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            herwig_genlistSD[i].SetBinContent(ibin, herwig_genlistSD[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            if i < 11:
                powheglist[i].SetBinContent(ibin, powheglist[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
                powheglistSD[i].SetBinContent(ibin, powheglistSD[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
        ########################################################################################## Add JER and JES Uncertainties
        for ibin in xrange(1,hReco.GetNbinsX()):
            val = float(hReco.GetBinContent(ibin))
            err1 = float(hReco.GetBinError(ibin))
            upjes = float(abs(jesUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjes = float(abs(nom.GetBinContent(ibin) - jeOWN.GetBinContent(ibin)))
            sys = float(((upjes + downjes)/2.))
            upjer = float(abs(jerUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjer = float(abs(nom.GetBinContent(ibin) - jerDOWN.GetBinContent(ibin)))
            sys2 = float(((upjer + downjer )/2.))
            err = add_quadrature( [sys, sys2, err1] )
            hReco.SetBinError(ibin, err)
        ####################################################################################### Add Jet Mass Resolution Band
        hRecoJMR = hReco.Clone()
        for ibin in xrange(1, hRecoJMR.GetNbinsX()):
            val = float(hRecoJMR.GetBinContent(ibin))
            err1 = float(hRecoJMR.GetBinError(ibin))
            upjmr = float(abs(jmrup.GetBinContent(ibin) - jmrnom.GetBinContent(ibin)))
            downjmr = float(abs(jmrnom.GetBinContent(ibin) - jmrdn.GetBinContent(ibin)))
            sys = float(((upjmr + downjmr)/2.))
            err = add_quadrature( [err1 , sys] )
            hRecoJMR.SetBinError(ibin, err)


        ####################################################################################### Add Jet Mass Resolution Band
        hRecoPU = hRecoJMR.Clone()
        for ibin in xrange(1, hRecoPU.GetNbinsX()):
            val = float(hRecoPU.GetBinContent(ibin))
            err1 = float(hRecoPU.GetBinError(ibin))
            uppu = float(abs(puup.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downpu = float(abs(nom.GetBinContent(ibin) - pudn.GetBinContent(ibin)))
            sys = float(((uppu + downpu)/2.))
            err = add_quadrature( [err1 , sys] )
            hRecoPU.SetBinError(ibin, err)
            
        ######################################################################################## Add Parton Shower Uncertainties
        hRecoCopy = hRecoPU.Clone()
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            temp = hRecoCopy.GetBinError(ibin)
            hRecoCopy.SetBinError(ibin, add_quadrature( [temp , (psdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1]) ]) )            
        ######################################################################################## Add PDF Uncertainties
        hRecoPDF = hRecoCopy.Clone()
        for ibin in xrange(1, hRecoPDF.GetNbinsX()):
            temp = hRecoPDF.GetBinError(ibin)
            hRecoPDF.SetBinError(ibin, add_quadrature( [temp , (pdfdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1] )] ))

        ####################################################################################### PDF Drawn Here
        #hRecoPDF.SetTitle(";;#frac{1}{d#sigma/dp_{T}} #frac{d^{2} #sigma}{dm dp_{T} } (#frac{1}{GeV})")
        hRecoPDF.SetTitle(";;Normalized cross section")
        hRecoPDF.GetYaxis().SetTitleSize(30)
        hRecoPDF.GetYaxis().SetTitleOffset(1.3)
        hRecoPDF.GetYaxis().SetLabelOffset(0.0001)
        hRecoPDF.GetYaxis().SetLabelSize(28)
        hRecoPDF.SetMarkerStyle(20)
        hRecoPDF.SetFillColor(ROOT.kOrange)
        hRecoPDF.Scale(1.0/hRecoPDF.Integral("width"))
        if i == 11:
            hRecoPDF.GetXaxis().SetRange(minmassbin,2000,"X")
        elif i > 11 and i < 18:
            hRecoPDF.GetXaxis().SetRange(minmassbin,1200, "X")
        elif i > 7 and i < 11:
            hRecoPDF.GetXaxis().SetRange(minmassbin,900, "X")
        elif i > 3 and i < 8:
            hRecoPDF.GetXaxis().SetRange(minmassbin,600, "X")
        elif i < 4:
            hRecoPDF.GetXaxis().SetRange(minmassbin,400,"X")
        hRecoPDF.Draw("E2 ][")
        hRecoBarePdf = hRecoPDF.Clone()
        hRecoBarePdf.SetName( hRecoPDF.GetName() + "_bare" )
        for ibin in xrange( hRecoBarePdf.GetXaxis().GetNbins() ) :
            hRecoBarePdf.SetBinError( ibin, 0.000000000001 )
        hRecoBarePdf.SetMarkerStyle(20)
#hRecoBarePdf.SetLineColor( hStat.GetLineColor() )
        hRecoBarePdf.SetFillStyle(0)
        hRecoBarePdf.Draw("e x0 ][ same")
        hRecoPDF.GetXaxis().SetTickLength(0.05)
        #hRecoPDF.Draw("E same")
        ####################################################################################### PS Drawn Here
        #hRecoCopy.SetTitle(";;#frac{1}{d#sigma/dp_{T}} #frac{d^{2} #sigma}{dm dp_{T} } (#frac{1}{GeV})")
        hRecoCopy.SetTitle(";;Normalized cross section")
        hRecoCopy.GetYaxis().SetTitleSize(30)
        hRecoCopy.GetYaxis().SetTitleOffset(1.3)
        hRecoCopy.GetYaxis().SetLabelOffset(0.0001)
        hRecoCopy.GetYaxis().SetLabelSize(28)
        hRecoCopy.SetMarkerStyle(20)
        hRecoCopy.Scale(1.0/hRecoCopy.Integral("width"))
        hRecoCopy.SetFillColor(ROOT.kAzure+2)
        hRecoCopy.Draw(" E2 ][ same")
        ####################################################################################### JMR Drawn Here
        hRecoJMR.SetTitle(";;#frac{1}{d#sigma/dp_{T}} #frac{d^{2} #sigma}{dm dp_{T} } (#frac{1}{GeV})")
        hRecoJMR.SetTitle(";;Normalized cross section")
        hRecoJMR.GetYaxis().SetTitleSize(30)
        hRecoJMR.GetYaxis().SetTitleOffset(1.3)
        hRecoJMR.GetYaxis().SetLabelOffset(0.0001)
        hRecoJMR.GetYaxis().SetLabelSize(28)
        hRecoJMR.SetMarkerStyle(20)
        hRecoJMR.Scale(1.0/hRecoJMR.Integral("width"))
        hRecoJMR.SetFillColor(ROOT.kGreen)
        hRecoJMR.Draw("E2 ][ same")    
        ####################################################################################### JES and JER Drawn Here
        hReco.SetTitle(";;#frac{1}{d#sigma/dp_{T}} #frac{d^{2} #sigma}{dm dp_{T} } (#frac{1}{GeV})")
        hReco.SetTitle(";;Normalized cross section")
        hReco.GetYaxis().SetTitleSize(30)
        hReco.GetYaxis().SetTitleOffset(1.3)
        hReco.GetYaxis().SetLabelOffset(0.0001)
        hReco.GetYaxis().SetLabelSize(28)
        hReco.SetMarkerStyle(20)
        hReco.SetFillColor(ROOT.kYellow)
        hReco.Scale(1.0/hReco.Integral("width"))
        hReco.SetAxisRange( 1e-5, 1, 'Y')
        hReco.Draw("][ same")

        ####################################################################################### PU Drawn Here
        hRecoPU.SetTitle(";;#frac{1}{d#sigma/dp_{T}} #frac{d^{2} #sigma}{dm dp_{T} } (#frac{1}{GeV})")
        hRecoPU.SetTitle(";;Normalized cross section")
        hRecoPU.GetYaxis().SetTitleSize(30)
        hRecoPU.GetYaxis().SetTitleOffset(1.3)
        hRecoPU.GetYaxis().SetLabelOffset(0.0001)
        hRecoPU.GetYaxis().SetLabelSize(28)
        hRecoPU.SetMarkerStyle(20)
        hRecoPU.Scale(1.0/hRecoPU.Integral("width"))
        hRecoPU.SetFillColor(ROOT.kGreen)
        hRecoPU.Draw("E2 ][ same") 
        
        keephists.append([hReco, hRecoPDF])
        ####################################################################################### Stat Drawn Here
        hRMS.SetTitle(";;Normalized cross section")
        hRMS.GetYaxis().SetTitleSize(30)
        hRMS.GetYaxis().SetTitleOffset(1.3)
        hRMS.GetYaxis().SetLabelOffset(0.0001)
        hRMS.GetYaxis().SetLabelSize(28)
        hRMS.SetMarkerStyle(20)
        hRMS.SetFillColor(ROOT.kMagenta + 2)
        hRMS.Scale(1.0/hRMS.Integral("width"))
        hRMS.SetAxisRange( 1e-5, 1, 'Y')
        hRMS.Draw("E2 ][ same")
        hRMS.Draw(" E ][ same")
        keephists.append(hRMS)
        
        ####################################################################################### Gen Drawn Here
        MC_list[i].SetLineColor(1)
        MC_list[i].SetLineStyle(2)
        MC_list[i].SetLineWidth(3)
        MC_list[i].Scale(1.0/MC_list[i].Integral("width"))
        MC_list[i].Draw( "hist ][ SAME" )
    
        ####################################################################################### Latex Drawn Here

        ####################################################################################### Legends Filled
        legends_list[i].AddEntry(hRecoJMR, 'JMR', 'f')
        legends_list[i].AddEntry(hRecoPDF, 'PDF', 'f')
        legends_list[i].AddEntry(hRecoPU, 'PU', 'f')
        legends_list[i].AddEntry(hRecoCopy, 'Parton Shower', 'f')
        legends_list[i].AddEntry(hReco, 'JES+JER', 'f')
        legends_list[i].AddEntry(hRMS, 'Stat', 'f')
        legends_list[i].AddEntry(MC_list[i], 'Pythia8', 'l')        
        #legends_list[i].Draw()
        herwig_gen = None
        if options.isSoftDrop:
            herwig_gen = herwig_genlistSD[i]
        else:
            herwig_gen = herwig_genlist[i]
        herwig_gen.Scale(1.0/herwig_gen.Integral("width"))
        herwig_gen.SetLineStyle(8)
        herwig_gen.SetLineColor(ROOT.kMagenta + 1)
        herwig_gen.SetLineWidth(3)
        herwig_gen.Draw("hist ][ same")
        legends_list[i].AddEntry(herwig_gen, "HERWIG++", 'l')
        herwigCopy = herwig_gen.Clone()
        herwigCopy.SetName( herwigCopy.GetName() + "_copy")

        powheg = None
        if i < 12:
            if options.isSoftDrop:
                powheg = powheglistSD[i]
            else:
                powheg = powheglist[i]
            powheg.Scale(1.0/powheg.Integral("width"))
            powheg.SetLineStyle(4)
            powheg.SetLineColor(ROOT.kGreen + 2)
            powheg.SetLineWidth(3)
            powheg.Draw("hist same")
            legends_list[i].AddEntry(powheg, "POWHEG + PYTHIA8", 'l')
            #legends_list[i].Draw("same")
            powhegcopy = powheg.Clone()
            powhegcopy.SetName( powheg.GetName()+"_copy")
            powhegcopy.SetLineStyle(4)
            powhegcopy.SetLineColor(ROOT.kGreen + 2)
            powhegcopy.SetLineWidth(3)            


        if i < 12 and options.isSoftDrop and isData:
            theory = theorylist[i]
            theory.Scale(1.0/theory.Integral("width"))
            #theory.Scale(1.0/(20.*theory.GetBinContent(7)))
            ratio_bin = float(hReco.GetBinContent( hReco.GetXaxis().FindBin(50.))/theory.GetBinContent( theory.GetXaxis().FindBin(50.)))
            theory.Scale(ratio_bin)
            #theory.Scale(scales[i])
            theory.SetFillStyle(3254)
            theory.SetFillColor(ROOT.kBlue)            
            #theory.SetAxisRange(1e-5, 1, "Y")
            theory.Draw("C E5 ][ same")            
            theorydumb = theory.Clone(theory.GetName() + "_dumb")
            theorydumb.SetFillStyle(0)
            theorydumb.SetLineWidth(3)
            theorydumb.Draw("C hist ][ same")
            theorydumb.GetXaxis().SetRangeUser(5, 100000)
            legends_list[i].AddEntry(theory, "Frye et al", 'f')
            #legends_list[i].AddEntry(theory, "Frye et al", 'l')
            #legends_list[i].Draw("same")
            
            theory2 = theorylist2[i]
            ratio_bin2 = float(hReco.GetBinContent( hReco.GetXaxis().FindBin(50.))/theory2.GetBinContent( theory2.GetXaxis().FindBin(50.)))
            #theory2.Scale(ratio_bin2)
            #theory2.Scale(1.0/theory2.Integral("width"))
            #ratio_bin2 = float(hRecoPDF.GetBinContent(7)/theory2.GetBinContent(7))
            #theory2.Scale(ratio_bin2)
            #theory2.Scale(1.0/hRecoPDF.Integral("width"))
            theory2.SetFillStyle(3245)
            theory2.SetFillColor(ROOT.kOrange+7)            
            theory2.Draw("hist ][ same")
            theory2dumb = theory2.Clone(theory2.GetName() + "_dumb")
            theory2dumb.SetLineWidth(3)
            theory2dumb.SetFillStyle(0)
            theory2dumb.Draw("C hist ][ same")
            legends_list[i].AddEntry(theory2, "Marzani et al", 'f')
        hRecoPDF.Draw("][ same")
        legends_list[i].Draw()
        latex_list[i].DrawLatex(0.2, 0.926, "CMS Preliminary")
        latex_list[i].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
            #if options.isSoftDrop and isData:
#latexpt_list[i].DrawLatex(0.6, 0.820, ptbins_dict[i])
        if options.logy:
            #if options.isSoftDrop and i > 15:
            #latexpt_list[i].DrawLatex(0.33, 0.490, ptbins_dict[i])
#elif options.isSoftDrop:
#latexpt_list[i].DrawLatex(0.38, 0.490, ptbins_dict[i])
#else:
            latexpt_list[i].DrawLatex(0.60, 0.830, ptbins_dict[i])
        else:
            if options.isSoftDrop:
                latexpt_list[i].DrawLatex(0.60, 0.830, ptbins_dict[i])
            else:
                latexpt_list[i].DrawLatex(0.22, 0.830, ptbins_dict[i])
        ####################################################################################### Hists Cloned and formatted for ratios
        trueCopy = MC_list[i].Clone()
        trueCopy.SetName( trueCopy.GetName() + "_copy")

        if i < 11 and options.isSoftDrop and isData:
            theorycopy = theory.Clone()
            theorycopy.SetName( theory.GetName() + "_copy" )
            theory2copy = theory2.Clone()
            theory2copy.SetName( theory2.GetName() + "_copy" )
        
        datcopy = hReco.Clone()
        datcopy.SetName( datcopy.GetName() + "_copy" )
        datcopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datcopy.GetYaxis().SetTitleOffset(1.3)
        datcopy.GetYaxis().SetTitleSize(30)
        datcopy.SetMarkerStyle(0)
        # this stuff here is parton shower, bad name, ------------------------------------------> NEEDS REFACTORING
        datcopycopy = hRecoCopy.Clone()
        datcopycopy.SetName(hRecoCopy.GetName()+"_copyofcopy")
        datcopycopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datcopycopy.GetYaxis().SetTitleOffset(1.3)
        datcopycopy.GetYaxis().SetLabelOffset(0.0001)
        datcopycopy.GetYaxis().SetTitleSize(30)
        datcopycopy.SetMarkerStyle(0)
        
        datPDF = hRecoPDF.Clone()
        datPDF.SetName(hRecoPDF.GetName()+"_pdfcopy")
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPDF.GetYaxis().SetTitleOffset(1.3)
        datPDF.GetYaxis().SetLabelOffset(0.0001)
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.SetMarkerStyle(0)

        datPU = hRecoPU.Clone()
        datPU.SetName(hRecoPU.GetName()+"_pucopy")
        datPU.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPU.GetYaxis().SetTitleOffset(1.3)
        datPU.GetYaxis().SetLabelOffset(0.0001)
        datPU.GetYaxis().SetTitleSize(30)
        datPU.SetMarkerStyle(0)

                
        datJMR = hRecoJMR.Clone()
        datJMR.SetName(hRecoJMR.GetName()+"_jmrcopy")
        datJMR.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datJMR.GetYaxis().SetTitleOffset(1.3)
        datJMR.GetYaxis().SetLabelOffset(0.0001)
        datJMR.GetYaxis().SetTitleSize(30)
        datJMR.SetMarkerStyle(0)

        datRMS = hRMS.Clone()
        datRMS.SetName(hRecoJMR.GetName()+"_jmrcopy")
        datRMS.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datRMS.GetYaxis().SetTitleOffset(1.3)
        datRMS.GetYaxis().SetLabelOffset(0.0001)
        datRMS.GetYaxis().SetTitleSize(30)
        datRMS.SetMarkerStyle(0)
        
        ##################################################################################### divide error by bin content and set to unity
        keephists.append( [datcopy,trueCopy, datPDF, datJMR, datPU])
        for ibin in xrange(1,datcopy.GetNbinsX()):
            if datcopy.GetBinContent(ibin) > 0: 
                datcopy.SetBinError(ibin, datcopy.GetBinError(ibin)/datcopy.GetBinContent(ibin))
                datcopycopy.SetBinError(ibin, datcopycopy.GetBinError(ibin)/datcopycopy.GetBinContent(ibin))
                datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
                datJMR.SetBinError(ibin, datJMR.GetBinError(ibin)/datJMR.GetBinContent(ibin))
                datRMS.SetBinError(ibin, datRMS.GetBinError(ibin)/datRMS.GetBinContent(ibin))
                datPU.SetBinError(ibin, datPU.GetBinError(ibin)/datPU.GetBinContent(ibin))
            else:
                datcopy.SetBinError(ibin, 0)
                datcopycopy.SetBinError(ibin, 0)
                datPDF.SetBinError(ibin, 0)
                datJMR.SetBinError(ibin, 0)
                datRMS.SetBinError(ibin, 0)
                datPU.SetBinError(ibin, 0)
            datJMR.SetBinContent(ibin, 1.0)
            datPDF.SetBinContent(ibin, 1.0)
            datcopy.SetBinContent(ibin, 1.0)
            datcopycopy.SetBinContent(ibin, 1.0)
            datRMS.SetBinContent(ibin, 1.0)
            datPU.SetBinContent(ibin, 1.0)
        ########################################################################################################## Take Ratio
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0 )
        herwigCopy.Divide( herwigCopy, hReco, 1.0, 1.0 )
        if i < 11 and options.isSoftDrop and isData:
            print 'N theory bins = ', theorycopy.GetNbinsX()
            print 'N data bins = ', hReco.GetNbinsX()
            print 'N theory UB bins = ', theory2copy.GetNbinsX()
            
            theorycopy.Divide( theorycopy, hReco, 1.0, 1.0 )
            theory2copy.Divide( theory2copy, hReco, 1.0, 1.0 )

        if i < 11:
            powhegcopy.Divide( powhegcopy, hReco, 1.0, 1.0)
        ########################################################################################################## change pad and set axis range
        pads_list[i][1].cd()
        pads_list[i][1].SetLogx()

        if options.isSoftDrop :
            xlabeloption = 'Groomed j'
        else :
            xlabeloption = 'J'
        
        trueCopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(2)
        trueCopy.GetYaxis().SetTitleOffset(1.3)

        herwigCopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
        herwigCopy.UseCurrentStyle()
        herwigCopy.GetXaxis().SetTitleOffset(2)
        herwigCopy.GetYaxis().SetTitleOffset(1.3)
        if i < 11 and options.isSoftDrop and isData:
            theorycopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            theorycopy.UseCurrentStyle()
            theorycopy.SetFillStyle(3254)
            theorycopy.SetFillColor(ROOT.kBlue)
            theorycopy.SetLineColor(ROOT.kBlue)
            theorycopy.SetLineWidth(3)
            theorycopy.GetXaxis().SetTitleOffset(2)
            theorycopy.GetYaxis().SetTitleOffset(1.3)
            theory2copy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            theory2copy.UseCurrentStyle()
            theory2copy.SetFillStyle(3245)
            theory2copy.SetFillColor(ROOT.kOrange+7)
            theory2copy.SetLineColor(ROOT.kOrange+7)
            theory2copy.SetLineWidth(3)
            theory2copy.GetXaxis().SetTitleOffset(2)
            theory2copy.GetYaxis().SetTitleOffset(1.3)
        if i < 11:
            powhegcopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            #powhegcopy.UseCurrentStyle()
            powhegcopy.GetXaxis().SetTitleOffset(2)
            powhegcopy.GetYaxis().SetTitleOffset(1.3)
    
        datcopy.SetMinimum(0.5)
        datcopy.SetMaximum(1.5)
        datcopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopy.SetFillColor(ROOT.kYellow)
        datcopy.GetXaxis().SetTickLength(0.5)

        datcopycopy.SetMinimum(0.5)
        datcopycopy.SetMaximum(1.5)
        datcopycopy.GetYaxis().SetNdivisions(2,4,0,False)
        datcopycopy.SetFillColor(ROOT.kAzure+2)
        
        datPDF.SetMinimum(0.5)
        datPDF.SetMaximum(1.5)
        datPDF.GetYaxis().SetNdivisions(2,4,0,False)
        datPDF.SetFillColor(ROOT.kOrange)
        
        datJMR.SetMinimum(0.5)
        datJMR.SetMaximum(1.5)
        datJMR.GetYaxis().SetNdivisions(2,4,0,False)
        datJMR.SetFillColor(ROOT.kGreen)

        datPU.SetMinimum(0.5)
        datPU.SetMaximum(1.5)
        datPU.GetYaxis().SetNdivisions(2,4,0,False)
        datPU.SetFillColor(ROOT.kGreen)

        
        datRMS.SetMinimum(0.5)
        datRMS.SetMaximum(1.5)
        datRMS.GetYaxis().SetNdivisions(2,4,0,False)
        datRMS.SetFillColor(ROOT.kMagenta+2)

        datcopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datcopy.GetYaxis().SetTitleSize(30)
        datcopy.GetYaxis().SetTitleOffset(1.3)
        datcopy.GetYaxis().SetLabelOffset(0.01)
        datcopy.GetYaxis().SetLabelSize(28)
        datcopy.GetXaxis().SetLabelSize(28)
        datcopycopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datcopycopy.GetYaxis().SetTitleSize(30)
        datcopycopy.GetYaxis().SetTitleOffset(1.3)
        datcopycopy.GetYaxis().SetLabelOffset(0.01)
        datcopycopy.GetYaxis().SetLabelSize(28)
        datcopycopy.GetXaxis().SetLabelSize(28)
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.GetYaxis().SetTitleOffset(1.3)
        datPDF.GetYaxis().SetLabelOffset(0.01)
        datPDF.GetYaxis().SetLabelSize(28)
        datPDF.GetXaxis().SetLabelSize(28)
        datJMR.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datJMR.GetYaxis().SetTitleSize(30)
        datJMR.GetYaxis().SetTitleOffset(1.3)
        datJMR.GetYaxis().SetLabelOffset(0.01)
        datJMR.GetYaxis().SetLabelSize(28)
        datJMR.GetXaxis().SetLabelSize(28)
        datJMR.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPU.GetYaxis().SetTitleSize(30)
        datPU.GetYaxis().SetTitleOffset(1.3)
        datPU.GetYaxis().SetLabelOffset(0.01)
        datPU.GetYaxis().SetLabelSize(28)
        datPU.GetXaxis().SetLabelSize(28)

        datRMS.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datRMS.GetYaxis().SetTitleSize(30)
        datRMS.GetYaxis().SetTitleOffset(1.3)
        datRMS.GetYaxis().SetLabelOffset(0.01)
        datRMS.GetYaxis().SetLabelSize(28)
        datRMS.GetXaxis().SetLabelSize(28)
        trueCopy.SetLineStyle(2)
        trueCopy.SetLineColor(1)
        trueCopy.SetLineWidth(3)

        herwigCopy.SetLineStyle(8)
        herwigCopy.SetLineColor(ROOT.kMagenta+3)
        herwigCopy.SetLineWidth(3)
        if i < 11 and options.isSoftDrop and isData:
            theorycopy.SetLineStyle(2)
            theorycopy.SetLineColor(ROOT.kBlue)
            theorycopy.SetLineWidth(3)
            theory2copy.SetLineStyle(10)
            theory2copy.SetLineColor(ROOT.kOrange+7)
            theory2copy.SetLineWidth(3)
        if i < 11:
            powhegcopy.SetLineStyle(4)
            powhegcopy.SetLineColor(ROOT.kGreen + 2)
            powhegcopy.SetLineWidth(3)

        datcopy.GetXaxis().SetTitleOffset(3.5)
        datcopycopy.GetXaxis().SetTitleOffset(3.5)
        datPDF.GetXaxis().SetTitleOffset(3.5)
        datJMR.GetXaxis().SetTitleOffset(3.5)
        datPU.GetXaxis().SetTitleOffset(3.5)
        datRMS.GetXaxis().SetTitleOffset(3.5)

        if options.isSoftDrop :
            xlabeloption = 'Groomed j'
        else :
            xlabeloption = 'J'
        datcopy.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")
        datcopycopy.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")
        datPDF.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")
        datJMR.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")
        datPU.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)") 
        datRMS.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")


        datcopy.GetXaxis().SetTickLength(0.2)
        datcopycopy.GetXaxis().SetTickLength(0.2)
        datPDF.GetXaxis().SetTickLength(0.2)
        datJMR.GetXaxis().SetTickLength(0.2)
        datRMS.GetXaxis().SetTickLength(0.2)
        datPU.GetXaxis().SetTickLength(0.2)
                
        datPDF.GetXaxis().SetTickLength(0.2)
        datPDF.GetXaxis().SetNoExponent()


        ######################################################################## Draw and save

        if i == 18:
            datPDF.GetXaxis().SetRange(minmassbin,2000,"X")
        elif i > 11 and i < 18:
            datPDF.GetXaxis().SetRange(minmassbin,1200, "X")
        elif i > 7 and i < 12:
            datPDF.GetXaxis().SetRange(minmassbin,900, "X")
        elif i > 3 and i < 8:
            datPDF.GetXaxis().SetRange(minmassbin,600, "X")
        elif i < 4:
            datPDF.GetXaxis().SetRange(minmassbin,400,"X")
        datPDF.Draw('e2 ][')
        datcopycopy.Draw('e2 ][ same')
        datJMR.Draw('e2 ][ same')
        datcopy.Draw('e2 ][ same')
        datRMS.Draw('e2 ][ same')
        datPU.Draw('e2 ][ same')
        datcopy.SetMarkerStyle(0)
        trueCopy.Draw("hist ][ same")
        herwigCopy.Draw("hist ][ same")
        if i < 11 and options.isSoftDrop and isData:
            theorycopy.Draw("C E5 ][ same")
            theory2copy.Draw("C E5 ][ same")
            theorycopydumb = theorycopy.Clone( theorycopy.GetName() + "_dumb")
            theory2copydumb = theory2copy.Clone( theorycopy.GetName() + "_dumb")
            theorycopydumb.SetFillStyle(0)
            theory2copydumb.SetFillStyle(0)
            theorycopydumb.Draw("C hist ][ same")
            theorycopydumb.GetXaxis().SetRangeUser(5, 100000)
            theory2copydumb.Draw("C hist ][ same")
        if i < 11:
            powhegcopy.Draw("hist ][ same")
    
        keephists.append([datcopy, datPDF])
        pads_list[i][0].Update()
        pads_list[i][0].RedrawAxis()
        pads_list[i][1].Update()
        pads_list[i][1].RedrawAxis()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")
        canvas_list[i].SaveAs(outname_str + str(i) + ".pdf")
        chi2.append(hRecoPDF.KolmogorovTest(MC_list[i]))
        if options.isSoftDrop and i < 12:
            chi2_marzani.append(theory2.KolmogorovTest(hReco))
            chi2_harvard.append(theory.KolmogorovTest(hReco))
    print "The KS values for Pythia8 Generator are "
    print chi2
    if options.isSoftDrop:
        print "The KS values for Marzani predicitons are "
        print chi2_marzani
        print "The KS values for Harvard predictions are "
        print chi2_harvard
    theoryfile.Close()
    theoryfile2.Close()
    powhegfile.Close()
    herwig_genfile.Close()

def setup(canvases_to_use, pads_to_use):
    for icanv,canv in enumerate ( canvases_to_use ) :
        canv.cd()
        pad1 = ROOT.TPad('pad' + str(icanv) + '1', 'pad' + str(icanv) + '1', 0., 0.3, 1.0, 1.0)
        pad1.SetBottomMargin(0.022)
        pad2 = ROOT.TPad('pad' + str(icanv) + '2', 'pad' + str(icanv) + '2', 0., 0.0, 1.0, 0.3)
        pad2.SetTopMargin(0.05)
        pad1.SetLeftMargin(0.20)
        pad2.SetLeftMargin(0.20)
        pad2.SetBottomMargin(0.5)
        pad1.Draw()
        pad2.Draw()
        pads_to_use.append( [pad1,pad2] )

def plot_OneBand(canvas_list, pads_list, data_list, MC_list, jecup_list, jecdn_list, jerup_list, jerdn_list, jernom_list, puup_list, pudn_list, psdif_list, pdfdif_list, legends_list, outname_str, jmrup_list, jmrdn_list, jmrnom_list, latex_list, latexpt_list, ptbins_dict, softdrop= "", keephists=[], jackknifeRMS=False, isData = False):
    
    the_stack = THStack("stack", "")
    build_the_stack = []
    stackleg = ROOT.TLegend(0.17, 0.7, 0.89, 0.89)
    stackleg.SetTextSize( 0.021 )
    stackleg.SetNColumns(3)
    stackleg.SetFillColor(0)
    stackleg.SetBorderSize(0)

    chi2_pythia = []
    chi2_herwig = []
    chi2_marzani = []
    chi2_harvard = []

    graphs = []
    #uncertainties on the stacks :D
    build_the_stack_band = []
    stack_canvas = TCanvas("sc", "sc", 800, 800)
    stack_canvas.SetLeftMargin(0.15)
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100.]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    theoryfile = ROOT.TFile("theory_predictions.root")
    theorylist = []
    theoryfile2 = ROOT.TFile("theory_predictions_marzani_newpred.root")
    theorylist2 = []
    herwig_genfile = ROOT.TFile("PS_hists.root")
    herwig_genlist = []
    herwig_genlistSD = []
    for h in xrange(0, 11):
        herwig_genlist.append(herwig_genfile.Get("herwig_gen"+str(h)))
        herwig_genlistSD.append(herwig_genfile.Get("herwig_gen_softdrop"+str(h)))
    
    powhegfile = ROOT.TFile("CMS_SMP_16_010.root")
    powheglist = []
    powheglistSD = []
    for h in [1,2,3,4,5,6,7,8,9]:
        powheglist.append( powhegfile.Get("CMS_SMP_16_010/d0"+str(h)+"-x01-y01"))
    for h in [10,11,12]:
        powheglist.append( powhegfile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))
    for h in [13,14,15,16,17,18,19,20,21,22,23,24]:
        powheglistSD.append( powhegfile.Get("CMS_SMP_16_010/d"+str(h)+"-x01-y01"))

    for h in xrange(0, 12):
        theorylist.append( theoryfile.Get("histSD_"+str(h)+"_ours"))
        theorylist2.append( theoryfile2.Get("hist_marzani_SD_"+str(h)))
    for i, canv in enumerate(canvas_list):
        minmassbin = minmassbin_ungroomed(i)
        if options.isSoftDrop :
            minmassbin = minmassbin_groomed(i)
        pads_list[i][0].cd()
        if options.logy:
            pads_list[i][0].SetLogy()
        pads_list[i][0].SetLogx()
        data_list[i].UseCurrentStyle()
        MC_list[i].UseCurrentStyle()
        data_list[i].Scale(scales[i])
        MC_list[i].Scale(scales[i])
        ########################################################################################## Get JER and JES Hists
        hRMS = data_list[i]
        nom = jernom_list[i]
        jesUP  = jecup_list[i]
        jeOWN = jecdn_list[i]
        jerUP  = jerup_list[i]
        jerDOWN = jerdn_list[i]
        ########################################################################################## Get JMR hists
        jmrup = jmrup_list[i]
        jmrdn = jmrdn_list[i]
        jmrnom = jmrnom_list[i]
        ########################################################################################## Get PU hists
        puup = puup_list[i]
        pudn = pudn_list[i]
        ########################################################################################## Scale the hists for Pt bins
        puup.Scale(scales[i])
        pudn.Scale(scales[i])
        jmrup.Scale(scales[i])
        jmrdn.Scale(scales[i])
        jmrnom.Scale(scales[i])
        jesUP.Scale(scales[i])
        jeOWN.Scale(scales[i])
        jerUP.Scale(scales[i])
        jerDOWN.Scale(scales[i])
        nom.Scale(scales[i])
        hStat = hRMS.Clone()

        #zero_hist_bins( 0, 1, [hRMS,hStat,puup,pudn,jmrup,jmrdn,jmrnom,jesUP,jeOWN,jerUP,jerDOWN,nom] )

        for ibin in xrange(1, hRMS.GetNbinsX()):
            hRMS.SetBinContent(ibin, hRMS.GetBinContent(ibin) * 1. / mbinwidths[ibin-1])
            hStat.SetBinContent(ibin, hStat.GetBinContent(ibin)* 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, hRMS.GetBinError(ibin) * 1. / mbinwidths[ibin-1])
            hStat.SetBinError(ibin, hStat.GetBinError(ibin) * 1. / mbinwidths[ibin-1])
            hRMS.SetBinError(ibin, add_quadrature( [hRMS.GetBinError(ibin) , ((jackknifeRMS[i][ibin-1])*scales[i]*(1./mbinwidths[ibin-1]) ) ]) )
        hReco = hRMS.Clone()

        
        ########################################################################################## Scale the hists for mass bins
        for ibin in xrange(1, hReco.GetNbinsX()):
            puup.SetBinContent(ibin, puup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            pudn.SetBinContent(ibin, pudn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrup.SetBinContent(ibin, jmrup.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrdn.SetBinContent(ibin, jmrdn.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jmrnom.SetBinContent(ibin, jmrnom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jesUP.SetBinContent(ibin, jesUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jeOWN.SetBinContent(ibin, jeOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerUP.SetBinContent(ibin, jerUP.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            jerDOWN.SetBinContent(ibin, jerDOWN.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            nom.SetBinContent(ibin, nom.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            MC_list[i].SetBinContent(ibin, MC_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            herwig_genlist[i].SetBinContent(ibin, herwig_genlist[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            herwig_genlistSD[i].SetBinContent(ibin, herwig_genlistSD[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            if i < 11:
                powheglist[i].SetBinContent(ibin, powheglist[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
                powheglistSD[i].SetBinContent(ibin, powheglistSD[i].GetBinContent(ibin) * 1./mbinwidths[ibin-1])
########################################################################################## Add JER and JES Uncertainties
        for ibin in xrange(1,hReco.GetNbinsX()):
            val = float(hReco.GetBinContent(ibin))
            err1 = float(hReco.GetBinError(ibin))
            upjes = float(abs(jesUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjes = float(abs(nom.GetBinContent(ibin) - jeOWN.GetBinContent(ibin)))
            sys = float(((upjes + downjes)/2.))
            upjer = float(abs(jerUP.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downjer = float(abs(nom.GetBinContent(ibin) - jerDOWN.GetBinContent(ibin)))
            sys2 = float(((upjer + downjer )/2.))
            err = add_quadrature([sys, sys2, err1])
            hReco.SetBinError(ibin, err)
        ####################################################################################### Add Jet mass Resolution Band
        hRecoJMR = hReco.Clone()
        for ibin in xrange(1, hRecoJMR.GetNbinsX()):
            val = float(hRecoJMR.GetBinContent(ibin))
            err1 = float(hRecoJMR.GetBinError(ibin))
            upjmr = float(abs(jmrup.GetBinContent(ibin) - jmrnom.GetBinContent(ibin)))
            downjmr = float(abs(jmrnom.GetBinContent(ibin) - jmrdn.GetBinContent(ibin)))
            sys = float(((upjmr + downjmr)/2.))
            err = add_quadrature( [err1 , sys] )
            hRecoJMR.SetBinError(ibin, err)

        ####################################################################################### Add Jet mass Resolution Band
        hRecoPU = hRecoJMR.Clone()
        for ibin in xrange(1, hRecoPU.GetNbinsX()):
            val = float(hRecoPU.GetBinContent(ibin))
            err1 = float(hRecoPU.GetBinError(ibin))
            uppu = float(abs(puup.GetBinContent(ibin) - nom.GetBinContent(ibin)))
            downpu = float(abs(nom.GetBinContent(ibin) - pudn.GetBinContent(ibin)))
            sys = float(((uppu + downpu)/2.))
            err = add_quadrature( [err1 , sys] )
            hRecoPU.SetBinError(ibin, err)
        ######################################################################################## Add Parton Shower Uncertainties
        hRecoCopy = hRecoPU.Clone()
        for ibin in xrange(1, hRecoCopy.GetNbinsX()):
            temp = hRecoCopy.GetBinError(ibin)
            hRecoCopy.SetBinError(ibin, add_quadrature( [temp , (psdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1]) ]))
        ######################################################################################## Add PDF Uncertainties
        hRecoPDF = hRecoCopy.Clone()
        for ibin in xrange(1, hRecoPDF.GetNbinsX()):
            temp = hRecoPDF.GetBinError(ibin)
            hRecoPDF.SetBinError(ibin, add_quadrature( [temp , (pdfdif_list[i][ibin-1] * 1./ mbinwidths[ibin-1] ) ]))
        ####################################################################################### PDF Drawn Here
        hReco.Scale(1.0/hReco.Integral("width"))
        hRecoPDF.SetTitle(";;Normalized cross section")
        hRecoPDF.GetYaxis().SetTitleSize(30)
        hRecoPDF.GetYaxis().SetTitleOffset(1.3)
        hRecoPDF.GetYaxis().SetLabelOffset(0.0001)
        hRecoPDF.GetYaxis().SetLabelSize(28)
        hRecoPDF.SetMarkerStyle(20)
        hRecoPDF.SetFillColor(ROOT.kGray)
        hRecoPDF.Scale(1.0/hRecoPDF.Integral("width"))
        hStat.SetTitle(";;Normalized cross section")
        hStat.GetYaxis().SetTitleSize(30)
        hStat.GetYaxis().SetTitleOffset(1.3)
        hStat.GetYaxis().SetLabelOffset(0.0001)
        hStat.GetYaxis().SetLabelSize(28)
        hStat.SetFillColor(ROOT.kGray+1)
        hStat.Scale(1./hStat.Integral("width"))
        if i == 11:
            hRecoPDF.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin(2000))
            hStat.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin( 2000 ))
        elif i > 11 and i < 18:
            hRecoPDF.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin(2000 ))
            hStat.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin( 2000 ))
        elif i > 7 and i < 11:
            hRecoPDF.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin(2000 ))
            hStat.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin( 2000 ))
        elif i > 3 and i < 8:
            hRecoPDF.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin(2000 ))
            hStat.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin( 2000 ))
        elif i < 4:
            hRecoPDF.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin(2000))
            hStat.GetXaxis().SetRange(minmassbin, hRecoPDF.GetXaxis().FindBin( 2000 ))
        build_the_stack_band.append(hRecoPDF.Clone())


        hRecoBarePdf = hRecoPDF.Clone()
        hRecoBarePdf.SetName( hRecoPDF.GetName() + "_bare" )
        for ibin in xrange( hRecoBarePdf.GetXaxis().GetNbins() ) :
            hRecoBarePdf.SetBinError( ibin, 0.000000000001 )
        hRecoBarePdf.SetMarkerStyle(20)
        hRecoBarePdf.SetLineColor( hStat.GetLineColor() )
        hRecoBarePdf.SetFillStyle(0)

        
        print '-------- integral : ' + str( hRecoPDF.Integral(0, hRecoPDF.GetNbinsX(), "width" ) )
        iisum = 0.
        for iibin in xrange( hRecoPDF.GetNbinsX() ):
            iisum += hRecoPDF.GetBinContent( iibin )
        print '-------- iisum : ' + str( iisum)

        ## for ibin in xrange( hRecoPDF.GetNbinsX() + 1) :
        ##     hRecoPDF.SetBinContent( ibin, hRecoPDF.GetBinContent(ibin) * hRecoPDF.GetBinCenter(ibin) )
        ##     hStat.SetBinContent( ibin, hStat.GetBinContent(ibin) * hStat.GetBinCenter(ibin) )
        ##     hRecoBarePdf.SetBinContent( ibin, hRecoBarePdf.GetBinContent(ibin) * hRecoBarePdf.GetBinCenter(ibin) )

        
        hRecoPDF.Draw("E2 ][")
        if options.isSoftDrop : 
            hRecoPDF.SetMaximum( 1.7 * hRecoPDF.GetMaximum() )
        else :
            hRecoPDF.SetMaximum( 1.2 * hRecoPDF.GetMaximum() )
        hStat.Draw("E2 ][ same")
        hRecoBarePdf.Draw("e x0 ][ same")


        for ibin in xrange( hRecoPDF.GetNbinsX()+1):
            err = hRecoPDF.GetBinError( ibin )
            val = hRecoPDF.GetBinContent( ibin )



            if (val == 0.0  or ( val > 0.0 and abs(err) / abs(val) > 0.6)) or (not options.isSoftDrop and hRecoPDF.GetXaxis().GetBinUpEdge(ibin) <= 10.0): 
                hRecoPDF.SetBinContent( ibin, 0.0 )
                hRecoPDF.SetBinError( ibin, 0.0 )
                hRecoBarePdf.SetBinContent( ibin, 0.0 )
                hRecoBarePdf.SetBinError( ibin, 0.0 )
                hStat.SetBinContent( ibin, 0.0 )
                hStat.SetBinError( ibin, 0.0 )
                MC_list[i].SetBinContent( ibin, 0.0 )
                MC_list[i].SetBinError( ibin, 0.0 )
                if options.isSoftDrop:
                    powheglistSD[i].SetBinContent( ibin, 0.0 )
                    powheglistSD[i].SetBinError( ibin, 0.0 )
                    herwig_genlistSD[i].SetBinContent( ibin, 0.0 )
                    herwig_genlistSD[i].SetBinError( ibin, 0.0 )
                else:
                    powheglist[i].SetBinContent( ibin, 0.0 )
                    powheglist[i].SetBinError( ibin, 0.0 )
                    herwig_genlist[i].SetBinContent( ibin, 0.0 )
                    herwig_genlist[i].SetBinError( ibin, 0.0 )
                    
                if i < 11 and options.isSoftDrop and isData : 
                    theorylist[i].SetBinContent( ibin, 0.0 )
                    theorylist[i].SetBinError( ibin, 0.0 )
                    theorylist2[i].SetBinContent( ibin, 0.0 )
                    theorylist2[i].SetBinError( ibin, 0.0 )

        if not options.isSoftDrop : 
            unpinch( hRecoPDF )
            unpinch( hRecoBarePdf )
            unpinch( hStat )
        hRecoPDF.GetXaxis().SetTickLength(0.05)
        keephists.append([hRecoPDF, hStat, hRecoBarePdf])
        
        ####################################################################################### Gen Drawn Here
        MC_list[i].SetLineColor(1)
        MC_list[i].SetLineStyle(2)
        MC_list[i].SetLineWidth(3)
        MC_list[i].Scale(1.0/MC_list[i].Integral("width"))
        MC_list[i].Draw( "hist ][ SAME" )
        
        ####################################################################################### Legends Filled
        legends_list[i].AddEntry(hRecoPDF, 'Data', 'p')
        legends_list[i].AddEntry(hRecoPDF, 'Stat. + Sys. Unc.', 'f')
        legends_list[i].AddEntry(hStat, 'Stat Unc.', 'f')
        legends_list[i].AddEntry(MC_list[i], 'Pythia8', 'l')
        herwig_gen = None
        if options.isSoftDrop:
            herwig_gen = herwig_genlistSD[i]
        else:
            herwig_gen = herwig_genlist[i]
        herwig_gen.Scale(1.0/herwig_gen.Integral("width"))
        herwig_gen.SetLineStyle(8)
        herwig_gen.SetLineColor(ROOT.kMagenta + 1)
        herwig_gen.SetLineWidth(3)
        herwig_gen.Draw("hist ][ same")
        legends_list[i].AddEntry(herwig_gen, "HERWIG++", 'l')
        herwigCopy = herwig_gen.Clone()
        herwigCopy.SetName( herwigCopy.GetName() + "_copy")

        powheg = None
        if i < 11:
            if options.isSoftDrop:
                powheg = powheglistSD[i]
            else:
                powheg = powheglist[i]
            powheg.Scale(1.0/powheg.Integral("width"))
            powheg.SetLineStyle(4)
            powheg.SetLineColor(ROOT.kGreen + 2)
            powheg.SetLineWidth(3)
            powheg.Draw("hist ][ same")
            legends_list[i].AddEntry(powheg, "POWHEG + PYTHIA8", 'l')
            powhegcopy = powheg.Clone()
            powhegcopy.SetName( powheg.GetName()+"_copy")
            powhegcopy.SetLineStyle(4)
            powhegcopy.SetLineColor(ROOT.kGreen + 2)
            powhegcopy.SetLineWidth(3)
            
        if i < 11 and options.isSoftDrop : #and isData:
            theory = theorylist[i]
            theory.Scale(1.0/theory.Integral("width"))
            #theory.Scale(1.0/(20.*theory.GetBinContent(7)))
            print 'i = ', i
            ratio_bin = float(hReco.GetBinContent( hReco.GetXaxis().FindBin(50.))/theory.GetBinContent( theory.GetXaxis().FindBin(50.)))
            theory.Scale(ratio_bin)
            #theory.Scale(scales[i])
            theory.SetFillStyle(3254)
            theory.SetFillColor(ROOT.kBlue)
            theory.SetLineColor(ROOT.kBlue)
            theory.SetLineWidth(0)
            #theory.SetAxisRange(1e-5, 1, "Y")

            theorygraph = getGraph( theory, width=3 ) 
            theorygraph.Draw("L3 0 ][ same")
            
            #theorydumb = theory.Clone(theory.GetName() + "_dumb")
            #theorydumb.SetFillStyle(0)
            #theorydumb.Draw("C hist same")
            #theorydumb.GetXaxis().SetRangeUser(5, 100000)
            legends_list[i].AddEntry(theory, "Frye et al", 'f')
            #legends_list[i].Draw("same")
            
            theory2 = theorylist2[i]
            ratio_bin2 = float(hReco.GetBinContent( hReco.GetXaxis().FindBin(50.))/theory2.GetBinContent( theory2.GetXaxis().FindBin(50.)))
            #theory2.Scale(ratio_bin2)
            #theory2.Scale(1.0/theory2.Integral("width"))
            #ratio_bin2 = float(hRecoPDF.GetBinContent(7)/theory2.GetBinContent(7))
            #theory2.Scale(ratio_bin2)
            #theory2.Scale(1.0/hRecoPDF.Integral("width"))
            #theory2.SetLineStyle(10)
            theory2.SetFillStyle(3245)
            theory2.SetFillColor(ROOT.kOrange+7)            
            theory2.SetLineColor(ROOT.kOrange+7)
            theory2.SetLineWidth(0)
            theory2graph = getGraph( theory2, width=3 )
            theory2graph.Draw("L3 0 ][ same") 
            #theory2.Draw("C E5 same")
            #theory2dumb = theory2.Clone(theory2.GetName() + "_dumb")
            #theory2dumb.SetFillStyle(0)
            #theory2dumb.Draw("C hist same")
            legends_list[i].AddEntry(theory2, "Marzani et al", 'f')
            ## add to the stack and scale
            theoryc = theory.Clone()
            theory2c = theory2.Clone()
            powhegc = powheg.Clone()
            for ibin in range(1, theoryc.GetNbinsX()):
                theoryc.SetBinError(ibin, 0)
                theory2c.SetBinError(ibin, 0)
                powhegc.SetBinError(ibin, 0)
            
            theoryc.Scale(10**(i-9))
            theory2c.Scale(10**(i-9))
            powhegc.Scale(10**(i-9))
            
            theoryc.SetLineStyle(0)
            theory2c.SetLineStyle(0)
            powhegc.SetLineStyle(0)

            theoryc.SetMarkerStyle(26)
            theory2c.SetMarkerStyle(32)
            powhegc.SetMarkerStyle(33)
            
            #build_the_stack.append(theoryc)
            #build_the_stack.append(theory2c)
            #build_the_stack.append(powhegc)
        legends_list[i].Draw()
        latex_list[i].DrawLatex(0.2, 0.926, "CMS Preliminary")
        latex_list[i].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")
        if options.logy:
            if options.isSoftDrop:
                latexpt_list[i].DrawLatex(0.3, 0.490, ptbins_dict[i])
            else:
                latexpt_list[i].DrawLatex(0.22, 0.830, ptbins_dict[i])
        else:
            if options.isSoftDrop:
                latexpt_list[i].DrawLatex(0.60, 0.830, ptbins_dict[i])
            else:
                latexpt_list[i].DrawLatex(0.22, 0.830, ptbins_dict[i])
        
        mcc = MC_list[i].Clone()
        pdfc = hRecoPDF.Clone()
        barepdfc = hRecoBarePdf.Clone()
        herwigc = herwig_gen.Clone()

        for ibin in range(1, mcc.GetNbinsX()):
            mcc.SetBinError(ibin, 0)
            herwigc.SetBinError(ibin, 0)
        
        mcc.Scale(10**(i-9))
        pdfc.Scale(10**(i-9))
        barepdfc.Scale(10**(i-9))
        herwigc.Scale(10**(i-9))
        
        mcc.SetMarkerStyle(34)
        #mcc.UseCurrentStyle()
        herwigc.SetMarkerStyle(23)
        #herwigc.UseCurrentStyle()
        pdfc.SetLineStyle(1)
        #pdfc.UseCurrentStyle()
        
        stackleg.AddEntry( pdfc, get_ptbins_std()[i], 'p')
        pdfc.SetFillColor(ROOT.kGray)
        pdfc.SetFillStyle(3101)
        pdfc.SetMarkerStyle( get_markers()[i] )
        build_the_stack.append( [mcc, 'hist'] )
        build_the_stack.append( [pdfc, 'e2'] )
        #build_the_stack.append(barepdfc)
        #build_the_stack.append(herwigc)
####################################################################################### Hists Cloned and formatted for ratios
        trueCopy = MC_list[i].Clone()
        trueCopy.SetName( trueCopy.GetName() + "_copy")
        
        if i < 11 and options.isSoftDrop and isData:
            theorycopy = theory.Clone()
            theorycopy.SetName( theory.GetName() + "_copy" )
            theory2copy = theory2.Clone()
            theory2copy.SetName( theory2.GetName() + "_copy" )



        if options.isSoftDrop :
            xlabeloption = 'Groomed j'
        else :
            xlabeloption = 'J'

            
        datPDF = hRecoPDF.Clone()
        datPDF.SetName(hRecoPDF.GetName()+"_pdfcopy")
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPDF.GetYaxis().SetTitleOffset(1.3)
        datPDF.GetYaxis().SetLabelOffset(0.0001)
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.SetMarkerStyle(0)
        datStat = hStat.Clone()
        datStat.SetName(hStat.GetName()+"copy")
        datStat.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datStat.GetYaxis().SetTitleOffset(1.3)
        datStat.GetYaxis().SetLabelOffset(0.0001)
        datStat.GetYaxis().SetTitleSize(30)
        datStat.SetMarkerStyle(0)
        ##################################################################################### divide error by bin content and set to unity
        keephists.append( [trueCopy, datPDF, datStat])
        for ibin in xrange(1,datPDF.GetNbinsX()):
            if datPDF.GetBinContent(ibin) > 0:
                datPDF.SetBinError(ibin, datPDF.GetBinError(ibin)/datPDF.GetBinContent(ibin))
                datStat.SetBinError(ibin, datStat.GetBinError(ibin)/datStat.GetBinContent(ibin))
            else:
                datPDF.SetBinError(ibin, 0)
                datStat.SetBinError(ibin, 0)
            datPDF.SetBinContent(ibin, 1.0)
            datStat.SetBinContent(ibin, 1.0)
########################################################################################################## Take Ratio
        trueCopy.Divide( trueCopy, hReco, 1.0, 1.0 )
        herwigCopy.Divide( herwigCopy, hReco, 1.0, 1.0 )
        if i < 11 and options.isSoftDrop and isData:
            print 'N theory bins = ', theorycopy.GetNbinsX()
            print 'N data bins = ', hReco.GetNbinsX()
            print 'N theory UB bins = ', theory2copy.GetNbinsX()
            theorycopy.Divide( theorycopy, hReco, 1.0, 1.0 )
            theory2copy.Divide( theory2copy, hReco, 1.0, 1.0 )
        if i < 11:
            powhegcopy.Divide( powhegcopy, hReco, 1.0, 1.0)
        ########################################################################################################## change pad and set axis range
        pads_list[i][1].cd()
        pads_list[i][1].SetLogx()
        trueCopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
        trueCopy.UseCurrentStyle()
        trueCopy.GetXaxis().SetTitleOffset(2)
        trueCopy.GetYaxis().SetTitleOffset(1.3)
        herwigCopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
        herwigCopy.UseCurrentStyle()
        herwigCopy.GetXaxis().SetTitleOffset(2)
        herwigCopy.GetYaxis().SetTitleOffset(1.3)
        if i < 11 and options.isSoftDrop and isData:

            theorycopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            theorycopy.UseCurrentStyle()
            theorycopy.SetFillStyle(3254)
            theorycopy.SetFillColor(ROOT.kBlue)
            theorycopy.SetLineColor(ROOT.kBlue)
            theorycopy.SetLineWidth(3)
            theorycopy.GetXaxis().SetTitleOffset(2)
            theorycopy.GetYaxis().SetTitleOffset(1.3)
            theory2copy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            theory2copy.UseCurrentStyle()
            theory2copy.SetFillStyle(3245)
            theory2copy.SetFillColor(ROOT.kOrange+7)            
            theory2copy.SetLineColor(ROOT.kOrange+7)
            theory2copy.SetLineWidth(3)
            theory2copy.GetXaxis().SetTitleOffset(2)
            theory2copy.GetYaxis().SetTitleOffset(1.3)

        if i < 11:
            powhegcopy.SetTitle(";" + xlabeloption + "et mass (GeV);#frac{Theory}{Data}")
            #powhegcopy.UseCurrentStyle()
            powhegcopy.GetXaxis().SetTitleOffset(2)
            powhegcopy.GetYaxis().SetTitleOffset(1.3)

        trueCopy.GetXaxis().SetTickLength(0.5)
        datPDF.SetMinimum(0.5)
        datPDF.SetMaximum(1.5)
        datPDF.GetYaxis().SetNdivisions(2,4,0,False)
        datPDF.GetXaxis().SetTickLength(10)
        datPDF.SetFillColor(ROOT.kGray)
        
        datPDF.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datPDF.GetYaxis().SetTitleSize(30)
        datPDF.GetYaxis().SetTitleOffset(1.3)
        datPDF.GetYaxis().SetLabelOffset(0.01)
        datPDF.GetYaxis().SetLabelSize(28)
        datPDF.GetXaxis().SetLabelSize(28)
		
        datStat.SetMinimum(0.5)
        datStat.SetMaximum(1.5)
        datStat.GetYaxis().SetNdivisions(2, 4, 0, False)
        datStat.SetFillColor(ROOT.kGray+1)
        datStat.GetYaxis().SetTitle("#frac{Theory}{Data}")
        datStat.GetYaxis().SetTitleSize(30)
        datStat.GetYaxis().SetTitleOffset(1.3)
        datStat.GetYaxis().SetLabelOffset(0.01)
        datStat.GetYaxis().SetLabelSize(28)
        datStat.GetXaxis().SetLabelSize(28)
		
		
        trueCopy.SetLineStyle(2)
        trueCopy.SetLineColor(1)
        trueCopy.SetLineWidth(3)

        herwigCopy.SetLineStyle(8)
        herwigCopy.SetLineColor(ROOT.kMagenta + 1)
        herwigCopy.SetLineWidth(3)

        #if i < 11 and options.isSoftDrop and isData:
        #    theorycopy.SetLineStyle(2)
        #    theorycopy.SetLineColor(ROOT.kBlue)
        #    theorycopy.SetLineWidth(3)
        #    theory2copy.SetLineStyle(10)
        #    theory2copy.SetLineColor(ROOT.kOrange+7)
        #    theory2copy.SetLineWidth(3)
        #if i < 11:
        #    powhegcopy.SetLineStyle(4)
        #    powhegcopy.SetLineColor(ROOT.kGreen + 2)
        #    powhegcopy.SetLineWidth(3)


        if options.isSoftDrop :
            xlabeloption = 'Groomed j'
        else :
            xlabeloption = 'J'
        
        datPDF.GetXaxis().SetTitleOffset(3.5)
    
        datPDF.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")
		
        datStat.GetXaxis().SetTitleOffset(3.5)
        datStat.GetXaxis().SetTitle(xlabeloption + "et mass (GeV)")

        ######################################################################## Draw and save

            
        if i == 11:
            datPDF.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin(2000) )
            datStat.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin( 2000 ) )
        elif i > 11 and i < 18:
            datPDF.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin(2000 ) )
            datStat.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin( 2000 ) )
        elif i > 7 and i < 11:
            datPDF.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin(2000 ) )
            datStat.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin( 2000 ) )
        elif i > 3 and i < 8:
            datPDF.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin(2000 ) )
            datStat.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin( 2000 ) )
        elif i < 4:
            datPDF.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin(2000) )
            datStat.GetXaxis().SetRange(minmassbin, datPDF.GetXaxis().FindBin( 2000 ) )
        datPDF.Draw('e2 ][ ')
        datPDF.GetXaxis().SetTickLength(0.10)
        datPDF.GetXaxis().SetNoExponent()
        datStat.Draw('e2 ][ same')
        trueCopy.Draw("hist ][ same")
        herwigCopy.Draw("hist ][ same")
        if i < 11 and options.isSoftDrop and isData:
            theorycopygraph = getGraph( theorycopy, width=3 )
            theorycopygraph.Draw("L3 same")
            theory2copygraph = getGraph( theory2copy, width=3 )
            theory2copygraph.Draw("L3 same")
            #theorycopy.Draw("C E5 same")
            #theory2copy.Draw("C E5 same")
            #theorycopydumb = theorycopy.Clone( theorycopy.GetName() + "_dumb")
            #theory2copydumb = theory2copy.Clone( theorycopy.GetName() + "_dumb")
            #theorycopydumb.SetFillStyle(0)
            #theory2copydumb.SetFillStyle(0)
            #theorycopydumb.Draw("C hist same")
            #theorycopydumb.GetXaxis().SetRangeUser(5, 100000)
            #theory2copydumb.Draw("C hist same")
        if i < 11:
            powhegcopy.Draw("hist ][ same")
        keephists.append([datPDF])
        pads_list[i][0].Update()
        pads_list[i][0].RedrawAxis()
        pads_list[i][1].Update()
        pads_list[i][1].RedrawAxis()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str + str(i) + ".png")
        canvas_list[i].SaveAs(outname_str + str(i) + ".pdf")
        hRecoKS = hRecoPDF.Clone( hRecoPDF.GetName() + "_KS")
        hMCKS = MC_list[i].Clone( MC_list[i].GetName() + "_KS")
        hMCKS_Herwig = herwig_gen.Clone( herwig_gen.GetName() + "_KS")



        hRecoKS.GetXaxis().SetRangeUser( expected_agreement()[i][0], 10000)
        hMCKS.GetXaxis().SetRangeUser(expected_agreement()[i][0],10000)
        hMCKS_Herwig.GetXaxis().SetRangeUser(expected_agreement()[i][0],10000)
        hRecoKS.Scale( 1.0 / hRecoKS.Integral("width") )
        hMCKS.Scale( 1.0 / hMCKS.Integral("width") )
        hMCKS_Herwig.Scale( 1.0 / hMCKS_Herwig.Integral("width") )

        ## for ihwbin in xrange( 1, hMCKS.GetNbinsX() ) :
        ##     val_py = hMCKS.GetBinContent(ihwbin)
        ##     val_hw = hMCKS_Herwig.GetBinContent(ihwbin)
        ##     val_data = hRecoKS.GetBinContent(ihwbin)
        ##     err_py = hMCKS.GetBinError(ihwbin)
        ##     err_hw = hMCKS_Herwig.GetBinError(ihwbin)
        ##     err_data = hRecoKS.GetBinError(ihwbin)
        ##     if val_py > 1e-10 and val_hw > 1e-10 :
        ##         err1 = err_py / val_py
        ##         err2 = err_hw / val_hw
        ##         valdiff_hw = (val_data - val_hw) / err_hw
        ##         valdiff_py = (val_data - val_py) / err_py
             
        ##         errtot = err1 * val_hw

        ##         hMCKS_Herwig.SetBinError( ihwbin, errtot )
        
        chi2_pythia.append(hRecoKS.Chi2Test(hMCKS, "WW"))
        chi2_herwig.append(hRecoKS.Chi2Test(hMCKS_Herwig, "WW"))
        if options.isSoftDrop and i < 12:
            theoryKS = theory.Clone(theory.GetName() + "_KS")
            theory2KS = theory2.Clone(theory2.GetName() + "_KS")
            theoryKS.GetXaxis().SetRangeUser(expected_agreement()[i][0], expected_agreement()[i][1])
            theory2KS.GetXaxis().SetRangeUser(expected_agreement()[i][0],expected_agreement()[i][1])
            #theory2KS.Scale( 1.0 / theory2KS.Integral("width") )
            theoryKS.Scale( 1.0 / theoryKS.Integral("width") )
            chi2_marzani.append(theory2KS.Chi2Test(hRecoKS, "WW"))
            chi2_harvard.append(theoryKS.Chi2Test(hRecoKS, "WW"))
                    
    stack_canvas.cd()
    stack_canvas.SetLogy()
    stack_canvas.SetLogx()
    #for hist in build_the_stack_band:
    #    hist.Draw('same E5')
    for ihist in xrange( 1, len(build_the_stack), 2) :
        hist = build_the_stack[ihist]
        mchist = build_the_stack[ihist - 1]
        mchist[0].SetLineColor(2)
        ptbin_stack = ihist/2
        for errbin in xrange ( 1, hist[0].GetNbinsX() + 1):
            ierr = hist[0].GetBinError( errbin )
            ival = hist[0].GetBinContent( errbin )
            if options.isSoftDrop == False and hist[0].GetXaxis().GetBinUpEdge(errbin) <= 20.0 :
                hist[0].SetBinContent(errbin,0.0)
                hist[0].SetBinError( errbin, 0.0 )
                mchist[0].SetBinContent(errbin,0.0)
                mchist[0].SetBinError( errbin, 0.0 )                
            if ival > 0.0 and ierr / ival > 0.6 :
                hist[0].SetBinContent(errbin,0.0)
                hist[0].SetBinError( errbin, 0.0 )
                mchist[0].SetBinContent(errbin,0.0)
                mchist[0].SetBinError( errbin, 0.0 )
            if ival == 0.0 :
                mchist[0].SetBinContent(errbin,0.0)
                mchist[0].SetBinError( errbin, 0.0 )
            if options.isSoftDrop==False and errbin < minmassbin_ungroomed(ptbin_stack) :
                hist[0].SetBinContent(errbin,0.0)
                hist[0].SetBinError( errbin, 0.0 )
                mchist[0].SetBinContent(errbin,0.0)
                mchist[0].SetBinError( errbin, 0.0 )
            if options.isSoftDrop==True and errbin < minmassbin_groomed(ptbin_stack) :
                hist[0].SetBinContent(errbin,0.0)
                hist[0].SetBinError( errbin, 0.0 )
                mchist[0].SetBinContent(errbin,0.0)
                mchist[0].SetBinError( errbin, 0.0 )
                
        the_stack.Add(hist[0], hist[1])
        the_stack.Add(mchist[0], mchist[1])

        
    the_stack.Draw("][ nostack")
    if options.isSoftDrop == False :
        the_stack.GetXaxis().SetRangeUser(1, 1000)
    else :
        the_stack.GetXaxis().SetRangeUser(1, 1000)
    the_stack.GetXaxis().SetNoExponent()
    the_stack.SetMinimum(1e-14)
    the_stack.SetMaximum(1e4)
    stackleg.AddEntry( mcc, 'PYTHIA8', 'l')
    stackleg.Draw()
    if(not options.isSoftDrop):
        the_stack.SetTitle(";Jet mass(GeV);Normalized cross section")
    else:
        the_stack.SetTitle(";Groomed jet mass(GeV);Normalized cross section")
    latex_list[0].DrawLatex(0.2, 0.926, "CMS Preliminary")
    latex_list[0].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")

    the_stack.GetYaxis().SetTitleSize(30)
    the_stack.GetYaxis().SetTitleOffset(1.3)
    the_stack.GetYaxis().SetLabelOffset(0.0001)
    the_stack.GetYaxis().SetLabelSize(28)
    stack_canvas.Update()
    if(not options.isSoftDrop):
        stack_canvas.SaveAs("fullstack.png")
        stack_canvas.SaveAs("fullstack.pdf")
    else:
        stack_canvas.SaveAs("fullstacksoftdrop.png")
        stack_canvas.SaveAs("fullstacksoftdrop.pdf")


    # Make plots of chi2
    print "The KS values for Pythia8 Generator are "
    for chi2val in chi2_pythia :
        print ' %6.2f & ' % ( round( chi2val, 2) )
    print "The KS values for Herwig Generator are "
    for chi2val in chi2_herwig :
        print ' %6.2f & ' % ( round( chi2val, 2) )
    if options.isSoftDrop:
        print "The KS values for Marzani predicitons are "
        for chi2val in chi2_marzani :
            print ' %6.2f & ' % ( round( chi2val, 2) )
        print "The KS values for Harvard predictions are "
        for chi2val in chi2_harvard :
            print ' %6.2f & ' % ( round( chi2val, 2) )


    chi2_canvas = TCanvas("cchi2", "cchi2" )
    chi2_canvas.SetLeftMargin(0.15)
    if options.isSoftDrop: 
        chi2_legend = ROOT.TLegend( 0.35, 0.17, 0.57, 0.4 )
    else :
        chi2_legend = ROOT.TLegend( 0.68, 0.16, 0.88, 0.38 )
    chi2_legend.SetFillColor(0)
    chi2_legend.SetBorderSize(0)

    
    chi2_0 = ROOT.TGraph(11, get_pt_bin_vals(), array.array('d', chi2_pythia ) )
    chi2_0.SetName("chi2_0")
    chi2_0.SetLineWidth(3)
    chi2_0.Draw('al')
    graphs.append( chi2_0 )
    chi2_legend.AddEntry( chi2_0, "PYTHIA8", 'l')
    chi2_1 = ROOT.TGraph(11, get_pt_bin_vals(), array.array('d', chi2_herwig ) )
    chi2_1.SetName("chi2_1")
    chi2_1.SetLineWidth(3)
    chi2_1.SetLineStyle(4)
    chi2_1.SetLineColor(ROOT.kMagenta + 1)
    chi2_1.Draw('l')
    graphs.append( chi2_1 )
    chi2_legend.AddEntry( chi2_1, "HERWIG++", 'l')

        
    if options.isSoftDrop :     
        chi2_2 = ROOT.TGraph(11, get_pt_bin_vals(), array.array('d', chi2_marzani ) )
        chi2_2.SetName("chi2_2")
        chi2_2.SetLineColor(ROOT.kOrange + 7)
        chi2_2.SetLineStyle(2)
        chi2_2.SetLineWidth(3)
        chi2_3 = ROOT.TGraph(11, get_pt_bin_vals(), array.array('d', chi2_harvard ) )
        chi2_3.SetName("chi2_3")
        chi2_3.SetLineColor(ROOT.kBlue)
        chi2_3.SetLineStyle(3)
        chi2_3.SetLineWidth(3)
        chi2_3.Draw('l')
        chi2_2.Draw('l')
        graphs.append( chi2_2 )
        graphs.append( chi2_3 )
        chi2_legend.AddEntry( chi2_3, "Frye et al", 'l')
        chi2_legend.AddEntry( chi2_2, "Marzani et al", 'l')
    
        
    chi2_canvas.SetTopMargin(0.1)
    chi2_canvas.SetBottomMargin(0.15)
    chi2_0.SetMaximum(1.0)
    chi2_0.SetMinimum(0.0)
    chi2_0.SetTitle(';Jet p_{T} (GeV);Probability')

    chi2_0.GetXaxis().SetNoExponent()
    latex_list[0].DrawLatex(0.2, 0.926, "CMS Preliminary")
    latex_list[0].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")

    chi2_legend.Draw()

    if isData : 
        if options.unrestrictedChi2 : 
            chi2_canvas.Print('chi2prob_unrestricted.png', 'png')
            chi2_canvas.Print('chi2prob_unrestricted.pdf', 'pdf')
        else :
            chi2_canvas.Print('chi2prob.png', 'png')
            chi2_canvas.Print('chi2prob.pdf', 'pdf')

    canvas_list.append( chi2_canvas )
    legends_list.append( chi2_legend )
    
    # Close the files
    theoryfile.Close()
    theoryfile2.Close()
    powhegfile.Close()
    herwig_genfile.Close()

def PlotBias(canvas_list, pads_list, gen_list, reco_list, legends_list, recolegname_str, genlegname_str, outname_str, latex_list, latexpt_list, ptbins_dict):
    scales = [1./60., 1./90., 1./110., 1./90., 1./100., 1./110, 1./140., 1./100., 1./100.,1./100., 1./100., 1./100.,1./100.,1./100.,1./100.,1./100.,1./100.,1./100., 1./10000]
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    for i, canvas in enumerate(canvas_list):
        pads_list[i][0].cd()
        #pads_list[i][0].SetLogy()
        for ibin in xrange(1, reco_list[i].GetNbinsX()):
            reco_list[i].SetBinContent(ibin, reco_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin])
            reco_list[i].SetBinError(ibin, reco_list[i].GetBinError(ibin) * 1./mbinwidths[ibin])
            gen_list[i].SetBinContent(ibin, gen_list[i].GetBinContent(ibin) * 1./mbinwidths[ibin])
            gen_list[i].SetBinError(ibin, gen_list[i].GetBinError(ibin) * 1./mbinwidths[ibin])
        reco_list[i].UseCurrentStyle()
        gen_list[i].UseCurrentStyle()
        reco_list[i].Scale(scales[i])
        gen_list[i].Scale(scales[i])
        reco_list[i].SetTitle(";;Normalized cross section")
        reco_list[i].GetYaxis().SetTitleSize(30)
        reco_list[i].SetLineColor(1)
        reco_list[i].SetAxisRange(1e-11, 1, "Y")
        reco_list[i].SetStats(0)
        reco_list[i].Draw("SAME ][ hist")
        reco_list[i].GetXaxis().SetNoExponent()
        reco_list[i].GetXaxis().SetTitle("Jet mass (GeV)")
        legends_list[i].AddEntry(reco_list[i], recolegname_str, 'l')
        legends_list[i].AddEntry(gen_list[i], genlegname_str, 'pl')
        legends_list[i].Draw()
        gen_list[i].SetAxisRange(1e-11, 1, "Y")
        gen_list[i].SetMarkerStyle(8)
        #gen_list[i].SetMarkerSize(30)
        gen_list[i].Draw("][ SAME")
        latex_list[i].DrawLatex(0.2, 0.926, "CMS preliminary, 40 pb^{-1} (13 TeV)")
        latexpt_list[i].DrawLatex(0.200, 0.779, ptbins_dict[i])
        
        recocopy = reco_list[i].Clone()
        recocopy.SetName( recocopy.GetName() + "_copy")
        gencopy = gen_list[i].Clone()
        gencopy.SetName(gencopy.GetName() + "_copy")

        for ibin in xrange(1,recocopy.GetNbinsX()):
            if recocopy.GetBinContent(ibin) > 0: 
                recocopy.SetBinError(ibin, recocopy.GetBinError(ibin)/recocopy.GetBinContent(ibin))
            else:
                recocopy.SetBinError(ibin, 0)
            recocopy.SetBinContent(ibin, 1.0)
        gencopy.Divide(gencopy, reco_list[i], 1.0, 1.0)

        pads_list[i][1].cd()
        gencopy.SetTitle(";" + xlabeloption + "et mass (GeV); #frac{Theory}{Data}")
        recocopy.SetMinimum(0.5)
        recocopy.SetMaximum(1.5)
        recocopy.GetYaxis().SetNdivisions(2,4,0,False)
        recocopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        recocopy.GetYaxis().SetTitleOffset(1.3)
        recocopy.GetYaxis().SetLabelOffset(0.01)
        recocopy.GetYaxis().SetLabelSize(28)
        recocopy.GetXaxis().SetLabelSize(28)
        recocopy.GetYaxis().SetTitleSize(30)
        recocopy.GetXaxis().SetTitleOffset(2.3)
        recocopy.GetXaxis().SetTickLength(0.5)

        gencopy.SetMinimum(0.5)
        gencopy.SetMaximum(1.5)
        gencopy.GetYaxis().SetNdivisions(2,4,0,False)
        gencopy.GetYaxis().SetTitle("#frac{Theory}{Data}")
        gencopy.GetYaxis().SetTitleOffset(1.3)
        gencopy.GetYaxis().SetLabelOffset(0.01)
        gencopy.GetYaxis().SetLabelSize(28)
        gencopy.GetXaxis().SetLabelSize(28)
        gencopy.GetYaxis().SetTitleSize(30)
        gencopy.GetXaxis().SetTitleOffset(2.3)
        #gencopy.SetMarkerSize(30)

        recocopy.Draw('][ SAME')
        gencopy.Draw("hist ][ SAME")
        
        pads_list[i][0].Update()
        pads_list[i][0].RedrawAxis()
        pads_list[i][1].Update()
        pads_list[i][1].RedrawAxis()
        canvas_list[i].Draw()
        canvas_list[i].SaveAs(outname_str+str(i)+".png")
        

def PlotRatios(ratio_canvas_list, post_data_list, post_MC_list, pre_data_list, pre_MC_list, legends_list, ptbins_dict, latex_list, latexpt_list, outname_str, genMC_list, manyratios_canvas_list, legends_list2, softdrop= ""):
    mbinwidths = [1., 4., 5, 10., 20, 20., 20., 20., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.]
    
    for i, canvas in enumerate(ratio_canvas_list):

############## unfolded/preunfolded data, MC
        
        preMC = pre_MC_list[i].Clone()
        preMC.SetName( preMC.GetName()+"_copy" )
        preMC.Scale(1.0/preMC.Integral("width"))
        postMC = post_MC_list[i].Clone()
        postMC.SetName( postMC.GetName()+"_copy" )
        postMC.Scale(1.0/postMC.Integral("width"))
        preData = pre_data_list[i].Clone()
        preData.SetName( preData.GetName()+"_copy" )
        preData.Scale(1.0/preData.Integral("width"))
        postData = post_data_list[i].Clone()
        postData.SetName( postData.GetName()+"_copy" )
        postData.Scale(1.0/postData.Integral("width"))
        for ibin in xrange(1, preMC.GetNbinsX()):
            preMC.SetBinContent(ibin, preMC.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            postMC.SetBinContent(ibin, postMC.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            preData.SetBinContent(ibin, preData.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            postData.SetBinContent(ibin, postData.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

        
        postMC.Divide( postMC, preMC, 1.0, 1.0 )
        postData.Divide( postData, preData, 1.0, 1.0 )

        canvas.cd()

        leg = legends_list[i]

        if options.isSoftDrop :
            xlabeloption = 'Groomed j'
        else :
            xlabeloption = 'J'


        
        postMC.SetLineColor(1)
        postMC.SetTitle(";" + xlabeloption + "et mass (GeV);Ratio of Unfolded to Preunfolded")
        postMC.Draw("][ hist")
        postData.SetLineColor(4)
        postData.Draw("hist ][ same")
        legends_list[i].AddEntry(postMC, 'Ratio of Unfolded to PreUnfolded Monte Carlo '+softdrop, 'l')
        legends_list[i].AddEntry(postData, 'Ratio of Unfolded to PreUnfolded Data '+softdrop, 'l')
        legends_list[i].Draw()
        if i == 11:
            latexpt_list[i].DrawLatex(0.40, 0.830, ptbins_dict[i])
        else:
            latexpt_list[i].DrawLatex(0.60, 0.830, ptbins_dict[i])
        latex_list[i].DrawLatex(0.2, 0.926, "CMS Preliminary")
        latex_list[i].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")            
        canvas.SaveAs(outname_str + str(i) + ".pdf")


################# (gen level / unfolded data) / (reco MC / reco data)

        genMC = genMC_list[i].Clone()
        genMC.SetName( genMC.GetName()+"_copy" )
        genMC.Scale(1.0/genMC.Integral("width"))
        preMC2 = pre_MC_list[i].Clone()
        preMC2.SetName( preMC2.GetName()+"_copy2" )
        preMC2.Scale(1.0/preMC2.Integral("width"))
        preData2 = pre_data_list[i].Clone()
        preData2.SetName( preData2.GetName()+"_copy2" )
        preData2.Scale(1.0/preData2.Integral("width"))
        postData2 = post_data_list[i].Clone()
        postData2.SetName( postData2.GetName()+"_copy2" )
        postData2.Scale(1.0/postData2.Integral("width"))
        
        for ibin in xrange(1, preMC.GetNbinsX()):
            preMC2.SetBinContent(ibin, preMC2.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            genMC.SetBinContent(ibin, genMC.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            preData2.SetBinContent(ibin, preData2.GetBinContent(ibin) * 1./mbinwidths[ibin-1])
            postData2.SetBinContent(ibin, postData2.GetBinContent(ibin) * 1./mbinwidths[ibin-1])

        genMC.Divide( genMC, postData2, 1.0, 1.0 )
        preMC2.Divide( preMC2, preData2, 1.0, 1.0 )
        genMC.Divide( genMC, preMC2, 1.0, 1.0 )
        
        canvas2 = manyratios_canvas_list[i]
        canvas2.cd()

        genMC.Draw("][ hist")
        leg2 = legends_list2[i]
        legends_list2[i].AddEntry(genMC, '(gen level/unfolded data)/(reco MC/reco data) '+softdrop, 'l')
        legends_list2[i].Draw()
        latexpt_list[i].DrawLatex(0.60, 0.830, ptbins_dict[i])
        latex_list[i].DrawLatex(0.2, 0.926, "CMS Preliminary")
        latex_list[i].DrawLatex(0.62, 0.926, "2.3 fb^{-1} (13 TeV)")        
        genMC.SetTitle(";" + xlabeloption + "et mass (GeV);(Gen/Unfolded Data)/(Preunfolded MC/Preunfolded Data)")
        canvas2.SaveAs("gen"+ outname_str + str(i) + ".pdf")
