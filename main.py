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

    print("開始點擊『查看』")

    buttons = page.get_by_text("查看")
    print("找到查看按鈕")
    print("查看總數：", buttons.count())

    for i in range(buttons.count()):
        print(
            i,
            buttons.nth(i).is_visible()
        )


    print("準備點擊第2個查看")

    buttons.nth(1).click(
        timeout=10000,
        force=True
    )

    print("已完成點擊查看")

    page.wait_for_timeout(5000)

    print("開始讀取頁面")

    text = page.locator("body").inner_text()

    print(text[-3000:])

    print("網頁文字長度：")
    print(len(text))

    browser.close()
