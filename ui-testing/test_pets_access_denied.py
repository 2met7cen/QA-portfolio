from playwright.sync_api import sync_playwright


def test_unauthorized_access_to_pets():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        try:
            page.goto(
                "https://X-X-X.com/login",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            page.goto(
                "https://X-X-X.com/pets",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            assert "/pets" not in page.url, "Доступ к /pets без логина разрешён"
        finally:
            browser.close()


if __name__ == "__main__":
    test_unauthorized_access_to_pets()
