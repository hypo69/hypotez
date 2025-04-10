### **Анализ кода модуля `bot_aiogram.py`**

## \file /src/endpoints/bots/telegram/bot_aiogram.py

Модуль представляет собой реализацию Telegram-бота с использованием фреймворка FastAPI для обработки входящих запросов через RPC. Он включает в себя настройку вебхуков, регистрацию обработчиков команд и обработку различных типов сообщений.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронности для обработки запросов.
  - Четкая структура класса `TelegramBot`.
  - Использование `j_loads_ns` для загрузки конфигурации.
  - Логирование с использованием модуля `logger`.
- **Минусы**:
  - Не все методы и функции имеют docstring.
  - Жестко заданные значения (например, порт 443).
  - Смешанный стиль кавычек (использованы и двойные, и одинарные).
  - Местами отсутствует аннотация типов.

**Рекомендации по улучшению:**

1.  **Добавить docstring**: Добавить docstring к методам `run`, `stop` и всем остальным, где они отсутствуют. Описать назначение каждого метода, принимаемые аргументы и возвращаемые значения.
2.  **Исправить стиль кавычек**: Привести весь код к использованию одинарных кавычек.
3.  **Добавить аннотации типов**: Добавить аннотации типов для переменных `port` в методе `__init__`.
4.  **Улучшить обработку ошибок**: Сделать обработку ошибок более специфичной, если это возможно.
5.  **Убрать дублирование кода**: Избавиться от дублирования кода, например, при формировании `webhook_url`.
6.  **Добавить комментарии**: Добавить комментарии к блокам кода, объясняющие их назначение.
7.  **Перевести комментарии**: Перевести все комментарии и docstring на русский язык.
8.  **Использовать `ex` вместо `e`**: В блоках обработки исключений использовать `ex` вместо `e`.
9. **Улучшить логирование**: Добавить `exc_info=True` при логировании ошибок.

**Оптимизированный код:**

```python
                # -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Телеграм бот через сервер FastAPI через RPC
====================================================

Модуль :mod:`src.endpoints.bots.telegram.telegram_webhooks`
:platform: Windows, Unix
:synopsis: Телеграм бот с сервером FAST API Через RPC

Пример использования
----------------------

>>> from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
>>> bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
>>> bot.run()
"""
import asyncio
import sys
from types import SimpleNamespace
from typing import Optional

import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from xmlrpc.client import ServerProxy

import header
from header import __root__
from src import gs
from src.endpoints.bots.telegram.bot_handlers import BotHandler
from src.logger.logger import logger

from src.utils.jjson import j_loads_ns


class TelegramBot:
    """
    Класс для управления Telegram ботом.
    Реализован как Singleton.
    """

    def __init__(self, token: str, route: str = 'telegram_webhook'):
        """
        Инициализация экземпляра TelegramBot.

        Args:
            token (str): Telegram bot token.
            route (str): Webhook route для FastAPI. По умолчанию '/telegram_webhook'.
        """
        self.token: str = token
        self.port: int = 443  # Порт для вебхука

        self.route: str = route
        self.config: SimpleNamespace = j_loads_ns(__root__ / 'src/endpoints/bots/telegram/telegram.json') # Загрузка конфигурации из JSON
        self.bot: Bot = Bot(token=self.token)
        self.dp: Dispatcher = Dispatcher()
        self.bot_handler: BotHandler = BotHandler()
        self._register_default_handlers()
        self.app: Optional[web.Application] = None
        self.rpc_client: Optional[ServerProxy] = None  # RPC клиент для взаимодействия с сервером

    def run(self) -> None:
        """
        Запуск бота, инициализация RPC и вебхука.
        """
        try:
            # Инициализация RPC клиента
            port: int = 9000

            self.rpc_client = ServerProxy(f'http://{gs.host}:{port}', allow_none=True)

            # Запуск сервера через RPC
            self.rpc_client.start_server(port, gs.host)

            # Регистрация маршрута через RPC
            logger.success(f'RPC Server running at http://{gs.host}:{port}/')
        except Exception as ex:
            logger.error('Ошибка FastApiServer: ', ex, exc_info=True)
            sys.exit()

        # Инициализация вебхука Telegram бота
        webhook_url: Optional[str] = self.initialize_bot_webhook(self.route)

        if webhook_url:
            self._register_route_via_rpc(self.rpc_client)
            try:
                # Использование веб-приложения для вебхука
                self.app = web.Application()
                webhook_requests_handler = SimpleRequestHandler(
                    dispatcher=self.dp,
                    bot=self.bot,
                )

                webhook_requests_handler.register(self.app, path=self.route)
                setup_application(self.app, self.dp, bot=self.bot)
                web.run_app(self.app, host='0.0.0.0', port=self.port)
                logger.info(f'Application started: {self.bot.id}')

            except Exception as ex:
                logger.error('Ошибка установки вебхука: ', ex, exc_info=True)

        else:
            asyncio.run(self.dp.start_polling(self.bot))

    def _register_default_handlers(self) -> None:
        """Регистрация стандартных обработчиков с использованием экземпляра BotHandler."""
        self.dp.message.register(self.bot_handler.start, Command('start'))
        self.dp.message.register(self.bot_handler.help_command, Command('help'))
        self.dp.message.register(self.bot_handler.send_pdf, Command('sendpdf'))
        self.dp.message.register(self._handle_message)
        self.dp.message.register(self.bot_handler.handle_voice, lambda message: message.voice is not None)
        self.dp.message.register(self.bot_handler.handle_document, lambda message: message.document is not None)
        self.dp.message.register(self.bot_handler.handle_log, lambda message: message.text is not None)

    async def _handle_message(self, message: types.Message) -> None:
        """Обработка любого текстового сообщения."""
        await self.bot_handler.handle_message(message)

    def initialize_bot_webhook(self, route: str) -> Optional[str]:
        """
        Инициализация вебхука бота.

        Args:
            route (str): Маршрут для вебхука.

        Returns:
            Optional[str]: URL вебхука или None в случае ошибки.
        """
        route = route if route.startswith('/') else f'/{route}'
        host = gs.host

        if host in ('127.0.0.1', 'localhost'):
            from pyngrok import ngrok
            ngrok.set_auth_token(os.getenv('NGROK_AUTH_TOKEN', ''))
            http_tunnel = ngrok.connect(self.port)
            host = http_tunnel.public_url

        host = host if host.startswith('http') else f'https://{host}'
        webhook_url = f'{host}{route}'

        try:
            asyncio.run(self.bot.set_webhook(url=webhook_url))
            logger.success(f'https://api.telegram.org/bot{self.token}/getWebhookInfo')
            return webhook_url
        except Exception as ex:
            logger.error(f'Error setting webhook: ', ex, exc_info=True)
            return False

    def _register_route_via_rpc(self, rpc_client: ServerProxy) -> None:
        """Регистрация маршрута вебхука Telegram через RPC."""
        try:
            route = self.route if self.route.startswith('/') else f'/{self.route}'
            rpc_client.add_new_route(
                route,
                'self.bot_handler.handle_message',
                ['POST']
            )
            logger.info(f'Route {self.route} registered via RPC.')
        except Exception as ex:
            logger.error('Failed to register route via RPC:', ex, exc_info=True)

    def stop(self) -> None:
        """Остановка бота и удаление вебхука."""
        if self.app:
            asyncio.run(self.app.shutdown())
            asyncio.run(self.app.cleanup())
        try:
            asyncio.run(self.bot.delete_webhook())
            logger.info('Bot stopped.')
        except Exception as ex:
            logger.error(f'Error deleting webhook:', ex, exc_info=True)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
    bot.run()