### **Анализ кода модуля `ToolBox_main.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на логические блоки, что облегчает понимание общей структуры.
    - Использование `Thread` для выполнения блокирующих операций (таких как запросы к API) в отдельных потоках, что позволяет избежать блокировки основного потока бота.
- **Минусы**:
    - Отсутствуют docstring для большинства функций.
    - Смешанный стиль именования переменных и функций (например, `StartProcessing` и `personal_account` используют разные стили).
    - Использование глобальных переменных (`db`, `photo_array`, `tb`, `bot`) может привести к проблемам с состоянием и отладкой.
    - Отсутствует обработка исключений.
    - Magic values.
    - Не используются аннотации типов.

**Рекомендации по улучшению:**

1.  **Добавить docstring ко всем функциям и классам**:
    - Описать назначение каждой функции, параметры и возвращаемые значения.
    - Добавить примеры использования.
2.  **Удалить глобальные переменные**:
    - Передавать необходимые объекты (например, `ToolBox`, `DataBase`, `telebot.TeleBot`) как аргументы функциям или использовать dependency injection.
3.  **Обработка исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений, особенно при работе с API и базой данных.
4.  **Улучшить стиль кодирования**:
    - Использовать `snake_case` для именования функций и переменных (например, `start_processing` вместо `StartProcessing`).
    - Привести код в соответствие со стандартами PEP8.
5.  **Улучшить структуру данных**:
    - Использовать более явные типы данных вместо `dict` для хранения информации о пользователях.
    - Рассмотреть возможность использования ORM для работы с базой данных.
6.  **Улучшить читаемость**:
    - Избавиться от излишней вложенности условий.
    - Разбить большие функции на более мелкие и специализированные.
7.  **Логирование**:
    - Использовать `logger` для записи информации о работе бота, ошибок и других важных событий.
8. **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.
9. **Переменные окружения**:
    - Использовать переменные окружения для хранения чувствительной информации, такой как API-ключи и токены.

**Оптимизированный код:**

