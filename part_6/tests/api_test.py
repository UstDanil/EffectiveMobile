import re
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_last_trading_dates_correct():
    response = client.get("/get_last_trading_dates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        assert isinstance(response.json()[0], str)
        assert re.findall(r"\d{4}-\d{2}-\d{2}", response.json()[0])


def test_get_last_trading_dates_correct_without_cache(mocker):
    mocker.patch("app.backend.redis_client.redis_client.get", return_value=None)
    response = client.get("/get_last_trading_dates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        assert isinstance(response.json()[0], str)
        assert re.findall(r"\d{4}-\d{2}-\d{2}", response.json()[0])


def test_get_dynamics_correct():
    response = client.get("/get_dynamics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        first_elem = response.json()[0]
        assert isinstance(first_elem, dict)
        assert "id" in first_elem and isinstance(uuid.UUID(first_elem["id"]), uuid.UUID)
        assert "delivery_basis_id" in first_elem and len(first_elem["delivery_basis_id"]) == 3
        assert all([key in first_elem for key in ["volume", "count", "total"]])
        assert all([isinstance(first_elem[key], int) for key in ["volume", "count", "total"]])
    response = client.get("/get_dynamics", params={"start_date": "2025-06-19", "end_date": "2025-06-20"})
    assert response.status_code == 200


def test_get_dynamics_correct_without_cache(mocker):
    mocker.patch('app.backend.redis_client.redis_client.get', return_value=None)
    response = client.get("/get_dynamics")
    assert response.status_code == 200


def test_get_dynamics_wrong_data_param():
    response = client.get("/get_dynamics", params={"start_date": "not_datetime", "end_date": "not_datetime"})
    assert response.status_code == 422


def test_get_trading_results():
    response = client.get("/get_trading_results")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json():
        first_elem = response.json()[0]
        assert isinstance(first_elem, dict)
        assert "id" in first_elem and isinstance(uuid.UUID(first_elem["id"]), uuid.UUID)
        assert "delivery_basis_id" in first_elem and len(first_elem["delivery_basis_id"]) == 3
        assert all([key in first_elem for key in ["volume", "count", "total"]])
        assert all([isinstance(first_elem[key], int) for key in ["volume", "count", "total"]])


def test_get_trading_results_without_cache(mocker):
    mocker.patch('app.backend.redis_client.redis_client.get', return_value=None)
    response = client.get("/get_trading_results")
    assert response.status_code == 200
