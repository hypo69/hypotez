## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода инициализирует бота Telegram, настраивает логгирование и подключает базу данных. 

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек:** 
    - `os`: для работы с файловой системой.
    - `typing`: для аннотирования типов.
    - `loguru`: для логирования.
    - `aiogram`: для работы с Telegram API.
    - `pydantic_settings`: для загрузки настроек из файла `.env`.
2. **Определение класса Settings:** 
    - Класс `Settings` использует `pydantic_settings` для загрузки настроек из файла `.env`.
    - Определены следующие настройки: 
        - `BOT_TOKEN`: токен бота Telegram.
        - `ADMIN_IDS`: список ID администраторов бота.
        - `PROVIDER_TOKEN`: токен платежного провайдера.
        - `FORMAT_LOG`: формат логов.
        - `LOG_ROTATION`: размер файла логов.
        - `DB_URL`: URL базы данных.
        - `SITE_URL`: URL сайта.
        - `SITE_HOST`: хост сайта.
        - `SITE_PORT`: порт сайта.
        - `MRH_LOGIN`: логин для робокассы.
        - `MRH_PASS_1`: первый пароль для робокассы.
        - `MRH_PASS_2`: второй пароль для робокассы.
        - `IN_TEST`: флаг тестового режима.
    - Методы `get_webhook_url` и `get_provider_hook_url` динамически формируют пути для вебхуков.
3. **Загрузка настроек:**
    - `settings = Settings()` загружает настройки из файла `.env`.
4. **Инициализация бота:**
    - `bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))` создает экземпляр бота Telegram.
    - `dp = Dispatcher(storage=MemoryStorage())` создает экземпляр диспетчера для бота.
    - `admins = settings.ADMIN_IDS` сохраняет список ID администраторов бота.
5. **Настройка логгирования:**
    - `log_file_path`  - путь до файла логов.
    - `logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)` настраивает логгирование в файл.
6. **Настройка базы данных:**
    - `database_url = settings.DB_URL` сохраняет URL базы данных.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.config import settings

# Получаем токен бота
bot_token = settings.BOT_TOKEN

# Получаем URL сайта
site_url = settings.SITE_URL

# Получаем URL вебхука
webhook_url = settings.get_webhook_url

# Используем настройки для создания бота и диспетчера
# ...

# Используем настройки для подключения к базе данных
# ...

# Запускаем бота
# ...
```