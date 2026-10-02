import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_KEY = os.environ["OPENAI_API_KEY"]

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def ask_ai(message):
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-5-mini",
        "input": message
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["output"][0]["content"][0]["text"]

def main():
    offset = None

    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"timeout": 30}

        if offset:
            params["offset"] = offset

        response = requests.get(url, params=params).json()

        for update in response.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            user_text = message["text"]

            try:
                reply = ask_ai(user_text)
            except Exception:
                reply = "Sorry, abhi AI response nahi de pa raha hoon."

            send_message(chat_id, reply)

if __name__ == "__main__":
    main()
