from flask import Flask
from app.routes import buku_bp

def create_app():
    app = Flask(__name__)

    # Registrasi Blueprint (Controller Layer)
    app.register_blueprint(buku_bp)

    @app.route('/')
    def index():
        return {
            "message": "Welcome to SITAKAN Elasticsearch API",
            "status": "Running",
            "version": "1.0.0"
        }

    return app

if __name__ == '__main__':
    app = create_app()
    # Host 0.0.0.0 agar bisa diakses jika kamu testing via device lain (mobile/flutter)
    app.run(debug=True, host='0.0.0.0', port=5000)