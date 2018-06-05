from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

with open("hindifuzzy.csv", encoding = "utf8") as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index = "hindi", doc_type = "document")


res = es.search(index = "hindi", body = {"query": {"match_all" : {}}})
print(res['hits']['total'])
print()

for hit in res['hits']['hits']:
    print(hit['_id']," -> ", hit['_source'])
    print()

query1 = {"query" : {
            "query_string" : {
                "query" : "आपरेटर",
                "fuzziness" : 1}}}

res = es.search(index = "hindi", body = query1)

print(res['hits']['total'])
print()

for hit in res['hits']['hits']: 
    print(hit['_id']," -> ", hit['_source'])
    print()
        
    
    
