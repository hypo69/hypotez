### **Анализ кода модуля `minibot.py`**

## \file /src/endpoints/emil/minibot.py

Модуль содержит класс `BotHandler`, который обрабатывает команды, получаемые от Telegram-бота, взаимодействует с AI-моделью Google Gemini и выполняет различные сценарии, связанные с обработкой URL и другими командами.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на логические блоки, такие как `BotHandler`, `Config` и обработчики сообщений бота.
  - Используется логгирование для отслеживания действий пользователей и ошибок.
  - Присутствует обработка различных типов сообщений (текст, голос, документы).
- **Минусы**:
  - Не все методы класса `BotHandler` имеют docstring.
  - Есть небольшие участки кода, которые можно улучшить с точки зрения читаемости и структуры.
  - Отсутствуют аннотации типов для некоторых переменных и параметров.
  - Есть смешение ответственности в `BotHandler` (обработка сообщений и взаимодействие с моделью).

**Рекомендации по улучшению:**

1.  **Документирование методов**:
    - Добавить docstring для всех методов класса `BotHandler`, включая `help_command`, `send_pdf`, `handle_voice`, `handle_document`, `_transcribe_voice`.
2.  **Улучшение обработки исключений**:
    - В блоках `except` добавить более конкретную обработку исключений, чтобы избежать перехвата всех исключений подряд.
3.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций, где это необходимо.
4.  **Рефакторинг класса `BotHandler`**:
    - Рассмотреть возможность разделения класса `BotHandler` на несколько классов для улучшения структуры и разделения ответственности. Например, можно создать отдельный класс для обработки сообщений и отдельный класс для взаимодействия с AI-моделью.
5.  **Использовать `j_loads` или `j_loads_ns`**:
    - Если конфигурационные данные хранятся в JSON-файлах, использовать `j_loads` или `j_loads_ns` для их загрузки.
6.  **Улучшение сообщений об ошибках**:
    - Сделать сообщения об ошибках более информативными и понятными для пользователя.
7.  **Использовать константы для magic strings**:
    - Заменить строковые литералы, такие как URL `https://one-tab.com`, на константы для повышения читаемости и удобства поддержки.

**Оптимизированный код:**

