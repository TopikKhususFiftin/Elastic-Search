import pytest
from unittest.mock import MagicMock, patch
from main import create_app
from app.services import BukuService

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# --- TEST UNTUK SERVICE LAYER ---
def test_service_tambah_buku_valid():
    mock_repo = MagicMock()
    mock_repo.save.return_value = {"_id": "123"}
    service = BukuService(mock_repo)
    result = service.tambah_buku({"judul": "Sistem Informasi Library", "penulis": "Fiftin Maizarni"})
    assert result["_id"] == "123"

def test_service_tambah_buku_invalid():
    service = BukuService(MagicMock())
    with pytest.raises(ValueError):
        service.tambah_buku({"judul": ""})

# --- TEST UNTUK ROUTE/CONTROLLER LAYER ---
def test_route_add_buku_success(client):
    # Kita mock service-nya agar tidak benar-benar memanggil Elasticsearch
    with patch('app.routes.service.tambah_buku') as mock_tambah:
        mock_tambah.return_value = {"_id": "999"}
        payload = {"judul": "Buku Test", "penulis": "Fiftin Maizarni"}
        response = client.post('/buku', json=payload)
        
        assert response.status_code == 201
        assert response.json['id'] == "999"

def test_route_add_buku_error(client):
    with patch('app.routes.service.tambah_buku') as mock_tambah:
        mock_tambah.side_effect = ValueError("Judul tidak boleh kosong")
        response = client.post('/buku', json={"judul": ""})
        
        assert response.status_code == 400
        assert "error" in response.json