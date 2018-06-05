from elasticsearch import Elasticsearch

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

res = es.search(index = "test", body = {"query": {"match_all" : {}}})

print(res['hits']['total'])

print(res['hits']['hits'])
print()
for hit in res['hits']['hits']:
    print(hit['_id']," -> ", hit['_source'])



