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