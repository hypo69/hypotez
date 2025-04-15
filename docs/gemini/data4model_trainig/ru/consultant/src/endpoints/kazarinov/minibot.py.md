### **Анализ кода модуля `minibot.py`**

## \file /src/endpoints/kazarinov/minibot.py

Модуль содержит реализацию Telegram-бота для работы с запросами на создание прайс-листов для проекта Казаринова.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на логические блоки (Config, BotHandler, bot.py).
  - Используется логирование для отслеживания работы бота.
  - Присутствует обработка исключений.
- **Минусы**:
  - Не все функции и методы имеют docstring.
  - Некоторые переменные не аннотированы типами.
  - Есть смешение стилей в форматировании строк (использование как `""`, так и `''`).
  - Отсутствуют примеры использования в docstring.

**Рекомендации по улучшению:**

1.  **Добавить docstring**: Добавить подробные docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
2.  **Аннотации типов**: Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.
3.  **Унифицировать стиль строк**: Использовать только одинарные кавычки (`'`) для определения строк.
4.  **Примеры использования**: Добавить примеры использования в docstring для основных функций и классов.
5.  **Обработка исключений**: Указывать конкретные типы исключений в блоках `except`.
6.  **Логирование**: Использовать форматированные строки для логирования, чтобы было легче читать и понимать сообщения.
7.  **Пересмотреть структуру `Config`**: Рассмотреть возможность использования `dataclasses` для более удобного и структурированного хранения конфигурации.

**Оптимизированный код:**

```python
## \file /src/endpoints/kazarinov/minibot.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с Telegram-ботом для обслуживания запросов на создание прайс-листов для проекта Казаринова
===========================================================================================================

Модуль содержит классы и функции для обработки команд и сообщений от Telegram-бота,
включая взаимодействие с Google Gemini AI и получение данных из OneTab.

[Документация](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/endpoints/kazarinov/minibot.py.md)
"""

import asyncio
import datetime
import os
import random
import time
from pathlib import Path
from typing import List, Optional, Tuple

import telebot

import header
from header import __root__
from src import gs
from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.kazarinov.scenarios.scenario import Scenario, fetch_target_urls_onetab
from src.logger import logger
from src.utils.printer import pprint as print
from src.utils.url import is_url
from src import USE_ENV

# --- config.py -----------------


class Config:
    """
    Конфигурация бота.
    """

    ENDPOINT: str = 'kazarinov'
    MODE: str = 'PRODUCTION'  # Определяет режим разработчика. Если MODE=='PRODUCTION' будет запущен kazarionaov бот, иначе тестбот
    # MODE:str = 'DEV'
    BOT_TOKEN: str

    if MODE == 'PRODUCTION':
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_kazarinov_bot
    else:
        BOT_TOKEN = os.getenv('TEST_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_test_bot

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

    if USE_ENV:
        from dotenv import load_dotenv

        load_dotenv()


# --- config.py end -----------------


class BotHandler:
    """Исполнитель команд, полученных ботом."""

    base_dir: Path = __root__ / 'src' / 'endpoints' / 'kazarinov'

    def __init__(self):
        """Инициализация обработчика событий телеграм-бота."""
        self.questions_list: List[str] = ['Я не понял?', 'Объясни пожалуйста']
        self.model: GoogleGenerativeAI = GoogleGenerativeAI(os.getenv('GEMINI_API') if USE_ENV else gs.credentials.gemini.kazarinov)

    def handle_message(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обработка текстовых сообщений, поступающих от пользователя.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            None

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
                logger.error(f"Error during model interaction: {ex}", exc_info=True)  # Добавлено exc_info=True
                bot.send_message(message.chat.id, "Произошла ошибка при обработке сообщения.")

    def _send_user_flowchart(self, bot: telebot.TeleBot, chat_id: int) -> None:
        """
        Отправка схемы user_flowchart пользователю.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            chat_id (int): ID чата пользователя.

        Returns:
            None

        """
        photo_path: Path = self.base_dir / 'assets' / 'user_flowchart.png'
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError as ex:
            logger.error(f"File not found: {photo_path}", exc_info=True)  # Добавлено exc_info=True
            bot.send_message(chat_id, "Схема не найдена.")

    def _handle_url(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обработка URL, присланного пользователем.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            None

        """
        url: str = message.text
        if not url.startswith(('https://one-tab.com', 'https://www.one-tab.com')):
            bot.send_message(message.chat.id, 'Мне на вход нужен URL `https://one-tab.com` Проверь, что ты мне посылаешь')
            return

        # Parsing https//one-tab.com/XXXXXXXXX
        try:
            price: float
            mexiron_name: str
            urls: List[str]
            price, mexiron_name, urls = fetch_target_urls_onetab(url)
            bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
        except Exception as ex:
            logger.error(f"Error fetching URLs from OneTab: {ex}", exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, "Произошла ошибка при получении данных из OneTab.")
            return
        if not urls:
            bot.send_message(message.chat.id, 'Некорректные данные. Не получил список URL комплектующих')
            return

        try:
            self.scenario: Scenario = Scenario(window_mode='headless' if Config.MODE == 'PRODUCTION' else 'normal')  # debug
            asyncio.run(
                self.scenario.run_scenario_async(
                    mexiron_name=mexiron_name,
                    urls=list(urls),
                    price=price,
                    bot=bot,
                    chat_id=message.chat.id,
                )
            )

        except Exception as ex:
            logger.error(f"Error during scenario execution: {ex}", exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, f"Произошла ошибка при выполнении сценария. {ex}")

    def _handle_next_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обработка команды '--next' и её аналогов.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            None

        """
        try:
            question: str = random.choice(self.questions_list)
            answer: str = self.model.ask(question)
            bot.send_message(message.chat.id, question)
            bot.send_message(message.chat.id, answer)
        except Exception as ex:
            logger.error(f'Ошибка чтения вопросов: {ex}', exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, 'Произошла ошибка при чтении вопросов.')

    def help_command(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обработка команды /help.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            None

        """
        bot.send_message(
            message.chat.id,
            'Available commands:\n' '/start - Start the bot\n' '/help - Show this help message\n' '/sendpdf - Send a PDF file',
        )

    def send_pdf(self, bot: telebot.TeleBot, message: 'telebot.types.Message', pdf_file: str) -> None:
        """
        Обработка команды /sendpdf для отправки PDF.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.
            pdf_file (str): Путь к PDF-файлу.

        Returns:
            None

        """
        try:
            with open(pdf_file, 'rb') as pdf_file_obj:
                bot.send_document(message.chat.id, document=pdf_file_obj)
        except Exception as ex:
            logger.error(f'Ошибка при отправке PDF-файла: {ex}', exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, 'Произошла ошибка при отправке PDF-файла. Попробуй ещё раз.')

    def handle_voice(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> None:
        """
        Обработка голосовых сообщений.

        Args:
            bot (telebot.TeleBot): Экземпляр бота.
            message (telebot.types.Message): Объект сообщения от пользователя.

        Returns:
            None

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
            logger.error(f'Ошибка при обработке голосового сообщения: {ex}', exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке голосового сообщения. Попробуй ещё раз.')

    def _transcribe_voice(self, file_path: Path) -> str:
        """
        Транскрибирование голосового сообщения (заглушка).

        Args:
            file_path (Path): Путь к файлу голосового сообщения.

        Returns:
            str: Распознанный текст.

        """
        return 'Распознавание голоса ещё не реализовано.'

    def handle_document(self, bot: telebot.TeleBot, message: 'telebot.types.Message') -> bool:
        """
        Обработка полученных документов.

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
            logger.error(f'Ошибка при обработке документа: {ex}', exc_info=True)  # Добавлено exc_info=True
            bot.send_message(message.chat.id, 'Произошла ошибка при обработке документа. Попробуй ещё раз.')
            return False


# --- bot.py ---
config: Config = Config()
handler: BotHandler = BotHandler()
bot: telebot.TeleBot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: 'telebot.types.Message') -> None:
    """
    Обработка команды /start.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)


@bot.message_handler(commands=['help'])
def command_help(message: 'telebot.types.Message') -> None:
    """
    Обработка команды /help.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)


