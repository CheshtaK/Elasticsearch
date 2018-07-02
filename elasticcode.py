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

sentence = 'please enter valid mobile'

'''please enter lan number'''
'''please enter valid loan income'''
'''please enter valid mobile'''

res = es.search(index='conversion', body={'query': {'match' : { 'English' : sentence }}})

english = []
hindi = []
temp = []
nenglish = []
nhindi = []
exists = False

for hit in res['hits']['hits']:
    print(hit['_id'], '->', hit['_source'])
    english.append(hit['_source']['English'])
    hindi.append(hit['_source']['Translation'])
    print()

'''Cleaning the corpus'''
translator = str.maketrans('','', string.punctuation)

for i in range(len(english)):
    temp.append(english[i].translate(translator))

for i in range(len(temp)):
    nenglish.append(temp[i].replace('\n',''))

for i in range(len(hindi)):
    nhindi.append(hindi[i].translate(translator))

print(nenglish,'\n')
print(nhindi,'\n')


'''If line exists in given corpus'''
for line in nenglish:
    if line == sentence:
        exists = True
        for hit in res['hits']['hits']:
            if hit['_source']['English'] == sentence+'\n':
                print(hit['_source']['Translation'])
                break


'''Case 1: Lines of the same length (Differs by one word)'''
if len(sentence) == len(nenglish[0]) and exists == False:
    sn = list(set(sentence.split()) - set(nenglish[0].split()))
    ns = list(set(nenglish[0].split()) - set(sentence.split()))
    snns = sn+ns

    t = []

    for word in snns:
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
            name1, count1 = counts.most_common(1)[0]
            name2, count2 = counts.most_common(2)[1]
            if count1 == count2:
                t.append(name1+' '+name2)
            else:
                t.append(name1)
        print(t)

    print (t[0].join(nhindi[0].split(t[1])))

elif len(sentence) < len(nenglish[0]):
    remove = list(set(nenglish[0].split()) - set(sentence.split()))
    print(remove)

    t = []
    res = es.search(index='conversion', body={'query': {'match' : { 'English' : 'no' }}})

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
        name1, count1 = counts.most_common(1)[0]
        name2, count2 = counts.most_common(2)[1]
        if count1 == count2:
            t.append(name1+' '+name2)
        else:
            t.append(name1)
    print(t)

    print (nhindi[0].replace(t[0],''))

