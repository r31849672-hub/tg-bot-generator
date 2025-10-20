import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем токены из переменных окружения

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Создаем экземпляр бота

bot = Bot(token=BOT_TOKEN)  # убрали parse_mode, чтобы избежать ошибки
dp = Dispatcher(bot)

# Обработчик команды /start

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
await message.reply("Привет! Я Telegram-бот, готов к работе 🚀")

# Запуск бота

if **name** == "**main**":
executor.start_polling(dp, skip_updates=True)



