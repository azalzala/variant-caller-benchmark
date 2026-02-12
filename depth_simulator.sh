#!/bin/bash

fasta="$1"
fastq1="$2"
fastq2="$3"
echo "Running script" 
echo "Calculating depth" 
length=$(sed '1d' $fasta | wc -c)
depth=$(($length*30/100))
echo "$depth"

wgsim -1 100 -2 100 -N $depth -e0.0001 -R0 -r0 -X0 -S4 $fasta $fastq1 $fastq2
