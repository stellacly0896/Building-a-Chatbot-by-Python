def word_edit_distance(x, y):
    """
    For simplicity, you can assume the input string would not contain punctuation.
    
    The comparison should not be case-sensitive
    
    """
    # TODO
    if len(x) < len(y): return word_edit_distance(y, x) # ensure s1 is longer
    if len(y) == 0: return len(x)
    
    s1 = x.lower().split()
    s2 = y.lower().split()
    previous_row = range( len(s2) + 1)
    

    for i, c1 in enumerate(s1):
        current_row = [i + 1]    
        for j, c2 in enumerate(s2):
            insertions = previous_row[j+1]  + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
    
            current_row.append( min( insertions, deletions, substitutions ) )      
        
        previous_row = current_row
        
    return previous_row[-1]



if __name__ == "__main__":
    print(word_edit_distance("TO BE OR NOT TO BE IS A QUESTION" , "to be or not to be is a question")) # 0
    
    print(word_edit_distance("Apple and Banana" , "apple banana")) # 1
    
    
    print(word_edit_distance("the quick brown fox jumped over the lazy dog" , "The slow brown fox jumped over the tired dog"))
    
