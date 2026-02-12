import random

def indel_sites(sequence, indel_store=None):
    MAX_VAL = len(sequence)-20

    if indel_store is None:
        indel_store = {}

    
    counter_indels = 0
    original_seq = sequence
    random_list = [MAX_VAL]
    for x in range(9):
        random_list.append(random.randint(0, random_list[-1] - 50))

    print(f"Random Descending List: {random_list}")
    j = random.randint(10,20) 
    
    for i in random_list[:6]: 
        if len(original_seq) == 0:
            raise Exception("Sorry, sequence is too short")
        else:
            original_segment = original_seq[i]
            post_mod_segment = ''.join(random.choices('ACTG', k=j))
            original_seq = (original_seq[:i] + post_mod_segment + original_seq[i+1:])
            ''' create a ground truth vcf''' 
            indel_store[i] = (original_segment, post_mod_segment)
  
    for i in random_list[6:]:
        if len(original_seq) == 0:
            raise Exception("Sorry, sequence is too short")
        else:   
            original = original_seq[i:i+j]
            new = ''
            original_seq = original_seq[:i] + new + original_seq[i+1:]
            ''' create a ground truth vcf''' 
            indel_store[i] = (original, new)
    
    return original_seq, indel_store
        

