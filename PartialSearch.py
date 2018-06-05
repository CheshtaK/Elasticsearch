    from elasticsearch import Elasticsearch

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

es.index(index = "hellos", doc_type = "string", id = "1", body = {"name": "hello"})

termQuery = {"query" : {
                    "term" : {"name" : "*ell*"}}}

res = es.search(index = "hellos", doc_type = "string", body = termQuery)
print(res)
print()

wildcardQuery1 = {"query" : {
                    "wildcard" : {"name" : "*ell*"}}}

res = es.search(index = "hellos", doc_type = "string", body = wildcardQuery1)
print(res)
print()

wildcardQuery2 = {"query" : {
                    "wildcard" : {"name" : " *zz* *ell*"}}}

res = es.search(index = "hellos", doc_type = "string", body = wildcardQuery2)
print(res)
print()

querystringQuery = {"query" : {
                    "query_string" : {
                        "default_field": "name",
                        "query" : "*zz* *ell*"}}}

res = es.search(index = "hellos", doc_type = "string", body = querystringQuery)
print(res)
print()

#term - no partial search
#wildcard - partial search with one token
#query_string - multiple tokens
