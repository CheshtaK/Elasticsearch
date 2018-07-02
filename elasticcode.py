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

sentence = 'please enter valid loan income'

'''please enter loan amount'''
'''please enter valid loan income'''

##
##worde = sentence.split()
##
##t = []
##
##'''Template'''
##
##template = {}
##inTemplate = False
##phrases = []
##template.update({'please enter': ['कृपया', 'दर्ज करें']})
##
##print(template['please enter'][0])
##
##words = sentence.split(' ')
##maxlen = 2
##index = 0
##
##while index < len(words):
##    for i in range(maxlen, 0, -1):
##        phrase = ' '.join(words[index:index+i])
##        if phrase in template:
##            inTemplate = True
##            sentence = sentence.replace(phrase,'')
##            phrases.append(phrase)
##            index += i
##            break
##    else:
##        index += 1
##
##print(sentence)
##
##worde = sentence.split()


##def preprocess(strings):
##    return [" ".join(string.split()).replace(",", "").replace(".", "").replace("?", "") for string in strings]
##
##def find_n_grams(string, n):
##    words = string.split(" ")
##    n_grams = []
##
##    for i in range(len(words) - n + 1):
##        n_grams.append(" ".join([words[i + idx] for idx in range(n)]))
##
##    return n_grams
##
##def find_modal_substring(strings, num_words):
##    n_grams_per_string = [find_n_grams(string, num_words) for string in strings]
##    max_num_occurences = 0
##    modal_substring = None
##
##    for i in range(len(strings)):
##        n_grams = n_grams_per_string[i]
##
##        for n_gram in n_grams:
##            num_occurences = 1
##
##            for j in range(i + 1, len(strings)):
##                if n_gram in n_grams_per_string[j]:
##                    num_occurences += 1
##
##            if num_occurences > max_num_occurences:
##                max_num_occurences = num_occurences
##                modal_substring = n_gram
##            elif num_occurences == max_num_occurences and len(modal_substring) < len(n_gram):
##                max_num_occurences = num_occurences
##                modal_substring = n_gram
##
##    return modal_substring
##
##print(find_modal_substring(preprocess(reqTranslation), 4))
##

t = []

res = es.search(index='conversion', body={'query': {'match' : { 'English' : sentence }}})

reqTranslation = []
hindi = []
nt = []

for hit in res['hits']['hits']:
    print(hit['_id'], '->', hit['_source'])
    reqTranslation.append(hit['_source']['English'])
    hindi.append(hit['_source']['Translation'])
    print()

'''Cleaning the corpus - Removing punctuations'''
translator = str.maketrans('','', string.punctuation)

for i in range(len(reqTranslation)):
    nt.append(reqTranslation[i].translate(translator))

print(nt,'\n\n')

sn = list(set(sentence.split()) - set(nt[0].split()))
print(sn)

ns = list(set(nt[0].split()) - set(sentence.split()))
print(ns)

snns = sn + ns
print(snns)

##def print_first_difference(string1, string2):
##    aggr_strings = zip(string1, string2)
##    for index, tup in enumerate(aggr_strings):
##        if tup[0] != tup[1]:
##            print("Strings differ at position " + str(index))
##            break
##    else:
##        if len(aggr_strings) != len(max(string1, string2)):
##            print("Strings differ at position " + str(len(min(string1, string2))))
##        else:
##            print("Strings are identical")
##
##print(print_first_difference(sentence, nt[0]))


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

print (t[0].join(hindi[0].split(t[1])))

##res = es.search(index='conversion', body={'query': {'terms' : { 'Translation' : common }}})
##occurence = []
##    
##for hit in res['hits']['hits']:
##    print(hit['_id'], '->', hit['_source'])
##    occurence.append(hit['_source']['Translation'])
##
##for line in occurence:
##    if all(word in line for word in common):
##        print(line)


    




