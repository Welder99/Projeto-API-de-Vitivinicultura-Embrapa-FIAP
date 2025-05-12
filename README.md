Projeto API de Vitivinicultura Embrapa

Índice

Sobre o Projeto

Funcionalidades

Tecnologias Utilizadas

Requisitos

Instalação e Configuração

Variáveis de Ambiente

Como Executar

Sem Docker

Com Docker

Autenticação JWT

Documentação com Swagger

Estrutura do Projeto

Contribuição

Sobre o Projeto

Esta API realiza scraping dos dados de vitivinicultura no site da Embrapa — produção, processamento, comercialização, importação e exportação — e os expõe via endpoints RESTful. As rotas são protegidas por JWT e possuem documentação interativa em Swagger UI. Em caso de instabilidade da fonte, a API utiliza arquivos JSON de fallback armazenados em data/.

Funcionalidades

✔️ Scraping de dados do site da Embrapa

🔒 Endpoints protegidos por JWT

📄 Documentação interativa com Swagger UI

🌐 CORS configurado para permitir chamadas de qualquer origem

📁 Fallback local: grava/recupera JSON em data/{chave}.json quando o site estiver offline

Tecnologias Utilizadas

Python ≥ 3.7

Flask

Flask-JWT-Extended

Flask-CORS

BeautifulSoup4

Gunicorn

Docker (opcional)

python-dotenv

Requisitos

Python 3.7 ou superior

pip

Git

Docker (opcional)

Instalação e Configuração

# Clone o repositório
git clone https://github.com/seu-usuario/vitivinicultura-api.git
cd vitivinicultura-api

# Crie e ative um ambiente virtual
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows PowerShell
venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt

Variáveis de Ambiente

Copie .env.example para .env na raiz e configure:

# Segurança JWT
JWT_SECRET_KEY=uma_chave_secreta

# Credenciais para /api/login
API_USER=admin
API_PASSWORD=senha123

# Configurações do Flask
env FLASK_DEBUG=true
PORT=5000

# Swagger UI
SWAGGER_URL=/swagger
SWAGGER_JSON_PATH=/static/swagger.json

Como Executar

Sem Docker

# Certifique-se de que o venv está ativo
python main.py

API disponível em http://localhost:5000/api e Swagger UI em http://localhost:5000/swagger.

Com Docker

# Build da imagem
docker build -t vitivinicultura-api .

# Remova container antigo (se existir)
docker rm -f vitivinicultura-api

# Run em modo detached
docker run -d --name vitivinicultura-api \
  --env-file .env \
  -p 5000:5000 \
  vitivinicultura-api

API e Swagger UI nos mesmos URLs acima.

Autenticação JWT

Obter token:

curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha123"}'

Resposta:

{ "access_token": "<token>" }

Chamar endpoints protegidos:
Adicione no header:

Authorization: Bearer <access_token>

Documentação com Swagger

Acesse http://localhost:5000/swagger

Clique em Authorize

Cole Bearer <access_token> e confirme

Teste todos os endpoints pela UI

Estrutura do Projeto

vitivinicultura-api/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── scraping.py
├── data/               # JSONs de fallback (gitignored)
│   └── producao.json
├── static/
│   └── swagger.json
├── .dockerignore
├── Dockerfile
├── main.py
├── requirements.txt
├── README.md
└── .env.example

Contribuição

Contribuições são bem-vindas!

Abra uma issue para discutir bugs ou melhorias.

Faça um fork, implemente a alteração e envie um pull request.

Nota: o site da Embrapa pode apresentar instabilidades. A API grava automáticos arquivos de fallback em data/ para manter os dados disponíveis mesmo quando scraping falhar.