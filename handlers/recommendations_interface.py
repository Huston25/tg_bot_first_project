"""Интерфейс с рекомендациями"""


import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from services.open_ai import client, get_recommendation_response

logger = logging.getLogger(__name__)
TYPE, ORIGIN, GENRE, MOOD, GOAL, RECOMMENDING = range(6)

async def recc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /recommendation"""
    return await recc_start(update, context)

async def recc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
        [InlineKeyboardButton("📖 Книга", callback_data="book")],
        [InlineKeyboardButton("🎬 Фильм", callback_data="movie")],
        [InlineKeyboardButton("📺 Сериал", callback_data="series")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(
                "Я помогу тебе подобрать книгу, фильм или сериал под твое настроение. \nТолько скажи:",
                reply_markup=reply_markup
            )
        elif update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(
                "Я помогу тебе подобрать книгу, фильм или сериал под твое настроение. \nТолько скажи:",
                reply_markup=reply_markup
            )
        logger.info('Ответ при нажатии на кнопку рекомендаций')
        return TYPE

    except Exception as e:
        logger.error('Ошибка при старте рекомендаций')
        return -1



async def type_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок в рекомендации"""
    query = update.callback_query
    await query.answer()

    context.user_data['type'] = query.data
    context.user_data["previous_recommendations"] = []

    keyboard = [
        [InlineKeyboardButton("Русское", callback_data="russian")],
        [InlineKeyboardButton("Зарубежное", callback_data="foreign")],
        [InlineKeyboardButton("Не важно", callback_data="any")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Выбери происхождение:", reply_markup=reply_markup)
    logger.info('Ответ от type')
    return ORIGIN


async def origin_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['origin'] = query.data

    await query.edit_message_text("Какой жанр ты хочешь?")
    return GENRE


async def genre_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["genre"] = update.message.text

    await update.message.reply_text("Какое настроение ты хочешь? (Например: веселое, грустное, напряженное)")

    return MOOD


async def mood_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mood"] = update.message.text

    await update.message.reply_text("Какая цель? (Отдохнуть, задуматься, посмеяться)")
    return GOAL

async def goal_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = update.message.text
    await update.message.reply_text("Выбираю, что тебе предложить...")

    user_data = context.user_data

    try:
        recommendation = await get_recommendation_response(
            user_data['type'],
            user_data['origin'],
            user_data['genre'],
            user_data['mood'],
            user_data['goal']
        )

        context.user_data.setdefault("previous_recommendations", [])
        context.user_data["previous_recommendations"].append(recommendation.strip())

        await update.message.reply_text(recommendation)

        logger.info('Ответ по рекомендациям книг и фильмам получен успешно')
        keyboard = [
            [InlineKeyboardButton("Ещё варианты", callback_data="more_recommendation")],
            [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Хочешь еще или вернуться в главное меню?", reply_markup=reply_markup)
        return RECOMMENDING

    except Exception as e:
        logger.error(f"Произошла ошибка при получении рекомендаций: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте еще раз")
        return ConversationHandler.END



async def recommend_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок после создания рекомендаций"""
    logger.info('Зашли в recommend_item')

    query = update.callback_query
    await query.answer()

    u = context.user_data

    keyboard = [
        [InlineKeyboardButton("Ещё варианты", callback_data="more_recommendation")],
        [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
    ]

    reply_markup= InlineKeyboardMarkup(keyboard)

    if query.data == "more_recommendation":
        logger.info('еще рекомендации')
        used = context.user_data.get("previous_recommendations", [])
        recommendation = await get_recommendation_response(
            u["type"],
            u["origin"],
            u["genre"],
            u["mood"],
            u["goal"],
            used
            )
        context.user_data["previous_recommendations"].append(recommendation.strip())

        try:
            await query.message.reply_text(recommendation, reply_markup=reply_markup, parse_mode='HTML')

        except Exception as e:
            await query.message.reply_text(
                text=recommendation,

            )
            await query.delete_message()
        return RECOMMENDING

    elif query.data == "main_menu":
        context.user_data.clear()
        await recc_command(update, context)
        return -1




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Ну ты это, заходи если че!")
    return ConversationHandler.END