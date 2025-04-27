# Модуль конфигурации Telegram-бота
## Overview
Модуль `config.py` предназначен для настройки Telegram-бота, используемого для взаимодействия с пользователями и выполнения различных задач, связанных с цифровым маркетингом. 

## Details
Модуль содержит класс `Settings`, который загружает конфигурационные параметры из файла `.env`. 

## Classes
### `Settings`

**Description**: Класс `Settings` используется для загрузки и хранения конфигурационных параметров бота.

**Inherits**: `pydantic_settings.BaseSettings`

**Attributes**:
- `BOT_TOKEN` (str): Токен доступа к Telegram API.
- `ADMIN_IDS` (List[int]): Список идентификаторов администраторов бота.
- `PROVIDER_TOKEN`: (str): Токен для работы с платежным шлюзом Robokassa.
- `FORMAT_LOG` (str): Формат логгирования.
- `LOG_ROTATION` (str): Настройки ротации лог-файлов.
- `DB_URL` (str): URL базы данных.
- `SITE_URL` (str): URL сайта.
- `SITE_HOST` (str): Хост сайта.
- `SITE_PORT` (int): Порт сайта.
- `MRH_LOGIN` (str): Логин для входа в систему Merchant.
- `MRH_PASS_1` (str): Первый пароль для входа в систему Merchant.
- `MRH_PASS_2` (str): Второй пароль для входа в систему Merchant.
- `IN_TEST` (int): Флаг, указывающий на то, что бот работает в тестовом режиме.

**Methods**:
- `get_webhook_url()`: Динамически формирует путь для вебхука на основе токена и URL сайта.
- `get_provider_hook_url()`: Динамически формирует путь для вебхука для работы с платежным шлюзом.

## Functions

### `settings`

**Purpose**: Создание экземпляра класса `Settings` для загрузки конфигурационных параметров из файла `.env`.

**How the Function Works**:
1. `settings = Settings()` - создает экземпляр класса `Settings`.

**Examples**:
```python
settings = Settings()
print(settings.BOT_TOKEN)
```

### `bot`

**Purpose**: Инициализация экземпляра Telegram бота с использованием полученных конфигурационных параметров.

**How the Function Works**:
1. `bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))` - инициализирует бота с использованием токена из `settings` и устанавливает режим парсинга HTML.

**Examples**:
```python
print(bot) 
```

### `dp`

**Purpose**: Инициализация экземпляра диспетчера для обработки событий Telegram бота.

**How the Function Works**:
1. `dp = Dispatcher(storage=MemoryStorage())` - создает диспетчер с использованием `MemoryStorage` для хранения состояния бота.

**Examples**:
```python
print(dp)
```

### `admins`

**Purpose**: Получение списка идентификаторов администраторов бота.

**How the Function Works**:
1. `admins = settings.ADMIN_IDS` - извлекает список идентификаторов из `settings`.

**Examples**:
```python
print(admins)
```

### `logger`

**Purpose**: Инициализация логгера для записи информации о работе бота в файл.

**How the Function Works**:
1. `logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)` - настраивает логгер для записи в файл `log.txt`, задает формат логов, уровень логирования и настройки ротации.

**Examples**:
```python
logger.info('Some information message')
```

### `database_url`

**Purpose**: Получение URL базы данных, хранящегося в `settings`.

**How the Function Works**:
1. `database_url = settings.DB_URL` - извлекает URL базы данных из `settings`.

**Examples**:
```python
print(database_url)
```

## Parameter Details
- `BOT_TOKEN` (str): Токен доступа к Telegram API.
- `ADMIN_IDS` (List[int]): Список идентификаторов администраторов бота.
- `PROVIDER_TOKEN`: (str): Токен для работы с платежным шлюзом Robokassa.
- `FORMAT_LOG` (str): Формат логгирования.
- `LOG_ROTATION` (str): Настройки ротации лог-файлов.
- `DB_URL` (str): URL базы данных.
- `SITE_URL` (str): URL сайта.
- `SITE_HOST` (str): Хост сайта.
- `SITE_PORT` (int): Порт сайта.
- `MRH_LOGIN` (str): Логин для входа в систему Merchant.
- `MRH_PASS_1` (str): Первый пароль для входа в систему Merchant.
- `MRH_PASS_2` (str): Второй пароль для входа в систему Merchant.
- `IN_TEST` (int): Флаг, указывающий на то, что бот работает в тестовом режиме.

## Examples
```python
# Import the necessary modules
import os
from typing import List
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the Settings class
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


# Получаем параметры для загрузки переменных среды
settings = Settings()

# Инициализируем бота и диспетчер
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
admins = settings.ADMIN_IDS

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url = settings.DB_URL

```