# Модуль конфигурации бота Telegram

## Обзор

Этот модуль содержит конфигурацию для бота Telegram, работающего в рамках проекта `hypotez`. Он определяет настройки для взаимодействия с ботом, 
включая:

- Токен бота (`BOT_TOKEN`)
- ID администраторов (`ADMIN_IDS`)
- Токен провайдера платежей (`PROVIDER_TOKEN`)
- Настройки логирования (`FORMAT_LOG`, `LOG_ROTATION`)
- Настройки базы данных (`DB_URL`)
- Настройки сайта (`SITE_URL`, `SITE_HOST`, `SITE_PORT`)
- Логины и пароли для работы с MRH (`MRH_LOGIN`, `MRH_PASS_1`, `MRH_PASS_2`)
- Флаг для тестового режима (`IN_TEST`)

## Классы

### `class Settings`

**Описание**: Класс `Settings` используется для хранения и управления настройками бота. 
Он наследует от `BaseSettings` и загружает настройки из файла `.env`.

**Атрибуты**:

- `BOT_TOKEN (str)`: Токен бота Telegram.
- `ADMIN_IDS (List[int])`: Список ID администраторов.
- `PROVIDER_TOKEN (str)`: Токен провайдера платежей.
- `FORMAT_LOG (str)`: Формат лог-файла. 
- `LOG_ROTATION (str)`: Настройки для ротации лог-файлов.
- `DB_URL (str)`: URL базы данных.
- `SITE_URL (str)`: URL сайта.
- `SITE_HOST (str)`: Хост сайта.
- `SITE_PORT (int)`: Порт сайта.
- `MRH_LOGIN (str)`: Логин для работы с MRH.
- `MRH_PASS_1 (str)`: Первый пароль для работы с MRH.
- `MRH_PASS_2 (str)`: Второй пароль для работы с MRH.
- `IN_TEST (int)`: Флаг для тестового режима.

**Методы**:

- `get_webhook_url()`: Возвращает URL вебхука для бота.
- `get_provider_hook_url()`: Возвращает URL вебхука для провайдера платежей.

## Пример использования

```python
from src.endpoints.bots.telegram.digital_market.bot.config import Settings

# Загрузка настроек
settings = Settings()

# Получение токена бота
bot_token = settings.BOT_TOKEN

# Получение URL вебхука
webhook_url = settings.get_webhook_url()

# Вывод настроек
print(f"Токен бота: {bot_token}")
print(f"URL вебхука: {webhook_url}")
```

## Параметры класса

- `BOT_TOKEN` (str): Токен бота Telegram.
- `ADMIN_IDS` (List[int]): Список ID администраторов.
- `PROVIDER_TOKEN` (str): Токен провайдера платежей.
- `FORMAT_LOG` (str): Формат лог-файла. 
- `LOG_ROTATION` (str): Настройки для ротации лог-файлов.
- `DB_URL` (str): URL базы данных.
- `SITE_URL` (str): URL сайта.
- `SITE_HOST` (str): Хост сайта.
- `SITE_PORT` (int): Порт сайта.
- `MRH_LOGIN` (str): Логин для работы с MRH.
- `MRH_PASS_1` (str): Первый пароль для работы с MRH.
- `MRH_PASS_2` (str): Второй пароль для работы с MRH.
- `IN_TEST` (int): Флаг для тестового режима.

## Примеры

```python
# Создание экземпляра класса Settings
settings = Settings()

# Вывод токена бота
print(f"Токен бота: {settings.BOT_TOKEN}")

# Вывод URL вебхука
print(f"URL вебхука: {settings.get_webhook_url()}")
```

##  Инициализация бота и диспетчера

```python
# Инициализация бота
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Инициализация диспетчера
dp = Dispatcher(storage=MemoryStorage())

# Список администраторов
admins = settings.ADMIN_IDS

# Путь к лог-файлу
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")

# Добавление логгера
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)

# URL базы данных
database_url = settings.DB_URL