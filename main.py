from playwright.sync_api import sync_playwright
import json


# 讀取設定
with open("config.json", "r", encoding="utf-8") as f:
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

    page = browser.new_page(
        viewport={"width": 1280, "height": 900}
    )

    print("開始載入網頁")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("網頁基本載入完成")

    # 給 OPENTIX JavaScript 足夠時間載入
    page.wait_for_timeout(15000)

    print("開始分析 OPENTIX 頁面")

    # 網頁標題
    print("========== 網頁標題 ==========")
    print(page.title())

    # 整個網頁文字
    text = page.locator("body").inner_text()

    print("========== 網頁文字長度 ==========")
    print(len(text))

    # 搜尋可能與售票有關的關鍵字
    print("========== 關鍵字檢查 ==========")

    keywords = [
        "2026/12/31",
        "2026年12月",
        "19:30",
        "3800",
        "4800",
        "5800",
        "自行選位",
        "電腦配位",
        "購票資訊",
        "售票"
    ]

    for keyword in keywords:
        print(keyword, "→", keyword in text)

    # 找出包含價格的文字行
    print("========== 包含價格的文字 ==========")

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if any(
            price in line
            for price in [
                "3800",
                "4800",
                "5800",
                "2800",
                "3300",
                "3500"
            ]
        ):
            print(line)

    # 輸出最後 5000 字
    print("========== 網頁最後 5000 字 ==========")
    print(text[-5000:])

    browser.close()

print("程式執行完成")
