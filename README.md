# variant-caller-benchmark
Research Project 1B Course Assessment

# H1 Evaluating the performance

The variant callers used are snippy and bcftools. Unlike Snippy, bcftools requires pre-processing with samtools mpileup to select for variants including small-variants like indels and point mutations from the alignment file. The snippy toolbox generates outputs including the final vcf for comparing with the ground truth vcf that was generated in the beginning. 

## H2 Part 1: 
#### h4 Intakes a reference genome for E.coli genomes and simulates SNP and Indel Mutations at 30x depth for 100bp reads with a ground truth VCF

`code`mkdir <output_dir> 
Download mutations_depth.py, differences_fasta.py and depth_simulator.sh 
`code`python mutations_depth.py <input.fasta> <output.fasta> <output.vcf> 
`code`python differences_fasta.py > <output_file.txt> 
`code`./depth_simulator.sh <input.fasta> <single/paired end files> (absolute path only)

## H2 Part 2: 
#### h4 Implements two variant callers and evaluates performance  

- SRR25083113_1.fastq.gz and SRR25083113_2.fastq.gz
- Reference EcoliK12-MG1655.fasta

`code` gzip read1 read2
`code` chmod +x pipeline.sh 
`code`./pipeline.sh fasta_reference read1 read2
`code` python evaluateVCF.py -a output.vcf -b bcf -c snippy empty-text-file.txt
    

## h2 Common issues
- Environment issue: Errors with environment resolved using separate environments for bcftools and snippy. Requires two conda environments with separate versioning due to compatibility issues. 
    - bcftools samtools=1.22 
    - snippy samtools>=1.6
- Algorithm issue: Indels in output.vcf not conducive with output.fasta following check with differences_fasta_files.py 
    - Next steps: experiment with SNPs only, test changing variable names as possible source of error 

## H2 Evaluation 

The precision and recall stats are available in the output file of evaluateVCF.py. These indicate issues with the pipeline, one occuring at the mutation simulation stage and the second after simulating read depth with wgsim. In the first instance it is possible to modify the mutations_depth.py script to only introduce SNPs which are verified in the output.fasta by the test python script. However, the variant callers benchmark performance are still 0 on both precision and recall. After testing the script multiple times the issue can be narrowed down to tool samtools compatibility issues. 


