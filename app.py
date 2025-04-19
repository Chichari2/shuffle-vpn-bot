import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import os
from dotenv import load_dotenv

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# Проверка токена
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ Токен бота не найден в .env файле!")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура с WebApp кнопкой (полноэкранный режим)
webapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text="🌐 Открыть VPN-панель",
            web_app=WebAppInfo(
                url="https://Chichari2.github.io/shuffletestvpn-web/",
                web_app_type="fullscreen"
            )
        )]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    logger.info(f"Новый пользователь: {message.from_user.id}")
    await message.answer(
        "🔐 Добро пожаловать в ShuffleVPN!\n\n"
        "Нажмите кнопку ниже для доступа к панели:",
        reply_markup=webapp_keyboard
    )

if __name__ == "__main__":
    logger.info("🟢 Запускаю бота...")
    try:
        dp.run_polling(bot)
    except Exception as e:
        logger.error(f"🔴 Ошибка: {e}")