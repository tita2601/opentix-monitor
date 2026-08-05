import requests
from bs4 import BeautifulSoup
import os
import json
import re


CONFIG_FILE = "config.json"
STATUS_FILE = "status.json"



def load_config():

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)



def load_status():

    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)

    except:
        return {
            "notified": False
        }



def save_status(status):

    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)



def check_ticket(event_url, max_price):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    response = requests.get(
        event_url,
        headers=headers
    )


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    text = soup.get_text()


    # 找出頁面中的價格
    prices = re.findall(
        r"\d{3,5}",
        text
    )


    for price in prices:

        price = int(price)

        if price <= max_price:

            return True, price


    return False, None



def send_line(message):

    token = os.environ["LINE_TOKEN"]

    user_id = os.environ["LINE_USER"]


    url = "https://api.line.me/v2/bot/message/push"


    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


    data = {

        "to": user_id,

        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }


    requests.post(
        url,
        headers=headers,
        json=data
    )



if __name__ == "__main__":


    config = load_config()

    status = load_status()


    found, price = check_ticket(
        config["event_url"],
        config["max_price"]
    )


    if found and not status["notified"]:


        message = (
            "🎫 OPENTIX售票提醒\n\n"
            f"節目：{config['event_name']}\n"
            f"符合價格：{price} 元\n"
            f"限制：{config['max_price']} 元以下\n\n"
            f"{config['event_url']}"
        )


        send_line(message)


        status["notified"] = True

        save_status(status)


    else:

        print("目前沒有符合條件的票")
