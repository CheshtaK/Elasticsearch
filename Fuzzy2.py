from elasticsearch import Elasticsearch
import string
import collections
from string import punctuation

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

## '__ |/: __' - Case

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

    print('Sentence -> ', sentence.rstrip())

    translated = []
    sentence = sentence.lower()
    
    if '|' in sentence.split():
        sentence = sentence.split('|')
        sep = '|'
    elif ':' in sentence.split():
        sentence = sentence.split(':')
        sep = ':'

    #For first part of sentence
    query = {'query' : {'query_string' : {'query': sentence[0].rstrip(), 'fuzziness' : 1}}}
    res = es.search(index = 'conversion', body = query)

    english = []
    hindi = []
    temp = []
    exists = False

    for hit in res['hits']['hits']:
        temp.append(hit['_source']['English'].lower())
        hindi.append(hit['_source']['Translation'])

    for line in temp:
        english.append(line.replace('\n',''))
    
    #If line exists in given corpus
    for line in english:
        if sentence[0].strip() == line.strip():
            exists = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'].lower().strip() == (sentence[0]+'\n').strip():
                    translated.append(hit['_source']['Translation'])
                    break
                break
            break


    if exists == False:
        removetemp = list(set(english[0].split()) - set(sentence[0].split()))
        remove = [value for value in removetemp if not value.isdigit()]
        findtemp = list(set(sentence[0].split()) - set(english[0].split()))
        find = [value for value in findtemp if not value.isdigit()]

        removeT = []
        findT = []

        if remove:
            removeT = translate(remove)

        if find:
            findT = translate(find)

        if removeT and findT:
            hindi[0] = hindi[0].replace(removeT[0], findT[0])
            translated.append(hindi[0])


    #For second part of sentence
    query = {'query' : {'query_string' : {'query': sentence[1].rstrip(), 'fuzziness' : 1}}}
    res = es.search(index = 'conversion', body = query)

    english = []
    hindi = []
    temp = []
    exists = False

    for hit in res['hits']['hits']:
        temp.append(hit['_source']['English'].lower())
        hindi.append(hit['_source']['Translation'])

    for line in temp:
        english.append(line.replace('\n',''))
    
    #If line exists in given corpus
    for line in english:
        if sentence[1].strip() == line.strip():
            exists = True
            for hit in res['hits']['hits']:
                if hit['_source']['English'].lower().strip() == (sentence[1]+'\n').strip():
                    translated.append(hit['_source']['Translation'])
                    break
            break

    if exists == False:
        for number in sentence[1].split():
            if number.isdigit() or any(char.isdigit() for char in number):
                a = number

        for n in hindi[2].split():
            if n.isdigit() or any(char.isdigit() for char in n):
                hindi[2] = hindi[2].replace(n, a)

        translated.append(hindi[2])

    print('TRANSLATED -> ', str(sep.join(translated)), '\n') 
        

def main():
    translated = []

    with open('cb.txt', 'r', encoding = 'utf-8-sig') as f:
        for line in f:
            translated.append(translateS(line))


if __name__ == '__main__':
    main()

