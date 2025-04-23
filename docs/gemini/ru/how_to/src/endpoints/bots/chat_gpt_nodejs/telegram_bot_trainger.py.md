## \file /src/bots/openai_bots/telegram_bot_trainger.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.bots.openai_bots
	:platform: Windows, Unix
	:synopsis:

"""


""" This script creates a simple Telegram bot using the python-telegram-bot library."""

from pathlib import Path
import tempfile
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import header
from src import gs
from src.llm.openai.model.training import Model
from src.utils.jjson import j_loads_ns, j_loads_ns, j_dumps
from src.logger.logger import logger
import speech_recognition as sr  # Библиотека для распознавания речи
import requests  # Для скачивания файлов
from pydub import AudioSegment  # Библиотека для конвертации аудио
from gtts import gTTS  # Библиотека для текстового воспроизведения
from src.utils.convertors.tts import recognizer, text_to_speech

model = Model()

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TELEGRAM_TOKEN = gs.credentials.telegram.bot_token


async def start(update: Update, context: CallbackContext) -> None:
    """ Handle the /start command."""
    await update.message.reply_text('Hello! I am your simple bot. Type /help to see available commands.')


async def help_command(update: Update, context: CallbackContext) -> None:
    """ Handle the /help command."""
    await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help message')

async def handle_document(update: Update, context: CallbackContext):
    # Получаем файл
    file = await update.message.document.get_file()
    # tmp_file_path = f"{tempfile.gettempdir()}/received.txt"
    tmp_file_path = await file.download_to_drive()  # Сохраняем файл локально

    # Читаем содержимое файла
    with open(tmp_file_path, 'r') as f:
        file_content = f.read()

    response = model.send_message(f"Обучение модели на следующем содержимом:{file_content}")
    await update.message.reply_text(response)
    # tts_file_path = await text_to_speech (response)
    # await update.message.reply_audio(audio=open(tts_file_path, 'rb'))

async def handle_message(update: Update, context: CallbackContext) -> None:
    """ Handle any text message."""
    text_received = update.message.text
    response = model.send_message(text_received)
    await update.message.reply_text(response)
    # tts_file_path = await text_to_speech (response)
    # await update.message.reply_audio(audio=open(tts_file_path, 'rb'))

async def handle_voice(update: Update, context: CallbackContext) -> None:
    """ Handle voice messages."""
    voice_file = await update.message.voice.get_file()
    message = recognizer(audio_url=voice_file.file_path)
    response = model.send_message(message)
    await update.message.reply_text(response)
    tts_file_path = await text_to_speech(response)
    await update.message.reply_audio(audio=open(tts_file_path, 'rb'))

def main() -> None:
    """ Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()

```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует Telegram-бота, использующего библиотеку `python-telegram-bot`. Бот обрабатывает текстовые, голосовые сообщения и документы, отправляя запросы к языковой модели для генерации ответов.

Шаги выполнения
-------------------------
1. **Инициализация бота**:
   - Создается экземпляр `Application` с использованием токена, полученного из `gs.credentials.telegram.bot_token`.
2. **Регистрация обработчиков команд**:
   - Регистрируются обработчики команд `/start` и `/help`, которые отвечают на соответствующие команды.
3. **Регистрация обработчиков сообщений**:
   - Регистрируются обработчики для текстовых сообщений, голосовых сообщений и документов.
4. **Обработка документа**:
   - Функция `handle_document` получает файл из сообщения, сохраняет его локально, считывает содержимое и отправляет его в модель для обучения.
5. **Обработка текстовых сообщений**:
   - Функция `handle_message` получает текст сообщения, отправляет его в модель и отправляет ответ обратно пользователю.
6. **Обработка голосовых сообщений**:
   - Функция `handle_voice` получает голосовое сообщение, распознает текст из аудио, отправляет текст в модель и отправляет ответ обратно пользователю.
7. **Запуск бота**:
   - Бот запускается в режиме опроса (polling), чтобы постоянно прослушивать новые сообщения.

Пример использования
-------------------------

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from src.llm.openai.model.training import Model
from src.utils.convertors.tts import recognizer, text_to_speech
from src import gs

# Инициализация модели
model = Model()

# Получение токена из настроек
TELEGRAM_TOKEN = gs.credentials.telegram.bot_token

async def start(update: Update, context: CallbackContext) -> None:
    """Функция отвечает на команду /start."""
    await update.message.reply_text("Привет! Я простой бот. Напишите /help, чтобы увидеть доступные команды.")

async def help_command(update: Update, context: CallbackContext) -> None:
    """Функция отвечает на команду /help."""
    await update.message.reply_text("Доступные команды:\n/start - Запустить бота\n/help - Показать это сообщение")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обрабатывает любое текстовое сообщение."""
    text_received = update.message.text
    response = model.send_message(text_received)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: CallbackContext) -> None:
    """Обрабатывает голосовые сообщения."""
    voice_file = await update.message.voice.get_file()
    message = recognizer(audio_url=voice_file.file_path)
    response = model.send_message(message)
    await update.message.reply_text(response)
    tts_file_path = await text_to_speech(response)
    await update.message.reply_audio(audio=open(tts_file_path, 'rb'))

def main() -> None:
    """Запускает бота."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    # Регистрация обработчиков сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()