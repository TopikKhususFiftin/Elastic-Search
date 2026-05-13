from elasticsearch import Elasticsearch

class BukuRepository:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        self.index = "buku_sitakan"

    def save(self, data):
        return self.es.index(index=self.index, document=data)

    def find_by_judul(self, query):
        body = {"query": {"match": {"judul": query}}}
        return self.es.search(index=self.index, body=body)