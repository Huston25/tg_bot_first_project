import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎲 Рандомный факт", callback_data="random_fact")],
        [InlineKeyboardButton("🤖 ChatGPT", callback_data="gpt_interface")],
        [InlineKeyboardButton("👥 Диалог с личностью", callback_data="talk_interface")],
        [InlineKeyboardButton("🧠 Квиз", callback_data="quiz_interface")],
        [InlineKeyboardButton("🎭 Рекомендации кино, книг, сериала", callback_data="recc_command")]
    ]
    replay_markup = InlineKeyboardMarkup(keyboard)


    welcome_text = (
        "🎉 <b>Добро пожаловать в ChatGPT бота!</b>\n\n"
        "🚀 <b>Доступные функции:</b>\n"
        "    💡 Рандомный факт - получи интересный факт\n"
        "    🤖 ChatGPT - общение с ИИ\n"
        "    🤩Диалог с личностью - говори с известными людьми\n"
        "    🎯 Квиз - проверь свои знания\n\n"
        "     🎭 Рекомендации кино, книг, сериала\n\n"
        "Выберите функцию из меню ниже:"
    )
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=welcome_text, parse_mode='HTML', reply_markup=replay_markup)


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()






