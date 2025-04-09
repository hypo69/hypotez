### **Анализ кода модуля `ToolBox_main.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_main.py`

**Описание:** Этот модуль содержит основной код для Telegram-бота ToolBox, включая обработку команд, колбэков, платежей и взаимодействие с базой данных.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код достаточно структурирован и логически разделен на обработку различных типов запросов и команд.
    - Использование `Thread` для выполнения задач в фоне позволяет избежать блокировки основного потока бота.
- **Минусы**:
    - Отсутствует полная документация функций и классов.
    - Присутствуют глобальные переменные (`db`, `photo_array`, `tb`, `bot`), что может привести к проблемам с состоянием и отладкой.
    - Использование `DATA_PATTERN` как lambda-функции может ухудшить читаемость кода.
    - Не все переменные аннотированы типами.
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    - Добавить docstring к каждой функции, описывая её назначение, аргументы, возвращаемые значения и возможные исключения.
    - Описать назначение каждой глобальной переменной.
2.  **Удаление глобальных переменных**:
    - По возможности избавиться от глобальных переменных, передавая необходимые данные между функциями.
    - Инкапсулировать переменные `tb` и `bot` в класс.
3.  **Использовать `logger` для логгирования**:
    - Добавить логирование для отслеживания ошибок и хода выполнения программы.
    - Заменить `print` на `logger.info` или `logger.error` в зависимости от ситуации.
4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.
5.  **Переименование переменных и функций**:
    - Привести имена переменных и функций к общему стилю (например, snake_case).
6.  **Обработка исключений**:
    - Добавить обработку исключений в ключевых местах, чтобы предотвратить падение бота.
7.  **Улучшение структуры данных**:
    - Рассмотреть возможность использования dataclass вместо lambda-функции `DATA_PATTERN` для улучшения читаемости и поддержки типов.
8. **Комментарии**:
    - Добавить комментарии в коде, чтобы объяснить сложные моменты и логику работы.

**Оптимизированный код:**

