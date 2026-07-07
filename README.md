# Elastic-Search

Proyek ini mendemonstrasikan implementasi mesin pencari menggunakan **Elasticsearch** dan **Flask Framework**. Arsitektur ini menggunakan pola **Layered Architecture** untuk memastikan setiap komponen (Data Access, Business Logic, dan API Control) terpisah dengan jelas, sehingga memudahkan proses *maintenance* dan pencapaian target *Unit Testing Coverage* di atas 80%.

## Daftar Isi

1. [Prasyarat](#1-prasyarat)
2. [Instalasi](#2-instalasi)
   - [Instalasi Elasticsearch](#instalasi-elasticsearch-native)
   - [Instalasi Library Python](#instalasi-library-python)
3. [Struktur Proyek](#3-struktur-proyek)
4. [Implementasi Kode](#4-implementasi-kode-per-layer)
   - [Repository Layer](#a-repository-layer-apprepositoriespy)
   - [Service Layer](#b-service-layer-appservicespy)
   - [Controller Layer](#c-controller-layer-approutespy)
   - [Main Entry Point](#d-main-entry-point-mainpy)
5. [Pengujian](#5-pengujian-testing)
   - [Unit Test dan Coverage](#menjalankan-unit-test-dan-coverage)
   - [Pengujian API Manual](#pengujian-api-manual)

---

## 1. Prasyarat

- **Python 3.10+** (Gunakan perintah `py` atau `python`)
- **Java (JDK) 17+** (Dibutuhkan untuk menjalankan Elasticsearch)
- **Elasticsearch 8.x** (Versi Native/ZIP)

---

## 2. Instalasi

### Instalasi Elasticsearch (Native)

1. Unduh paket Elasticsearch dari situs resmi [Elastic](https://www.elastic.co/downloads/elasticsearch)
2. Ekstrak file ZIP/Tarball ke direktori lokal Anda
3. **Konfigurasi Keamanan (Development Mode):** Buka file `config/elasticsearch.yml` dan tambahkan konfigurasi berikut di bagian paling bawah:

```yaml
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl.enabled: false
discovery.type: single-node
```

4. **Jalankan Elasticsearch:**
   - Windows: Buka folder `bin`, lalu jalankan `elasticsearch.bat`
   - Linux/macOS: Jalankan `./elasticsearch` pada folder `bin`

5. Verifikasi melalui browser di alamat http://localhost:9200

### Instalasi Library Python

Instal seluruh dependensi yang diperlukan:

```bash
py -m pip install flask elasticsearch pytest pytest-cov
```

---

## 3. Struktur Proyek

Repositori ini disusun dengan struktur folder sebagai berikut:

```
project-es/
├── app/
│   ├── __init__.py      # Inisialisasi package
│   ├── repositories.py  # Layer 1: Data Access (Elasticsearch)
│   ├── services.py      # Layer 2: Business Logic & Validation
│   └── routes.py        # Layer 3: Controller (API Endpoints)
├── tests/
│   └── test_layers.py   # Unit Testing & Mocking
├── main.py              # Entry Point Aplikasi
└── README.md            # Dokumentasi Proyek
```

---

## 4. Implementasi Kode Per Layer

### A. Repository Layer (`app/repositories.py`)

Bertanggung jawab untuk komunikasi langsung dengan server Elasticsearch.

```python
from elasticsearch import Elasticsearch

class BukuRepository:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        self.index = "buku_sitakan"

    def save(self, data):
        return self.es.index(index=self.index, document=data)
```

### B. Service Layer (`app/services.py`)

Berisi logika bisnis dan validasi data sebelum diteruskan ke repository.

```python
class BukuService:
    def __init__(self, repository):
        self.repo = repository

    def tambah_buku(self, data):
        if "judul" not in data or not data["judul"]:
            raise ValueError("Judul tidak boleh kosong")
        return self.repo.save(data)
```

### C. Controller Layer (`app/routes.py`)

Mengelola endpoint API dan request/response HTTP.

```python
from flask import Blueprint, request, jsonify
from .repositories import BukuRepository
from .services import BukuService

buku_bp = Blueprint('buku', __name__)
service = BukuService(BukuRepository())

@buku_bp.route('/buku', methods=['POST'])
def add_buku():
    try:
        data = request.json
        res = service.tambah_buku(data)
        return jsonify({"status": "success", "id": res['_id']}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
```

### D. Main Entry Point (`main.py`)

```python
from flask import Flask
from app.routes import buku_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(buku_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 5. Pengujian (Testing)

### Menjalankan Unit Test dan Coverage

Untuk mencapai target coverage minimal 80%, pengujian menggunakan teknik **Mocking** agar logika bisnis dapat diuji secara terisolasi tanpa bergantung pada server Elasticsearch yang aktif.

Jalankan perintah berikut di terminal:

```bash
py -m pytest --cov=app tests/
```

### Pengujian API (Manual)

Gunakan **Thunder Client** atau **Postman** untuk melakukan verifikasi integrasi:

| Field | Value |
|-------|-------|
| **Endpoint** | POST http://localhost:5000/buku |
| **Method** | POST |
| **Content-Type** | application/json |

**Payload (JSON):**

```json
{
  "judul": "Analisis Keamanan Sistem SITAKAN",
  "penulis": "Fauzi Fernanda",
  "nim": "2311081015"
}
```

---

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran.
