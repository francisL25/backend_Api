from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.auth import auth_bp
from .routes.document import document_bp
from .routes.user import user_bp
from .routes.data import data_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=['http://localhost:4200'])
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(document_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(data_bp, url_prefix='/api')
    return app