import pytest
import requests

BASE_URL = "https://X-X-X.com"
TOKEN = "XXX"  # подставь свой токен


@pytest.fixture
def auth_token():
    return TOKEN


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def created_pet_id(auth_headers):
    pet_data = {
        "name": "Барсик",
        "category_id": 1,
        "status": "available",
        "price": 100.50,
        "description": "Тестик",
    }
    response = requests.post(f"{BASE_URL}/api/pets", json=pet_data, headers=auth_headers)
    assert response.status_code == 201, f"Ошибка создания питомца: {response.status_code}"
    pet_id = response.json().get("id")
    assert pet_id is not None, "ID питомца не получен"
    return pet_id


def test_get_pets(auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/pets",
        headers=auth_headers,
        params={"limit": 1},
    )
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"


def test_create_pet(auth_headers):
    pet_data = {
        "name": "Мурка",
        "category_id": 2,
        "status": "available",
        "price": 500,
        "description": "Тестик",
    }
    response = requests.post(f"{BASE_URL}/api/pets", json=pet_data, headers=auth_headers)
    assert response.status_code == 201, f"Ошибка создания: {response.status_code}"
    data = response.json()
    assert "id" in data, "В ответе нет id"
    assert data["name"] == pet_data["name"], "Имя не совпадает"


def test_get_pets_with_created(created_pet_id, auth_headers):
    response = requests.get(
        f"{BASE_URL}/api/pets",
        headers=auth_headers,
        params={"limit": 100},
    )
    assert response.status_code == 200
    pets = response.json().get("data", [])
    ids = [pet["id"] for pet in pets]
    assert created_pet_id in ids, f"Питомец с id {created_pet_id} не найден в списке"
