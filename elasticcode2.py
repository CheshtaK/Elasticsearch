# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
import re
import string
import collections

import requests
import json
import pprint

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()



'''Indexing the corpus'''
##with open('paytm2.txt', encoding = 'utf-8') as f:
##    lineNum = 0
##    txtNum = 0
##    uNum = 0
##    for line in f:
##        lineNum += 1
##        print(lineNum)
##        if len(line) > 0:
##            if '|' in line:
##                txtNum += 1
##                val = re.split('[\t|]+', line)
##                
##                if val[2].find('Upto') != -1 and val[2].find('Cashback') != -1:
##                    print('Upto')
##                    uNum += 1
##                    es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[0],'English': val[2]}, request_timeout=30)
##                    
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[2]}, request_timeout=30)
##                
##                txtNum += 1
##                if val[3].find('Upto') != -1 and val[3].find('Cashback') != -1:
##                    print('Upto')
##                    uNum += 1
##                    es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[1],'English': val[3]}, request_timeout=30)
##                    
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[1],'English': val[3]}, request_timeout=30)
##                
##            else:
##                txtNum += 1
##                val = line.split('\t')
##                if val[1].find('Upto') != -1 and val[1].find('Cashback') != -1:
##                    print('Upto')
##                    uNum += 1
##                    es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[0],'English': val[1]}, request_timeout=30)
##
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[1]}, request_timeout=30)



'''Check if indexed'''
##res = es.get(index = "conversion", doc_type = "file", id = "1")
##print(res['_source'])



'''Function to translate a single word at a time'''
def translate(lst):
    t = []

    for word in lst:
        res = es.search(index='conversion', body={'query': {'match' : { 'English' : word }}})

        reqTranslation = []
        nt = []
        
        for hit in res['hits']['hits']:
            print(hit['_id'], '->', hit['_source'])
            reqTranslation.append(hit['_source']['Translation'])
            print()

        '''Cleaning the corpus - Removing punctuations'''
        translator = str.maketrans('','', string.punctuation)

        for i in range(len(reqTranslation)):
            nt.append(reqTranslation[i].translate(translator))

        words = [word for line in nt for word in line.split()] 

        counts = collections.Counter(words)

        if counts:
            name, count = counts.most_common(1)[0]
            t.append(name)
    return t    


'''Main Translation'''

sentence = 'supply chain management'
sentence = sentence.lower()


res = es.search(index='conversion', body={'query': {'match' : { 'English' : sentence }}})

english = []
temp = []
hindi = []
exists = False

for hit in res['hits']['hits']:
    print(hit['_id'], '->', hit['_source'])
    temp.append(hit['_source']['English'].lower())
    hindi.append(hit['_source']['Translation'])
    print()

print('HINDI')
print(hindi,'\n')


'''Cleaning the English corpus'''
for line in temp:
    english.append(line.replace('\n',''))

print('ENGLISH')
print(english,'\n')


#If line exists in given corpus
for line in english:
    if line.lower() == sentence:
        exists = True
        for hit in res['hits']['hits']:
            if hit['_source']['English'].lower() == sentence+'\n':
                print(hit['_source']['Translation'])
                break


print(exists)


#UPTO CASHBACK case
if sentence.find('Upto') != -1 and sentence.find('Cashback') != -1 and exists == False:
    resUC = es.search(index='upto', body={'query': {'match' : { 'English' : sentence }}})

    ucEnglish = []
    ucHindi = []

    for hit in resUC['hits']['hits']:
        print(hit['_id'], '->', hit['_source'])
        ucEnglish.append(hit['_source']['English'].lower())
        ucHindi.append(hit['_source']['Translation'])
        
    remove = list(set(ucEnglish[0].split()) - set(sentence.split()))
    print('REMOVE', remove, '\n')

    find = list(set(sentence.split()) - set(ucEnglish[0].split()))
    print('FIND', find, '\n')

    removeT = translate(remove)
    print('REMOVE TRANSLATED', removeT, '\n')

    findT = translate(find)
    print('FIND TRANSLATED', findT)

    ucHindi[0] = ucHindi[0].replace(removeT[0], str(''.join(findT)))
    print(ucHindi[0])


#When sentence length equal to search result
elif len(sentence) == len(english[0]) and exists == False:
    words = sentence.split()
    t = translate(words)
    print(str(' '.join(t)))


#Length of search result greater than sentence
elif len(sentence) < len(english[0]):
    remove = list(set(english[0].split()) - set(sentence.split()))
    t = translate(remove)

    for i in range(len(t)):
        hindi[0] = hindi[0].replace(t[i],'')

    print(hindi[0])






###When the sentence has only one word(for accurate results)
##if len(sentence.split()) == 1 and exists == False:
##    search = []
##    search.append(sentence)
##    print(str(''.join(translate(search))))



    

