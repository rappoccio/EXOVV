#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--file', type='string', action='store',
                  dest='file',
                  default = 'jetht.root',
                  help='Input file')


parser.add_option('--outname', type='string', action='store',
                  dest='outname',
                  default = "jetht",
                  help='Output string for output file')




parser.add_option('--plotPre', action='store_true',
                  dest='plotPre',
                  default = False,
                  help='Output string for output file')

(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF
import math
import ROOT
import sys
ROOT.gROOT.Macro("rootlogon.C")

if options.plotPre :
    appendstr = '_pre'
else :
    appendstr = ''

f = ROOT.TFile(options.file)
trigs = [
#    'HLT_PFJet60',
    'HLT_PFJet80' + appendstr,
    'HLT_PFJet140' + appendstr,
    'HLT_PFJet200' + appendstr,
    'HLT_PFJet260' + appendstr,
    'HLT_PFJet320' + appendstr,
    'HLT_PFJet400' + appendstr,
    'HLT_PFJet450' + appendstr,
    #'HLT_PFJet500' 
    ]
import array
ptBinA = array.array('d', [  200., 260., 350., 460., 550., 650., 760.] )
scales = [
    #66, 12, 4, 1, 1, 1
    30000.0 *0.146887199206 ,
    2000.0 * 0.41390688527999997,
    65.63430 *1.723102857142857,
    11.73224 * 0.9871328025,
     3.96795 * 1.3415549004,
     1.23341 * 1.9324477524,
     1.00000 * 1.00000,

    ]
colors = [ #ROOT.kRed + 1,
            ROOT.kWhite, ROOT.kRed - 10, ROOT.kRed - 9, ROOT.kRed - 8, ROOT.kRed - 7, ROOT.kRed - 4, ROOT.kRed - 3, ROOT.kRed, ROOT.kRed + 1,    ]

mcolors = [
    ROOT.kBlack,
    ROOT.kRed,
    ROOT.kGreen + 3,
    ROOT.kBlue,
    ROOT.kOrange,
    ROOT.kMagenta,
    ROOT.kBlack,
    #ROOT.kRed,
    ]

markers =[
    24,
    20,
    21,
    22,
    23,
    29,
    33,
    #34
    ]

    
logy = [ True, True, False, True, True, True, True, True, True, False, False ]
palette = [0, 2]


histnames = ['FatJetPt']#, 'ptAK8', 'yAK8', 'mAK8', 'msoftdropAK8', 'mprunedAK8', 'mtrimmedAK8', 'mfilteredAK8', 'tau21AK8', 'subjetDRAK8', 'jetzAK8']
titles = [
    'Leading AK8 p_{T};p_{T} (GeV)',
#    'AK8 p_{T};p_{T} (GeV)',
#    'AK8 Rapidity;y',
#    'AK8 ungroomed mass;Mass (GeV)',
#    'AK8 soft-drop mass, z_{cut}=0.1, #beta=0;Mass (GeV)',
#    'AK8 pruned mass;Mass (GeV)',
#    'AK8 trimmed mass;Mass (GeV)',
#    'AK8 filtered mass;Mass (GeV)',
#    'AK8 #tau_{21} = #tau_{2} / #tau_{1};#tau_{21}',
#    'AK8 #Delta R between subjets;#Delta R',
#    'AK8 Jet Fragmentation z = min(p_{T}^{i}, p_{T}^{j})/(p_{T}^{i} + p_{T}^{j});z'
    ]
hists = []
stacks = []
canvs = []
legs = []


ROOT.gStyle.SetPadRightMargin(0.15)

for ihist,histname in enumerate(histnames):
    stack = ROOT.THStack(histname + '_stack', titles[ihist])
    canv = ROOT.TCanvas(histname + '_canv', histname +'_canv')
    leg = ROOT.TLegend(0.86, 0.3, 1.0, 0.8)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)    
    for itrig,trigname in enumerate(trigs) :
        s = histname + "_" + trigname
        print 'Getting ' + s
        hist = f.Get( s )
        if not options.plotPre : 
            hist.SetFillColor( colors[itrig] )
        else :
            hist.SetMarkerColor( mcolors[itrig] )
            hist.SetMarkerStyle( markers[itrig] )

        if options.plotPre: 
            hist.Scale( scales[itrig] )
        stack.Add( hist )
        hists.append( hist )
        if not options.plotPre : 
            leg.AddEntry( hist, trigname, 'f')
        else :
            leg.AddEntry( hist, trigname, 'p')

    if not options.plotPre :
        stack.Draw('hist')
    else :
        stack.Draw('nostack e')
    if logy[ihist] : 
        canv.SetLogy()
        stack.SetMinimum(0.1)
    leg.Draw()
    canv.Update()
    canvs.append(canv)
    stacks.append(stack)
    legs.append(leg)
    canv.Print( 'trigplots_' + histname + '_' + options.outname + '.png', 'png')
    canv.Print( 'trigplots_' + histname + '_' + options.outname + '.pdf', 'pdf')


if options.plotPre:
    ratios = []
    cratios = []
    fits = []
    vals = [1.0] * len(hists)
    refHist = [ 1, 3, 4, 6, 6, 6, 6 ]
    ranges = [
        [200,400],
        [500,1000],
        [550,1000],
        [700, 1600],
        [800, 2000],
        [900,2000]
        ]
    for ihist in xrange( len(hists)-2,-1,-1 ) :
        ratio = hists[ihist].Clone()
        ratio.SetName('ratio' + str(ihist) )
        ratio.Sumw2()
        ratio.Divide( hists[ refHist[ihist] ] )
        ratios.append(ratio)
        cratio = ROOT.TCanvas("cratio" + str(ihist),"cratio" + str(ihist))
        minval = ranges[ihist][0]
        maxval = ranges[ihist][1]
        fit = ROOT.TF1('fit' + str(ihist), 'pol0', minval, maxval) 
        ratio.Fit( 'fit' + str(ihist), 'LRM')
        #ratio.GetXaxis().SetRangeUser(minval-50, maxval)
        fits.append(fit)
        ratio.SetMaximum(10)
        val = fit.GetParameter(0)
        vals[ihist] = val
        print '------- FITTED VALUE : ', fit.GetParameter(0)
        cratios.append(cratio)




    for ival in xrange(len(vals)):
        print '%20s : %12.5f * %6.5f' % (trigs[ival], scales[ival], 1.0/vals[ival])
