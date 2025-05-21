import json
import pytest

def get_token(client):
    resp = client.post('/api/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    return data['access_token']

def test_login_success(client):
    token = get_token(client)
    assert isinstance(token, str)

def test_login_failure(client):
    resp = client.post('/api/login', json={
        "username": "wrong", "password": "wrong"
    })
    assert resp.status_code == 401

def test_protected_without_token(client):
    resp = client.get('/api/producao')
    assert resp.status_code == 401

def test_protected_with_token(monkeypatch, client):
    # Monkeypatch scraping to return a known dict
    monkeypatch.setattr(
        'app.scraping._obter',
        lambda chave: {"dados": [{"foo": "bar"}]}
    )
    token = get_token(client)
    resp = client.get(
        '/api/producao',
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert resp.get_json() == {"dados": [{"foo": "bar"}]}
