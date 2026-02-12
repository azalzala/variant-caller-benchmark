with open('EcoliK12-MG1655.fasta', 'r') as f: 
    lines = f.readlines()
    sequence_original = ''.join(lines)
    print(len(sequence_original))
with open('output.fasta', 'r') as m: 
    all_reads = m.readlines()
    sequence_mutated = ''.join(all_reads)
    print(len(sequence_mutated))

def count_differing_positions(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

result = count_differing_positions(sequence_original, sequence_mutated)
print(result)