```python
## \file /src/endpoints/emil/minibot.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с Telegram-ботом emil-design.com
=====================================================

Модуль содержит класс :class:`BotHandler`, который обрабатывает команды, получаемые от Telegram-бота,
взаимодействует с AI-моделью Google Gemini и выполняет различные сценарии, связанные с обработкой URL и другими командами.

Пример использования
----------------------

>>> from src.endpoints.emil.minibot import BotHandler, Config
>>> from telebot import TeleBot
>>> config = Config()
>>> handler = BotHandler()
>>> bot = TeleBot(config.BOT_TOKEN)
"""

import telebot
import os
import datetime
import random
from pathlib import Path
import asyncio
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

import header
from header import __root__
from src import gs
from src.logger import logger
from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.kazarinov.scenarios.scenario import fetch_target_urls_onetab, Scenario

from src.utils.url import is_url
from src.utils.printer import pprint as print

##############################################################

ENDPOINT: str = 'emil'
USE_ENV: bool = True  # <- Определает откуда брать ключи. Если False - то из базы данных с паролями, иначе из .env

#############################################################

class BotHandler:
    """Исполнитель команд, полученных ботом."""

    base_dir: Path = __root__ / 'src' / 'endpoints' / 'kazarinov'

    def __init__(self) -> None:
        """Инициализация обработчика событий телеграм-бота."""
        self.scenario: Scenario = Scenario()
        self.model: GoogleGenerativeAI = GoogleGenerativeAI(os.getenv('GEMINI_API'))
        self.questions_list: list[str] = ['Я не понял?', 'Объясни пожалуйста']


    def handle_message(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """Обработка текстовых сообщений.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        """
        text: str = message.text
        if text == '?':
            self._send_user_flowchart(bot, message.chat.id)
        elif is_url(text):
            self._handle_url(bot, message)
        elif text in ('--next', '-next', '__next', '-n', '-q'):
            self._handle_next_command(bot, message)
        else:
            try:
                answer: str = self.model.chat(text)
                bot.send_message(message.chat.id, answer)
            except Exception as ex:
                logger.error('Error during model interaction', ex, exc_info=True)
                bot.send_message(message.chat.id, 'Произошла ошибка при обработке сообщения.')


    def _send_user_flowchart(self, bot: telebot.TeleBot, chat_id: int) -> None:
        """Отправка схемы user_flowchart.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            chat_id (int): ID чата для отправки сообщения.

        """
        photo_path: Path = self.base_dir / 'assets' / 'user_flowchart.png'
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError as ex:
            logger.error(f'File not found: {photo_path}', ex, exc_info=True)
            bot.send_message(chat_id, 'Схема не найдена.')


    def _handle_url(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """Обработка URL, присланного пользователем.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        """
        url: str = message.text
        ONE_TAB_URLS: tuple[str, str] = ('https://one-tab.com', 'https://www.one-tab.com') # Константа для URL OneTab
        if not url.startswith(ONE_TAB_URLS):
            bot.send_message(message.chat.id, 'Мне на вход нужен URL `https://one-tab.com` Проверь, что ты мне посылаешь')
            return

        # Parsing https//one-tab.com/XXXXXXXXX page
        try:
            price: float
            mexiron_name: str
            urls: list[str]
            price, mexiron_name, urls = fetch_target_urls_onetab(url)
            bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
        except Exception as ex:
            logger.error('Error fetching URLs from OneTab', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при получении данных из OneTab.')
            return

        if not urls:
            bot.send_message(message.chat.id, 'Некорректные данные. Не получил список URL комплектующих')
            return

        try:
            asyncio.run(
                self.scenario.run_scenario(
                    bot=bot,
                    chat_id=message.chat.id,
                    urls=list(urls),
                    price=price,
                    mexiron_name=mexiron_name
                ))

        except Exception as ex:
            logger.error('Error during scenario execution', ex, exc_info=True)
            bot.send_message(message.chat.id, f'Произошла ошибка при выполнении сценария. {print(ex.args)}')


    def _handle_next_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """Обработка команды \'--next\' и её аналогов.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        """
        try:
            question: str = random.choice(self.questions_list)
            answer: str = self.model.ask(question)
            bot.send_message(message.chat.id, question)
            bot.send_message(message.chat.id, answer)
        except Exception as ex:
            logger.error('Ошибка чтения вопросов', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при чтении вопросов.')


    def help_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """Обработка команды /help.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        """
        bot.send_message(
            message.chat.id,
            'Available commands:\n'
            '/start - Start the bot\n'
            '/help - Show this help message\n'
            '/sendpdf - Send a PDF file'
        )


    def send_pdf(self, bot: telebot.TeleBot, message: 'telebot.types.Message', pdf_file: str) -> None:
        """Обработка команды /sendpdf для отправки PDF.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.
            pdf_file (str): Путь к PDF-файлу.

        """
        try:
            with open(pdf_file, 'rb') as pdf_file_obj:
                bot.send_document(message.chat.id, document=pdf_file_obj)
        except FileNotFoundError as ex:
            logger.error('Ошибка при отправке PDF-файла', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при отправке PDF-файла. Попробуй ещё раз.')


    def handle_voice(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """Обработка голосовых сообщений.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        """
        try:
            file_info: telebot.types.File = bot.get_file(message.voice.file_id)
            file: bytes = bot.download_file(file_info.file_path)
            file_path: Path = gs.path.temp / f'{message.voice.file_id}.ogg'
            with open(file_path, 'wb') as f:
                f.write(file)
            transcribed_text: str = self._transcribe_voice(file_path)
            bot.send_message(message.chat.id, f'Распознанный текст: {transcribed_text}')
        except Exception as ex:
            logger.error('Ошибка при обработке голосового сообщения', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке голосового сообщения. Попробуй ещё раз.')


    def _transcribe_voice(self, file_path: str | Path) -> str:
        """Транскрибирование голосового сообщения (заглушка).

        Args:
            file_path (str | Path): Путь к файлу голосового сообщения.

        Returns:
            str: Сообщение о том, что распознавание голоса еще не реализовано.

        """
        return 'Распознавание голоса ещё не реализовано.'


    def handle_document(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> bool:
        """Обработка полученных документов.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            bool: True в случае успешной обработки, False в случае ошибки.

        """
        try:
            file_info: telebot.types.File = bot.get_file(message.document.file_id)
            file: bytes = bot.download_file(file_info.file_path)
            tmp_file_path: Path = gs.path.temp / message.document.file_name
            with open(tmp_file_path, 'wb') as f:
                f.write(file)
            bot.send_message(message.chat.id, f'Файл сохранен в {tmp_file_path}')
            return True
        except Exception as ex:
            logger.error('Ошибка при обработке документа', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке документа. Попробуй ещё раз.')
            return False

# --- config.py -----------------
class Config:
    """Конфигурация бота."""
    BOT_TOKEN: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_emil_design_bot
    CHANNEL_ID: str = '@onela'
    PHOTO_DIR: Path = Path(__root__ / 'endpoints' / 'kazarinov' / 'assets')
    COMMAND_INFO: str = 'This is a simple bot. Use /help to see commands.'
    UNKNOWN_COMMAND_MESSAGE: str = 'Unknown command. Use /help to see available commands.'
    START_MESSAGE: str = "Howdy, how are you doing?"
    HELP_MESSAGE: str = """
    Here are the available commands:
    /start - Starts the bot.
    /help - Shows this help message.
    /info - Shows information about the bot.
    /time - Shows the current time.
    /photo - Sends a random photo.
    """
# --- config.py end -----------------

# --- bot.py ---
config: Config = Config()
handler: BotHandler = BotHandler()
bot: telebot.TeleBot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message: 'telebot.types.Message') -> None:
    """Обработка команды /start."""
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)

@bot.message_handler(commands=['help'])
def command_help(message: 'telebot.types.Message') -> None:
    """Обработка команды /help."""
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)

@bot.message_handler(commands=['info'])
def command_info(message: 'telebot.types.Message') -> None:
    """Обработка команды /info."""
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)

@bot.message_handler(commands=['time'])
def command_time(message: 'telebot.types.Message') -> None:
    """Обработка команды /time."""
    logger.info(f"User {message.from_user.username} send /time command")
    now: datetime.datetime = datetime.datetime.now()
    current_time: str = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")

@bot.message_handler(commands=['photo'])
def command_photo(message: 'telebot.types.Message') -> None:
    """Обработка команды /photo."""
    logger.info(f"User {message.from_user.username} send /photo command")
    try:
        photo_files: list[str] = os.listdir(config.PHOTO_DIR)
        if photo_files:
            random_photo: str = random.choice(photo_files)
            photo_path: str = os.path.join(config.PHOTO_DIR, random_photo)
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "No photos in the folder.")
    except FileNotFoundError as ex:
        logger.error("Photo directory not found", ex, exc_info=True)
        bot.send_message(message.chat.id, "Photo directory not found.")

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: 'telebot.types.Message') -> None:
    """Обработка голосовых сообщений."""
    logger.info(f"User {message.from_user.username} send voice message")
    handler.handle_voice(bot, message)

@bot.message_handler(content_types=['document'])
def handle_document_message(message: 'telebot.types.Message') -> None:
    """Обработка сообщений с документами."""
    logger.info(f"User {message.from_user.username} send document message")
    handler.handle_document(bot, message)

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message: 'telebot.types.Message') -> None:
    """Обработка текстовых сообщений, не начинающихся с '/'. """
    logger.info(f"User {message.from_user.username} sent message: {message.text}")
    handler.handle_message(bot, message)

@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message: 'telebot.types.Message') -> None:
    """Обработка неизвестных команд."""
    logger.info(f"User {message.from_user.username} send unknown command: {message.text}")
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)

bot.polling(none_stop=True)
# --- bot.py end ---