from elasticsearch import Elasticsearch

es = Elasticsearch(HOST = "http://localhost", PORT = 9200)
es = Elasticsearch()

doc1 = {"sentence": "Today is a sunny day"}
doc2 = {"sentence": "Today is a bright sunny day"}

es.index(index = "english", doc_type = "sentences", id = "1", body = doc1)
es.index(index = "english", doc_type = "sentences", id = "2", body = doc2)

query1 = {"from": 0,
          "size" : 0,
          "query" : {
            "match" : {
                "sentence" : "sunny"}}}

res = es.search(index = "english", doc_type = "sentences", body = query1)
print(res)
print()

query2 = {"from": 0,
          "size" : 2,
          "query" : {
            "match" : {
                "sentence" : "sunny"}}}

res = es.search(index = "english", doc_type = "sentences", body = query2)
print(res)
print()

query3 = {"from": 0,
          "size" : 0,
          "query" : {
            "match_phrase" : {
                "sentence" : "bright sunny"}}}

res = es.search(index = "english", doc_type = "sentences", body = query3)
print(res)
print()

query4 = {"from": 0,
          "size" : 0,
          "query" : {
            "term" : {
                "sentence" : "bright sunny"}}}

res = es.search(index = "english", doc_type = "sentences", body = query4)
print(res)
print()

#term - matches a single term, not analyzed
#match_phrase - all terms should appear, order should be same
#query_string - returns every document 