```python
"""
Модуль для управления Telegram ботом ToolBox
==============================================

Этот модуль содержит основной код для Telegram-бота ToolBox, включая обработку команд, колбэков, платежей и взаимодействие с базой данных.
"""

import asyncio
import base64
import string
import random
from telebot import types
from random import randint
from dotenv import load_dotenv
from datetime import datetime
from threading import Thread
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional
from src.logger import logger  # Import logger
from ToolBox_requests import ToolBox
from ToolBox_DataBase import DataBase

# Number of text types
N: int = 8

# User data initialization pattern
class UserData:
    def __init__(self, text: Optional[List[int]] = None, sessions_messages: Optional[List[dict]] = None, some: bool = False, images: str = "", free: bool = False, basic: bool = False, pro: bool = False, incoming_tokens: int = 0, outgoing_tokens: int = 0, free_requests: int = 10, datetime_sub: datetime = datetime.now().replace(microsecond=0) + relativedelta(days=1), promocode: bool = False, ref: str = ''):
        self.text = text if text is not None else [0] * N
        self.sessions_messages = sessions_messages if sessions_messages is not None else []
        self.some = some
        self.images = images
        self.free = free
        self.basic = basic
        self.pro = pro
        self.incoming_tokens = incoming_tokens
        self.outgoing_tokens = outgoing_tokens
        self.free_requests = free_requests
        self.datetime_sub = datetime_sub
        self.promocode = promocode
        self.ref = ref

# Load environment variables
load_dotenv()

# Objects initialization
class TelegramBot:
    """
    Класс для управления Telegram ботом ToolBox.

    Args:
        db_name (str): Имя файла базы данных.
        table_name (str): Имя таблицы в базе данных.

    """
    def __init__(self, db_name: str = "UsersData.db", table_name: str = "users_data_table"):
        """
        Инициализация экземпляра класса TelegramBot.

        Args:
            db_name (str, optional): Имя файла базы данных. Defaults to "UsersData.db".
            table_name (str, optional): Имя таблицы в базе данных. Defaults to "users_data_table".
        """
        self.photo_array: List[str] = []
        self.tb = ToolBox()
        self.bot = self.tb.bot
        self.base = DataBase(db_name=db_name, table_name=table_name,
                            titles={"id": "TEXT PRIMARY KEY", "text": "INTEGER[]", "sessions_messages": "TEXT[]", "some": "BOOLEAN",
                                    "images": "CHAR", "free" : "BOOLEAN", "basic" : "BOOLEAN",
                                    "pro" : "BOOLEAN", "incoming_tokens": "INTEGER", "outgoing_tokens" : "INTEGER",
                                    "free_requests" : "INTEGER", "datetime_sub": "DATETIME", "promocode": "BOOLEAN", "ref": "TEXT"}
                            )
        self.base.create()
        self.db: Dict[str, UserData] = self.load_data()

    def load_data(self) -> Dict[str, UserData]:
        """
        Загружает данные из базы данных и преобразует их в словарь объектов UserData.

        Returns:
            Dict[str, UserData]: Словарь, где ключи - user_id, а значения - объекты UserData.
        """
        db_data = self.base.load_data_from_db()
        db: Dict[str, UserData] = {}
        for user_id, data in db_data.items():
            db[user_id] = UserData(
                text=data['text'],
                sessions_messages=data['sessions_messages'],
                some=data['some'],
                images=data['images'],
                free=data['free'],
                basic=data['basic'],
                pro=data['pro'],
                incoming_tokens=data['incoming_tokens'],
                outgoing_tokens=data['outgoing_tokens'],
                free_requests=data['free_requests'],
                datetime_sub=data['datetime_sub'],
                promocode=data['promocode'],
                ref=data['ref']
            )
        return db

    def insert_or_update_data(self, user_id: str, user_data: UserData) -> None:
        """
        Вставляет или обновляет данные пользователя в базе данных.

        Args:
            user_id (str): Идентификатор пользователя.
            user_data (UserData): Объект UserData с данными пользователя.
        """
        data = {
            'text': user_data.text,
            'sessions_messages': user_data.sessions_messages,
            'some': user_data.some,
            'images': user_data.images,
            'free': user_data.free,
            'basic': user_data.basic,
            'pro': user_data.pro,
            'incoming_tokens': user_data.incoming_tokens,
            'outgoing_tokens': user_data.outgoing_tokens,
            'free_requests': user_data.free_requests,
            'datetime_sub': user_data.datetime_sub,
            'promocode': user_data.promocode,
            'ref': user_data.ref
        }
        self.base.insert_or_update_data(user_id, data)
        self.db[user_id] = user_data

    def process_pre_checkout_query(self, pre_checkout_query: types.PreCheckoutQuery) -> None:
        """
        Обрабатывает предварительный запрос перед оплатой.

        Args:
            pre_checkout_query (types.PreCheckoutQuery): Объект запроса.
        """
        self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    def successful_payment(self, message: types.Message) -> None:
        """
        Обрабатывает успешный платеж.

        Args:
            message (types.Message): Объект сообщения.
        """
        user_id = str(message.chat.id)

        # tariffs pay separation
        if message.successful_payment.invoice_payload == 'basic_invoice_payload':
            self.db[user_id].basic = True
        elif message.successful_payment.invoice_payload == 'pro_invoice_payload':
            self.db[user_id].pro = True
            self.db[user_id].basic = True

        # Tokens enrollment
        self.db[user_id].incoming_tokens = int(1.7 * 10**5)
        self.db[user_id].outgoing_tokens = int(5 * 10**5)

        # Datetime tariff subscribe
        self.db[user_id].datetime_sub = datetime.now().replace(microsecond=0) + relativedelta(months=1)
        self.insert_or_update_data(user_id, self.db[user_id])
        self.bot.send_message(user_id, "Спасибо за оплату! Ваша подписка активирована.")
        self.tb.restart(message)

    def start_processing(self, message: types.Message) -> None:
        """
        Обрабатывает команду /start.

        Args:
            message (types.Message): Объект сообщения.
        """
        user_id = str(message.chat.id)
        if user_id not in self.db:
            self.db[user_id] = UserData()
        else:
            self.db[user_id] = UserData(
                basic=self.db[user_id].basic,
                pro=self.db[user_id].pro,
                incoming_tokens=self.db[user_id].incoming_tokens,
                outgoing_tokens=self.db[user_id].outgoing_tokens,
                free_requests=self.db[user_id].free_requests,
                datetime_sub=self.db[user_id].datetime_sub,
                promocode=self.db[user_id].promocode,
                ref=self.db[user_id].ref
            )
        self.insert_or_update_data(user_id, self.db[user_id])
        self.tb.start_request(message)

    def personal_account(self, message: types.Message) -> None:
        """
        Отображает информацию о тарифном плане пользователя.

        Args:
            message (types.Message): Объект сообщения.
        """
        user_id = str(message.chat.id)
        if self.db[user_id].basic and (not self.db[user_id].pro):
            self.bot.send_message(chat_id=user_id, text="Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет", parse_mode='html')
        elif self.db[user_id].basic and self.db[user_id].pro:
            self.bot.send_message(chat_id=user_id, text="Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит", parse_mode='html')
        else:
            self.bot.send_message(chat_id=user_id, text=f"У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{self.db[user_id].free_requests}\nГенерация изображений: нет", parse_mode='html')

    def show_stat(self, message: types.Message) -> None:
        """
        Отображает статистику по пользователям (доступно только для определенных user_id).

        Args:
            message (types.Message): Объект сообщения.
        """
        user_id = str(message.chat.id)
        if user_id in ['2004851715', '206635551']:
            promocodes_count = sum(1 for el in self.db.values() if el.promocode)
            self.bot.send_message(chat_id=user_id, text=f"Всего пользователей: {len(self.db)}\nС промокодом: {promocodes_count}")

    def generate_promo_code(self, length: int) -> str:
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

    def calls_processing(self, call: types.CallbackQuery) -> None:
        """
        Обрабатывает callback запросы от кнопок.

        Args:
            call (types.CallbackQuery): Объект callback запроса.
        """
        user_id = str(call.message.chat.id)
        text_buttons = [
            "comm-text", "smm-text", "brainst-text",
            "advertising-text", "headlines-text",
            "seo-text", "news", "editing"
        ]

        # User data create
        if user_id not in self.db:
            self.db[user_id] = UserData()
            self.insert_or_update_data(user_id, self.db[user_id])

        # Main tasks buttons
        if call.data in self.tb.data:
            match call.data:
                # Text button
                case "text":
                    self.tb.Text_types(call.message)
                # Image button
                case "images":
                    if self.db[user_id].pro:
                        self.tb.ImageSize(call.message)
                    else:
                        self.bot.send_message(chat_id=user_id, text="Обновите ваш тариф до PRO")
                        self.tb.restart(call.message)
                # Free mode button
                case "free":
                    self.db[user_id].free = True
                    self.insert_or_update_data(user_id, self.db[user_id])
                    self.bot.delete_message(user_id, message_id=call.message.message_id)
                    self.tb.FreeArea(call.message)
                # Tariff button
                case "tariff":
                    self.tb.TariffArea(call.message)

        # Image size buttons
        elif call.data in ["576x1024", "1024x1024", "1024x576"]:
            self.db[user_id].images = call.data
            self.insert_or_update_data(user_id, self.db[user_id])
            self.tb.ImageArea(call.message)

        elif call.data in ["upscale", "regenerate"]:
            size, prompt, seed = self.db[user_id].images.split('|')
            size = [int(el) for el in size.split('x')]
            match call.data:
                case "upscale":
                    self.bot.delete_message(user_id, call.message.message_id)
                    thr = Thread(target=self.tb.Image_Regen_And_Upscale, args=(call.message, prompt, size, int(seed), 30))
                    thr.start()
                    thr.join()
                    self.tb.BeforeUpscale(call.message)
                case "regenerate":
                    self.bot.delete_message(user_id, call.message.message_id)
                    seed = randint(1, 1000000)
                    thr = Thread(target=self.tb.Image_Regen_And_Upscale, args=(call.message, prompt, size, seed))
                    thr.start()
                    self.db[user_id].images = '|'.join(self.db[user_id].images.rsplit('|')[:2]) + '|' + str(seed)
                    self.insert_or_update_data(user_id, self.db[user_id])
                    thr.join()
                    self.tb.ImageChange(call.message)

        # Tariffs buttons
        elif call.data in ["basic", "pro", "promo", "ref"]:
            match call.data:
                # basic
                case "basic":
                    if not self.db[user_id].basic:
                        self.tb.Basic_tariff(call.message)
                    else:
                        self.bot.send_message(chat_id=user_id, text="Вы уже подключили тариф BASIC.")
                        self.tb.restart(call.message)
                # pro
                case "pro":
                    if not self.db[user_id].pro:
                        self.tb.Pro_tariff(call.message)
                    else:
                        self.bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO.")
                        self.tb.restart(call.message)
                # promo
                case "promo":
                    if (not self.db[user_id].pro) and (not self.db[user_id].promocode):
                        msg = self.bot.send_message(chat_id=user_id, text="Введите ваш промокод")

                        def get_promo_code(message: types.Message) -> None:
                            """
                            Обрабатывает введенный промокод.

                            Args:
                                message (types.Message): Объект сообщения с промокодом.
                            """
                            if message.text.lower() == "free24" or message.text in [us.ref for us in self.db.values()] and self.db[user_id].ref != message.text:
                                self.db[user_id].pro = True
                                self.db[user_id].basic = True
                                self.db[user_id].incoming_tokens = int(1.7 * 10**5)
                                self.db[user_id].outgoing_tokens = int(5 * 10**5)
                                self.db[user_id].datetime_sub = datetime.now().replace(microsecond=0) + relativedelta(months=1)
                                self.db[user_id].promocode = True
                                self.insert_or_update_data(user_id, self.db[user_id])
                                self.bot.send_message(chat_id=user_id, text="Ваша подписка активирвана. Приятного использования ☺️", parse_mode='html')
                            else:
                                self.bot.send_message(chat_id=user_id, text="Неверный промокод.")
                            self.tb.restart(message)

                        self.bot.register_next_step_handler(msg, get_promo_code)
                    else:
                        self.bot.send_message(chat_id=user_id, text="Вы уже подключили тариф PRO или уже активировали промокод")
                        self.tb.restart(call.message)

                case "ref":
                    if self.db[user_id].ref == '':
                        referal = self.generate_promo_code(10)
                        self.db[user_id].ref = referal
                    else:
                        referal = self.db[user_id].ref
                    self.bot.send_message(chat_id=user_id, text=f"Ваш реферальный код: {referal}", parse_mode='html')
                    self.tb.restart(call.message)
                    self.insert_or_update_data(user_id, self.db[user_id])
        # Texts buttons
        elif call.data in text_buttons:
            avalib = [0, 1, 3, 5, 6]
            index = text_buttons.index(call.data)
            if index in avalib:
                self.tb.SomeTexts(call.message, avalib.index(index))
            else:
                self.db[user_id].text[index] = 1
                self.insert_or_update_data(user_id, self.db[user_id])
                self.tb.OneTextArea(call.message, index)

        # All exit buttons
        elif call.data in ["exit", "text_exit", "tariff_exit"]:
            match call.data:
                # Cancel to main menu button
                case "exit":
                    self.db[user_id] = UserData(
                        basic=self.db[user_id].basic,
                        pro=self.db[user_id].pro,
                        incoming_tokens=self.db[user_id].incoming_tokens,
                        outgoing_tokens=self.db[user_id].outgoing_tokens,
                        free_requests=self.db[user_id].free_requests,
                        datetime_sub=self.db[user_id].datetime_sub,
                        promocode=self.db[user_id].promocode,
                        ref=self.db[user_id].ref
                    )
                    self.insert_or_update_data(user_id, self.db[user_id])
                    self.tb.restart_markup(call.message)
                # Cancel from text field input
                case "text_exit":
                    self.db[user_id].text = [0] * N
                    self.db[user_id].some = False
                    self.insert_or_update_data(user_id, self.db[user_id])
                    self.tb.Text_types(call.message)
                # Cancel from tariff area selection
                case "tariff_exit":
                    self.bot.delete_message(user_id, call.message.message_id)
                    self.tb.TariffExit(call.message)

        # One text area buttons
        elif call.data in [f"one_{ind}" for ind in range(N)]:
            index = [0, 1, 3, 5, 6][int(call.data[-1])]
            self.db[user_id].text[index] = 1
            self.insert_or_update_data(user_id, self.db[user_id])
            self.tb.OneTextArea(call.message, index)

        # Some texts area buttons
        elif call.data in [f"some_{ind}" for ind in range(N)]:
            index = [0, 1, 3, 5, 6][int(call.data[-1])]
            self.db[user_id].text[index] = 1
            self.db[user_id].some = True
            self.insert_or_update_data(user_id, self.db[user_id])
            self.tb.SomeTextsArea(call.message, int(call.data[-1]))

    def tokens_cancelletion_pattern(self, user_id: str, func, message: types.Message, i: Optional[int] = None) -> None:
        """
        Управляет использованием токенов или бесплатных запросов для генерации текста.

        Args:
            user_id (str): Идентификатор пользователя.
            func: Функция для выполнения (генерация текста).
            message (types.Message): Объект сообщения.
            i (Optional[int]): Индекс для конкретных текстовых команд.
        """
        in_tokens = self.db[user_id].incoming_tokens
        out_tokens = self.db[user_id].outgoing_tokens
        free_requests = self.db[user_id].free_requests

        if in_tokens > 0 and out_tokens > 0 or free_requests > 0:
            if i is None:
                incoming_tokens, outgoing_tokens, self.db[user_id].sessions_messages = func(message, self.db[user_id].sessions_messages)
                cnt = 1
            else:
                params = {"incoming_tokens": in_tokens, "outgoing_tokens": out_tokens, "free_requests": free_requests}
                incoming_tokens, outgoing_tokens, cnt = func(message, i, params) if func == self.tb.TextCommands else func(message, i, params)

            if in_tokens > 0 and out_tokens > 0:
                self.db[user_id].incoming_tokens -= incoming_tokens
                self.db[user_id].outgoing_tokens -= outgoing_tokens

            elif free_requests > 0:
                self.db[user_id].free_requests -= cnt

        elif self.db[user_id].free_requests == 0:
            self.tb.FreeTariffEnd(message)

        else:
            self.tb.TarrifEnd(message)
            self.db[user_id].incoming_tokens = 0 if in_tokens <= 0 else in_tokens
            self.db[user_id].outgoing_tokens = 0 if out_tokens <= 0 else out_tokens
            self.tb.restart(message)
        self.insert_or_update_data(user_id, self.db[user_id])

    def tasks_processing(self, message: types.Message) -> None:
        """
        Обрабатывает сообщения, включая изображения и текст.

        Args:
            message (types.Message): Объект сообщения.
        """
        user_id = str(message.chat.id)

        # Images processing
        if self.db[user_id].images != "" and len(self.db[user_id].images.split('|')) == 1:
            size = [int(el) for el in self.db[user_id].images.split('x')]
            prompt = message.text
            seed = self.tb.ImageCommand(message, prompt, size)
            self.db[user_id].images += "|" + prompt + "|" + str(int(seed))

        # Main menu exit button
        elif self.db[user_id].free and message.text == 'В меню':
            self.db[user_id].sessions_messages = []
            self.db[user_id].free = False
            self.bot.send_message(chat_id=user_id, text='Сессия завершена', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            self.tb.restart(message)

        # Free mode processing
        elif self.db[user_id].free:
            if message.content_type == 'photo':
                photo = base64.b64encode(self.bot.download_file(self.bot.get_file(message.photo[-1].file_id).file_path)).decode()
                content = [{"type": "text", "text": message.caption}] if message.caption else []
                content.append({"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"})
                self.db[user_id].sessions_messages.append({"content": content, "role": "user"})
                thr = Thread(target=self.tokens_cancelletion_pattern, args=(user_id, self.tb.FreeCommand, message))
                thr.start()
                thr.join()
            else:
                thr = Thread(target=self.tokens_cancelletion_pattern, args=(user_id, self.tb.FreeCommand, message))
                thr.start()
                thr.join()
        # Text processing
        else:
            for i in range(len(self.db[user_id].text)):
                if self.db[user_id].text[i] and not self.db[user_id].some:
                    thr = Thread(target=self.tokens_cancelletion_pattern, args=(user_id, self.tb.TextCommands, message, i))
                    thr.start()
                    self.db[user_id].text[i] = 0
                    thr.join()
                elif self.db[user_id].text[i] and self.db[user_id].some:
                    thr = Thread(target=self.tokens_cancelletion_pattern, args=(user_id, self.tb.SomeTextsCommand, message, i))
                    thr.start()
                    self.db[user_id].text[i] = 0
                    self.db[user_id].some = False
                    thr.join()
        self.insert_or_update_data(user_id, self.db[user_id])

    async def end_check_tariff_time(self) -> None:
        """
        Проверяет и обновляет статус подписки пользователей.
        """
        while True:
            for user_id, data in self.db.items():
                deltaf = data.datetime_sub - datetime.now().replace(microsecond=0)
                if int(deltaf.total_seconds()) <= 0 and (data.basic or data.pro or data.free_requests < 10):
                    self.db[user_id] = UserData(
                        text=data.text,
                        images=data.images,
                        free=data.free,
                        promocode=data.promocode,
                        ref=data.ref
                    )
                    self.insert_or_update_data(user_id, self.db[user_id])
            await asyncio.sleep(10)

# Bot launch
if __name__ == "__main__":
    bot_instance = TelegramBot()

    # Register handlers
    bot_instance.bot.pre_checkout_query_handler(func=lambda query: True)(bot_instance.process_pre_checkout_query)
    bot_instance.bot.message_handler(content_types=['successful_payment'])(bot_instance.successful_payment)
    bot_instance.bot.message_handler(commands=['start'])(bot_instance.start_processing)
    bot_instance.bot.message_handler(commands=['profile'])(bot_instance.personal_account)
    bot_instance.bot.message_handler(commands=['stat'])(bot_instance.show_stat)
    bot_instance.bot.callback_query_handler(func=lambda call: True)(bot_instance.calls_processing)
    bot_instance.bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])(bot_instance.tasks_processing)

    Thread(target=bot_instance.bot.infinity_polling).start()
    asyncio.run(bot_instance.end_check_tariff_time())