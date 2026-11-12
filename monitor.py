
import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


def telegram(method, data=None):
    payload = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(BASE_URL + method, data=payload)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def send_message(chat_id, message):
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": message
    })


def main():
    result = telegram("getUpdates", {"timeout": 0})

    if not result.get("ok"):
        raise RuntimeError("Telegram API error")

    updates = result.get("result", [])
    next_offset = None

    for update in updates:
        next_offset = update["update_id"] + 1

        message = update.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        user_text = message.get("text", "").strip()

        if not chat_id:
            continue

        if user_text == "/start":
            send_message(
                chat_id,
                "🇪🇸 Welcome to Spain TIE Appointment Monitor!\n\n"
                "Bienvenido a Spain TIE Appointment Monitor!\n\n"
                "Please send the province where you want an appointment.\n"
                "Por favor, envía la provincia donde quieres una cita.\n\n"
                "Examples / Ejemplos:\n"
                "Madrid\n"
                "Barcelona\n"
                "Valencia\n"
                "All Spain / Toda España"
            )

        elif user_text == "/help":
            send_message(
                chat_id,
                "Send a province name or 'All Spain'.\n"
                "Envía el nombre de una provincia o 'Toda España'."
            )

        else:
            send_message(
                chat_id,
                "Your request has been received.\n"
                "Hemos recibido tu solicitud.\n\n"
                f"Requested area / Zona solicitada: {user_text}\n\n"
                "Appointment search is not active yet.\n"
                "La búsqueda de citas todavía no está activa."
            )

    if next_offset is not None:
        telegram("getUpdates", {
            "offset": next_offset,
            "timeout": 0
        })

    print("Updates processed:", len(updates))


if __name__ == "__main__":
    main()
