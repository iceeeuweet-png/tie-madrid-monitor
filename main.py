
import os
import json
import time
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

def telegram_request(method, data=None):
    url = BASE_URL + method
    payload = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(url, data=payload)
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode())

def send_message(chat_id, message):
    telegram_request("sendMessage", {
        "chat_id": chat_id,
        "text": message
    })

def main():
    offset = None
    print("TIE Madrid Monitor bot started")

    while True:
        try:
            data = {"timeout": 30}
            if offset is not None:
                data["offset"] = offset

            result = telegram_request("getUpdates", data)

            for update in result.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                text = message.get("text", "")

                if not chat_id:
                    continue

                if text == "/start":
                    send_message(
                        chat_id,
                        "Welcome to TIE Madrid Monitor! "
                        "Your Telegram bot is connected."
                    )
                elif text == "/help":
                    send_message(
                        chat_id,
                        "The monitoring service is being prepared."
                    )

        except Exception as error:
            print("Error:", error)
            time.sleep(5)

if __name__ == "__main__":
    main()
