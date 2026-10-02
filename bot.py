import os
import time
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_KEY = os.environ["OPENAI_API_KEY"]

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
OPENAI_URL = "https://api.openai.com/v1/responses"


def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30
    )


def ask_ai(user_message):
    response = requests.post(
        OPENAI_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-5-mini",
            "input": user_message
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "")

    return "AI se response nahi mila."


def main():
    offset = None

    while True:
        try:
            params = {"timeout": 30}

            if offset is not None:
                params["offset"] = offset

            response = requests.get(
                f"{TELEGRAM_URL}/getUpdates",
                params=params,
                timeout=40
            )

            updates = response.json().get("result", [])

            for update in updates:
                offset = update["update_id"] + 1

                message = update.get("message")
                if not message or "text" not in message:
                    continue

                chat_id = message["chat"]["id"]
                user_text = message["text"]

                if user_text == "/start":
                    send_message(
                        chat_id,
                        "🤖 Namaste! Main ASHISH AI 2.0 hoon. Mujhse kuch bhi pooch sakte ho."
                    )
                else:
                    reply = ask_ai(user_text)
                    send_message(chat_id, reply)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
