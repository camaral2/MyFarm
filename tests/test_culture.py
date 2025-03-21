import pytest


def test_create_culture(authorized_client):
    data = { "name": "Abobora" }

    res = authorized_client.post("/culture/", json=data)
    assert res.status_code == 201