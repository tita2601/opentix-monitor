import requests
from bs4 import BeautifulSoup
import os


EVENT_URL = "https://www.opentix.life/event/2076925048527581185"


def check_ticket():

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }


    response = requests.get(
        EVENT_URL,
        headers=headers
    )


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    page_text = soup.get_text()


    keywords = [
        "立即購票",
        "購票",
        "票價"
    ]


    for word in keywords:

        if word in page_text:

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

        "to":
        user_id,

        "messages":[

            {
            "type":"text",
            "text":message
            }

        ]

    }


    requests.post(
        url,
        headers=headers,
        json=data
    )



if __name__ == "__main__":


    if check_ticket():

        send_line(
            "🎫 OPENTIX可能有票！\n"
            + EVENT_URL
        )


    else:

        print(
            "目前沒有偵測到售票"
        )
