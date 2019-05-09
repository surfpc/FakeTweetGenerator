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

#consumerKey = "#"
#consumerSecret = "#"
#accessToken = "#-#"
#accessSecret = "#"
 
class MarkovTweet: 
    
    consumerKey = ""
    consumerSecret = ""
    accessToken = ""
    accessSecret = ""
    
    def __init__(self, consumerKey, consumerSecret, accessToken, accessSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessToken = accessToken
        self.accessSecret = accessSecret
        
    def updateValues(self, consumerKey, consumerSecret, accessToken, accessSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessToken = accessToken
        self.accessSecret = accessSecret
    
    # markovText :: Dict -> [String] -> ([String] -> Bool) -> IO [String]
    def markovText(self, dct):
        '''nGram-hashed word dict -> opening words -> end condition -> text
        '''
        # nGram length
        n = len(list(dct.keys())[0].split()) #0
     
        # step :: [String] -> [String]
        def step(xs):
            return xs + [choice(dct[' '.join(xs[-n:])])]
        return lambda ws: lambda p: (
            self.until(p)(step)(ws)
        )
     
     
    # markovRules :: Int -> [String] -> Dict
    def markovRules(self, n):
        '''All words in ordered list hashed by
           preceding nGrams of length n.
        '''
        def nGramKey(dct, tpl):
            k = ' '.join(list(tpl[:-1]))
            dct[k] = (dct[k] if k in dct else []) + [tpl[-1]]
            return dct
        return lambda ws: reduce(
            nGramKey,
            self.nGramsFromWords(1 + n)(ws), #1+n
            {}
        )
     
     
    # TWEET ----------------------------------------------------
    def tweet(self, user_id):
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
                         consumerKey=self.consumerKey, 
                         consumerSecret=self.consumerSecret, 
                         accessToken=self.accessToken, 
                         accessSecret=self.accessSecret)
            
            #coverts from a json file to a text file
            jh.jsonToText(twitterId, twitterId)
     
        nGramLength = 3 #3
        dctNGrams = self.markovRules(nGramLength)(
            self.readFile(getcwd() + '/' + 'people/' + str(twitterId) + '_tweets.txt').split()
        )
        #print(__doc__ + ':\n')
        
        return fill(
                ' '.join(
                    self.markovText(dctNGrams)(
                        self.anyNGramWithInitialCap(dctNGrams)
                    )(self.sentenceEndAfterMinWords(30)) #200
                ),
                width=75 #75
            )
     
     
    # HELPER FUNCTIONS ----------------------------------------
     
    # nGramsFromWords :: Int -> [String] -> [Tuple]
    def nGramsFromWords(self, n):
        '''List of nGrams, of length n, derived
           from ordered list of words ws.
        '''
        return lambda ws: self.zipWithN(lambda *xs: xs)(
            map(lambda i: ws[i:], range(0, n))
        )
     
     
    # anyNGramWithInitialCap :: Dict -> [String]
    def anyNGramWithInitialCap(self, dct):
        '''Random pick from nGrams which
           start with capital letters
        '''
        return choice(list(filter(
            lambda k: 1 < len(k) and k[0].isupper() and k[1].islower(),
            dct.keys()
        ))).split()
     
     
    # sentenceEndAfterMinWords :: Int -> [String] -> Bool
    def sentenceEndAfterMinWords(self, n):
        '''Predicate :: Sentence punctuation
           after minimum word count
        '''
        return lambda ws: n <= len(ws) and (
            ws[-1][-1] in ['.', "'", '!', '?']
        )
     
     
    # GENERIC -------------------------------------------------
     
    # readFile :: FilePath -> IO String
    def readFile(self, fp):
        '''The contents of any file at the path
           derived by expanding any ~ in fp.'''
        with open(expanduser(fp), 'r', encoding='utf-8') as f:
            return f.read()
     
     
    # until :: (a -> Bool) -> (a -> a) -> a -> a
    def until(self, p):
        '''The result of repeatedly applying f until p holds.
           The initial seed value is x.'''
        def go(f, x):
            v = x
            while not p(v):
                v = f(v)
            return v
        return lambda f: lambda x: go(f, x)
     
     
    # zipWithN :: (a -> b -> ... -> c) -> ([a], [b] ...) -> [c]
    def zipWithN(self, f):
        '''A new list constructed by the application of f
           to each tuple in the zip of an arbitrary
           number of existing lists.
        '''
        return lambda xs: list(
            starmap(f, zip(*xs))
        )
 
 
