from flask.testing import FlaskClient


def test_shopping_rejects_not_logged_in(client: FlaskClient):
    response = client.get("/api/reports/shopping/uid1")
    assert response.status_code == 401


def test_shopping_returns_404_on_invalid_trip_id(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/reports/shopping/uid100")
    assert response.status_code == 404


def test_shopping_returns_data(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/reports/shopping/uid1")
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 14
    assert response.json[0]["id"] == 1
    assert response.json[0]["name"] == "Multigrain cereal"
    assert response.json[0]["mass"] == 1200
    assert response.json[4]["id"] == 9
    assert response.json[4]["name"] == "Ptitsa divnaya sweet"
    assert response.json[4]["mass"] == 600
    assert response.json[4]["pieces"] > 109


def test_shopping_returns_data_non_shared_trip(org_logged_client: FlaskClient):
    response = org_logged_client.get("/api/reports/shopping/uid3")
    assert response.status_code == 200
    assert response.json
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1
    assert response.json[0]["mass"] == 60
    assert response.json[0]["name"] == "Multigrain cereal"
