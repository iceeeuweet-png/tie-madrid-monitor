
import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

PROVINCES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla",
    "Alicante", "Málaga", "Murcia", "Zaragoza",
    "Cádiz", "Granada", "Toledo", "Segovia",
    "Valladolid", "Salamanca", "Burgos", "León",
    "Almería", "Córdoba", "Huelva", "Jaén",
    "Cáceres", "Badajoz", "Ciudad Real", "Cuenca",
    "Guadalajara", "Ávila", "Soria", "Palencia",
    "Zamora", "Girona", "Lleida", "Tarragona",
    "Castellón", "Albacete", "A Coruña", "Lugo",
    "Ourense", "Pontevedra", "Asturias", "Cantabria",
    "Álava", "Bizkaia", "Gipuzkoa", "Navarra",
    "La Rioja", "Huesca", "Teruel", "Las Palmas",
    "Santa Cruz de Tenerife", "Baleares",
"Ceuta", "Melilla"
]

def telegram(method, data=None):
    payload = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(BASE_URL + method, data=payload)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())

def send_message(chat_id, message, keyboard=None):
    data = {"chat_id": chat_id, "text": message}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    telegram("sendMessage", data)

def show_provinces(chat_id):
    buttons = [
        [{"text": province}] for province in PROVINCES
    ]
    buttons.insert(0, [{"text": "Toda España / All Spain"}])

    send_message(
        chat_id,
        "Select your province / Selecciona tu provincia:",
        {"keyboard": buttons, "resize_keyboard": True}
    )

def main():
    result = telegram("getUpdates", {"timeout": 0})

    for update in result.get("result", []):
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user_text = message.get("text", "").strip()

        if not chat_id:
            continue

        if user_text == "/start":
            send_message(
                chat_id,
                "Welcome to TIE Appointment Monitor!\n"
                "Bienvenido al monitor de citas TIE!\n\n"
                "Use /province to select a province."
            )

        elif user_text == "/province":
            show_provinces(chat_id)

        elif user_text == "Toda España / All Spain":
            send_message(
                chat_id,
                "Selected: All Spain / Toda España.\n"
                "Appointment checking is not active yet."
            )

        elif user_text in PROVINCES:
            send_message(
                chat_id,
                f"Selected: {user_text}\n"
                f"Provincia seleccionada: {user_text}\n\n"
                "Appointment checking is not active yet."
            )

        elif user_text == "/help":
            send_message(
                chat_id,
                "Commands / Comandos:\n"
                "/start - Start the bot\n"
                "/province - Select a province\n"
                "/help - Help"
            )

        else:
            send_message(
                chat_id,
                "Use /province to choose a province.\n"
                "Usa /province para elegir una provincia."
            )

    if result.get("result"):
        last_id = result["result"][-1]["update_id"]
        telegram("getUpdates", {"offset": last_id + 1, "timeout": 0})

if __name__ == "__main__":
    main()
