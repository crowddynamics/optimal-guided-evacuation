#!/bin/bash

cells=(3 4 5 6 12 13 14 15 16 17 21 22 23 24 25 26 27 28 31 32 33 34 35 36 37 38 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 61 62 63 64 65 66 67 68 71 72 73 74 75 76 77 78 82 83 84 85 86 87 93 94 95 96)
exits=(0 1 2 3 4 5)
tags=(0 1)
ncells=${#cells[@]}
nexits=${#exits[@]}
ntags=${#tags[@]}
population=$1
samples=$2

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell1[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit1[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag1[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${#randtag1[@]}
echo ${#randcell1[@]}
echo ${#randexit1[@]}

echo ${randtag1[*]} >> "tags1_0.txt"
echo ${randcell1[*]} >> "cells1_0.txt"
echo ${randexit1[*]} >> "exits1_0.txt"

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell2[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit2[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag2[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${randtag2[*]} >> "tags2_0.txt"
echo ${randcell2[*]} >> "cells2_0.txt"
echo ${randexit2[*]} >> "exits2_0.txt"

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell3[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit3[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag3[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${randtag3[*]} >> "tags3_0.txt"
echo ${randcell3[*]} >> "cells3_0.txt"
echo ${randexit3[*]} >> "exits3_0.txt"

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell4[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit4[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag4[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${randtag4[*]} >> "tags4_0.txt"
echo ${randcell4[*]} >> "cells4_0.txt"
echo ${randexit4[*]} >> "exits4_0.txt"

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell5[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit5[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag5[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${randtag5[*]} >> "tags5_0.txt"
echo ${randcell5[*]} >> "cells5_0.txt"
echo ${randexit5[*]} >> "exits5_0.txt"

count=1
while [ "$count" -le $population ]; do
  rnd=${cells[$((RANDOM%$ncells))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randcell6[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${exits[$((RANDOM%$nexits))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randexit6[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

count=1
while [ "$count" -le $population ]; do
  rnd=${tags[$((RANDOM%$ntags))]}
  b_count=1
  while [ "$b_count" -le $samples ]; do
    indx=$((($count-1)*$samples + $b_count))
    randtag6[$indx]=$rnd
    let "b_count += 1"
  done
  let "count += 1"
done

echo ${randtag6[*]} >> "tags6_0.txt"
echo ${randcell6[*]} >> "cells6_0.txt"
echo ${randexit6[*]} >> "exits6_0.txt"
