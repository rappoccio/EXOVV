#!/bin/bash 

python restrict_xaxis.py --files "inputs/rawout_fullxs_absolute[1-6].root" --xmin 20 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_normalized[1-6].root" --xmin 20 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_absolute[7-9].root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_normalized[7-9].root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_absolute10.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_normalized10.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_absolute11.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_normalized11.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_absolute12.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/rawout_fullxs_normalized12.root" --xmin 40 --xmax 2000
python restrict_xaxis.py --files "inputs/*softdrop*.root" --xmin 10 --xmax 2000
