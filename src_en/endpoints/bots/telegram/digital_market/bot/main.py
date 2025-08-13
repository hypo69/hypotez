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


# Function for installing the default commands for the bot
async def set_default_commands():
    """Installs the default commands for the bot."""
    commands = [BotCommand(command='start', description='Запустить бота')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Functions for launching and stopping the bot
async def on_startup(app):
    """It is performed when the application is launched."""
    await set_default_commands()
    await bot.set_webhook(settings.get_webhook_url)
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот запущен 🥳.')
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    logger.info("Бот успешно запущен.")


async def on_shutdown(app):
    """It is performed when the application stops."""
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот остановлен. Почему? 😔')
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logger.error("Бот остановлен!")


# Registration of midlugers and routers
def register_middlewares():
    """Recording Midlvari for the dispatcher."""
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())


def register_routers():
    """Recording routes for the dispatcher."""
    dp.include_router(catalog_router)
    dp.include_router(user_router)
    dp.include_router(admin_router)


# Function for creating the Aiohttp application
def create_app():
    """Creates and sets up the Aiohttp application."""
    # Creating an application
    app = web.Application()

    # Registration of route handlers
    app.router.add_post(f"/{settings.BOT_TOKEN}", handle_webhook)
    app.router.add_post("/robokassa/result/", robokassa_result)
    app.router.add_get("/robokassa/fail/", robokassa_fail)
    app.router.add_get("/", home_page)

    # Setting up an application with a dispatcher and a bot
    setup_application(app, dp, bot=bot)

    # Registration of starting and stopping functions
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


# The main function
def main():
    """The main function for starting the application."""
    # Registration of midlugers and routers
    register_middlewares()
    register_routers()

    # creation of the application and launch it
    app = create_app()
    web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)


if __name__ == "__main__":
    main()
