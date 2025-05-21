import os
import functools
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from app.scraping import (
    obter_dados_producao,
    obter_dados_processamento,
    obter_dados_comercializacao,
    obter_dados_exportacao,
    obter_dados_importacao,
)

routes_blueprint = Blueprint('routes', __name__)

# ——— Autenticação ———
@routes_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if (
        username == os.getenv('API_USER')
        and password == os.getenv('API_PASSWORD')
    ):
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200

    return jsonify({"msg": "Credenciais inválidas"}), 401


def trata_scraping(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)

        # Se já vier (data, status)
        if isinstance(result, tuple):
            data, status = result
            return jsonify(data), status

        # Se for dict com erro
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 500

        # Sucesso
        return jsonify(result), 200

    return wrapper


# ——— Endpoints protegidos ———
@routes_blueprint.route('/producao', methods=['GET'])
@jwt_required()
@trata_scraping
def producao():
    return obter_dados_producao()


@routes_blueprint.route('/processamento', methods=['GET'])
@jwt_required()
@trata_scraping
def processamento():
    return obter_dados_processamento()


@routes_blueprint.route('/comercializacao', methods=['GET'])
@jwt_required()
@trata_scraping
def comercializacao():
    return obter_dados_comercializacao()


@routes_blueprint.route('/exportacao', methods=['GET'])
@jwt_required()
@trata_scraping
def exportacao():
    return obter_dados_exportacao()


@routes_blueprint.route('/importacao', methods=['GET'])
@jwt_required()
@trata_scraping
def importacao():
    return obter_dados_importacao()