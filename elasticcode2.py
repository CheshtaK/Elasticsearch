# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
import re
import string
import collections

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

##with open('paytm2.txt', encoding = 'utf-8') as f:
##    lineNum = 0
##    txtNum = 0
##    for line in f:
##        lineNum += 1
##        print(lineNum)
##        if len(line) > 0:
##            if '|' in line:
##                txtNum += 1
##                val = re.split('[\t|]+', line)
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[2]}, request_timeout=30)
##                txtNum += 1
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[1],'English': val[3]}, request_timeout=30)
##            else:
##                txtNum += 1
##                val = line.split('\t')
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[1]}, request_timeout=30)


##res = es.get(index = "conversion", doc_type = "file", id = "500")
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
                
    return t    


sentence = ''

res = es.search(index='conversion', body={'query': {'match' : { 'English' : sentence }}})

english = []
nenglish = []
hindi = []
exists = False

for hit in res['hits']['hits']:
    print(hit['_id'], '->', hit['_source'])
    english.append(hit['_source']['English'])
    hindi.append(hit['_source']['Translation'])
    print()

print(english,'\n')
print(hindi,'\n')


'''Cleaning the English corpus'''
for line in english:
    nenglish.append(line.replace('\n',''))

print(nenglish,'\n')


#If line exists in given corpus
for line in nenglish:
    if line == sentence:
        exists = True
        for hit in res['hits']['hits']:
            if hit['_source']['English'] == sentence:
                print(hit['_source']['Translation'])
                break


#If line does not exist
if exists == False:
    words = sentence.split()
    t = translate(words)
    print(str(' '.join(t)))
