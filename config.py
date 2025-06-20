"""Токены бота"""

import os
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
CHAT_GPT_TOKEN = os.getenv('CHAT_GPT_TOKEN')

if not all([TG_BOT_TOKEN, CHAT_GPT_TOKEN]):
    raise ValueError('Введите свои токены в .env')
