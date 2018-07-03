# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
import re

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

with open('paytm.txt', encoding = 'utf-8') as f:
    lineNum = 0
    txtNum = 0
    for line in f:
        lineNum += 1
        print(lineNum)
        if len(line) > 0:
##            if '|' in line:
##                print('yes')
##                line.replace('|','\t')
##                print(line)
            if '|' in line:
                txtNum += 1
                val = re.split('[\t|]+', line)
                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[2]}, request_timeout=30)
                txtNum += 1
                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[1],'English': val[3]}, request_timeout=30)
            else:
                txtNum += 1
                val = line.split('\t')
                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[1]}, request_timeout=30)
            
##            if '|' in val[0]:
##                t = val[0].split('|')
##                e = val[1].split('|')
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': t,'English': e}, request_timeout=30)
##            else:
##                es.index(index='conversion', doc_type='file', id=txtNum, body = {'Translation': val[0],'English': val[1]}, request_timeout=30)


res = es.get(index = 'conversion', doc_type='file', id='1')
print(res['_source'])

res = es.get(index = 'conversion', doc_type='file', id='2')
print(res['_source'])

res = es.get(index = 'conversion', doc_type='file', id='3')
print(res['_source'])

res = es.get(index = 'conversion', doc_type='file', id='4')
print(res['_source'])

res = es.get(index = 'conversion', doc_type='file', id='5')
print(res['_source'])

res = es.get(index = 'conversion', doc_type='file', id='6')
print(res['_source'])
