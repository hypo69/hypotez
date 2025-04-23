## \file hypotez/src/endpoints/bots/telegram/digital_market/bot/config.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Настройки и инициализация Telegram-бота для цифрового магазина.
===============================================================
Модуль содержит классы и переменные для конфигурации и инициализации
Telegram-бота, включая параметры безопасности, URL, настройки логирования
и подключения к базе данных.

 .. module:: hypotez/src/endpoints/bots/telegram/digital_market/bot/config
"""

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода отвечает за настройку и инициализацию Telegram-бота, включая загрузку переменных окружения, определение URL-ов для вебхуков, настройку логирования и создание экземпляров бота и диспетчера. Он использует библиотеку `aiogram` для управления ботом и `pydantic-settings` для загрузки настроек из переменных окружения.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются модули `os`, `List` из `typing`, `logger` из `loguru`, `Bot` и `Dispatcher` из `aiogram`, `ParseMode` из `aiogram.enums`, `MemoryStorage` из `aiogram.fsm.storage.memory`, `DefaultBotProperties` из `aiogram.client.default` и `BaseSettings`, `SettingsConfigDict` из `pydantic_settings`.
2. **Определение класса Settings**:
   - Создается класс `Settings`, наследующийся от `BaseSettings`, для хранения настроек бота.
   - Определяются атрибуты класса, такие как `BOT_TOKEN` (токен бота), `ADMIN_IDS` (список ID администраторов), `PROVIDER_TOKEN` (токен провайдера платежей), `FORMAT_LOG` (формат логов), `LOG_ROTATION` (ротация логов), `DB_URL` (URL базы данных), `SITE_URL` (URL сайта), `SITE_HOST` (хост сайта), `SITE_PORT` (порт сайта), `MRH_LOGIN` (логин MRH), `MRH_PASS_1` (пароль MRH), `MRH_PASS_2` (пароль MRH), `IN_TEST` (флаг тестовой среды).
   - Определяется конфигурация модели `SettingsConfigDict` для загрузки переменных окружения из файла `.env`, расположенного в директории на уровень выше текущей.
   - Создаются свойства `get_webhook_url` и `get_provider_hook_url`, которые динамически формируют URL-ы для вебхуков на основе `SITE_URL` и `BOT_TOKEN`.
3. **Инициализация настроек**: Создается экземпляр класса `Settings`, который загружает переменные окружения.
4. **Инициализация бота и диспетчера**:
   - Создается экземпляр класса `Bot` с использованием токена, полученного из настроек, и устанавливается режим парсинга HTML.
   - Создается экземпляр класса `Dispatcher` с использованием `MemoryStorage` для хранения состояния.
   - Получается список ID администраторов из настроек.
5. **Настройка логирования**:
   - Формируется путь к файлу логов.
   - Настраивается логирование с использованием `logger.add`, указывается путь к файлу, формат логов, уровень логирования и ротация логов.
6. **Определение URL базы данных**: URL базы данных берется из настроек.

Пример использования
-------------------------

```python
import os
from typing import List
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    PROVIDER_TOKEN: str
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'
    SITE_URL: str
    SITE_HOST: str
    SITE_PORT: int
    MRH_LOGIN: str
    MRH_PASS_1: str
    MRH_PASS_2: str
    IN_TEST: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    @property
    def get_webhook_url(self) -> str:
        """Динамически формирует путь для вебхука на основе токена и URL сайта."""
        return f"{self.SITE_URL}/{self.BOT_TOKEN}"

    @property
    def get_provider_hook_url(self) -> str:
        """Динамически формирует путь для вебхука на основе токена и URL сайта."""
        return f"{self.SITE_URL}/robokassa"


# Функция извлекает параметры для загрузки переменных среды
settings = Settings()

# Функция инициализирует бота и диспетчер
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
admins = settings.ADMIN_IDS

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.DB_URL

# Пример использования:
# Получение токена бота
bot_token = settings.BOT_TOKEN
print(f"Bot token: {bot_token}")

# Получение URL вебхука
webhook_url = settings.get_webhook_url
print(f"Webhook URL: {webhook_url}")