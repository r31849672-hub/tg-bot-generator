import os
import logging
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command  # Импортируем фильтр Command
import openai
from aiogram.client.default import DefaultBotProperties

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Не найдены BOT_TOKEN или OPENAI_API_KEY в переменных окружения.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# Dispatcher теперь создается без аргументов
dp = Dispatcher()

# Настраиваем OpenAI
openai.api_key = OPENAI_API_KEY


# Обработка команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Напиши что-нибудь!")


# Обработка обычных сообщений
@dp.message()
async def handle_message(message: Message):
    try:
        user_text = message.text

        # Получаем ответ от OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": user_text},
            ],
        )

        reply_text = response.choices[0].message.content
        await message.answer(reply_text)

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Проверь API-ключ или токен.")
        print(e)


# Запуск бота
async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


