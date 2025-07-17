## \file /src/endpoints/kazarinov/minibot.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module implements a Telegram bot that interacts with users to fetch and process data from OneTab links, allowing for the creation of a price list for Kazarinov.
========================================================================
```rst
.. module:: src.endpoints.kazarinov.minibot 
```
"""
import time
import threading
import requests
import telebot
from telebot import TeleBot
from telebot.types import Message, User
import os
from dataclasses import dataclass, field
from datetime import datetime
import random
from pathlib import Path
from types import SimpleNamespace
from typing import Callable
import asyncio

import header
from header import __root__
from src import gs, USE_ENV
from src.logger import logger
from src.endpoints.kazarinov.scenarios.scenario import Scenario
from src.endpoints.kazarinov.scenarios.fetch_one_tab import fetch_one_tab_data
from src.utils.url import is_url
from src.utils.jjson import j_loads_ns 
from src.utils.printer import pprint as print



# --- config.py -----------------

class Config:
    """! Конфигурация бота Kazarinov с статическими атрибутами."""

    ENDPOINT:str = 'kazarinov'
    config: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'endpoints' / ENDPOINT / f'{ENDPOINT}.json')
    if not config:
        raise FileNotFoundError(f"Configuration file not found: {__root__ / 'src' / 'endpoints' / ENDPOINT / f'{ENDPOINT}.json'}")

    MODE:str = 'PRODUCTION' # 'DEV' # <- Определяет режим разработчика. Если MODE=='PRODUCTION' будет запущен kazarionaov бот, иначе тестбот
    BOT_TOKEN:str
   
    if MODE=='PRODUCTION':
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_kazarinov_bot.token
    else:
        BOT_TOKEN = os.getenv('TEST_BOT_TOKEN') if USE_ENV else gs.credentials.telegram.hypo69_test_bot.token

    CHANNEL_ID: str = '@onela'
    PHOTO_DIR: Path = Path(__root__ / 'src' / 'endpoints' / 'kazarinov' / 'assets')
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
    CONNECTION_CHECK_INTERVAL: float = 30.0  # Интервал проверки соединения с ботом в секундах

    if USE_ENV:
        from dotenv import load_dotenv
        load_dotenv()

    DEFAULT_GEMINI_MODEL: str = 'gemini-2.5-flash'  # Default model for Gemini API'

# --- config.py end -----------------


# --- handlers.py -----------------
@dataclass(slots=True, kw_only=True)
class BotHandler:
    """! Обработчик команд Telegram-бота Kazarinov."""
    _connection_checker_started: bool = field(default=False, init=False)
    questions_list: list[str] = field(default_factory=lambda: ['Я не понял?', 'Объясни пожалуйста'])

    def handle_message(self, bot: TeleBot, message: Message) -> None:
        text = message.text
        if text == '?':
            self._send_user_flowchart(bot, message.chat.id)
        elif is_url(text):
            self._handle_url(bot, message)
        elif text in ('--next', '-next', '__next', '-n', '-q'):
            self._handle_next_command(bot, message)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда. Введите /help")

    def _send_user_flowchart(self, bot: TeleBot, chat_id: int) -> None:
        photo_path = Config.PHOTO_DIR / 'user_flowchart.png'
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError:
            logger.error(f"File not found: {photo_path}")
            bot.send_message(chat_id, "Схема не найдена.")

    def _handle_url(self, bot: TeleBot, message: Message) -> None:
        url = message.text
        if not url.startswith(('https://one-tab.com', 'https://www.one-tab.com')):
            bot.send_message(message.chat.id, 'Мне на вход нужен URL `https://one-tab.com`.')
            return

        try:
            mexiron_name, price, urls = fetch_one_tab_data(url)
            bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
        except Exception as ex:
            logger.error(f"\nError fetching URLs from OneTab: ", ex,  exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при получении данных из OneTab.")
            return

        if not urls:
            bot.send_message(message.chat.id, 'Список URL пуст')
            logger.debug(f"\nError fetching URLs from OneTab: ", ex,  exc_info=True)
            return

        try:
            #scenario = Scenario()
            asyncio.run(
                Scenario().run_scenario_async(
                    mexiron_name = mexiron_name or gs.now,
                    price=price,
                    urls=list(urls),
                    bot=bot,
                    chat_id=message.chat.id,
                )
            )
        except Exception as ex:
            logger.error(f"Error during scenario execution: \n", ex, exc_info=True)
            bot.send_message(message.chat.id, f"Ошибка запуска сценария: \n{ex}\n")

    def _handle_next_command(self, bot: TeleBot, message: Message) -> None:
        try:
            question = random.choice(self.questions_list)
            bot.send_message(message.chat.id, f"Вопрос: {question}\n(Ответ не реализован)")
        except Exception as ex:
            logger.error(f'Ошибка в _handle_next_command: {ex}')
            bot.send_message(message.chat.id, 'Ошибка при обработке команды.')

    def help_command(self, bot: TeleBot, message: Message) -> None:
        bot.send_message(message.chat.id, Config.HELP_Message)

    def handle_voice(self, bot: TeleBot, message: Message) -> None:
        bot.send_message(message.chat.id, 'Распознавание голоса не реализовано.')

    def handle_document(self, bot: TeleBot, message: Message) -> None:
        bot.send_message(message.chat.id, 'Обработка документов не реализована.')
# --- handlers.py end---


# --- bot.py ---

@dataclass(slots=True, kw_only=True)
class KazarinovBot:
    """! Telegram-бот для проекта Kazarinov."""

    config: Config = field(default_factory=Config)
    handler: BotHandler = field(default_factory=BotHandler)
    bot: TeleBot = field(init=False)

    def __post_init__(self) -> None:
        self.bot = TeleBot(self.config.BOT_TOKEN)
        self._register_handlers()
        

    def _register_handlers(self) -> None:
        self.bot.message_handler(commands=['start'])(self._wrap(self._command_start))
        self.bot.message_handler(commands=['help'])(self._wrap(self._command_help))
        self.bot.message_handler(commands=['info'])(self._wrap(self._command_info))
        self.bot.message_handler(commands=['time'])(self._wrap(self._command_time))
        self.bot.message_handler(commands=['photo'])(self._wrap(self._command_photo))
        self.bot.message_handler(content_types=['voice'])(self._wrap(self._handle_voice))
        self.bot.message_handler(content_types=['document'])(self._wrap(self._handle_document))
        self.bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith('/'))(self._wrap(self._handle_text))
        self.bot.message_handler(func=lambda msg: msg.text and msg.text.startswith('/'))(self._wrap(self._handle_unknown))

    def _wrap(self, func: Callable) -> Callable:
        def wrapper(message: Message):
            try:
                logger.info(f"User {message.from_user.username} sent message: {message.text}")
                func(message)
            except Exception as ex:
                logger.error(f"Ошибка в обработчике {func.__name__}: {ex}", exc_info=True)
                self.bot.send_message(message.chat.id, "⚠ Произошла внутренняя ошибка.")
        return wrapper

    def _command_start(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, self.config.START_MESSAGE)

    def _command_help(self, message: Message) -> None:
        self.handler.help_command(self.bot, message)

    def _command_info(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, self.config.COMMAND_INFO)

    def _command_time(self, message: Message) -> None:
        current_time = datetime.now().strftime("%H:%M:%S")
        self.bot.send_message(message.chat.id, f"Current time: {current_time}")

    def _command_photo(self, message: Message) -> None:
        try:
            photo_files = [f for f in self.config.PHOTO_DIR.iterdir() if f.is_file()]
            if photo_files:
                random_photo = random.choice(photo_files)
                with open(random_photo, 'rb') as photo:
                    self.bot.send_photo(message.chat.id, photo)
            else:
                self.bot.send_message(message.chat.id, "No photos in the folder.")
        except FileNotFoundError:
            self.bot.send_message(message.chat.id, "Photo directory not found.")

    def _handle_voice(self, message: Message) -> None:
        self.handler.handle_voice(self.bot, message)

    def _handle_document(self, message: Message) -> None:
        self.handler.handle_document(self.bot, message)

    def _handle_text(self, message: Message) -> None:
        self.handler.handle_message(self.bot, message)

    def _handle_unknown(self, message: Message) -> None:
        self.bot.send_message(message.chat.id, self.config.UNKNOWN_COMMAND_MESSAGE)


    

    def check_connection_status(self, url: str = "https://api.telegram.org") -> None:
        while True:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    logger.warning(f"Статус ответа от сервера: {response.status_code}")
                    ...
            except Exception:
                logger.error("Обнаружена потеря соединения с сервером!", exc_info=True)
                self.restart_bot()
            threading.Event().wait(Config.CONNECTION_CHECK_INTERVAL)


    def restart_bot(self) -> bool:
        logger.info("Restarting bot...")
        if self.bot_stop():
            return self.bot_start()
        return False


    def bot_stop(self) -> bool:
        try:
            logger.info("Initiating bot shutdown...")
            self.bot.stop_polling()
            time.sleep(1)
            return True
        except Exception as ex:
            logger.error("Error during bot shutdown", ex)
            return False



    def bot_start(self, attempts: int = 3) -> bool:
        while attempts > 0:
            try:
                logger.info("Starting bot polling...")
                self.bot.infinity_polling()
                return True
            except Exception as ex:
                logger.error("Error during polling", ex)
                attempts -= 1
                logger.debug(f"Retrying in 10 seconds... Attempts left: {attempts}")
                time.sleep(10)
        raise RuntimeError("Failed to start bot after multiple attempts.")



if __name__ == '__main__':
    KazarinovBot().bot_start()

