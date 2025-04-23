### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует Telegram-бота для обработки различных типов сообщений и команд, отправленных пользователями. Он использует библиотеку `telebot` для взаимодействия с API Telegram и включает функциональность для обработки текстовых сообщений, URL-адресов, команд, голосовых сообщений и документов. Бот также интегрирован с моделью `GoogleGenerativeAi` для генерации ответов на текстовые запросы.

Шаги выполнения
-------------------------
1. **Инициализация бота и обработчиков**:
   - Создается экземпляр класса `Config`, который загружает параметры конфигурации из переменных окружения или альтернативного источника.
   - Создается экземпляр класса `BotHandler`, который отвечает за обработку различных типов сообщений и команд.
   - Создается экземпляр класса `telebot.TeleBot` с использованием токена бота из конфигурации.

2. **Обработка команды `/start`**:
   - Функция `command_start` регистрируется для обработки команды `/start`.
   - При получении команды `/start` бот отправляет пользователю приветственное сообщение, определенное в `config.START_MESSAGE`.
   - Логируется информация об использовании команды `/start` пользователем.

3. **Обработка команды `/help`**:
   - Функция `command_help` регистрируется для обработки команды `/help`.
   - При получении команды `/help` вызывается метод `help_command` обработчика `BotHandler`, который отправляет пользователю список доступных команд.
   - Логируется информация об использовании команды `/help` пользователем.

4. **Обработка команды `/info`**:
   - Функция `command_info` регистрируется для обработки команды `/info`.
   - При получении команды `/info` бот отправляет пользователю информацию о боте, определенную в `config.COMMAND_INFO`.
   - Логируется информация об использовании команды `/info` пользователем.

5. **Обработка команды `/time`**:
   - Функция `command_time` регистрируется для обработки команды `/time`.
   - При получении команды `/time` бот отправляет пользователю текущее время.
   - Логируется информация об использовании команды `/time` пользователем.

6. **Обработка команды `/photo`**:
   - Функция `command_photo` регистрируется для обработки команды `/photo`.
   - При получении команды `/photo` бот отправляет пользователю случайное фото из директории, указанной в `config.PHOTO_DIR`.
   - Если директория не найдена или в ней нет фотографий, отправляется соответствующее сообщение об ошибке.
   - Логируется информация об использовании команды `/photo` пользователем.

7. **Обработка голосовых сообщений**:
   - Функция `handle_voice_message` регистрируется для обработки голосовых сообщений.
   - При получении голосового сообщения вызывается метод `handle_voice` обработчика `BotHandler`, который обрабатывает голосовое сообщение.
   - Логируется информация об отправке голосового сообщения пользователем.

8. **Обработка документов**:
   - Функция `handle_document_message` регистрируется для обработки документов.
   - При получении документа вызывается метод `handle_document` обработчика `BotHandler`, который обрабатывает документ.
   - Логируется информация об отправке документа пользователем.

9. **Обработка текстовых сообщений**:
   - Функция `handle_text_message` регистрируется для обработки текстовых сообщений, не начинающихся с `/`.
   - При получении текстового сообщения вызывается метод `handle_message` обработчика `BotHandler`, который обрабатывает текстовое сообщение.
   - Логируется информация об отправке текстового сообщения пользователем.

10. **Обработка неизвестных команд**:
    - Функция `handle_unknown_command` регистрируется для обработки текстовых сообщений, начинающихся с `/`, но не соответствующих известным командам.
    - При получении неизвестной команды бот отправляет пользователю сообщение об неизвестной команде, определенное в `config.UNKNOWN_COMMAND_MESSAGE`.
    - Логируется информация об отправке неизвестной команды пользователем.

11. **Запуск бота**:
    - Вызывается метод `bot.polling(none_stop=True)` для запуска бота в режиме непрерывного ожидания входящих сообщений.

Пример использования
-------------------------

```python
import telebot
import os
import datetime
import random
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv
load_dotenv()

from src.logger import logger

##############################################################

USE_ENV:bool = True # <- Определает откуда брать ключи. Если False - то из базы данных с паролями, иначе из .env

#############################################################

@dataclass
class Config:
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHANNEL_ID = '@onela'
    PHOTO_DIR = Path('./assets')
    COMMAND_INFO = 'This is a simple bot. Use /help to see commands.'
    UNKNOWN_COMMAND_MESSAGE = 'Unknown command. Use /help to see available commands.'
    START_MESSAGE = "Howdy, how are you doing?"
    HELP_MESSAGE = """
    Here are the available commands:
    /start - Starts the bot.
    /help - Shows this help message.
    /info - Shows information about the bot.
    /time - Shows the current time.
    /photo - Sends a random photo.
    """

class BotHandler:
    """Исполнитель команд, полученных ботом."""

    def help_command(self, bot, message):
        """Обработка команды /help."""
        bot.send_message(
            message.chat.id,
            'Available commands:\n'
            '/start - Start the bot\n'
            '/help - Show this help message\n'
            '/sendpdf - Send a PDF file'
        )

config = Config()
handler = BotHandler()
bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message):
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)

@bot.message_handler(commands=['help'])
def command_help(message):
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)

@bot.message_handler(commands=['info'])
def command_info(message):
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)

@bot.message_handler(commands=['time'])
def command_time(message):
    logger.info(f"User {message.from_user.username} send /time command")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")

@bot.message_handler(commands=['photo'])
def command_photo(message):
    logger.info(f"User {message.from_user.username} send /photo command")
    try:
        photo_files = os.listdir(config.PHOTO_DIR)
        if photo_files:
            random_photo = random.choice(photo_files)
            photo_path = os.path.join(config.PHOTO_DIR, random_photo)
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "No photos in the folder.")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Photo directory not found.")

@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    logger.info(f"User {message.from_user.username} sent message: {message.text}")
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    logger.info(f"User {message.from_user.username} send unknown command: {message.text}")
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)

bot.polling(none_stop=True)