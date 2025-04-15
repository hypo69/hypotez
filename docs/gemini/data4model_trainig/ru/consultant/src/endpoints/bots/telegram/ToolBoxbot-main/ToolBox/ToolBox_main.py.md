### **Анализ кода модуля `ToolBox_main.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет функции Telegram-бота для обработки текста и изображений, интеграции с базой данных и управления тарифами.
    - Использование многопоточности для выполнения задач обработки позволяет избежать блокировки основного потока бота.
    - Применение `DATA_PATTERN` для инициализации данных пользователей обеспечивает единообразие структуры данных.
- **Минусы**:
    - Отсутствует подробная документация для функций и классов, что усложняет понимание и поддержку кода.
    - Переменные и функции именованы не всегда информативно.
    - Использование глобальных переменных может привести к проблемам с состоянием и отладкой.
    - Отсутствуют аннотации типов.
    - Местами используется небезопасное форматирование строк (например, `f"Ваш реферальный код: {referal}"`).
    - Не все блоки `try...except` снабжены логированием ошибок, что затрудняет отладку и мониторинг.
    - Не используется менеджер контекста (`with`) при работе с базой данных.
    - Дублирование кода в блоках обработки callback-запросов.
    - Использование `Thread.join()` сразу после запуска потока может нивелировать эффект многопоточности.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавь docstring для каждой функции, метода и класса, описывающий их назначение, аргументы, возвращаемые значения и возможные исключения.
    *   Добавь описание модуля в начале файла.

2.  **Типизация**:
    *   Добавь аннотации типов для всех переменных и аргументов функций. Это улучшит читаемость и позволит статическим анализаторам кода выявлять ошибки.

3.  **Именование**:
    *   Переименуй переменные и функции, чтобы их имена были более информативными и отражали их назначение. Например, `StartProcessing` -> `process_start_command`, `tb` -> `toolbox`.
    *   Избегай сокращений, если они не общеприняты.

4.  **Глобальные переменные**:
    *   По возможности избегай использования глобальных переменных. Рассмотри возможность использования классов или объектов для хранения состояния бота.

5.  **Форматирование строк**:
    *   Используй f-строки или `.format()` для безопасного форматирования строк.

6.  **Обработка исключений и логирование**:
    *   Добавь блоки `try...except` для обработки возможных исключений.
    *   Используй `logger` для логирования ошибок и других важных событий.

7.  **Менеджер контекста**:
    *   Используй менеджер контекста (`with`) при работе с базой данных, чтобы гарантировать закрытие соединения после завершения работы.

8.  **Рефакторинг**:
    *   Вынеси повторяющийся код в отдельные функции.
    *   Используй более структурированный подход к обработке callback-запросов, например, словарь соответствий `callback_data: function`.

9.  **Многопоточность**:
    *   Убери вызовы `thr.join()` сразу после запуска потоков, если не требуется немедленное ожидание их завершения. В противном случае, многопоточность не имеет смысла.

10. **Безопасность**:
    *   Рассмотри возможность использования более надежного способа хранения и обработки промокодов.

**Оптимизированный код:**

