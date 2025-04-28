import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv
import asyncio

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

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура с WebApp кнопкой
webapp_url = "https://chichari2.github.io/shuffle-vpn-bot/"
webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(
            text="🌐 Открыть VPN-панель",
            web_app=WebAppInfo(url=webapp_url)
        )
    ]],
    resize_keyboard=True
)

# Временное хранилище для отслеживания пользователей, которым было отправлено приветственное сообщение
sent_welcome_users = set()
user_locks = {}

# Ожидание для обработки многократных запросов
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    # Создаём lock для каждого пользователя, чтобы избежать параллельных отправок
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()

    async with user_locks[user_id]:
        if user_id not in sent_welcome_users:
            logger.info(f"Новый пользователь: {user_id}")
            await message.answer(
                "🔐 Добро пожаловать в ShuffleVPN!\n\n"
                "Нажмите кнопку ниже для доступа к панели:",
                reply_markup=webapp_keyboard
            )
            sent_welcome_users.add(user_id)  # Добавляем в список отправленных

@dp.message(Command("start"))
async def start(message: types.Message):
    await send_welcome(message)

if __name__ == "__main__":
    logger.info("🟢 Запуск бота...")
    try:
        dp.run_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"🔴 Ошибка: {e}")

