import os, json
import pytest
from app.scraping import _obter, DATA_DIR

def test_obter_fallback(tmp_path, monkeypatch):
    # prepara um fallback fake
    chave = 'producao'
    data = [{"x": 1}]
    p = tmp_path / f"{chave}.json"
    p.write_text(json.dumps(data))
    # força o DATA_DIR para tmp_path
    monkeypatch.setenv('DATA_DIR', str(tmp_path))
    monkeypatch.setattr('app.scraping.DATA_DIR', str(tmp_path))
    # simula falha de network
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: (_ for _ in ()).throw(Exception("fail")))
    result = _obter(chave)
    assert result == {"dados": data}

def test_obter_live(monkeypatch, tmp_path):
    # simula resposta HTML com uma tabela
    html = "<table><th>Col</th><tr><td>Val</td></tr></table>"
    class DummyResp:
        content = html.encode()
        def raise_for_status(self): pass
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: DummyResp())
    # monkeypatch DataDir para tmp_path
    monkeypatch.setattr('app.scraping.DATA_DIR', str(tmp_path))
    res = _obter('producao')
    assert "dados" in res
    assert isinstance(res["dados"], list)
