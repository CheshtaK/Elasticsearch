# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
import string
import collections
import requests
import re

from string import punctuation

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()


'''Function to translate a single word at a time'''
def translate(lst):
    t = []

    for word in lst:
        res = es.search(index='conversion', body={'query': {'match' : { 'English' : word }}})

        reqTranslation = []
        e = []
        nt = []
        exists = False

        for hit in res['hits']['hits']:
            e.append(hit['_source']['English'].lower())
            reqTranslation.append(hit['_source']['Translation'])

        if word.replace('.','',1).isdigit() or any(char.isdigit() for char in word):
            t.append(word)
        else:
            for line in e:
                if word == line:
                    exists = True
                    for hit in res['hits']['hits']:
                        if hit['_source']['English'].lower().strip() == word:
                            t.append(hit['_source']['Translation'])
                            break

            if exists == False:
                '''Cleaning the corpus - Removing punctuations'''
                translator = str.maketrans('','', string.punctuation)

                for i in range(len(reqTranslation)):
                    nt.append(reqTranslation[i].translate(translator))

                words = [word for line in nt for word in line.split()] 

                counts = collections.Counter(words)

                if counts:
                    name, count = counts.most_common(1)[0]
                    if name != 'का' and name != 'के':
                        t.append(name)
                    else:
                        name2, count2 = counts.most_common(2)[1]
                        t.append(name2)

    return t    



'''Main Translation (Translates a sentence)'''
def translateS(sentence):  
    sentence = sentence.lower()

    print(sentence)

    newS = []

    '''Removing all punctuations'''
    translator = str.maketrans('','', string.punctuation)
    out = sentence.translate(translator)
    words = out.split()

    res = es.search(index='conversion', body={'query': {'match' : { 'English' : sentence }}})

    english = []
    temp = []
    hindi = []
    existsM = False

    for hit in res['hits']['hits']:
        temp.append(hit['_source']['English'].lower())
        hindi.append(hit['_source']['Translation'])

    '''Cleaning the English corpus'''
    for line in temp:
        english.append(line.replace('\n',''))


    #If line exists in given corpus
    for line in english:
        if sentence.strip() == line.strip():
            existsM = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'].lower().strip() == (sentence+'\n').strip():
                    print('Direct Translation -> ', hit['_source']['Translation'])
                    return (hit['_source']['Translation'])
                    break


    #RECHARGE OF case
    if sentence.find('recharge of') != -1 and existsM == False:
        resRO = es.search(index='recharge', body={'query': {'match' : { 'English' : sentence }}})

        roEnglish = []
        roHindi = []
        removeT = []
        findT = []
        exists = False

        for hit in resRO['hits']['hits']:
            roEnglish.append(hit['_source']['English'].lower())
            roHindi.append(hit['_source']['Translation'])

        for line in roEnglish:
            if sentence.strip() == line.strip():
                exists = True
                for hit in resRO['hits']['hits']:
                    if hit['_source']['English'].lower().strip() == (sentence+'\n').strip():
                        print('Direct Translation(Recharge case) -> ', hit['_source']['Translation'])
                        return (hit['_source']['Translation'])
                        break
        
        if exists == False:
            remove = list(set(roEnglish[0].split()) - set(sentence.split()))
            find = list(set(sentence.split()) - set(roEnglish[0].split()))

            if remove:
                removeT = translate(remove)

            if find:
                findT = translate(find)

            if remove and find:
                if len(remove) > 1:
                    roHindi[0] = roHindi[0].replace(removeT[0], '').replace(removeT[1], str(' '.join(findT)))
                else:
                    roHindi[0] = roHindi[0].replace(removeT[0], str(' '.join(findT)))
                
            print('Translation(Recharge case) -> ', roHindi[0],'\n')
            return(roHindi[0])

    #UPTO CASHBACK case
    elif sentence.find('upto') != -1 and sentence.find('cashback') != -1 and existsM == False:
        resUC = es.search(index='upto', body={'query': {'match' : { 'English' : sentence }}})

        ucEnglish = []
        ucHindi = []

        for hit in resUC['hits']['hits']:
            ucEnglish.append(hit['_source']['English'].lower())
            ucHindi.append(hit['_source']['Translation'])
            
        remove = list(set(ucEnglish[0].split()) - set(sentence.split()))
        find = list(set(sentence.split()) - set(ucEnglish[0].split()))

        removeT = translate(remove)
        findT = translate(find)

        ucHindi[0] = ucHindi[0].replace(removeT[0], str(''.join(findT)))
        
        print('Translation(Upto Case) -> ', ucHindi[0],'\n')
        return(ucHindi[0])
    
    else:
        translated = translate(words)


        '''Adding back the punctuations'''
        e = []
        positions = []
        punctuations = []
        h = []
        final = []

        for word in enumerate(sentence.split()):
            e.append(word)
   
        for pos, word in e:
            for i in word:
                if i in punctuation:
                    positions.append(pos)
                    punctuations.append(i)

        for hword in enumerate(translated):
            h.append(hword)

        i = 0        
        for pos, word in h:
            if pos in positions:
                word = word+punctuations[i]
                i += 1
            final.append(word)

        print('Word Translated -> ', str(' '.join(final)))
        return(str(' '.join(final)))




