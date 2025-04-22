### **Анализ кода модуля `minibot.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован, разделен на классы и функции, что облегчает понимание и поддержку.
    - Используется логирование для отслеживания работы бота и обработки ошибок.
    - Применяются переменные окружения для конфиденциальных данных (токен бота).
    - Обработка различных типов сообщений (текст, голосовые сообщения, документы).
- **Минусы**:
    - В некоторых местах отсутствует аннотация типов.
    - Смешанный стиль использования кавычек (как двойных, так и одинарных).
    - Не все функции имеют подробные docstring, описывающие их назначение, аргументы и возвращаемые значения.
    - Есть участки кода, которые можно улучшить с точки зрения обработки исключений и логирования.
    - Есть глобальные переменные: `ENDPOINT`, `USE_ENV`
    - Жестко заданные пути к файлам (например, `self.base_dir / 'assets' / 'user_flowchart.png'`) могут быть негибкими.
    - Не используется `cls` вместо `self` в методах класса.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    *   Добавить docstring к каждой функции, описывающие её назначение, аргументы, возвращаемые значения и возможные исключения.
    *   Использовать примеры в docstring, чтобы показать, как использовать функцию.
2.  **Улучшить аннотацию типов**:
    *   Добавить аннотации типов ко всем переменным и аргументам функций, где они отсутствуют.
3.  **Привести к единообразию стиль кавычек**:
    *   Использовать только одинарные кавычки (`'`) для строковых литералов.
4.  **Улучшить обработку исключений**:
    *   Указывать конкретные типы исключений в блоках `except`.
    *   Добавить больше контекста в сообщения об ошибках в логах.
    *   Использовать `ex.args` для получения аргументов исключения при логировании.
5.  **Конфигурация и пути**:
    *   Использовать переменные конфигурации для задания путей к файлам и каталогам, чтобы сделать код более гибким.
6.  **Использовать `cls` вместо `self`**:
    *   Использовать `cls` вместо `self` в методах класса.
7.  **Избавиться от глобальных переменных**:
    *   Определить `ENDPOINT` и `USE_ENV`  в классе `Config`.

**Оптимизированный код:**

