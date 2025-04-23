# Модуль конфигурации Telegram-бота для цифрового рынка

## Обзор

Модуль `config.py` предназначен для хранения и управления конфигурационными параметрами Telegram-бота, используемого для цифрового рынка. Он определяет класс `Settings`, который загружает параметры из переменных окружения и предоставляет удобный доступ к ним.

## Подробнее

Этот модуль играет важную роль в инициализации и настройке Telegram-бота. Он использует библиотеку `pydantic-settings` для загрузки параметров из `.env` файла и предоставляет методы для динамического формирования URL вебхуков. Модуль также инициализирует объекты `Bot` и `Dispatcher` из библиотеки `aiogram`, необходимые для работы бота.

## Классы

### `Settings`

**Описание**: Класс `Settings` используется для хранения конфигурационных параметров бота.

**Наследует**: `BaseSettings` из библиотеки `pydantic_settings`.

**Атрибуты**:

- `BOT_TOKEN` (str): Токен Telegram-бота.
- `ADMIN_IDS` (List[int]): Список ID администраторов бота.
- `PROVIDER_TOKEN` (str): Токен провайдера платежей (например, Robokassa).
- `FORMAT_LOG` (str): Формат логгирования (по умолчанию: "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}").
- `LOG_ROTATION` (str): Размер ротации лог-файлов (по умолчанию: "10 MB").
- `DB_URL` (str): URL базы данных (по умолчанию: 'sqlite+aiosqlite:///data/db.sqlite3').
- `SITE_URL` (str): URL сайта.
- `SITE_HOST` (str): Хост сайта.
- `SITE_PORT` (int): Порт сайта.
- `MRH_LOGIN` (str): Логин Merchant.
- `MRH_PASS_1` (str): Первый пароль Merchant.
- `MRH_PASS_2` (str): Второй пароль Merchant.
- `IN_TEST` (int): Флаг, указывающий на тестовый режим.

**Принцип работы**:

Класс `Settings` наследуется от `BaseSettings` и использует `SettingsConfigDict` для указания файла `.env`, из которого загружаются переменные окружения. Параметры загружаются при создании экземпляра класса. Также класс содержит property методы для динамического формирования URL вебхуков на основе загруженных параметров.

## Методы класса

### `get_webhook_url`

```python
def get_webhook_url(self) -> str:
    """Динамически формирует путь для вебхука на основе токена и URL сайта."""
    ...
```

**Назначение**: Динамически формирует URL для вебхука на основе токена бота и URL сайта.

**Параметры**:

- `self`: Экземпляр класса `Settings`.

**Возвращает**:

- `str`: URL вебхука.

**Как работает функция**:

Функция формирует URL, объединяя `SITE_URL` и `BOT_TOKEN`.

**Примеры**:

```python
settings = Settings()
webhook_url = settings.get_webhook_url
print(webhook_url)  # Пример: https://example.com/123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### `get_provider_hook_url`

```python
def get_provider_hook_url(self) -> str:
    """Динамически формирует путь для вебхука на основе токена и URL сайта."""
    ...
```

**Назначение**: Динамически формирует URL для вебхука провайдера платежей (например, Robokassa) на основе URL сайта.

**Параметры**:

- `self`: Экземпляр класса `Settings`.

**Возвращает**:

- `str`: URL вебхука провайдера.

**Как работает функция**:

Функция формирует URL, объединяя `SITE_URL` и `/robokassa`.

**Примеры**:

```python
settings = Settings()
provider_hook_url = settings.get_provider_hook_url
print(provider_hook_url)  # Пример: https://example.com/robokassa
```

## Переменные модуля

- `settings`: Экземпляр класса `Settings`, содержащий конфигурационные параметры.
- `bot`: Экземпляр класса `Bot` из библиотеки `aiogram`, инициализированный с использованием токена из `settings`.
- `dp`: Экземпляр класса `Dispatcher` из библиотеки `aiogram`, используемый для обработки входящих сообщений и событий.
- `admins`: Список ID администраторов бота, полученный из `settings.ADMIN_IDS`.
- `log_file_path`: Путь к файлу логов, формируется на основе директории текущего файла и имени "log.txt".
- `database_url`: URL базы данных, полученный из `settings.DB_URL`.

## Примеры

Инициализация бота и диспетчера:

```python
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from src.logger import logger
import os

# Инициализируем бота и диспетчер
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)