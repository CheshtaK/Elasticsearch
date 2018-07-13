from elasticsearch import Elasticsearch
import string
import collections
from string import punctuation

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

## 'upto rs _ cashback when you pay using Paytm at _' - Case

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


'''Main Translation (Translates a sentence)'''
def translateS(sentence):
    sentence = sentence.lower()
    print('Sentence -> ', sentence.rstrip())

    query = {'query' : {'query_string' : {'query': sentence, 'fuzziness' : 2}}}
    res = es.search(index = 'conversion', body = query)

    english = []
    hindi = []
    temp = []
    exists = False

    for hit in res['hits']['hits']:
        print(hit['_source'])
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
                    print('Direct Translation -> ', hit['_source']['Translation'])
                    return (hit['_source']['Translation'])

    if exists == False:
        removetemp = list(set(english[0].split()) - set(sentence.split()))
        remove = [value for value in removetemp if not value.isdigit()]
        findtemp = list(set(sentence.split()) - set(english[0].split()))
        find = [value for value in findtemp if not value.isdigit()]

        if remove:
            removeT = translate(remove)

        if find:
            findT = translate(find)

        #Replacing the number
        for number in sentence.split():
            if number.isdigit():
                a = number

        for n in hindi[0].split():
            if n.isdigit():
                hindi[0] = hindi[0].replace(n, a)

        if removeT and findT:
            hindi[0] = hindi[0].replace(removeT[0], findT[0])
            print('Translation -> ', hindi[0], '\n')
            return hindi[0]



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
