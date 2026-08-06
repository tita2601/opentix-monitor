from playwright.sync_api import sync_playwright
import json


with open("config.json", "r") as f:
    config = json.load(f)


url = config["event_url"]


print("開始開啟 OPENTIX")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = browser.new_page()


    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(15000)
    # 再等一下讓畫面完全載入
    page.wait_for_timeout(3000)

    print("===== 找日期與票價文字 =====")

    text = page.locator("body").inner_text()

    keywords = [
        "2026",
        "12月",
        "3800",
        "票",
        "元",
        "NT"
    ]

    for k in keywords:
        print(
            k,
            k in text
        )

    print("===== 後3000字 =====")
    print(text[-3000:])

    print("網頁文字長度：")
    print(len(text))

    browser.close()
