python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 0 >& responses_rejec_output_0.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 1 >& responses_rejec_output_1.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 2 >& responses_rejec_output_2.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 3 >& responses_rejec_output_3.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 4 >& responses_rejec_output_4.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 5 >& responses_rejec_output_5.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 6 >& responses_rejec_output_6.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 7 >& responses_rejec_output_7.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 8 >& responses_rejec_output_8.txt &
python responses_otherway.py --outlabel responses_jecsrcs_otherway_qcdmc_2dplots.root --split 9 >& responses_rejec_output_9.txt &



python responses_otherway.py --herwigFlat --outlabel qcdmc_herwig_otherway_rejec_2dplots.root >& responses_rejec_herwig_output.txt &
python make_jackknife_otherway.py >& jackknife_output.txt & 
python plot_trigdists_onthefly_otherway.py  --file jetht_2015_rejec.root  --outname jetht_weighted_dataplots_otherway_rejec.root  >& data_output.txt &
