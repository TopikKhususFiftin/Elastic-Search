class BukuService:
    def __init__(self, repository):
        self.repo = repository

    def tambah_buku(self, data):
        if "judul" not in data or not data["judul"]:
            raise ValueError("Judul tidak boleh kosong")
        return self.repo.save(data)

    def cari_buku(self, keyword):
        if not keyword:
            return []
        res = self.repo.find_by_judul(keyword)
        return [hit['_source'] for hit in res['hits']['hits']]