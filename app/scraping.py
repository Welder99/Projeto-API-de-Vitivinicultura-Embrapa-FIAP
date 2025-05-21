import os
import json
import requests
from bs4 import BeautifulSoup

# Mapeia chaves para URLs
URLS = {
    "producao":      "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "comercializacao":"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "importacao":    "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
    "exportacao":    "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06",
}

# Pasta onde ficam os JSONs de fallback
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

def obter_dados_producao():
    return _obter("producao")

def obter_dados_processamento():
    return _obter("processamento")

def obter_dados_comercializacao():
    return _obter("comercializacao")

def obter_dados_importacao():
    return _obter("importacao")

def obter_dados_exportacao():
    return _obter("exportacao")


def _obter(chave: str):
    """
    Tenta scrapear a URL ao vivo. Em caso de sucesso:
      - Extrai as tabelas,
      - Salva em data/{chave}.json,
      - Retorna {"dados": [...]}

    Se falhar qualquer erro, tenta ler data/{chave}.json.
    Se não existir, retorna erro.
    """
    url = URLS.get(chave)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        resultado = []
        for tbl in soup.find_all("table"):
            headers = [th.get_text(strip=True) for th in tbl.find_all("th")]
            rows = []
            for tr in tbl.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    rows.append(dict(zip(headers, cols)))
            if rows:
                resultado.append(rows)

        # salva JSON de fallback
        fallback_path = os.path.join(DATA_DIR, f"{chave}.json")
        with open(fallback_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        return {"dados": resultado}

    except Exception as e:
        # tenta o fallback local em qualquer erro
        fallback_path = os.path.join(DATA_DIR, f"{chave}.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {"dados": data}
        # sem fallback, retornamos erro
        return {"error": f"Scraping falhou e não há JSON de fallback ({e})"}, 500
