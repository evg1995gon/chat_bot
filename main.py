import logging
import openai
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from logic import message_gpt

load_dotenv()

# Getting API keys from environment
API_TOKEN = os.getenv('TELEGRAM_API')


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Preparing GPT
openai.api_key = os.getenv('GPT_API')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!\
\nЯ буду помогать тебе, спроси у меня что-нибудь...\
\nНапример придумай 5 имен которые начинаются на букву 'Ю'"
    )


@dp.message_handler()
async def echo(message: types.Message):
    """Телеграм handler в котором реализована логика Chat-GPT."""
    await message.answer(message_gpt(message))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
