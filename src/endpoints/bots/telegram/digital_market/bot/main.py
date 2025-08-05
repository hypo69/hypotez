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


# Функция для установки команд по умолчанию для бота
async def set_default_commands():
    """
    Устанавливает команды по умолчанию для бота.
    """
    commands = [BotCommand(command='start', description='Запустить бота')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функции для запуска и остановки бота
async def on_startup(app):
    """
    Выполняется при запуске приложения.
    """
    await set_default_commands()
    await bot.set_webhook(settings.get_webhook_url)
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот запущен 🥳.')
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    logger.info("Бот успешно запущен.")


async def on_shutdown(app):
    """
    Выполняется при остановке приложения.
    """
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот остановлен. Почему? 😔')
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logger.error("Бот остановлен!")


# Регистрация мидлварей и роутеров
def register_middlewares():
    """
    Регистрирует мидлвари для диспетчера.
    """
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())


def register_routers():
    """
    Регистрирует маршруты для диспетчера.
    """
    dp.include_router(catalog_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)


# Функция для создания приложения aiohttp
def create_app():
    """
    Создает и настраивает приложение aiohttp.
    """
    # создание приложение
    app = web.Application()

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

    return app


# Главная функция
def main():
    """
    Главная функция для запуска приложения.
    """
    # Регистрация мидлварей и роутеров
    register_middlewares()
    register_routers()

    # создание приложение и запускаем его
    app = create_app()
    web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)


if __name__ == "__main__":
    main()
