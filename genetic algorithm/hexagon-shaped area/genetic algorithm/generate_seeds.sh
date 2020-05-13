#!/bin/bash

population=$1
samples=$2
MAXCOUNT=$(($population*$samples))

count=1
seed=0
while [ "$count" -le $MAXCOUNT ]; do
  seeds[$count]=$seed
  let "seed += 1"
  echo $seed
  if [ "$seed" -eq $samples ]
  then
    seed=0
  fi
  let "count += 1"
done

echo ${seeds[*]} >> seeds.txt

