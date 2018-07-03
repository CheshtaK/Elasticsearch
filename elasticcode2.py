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
#(UPTO CASHBACK cases) 

sentence = 'Upto Rs. 50 Cashback'

translation = 'तक का कैशबैक'

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

print('HINDI')
print(hindi,'\n')


'''Cleaning the English corpus'''
for line in english:
    nenglish.append(line.replace('\n',''))

print('ENGLISH')
print(nenglish,'\n')


#UPTO CASHBACK
if sentence.find('Upto') != -1 and sentence.find('Cashback') != -1:
    start, *middle, end = sentence.split()
    if '%' not in sentence:
        number = [s for s in middle if s.isdigit()]
        toTranslate = [s for s in middle if not s.isdigit()]
        translated = translate(toTranslate)
        print('TRANSLATED', translated)
        print(translated[0]+' '+number[0]+' '+translation)
    else:
        print(str(''.join(middle))+' '+ translation)

else:
    print('WHY AM I IN ELSE?')
    #If line exists in given corpus
    for line in nenglish:
        if line.lower() == sentence.lower():
            exists = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'] == sentence+'\n':
                    print(hit['_source']['Translation'])
                    break

    #When sentence length equal to search result
    if len(sentence) == len(nenglish[0]) and exists == False:
        words = sentence.split()
        t = translate(words)
        print(str(' '.join(t)))

    #Length of search result greater than sentence
    elif len(sentence) < len(nenglish[0]):
        remove = list(set(nenglish[0].split()) - set(sentence.split()))
        t = translate(remove)

        for i in range(len(t)):
            hindi[0] = hindi[0].replace(t[i],'')

        print(hindi[0])


    ###When the sentence has only one word(for accurate results)
    ##if len(sentence.split()) == 1 and exists == False:
    ##    search = []
    ##    search.append(sentence)
    ##    print(str(''.join(translate(search))))



    

