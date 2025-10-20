import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram import F
import asyncio
import openai

# Логирование (помогает отслеживать ошибки)
logging.basicConfig(level=logging.INFO)

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка токенов
if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в переменных окружения.")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не найден OPENAI_API_KEY в переменных окружения.")

# Настройка API OpenAI
openai.api_key = OPENAI_API_KEY

# Инициализация бота и диспетчера
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в переменных окружения.")

# Новый синтаксис для aiogram 3.x
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=types.ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🤖 Привет! Я AI-копирайтер. Введи тему, и я создам продающий текст.\n\n"
        "✍️ Просто напиши, что тебе нужно: пост, описание товара, сторис и т.д."
    )

@dp.message(F.text)
async def generate_text(message: Message):
    user_input = message.text.strip()

    await message.answer("⏳ Генерирую текст, подожди пару секунд...")

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты опытный копирайтер, создавай тексты живые, понятные и продающие."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.9
        )

        reply = completion.choices[0].message.content
        await message.answer(reply)

    except Exception as e:
        logging.error(e)
        await message.answer("⚠️ Произошла ошибка при генерации. Попробуй снова позже.")


