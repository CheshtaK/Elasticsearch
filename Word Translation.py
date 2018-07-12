from elasticsearch import Elasticsearch
import string
import collections
from string import punctuation

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

def translate(word):
    word = word.lower()

    translator = str.maketrans('','', string.punctuation)
    word = word.translate(translator)
    
    res = es.search(index='conversion', body={'query': {'match' : { 'English' : word }}})

    reqTranslation = []
    e = []
    nt = []
    exists = False

    for hit in res['hits']['hits']:
        e.append(hit['_source']['English'].lower())
        reqTranslation.append(hit['_source']['Translation'])

    if word.replace('.','',1).isdigit() or any(char.isdigit() for char in word):
        exists = True
        return (word.rstrip() + '\t' + word.rstrip())
    else:
        for line in e:
            if word == line:
                exists = True
                for hit in res['hits']['hits']:
                    if hit['_source']['English'].lower().strip() == word:
                        return (word.rstrip() + '\t' + hit['_source']['Translation'])

    if exists == False:
        '''Cleaning the corpus - Removing punctuations'''

        for i in range(len(reqTranslation)):
            nt.append(reqTranslation[i].translate(translator))

        words = [word for line in nt for word in line.split()] 

        counts = collections.Counter(words)

        if counts:
            name, count = counts.most_common(1)[0]
            if name != 'का' and name != 'के':
                return (word.rstrip() + '\t' + name)
            else:
                name2, count2 = counts.most_common(2)[1]
                return (word.rstrip() + '\t' + name2)

    return (word.rstrip() + '\t' + word.rstrip())


def main():
    '''Finding unique words from file'''
    with open('test.txt', 'r', encoding = 'utf-8-sig') as f:
        contents = f.read()
        word_list = contents.split()
    
    unique_words = set(word_list)
    
    with open('words.txt', 'w', encoding = 'utf-8-sig') as out:
        for word in unique_words:
            out.write(str(word) + '\n')


    '''Translating each word'''

    trans = []
    with open('words.txt', 'r', encoding = 'utf-8-sig') as f:
        for line in f:
            trans.append(translate(line))

    with open('wordTranslate.txt', 'w', encoding = 'utf-8-sig') as f:
        for i in trans:
            f.write(str(i) +'\n')

if __name__ == '__main__':
    main()
