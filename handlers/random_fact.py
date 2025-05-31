import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.basic import start
from services.open_ai import get_random_fact


logger = logging.getLogger(__name__)

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        loading_msg = await update.effective_message.reply_text('Ищу интересный факт...')
        fact = await get_random_fact()
        keyboard = [
            [InlineKeyboardButton('Еще один', callback_data='random_more')],
            [InlineKeyboardButton('Выйти', callback_data='random_finish')]
        ]
        replay_markup = InlineKeyboardMarkup(keyboard)

        await update.effective_message.reply_text('Хочешь еще факт или хочешь выйти?')
        await loading_msg.edit_text(
            f'<b>Как тебе такое?</b>\n\n{fact}',
            parse_mode='HTML',
            reply_markup=replay_markup

        )

    except Exception as e:
        logger.exception(f'Ошибка в рандом факте {e}')
        await update.message.reply_text('Не получилось, произошла ошибка')


async def random_fact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'random_more':
        await random_fact(update, context)
    elif query.data == 'random_finish':
        await start(update, context)
    elif query.data == 'random_fact':
        await random_fact(update, context)