import os
from snps import repeat_point
from indel_sites import indel_sites
from pathlib import Path
import argparse 
from argparse import ArgumentParser

def file_in_cwd(file_path):
    """Custom type: ensures file exists in current directory"""
    cwd_file = Path.cwd() / file_path
    if cwd_file.is_file():
        return str(cwd_file.absolute())  # Return absolute path
    else:
        raise argparse.ArgumentTypeError(f"'{file_path}' not found in {Path.cwd()}")

# Create parser
parser = argparse.ArgumentParser(description="Process FASTA files")
parser.add_argument("input_fasta", 
                   type=file_in_cwd, 
                   help="Input FASTA file (in current directory)")
parser.add_argument("output_fasta", 
                   default="output.fasta",
                   type=str,
                   help="Output file (default: output.fasta in current dir)")
parser.add_argument("output_vcf", 
                    type=str,
                    help="Output file for stores of indels and SNPs")

args = parser.parse_args()

with open(args.input_fasta, 'r') as f:
    lines = f.readlines()
    header = lines[0]
    extract_chr = header[1:13]
    sequence_joined = ''.join(line for line in lines[1:])
    length = len(sequence_joined)

new_sequence, store = repeat_point(sequence_joined, 10) # list object of two items [0] = sequence and [1] = store of snps 
mutated_sequence, indel_store = indel_sites(new_sequence)

## write indels.fasta with output of snps
with open(args.output_fasta, 'x') as f: 
    f.write(f"{header}{mutated_sequence}")


## write text file 
with open(args.output_vcf, 'w') as c:
    c.write(f''''##file.format=VCFv4.2\n##contig<ID={extract_chr}, length = {length}\n#CHROM \t POS \t REF \t ALT \t QUAL \t FILTER \t INFO \n''')
    for i, x in store.items(): 
        c.write(f'{extract_chr} \t {i} \t {x[0]} \t {x[1]} \t . \t PASS \t . \n')
    for j, y in indel_store.items():
        c.write(f'{extract_chr} \t {j} \t {y[0]} \t {y[1]} \t . \t PASS \t . \n')

