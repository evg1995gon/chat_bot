import logging
import openai
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types


load_dotenv()

# Getting API keys from environment
API_TOKEN = os.getenv('TELEGRAM_API')
GPT_API = os.getenv('GPT_API')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Preparing GPT
openai.api_key = os.getenv('GPT_API')
messages = []
messages.append({"role": "system", "content": "You are a helpful assistant that speaks and understand Russian language."})


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ буду помогать тебе, спроси у меня что-нибудь\nНапример придумай 5 имен которые начинаются на букву 'Ю'")


@dp.message_handler()
async def echo(message: types.Message):
    """Телеграм handler в котором реализована логика Chat-GPT."""
    messages.append({"role": "user", "content": str(message)})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    await message.answer(reply)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
