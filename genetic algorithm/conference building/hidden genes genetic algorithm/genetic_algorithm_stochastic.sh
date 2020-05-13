#!/bin/bash
#SBATCH -n 1
#SBATCH -t 01:00:00
#SBATCH --mem-per-cpu=10000

module load anaconda3
source activate crowd-development

generation=$1
part=$2

seeds="seeds.txt"
seeds=$(cat "$seeds")
seeds=($seeds)
n_simulations=${#seeds[@]}
n_part=$(($n_simulations/4))

# First gene data
cells1="cells1_${generation}.txt"
randcell1=$(cat "$cells1")
randcell1=($randcell1)

exits1="exits1_${generation}.txt"
randexit1=$(cat "$exits1")
randexit1=($randexit1)

tags1="tags1_${generation}.txt"
randtag1=$(cat "$tags1")
randtag1=($randtag1)

# Second gene data
cells2="cells2_${generation}.txt"
randcell2=$(cat "$cells2")
randcell2=($randcell2)

exits2="exits2_${generation}.txt"
randexit2=$(cat "$exits2")
randexit2=($randexit2)

tags2="tags2_${generation}.txt"
randtag2=$(cat "$tags2")
randtag2=($randtag2)

# Third gene data
cells3="cells3_${generation}.txt"
randcell3=$(cat "$cells3")
randcell3=($randcell3)

exits3="exits3_${generation}.txt"
randexit3=$(cat "$exits3")
randexit3=($randexit3)

tags3="tags3_${generation}.txt"
randtag3=$(cat "$tags3")
randtag3=($randtag3)

# Fourth gene data
cells4="cells4_${generation}.txt"
randcell4=$(cat "$cells4")
randcell4=($randcell4)

exits4="exits4_${generation}.txt"
randexit4=$(cat "$exits4")
randexit4=($randexit4)

tags4="tags4_${generation}.txt"
randtag4=$(cat "$tags4")
randtag4=($randtag4)

# Fifth gene data
cells5="cells5_${generation}.txt"
randcell5=$(cat "$cells5")
randcell5=($randcell5)

exits5="exits5_${generation}.txt"
randexit5=$(cat "$exits5")
randexit5=($randexit5)

tags5="tags5_${generation}.txt"
randtag5=$(cat "$tags5")
randtag5=($randtag5)

# Sixth gene data
cells6="cells6_${generation}.txt"
randcell6=$(cat "$cells6")
randcell6=($randcell6)

exits6="exits6_${generation}.txt"
randexit6=$(cat "$exits6")
randexit6=($randexit6)

tags6="tags6_${generation}.txt"
randtag6=$(cat "$tags6")
randtag6=($randtag6)

# Seventh gene data
cells7="cells7_${generation}.txt"
randcell7=$(cat "$cells7")
randcell7=($randcell7)

exits7="exits7_${generation}.txt"
randexit7=$(cat "$exits7")
randexit7=($randexit7)

tags7="tags7_${generation}.txt"
randtag7=$(cat "$tags7")
randtag7=($randtag7)

# Eight gene data
cells8="cells8_${generation}.txt"
randcell8=$(cat "$cells8")
randcell8=($randcell8)

exits8="exits8_${generation}.txt"
randexit8=$(cat "$exits8")
randexit8=($randexit8)

tags8="tags8_${generation}.txt"
randtag8=$(cat "$tags8")
randtag8=($randtag8)

# Ninth gene data
cells9="cells9_${generation}.txt"
randcell9=$(cat "$cells9")
randcell9=($randcell9)

exits9="exits9_${generation}.txt"
randexit9=$(cat "$exits9")
randexit9=($randexit9)

tags9="tags9_${generation}.txt"
randtag9=$(cat "$tags9")
randtag9=($randtag9)

# Tenth gene data
cells10="cells10_${generation}.txt"
randcell10=$(cat "$cells10")
randcell10=($randcell10)

exits10="exits10_${generation}.txt"
randexit10=$(cat "$exits10")
randexit10=($randexit10)

tags10="tags10_${generation}.txt"
randtag10=$(cat "$tags10")
randtag10=($randtag10)


if [ $part -eq "0" ]
then
  seeds=(${seeds[@]:0:$n_part})
  randcell1=(${randcell1[@]:0:$n_part})
  randexit1=(${randexit1[@]:0:$n_part})
  randtag1=(${randtag1[@]:0:$n_part})
  randcell2=(${randcell2[@]:0:$n_part})
  randexit2=(${randexit2[@]:0:$n_part})
  randtag2=(${randtag2[@]:0:$n_part})
  randcell3=(${randcell3[@]:0:$n_part})
  randexit3=(${randexit3[@]:0:$n_part})
  randtag3=(${randtag3[@]:0:$n_part})
  randcell4=(${randcell4[@]:0:$n_part})
  randexit4=(${randexit4[@]:0:$n_part})
  randtag4=(${randtag4[@]:0:$n_part})
  randcell5=(${randcell5[@]:0:$n_part})
  randexit5=(${randexit5[@]:0:$n_part})
  randtag5=(${randtag5[@]:0:$n_part})
  randcell6=(${randcell6[@]:0:$n_part})
  randexit6=(${randexit6[@]:0:$n_part})
  randtag6=(${randtag6[@]:0:$n_part})
  randcell7=(${randcell7[@]:0:$n_part})
  randexit7=(${randexit7[@]:0:$n_part})
  randtag7=(${randtag7[@]:0:$n_part})
  randcell8=(${randcell8[@]:0:$n_part})
  randexit8=(${randexit8[@]:0:$n_part})
  randtag8=(${randtag8[@]:0:$n_part})
  randcell9=(${randcell9[@]:0:$n_part})
  randexit9=(${randexit9[@]:0:$n_part})
  randtag9=(${randtag9[@]:0:$n_part})
  randcell10=(${randcell10[@]:0:$n_part})
  randexit10=(${randexit10[@]:0:$n_part})
  randtag10=(${randtag10[@]:0:$n_part})

elif [ $part -eq "1" ]
then
  seeds=(${seeds[@]:$n_part:$(($n_part*2))})
  randcell1=(${randcell1[@]:$n_part:$(($n_part*2))})
  randexit1=(${randexit1[@]:$n_part:$(($n_part*2))})
  randtag1=(${randtag1[@]:$n_part:$(($n_part*2))})
  randcell2=(${randcell2[@]:$n_part:$(($n_part*2))})
  randexit2=(${randexit2[@]:$n_part:$(($n_part*2))})
  randtag2=(${randtag2[@]:$n_part:$(($n_part*2))})
  randcell3=(${randcell3[@]:$n_part:$(($n_part*2))})
  randexit3=(${randexit3[@]:$n_part:$(($n_part*2))})
  randtag3=(${randtag3[@]:$n_part:$(($n_part*2))})
  randcell4=(${randcell4[@]:$n_part:$(($n_part*2))})
  randexit4=(${randexit4[@]:$n_part:$(($n_part*2))})
  randtag4=(${randtag4[@]:$n_part:$(($n_part*2))})
  randcell5=(${randcell5[@]:$n_part:$(($n_part*2))})
  randexit5=(${randexit5[@]:$n_part:$(($n_part*2))})
  randtag5=(${randtag5[@]:$n_part:$(($n_part*2))})
  randcell6=(${randcell6[@]:$n_part:$(($n_part*2))})
  randexit6=(${randexit6[@]:$n_part:$(($n_part*2))})
  randtag6=(${randtag6[@]:$n_part:$(($n_part*2))})
  randcell7=(${randcell7[@]:$n_part:$(($n_part*2))})
  randexit7=(${randexit7[@]:$n_part:$(($n_part*2))})
  randtag7=(${randtag7[@]:$n_part:$(($n_part*2))})
  randcell8=(${randcell8[@]:$n_part:$(($n_part*2))})
  randexit8=(${randexit8[@]:$n_part:$(($n_part*2))})
  randtag8=(${randtag8[@]:$n_part:$(($n_part*2))})
  randcell9=(${randcell9[@]:$n_part:$(($n_part*2))})
  randexit9=(${randexit9[@]:$n_part:$(($n_part*2))})
  randtag9=(${randtag9[@]:$n_part:$(($n_part*2))})
  randcell10=(${randcell10[@]:$n_part:$(($n_part*2))})
  randexit10=(${randexit10[@]:$n_part:$(($n_part*2))})
  randtag10=(${randtag10[@]:$n_part:$(($n_part*2))})

elif [ $part -eq "2" ]
then
  seeds=(${seeds[@]:$(($n_part*2)):$(($n_part*3))})
  randcell1=(${randcell1[@]:$(($n_part*2)):$(($n_part*3))})
  randexit1=(${randexit1[@]:$(($n_part*2)):$(($n_part*3))})
  randtag1=(${randtag1[@]:$(($n_part*2)):$(($n_part*3))})
  randcell2=(${randcell2[@]:$(($n_part*2)):$(($n_part*3))})
  randexit2=(${randexit2[@]:$(($n_part*2)):$(($n_part*3))})
  randtag2=(${randtag2[@]:$(($n_part*2)):$(($n_part*3))})
  randcell3=(${randcell3[@]:$(($n_part*2)):$(($n_part*3))})
  randexit3=(${randexit3[@]:$(($n_part*2)):$(($n_part*3))})
  randtag3=(${randtag3[@]:$(($n_part*2)):$(($n_part*3))})
  randcell4=(${randcell4[@]:$(($n_part*2)):$(($n_part*3))})
  randexit4=(${randexit4[@]:$(($n_part*2)):$(($n_part*3))})
  randtag4=(${randtag4[@]:$(($n_part*2)):$(($n_part*3))})
  randcell5=(${randcell5[@]:$(($n_part*2)):$(($n_part*3))})
  randexit5=(${randexit5[@]:$(($n_part*2)):$(($n_part*3))})
  randtag5=(${randtag5[@]:$(($n_part*2)):$(($n_part*3))})
  randcell6=(${randcell6[@]:$(($n_part*2)):$(($n_part*3))})
  randexit6=(${randexit6[@]:$(($n_part*2)):$(($n_part*3))})
  randtag6=(${randtag6[@]:$(($n_part*2)):$(($n_part*3))})
  randcell7=(${randcell7[@]:$(($n_part*2)):$(($n_part*3))})
  randexit7=(${randexit7[@]:$(($n_part*2)):$(($n_part*3))})
  randtag7=(${randtag7[@]:$(($n_part*2)):$(($n_part*3))})
  randcell8=(${randcell8[@]:$(($n_part*2)):$(($n_part*3))})
  randexit8=(${randexit8[@]:$(($n_part*2)):$(($n_part*3))})
  randtag8=(${randtag8[@]:$(($n_part*2)):$(($n_part*3))})
  randcell9=(${randcell9[@]:$(($n_part*2)):$(($n_part*3))})
  randexit9=(${randexit9[@]:$(($n_part*2)):$(($n_part*3))})
  randtag9=(${randtag9[@]:$(($n_part*2)):$(($n_part*3))})
  randcell10=(${randcell10[@]:$(($n_part*2)):$(($n_part*3))})
  randexit10=(${randexit10[@]:$(($n_part*2)):$(($n_part*3))})
  randtag10=(${randtag10[@]:$(($n_part*2)):$(($n_part*3))})

else
  seeds=(${seeds[@]:$(($n_part*3)):$(($n_part*4))})
  randcell1=(${randcell1[@]:$(($n_part*3)):$(($n_part*4))})
  randexit1=(${randexit1[@]:$(($n_part*3)):$(($n_part*4))})
  randtag1=(${randtag1[@]:$(($n_part*3)):$(($n_part*4))})
  randcell2=(${randcell2[@]:$(($n_part*3)):$(($n_part*4))})
  randexit2=(${randexit2[@]:$(($n_part*3)):$(($n_part*4))})
  randtag2=(${randtag2[@]:$(($n_part*3)):$(($n_part*4))})
  randcell3=(${randcell3[@]:$(($n_part*3)):$(($n_part*4))})
  randexit3=(${randexit3[@]:$(($n_part*3)):$(($n_part*4))})
  randtag3=(${randtag3[@]:$(($n_part*3)):$(($n_part*4))})
  randcell4=(${randcell4[@]:$(($n_part*3)):$(($n_part*4))})
  randexit4=(${randexit4[@]:$(($n_part*3)):$(($n_part*4))})
  randtag4=(${randtag4[@]:$(($n_part*3)):$(($n_part*4))})
  randcell5=(${randcell5[@]:$(($n_part*3)):$(($n_part*4))})
  randexit5=(${randexit5[@]:$(($n_part*3)):$(($n_part*4))})
  randtag5=(${randtag5[@]:$(($n_part*3)):$(($n_part*4))})
  randcell6=(${randcell6[@]:$(($n_part*3)):$(($n_part*4))})
  randexit6=(${randexit6[@]:$(($n_part*3)):$(($n_part*4))})
  randtag6=(${randtag6[@]:$(($n_part*3)):$(($n_part*4))})
  randcell7=(${randcell7[@]:$(($n_part*3)):$(($n_part*4))})
  randexit7=(${randexit7[@]:$(($n_part*3)):$(($n_part*4))})
  randtag7=(${randtag7[@]:$(($n_part*3)):$(($n_part*4))})
  randcell8=(${randcell8[@]:$(($n_part*3)):$(($n_part*4))})
  randexit8=(${randexit8[@]:$(($n_part*3)):$(($n_part*4))})
  randtag8=(${randtag8[@]:$(($n_part*3)):$(($n_part*4))})
  randcell9=(${randcell9[@]:$(($n_part*3)):$(($n_part*4))})
  randexit9=(${randexit9[@]:$(($n_part*3)):$(($n_part*4))})
  randtag9=(${randtag9[@]:$(($n_part*3)):$(($n_part*4))})
  randcell10=(${randcell10[@]:$(($n_part*3)):$(($n_part*4))})
  randexit10=(${randexit10[@]:$(($n_part*3)):$(($n_part*4))})
  randtag10=(${randtag10[@]:$(($n_part*3)):$(($n_part*4))})

fi

#cd ..

python shell_run_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randtag1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${randtag2[$SLURM_ARRAY_TASK_ID]} ${randcell3[$SLURM_ARRAY_TASK_ID]} ${randexit3[$SLURM_ARRAY_TASK_ID]} ${randtag3[$SLURM_ARRAY_TASK_ID]} ${randcell4[$SLURM_ARRAY_TASK_ID]} ${randexit4[$SLURM_ARRAY_TASK_ID]} ${randtag4[$SLURM_ARRAY_TASK_ID]} ${randcell5[$SLURM_ARRAY_TASK_ID]} ${randexit5[$SLURM_ARRAY_TASK_ID]} ${randtag5[$SLURM_ARRAY_TASK_ID]} ${randcell6[$SLURM_ARRAY_TASK_ID]} ${randexit6[$SLURM_ARRAY_TASK_ID]} ${randtag6[$SLURM_ARRAY_TASK_ID]} ${randcell7[$SLURM_ARRAY_TASK_ID]} ${randexit7[$SLURM_ARRAY_TASK_ID]} ${randtag7[$SLURM_ARRAY_TASK_ID]} ${randcell8[$SLURM_ARRAY_TASK_ID]} ${randexit8[$SLURM_ARRAY_TASK_ID]} ${randtag8[$SLURM_ARRAY_TASK_ID]} ${randcell9[$SLURM_ARRAY_TASK_ID]} ${randexit9[$SLURM_ARRAY_TASK_ID]} ${randtag9[$SLURM_ARRAY_TASK_ID]} ${randcell10[$SLURM_ARRAY_TASK_ID]} ${randexit10[$SLURM_ARRAY_TASK_ID]} ${randtag10[$SLURM_ARRAY_TASK_ID]}  ${seeds[$SLURM_ARRAY_TASK_ID]}
