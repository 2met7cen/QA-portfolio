from playwright.sync_api import sync_playwright


def test_open_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()
        page.goto("https://X-X-X.com/")
        page.screenshot(path="homepage.png")
        browser.close()


if __name__ == "__main__":
    test_open_homepage()
