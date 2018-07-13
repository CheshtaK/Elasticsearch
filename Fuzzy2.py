from elasticsearch import Elasticsearch
import string
import collections
from string import punctuation

import regex as re

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

## '__ | __' - Case

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
                    if name != 'का' and name != 'के' and name != 'पर':
                        t.append(name)
                    else:
                        name2, count2 = counts.most_common(2)[1]
                        t.append(name2)

    return t

def translateS(sentence):

    print('Sentence -> ', sentence.rstrip(), '\n')

    toremove = []
    sentence = sentence.lower()
    orig = sentence

    ## Removing numbers and percentages
    for word in sentence.split():
        if word.isdigit():
            a1 = word
            sentence = sentence.replace(a1, '')
        elif any(char == '%' for char in word):
            a2 = re.findall(r'\d+%', sentence)
            sentence = sentence.replace(a2[0], '')

    print('New Sentence -> ', sentence.rstrip(), '\n')
    
    # Searching
    query = {'query' : {'query_string' : {'query': sentence.rstrip(), 'fuzziness' : 1}}}
    res = es.search(index = 'conversion', body = query)

    english = []
    hindi = []
    temp = []
    exists = False
    num = False

    for hit in res['hits']['hits']:
        temp.append(hit['_source']['English'].lower())
        hindi.append(hit['_source']['Translation'])

    for line in temp:
        english.append(line.replace('\n',''))
    
    #If line exists in given corpus
    for line in english:
        if sentence.strip() == line.strip():
            exists = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'].lower().strip() == (sentence+'\n').strip():
                    t1 = hit['_source']['Translation']
                    toremove.append(hit['_source']['English'])
                    break
                break
            break

    #Replacing given number with our number
    for word in hindi[0].split():
        if word.isdigit():
            num = True
            hindi[0] = hindi[0].replace(word, a1)
        elif any(char == '%' for char in word):
            num = True
            a = re.findall(r'\d+%', hindi[0])
            hindi[0] = hindi[0].replace(a[0], a2[0])

    t1 = hindi[0]

    # Getting the string to be removed
    if num:
        for word in english[0].split():
            if word.isdigit():
                english[0] = english[0].replace(word, '')
            elif any(char == '%' for char in word):
                b2 = re.findall(r'\d+%', english[0])
                english[0] = english[0].replace(b2[0], '')
        toremove.append(english[0])

    #For non-number containing string
    t = []
    if exists == False and num == False:
        t.append(sentence.split('|', 1)[0])
        toremove.append(sentence.split('|', 1)[0])
        t = translate(t)
        if t:
            t1 = t[0]
    
    sentence = str(''.join(sentence.rsplit(toremove[0].strip())))

    if '|' in sentence.split():
        sentence = sentence.replace('|', '')
    elif ':' in sentence.split():
        sentence = sentence.replace(':', '')

    print('First Transation -> ', t1, '\n')
    print('To Remove -> ', toremove[0], '\n')
    print('Sentence Left -> ', sentence.rstrip(), '\n')

    '''SECOND PART'''

    # Searching
    query = {'query' : {'query_string' : {'query': sentence.rstrip(), 'fuzziness' : 1}}}
    res = es.search(index = 'conversion', body = query)

    english = []
    hindi = []
    temp = []
    num = False
    exists = False

    for hit in res['hits']['hits']:
        temp.append(hit['_source']['English'].lower())
        hindi.append(hit['_source']['Translation'])

    for line in temp:
        english.append(line.replace('\n',''))
    
    #If line exists in given corpus
    for line in english:
        if sentence.strip() == line.strip():
            exists = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'].lower().strip() == (sentence+'\n').strip():
                    t2 = hit['_source']['Translation']
                    break
                break
            break

    #Replacing given number with our number
    for word in hindi[0].split():
        if word.isdigit():
            num = True
            hindi[0] = hindi[0].replace(word, a1)
        elif any(char == '%' for char in word):
            num = True
            a = re.findall(r'\d+%', hindi[0])
            hindi[0] = hindi[0].replace(a[0], a2[0])

    if num:
        t2 = hindi[0]

    # Getting the string to be removed
    if num:
        for word in english[0].split():
            if word.isdigit():
                english[0] = english[0].replace(word, '')
            elif any(char == '%' for char in word):
                b2 = re.findall(r'\d+%', english[0])
                english[0] = english[0].replace(b2[0], '')


    #For non-number containing string
    t = []
    if exists == False and num == False:
        t.append(sentence.split('|', 1)[0])
        removetemp = list(set(english[0].split()) - set(t[0].split()))
        remove = [value for value in removetemp if not value.isdigit()]
        findtemp = list(set(t[0].split()) - set(english[0].split()))
        find = [value for value in findtemp if not value.isdigit()]

        if remove:
            removeT = translate(remove)

        if find:
            findT = translate(find)

        if removeT and findT:
            hindi[0] = hindi[0].replace(removeT[0], findT[0])
            t2 = hindi[0]


    print('Second Translation -> ', t2, '\n')

    #To get position of first and second segment
    if all(i in sentence.split() for i in orig.split('|', 1)[0].split()):
        print('FINAL -> ', t2, '|', t1, '\n\n\n')
        return (t2 + '|' + t1)
    else:
        print('FINAL -> ', t1, '|', t2, '\n\n\n')
        return (t1 + '|' + t2)

def main():
    translated = []

    with open('cb.txt', 'r', encoding = 'utf-8-sig') as f:
        for line in f:
            translated.append(translateS(line))

    with open('final.txt', 'w', encoding = 'utf-8-sig') as t:
        for line in translated:
            t.write('%s\n' %line)


if __name__ == '__main__':
    main()