```python
"""
Модуль для обработки Telegram-бота ToolBox
==========================================

Модуль содержит обработчики команд и callback-запросов,
а также функции для взаимодействия с базой данных пользователей
и обработки различных сценариев использования бота.
"""

import asyncio
import base64
import string
import random
from typing import Optional
from telebot import types, TeleBot
from random import randint
from dotenv import load_dotenv
from datetime import datetime
from threading import Thread
from dateutil.relativedelta import relativedelta

from ToolBox_requests import ToolBox #  модуль для выполнения запросов к внешним API
from ToolBox_DataBase import DataBase #  модуль для работы с базой данных
from src.logger import logger

# Количество типов текста
N: int = 8
# Шаблон инициализации данных пользователя
DATA_PATTERN = lambda text=None, sessions_messages=None, some=False, images="", free=False, basic=False, pro=False, incoming_tokens=0, outgoing_tokens=0, free_requests=10, datetime_sub=datetime.now().replace(microsecond=0)+relativedelta(days=1), promocode=False, ref='': { #  шаблон для инициализации данных пользователя
    'text': text or [0]*N,
    "sessions_messages": sessions_messages or [],
    "some": some,
    'images': images,
    'free': free,
    'basic': basic,
    'pro': pro,
    'incoming_tokens': incoming_tokens,
    'outgoing_tokens': outgoing_tokens,
    'free_requests': free_requests,
    'datetime_sub': datetime_sub,
    'promocode': promocode,
    'ref': ref
}

# Загрузка переменных окружения
load_dotenv()
photo_array: list = []

# Инициализация объектов
tb = ToolBox()
bot: TeleBot = tb.bot
base = DataBase(
    db_name="UsersData.db",
    table_name="users_data_table",
    titles={
        "id": "TEXT PRIMARY KEY",
        "text": "INTEGER[]",
        "sessions_messages": "TEXT[]",
        "some": "BOOLEAN",
        "images": "CHAR",
        "free" : "BOOLEAN",
        "basic" : "BOOLEAN",
        "pro" : "BOOLEAN",
        "incoming_tokens": "INTEGER",
        "outgoing_tokens" : "INTEGER",
        "free_requests" : "INTEGER",
        "datetime_sub": "DATETIME",
        "promocode": "BOOLEAN",
        "ref": "TEXT"
    }
)

# Инициализация и подключение к базе данных
base.create()
db: dict = base.load_data_from_db()

# Обработка запроса перед оплатой
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery) -> None:
    """
    Обрабатывает запрос перед оплатой, подтверждая возможность проведения платежа.

    Args:
        pre_checkout_query (types.PreCheckoutQuery): Объект запроса перед оплатой.
    """
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработка успешной оплаты
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: types.Message) -> None:
    """
    Обрабатывает успешную оплату, обновляя данные пользователя в базе данных.

    Args:
        message (types.Message): Объект сообщения об успешной оплате.
    """
    global db
    user_id: str = str(message.chat.id)

    # Определение оплаченного тарифа
    if message.successful_payment.invoice_payload == 'basic_invoice_payload':
        db[user_id]['basic'] = True
    elif message.successful_payment.invoice_payload == 'pro_invoice_payload':
        db[user_id]['pro'] = True
        db[user_id]['basic'] = True

    # Начисление токенов
    db[user_id]['incoming_tokens'] = 1.7*10**5
    db[user_id]['outgoing_tokens'] = 5*10**5

    # Установка даты окончания подписки
    db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)
    base.insert_or_update_data(user_id, db[user_id])
    bot.send_message(user_id, "Спасибо за оплату! Ваша подписка активирована.")
    tb.restart(message)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_processing(message: types.Message) -> None:
    """
    Обрабатывает команду /start, инициализируя данные пользователя или обновляя их.

    Args:
        message (types.Message): Объект сообщения с командой /start.
    """
    global db
    user_id: str = str(message.chat.id)

    # Инициализация данных пользователя, если их нет в базе данных
    db[user_id] = DATA_PATTERN() if not db.get(user_id, False) else DATA_PATTERN(
        basic=db[user_id]['basic'],
        pro=db[user_id]['pro'],
        incoming_tokens=db[user_id]['incoming_tokens'],
        outgoing_tokens=db[user_id]['outgoing_tokens'],
        free_requests=db[user_id]['free_requests'],
        datetime_sub=db[user_id]['datetime_sub'],
        promocode=db[user_id]['promocode'],
        ref=db[user_id]['ref']
    )
    base.insert_or_update_data(user_id, db[user_id])
    tb.start_request(message)

# Отображение информации о тарифе
@bot.message_handler(commands=['profile'])
def personal_account(message: types.Message) -> None:
    """
    Отображает информацию о текущем тарифе пользователя.

    Args:
        message (types.Message): Объект сообщения с командой /profile.
    """
    global db
    user_id: str = str(message.chat.id)

    if db[user_id]['basic'] and (not db[user_id]['pro']):
        bot.send_message(chat_id=user_id, text="Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет", parse_mode='html')
    elif db[user_id]['basic'] and db[user_id]['pro']:
        bot.send_message(chat_id=user_id, text="Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит", parse_mode='html')
    else:
        bot.send_message(chat_id=user_id, text=f"У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{db[user_id]['free_requests']}\nГенерация изображений: нет", parse_mode='html')

# Отображение статистики
@bot.message_handler(commands=['stat'])
def show_stat(message: types.Message) -> None:
    """
    Отображает статистику по использованию бота (доступно только для администраторов).

    Args:
        message (types.Message): Объект сообщения с командой /stat.
    """
    global db
    user_id: str = str(message.chat.id)

    if user_id in ['2004851715', '206635551']:
        bot.send_message(chat_id=user_id, text=f"Всего пользователей: {len(db)}\nС промокодом: {len([1 for el in db.values() if el['promocode']])}")

def generate_promo_code(length: int) -> str:
    """
    Генерирует случайный промокод заданной длины.

    Args:
        length (int): Длина промокода.

    Returns:
        str: Сгенерированный промокод.
    """
    characters: str = string.ascii_letters + string.digits
    promo_code: str = ''.join(random.choices(characters, k=length))
    return promo_code

# Обработка callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def calls_processing(call: types.CallbackQuery) -> None:
    """
    Обрабатывает callback-запросы от кнопок в боте.

    Args:
        call (types.CallbackQuery): Объект callback-запроса.
    """
    global db
    user_id: str = str(call.message.chat.id)

    text_buttons: list = [
        "comm-text", "smm-text", "brainst-text",
        "advertising-text", "headlines-text",
        "seo-text", "news", "editing"
    ]
    # Создание данных пользователя
    if not db.get(user_id):
        db[user_id] = DATA_PATTERN()
        base.insert_or_update_data(user_id, db[user_id])

    # Обработка основных кнопок
    if call.data in tb.data:
        match call.data:
            # Кнопка "Текст"
            case "text":
                tb.Text_types(call.message)
            # Кнопка "Изображения"
            case "images":
                if db[user_id]["pro"]:
                    tb.ImageSize(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Обновите ваш тариф до PRO")
                    tb.restart(call.message)
            # Кнопка "Бесплатный режим"
            case "free":
                db[user_id]['free'] = True
                base.insert_or_update_data(user_id, db[user_id])
                bot.delete_message(user_id, message_id=call.message.message_id)
                tb.FreeArea(call.message)
            # Кнопка "Тариф"
            case "tariff":
                tb.TariffArea(call.message)

    # Обработка кнопок выбора размера изображения
    elif call.data in ["576x1024", "1024x1024", "1024x576"]:
        db[user_id]['images'] = call.data
        base.insert_or_update_data(user_id, db[user_id])
        tb.ImageArea(call.message)

    elif call.data in ["upscale", "regenerate"]:
        size, prompt, seed = db[user_id]["images"].split('|')
        size = [int(el) for el in size.split('x')]
        match call.data:
            case "upscale":
                bot.delete_message(user_id, call.message.message_id)
                thr=Thread(target=tb.Image_Regen_And_Upscale, args=(call.message, prompt, size, int(seed), 30))
                thr.start(); thr.join()
                tb.BeforeUpscale(call.message)
            case "regenerate":
                bot.delete_message(user_id, call.message.message_id)
                seed = randint(1, 1000000)
                thr=Thread(target=tb.Image_Regen_And_Upscale, args=(call.message, prompt, size, seed))
                thr.start()
                db[user_id]["images"] = '|'.join(db[user_id]["images"].rsplit('|')[:2])+'|'+str(seed)
                base.insert_or_update_data(user_id, db[user_id])
                thr.join()
                tb.ImageChange(call.message)

    # Обработка кнопок выбора тарифа
    elif call.data in ["basic", "pro", "promo", "ref"]:
        match call.data:
            # basic
            case "basic":
                if not db[user_id]['basic']:
                    tb.Basic_tariff(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф BASIC.")
                    tb.restart(call.message)
            # pro
            case "pro":
                if not db[user_id]['pro']:
                    tb.Pro_tariff(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO.")
                    tb.restart(call.message)
            # promo
            case "promo":
                if (not db[user_id]['pro']) and (not db[user_id]['promocode']):
                    msg = bot.send_message(chat_id=user_id, text="Введите ваш промокод")
                    def get_promo_code(message: types.Message) -> None:
                        """
                        Обрабатывает введенный промокод.

                        Args:
                            message (types.Message): Объект сообщения с введенным промокодом.
                        """
                        if message.text.lower() == "free24" or message.text == [us['ref'] for us in db.values()] and db[user_id]['ref']!=message.text:
                            db[user_id]['pro'] = True
                            db[user_id]['basic'] = True
                            db[user_id]['incoming_tokens'] = 1.7*10**5
                            db[user_id]['outgoing_tokens'] = 5*10**5
                            db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)
                            db[user_id]['promocode'] = True
                            base.insert_or_update_data(user_id, db[user_id])
                            bot.send_message(chat_id=user_id, text="Ваша подписка активирвана. Приятного использования ☺️", parse_mode='html')
                        else:
                            bot.send_message(chat_id=user_id, text="Неверный промокод.")
                        tb.restart(message)
                    bot.register_next_step_handler(msg, get_promo_code)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO или уже активировали промокод")
                    tb.restart(call.message)

            case "ref":
                if db[user_id]['ref'] == '':
                    referal: str = generate_promo_code(10)
                    db[user_id]['ref'] = referal
                else:
                    referal: str = db[user_id]['ref']
                bot.send_message(chat_id=user_id, text=f"Ваш реферальный код: {referal}", parse_mode='html')
                tb.restart(call.message)
                base.insert_or_update_data(user_id, db[user_id])
    # Обработка кнопок выбора текста
    elif call.data in text_buttons:
        avalib: list = [0, 1, 3, 5, 6]
        index: int = text_buttons.index(call.data)
        if index in avalib:
            tb.SomeTexts(call.message, avalib.index(index))
        else:
            db[user_id]['text'][index] = 1
            base.insert_or_update_data(user_id, db[user_id])
            tb.OneTextArea(call.message, index)

    # Обработка кнопок выхода
    elif call.data in ["exit", "text_exit", "tariff_exit"]:
        match call.data:
            # Кнопка "Выход в главное меню"
            case "exit":
                db[user_id] = DATA_PATTERN(
                    basic=db[user_id]['basic'],
                    pro=db[user_id]['pro'],
                    incoming_tokens=db[user_id]['incoming_tokens'],
                    outgoing_tokens=db[user_id]['outgoing_tokens'],
                    free_requests=db[user_id]['free_requests'],
                    datetime_sub=db[user_id]['datetime_sub'],
                    promocode=db[user_id]['promocode'],
                    ref=db[user_id]['ref']
                )
                base.insert_or_update_data(user_id, db[user_id])
                tb.restart_markup(call.message)
            # Кнопка "Выход из текстового поля"
            case "text_exit":
                db[user_id]['text'] = [0]*N
                db[user_id]['some'] = False
                base.insert_or_update_data(user_id, db[user_id])
                tb.Text_types(call.message)
            # Кнопка "Выход из области тарифов"
            case "tariff_exit":
                bot.delete_message(user_id, call.message.message_id)
                tb.TariffExit(call.message)

    # Обработка кнопок выбора одной текстовой области
    elif call.data in [f"one_{ind}" for ind in range(N)]:
        index: int = [0, 1, 3, 5, 6][int(call.data[-1])]
        db[user_id]['text'][index] = 1
        base.insert_or_update_data(user_id, db[user_id])
        tb.OneTextArea(call.message, index)

    # Обработка кнопок выбора нескольких текстовых областей
    elif call.data in [f"some_{ind}" for ind in range(N)]:
        index: int = [0, 1, 3, 5, 6][int(call.data[-1])]
        db[user_id]['text'][index] = 1
        db[user_id]['some'] = True
        base.insert_or_update_data(user_id, db[user_id])
        tb.SomeTextsArea(call.message, int(call.data[-1]))

# Шаблон отмены токенов
def tokens_cancelletion_pattern(user_id: str, func, message: types.Message, i: Optional[int] = None) -> None:
    """
    Шаблон для обработки списания токенов или запросов в зависимости от типа подписки пользователя.

    Args:
        user_id (str): Идентификатор пользователя.
        func: Функция для выполнения (например, генерация текста или изображения).
        message (types.Message): Объект сообщения пользователя.
        i (Optional[int]): Индекс для передачи в функцию, если необходимо.
    """
    global db
    in_tokens: int = db[user_id]['incoming_tokens']
    out_tokens: int = db[user_id]['outgoing_tokens']
    free_requests: int = db[user_id]['free_requests']

    if in_tokens > 0 and out_tokens > 0 or free_requests > 0:
        if i is None:
            incoming_tokens, outgoing_tokens, db[user_id]['sessions_messages'] = func(message, db[user_id]['sessions_messages'])
            cnt: int = 1
        else:
            incoming_tokens, outgoing_tokens, cnt = func(message, i) if func == tb.TextCommands else func(message, i, {"incoming_tokens": in_tokens,
                                                                                                                        "outgoing_tokens": out_tokens,
                                                                                                                        "free_requests": free_requests})
        if in_tokens > 0 and out_tokens > 0:
            db[user_id]['incoming_tokens'] -= incoming_tokens
            db[user_id]['outgoing_tokens'] -= outgoing_tokens

        elif free_requests > 0:
            db[user_id]['free_requests'] -= cnt

    elif db[user_id]['free_requests'] == 0:
        tb.FreeTariffEnd(message)

    else:
        tb.TarrifEnd(message)
        db[user_id]['incoming_tokens'] = 0 if in_tokens <= 0 else in_tokens
        db[user_id]['outgoing_tokens'] = 0 if out_tokens <= 0 else out_tokens
        tb.restart(message)

# Обработка задач
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def tasks_processing(message: types.Message) -> None:
    """
    Обрабатывает задачи, отправленные пользователем (текст или изображения).

    Args:
        message (types.Message): Объект сообщения пользователя.
    """
    global db
    user_id: str = str(message.chat.id)

    # Обработка изображений
    if db[user_id]['images'] != "" and len(db[user_id]['images'].split('|')) == 1:
        size: list = [int(el) for el in db[user_id]['images'].split('x')]
        prompt: str = message.text
        seed: float = tb.ImageCommand(message, prompt, size)
        db[user_id]['images']+='|'+prompt+'|'+str(int(seed))

    # Обработка выхода в главное меню из бесплатного режима
    elif db[user_id]['free'] and message.text == 'В меню':
        db[user_id]['sessions_messages'] = []
        db[user_id]['free'] = False
        bot.send_message(chat_id=user_id, text='Сессия завершена', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        tb.restart(message)

    # Обработка бесплатного режима
    elif db[user_id]['free']:
        if message.content_type == 'photo':
            photo: str = base64.b64encode(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)).decode()
            if message.caption is not None:
                db[user_id]['sessions_messages'].append({"content": [{"type": "text", "text": message.caption}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            else:
                db[user_id]['sessions_messages'].append({"content": [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            thr: Thread = Thread(target=tokens_cancelletion_pattern, args=(user_id, tb.FreeCommand, message))
            thr.start(); thr.join()
        else:
            thr: Thread = Thread(target=tokens_cancelletion_pattern, args=(user_id, tb.FreeCommand, message))
            thr.start(); thr.join()
    # Обработка текста
    else:
        for i in range(len(db[user_id]['text'])):
            if db[user_id]['text'][i] and not db[user_id]['some']:
                thr: Thread = Thread(target=tokens_cancelletion_pattern, args=(user_id, tb.TextCommands, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                thr.join()
            elif db[user_id]['text'][i] and db[user_id]['some']:
                thr: Thread = Thread(target=tokens_cancelletion_pattern, args=(user_id, tb.SomeTextsCommand, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                db[user_id]['some'] = False
                thr.join()
    base.insert_or_update_data(user_id, db[user_id])

# Проверка времени окончания тарифа
async def end_check_tariff_time() -> None:
    """
    Асинхронная функция для проверки времени окончания тарифа у пользователей и обновления их статуса.
    """
    while True:
        global db
        for user_id, data in db.items():
            deltaf: relativedelta = data['datetime_sub'] - datetime.now().replace(microsecond=0)
            if int(deltaf.total_seconds()) <= 0 and (data['basic'] or data['pro'] or data['free_requests']<10):
                db[user_id] = DATA_PATTERN(text=data['text'], images=data['images'],
                                        free=data['free'], promocode=data['promocode'], ref=data['ref'])
                base.insert_or_update_data(user_id, db[user_id])
        await asyncio.sleep(10)

# Запуск бота
if __name__ == "__main__":
    Thread(target=bot.infinity_polling).start()
    asyncio.run(end_check_tariff_time())