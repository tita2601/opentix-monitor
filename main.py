from playwright.sync_api import sync_playwright
import json
import os
import requests


# =========================
# 基本設定
# =========================

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

url = config["event_url"]

PRICE_LIMIT = 3800

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_USER = os.environ.get("LINE_USER")


# =========================
# LINE 通知
# =========================

def send_line(message):

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": LINE_USER,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(
        "https://api.line.api/v2/bot/message/push",
        headers=headers,
        json=data,
        timeout=30
    )

    print("LINE 狀態：", response.status_code)


# =========================
# 開始監控
# =========================

print("開始開啟 OPENTIX")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    page = browser.new_page(
        viewport={
            "width": 1280,
            "height": 900
        }
    )

    print("開始載入網頁")

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("網頁基本載入完成")

    page.wait_for_timeout(15000)


    # =========================
    # 關閉翻譯提示
    # =========================

    try:

        got_it = page.get_by_text("Got it")

        if got_it.is_visible():
            got_it.click()
            print("已關閉翻譯提示")

    except Exception:

        print("沒有找到翻譯提示")


    print("開始分析 OPENTIX")


    # =========================
    # 找電腦配位
    # =========================

    seat_buttons = page.get_by_text("電腦配位")

    print(
        "電腦配位數量：",
        seat_buttons.count()
    )

    clicked = False

    for i in range(seat_buttons.count()):

        if seat_buttons.nth(i).is_visible():

            print(
                "點擊第",
                i,
                "個電腦配位"
            )

            seat_buttons.nth(i).click(
                timeout=10000
            )

            clicked = True
            break


    if not clicked:

        print("找不到可以點擊的電腦配位")

        browser.close()
        exit()


    print("電腦配位已點擊")

    page.wait_for_timeout(5000)


    # =========================
    # 讀取頁面
    # =========================

    text = page.locator("body").inner_text()

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    # =========================
    # 找場次
    # =========================

    show_time = None

    for line in lines:

        if (
            line.startswith("2026/")
            and ":" in line
        ):

            show_time = line
            break


    print(
        "場次：",
        show_time
    )


    # =========================
    # 找票價與剩餘數量
    # =========================

    available_tickets = []

    print("========== 票價分析 ==========")


    for i, line in enumerate(lines):

        if "元區" not in line:
            continue


        # -------------------------
        # 取得票價
        # -------------------------

        try:

            price_text = line.split("$")[1]

            price_text = price_text.replace(
                ",",
                ""
            )

            price = int(price_text)

        except Exception:

            continue


        # -------------------------
        # 找最近的「剩：」
        # -------------------------

        remaining = None


        for j in range(
            i + 1,
            min(i + 15, len(lines))
        ):

            next_line = lines[j]


            if next_line.startswith("剩："):

                remaining_text = (
                    next_line
                    .replace("剩：", "")
                    .strip()
                )


                # 「剩：0 ／ 完售」
                if "／" in remaining_text:

                    remaining_text = (
                        remaining_text
                        .split("／")[0]
                        .strip()
                    )


                try:

                    remaining = int(
                        remaining_text
                    )

                except Exception:

                    remaining = None


                break


        print(
            "票價：",
            price,
            "剩餘：",
            remaining
        )


        # -------------------------
        # 判斷是否符合條件
        # -------------------------

        if (
            price <= PRICE_LIMIT
            and remaining is not None
            and remaining > 0
        ):

            available_tickets.append(
                {
                    "price": price,
                    "remaining": remaining
                }
            )


    # =========================
    # LINE 通知
    # =========================

    if available_tickets:

        message = (
            "🎫《神隱少女》舞台劇\n\n"
        )


        if show_time:

            message += (
                f"📅 場次：{show_time}\n"
            )


        message += (
            "\n🎟️ 找到 3800 元以下票券：\n"
        )


        for ticket in available_tickets:

            message += (
                f"💰 ${ticket['price']:,} "
                f"剩餘 {ticket['remaining']} 張\n"
            )


        message += (
            "\n🔔 請盡快前往 OPENTIX 查看！"
        )


        print(
            "========== 發送 LINE =========="
        )

        print(message)

        send_line(message)


    else:

        print(
            "目前沒有符合條件的票券"
        )


    browser.close()


print("程式執行完成")
