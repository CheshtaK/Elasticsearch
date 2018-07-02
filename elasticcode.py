# -*- coding: utf-8 -*-
import requests
import sys
import os

import json
import collections
import string

res = requests.get('http://localhost:9200')
print(res.content)

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

book = open(r'enhitr.txt', encoding = 'utf-8')
lineNum = 0 
txtNum = 0 

##for line in book:
##    lineNum += 1
##    print(lineNum)
##    if len(line) > 0:
##            txtNum += 1
##            val = line.split('\t')
##            es.index(index='conversion', doc_type='file', id=txtNum, body = {
##                'Translation': val[0],
##                'English': val[1]
##            }, request_timeout=30)
##    

book.close()

sentence = 'please enter loan amount'

#income
#loan amount
#phone number

t = []

'''Template'''

template = {}
inTemplate = False
template.update({'please enter': ['कृपया', 'दर्ज करें']})

print(template['please enter'][0])

words = sentence.split(' ')
maxlen = 2
index = 0

while index < len(words):
    for i in range(maxlen, 0, -1):
        phrase = ' '.join(words[index:index+i])
        if phrase in template:
            inTemplate = True
            sentence = sentence.replace(phrase,'')
            index += i
            break
    else:
        index += 1

print(sentence)

worde = sentence.split()

for word in worde:
    res = es.search(index='conversion', body={'query': {'match' : { 'English' : word }}})

    reqTranslation = []
    nt = []

    for hit in res['hits']['hits']:
        print(hit['_id'], '->', hit['_source'])
        reqTranslation.append(hit['_source']['Translation'])
        print()

    print(reqTranslation)

    '''Cleaning the corpus - Removing punctuations'''
    translator = str.maketrans('','', string.punctuation)

    for i in range(len(reqTranslation)):
        nt.append(reqTranslation[i].translate(translator))

    print(nt)

    words = [word for line in nt for word in line.split()] 

    print(words,'\n\n')

    counts = collections.Counter(words)

    if counts:
        name1, count1 = counts.most_common(2)[0]
        name2, count2 = counts.most_common(2)[1]
        if count1 == count2:
            t.append(name1+' '+name2)
        else:
            t.append(name1)

if inTemplate == True:
    print('Translation -> ', template['please enter'][0], str(' '.join(t)), template['please enter'][1])

    




