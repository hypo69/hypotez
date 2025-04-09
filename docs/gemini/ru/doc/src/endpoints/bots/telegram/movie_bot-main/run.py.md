# Модуль запуска Telegram-бота

## Обзор

Модуль `run.py` является точкой входа для запуска Telegram-бота. Он инициализирует и запускает бота, используя библиотеку `aiogram`. Модуль загружает переменные окружения из файла `.dotenv`, настраивает диспетчер (`Dispatcher`), регистрирует маршрутизаторы (`router`) и запускает процесс опроса (`polling`) для обработки входящих сообщений.

## Подробнее

Этот модуль предназначен для запуска Telegram-бота и обработки входящих сообщений. Он использует библиотеку `aiogram` для взаимодействия с Telegram API. Модуль загружает переменные окружения из файла `.dotenv`, настраивает диспетчер (`Dispatcher`), регистрирует маршрутизаторы (`router`) и запускает процесс опроса (`polling`) для обработки входящих сообщений.

## Функции

### `main`

**Назначение**: Асинхронная функция для инициализации и запуска Telegram-бота.

**Параметры**:

-   отсутствуют

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создает экземпляр бота (`Bot`) с использованием токена, полученного из переменной окружения `TOKEN`.
2.  Регистрирует промежуточное ПО (`middleware`) для управления частотой запросов (`ThrottlingMiddleware`).
3.  Включает маршрутизатор (`router`), который содержит обработчики сообщений.
4.  Запускает процесс опроса (`start_polling`) для получения и обработки входящих сообщений.

**Примеры**:

```python
import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from apps.hendlers import router
from middlewares.throttling import ThrottlingMiddleware

async def main() -> None:
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.message.middleware(ThrottlingMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())
```

## Переменные

### `dp`

**Описание**: Диспетчер (`Dispatcher`) для обработки входящих сообщений.

```python
dp = Dispatcher()
```