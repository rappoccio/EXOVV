# EXOVV
EXO VV analysis


* Setting up :

```
cmsrel CMSSW_8_0_10_patch2
cd CMSSW_8_0_10_patch2/src
cmsenv
git clone https://github.com/rappoccio/PredictedDistribution.git Analysis/PredictedDistribution
git clone https://github.com/rappoccio/EXOVV.git Analysis/EXOVV
scram b -j 10
cd Analysis/EXOVV/test
```

* To create the mistag rate inputs :
```
python EXOVV_fwlite.py --files QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.txt --outname QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut6_mcut50.root --selection 2 --minAK8Pt 200. --maxAK8Pt 300. --sdmassCutLo 50.0 --makeMistag 

python EXOVV_fwlite.py --files QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.txt --outname QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut7_mcut33.root --selection 2 --minAK8Pt 200. --maxAK8Pt 300. --sdmassCutLo 33.333 --makeMistag --tau21Cut 0.7 

python EXOVV_fwlite.py --files QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.txt --outname QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_pthi_taucut6_mcut50.root --selection 2 --minAK8Pt 300. --maxAK8Pt 30000. --sdmassCutLo 50.0 --makeMistag 
```

* To create the mistag rate itself :
```
python getthatrho.py --selection 2 --fileLo QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut6_mcut50.root --fileLoMod QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_ptlo_taucut7_mcut33.root --fileHi QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_pthi_taucut6_mcut50.root --outname allhad
```

* To create predicted distribution from mistag rates :
```
python EXOVV_fwlite.py --files QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.txt --outname QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_pthi_predicted.root --selection 2 --minAK8Pt 300. --maxAK8Pt 30000. --sdmassCutLo 0.0 --predRate mistagRate_modallhad.root
```

* To plot the observed and predicted :
```
python -i plotobspred.py --file QCD_Pt-15TTo7000_TuneZ2star-Flat_13TeV_pythia6_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_pthi_predicted
```
