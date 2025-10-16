import uuid

async def test_create_and_get_user(client):
    payload = {"username": f"user_{uuid.uuid4().hex[:6]}", "email": f"u{uuid.uuid4().hex[:6]}@x.com"}
    r = await client.post("/users/", json=payload)
    assert r.status_code == 201, r.text
    user = r.json()
    r2 = await client.get(f"/users/{user['id']}")
    assert r2.status_code == 200, r2.text
    assert r2.json()["email"] == payload["email"]
