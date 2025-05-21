Projeto API de Vitivinicultura Embrapa

1. Índice

2. Sobre o Projeto

3. Funcionalidades

4. Tecnologias Utilizadas

5. Requisitos

6. Instalação e Configuração

7. Variáveis de Ambiente

8. Como Executar

9. Sem Docker

10. Com Docker

11. Autenticação JWT

12. Documentação com Swagger

Estrutura do Projeto

Testes

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
git clone https://github.com/Welder99/Projeto-API-de-Vitivinicultura-Embrapa-FIAP.git
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
FLASK_DEBUG=true
PORT=5000

# Swagger UI
env SWAGGER_URL=/swagger/
env SWAGGER_JSON_PATH=/static/swagger.json

Como Executar

Sem Docker

# Certifique-se de que o venv está ativo
python main.py

A API ficará disponível em http://localhost:5000/api e o Swagger em http://localhost:5000/swagger/.

Com Docker

# Build da imagem
docker build -t vitivinicultura-api .

# Remova container antigo (se existir)
docker rm -f vitivinicultura-api

# Execute o container
docker run -d --name vitivinicultura-api \
  --env-file .env \
  -p 5000:5000 \
  vitivinicultura-api

A API e o Swagger estarão nos mesmos URLs acima.

Autenticação JWT

Obter token:

curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha123"}'

Resposta:

{ "access_token": "<token>" }

Usar o token:
Adicione no header de chamadas protegidas:

Authorization: Bearer <access_token>

Documentação com Swagger

Acesse: http://localhost:5000/swagger/

Clique em Authorize e cole Bearer <access_token>

Teste todos os endpoints diretamente na UI

Estrutura do Projeto

vitivinicultura-api/
├── app/
│   ├── routes.py
│   └── scraping.py
├── data/               # JSONs de fallback
│   ├── producao.json
│   ├── processamento.json
│   ├── comercializacao.json
│   ├── importacao.json
│   └── exportacao.json
├── static/
│   └── swagger.json
├── .dockerignore
├── .env.example
├── Dockerfile
├── main.py
├── requirements.txt
├── tests/              # Suíte de testes pytest
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_routes.py
│   └── test_scraping.py
└── README.md

Testes

A suíte de testes usa pytest e cobre:

Health-check e redirecionamento (main.py)

Login e autorização de rotas (routes.py)

Lógica de scraping ao vivo e fallback (scraping.py)

Executar os testes

pytest --cov=app tests/



Contribuição

Contribuições são bem-vindas!

Abra uma issue para discutir bugs ou melhorias.

Faça um fork, implemente as alterações e envie um pull request.

Nota: o site da Embrapa pode apresentar instabilidades; a API grava automaticamente arquivos de fallback em data/ para manter os dados disponíveis mesmo quando o scraping falhar.