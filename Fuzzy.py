from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

with open("h.csv", encoding = "utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index = "hindif", doc_type = "document")

res = es.search(index = "hindif", body = {"query": {"match_all" : {}}})

#print(res)

print(res['hits']['total'])
print()

#for hit in res['hits']['hits']:
    #print(hit['_id']," -> ", hit['_source'])
    #print()

query1 = {"query" : {
            "query_string" : {
                "query" : "hidden charges",
                "fuzziness" : 1}}}

res = es.search(index = "hindif", body = query1)

#print(res)

print(res['hits']['total'])
#print()

#for hit in res['hits']['hits']: 
    #print(hit['_id']," -> ", hit['_source'])
    #print()
        
