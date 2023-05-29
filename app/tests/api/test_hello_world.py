def test_hello_world(client):
    response = client.get("/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, World!", "environment": "Test"}
