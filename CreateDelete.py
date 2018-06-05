import elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

create = es.create(index = "test", doc_type = "articles",
                   body = {"content":"One fox"}, id = "1")
print(create)

res = es.get(index = "test", doc_type = "articles", id = "1")
print(res['_source'])

exists = es.exists(index = "test", doc_type = "articles", id = "1")
print(exists)

delete = es.delete(index = "test", doc_type = "articles", id = "1")
print(delete)

exists = es.exists(index = "test", doc_type = "articles", id = "1")
print(exists)