'''Subtract lines method'''

##    if exists == False:
##        remove = list(set(english[0].split()) - set(sentence.split()))
##        find = list(set(sentence.split()) - set(english[0].split()))
##
##        if remove:
##            removeT = translate(remove)
##
##        if find:
##            findT = translate(find)
##
##        print('REMOVE', remove)
##        print('FIND', find)
##        print('REMOVET', removeT)
##        print('FINDT', findT)
##
##        for i in range(len(removeT)):
##            hindi[0] = hindi[0].replace(removeT[i],'')
##
##        hindi[0] = hindi[0] + ' ' + str(' '.join(findT))
##
##        print('TRANSLATION', hindi[0])
##        return hindi[0]

##    #When sentence length equal to search result
##    elif len(sentence) == len(english[0]) and exists == False:
##        words = sentence.split()
##        t = translate(words)
##        return(str(' '.join(t)))
##
##
##    #Length of search result greater than sentence
##    elif len(sentence) < len(english[0]):
##        remove = list(set(english[0].split()) - set(sentence.split()))
##        t = translate(remove)
##
##        for i in range(len(t)):
##            hindi[0] = hindi[0].replace(t[i],'')
##
##        return(hindi[0])
##

##    #When the sentence has only one word(for accurate results)
##    if len(sentence.split()) == 1 and exists == False:
##        search = []
##        search.append(sentence)
##        print(str(''.join(translate(search))))



'''Main function'''
def main():
    
##    '''Indexing the corpus'''
##    with open('finalpaytm.txt', encoding = 'utf-8') as f:
##        lineNum = 0
##        txtNum = 0
##        uNum = 0
##        rNum = 0
##        for line in f:
##            lineNum += 1
##            print(lineNum)
##            if len(line) > 0:
##                if '|' in line:
##                    txtNum += 1
##                    val = re.split('[\t|]+', line)
##
##                    if val[2].find('Recharge of') != -1:
##                        rNum += 1
##                        es.index(index='recharge', doc_type='file', id=rNum, body = {'Translation': val[0],'English': val[2].replace('\n','').lower()}, request_timeout=30)
##                    
##                    elif val[2].find('Upto') != -1 and val[2].find('Cashback') != -1:
##                        uNum += 1
##                        es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[0],'English': val[2].replace('\n','').lower()}, request_timeout=30)
##                        
##                    es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[2].replace('\n','').lower()}, request_timeout=30)
##                    
##                    txtNum += 1
##                    
##                    if val[3].find('Recharge of') != -1:
##                        rNum += 1
##                        es.index(index='recharge', doc_type='file', id=rNum, body = {'Translation': val[1],'English': val[3].replace('\n','').lower()}, request_timeout=30)
##                        
##                    elif val[3].find('Upto') != -1 and val[3].find('Cashback') != -1:
##                        uNum += 1
##                        es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[1],'English': val[3].replace('\n','').lower()}, request_timeout=30)
##                        
##                    es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[1],'English': val[3].replace('\n','').lower()}, request_timeout=30)
##                    
##                else:
##                    txtNum += 1
##                    val = line.split('\t')
##
##                    if val[1].find('Recharge of') != -1:
##                        rNum += 1
##                        es.index(index='recharge', doc_type='file', id=rNum, body = {'Translation': val[0],'English': val[1].replace('\n','').lower()}, request_timeout=30)
##                    
##                    elif val[1].find('Upto') != -1 and val[1].find('Cashback') != -1:
##                        uNum += 1
##                        es.index(index='upto', doc_type='file', id=uNum, body = {'Translation': val[0],'English': val[1].replace('\n','').lower()}, request_timeout=30)
##    
##                    es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[1].replace('\n','').lower()}, request_timeout=30)


##    '''Check if indexed'''
##    res = es.get(index = "conversion", doc_type = "file", id = "1")
##    print(res['_source'])
##
##    res = es.get(index = "upto", doc_type = "file", id = "1")
##    print(res['_source'])
##
##    res = es.get(index = "recharge", doc_type = "file", id = "1")
##    print(res['_source'])



    '''List to contain the final translated line'''
    translated = []

    '''Reading the English file'''
    with open('en.txt', 'r', encoding = 'utf-8-sig') as english:
        for line in english:
            translated.append(translateS(line))

    '''Writing the translated lines'''
    with open('hi.txt', 'w', encoding = 'utf-8-sig') as t:
        for line in translated:
            t.write('%s\n' %line)



if __name__ == '__main__':
    main()




    

