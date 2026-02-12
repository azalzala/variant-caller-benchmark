import argparse 
from argparse import ArgumentParser

parser = argparse.ArgumentParser(description="Process FASTA files")
parser.add_argument("-a", "--simulation",  
                   type=str, 
                   help="Input simulated genome VCF file")
parser.add_argument("-b","--bcf",
                   type=str,
                   help="Input BCF VCF file")
parser.add_argument("-c", "--snippy",
                    default=None, 
                    type=str,
                    help="Input snippy VCF file")

args = parser.parse_args()

def find_pr3(s_pos, b_pos, snippy_pos): 
    tp_bcf = 0
    fn_bcf = 0
    tp_snippy = 0
    fn_snippy = 0
    precision_bcf = 0
    precision_snippy = 0

    for i in s_pos: 
        if i in b_pos: 
            tp_bcf += 1 
        else: 
            fn_bcf += 1
        if i in snippy_pos: 
            tp_snippy += 1 
        else:
            fn_snippy += 1

    fp_bcf = len(b_pos) - tp_bcf
    fp_snippy = len(snippy_pos) - tp_snippy 

    precision_bcf = tp_bcf / (tp_bcf + fp_bcf)
    precision_snippy = tp_snippy / (tp_snippy + fp_bcf)

    recall_bcf = tp_bcf / (tp_bcf + fn_bcf)
    recall_snippy = tp_bcf / (tp_bcf + fn_bcf)

    print(f'Variant caller: \t recall: \t precision: \n')
    print(f' bcftools \t {recall_bcf} \t {precision_bcf}')
    print(f' snippy \t {recall_snippy} \t {precision_snippy}')
    
def find_pr2(s_pos, b_pos):
    tp_bcf = 0
    fn_bcf = 0
    precision_bcf = 0
    try:
        for i in s_pos: 
            if i in b_pos: 
                tp_bcf += 1 
            else: 
                fn_bcf += 1

        fp_bcf = len(b_pos) - tp_bcf

        precision_bcf = tp_bcf / (tp_bcf + fp_bcf)

        recall_bcf = tp_bcf / (tp_bcf + fn_bcf)
    except ZeroDivisionError:
        precision_bcf = 0 
        recall_bcf = 0
        
    print(f'Variant caller:    recall:   precision: \n')
    print(f' bcftools \t {recall_bcf} \t {precision_bcf}')

if args.simulation is None:
    pass
else:
    with open(args.simulation, 'r') as truth_file:
        # have a list of positions column 1 
        # if positions are in bcftools and snippy files check ref - alt columns -> TP_bcf, TP_snippy counter + 1 else FN + 1 
        # total number of the snps / indels 
        # fp are ref in files (count number of lines and subtract TP counter, FP_bcf, FP_snippy)

        vcf = truth_file.readlines()
        s_pos = []
        for line in vcf: 
            line = line.strip()
            if line.startswith('#'):
                continue
            fields = line.split('\t')
            if len(fields) >= 2:
                pos = int(fields[1])
                s_pos.append(pos)
            else:
                print(f"Warning: Malformed VCF line: {line}")
        
if args.bcf is None: 
    pass
else: 
    with open(args.bcf, 'r') as bcf_file: 
        bcf_vcf = bcf_file.readlines()
        b_pos = []
        for line in bcf_vcf:
            line = line.strip()
            if line.startswith('#'):
                continue
            fields = line.split('\t')
            if len(fields) >= 2:
                pos = int(fields[1])
                b_pos.append(pos)
            else:
                print(f"Warning: Malformed VCF line: {line}")

if args.snippy is None: 
    precision_recall_2 = find_pr2(s_pos, b_pos)
    print(precision_recall_2)
else: 
    with open(args.snippy, 'r') as snippy_file:
        snippy_vcf = snippy_file.readlines()
        snippy_pos = []
        for line in snippy_vcf:
            line = line.strip()
            if line.startswith('#'):
                print(line)
                continue
            fields = line.split('\t')
            if len(fields) >= 2:
                pos = int(fields[1])
                snippy_pos.append(pos)
            else:
                print(f"Warning: Malformed VCF line: {line}")

    
    precision_recall_3 = find_pr3(s_pos, b_pos, snippy_pos)
    print(precision_recall_3)