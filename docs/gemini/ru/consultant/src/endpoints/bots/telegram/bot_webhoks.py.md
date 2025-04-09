### **Анализ кода модуля `telegram_webhooks`**

## Качество кода:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `logger` для логирования.
  - Использование `j_loads_ns` для загрузки JSON-конфигурации.
  - Наличие обработки исключений.
  - Документация присутствует, но требует доработки.
- **Минусы**:
  - Не все функции и методы имеют docstring.
  - Отсутствуют аннотации типов для параметров и возвращаемых значений в некоторых местах.
  - Смешанный стиль кавычек (используются как двойные, так и одинарные).
  - В некоторых блоках `try...except` отсутствует обработка исключений (многоточие `...`).
  - Не все комментарии переведены на русский язык.

## Рекомендации по улучшению:

1. **Документирование кода**:
   - Добавить docstring для всех функций и методов, включая `_handle_message`, `initialize_bot_webhook`, `_register_route_via_rpc`, `stop`.
   - Перевести все docstring на русский язык и привести их к единому стандарту, указанному в инструкции.
   - Добавить примеры использования для ключевых функций.

2. **Аннотация типов**:
   - Добавить аннотации типов для параметров и возвращаемых значений всех функций и методов.
   - Убедиться, что все переменные также аннотированы типами.

3. **Использование кавычек**:
   - Привести все строки к единому стилю: использовать только одинарные кавычки (`'`).

4. **Обработка исключений**:
   - Заменить многоточия (`...`) в блоках `try...except` на конкретную обработку исключений или логирование ошибок с использованием `logger.error`.
   - Использовать переменную `ex` для исключений вместо `e`.

5. **Логирование**:
   - Убедиться, что все ошибки логируются с использованием `logger.error` и передачей исключения в качестве второго аргумента, а также с указанием `exc_info=True`.

6. **Комментарии**:
   - Перевести все комментарии на русский язык.
   - Сделать комментарии более информативными и конкретными, избегая общих фраз вроде "получаем" или "делаем".
   - Добавить комментарии к блокам кода, где это необходимо, для пояснения их назначения.

7. **Стиль кода**:
   - Следовать стандартам PEP8 для форматирования кода, включая добавление пробелов вокруг операторов присваивания.

8. **Использование `webdriver`**:
   - В данном коде не используется `webdriver`, но если бы использовался, следовало бы использовать `Driver`, `Chrome`, `Firefox`, `Playwright` из `src.webdriver`.

## Оптимизированный код:

```python
## \file /src/endpoints/bots/telegram/telegram_webhooks.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для работы с Телеграм ботом через сервер FastAPI через RPC
==================================================================

Модуль содержит класс :class:`TelegramBot`, который реализует Телеграм бота, управляемого через сервер FastAPI с использованием RPC.
"""
from pathlib import Path
import asyncio
import json
import sys
from types import SimpleNamespace
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from xmlrpc.client import ServerProxy
from fastapi import FastAPI, Request, Response
import socket
import os

import header
from header import __root__
from src import gs
from src.endpoints.bots.telegram.handlers import BotHandler
from src.utils.printer import pprint as print
from src.logger.logger import logger

from src.utils.jjson import j_loads_ns


class TelegramBot:
    """
    Класс для управления Telegram ботом. Реализован как Singleton.
    """

    def __init__(self, token: str, route: str = 'telegram_webhook'):
        """
        Инициализация экземпляра класса TelegramBot.

        Args:
            token (str): Токен Telegram бота.
            route (str): Webhook route для FastAPI. По умолчанию '/telegram_webhook'.
        """
        self.token: str = token
        self.port: int = 443
        self.route: str = route
        self.config: SimpleNamespace = j_loads_ns(__root__ / 'src/endpoints/bots/telegram/telegram.json')
        self.application: Application = Application.builder().token(self.token).build()
        self.handler: BotHandler = BotHandler()
        self._register_default_handlers()

    def run(self) -> None:
        """
        Запускает бота, инициализирует RPC и webhook.
        """
        try:
            # Инициализация RPC клиента
            rpc_client = ServerProxy(f'http://{gs.host}:9000', allow_none=True)

            # Запуск сервера через RPC
            rpc_client.start_server(self.port, gs.host)

            # Регистрация маршрута через RPC
            # Динамическое добавление маршрутов
            logger.success(f'Server running at http://{gs.host}:{self.port}/hello')
        except Exception as ex:
            logger.error(f'Ошибка FastApiServer: {ex}', exc_info=True)
            sys.exit()

        # Инициализация Telegram bot webhook
        webhook_url = self.initialize_bot_webhook(self.route)
        # 
        if webhook_url:
            self._register_route_via_rpc(rpc_client)
            try:
                self.application.run_webhook(listen='0.0.0.0',
                                                         webhook_url=webhook_url, 
                                                         port=self.port)
                
                logger.info(f'Application started: {self.application.bot_data}')

            except Exception as ex:
                logger.error('Ошибка установки вебхука', ex, exc_info=True)

        else:
            self.application.run_polling()

    def _register_default_handlers(self) -> None:
        """
        Регистрирует обработчики по умолчанию, используя экземпляр класса BotHandler.
        """
        self.application.add_handler(CommandHandler('start', self.handler.start))
        self.application.add_handler(CommandHandler('help', self.handler.help_command))
        self.application.add_handler(CommandHandler('sendpdf', self.handler.send_pdf))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handler.handle_voice))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handler.handle_document))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.handle_log))

    async def _handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Обрабатывает любое текстовое сообщение.

        Args:
            update (Update): Объект Update от Telegram.
            context (CallbackContext): Контекст обратного вызова.
        """
        await self.handler.handle_message(update, context)

    def initialize_bot_webhook(self, route: str) -> str | bool:
        """
        Инициализирует webhook для бота.

        Args:
            route (str): Маршрут для webhook.

        Returns:
            str | bool: URL webhook в случае успеха, False в случае ошибки.
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

        _dev = True
        if _dev:
            import requests
            response = requests.post(f'{webhook_url}')
            print(response.json, text_color='green', bg_color='gray')

        try:
            self.application.bot.set_webhook(url=webhook_url)
            logger.success(f'https://api.telegram.org/bot{self.token}/getWebhookInfo')
            return webhook_url
        except Exception as ex:
            logger.error(f'Error setting webhook: ',ex, exc_info=True)
            return False

    def _register_route_via_rpc(self, rpc_client: ServerProxy) -> None:
        """
        Регистрирует маршрут Telegram webhook через RPC.

        Args:
            rpc_client (ServerProxy): RPC клиент.
        """
        try:
            # Регистрация маршрута через RPC
            route = self.route if self.route.startswith('/') else f'/{self.route}'
            rpc_client.add_new_route(
                route,
                'self.bot_handler.handle_message',
                ['POST']
            )

            logger.info(f'Route {self.route} registered via RPC.')
        except Exception as ex:
            logger.error(f'Failed to register route via RPC:',ex, exc_info=True)

    def stop(self) -> None:
        """
        Останавливает бота и удаляет webhook.
        """
        try:
            self.application.stop()
            self.application.bot.delete_webhook()
            logger.info('Bot stopped.')
        except Exception as ex:
            logger.error(f'Error deleting webhook:',ex, exc_info=True)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
    bot.run()