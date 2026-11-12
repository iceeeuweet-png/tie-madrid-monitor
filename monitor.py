
import os
import json
import urllib.request
import urllib.parse
import urllib.error

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from GitHub Secrets.")

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

SERVICES = [
    "Toma de Huellas (Expedición de Tarjeta)",
    "Recogida de Tarjeta TIE"
]


def telegram(method, data=None):
    payload = urllib.parse.urlencode(data or {}).encode("utf-8")

    request = urllib.request.Request(
        BASE_URL + method,
        data=payload
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")

    return result


def send_message(chat_id, message, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": message
    }

    if keyboard:
        data["reply_markup"] = json.dumps(
            keyboard,
            ensure_ascii=False
        )

    telegram("sendMessage", data)


def show_services(chat_id):
    buttons = [
        [{"text": service}]
        for service in SERVICES
    ]

    send_message(
        chat_id,
        "Select your service / Selecciona tu trámite:",
        {
            "keyboard": buttons,
            "resize_keyboard": True
        }
    )


def show_provinces(chat_id):
    buttons = [
        [{"text": "Toda España / All Spain"}]
    ]

    buttons.extend(
        [[{"text": province}] for province in PROVINCES]
    )

    send_message(
        chat_id,
        "Select your province / Selecciona tu provincia:",
        {
            "keyboard": buttons,
            "resize_keyboard": True
        }
    )


def process_update(update):
    message = update.get("message", {})

    chat_id = message.get("chat", {}).get("id")
    user_text = message.get("text", "").strip()

    if not chat_id or not user_text:
        print("Ignored update without a text message.")
        return

    print(
        f"Processing update {update.get('update_id')} "
        f"with message: {user_text}"
    )

    if user_text == "/start":
        send_message(
            chat_id,
            "Welcome to TIE Appointment Monitor!\n"
            "¡Bienvenido al monitor de citas TIE!\n\n"
            "Choose an option below / Elige una opción:"
        )
        show_services(chat_id)

    elif user_text == "/help":
        send_message(
            chat_id,
            "Commands / Comandos:\n"
            "/start - Start the bot\n"
            "/province - Select a province\n"
            "/help - Help"
        )

    elif user_text == "/province":
        show_provinces(chat_id)

    elif user_text in SERVICES:
        send_message(
            chat_id,
            "Selected service / Trámite seleccionado:\n"
            + user_text
        )
        show_provinces(chat_id)

    elif user_text == "Toda España / All Spain":
        send_message(
            chat_id,
            "Selected: All Spain / Toda España.\n\n"
            "Appointment checking is not active yet.\n"
            "La búsqueda de citas todavía no está activa."
        )

    elif user_text in PROVINCES:
        send_message(
            chat_id,
            f"Selected province: {user_text}\n"
            f"Provincia seleccionada: {user_text}\n\n"
            "Appointment checking is not active yet.\n"
            "La búsqueda de citas todavía no está activa."
        )

    else:
        send_message(
            chat_id,
            "Please use /start or /province.\n"
            "Por favor, utiliza /start o /province."
        )


def main():
    print("Madrid TIE Monitor started.")

    result = telegram(
        "getUpdates",
        {
            "timeout": 0,
            "allowed_updates": json.dumps(["message"])
        }
    )

    updates = result.get("result", [])

    print(f"Received {len(updates)} update(s).")

    for update in updates:
        try:
            process_update(update)
        except Exception as error:
            print(
                f"Error processing update "
                f"{update.get('update_id')}: {error}"
            )

    if updates:
        last_id = updates[-1]["update_id"]

        telegram(
            "getUpdates",
            {
                "offset": last_id + 1,
                "timeout": 0
            }
        )

        print("Processed updates acknowledged.")

    print("Madrid TIE Monitor finished.")


if __name__ == "__main__":
    main()
