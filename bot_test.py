import os
import json
import urllib.request
import urllib.parse

token = os.environ["TELEGRAM_BOT_TOKEN"]
base_url = f"https://api.telegram.org/bot{token}/"

def telegram(method, data=None):
    body = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(base_url + method, data=body)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())

updates = telegram("getUpdates", {"timeout": 20})

messages = updates.get("result", [])
print("Messages received:", len(messages))

if not updates.get("ok"):
    raise Exception("Telegram API returned an error")

if messages:
    chat_id = messages[-1]["message"]["chat"]["id"]

    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": "✅ Telegram connection successful! Your bot is working."
    })

    print("Test message sent successfully.")
else:
    print("No incoming messages. Send /start to the bot and try again.")