@bot.message_handler(commands=['info'])
def command_info(message: 'telebot.types.Message') -> None:
    """
    Обработка команды /info.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)


@bot.message_handler(commands=['time'])
def command_time(message: 'telebot.types.Message') -> None:
    """
    Обработка команды /time.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send /time command")
    now: datetime.datetime = datetime.datetime.now()
    current_time: str = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")


@bot.message_handler(commands=['photo'])
def command_photo(message: 'telebot.types.Message') -> None:
    """
    Обработка команды /photo.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send /photo command")
    try:
        photo_files: List[str] = os.listdir(config.PHOTO_DIR)
        if photo_files:
            random_photo: str = random.choice(photo_files)
            photo_path: str = os.path.join(config.PHOTO_DIR, random_photo)
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "No photos in the folder.")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Photo directory not found.")


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message: 'telebot.types.Message') -> None:
    """
    Обработка голосовых сообщений.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f"User {message.from_user.username} send voice message")
    handler.handle_voice(bot, message)


@bot.message_handler(content_types=['document'])
def handle_document_message(message: 'telebot.types.Message') -> None:
    """
    Обработка сообщений с документами.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f'User {message.from_user.username} send document message')
    handler.handle_document(bot, message)


@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message: 'telebot.types.Message') -> None:
    """
    Обработка текстовых сообщений, не являющихся командами.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f'User {message.from_user.username} sent message: {message.text}')
    handler.handle_message(bot, message)


@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message: 'telebot.types.Message') -> None:
    """
    Обработка неизвестных команд.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.

    Returns:
        None

    """
    logger.info(f'User {message.from_user.username} send unknown command: {message.text}')
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)


def main(restarts: int = 5) -> None:
    """
    Основная функция для запуска бота.

    Args:
        restarts (int, optional): Количество попыток перезапуска бота в случае ошибки. Defaults to 5.

    Returns:
        None

    """
    try:
        logger.info(f'Starting bot in {Config.MODE} mode')
        restarts: int = 5  # <- пусть будет бесконечный цикл
        bot.polling(none_stop=True)

    except Exception as ex:
        logger.error(f'Error during bot polling: {ex}', exc_info=True)
        ...
        if restarts > 1:
            try:
                bot.stop_bot()
            except Exception as ex:
                logger.error(f'Ошибка останова бота:{ex}', exc_info=True)
            logger.debug('Повторный запуск через 10 сек')
            time.sleep(10)
            main(restarts - 1)
        else:
            logger.error(f'Превышено количество переподключений')


if __name__ == '__main__':
    main(restarts=5)