import random
import numpy as np
import pdb


def weighted_random_sample(d):
    """
    Input: a dictioanry
    Output: a weighted random sample of the key from the dictionary

    Example: 
    If the input is: d = { "a": 3, "b": 7 }
    then, the output has 30% probability of "a" and 70% probability of "b"
    """

    # TODO
    # Hint: use "np.random.choice" function. The probability should sum to 1
    #       test "np.random.choice" first, and try to understand how it works. 
    #       https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html

    vals = list(d.values())
    rst =  np.random.choice( list(d.keys()) ,1, p = np.array(vals)/np.sum(vals) )
    return rst[0]


d = {'a': 10, 'z':20, 'b':30, 'c':40 }

print(weighted_random_sample(d))

# %%
    
class Markov_Chain:
    def __init__(self):
        self.dict = {}


    def learn( self, text ):
        """
        Input: a string of text
        Effect: learn the Character-based model of text.
        """
        # TODO: learn the model, use the 'self.dict' dictionary。
        # Do NOT use tokenization, because it's a character-level Markov Chain

        for i in range( len(text)  - 1 ):
            if text[i] not in self.dict: self.dict[ text[i] ] = {}

            if text[i+1] not in self.dict[ text[i] ]:
                self.dict[ text[i] ][ text[i+1] ] = 1
            else:
                self.dict[ text[i] ][ text[i+1] ] += 1

        return


    def generate( self, max_len, seed = None):
        """ Inference of Markov Chain
        Input: the maximum length of generated string
        Output: a randomly generated string within the length of "max_len"
        """
        
        if seed is not None: random.seed( seed )
        
        curr_word = random.choice( list(self.dict.keys()) ) # randomly choose the first word

        rst = ""
        
        # TODO
        # Hint: pay attention to the case when the generation hit end

        while len(rst) < max_len:
            if curr_word not in self.dict: break
            curr_word = weighted_random_sample( self.dict[ curr_word ] )
            rst += curr_word
        
        return rst




#%%  test
if __name__ == "__main__":
#    m = Markov_Chain()
#    m.learn( "科学技术是第一生产力！" )
#    for _ in range(10):
#    print( m.generate( 30 , seed = None ) )
        
        
    m = Markov_Chain()
    f = open( "poets.txt" , "r", encoding = "utf-8" )
    for line in f:
        if len(line) > 5: m.learn( line.strip() )
        
    # %%
    for _ in range(10):
        print( m.generate( 10 ) )
    
    