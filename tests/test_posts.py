async def test_create_and_list_posts(client):
    # crear autor
    u = await client.post("/users/", json={"username":"author1","email":"a1@x.com"})
    uid = u.json()["id"]
    # crear post
    p = await client.post("/posts/", json={"title":"Hola","content":"Contenido","author_id":uid})
    assert p.status_code == 201, p.text
    # listar
    r = await client.get("/posts/?limit=5")
    assert r.status_code == 200, r.text
    assert len(r.json()) >= 1
