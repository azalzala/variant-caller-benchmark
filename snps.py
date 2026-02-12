import random 

random.seed(30)

def repeat_point(sequence, n, store=None):
    if store is None:
        store = {}
        
    if n == 0:
        return sequence, store

    i = random.randrange(len(sequence))  # 0 .. len-1
    
    original = sequence[i]
    
    nt = 'ACTG'
    new = random.choice(nt)
    
    # ensure new != original
    while new == original:
        new = random.choice(nt)
        
    # record mutation
    store[i] = (original, new)
    
    # apply mutation
    sequence_list = list(sequence)
    sequence_list[i] = new
    new_sequence = "".join(sequence_list)
    
    # recurse
    return repeat_point(new_sequence, n-1, store)
 