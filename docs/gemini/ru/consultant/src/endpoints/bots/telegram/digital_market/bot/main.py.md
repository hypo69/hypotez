### **Анализ кода модуля `main.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код разбит на отдельные функции, что улучшает читаемость и поддержку.
    - Используются `async` функции для асинхронной обработки, что важно для ботов.
    - Присутствует обработка ошибок при отправке сообщений администраторам.
    - Есть функции для регистрации middlewares и routers.
- **Минусы**:
    - Отсутствуют аннотации типов для аргументов и возвращаемых значений функций.
    - Не используется `logger` из `src.logger` для логирования ошибок в функциях `on_startup` и `on_shutdown`.
    - В docstring отсутсвует параметр `Args` и `Return`.
    - Не используются одинарные кавычки.

#### **Рекомендации по улучшению**:
- Добавить аннотации типов для всех функций и переменных, чтобы улучшить читаемость и облегчить отладку.
- Использовать `logger` из `src.logger` для логирования ошибок вместо `print`.
- Привести строки к одинарным кавычкам.
- Добавить полные docstring к каждой функции (включая описание аргументов, возвращаемых значений и возможных исключений).

#### **Оптимизированный код**:
```python
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from aiogram.types import BotCommand, BotCommandScopeDefault
from src.logger.logger import logger  # Используем logger из src.logger
from bot.app.app import handle_webhook, robokassa_result, robokassa_fail, home_page
from bot.config import bot, admins, dp, settings
from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit
from bot.admin.admin import admin_router
from bot.user.user_router import user_router
from bot.user.catalog_router import catalog_router


# Функция для установки команд по умолчанию для бота
async def set_default_commands() -> None:
    """
    Устанавливает команды по умолчанию для бота.
    """
    commands: list[BotCommand] = [BotCommand(command='start', description='Запустить бота')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функции для запуска и остановки бота
async def on_startup(app: web.Application) -> None:
    """
    Выполняется при запуске приложения.

    Args:
        app (web.Application): Веб-приложение aiohttp.

    Returns:
        None

    Raises:
        Exception: Если не удается отправить сообщение администратору.
    """
    await set_default_commands()
    await bot.set_webhook(settings.get_webhook_url)
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот запущен 🥳.')
        except Exception as ex:
            logger.error(f'Не удалось отправить сообщение админу {admin_id}', ex, exc_info=True)
    logger.info('Бот успешно запущен.')


async def on_shutdown(app: web.Application) -> None:
    """
    Выполняется при остановке приложения.

    Args:
        app (web.Application): Веб-приложение aiohttp.

    Returns:
        None

    Raises:
        Exception: Если не удается отправить сообщение администратору.
    """
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот остановлен. Почему? 😔')
        except Exception as ex:
            logger.error(f'Не удалось отправить сообщение админу {admin_id}', ex, exc_info=True)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logger.error('Бот остановлен!')


# Регистрация мидлварей и роутеров
def register_middlewares() -> None:
    """
    Регистрирует мидлвари для диспетчера.

    Args:
        None

    Returns:
        None
    """
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())


def register_routers() -> None:
    """
    Регистрирует маршруты для диспетчера.

    Args:
        None

    Returns:
        None
    """
    dp.include_router(catalog_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)


# Функция для создания приложения aiohttp
def create_app() -> web.Application:
    """
    Создает и настраивает приложение aiohttp.

    Args:
        None

    Returns:
        web.Application: Сконфигурированное веб-приложение aiohttp.
    """
    # Создаем приложение
    app: web.Application = web.Application()

    # Регистрация обработчиков маршрутов
    app.router.add_post(f'/{settings.BOT_TOKEN}', handle_webhook)
    app.router.add_post('/robokassa/result/', robokassa_result)
    app.router.add_get('/robokassa/fail/', robokassa_fail)
    app.router.add_get('/', home_page)

    # Настройка приложения с диспетчером и ботом
    setup_application(app, dp, bot=bot)

    # Регистрация функций запуска и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


# Главная функция
def main() -> None:
    """
    Главная функция для запуска приложения.

    Args:
        None

    Returns:
        None
    """
    # Регистрация мидлварей и роутеров
    register_middlewares()
    register_routers()

    # Создаем приложение и запускаем его
    app: web.Application = create_app()
    web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)


if __name__ == '__main__':
    main()