def test_healthz(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}

def test_root_redirects_to_swagger(client):
    resp = client.get('/', follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'].endswith('/swagger/')
