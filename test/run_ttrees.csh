python responses_otherway.py --outlabel responses_rejec_otherway_qcdmc_2dplots.root >& responses_rejec_output.txt &
python responses_otherway.py --herwigFlat --outlabel qcdmc_herwig_otherway_rejec_2dplots.root >& responses_rejec_herwig_output.txt &
python make_jackknife_otherway.py >& jackknife_output.txt & 
