#!/bin/bash
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH --mem-per-cpu=2000

module load anaconda3
source activate crowd-development

echo $1
echo $2
echo $3
echo $4
echo $5
echo $6
echo $7
python selection_stochastic.py $1 $2 $3 $4 $5 $6 $7
rm *.out