```python
"""
Модуль для работы с Telegram-ботом ToolBox
===========================================

Модуль содержит функции для обработки команд и callback-запросов от пользователей,
взаимодействия с базой данных, управления тарифами и генерации контента.
"""

import asyncio, base64, string, random
from telebot import types
from random import randint
from dotenv import load_dotenv
from datetime import datetime
from threading import Thread
from dateutil.relativedelta import relativedelta
from ToolBox_requests import ToolBox
from ToolBox_DataBase import DataBase
from src.logger import logger

# Number of text types
N: int = 8
# User data initialization pattern
DATA_PATTERN = lambda text=[0]*N, sessions_messages=[], some=False, images="", free=False, basic=False, pro=False, incoming_tokens=0, outgoing_tokens=0, free_requests=10, datetime_sub=datetime.now().replace(microsecond=0)+relativedelta(days=1), promocode=False, ref='': \
    {'text':text, "sessions_messages": sessions_messages, "some":some, 'images':images, 'free': free, 'basic': basic, 'pro': pro,
     'incoming_tokens': incoming_tokens, 'outgoing_tokens': outgoing_tokens,
     'free_requests': free_requests, 'datetime_sub': datetime_sub, 'promocode': promocode, 'ref': ref}

# Load environment variables
load_dotenv()
photo_array: list = []

# Objects initialized
toolbox = ToolBox()
bot = toolbox.bot
base = DataBase(db_name="UsersData.db", table_name="users_data_table",
                titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]", "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                        "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                        "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                        "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"}
                )

# Database initialization and connection
base.create()
db = base.load_data_from_db()

# Processing payment request
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery) -> None:
    """
    Обрабатывает предварительный запрос на оплату.

    Args:
        pre_checkout_query (types.PreCheckoutQuery): Объект запроса на оплату.
    """
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Processing success payment
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: types.Message) -> None:
    """
    Обрабатывает успешный платеж.

    Args:
        message (types.Message): Объект сообщения об успешной оплате.
    """
    global db
    user_id = str(message.chat.id)
    # tariffs pay separation
    if message.successful_payment.invoice_payload == 'basic_invoice_payload':
        db[user_id]['basic'] = True
    elif message.successful_payment.invoice_payload == 'pro_invoice_payload':
        db[user_id]['pro'] = True
        db[user_id]['basic'] = True

    # Tokens enrollment
    db[user_id]['incoming_tokens'] = int(1.7e5)
    db[user_id]['outgoing_tokens'] = int(5e5)

    # Datetime tariff subscribe
    db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0) + relativedelta(months=1)
    base.insert_or_update_data(user_id, db[user_id])
    bot.send_message(user_id, "Спасибо за оплату! Ваша подписка активирована.")
    toolbox.restart(message)

# Processing start command
@bot.message_handler(commands=['start'])
def process_start_command(message: types.Message) -> None:
    """
    Обрабатывает команду /start.

    Args:
        message (types.Message): Объект сообщения с командой /start.
    """
    global db
    user_id = str(message.chat.id)
    db[user_id] = DATA_PATTERN() if not db.get(user_id, False) else DATA_PATTERN(basic=db[user_id]['basic'], pro=db[user_id]['pro'], incoming_tokens=db[user_id]['incoming_tokens'],
                                                                                outgoing_tokens=db[user_id]['outgoing_tokens'], free_requests=db[user_id]['free_requests'], datetime_sub=db[user_id]['datetime_sub'],
                                                                                promocode=db[user_id]['promocode'], ref=db[user_id]['ref']
                                                                                )
    base.insert_or_update_data(user_id, db[user_id])
    toolbox.start_request(message)

# Tariff information show
@bot.message_handler(commands=['profile'])
def personal_account(message: types.Message) -> None:
    """
    Отображает информацию о тарифном плане пользователя.

    Args:
        message (types.Message): Объект сообщения с командой /profile.
    """
    global db
    user_id = str(message.chat.id)
    if db[user_id]['basic'] and (not db[user_id]['pro']):
        bot.send_message(chat_id=user_id, text="Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет", parse_mode='html')
    elif db[user_id]['basic'] and db[user_id]['pro']:
        bot.send_message(chat_id=user_id, text="Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит", parse_mode='html')
    else:
        bot.send_message(chat_id=user_id, text=f"У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{db[user_id]['free_requests']}\nГенерация изображений: нет", parse_mode='html')

@bot.message_handler(commands=['stat'])
def show_stat(message: types.Message) -> None:
    """
    Отображает статистику бота (доступно только для определенных пользователей).

    Args:
        message (types.Message): Объект сообщения с командой /stat.
    """
    global db
    user_id = str(message.chat.id)
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
    characters = string.ascii_letters + string.digits
    promo_code = ''.join(random.choices(characters, k=length))
    return promo_code

# Processing callback requests
@bot.callback_query_handler(func=lambda call: True)
def process_callback_query(call: types.CallbackQuery) -> None:
    """
    Обрабатывает callback-запросы от inline-кнопок.

    Args:
        call (types.CallbackQuery): Объект callback-запроса.
    """
    global db
    user_id = str(call.message.chat.id)

    text_buttons = [
        "comm-text", "smm-text", "brainst-text",
        "advertising-text", "headlines-text",
        "seo-text", "news", "editing"
    ]
    # User data create
    if not db.get(user_id):
        db[user_id] = DATA_PATTERN()
        base.insert_or_update_data(user_id, db[user_id])

    # Main tasks buttons
    if call.data in toolbox.data:
        match call.data:
            # Text button
            case "text":
                toolbox.Text_types(call.message)
            # Image button
            case "images":
                if db[user_id]["pro"]:
                    toolbox.ImageSize(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Обновите ваш тариф до PRO")
                    toolbox.restart(call.message)
            # Free mode button
            case "free":
                db[user_id]['free'] = True
                base.insert_or_update_data(user_id, db[user_id])
                bot.delete_message(user_id, message_id=call.message.message_id)
                toolbox.FreeArea(call.message)
            # Tariff button
            case "tariff":
                toolbox.TariffArea(call.message)

    # Image size buttons
    elif call.data in ["576x1024", "1024x1024", "1024x576"]:
        db[user_id]['images'] = call.data
        base.insert_or_update_data(user_id, db[user_id])
        toolbox.ImageArea(call.message)

    elif call.data in ["upscale", "regenerate"]:
        size, prompt, seed = db[user_id]["images"].split('|')
        size = [int(el) for el in size.split('x')]
        match call.data:
            case "upscale":
                bot.delete_message(user_id, call.message.message_id)
                thr=Thread(target=toolbox.Image_Regen_And_Upscale, args=(call.message, prompt, size, int(seed), 30))
                thr.start()
                thr.join()
                toolbox.BeforeUpscale(call.message)
            case "regenerate":
                bot.delete_message(user_id, call.message.message_id)
                seed = randint(1, 1000000)
                thr=Thread(target=toolbox.Image_Regen_And_Upscale, args=(call.message, prompt, size, seed))
                thr.start()
                db[user_id]["images"] = '|'.join(db[user_id]["images"].rsplit('|')[:2])+'|'+str(seed)
                base.insert_or_update_data(user_id, db[user_id])
                thr.join()
                toolbox.ImageChange(call.message)

    # Tariffs buttons
    elif call.data in ["basic", "pro", "promo", "ref"]:
        match call.data:
            # basic
            case "basic":
                if not db[user_id]['basic']:
                    toolbox.Basic_tariff(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф BASIC.")
                    toolbox.restart(call.message)
            # pro
            case "pro":
                if not db[user_id]['pro']:
                    toolbox.Pro_tariff(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO.")
                    toolbox.restart(call.message)
            # promo
            case "promo":
                if (not db[user_id]['pro']) and (not db[user_id]['promocode']):
                    msg = bot.send_message(chat_id=user_id, text="Введите ваш промокод")
                    def get_promo_code(message: types.Message) -> None:
                        """
                        Получает и обрабатывает введенный промокод.

                        Args:
                            message (types.Message): Объект сообщения с промокодом.
                        """
                        if message.text.lower() == "free24" or message.text == [us['ref'] for us in db.values()] and db[user_id]['ref']!=message.text:
                            db[user_id]['pro'] = True
                            db[user_id]['basic'] = True
                            db[user_id]['incoming_tokens'] = int(1.7e5)
                            db[user_id]['outgoing_tokens'] = int(5e5)
                            db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)
                            db[user_id]['promocode'] = True
                            base.insert_or_update_data(user_id, db[user_id])
                            bot.send_message(chat_id=user_id, text="Ваша подписка активирвана. Приятного использования ☺️", parse_mode='html')
                        else:
                            bot.send_message(chat_id=user_id, text="Неверный промокод.")
                        toolbox.restart(message)
                    bot.register_next_step_handler(msg, get_promo_code)
                else:
                    bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO или уже активировали промокод")
                    toolbox.restart(call.message)

            case "ref":
                if db[user_id]['ref'] == '':
                    referal = generate_promo_code(10)
                    db[user_id]['ref'] = referal
                else:
                    referal = db[user_id]['ref']
                bot.send_message(chat_id=user_id, text=f"Ваш реферальный код: {referal}", parse_mode='html')
                toolbox.restart(call.message)
                base.insert_or_update_data(user_id, db[user_id])
    # Texts buttons
    elif call.data in text_buttons:
        avalib = [0, 1, 3, 5, 6]
        index = text_buttons.index(call.data)
        if index in avalib:
            toolbox.SomeTexts(call.message, avalib.index(index))
        else:
            db[user_id]['text'][index] = 1
            base.insert_or_update_data(user_id, db[user_id])
            toolbox.OneTextArea(call.message, index)

    # All exit buttons
    elif call.data in ["exit", "text_exit", "tariff_exit"]:
        match call.data:
            # Cancel to main menu button
            case "exit":
                db[user_id] = DATA_PATTERN(basic=db[user_id]['basic'], pro=db[user_id]['pro'], incoming_tokens=db[user_id]['incoming_tokens'],
                                        outgoing_tokens=db[user_id]['outgoing_tokens'], free_requests=db[user_id]['free_requests'],
                                        datetime_sub=db[user_id]['datetime_sub'], promocode=db[user_id]['promocode'], ref=db[user_id]['ref'])
                base.insert_or_update_data(user_id, db[user_id])
                toolbox.restart_markup(call.message)
            # Cancel from text field input
            case "text_exit":
                db[user_id]['text'] = [0]*N
                db[user_id]['some'] = False
                base.insert_or_update_data(user_id, db[user_id])
                toolbox.Text_types(call.message)
            # Cancel from tariff area selection
            case "tariff_exit":
                bot.delete_message(user_id, call.message.message_id)
                toolbox.TariffExit(call.message)

    # One text area buttons
    elif call.data in [f"one_{ind}" for ind in range(N)]:
        index = [0, 1, 3, 5, 6][int(call.data[-1])]
        db[user_id]['text'][index] = 1
        base.insert_or_update_data(user_id, db[user_id])
        toolbox.OneTextArea(call.message, index)

    # Some texts area buttons
    elif call.data in [f"some_{ind}" for ind in range(N)]:
        index = [0, 1, 3, 5, 6][int(call.data[-1])]
        db[user_id]['text'][index] = 1
        db[user_id]['some'] = True
        base.insert_or_update_data(user_id, db[user_id])
        toolbox.SomeTextsArea(call.message, int(call.data[-1]))

# Text generation pattern
def TokensCancelletionPattern(user_id: str, func, message: types.Message, i: int | None = None) -> None:
    """
    Шаблон для обработки списания токенов или бесплатных запросов.

    Args:
        user_id (str): ID пользователя.
        func: Функция для выполнения.
        message (types.Message): Объект сообщения.
        i (int | None): Индекс (опционально).
    """
    global db
    in_tokens = db[user_id]['incoming_tokens']
    out_tokens = db[user_id]['outgoing_tokens']
    free_requests = db[user_id]['free_requests']

    if in_tokens > 0 and out_tokens > 0 or free_requests > 0:
        if i is None:
            incoming_tokens, outgoing_tokens, db[user_id]['sessions_messages'] = func(message, db[user_id]['sessions_messages']); cnt = 1
        else:
            incoming_tokens, outgoing_tokens, cnt = func(message, i) if func == toolbox.TextCommands else func(message, i, {"incoming_tokens": in_tokens,
                                                                                                                        "outgoing_tokens": out_tokens,
                                                                                                                        "free_requests": free_requests})
        if in_tokens > 0 and out_tokens > 0:
            db[user_id]['incoming_tokens'] -= incoming_tokens
            db[user_id]['outgoing_tokens'] -= outgoing_tokens

        elif free_requests > 0:
            db[user_id]['free_requests'] -= cnt

    elif db[user_id]['free_requests'] == 0:
        toolbox.FreeTariffEnd(message)

    else:
        toolbox.TarrifEnd(message)
        db[user_id]['incoming_tokens'] = 0 if in_tokens <= 0 else in_tokens
        db[user_id]['outgoing_tokens'] = 0 if out_tokens <= 0 else out_tokens
        toolbox.restart(message)

# Tasks messages processing
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def TasksProcessing(message: types.Message) -> None:
    """
    Обрабатывает входящие текстовые и фото-сообщения.

    Args:
        message (types.Message): Объект входящего сообщения.
    """
    global db
    user_id = str(message.chat.id)

    # Images processing
    if db[user_id]['images'] != "" and len(db[user_id]['images'].split('|')) == 1:
        size = [int(el) for el in db[user_id]['images'].split('x')]
        prompt = message.text
        seed = toolbox.ImageCommand(message, prompt, size)
        db[user_id]['images']+='|'+prompt+'|'+str(int(seed))

    # Main menu exit button
    elif db[user_id]['free'] and message.text == 'В меню':
        db[user_id]['sessions_messages'] = []
        db[user_id]['free'] = False
        bot.send_message(chat_id=user_id, text='Сессия завершена', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        toolbox.restart(message)

    # Free mode processing
    elif db[user_id]['free']:
        if message.content_type == 'photo':
            photo = base64.b64encode(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)).decode()
            if message.caption is not None:
                db[user_id]['sessions_messages'].append({"content": [{"type": "text", "text": message.caption}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            else:
                db[user_id]['sessions_messages'].append({"content": [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            thr = Thread(target=TokensCancelletionPattern, args=(user_id, toolbox.FreeCommand, message))
            thr.start()
            thr.join()
        else:
            thr = Thread(target=TokensCancelletionPattern, args=(user_id, toolbox.FreeCommand, message))
            thr.start()
            thr.join()
    # Text processing
    else:
        for i in range(len(db[user_id]['text'])):
            if db[user_id]['text'][i] and not db[user_id]['some']:
                thr=Thread(target=TokensCancelletionPattern, args=(user_id, toolbox.TextCommands, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                thr.join()
            elif db[user_id]['text'][i] and db[user_id]['some']:
                thr=Thread(target=TokensCancelletionPattern, args=(user_id, toolbox.SomeTextsCommand, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                db[user_id]['some'] = False
                thr.join()
    base.insert_or_update_data(user_id, db[user_id])

# Time to end tariff check
async def end_check_tariff_time():
    """
    Асинхронно проверяет время окончания действия тарифа у пользователей.
    """
    while True:
        global db
        for user_id, data in db.items():
            deltaf = data['datetime_sub'] - datetime.now().replace(microsecond=0)
            if int(deltaf.total_seconds()) <= 0 and (data['basic'] or data['pro'] or data['free_requests']<10):
                db[user_id] = DATA_PATTERN(text=data['text'], images=data['images'],
                                        free=data['free'], promocode=data['promocode'], ref=data['ref'])
                base.insert_or_update_data(user_id, db[user_id])
        await asyncio.sleep(10)

# Bot launch
if __name__ == "__main__":
    Thread(target=bot.infinity_polling).start()
    asyncio.run(end_check_tariff_time())