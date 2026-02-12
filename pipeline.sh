#!/bin/bash

# save files independently - folder in github "Sequence reads and reference genomes" 

# use relative path for files 
## inputs: fastq reads, reference 
echo "Running script" 
fasta_reference="$1"
fastq_1="$2"
fastq_2="$3" 

source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate varcall 

minimap2 -a -x sr $fasta_reference $fastq_1 $fastq_2 | samtools view -h -F 0x900 | samtools sort -O bam > sorted_reads.bam

echo "Alignment complete" 

samtools flagstat sorted_reads.bam > map_read_stats  

samtools depth -a sorted_reads.bam > depth.txt

echo "Quality and depth files ready" 

samtools mpileup -Ou -f $fasta_reference sorted_reads.bam | bcftools call -cv -Ov > bcf.vcf

echo "Variant caller bcftools complete" 

samtools index sorted_reads.bam sorted_reads.bai 

echo "Index file for tview complete" 


conda activate snippy

echo "Running snippy variant caller pipeline" 
snippy --outdir $PWD/snippy_vcfpipe --reference $fasta_reference --R1 $fastq_1 --R2 $fastq_2

echo "Snippy output vcf, alignment is available at $PWD/snippy_vcfpipe"
# outputs: depth.txt (confirm coverage / 100bp regions), quality.txt, mapped_reads.bam, .bai file for tview 


