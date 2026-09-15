import requests

TOKEN = "XXX"


def get_me():
    return requests.get(
        "https://X-X-X.com/api/auth/me",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )


if __name__ == "__main__":
    get_me()
