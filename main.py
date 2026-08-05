import requests
import os


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

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("LINE response:")
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":

    send_line(
        "🎉 OPENTIX監控系統測試成功！"
    )
