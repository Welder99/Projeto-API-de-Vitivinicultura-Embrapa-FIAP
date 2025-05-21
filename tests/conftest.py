import os
import sys

# Ajusta o sys.path para incluir a raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import pytest
from main import create_app

@pytest.fixture
def app():
    # configurações de teste
    os.environ['API_USER'] = 'testuser'
    os.environ['API_PASSWORD'] = 'testpass'
    os.environ['JWT_SECRET_KEY'] = 'test-secret'
    os.environ['SWAGGER_URL'] = '/swagger/'
    os.environ['SWAGGER_JSON_PATH'] = '/static/swagger.json'
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()
