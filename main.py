import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

Загружаем токены из переменных окружения



BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




if not BOT_TOKEN:
raise ValueError("❌ Не найден BOT_TOKEN в переменных окружения.")
if not OPENAI_API_KEY:
raise ValueError("❌ Не найден OPENAI_API_KEY в переменных окружения.")

Инициализация клиентов



bot = Bot(
token=BOT_TOKEN,
default=DefaultBotProperties(parse_mode=types.ParseMode.HTML)
)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

Обработчик команды /start



@dp.message(Command("start"))
async def start_handler(message: Message):
await message.answer("👋 Привет! Я твой AI-бот. Напиши что-нибудь!")

Обработчик обычных сообщений



@dp.message(F.text)
async def handle_message(message: Message):
user_text = message.text

try:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты умный Telegram-бот-ассистент."},
            {"role": "user", "content": user_text},
        ],
    )

    bot_reply = response.choices[0].message.content
    await message.answer(bot_reply)

except Exception as e:
    await message.answer(f"⚠️ Ошибка: {e}")

Основной запуск



async def main():
await dp.start_polling(bot)




if name == "main":
asyncio.run(main())


