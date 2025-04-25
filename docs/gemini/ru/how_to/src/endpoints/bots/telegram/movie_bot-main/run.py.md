## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код запускает Telegram-бота, используя библиотеку `aiogram`. Он настраивает бота, добавляет обработчики сообщений, запускает механизм опроса (polling) и обрабатывает ошибки.

Шаги выполнения
-------------------------
1. **Загрузка переменных окружения**: 
    - Использует `load_dotenv()` для загрузки переменных окружения из файла `.env`.
2. **Создание диспетчера**:
    - Создает экземпляр `Dispatcher` - объекта для обработки входящих сообщений.
3. **Создание бота**: 
    - Создает экземпляр `Bot` с помощью токена из переменной окружения `TOKEN`.
4. **Добавление middleware**:
    - Добавляет middleware `ThrottlingMiddleware` в обработчик сообщений (`dp.message`). 
5. **Включение маршрутизатора**: 
    - Использует `dp.include_router` для добавления маршрутизатора `router`, который содержит обработчики для различных команд и сообщений.
6. **Запуск механизма опроса**:
    - Запускает механизм опроса (polling) с помощью `dp.start_polling(bot)`. 
7. **Обработка ошибок**:
    - В блоке `try-except` обрабатывает ошибки, возникшие при выполнении кода.

Пример использования
-------------------------
```python
import asyncio
import betterlogging as logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from apps.hendlers import router
from middlewares.throttling import ThrottlingMiddleware

# Загружаем переменные окружения из .env
load_dotenv()

# Создаем диспетчер
dp = Dispatcher()

# Запускаем бота
async def main() -> None:
    bot = Bot(os.getenv('TOKEN'))
    # Добавляем middleware
    dp.message.middleware(ThrottlingMiddleware())
    # Включаем маршрутизатор
    dp.include_router(router)
    # Запускаем механизм опроса
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Настраиваем логгирование
    logging.basic_colorized_config(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(name)s - '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
        datefmt='%H:%M:%S'
    )
    # Запускаем бота
    asyncio.run(main())

```

**Рекомендации**

*  **Переменные окружения**: Рекомендуется использовать `.env` файл для хранения токена доступа к боту. Это позволяет хранить конфиденциальные данные отдельно от кода.
* **Обработка ошибок**: Добавьте  `logging` для более подробного  просмотра ошибок, чтобы легче отслеживать и исправлять ошибки. 
* **Документация**: Добавьте  более подробную документацию  к  `router`,  `ThrottlingMiddleware`  и  другим  элементам  кода.