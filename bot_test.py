
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

for update in updates.get("result", []):
    message = update.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if chat_id:
        telegram("sendMessage", {
            "chat_id": chat_id,
            "text": "✅ TIE Madrid Monitor: Telegram connection successful!"
        })

print("Telegram test completed.")
