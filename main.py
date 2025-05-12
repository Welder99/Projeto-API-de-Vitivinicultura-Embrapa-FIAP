import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes import routes_blueprint
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    # Carrega .env
    load_dotenv()

    # Cria app e configura pasta de estáticos
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='/static'
    )

    # Habilita CORS apenas para /api/*
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'troque_essa_chave!')
    JWTManager(app)

    # Rotas da API
    app.register_blueprint(routes_blueprint, url_prefix='/api')

    # Swagger UI
    swagger_url  = os.getenv('SWAGGER_URL', '/swagger')
    api_docs     = os.getenv('SWAGGER_JSON_PATH', '/static/swagger.json')
    swagger_bp = get_swaggerui_blueprint(
        swagger_url,
        api_docs,
        config={'app_name': "API Vitivinicultura Embrapa"}
    )
    app.register_blueprint(swagger_bp, url_prefix=swagger_url)

    return app

if __name__ == "__main__":
    app = create_app()
    port  = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1')
    app.run(host='0.0.0.0', port=port, debug=debug)
