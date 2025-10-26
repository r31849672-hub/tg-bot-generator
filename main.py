import os
import logging
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
import openai

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Не найдены BOT_TOKEN или OPENAI_API_KEY в .env файле.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Настройка бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

openai.api_key = OPENAI_API_KEY


@dp.message()
async def handle_message(message: types.Message):
    try:
        user_text = message.text

        # Запрос к OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помогаешь писать креативные посты и тексты для соцсетей."},
                {"role": "user", "content": user_text},
            ],
        )

        reply_text = response.choices[0].message.content
        await message.answer(reply_text)

    except Exception as e:
        logging.error(e)
        await message.answer("⚠️ Произошла ошибка. Проверь API-ключ или токен.")


async def main():
    print("🚀 Бот запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
