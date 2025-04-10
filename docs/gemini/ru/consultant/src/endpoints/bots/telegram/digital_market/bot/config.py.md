### **Анализ кода модуля `config.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `pydantic_settings` для управления конфигурацией.
  - Разделение конфигурации и логики приложения.
  - Использование `loguru` для логирования.
  - Аннотация типов.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - Использование `os.path.join` вместо `pathlib`.
  - Отсутствует docstring для модуля.
  - Не используется модуль `src.logger.logger` для логирования.
  - Не все функции документированы.
  - Отсутствуют примеры использования в docstring.

**Рекомендации по улучшению**:

1.  **Добавить docstring для модуля**:
    - Описать назначение модуля и предоставить примеры использования.
2.  **Добавить аннотации типов**:
    - Указывать типы для всех переменных, чтобы повысить читаемость и упростить отладку.
3.  **Использовать `pathlib` вместо `os.path.join`**:
    - `pathlib` обеспечивает более современный и удобный способ работы с путями файлов.
4.  **Использовать модуль `src.logger.logger` для логирования**:
    - Это позволит унифицировать логирование во всем проекте.
5.  **Добавить документацию для методов**:
    - Описать параметры, возвращаемые значения и возможные исключения для каждого метода.
6.  **Добавить примеры использования в docstring**:
    - Это поможет пользователям понять, как использовать классы и функции.
7.  **Использовать одинарные кавычки**:
    - Привести все строки к использованию одинарных кавычек.
8.  **Улучшить структуру `Settings`**:
    - Изменить `model_config` на более явное объявление.
9. **Переименовать переменные**:
   -  `MRH_PASS_1, MRH_PASS_2` в более понятные имена, например, `MRH_PASSWORD_PART_1, MRH_PASSWORD_PART_2`.
10. **Использовать logger.error**:
    - При возникновении исключений использовать `logger.error` для логирования ошибок.

**Оптимизированный код**:

```python
"""
Модуль конфигурации Telegram-бота для Digital Market
=====================================================

Модуль содержит класс :class:`Settings`, который загружает параметры из переменных среды
и предоставляет методы для формирования URL вебхуков.

Пример использования
----------------------

>>> settings = Settings()
>>> print(settings.BOT_TOKEN)
>>> print(settings.get_webhook_url)
"""
import os
from typing import List
from src.logger.logger import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Класс настроек для Telegram-бота.

    Args:
        BOT_TOKEN (str): Токен бота, полученный от BotFather.
        ADMIN_IDS (List[int]): Список ID администраторов бота.
        PROVIDER_TOKEN (str): Токен провайдера платежей.
        FORMAT_LOG (str): Формат логов. По умолчанию "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}".
        LOG_ROTATION (str): Размер ротации логов. По умолчанию "10 MB".
        DB_URL (str): URL базы данных. По умолчанию 'sqlite+aiosqlite:///data/db.sqlite3'.
        SITE_URL (str): URL сайта.
        SITE_HOST (str): Хост сайта.
        SITE_PORT (int): Порт сайта.
        MRH_LOGIN (str): Логин MRH.
        MRH_PASS_1 (str): Пароль MRH часть 1.
        MRH_PASS_2 (str): Пароль MRH часть 2.
        IN_TEST (int): Флаг тестового режима.

    Returns:
        str: URL вебхука.

    Raises:
        ValueError: Если не удалось получить URL вебхука.

    Example:
        >>> settings = Settings()
        >>> print(settings.BOT_TOKEN)
        'токен_бота'
    """
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
        env_file=Path(__file__).resolve().parent.parent / '.env'
    )

    @property
    def get_webhook_url(self) -> str:
        """
        Формирует URL для вебхука на основе токена и URL сайта.

        Returns:
            str: URL вебхука.

        Example:
            >>> settings = Settings()
            >>> print(settings.get_webhook_url)
            'https://example.com/токен_бота'
        """
        return f"{self.SITE_URL}/{self.BOT_TOKEN}"

    @property
    def get_provider_hook_url(self) -> str:
        """
        Формирует URL для вебхука провайдера на основе URL сайта.

        Returns:
            str: URL вебхука провайдера.

        Example:
            >>> settings = Settings()
            >>> print(settings.get_provider_hook_url)
            'https://example.com/robokassa'
        """
        return f"{self.SITE_URL}/robokassa"


# Получаем параметры для загрузки переменных среды
settings: Settings = Settings()

# Инициализируем бота и диспетчер
bot: Bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp: Dispatcher = Dispatcher(storage=MemoryStorage())
admins: List[int] = settings.ADMIN_IDS

log_file_path: Path = Path(__file__).resolve().parent / "log.txt"
logger.add(str(log_file_path), format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url: str = settings.DB_URL