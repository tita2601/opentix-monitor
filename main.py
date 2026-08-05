import requests
from bs4 import BeautifulSoup
import os
import json


EVENT_URL = "https://www.opentix.life/event/2076925048527581185"

STATUS_FILE = "status.json"


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



def check_ticket():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    response = requests.get(
        EVENT_URL,
        headers=headers
    )


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    text = soup.get_text()


    keywords = [
        "立即購票",
        "購票"
    ]


    for word in keywords:

        if word in text:
            return True


    return False



def send_line(message):

    token = os.environ["LINE_TOKEN"]

    user_id = os.environ["LINE_USER"]


    url = "https://api.line.me/v2/bot/message/push"


    headers = {

        "Authorization":
        f"Bearer {token}",

        "Content-Type":
        "application/json"

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


    status = load_status()


    ticket = check_ticket()


    if ticket and not status["notified"]:


        send_line(
            "🎫 OPENTIX可能開放購票！\n"
            + EVENT_URL
        )


        status["notified"] = True


        save_status(status)


    else:

        print(
            "沒有新的售票通知"
        )
