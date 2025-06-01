import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.open_ai import get_chatgpt_response
import os

logger = logging.getLogger(__name__)

CAPTION = '<b>Можешь задавать свой вопрос чату GPT</b>\n\n'
WAITING_FOR_MESSAGE = 1

async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await gpt_start(update, context)

async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        image_path = 'images/chat-gpt.png'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                if update.callback_query:
                    await update.callback_query.message.reply_photo(
                        photo=photo,
                        caption=CAPTION,
                        parse_mode='HTML'
                    )

                else:
                    await update.callback_query.message.reply_photo(
                        photo=photo,
                        caption=CAPTION,
                        parse_mode='HTML'
                    )
        else:
            message_text = CAPTION
            if update.callback_query:
                await update.callback_query.edit_message_text(message_text, parse_mode='HTML')
            else:
                await update.message.reply_text(message_text, parse_mode='HTML')


        if update.callback_query:
            await update.callback_query.answer()

        return WAITING_FOR_MESSAGE
    except Exception as e:
        logger.error(f'Ошибка при запуске ChatGPT {e}')
        error_text = 'При запуске произошла ошибка, повторите или попробуйте позже'
        if update.callback_query:
            await update.callback_query.edit_message_text(error_text)
        else:
            await update.message.reply_text(error_text)

        return -1


async def handle_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        processing_msg = await update.message.reply_text('Думаю...')

        get_response = await get_chatgpt_response(user_message)

        keyboard = [
            [InlineKeyboardButton('Задать еще вопрос', callback_data='continue')],
            [InlineKeyboardButton('Вернуться в меню', callback_data='finish')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)


        await processing_msg.delete()
        await update.message.reply_text(
            f'<b>Отвечаю на твой вопрос</b>\n\n{get_response}',
            parse_mode='HTML',
            reply_markup=reply_markup

        )

        return WAITING_FOR_MESSAGE
    except Exception as e:
        logger.error(f'Ошибка при обработке сообщения GPT {e}')
        await update.message.reply_text(
            'Произошла ошибка. Попробуйте еще раз или вернитесь в главное меню',
        )
        return WAITING_FOR_MESSAGE