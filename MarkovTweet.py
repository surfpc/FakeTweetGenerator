'''Markov chain text generation'''
 
from os.path import (expanduser)
from os import (getcwd)
from os import walk
 
from itertools import (starmap)
from functools import (reduce)
from random import (choice)
from textwrap import (fill)

import twitterPeople as tp
import jsonHelper as jh

consumerKey = "#"
consumerSecret = "#"
accessToken = "#-#"
accessSecret = "#"

def test():
    print('test')
 
 
# markovText :: Dict -> [String] -> ([String] -> Bool) -> IO [String]
def markovText(dct):
    '''nGram-hashed word dict -> opening words -> end condition -> text
    '''
    # nGram length
    n = len(list(dct.keys())[0].split()) #0
 
    # step :: [String] -> [String]
    def step(xs):
        return xs + [choice(dct[' '.join(xs[-n:])])]
    return lambda ws: lambda p: (
        until(p)(step)(ws)
    )
 
 
# markovRules :: Int -> [String] -> Dict
def markovRules(n):
    '''All words in ordered list hashed by
       preceding nGrams of length n.
    '''
    def nGramKey(dct, tpl):
        k = ' '.join(list(tpl[:-1]))
        dct[k] = (dct[k] if k in dct else []) + [tpl[-1]]
        return dct
    return lambda ws: reduce(
        nGramKey,
        nGramsFromWords(1 + n)(ws), #1+n
        {}
    )
 
 
# TEST ----------------------------------------------------
# main :: IO ()
def tweet(user_id):
    '''Text generation.'''
    
    #This id changes who the markov chain is impersonating
    twitterId = user_id
    
    #used to determine if the program needs to use tweepy to get the tweets from
    #twitter or if they have already been analyzed
    ppls = []
    direc = getcwd() + '/' + 'people'
    for (dirpath, dirnames, filenames) in walk(direc):
        ppls.extend(filenames)
        break
        
    if not (str(twitterId) + '_tweets.txt') in ppls:
        
        #gets the tweets using the given id number
        tp.getTweets(id_num=twitterId, 
                     consumerKey=consumerKey, 
                     consumerSecret=consumerSecret, 
                     accessToken=accessToken, 
                     accessSecret=accessSecret)
        
        #coverts from a json file to a text file
        jh.jsonToText(twitterId, twitterId)
 
    nGramLength = 3 #3
    dctNGrams = markovRules(nGramLength)(
        readFile(getcwd() + '/' + 'people/' + str(twitterId) + '_tweets.txt').split()
    )
    #print(__doc__ + ':\n')
    
    return fill(
            ' '.join(
                markovText(dctNGrams)(
                    anyNGramWithInitialCap(dctNGrams)
                )(sentenceEndAfterMinWords(30)) #200
            ),
            width=75 #75
        )
    
    #print(
#        fill(
#            ' '.join(
#                markovText(dctNGrams)(
#                    anyNGramWithInitialCap(dctNGrams)
#                )(sentenceEndAfterMinWords(30)) #200
#            ),
#            width=75 #75
#        )
#    )
 
 
# HELPER FUNCTIONS ----------------------------------------
 
# nGramsFromWords :: Int -> [String] -> [Tuple]
def nGramsFromWords(n):
    '''List of nGrams, of length n, derived
       from ordered list of words ws.
    '''
    return lambda ws: zipWithN(lambda *xs: xs)(
        map(lambda i: ws[i:], range(0, n))
    )
 
 
# anyNGramWithInitialCap :: Dict -> [String]
def anyNGramWithInitialCap(dct):
    '''Random pick from nGrams which
       start with capital letters
    '''
    return choice(list(filter(
        lambda k: 1 < len(k) and k[0].isupper() and k[1].islower(),
        dct.keys()
    ))).split()
 
 
# sentenceEndAfterMinWords :: Int -> [String] -> Bool
def sentenceEndAfterMinWords(n):
    '''Predicate :: Sentence punctuation
       after minimum word count
    '''
    return lambda ws: n <= len(ws) and (
        ws[-1][-1] in ['.', "'", '!', '?']
    )
 
 
# GENERIC -------------------------------------------------
 
# readFile :: FilePath -> IO String
def readFile(fp):
    '''The contents of any file at the path
       derived by expanding any ~ in fp.'''
    with open(expanduser(fp), 'r', encoding='utf-8') as f:
        return f.read()
 
 
# until :: (a -> Bool) -> (a -> a) -> a -> a
def until(p):
    '''The result of repeatedly applying f until p holds.
       The initial seed value is x.'''
    def go(f, x):
        v = x
        while not p(v):
            v = f(v)
        return v
    return lambda f: lambda x: go(f, x)
 
 
# zipWithN :: (a -> b -> ... -> c) -> ([a], [b] ...) -> [c]
def zipWithN(f):
    '''A new list constructed by the application of f
       to each tuple in the zip of an arbitrary
       number of existing lists.
    '''
    return lambda xs: list(
        starmap(f, zip(*xs))
    )
 
 
