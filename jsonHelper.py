# -*- coding: utf-8 -*-

import json


#coverts a JSON file to a text file
def jsonToText(jsonFile, outputFile):
    
    with open('json/'+str(jsonFile)+'_tweets.json') as json_file:
        data = json.load(json_file)
        file = open('people/'+str(outputFile)+'_tweets.txt', 'w+', encoding="utf-8")
        
        for d in data:
            file.write(d['text'])
        file.close()

