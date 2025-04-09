### **Анализ кода модуля `main.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на логические блоки (функции).
  - Используются асинхронные функции для неблокирующего выполнения задач.
  - Присутствует обработка исключений при отправке сообщений администраторам.
  - Код документирован с использованием docstring, что облегчает понимание его функциональности.
- **Минусы**:
  - Отсутствуют аннотации типов для параметров функций и возвращаемых значений.
  - Используется `Exception as e` вместо `Exception as ex` в блоках `try...except`.
  - Не все строки залогированы с использованием `logger` из `src.logger`.

#### **Рекомендации по улучшению**:
1. **Добавить аннотации типов**:
   - Для всех параметров функций и возвращаемых значений необходимо добавить аннотации типов. Это улучшит читаемость и позволит статическим анализаторам кода (например, MyPy) находить ошибки на ранних этапах разработки.

2. **Использовать `logger` для логирования**:
   - Добавьте логирование с использованием `logger` из `src.logger` для более детальной информации о работе приложения, особенно в функциях `set_default_commands`, `register_middlewares`, `register_routers` и `create_app`.
   - Обеспечить передачу ошибок через `logger.error(message, ex, exc_info=True)`.

3. **Исправить использование `e` на `ex`**:
   - В блоках `try...except` следует использовать `ex` вместо `e` для обозначения исключения.

4. **Добавить docstring в модуль**:
   - Добавить docstring в начале файла с описанием модуля.

#### **Оптимизированный код**:
```python
"""
Модуль для запуска Telegram-бота цифрового рынка.
====================================================

Этот модуль содержит основные функции для запуска и настройки Telegram-бота,
включая установку команд, регистрацию маршрутизаторов, мидлварей и обработку
вебхуков.

Пример использования:
----------------------
>>> python main.py
"""

from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger
from bot.app.app import handle_webhook, robokassa_result, robokassa_fail, home_page
from bot.config import bot, admins, dp, settings
from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit
from bot.admin.admin import admin_router
from bot.user.user_router import user_router
from bot.user.catalog_router import catalog_router
from typing import List


# Функция для установки команд по умолчанию для бота
async def set_default_commands() -> None:
    """
    Устанавливает команды по умолчанию для бота.
    """
    commands: List[BotCommand] = [BotCommand(command='start', description='Запустить бота')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    logger.info("Установлены команды по умолчанию для бота.")


# Функции для запуска и остановки бота
async def on_startup(app: web.Application) -> None:
    """
    Выполняется при запуске приложения.
    Устанавливает вебхук, отправляет сообщение администраторам и логирует запуск бота.

    Args:
        app (web.Application): Экземпляр приложения aiohttp.
    """
    await set_default_commands()
    await bot.set_webhook(settings.get_webhook_url)
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот запущен 🥳.')
        except Exception as ex:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {ex}", ex, exc_info=True)
    logger.info("Бот успешно запущен.")


async def on_shutdown(app: web.Application) -> None:
    """
    Выполняется при остановке приложения.
    Отправляет сообщение администраторам, удаляет вебхук и закрывает сессию бота.

    Args:
        app (web.Application): Экземпляр приложения aiohttp.
    """
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот остановлен. Почему? 😔')
        except Exception as ex:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {ex}", ex, exc_info=True)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logger.error("Бот остановлен!")


# Регистрация мидлварей и роутеров
def register_middlewares() -> None:
    """
    Регистрирует мидлвари для диспетчера.
    """
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    logger.info("Мидлвари зарегистрированы.")


def register_routers() -> None:
    """
    Регистрирует маршруты для диспетчера.
    """
    dp.include_router(catalog_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    logger.info("Роутеры зарегистрированы.")


# Функция для создания приложения aiohttp
def create_app() -> web.Application:
    """
    Создает и настраивает приложение aiohttp.
    """
    # Создаем приложение
    app: web.Application = web.Application()

    # Регистрация обработчиков маршрутов
    app.router.add_post(f"/{settings.BOT_TOKEN}", handle_webhook)
    app.router.add_post("/robokassa/result/", robokassa_result)
    app.router.add_get("/robokassa/fail/", robokassa_fail)
    app.router.add_get("/", home_page)

    # Настройка приложения с диспетчером и ботом
    setup_application(app, dp, bot=bot)

    # Регистрация функций запуска и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logger.info("Приложение aiohttp создано и настроено.")
    return app


# Главная функция
def main() -> None:
    """
    Главная функция для запуска приложения.
    """
    # Регистрация мидлварей и роутеров
    register_middlewares()
    register_routers()

    # Создаем приложение и запускаем его
    app: web.Application = create_app()
    web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)
    logger.info(f"Приложение запущено на хосте {settings.SITE_HOST}:{settings.SITE_PORT}")


if __name__ == "__main__":
    main()