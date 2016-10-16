python responses_otherway.py --outlabel responses_repdf_otherway_qcdmc_2dplots.root >& responses_repdf_output.txt &
python responses_otherway.py --herwigFlat --outlabel qcdmc_herwig_otherway_repdf_2dplots.root >& responses_repdf_herwig_output.txt &
python make_jackknife_otherway.py >& jackknife_output.txt & 
