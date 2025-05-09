import os
import logging
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ Токен бота не найден в .env файле!")
    exit(1)

API_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://вашдомен.com/webhook

app = Flask(__name__)

# URL веб-приложения
webapp_url = "https://chichari2.github.io/shuffle-vpn-bot/"

# Клавиатура с WebApp кнопкой
keyboard = {
    "keyboard": [[{
        "text": "🌐 Открыть VPN-панель",
        "web_app": {"url": webapp_url}
    }]],
    "resize_keyboard": True
}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    logger.info(f"📩 Получено сообщение: {data}")

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text')

        # Приветствие при /start
        if text == '/start':
            send_message(chat_id, "🔐 Добро пожаловать в ShuffleVPN!\n\nНажмите кнопку ниже для доступа к панели:", keyboard)

    return jsonify(ok=True)


def send_message(chat_id, text, reply_markup=None):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": reply_markup
    }
    response = requests.post(url, json=payload)
    logger.info(f"📤 Отправка сообщения: {response.status_code} — {response.text}")


@app.route('/setwebhook', methods=['GET'])
def set_webhook_route():
    response = set_webhook(WEBHOOK_URL)
    return jsonify(response)


def set_webhook(url):
    url_api = f"{API_URL}/setWebhook"
    payload = {
        "url": url,
        "drop_pending_updates": True
    }
    response = requests.post(url_api, json=payload)
    logger.info(f"🔧 Установка вебхука: {response.status_code} — {response.json()}")
    return response.json()


@app.route('/')
def index():
    # HTML для полноэкранного приложения
    html_code = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ShuffleVPN</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                font-family: Arial, sans-serif;
            }
            h1 {
                margin-bottom: 20px;
            }
            .button {
                display: block;
                width: 200px;
                margin: 10px;
                padding: 15px;
                font-size: 18px;
                text-align: center;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                text-decoration: none;
            }
            .button:hover {
                background-color: #45a049;
            }
            #close-button {
                position: absolute;
                top: 10px;
                right: 10px;
                background: red;
                color: white;
                border: none;
                padding: 10px;
                font-size: 20px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <button id="close-button" onclick="window.close()">❌</button>
        <h1>Выберите сервер VPN</h1>
        <a href="/connect?country=Germany" class="button">🇩🇪 Германия</a>
        <a href="/connect?country=USA" class="button">🇺🇸 США</a>
        <a href="/connect?country=France" class="button">🇫🇷 Франция</a>
        <a href="/connect?country=Netherlands" class="button">🇳🇱 Нидерланды</a>
    </body>
    </html>
    '''

    return render_template_string(html_code)


if __name__ == "__main__":
    logger.info("🟢 Запуск бота...")
    set_webhook(WEBHOOK_URL)
    app.run(host='0.0.0.0', port=5001)