```python
## \file /src/endpoints/emil/minibot.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для создания простого Telegram-бота, обслуживающего запросы для emil-design.com.
=========================================================================================

Модуль содержит класс :class:`BotHandler`, который обрабатывает команды и сообщения,
полученные от Telegram-бота. Он также включает в себя конфигурацию бота и функции для
обработки различных типов сообщений, таких как текст, голосовые сообщения и документы.

Пример использования
----------------------

>>> bot_handler = BotHandler()
>>> bot_handler.handle_message(bot, message)
"""

import telebot
import os
import datetime
import random
from pathlib import Path
import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

import header
from header import __root__
from src import gs
from src.logger import logger
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.kazarinov.scenarios.scenario import fetch_target_urls_onetab, Scenario
from src.utils.url import is_url
from src.utils.printer import pprint as print


##############################################################

#############################################################


class Config:
    """Конфигурация бота."""

    BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_emil_design_bot
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
    ENDPOINT: str = 'emil'
    USE_ENV: bool = True  # <- Определает откуда брать ключи. Если False - то из базы данных с паролями, иначе из .env


class BotHandler:
    """Исполнитель команд, полученных ботом."""

    base_dir: Path = __root__ / 'src' / 'endpoints' / 'kazarinov'

    def __init__(self) -> None:
        """Инициализация обработчика событий телеграм-бота."""
        self.scenario: Scenario = Scenario()
        self.model: GoogleGenerativeAi = GoogleGenerativeAi(os.getenv('GEMINI_API'))
        self.questions_list: list[str] = ['Я не понял?', 'Объясни пожалуйста']

    def handle_message(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обрабатывает текстовые сообщения, поступающие от пользователя.

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
                logger.error(f"Error during model interaction: {ex}", ex, exc_info=True)
                bot.send_message(message.chat.id, "Произошла ошибка при обработке сообщения.")

    def _send_user_flowchart(self, bot: telebot.TeleBot, chat_id: int) -> None:
        """
        Отправляет схему user_flowchart пользователю.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            chat_id (int): ID чата пользователя.
        """
        photo_path: Path = self.base_dir / 'assets' / 'user_flowchart.png'
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError as ex:
            logger.error(f"File not found: {photo_path}", ex, exc_info=True)
            bot.send_message(chat_id, "Схема не найдена.")

    def _handle_url(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обрабатывает URL, присланный пользователем.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.
        """
        url: str = message.text
        if not url.startswith(('https://one-tab.com', 'https://www.one-tab.com')):
            bot.send_message(
                message.chat.id, 'Мне на вход нужен URL `https://one-tab.com` Проверь, что ты мне посылаешь'
            )
            return

        # Parsing https//one-tab.com/XXXXXXXXX page
        try:
            price: float
            mexiron_name: str
            urls: list[str]
            price, mexiron_name, urls = fetch_target_urls_onetab(url)
            bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
        except Exception as ex:
            logger.error(f"Error fetching URLs from OneTab: {ex}", ex, exc_info=True)
            bot.send_message(message.chat.id, "Произошла ошибка при получении данных из OneTab.")
            return
        if not urls:
            bot.send_message(message.chat.id, 'Некорректные данные. Не получил список URL комплектующих')
            return

        try:
            asyncio.run(
                self.scenario.run_scenario(
                    bot=bot, chat_id=message.chat.id, urls=list(urls), price=price, mexiron_name=mexiron_name
                )
            )

        except Exception as ex:
            logger.error(f"Error during scenario execution: {ex}", ex, exc_info=True)
            bot.send_message(message.chat.id, f"Произошла ошибка при выполнении сценария. {print(ex.args)}")

    def _handle_next_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обрабатывает команду '--next' и её аналоги.

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
            logger.error(f'Ошибка чтения вопросов: {ex}', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при чтении вопросов.')

    def help_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обрабатывает команду /help.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.
        """
        bot.send_message(
            message.chat.id,
            'Available commands:\n'
            '/start - Start the bot\n'
            '/help - Show this help message\n'
            '/sendpdf - Send a PDF file',
        )

    def send_pdf(self, bot: telebot.TeleBot, message: 'telebot.types.Message', pdf_file: str) -> None:
        """
        Обрабатывает команду /sendpdf для отправки PDF.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.
            pdf_file (str): Путь к PDF-файлу.
        """
        try:
            with open(pdf_file, 'rb') as pdf_file_obj:
                bot.send_document(message.chat.id, document=pdf_file_obj)
        except Exception as ex:
            logger.error(f'Ошибка при отправке PDF-файла: {ex}', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при отправке PDF-файла. Попробуй ещё раз.')

    def handle_voice(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обрабатывает голосовые сообщения.

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
            logger.error(f'Ошибка при обработке голосового сообщения: {ex}', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке голосового сообщения. Попробуй ещё раз.')

    def _transcribe_voice(self, file_path: Path) -> str:
        """
        Транскрибирует голосовое сообщение (заглушка).

        Args:
            file_path (Path): Путь к файлу голосового сообщения.

        Returns:
            str: Распознанный текст (в данном случае, заглушка).
        """
        return 'Распознавание голоса ещё не реализовано.'

    def handle_document(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> bool:
        """
        Обрабатывает полученные документы.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            bool: True, если обработка прошла успешно, False в противном случае.
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
            logger.error(f'Ошибка при обработке документа: {ex}', ex, exc_info=True)
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке документа. Попробуй ещё раз.')
            return False


config: Config = Config()
handler: BotHandler = BotHandler()
bot: telebot.TeleBot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает команду /start.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)


@bot.message_handler(commands=['help'])
def command_help(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает команду /help.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)


@bot.message_handler(commands=['info'])
def command_info(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает команду /info.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)


@bot.message_handler(commands=['time'])
def command_time(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает команду /time.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send /time command")
    now: datetime.datetime = datetime.datetime.now()
    current_time: str = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")


@bot.message_handler(commands=['photo'])
def command_photo(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает команду /photo.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
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
        logger.error(f"Photo directory not found: {ex}", ex, exc_info=True)
        bot.send_message(message.chat.id, "Photo directory not found.")


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает голосовые сообщения.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send voice message")
    handler.handle_voice(bot, message)


@bot.message_handler(content_types=['document'])
def handle_document_message(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает сообщения с документами.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send document message")
    handler.handle_document(bot, message)


@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает текстовые сообщения, не начинающиеся с '/'.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} sent message: {message.text}")
    handler.handle_message(bot, message)


@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message: 'telebot.types.Message') -> None:
    """
    Обрабатывает неизвестные команды.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
    logger.info(f"User {message.from_user.username} send unknown command: {message.text}")
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)


bot.polling(none_stop=True)