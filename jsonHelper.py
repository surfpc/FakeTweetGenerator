# -*- coding: utf-8 -*-

import json


def jsonToText(jsonFile, outputFile):
    
    with open('json/'+str(jsonFile)+'_tweets.json') as json_file:
        data = json.load(json_file)
        file = open('people/'+str(outputFile)+'_tweets.txt', 'w+', encoding="utf-8")
        
        for d in data:
            #file.write('')
            file.write(d['text'])
        file.close()

