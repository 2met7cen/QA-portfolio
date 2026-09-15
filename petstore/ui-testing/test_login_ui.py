from playwright.sync_api import sync_playwright


def test_pets_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False, slow_mo=300)
        page = browser.new_page()

        page.goto("https://X-X-X.com/login")
        page.locator('input').nth(0).fill("testuser")
        page.locator('input').nth(1).fill("12345678")
        page.locator('button[type="submit"]').click()
        page.wait_for_url("**/task", timeout=5000)

        page.goto("https://X-X-X.com/pets")
        page.wait_for_selector('table.clip-table tbody tr', timeout=10000)
        page.screenshot(path="pets_visible.png", full_page=True)

        rows = page.locator('table.clip-table tbody tr').count()
        assert rows > 0, "В таблице нет питомцев"

        browser.close()


if __name__ == "__main__":
    test_pets_visible()
