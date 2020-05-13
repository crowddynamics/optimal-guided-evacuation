#!/bin/bash
#SBATCH -n 1
#SBATCH -t 00:05:00
#SBATCH --mem-per-cpu=1000

module load anaconda3
source activate crowd-development

generation=$1
part=$2
guides=$3

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

if [ $guides -ge "2" ]
then
  # Second gene data
  cells2="cells2_${generation}.txt"
  randcell2=$(cat "$cells2")
  randcell2=($randcell2)

  exits2="exits2_${generation}.txt"
  randexit2=$(cat "$exits2")
  randexit2=($randexit2)

  if [ $guides -ge "3" ]
  then
    # Third gene data
    cells3="cells3_${generation}.txt"
    randcell3=$(cat "$cells3")
    randcell3=($randcell3)

    exits3="exits3_${generation}.txt"
    randexit3=$(cat "$exits3")
    randexit3=($randexit3)

    if [ $guides -ge "4" ]
    then
      # Fourth gene data
      cells4="cells4_${generation}.txt"
      randcell4=$(cat "$cells4")
      randcell4=($randcell4)

      exits4="exits4_${generation}.txt"
      randexit4=$(cat "$exits4")
      randexit4=($randexit4)

      if [ $guides -ge "5" ]
      then
        # Fifth gene data
        cells5="cells5_${generation}.txt"
        randcell5=$(cat "$cells5")
        randcell5=($randcell5)

        exits5="exits5_${generation}.txt"
        randexit5=$(cat "$exits5")
        randexit5=($randexit5)

        if [ $guides -ge "6" ]
        then
          # Sixth gene data
          cells6="cells6_${generation}.txt"
          randcell6=$(cat "$cells6")
          randcell6=($randcell6)

          exits6="exits6_${generation}.txt"
          randexit6=$(cat "$exits6")
          randexit6=($randexit6)
        fi
      fi
    fi
  fi
fi

if [ $part -eq "0" ]
then
  seeds=(${seeds[@]:0:$n_part})
  randcell1=(${randcell1[@]:0:$n_part})
  randexit1=(${randexit1[@]:0:$n_part})
  if [ $guides -ge "2" ]
  then
    randcell2=(${randcell2[@]:0:$n_part})
    randexit2=(${randexit2[@]:0:$n_part})
    if [ $guides -ge "3" ]
    then
      randcell3=(${randcell3[@]:0:$n_part})
      randexit3=(${randexit3[@]:0:$n_part})
      if [ $guides -ge "4" ]
      then
        randcell4=(${randcell4[@]:0:$n_part})
        randexit4=(${randexit4[@]:0:$n_part})
        if [ $guides -ge "5" ]
        then
          randcell5=(${randcell5[@]:0:$n_part})
          randexit5=(${randexit5[@]:0:$n_part})
          if [ $guides -ge "6" ]
          then
            randcell6=(${randcell6[@]:0:$n_part})
            randexit6=(${randexit6[@]:0:$n_part})
          fi
        fi
      fi
    fi
  fi
elif [ $part -eq "1" ]
then
  seeds=(${seeds[@]:$n_part:$(($n_part*2))})
  randcell1=(${randcell1[@]:$n_part:$(($n_part*2))})
  randexit1=(${randexit1[@]:$n_part:$(($n_part*2))})
  if [ $guides -ge "2" ]
  then
    randcell2=(${randcell2[@]:$n_part:$(($n_part*2))})
    randexit2=(${randexit2[@]:$n_part:$(($n_part*2))})
    if [ $guides -ge "3" ]
    then
      randcell3=(${randcell3[@]:$n_part:$(($n_part*2))})
      randexit3=(${randexit3[@]:$n_part:$(($n_part*2))})
      if [ $guides -ge "4" ]
      then
        randcell4=(${randcell4[@]:$n_part:$(($n_part*2))})
        randexit4=(${randexit4[@]:$n_part:$(($n_part*2))})
        if [ $guides -ge "5" ]
        then
          randcell5=(${randcell5[@]:$n_part:$(($n_part*2))})
          randexit5=(${randexit5[@]:$n_part:$(($n_part*2))})
          if [ $guides -ge "6" ]
          then
            randcell6=(${randcell6[@]:$n_part:$(($n_part*2))})
            randexit6=(${randexit6[@]:$n_part:$(($n_part*2))})
          fi
        fi
      fi
    fi
  fi
