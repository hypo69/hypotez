### **Анализ кода модуля `config.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `pydantic_settings` для управления настройками.
    - Разделение настроек и логики инициализации бота.
    - Динамическое формирование URL для вебхуков.
    - Инициализация логгера с ротацией файлов.
- **Минусы**:
    - Использование строк для формирования путей к файлам, что может привести к ошибкам.
    - Смешивание логики инициализации и конфигурации.
    - Не все переменные аннотированы типами.
    - Отсутствие обработки исключений при инициализации бота и диспетчера.
    - Использование устаревшего `loguru` вместо `src.logger.logger`.

**Рекомендации по улучшению**:

1.  **Использовать `Path` для работы с путями к файлам**:
    - Замените использование `os.path.join` на `Path` для более надежной работы с путями.
2.  **Перенести инициализацию логгера в отдельный модуль**:
    - Создайте отдельный модуль для инициализации логгера и используйте его в других модулях.
3.  **Добавить обработку исключений при инициализации бота и диспетчера**:
    - Добавьте блоки `try...except` для обработки исключений, которые могут возникнуть при инициализации бота и диспетчера.
4.  **Использовать f-строки для формирования строк**:
    - Используйте f-строки вместо конкатенации строк для формирования URL вебхуков.
5.  **Добавить docstring для класса `Settings` и его методов**:
    - Добавьте docstring для класса `Settings` и его методов, чтобы объяснить их назначение.
6.  **Использовать `src.logger.logger` вместо `loguru`**:
    - Замените использование `loguru` на `src.logger.logger` для соответствия стандартам проекта.
7.  **Добавить аннотации типов для всех переменных**:
    - Добавьте аннотации типов для всех переменных, чтобы улучшить читаемость и поддерживаемость кода.

**Оптимизированный код**:

```python
import os
from typing import List
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from src.logger import logger  # Используем logger из проекта


class Settings(BaseSettings):
    """
    Класс настроек для Telegram-бота.
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
        env_file=Path(__file__).parent.joinpath("..", ".env")
    )

    @property
    def get_webhook_url(self) -> str:
        """
        Формирует URL для вебхука на основе токена и URL сайта.
        """
        return f"{self.SITE_URL}/{self.BOT_TOKEN}"

    @property
    def get_provider_hook_url(self) -> str:
        """
        Формирует URL для вебхука на основе токена и URL сайта провайдера.
        """
        return f"{self.SITE_URL}/robokassa"


# Получаем параметры для загрузки переменных среды
settings: Settings = Settings()

# Инициализируем бота и диспетчер
try:
    bot: Bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher(storage=MemoryStorage())
    admins: List[int] = settings.ADMIN_IDS
except Exception as ex:
    logger.error('Error while initializing bot or dispatcher', ex, exc_info=True)

log_file_path: Path = Path(__file__).parent.joinpath("log.txt")
# Настраиваем логгер
logger.add(str(log_file_path), format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
database_url: str = settings.DB_URL