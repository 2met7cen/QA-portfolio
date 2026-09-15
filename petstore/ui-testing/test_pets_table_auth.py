from playwright.sync_api import sync_playwright

TOKEN = "XXX"


def test_authenticated_pets():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        page.add_init_script(f"localStorage.setItem('token', '{TOKEN}');")

        page.goto(
            "https://X-X-X.com/pets",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        page.wait_for_selector("body", state="visible", timeout=10000)

        browser.close()
