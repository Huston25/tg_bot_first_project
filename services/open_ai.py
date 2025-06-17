import logging

from openai import AsyncOpenAI
from config import CHAT_GPT_TOKEN

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)


async def get_random_fact():
    """Получить случайный факт от ChatGPT"""
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты помощник, который рассказывает интересные и познавательные факты. Отвечай на русском языке. Можешь добавить шуток"
                },
                {
                    "role": "user",
                    "content": "Расскажи интересный случайный факт из любой области знаний. Факт должен быть познавательным, удивительным и не слишком длинным (максимум 3-4 предложения)."
                }
            ],
            max_tokens=200,
            temperature=0.8
        )

        fact = response.choices[0].message.content.strip()
        logger.info("Факт успешно получен от OpenAI")
        return fact

    except Exception as e:
        logger.error(f"Ошибка при получении факта от OpenAI: {e}")
        return "🤔 К сожалению, не удалось получить факт в данный момент. Попробуйте позже!"


async def get_chatgpt_response(user_message: str):
    """Получить ответ от ChatGPT на произвольное сообщение пользователя"""
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты полезный помощник. Отвечай на русском языке, будь дружелюбным и информативным. Если не знаешь ответ, честно об этом скажи."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()
        logger.info("Ответ успешно получен от OpenAI")
        return answer

    except Exception as e:
        logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
        return "😔 Извините, произошла ошибка при обращении к ChatGPT. Попробуйте позже!"


async def get_personality_response(user_message, personality_prompt):
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": personality_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1000,
            temperature=1
        )

        answer = response.choices[0].message.content.strip()
        logger.info("Ответ от личности успешно получен от OpenAI")
        return answer

    except Exception as e:
        logger.error(f"Ошибка при получении ответа от личности: {e}")
        return "😔 Извините, произошла ошибка при обращении к личности. Попробуйте позже!"


async def get_recommendation_response(
        type_chosen: str,
        origin: str,
        genre: str,
        mood: str,
        goal: str
, used=None) -> str:
    used = used or []
    used_text = "\n".join(f" - {item}" for item in used) if used else "Нет"
    origin_map = {
        "russian": "Русское",
        "foreign": "Зарубежное",
        "any": "Не важно"
    }
    origin_text = origin_map.get(origin)
    prompt = (f"""Ты выступаешь как интеллектуальный ассистент. Твоя задача помочь выбрать {type_chosen} 
        ({origin_text})
            на русском языке Не предлагай повторно {used_text}.
            Учитывай:
                - Жанр: {genre}
                - Настроение: {mood}
                - Цель: {goal}
            Формат:
            Название:
            Автор/Режиссер:
            Описание:
            Почему рекомендовано:\n\n
            Список рекомендаций: \n{used_text}""")

    try:
        response = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'system',
                    'content': 'Ты умный помощник, который советует книги, фильмы и сериалы'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f'Произошла ошибка при получении рекомендаций по фильмам и книгам: {e}')
        return 'Произошла ошибка в рекомендациях. Попробуйте повторить'
