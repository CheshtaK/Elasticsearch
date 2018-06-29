# -*- coding: utf-8 -*-
import requests
import sys
import os

import json
import collections

res = requests.get('http://localhost:9200')
print(res.content)

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

book = open(r'paytm2.txt', encoding = 'utf-8')
lineNum = 0 
txtNum = 0 

##for line in book:
##    lineNum += 1
##    if len(line) > 0:
##            txtNum += 1
##            val = line.split('\t')
##            es.index(index='conversion', doc_type='file', id=txtNum, body = {
##                'Translation': val[0],
##                'English': val[1]
##            })
    

book.close()

sentence = 'science and diploma'

worde = sentence.split()
print(worde)

t = []

for word in worde:
    res = es.search(index='conversion', body={'query': {'match' : { 'English' : word }}})

    reqTranslation = []

    for hit in res['hits']['hits']:
        print(hit['_id'], '->', hit['_source'])
        reqTranslation.append(hit['_source']['Translation'])
        print()

    print(reqTranslation)

    words = [word for line in reqTranslation for word in line.split()] 

    print(words,'\n\n')

    counts = collections.Counter(words)

    if counts:
        name, count = counts.most_common(1)[0]
        t.append(name)

print('Translation -> ', str(' '.join(t)))
    