elif [ $part -eq "2" ]
then
  seeds=(${seeds[@]:$(($n_part*2)):$(($n_part*3))})
  randcell1=(${randcell1[@]:$(($n_part*2)):$(($n_part*3))})
  randexit1=(${randexit1[@]:$(($n_part*2)):$(($n_part*3))})
  if [ $guides -ge "2" ]
  then
    randcell2=(${randcell2[@]:$(($n_part*2)):$(($n_part*3))})
    randexit2=(${randexit2[@]:$(($n_part*2)):$(($n_part*3))})
    if [ $guides -ge "3" ]
    then
      randcell3=(${randcell3[@]:$(($n_part*2)):$(($n_part*3))})
      randexit3=(${randexit3[@]:$(($n_part*2)):$(($n_part*3))})
      if [ $guides -ge "4" ]
      then
        randcell4=(${randcell4[@]:$(($n_part*2)):$(($n_part*3))})
        randexit4=(${randexit4[@]:$(($n_part*2)):$(($n_part*3))})
        if [ $guides -ge "5" ]
        then
          randcell5=(${randcell5[@]:$(($n_part*2)):$(($n_part*3))})
          randexit5=(${randexit5[@]:$(($n_part*2)):$(($n_part*3))})
          if [ $guidfes -ge "6" ]
          then
            randcell6=(${randcell6[@]:$(($n_part*2)):$(($n_part*3))})
            randexit6=(${randexit6[@]:$(($n_part*2)):$(($n_part*3))})
          fi
        fi
      fi
    fi
  fi
else
  seeds=(${seeds[@]:$(($n_part*3)):$(($n_part*4))})
  randcell1=(${randcell1[@]:$(($n_part*3)):$(($n_part*4))})
  randexit1=(${randexit1[@]:$(($n_part*3)):$(($n_part*4))})
  if [ $guides -ge "2" ]
  then
    randcell2=(${randcell2[@]:$(($n_part*3)):$(($n_part*4))})
    randexit2=(${randexit2[@]:$(($n_part*3)):$(($n_part*4))})
    if [ $guides -ge "3" ]
    then
      randcell3=(${randcell3[@]:$(($n_part*3)):$(($n_part*4))})
      randexit3=(${randexit3[@]:$(($n_part*3)):$(($n_part*4))})
      if [ $guides -ge "4" ]
      then
        randcell4=(${randcell4[@]:$(($n_part*3)):$(($n_part*4))})
        randexit4=(${randexit4[@]:$(($n_part*3)):$(($n_part*4))})
        if [ $guides -ge "5" ]
        then
          randcell5=(${randcell5[@]:$(($n_part*3)):$(($n_part*4))})
          randexit5=(${randexit5[@]:$(($n_part*3)):$(($n_part*4))})
          if [ $guides -ge "6" ]
          then
            randcell6=(${randcell6[@]:$(($n_part*3)):$(($n_part*4))})
            randexit6=(${randexit6[@]:$(($n_part*3)):$(($n_part*4))})
          fi
        fi
      fi
    fi
  fi
fi

#cd ..

if [ $guides -eq "1" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi

if [ $guides -eq "2" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi

if [ $guides -eq "3" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${randcell3[$SLURM_ARRAY_TASK_ID]} ${randexit3[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi

if [ $guides -eq "4" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${randcell3[$SLURM_ARRAY_TASK_ID]} ${randexit3[$SLURM_ARRAY_TASK_ID]} ${randcell4[$SLURM_ARRAY_TASK_ID]} ${randexit4[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi

if [ $guides -eq "5" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${randcell3[$SLURM_ARRAY_TASK_ID]} ${randexit3[$SLURM_ARRAY_TASK_ID]} ${randcell4[$SLURM_ARRAY_TASK_ID]} ${randexit4[$SLURM_ARRAY_TASK_ID]} ${randcell5[$SLURM_ARRAY_TASK_ID]} ${randexit5[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi

if [ $guides -eq "6" ]
then
python shell_run_simple_nohidden_stochastic.py ${randcell1[$SLURM_ARRAY_TASK_ID]} ${randexit1[$SLURM_ARRAY_TASK_ID]} ${randcell2[$SLURM_ARRAY_TASK_ID]} ${randexit2[$SLURM_ARRAY_TASK_ID]} ${randcell3[$SLURM_ARRAY_TASK_ID]} ${randexit3[$SLURM_ARRAY_TASK_ID]} ${randcell4[$SLURM_ARRAY_TASK_ID]} ${randexit4[$SLURM_ARRAY_TASK_ID]} ${randcell5[$SLURM_ARRAY_TASK_ID]} ${randexit5[$SLURM_ARRAY_TASK_ID]} ${randcell6[$SLURM_ARRAY_TASK_ID]} ${randexit6[$SLURM_ARRAY_TASK_ID]} ${seeds[$SLURM_ARRAY_TASK_ID]}
fi
