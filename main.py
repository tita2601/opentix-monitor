from playwright.sync_api import sync_playwright
import json


with open("config.json", "r") as f:
    config = json.load(f)


url = config["event_url"]


print("開始開啟 OPENTIX")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = browser.new_page()


    page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )
    
    page.wait_for_timeout(5000)

    title = page.title()

    print("網頁標題：")
    print(title)


    text = page.locator("body").inner_text()


    print("網頁文字前500字：")
    print(text[:500])


    browser.close()
