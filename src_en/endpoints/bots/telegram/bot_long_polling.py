# -*- coding: utf-8 -*-
# parent_bot.py
import os
from pathlib import Path
import tempfile
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext,  CallbackQueryHandler
from typing import Callable

import header
from src.endpoints.bots.telegram.handlers import BotHandler
from src.logger.logger import logger
import requests  # For downloading files
from src.utils.convertors.tts import speech_recognizer, text2speech
from src.utils.file import read_text_file


class TelegramBot:
    """Telegram bot interface class."""

    application: Application
    handler: BotHandler
    def __init__(self, token: str):
        """initialized the telegram bot.

        Args:
            Token (STR): Telegram Bot Token, E.G., `gs.credentials.telegrapher.bot.kazarinov`."""
        self.application = Application.builder().token(token).build()
        self.handler = BotHandler() # Initialization The Manufacturer in Constructor
        self._original_message_handler = None
        self.register_handlers()


    def register_handlers(self) -> None:
        """Register bot commands and message handlers."""
        self.application.add_handler(CommandHandler('start', self.handler.start))
        self.application.add_handler(CommandHandler('help', self.handler.help_command))
        self.application.add_handler(CommandHandler('sendpdf', self.handler.send_pdf))

        # We keep the link
        self._original_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.handle_message)
        self.application.add_handler(self._original_message_handler)

        self.application.add_handler(MessageHandler(filters.VOICE, self.handler.handle_voice))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handler.handle_document))
    
    def replace_message_handler(self, new_handler: Callable) -> None:
        """Replaces the current processor of text messages for a new one.

        Args:
            New_HANDLER (CALLABLE): A new function for processing messages."""
        # 2. Delete the old handler
        if self._original_message_handler in self.application.handlers[0]:
            self.application.handlers[0].remove(self._original_message_handler)

        # 3. Create a new handler
        self._original_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, new_handler)
        # 4. We register a new handler
        self.application.add_handler(self._original_message_handler)



    async def start(self, update: Update, context: CallbackContext) -> None:
        """Handle the /start command."""
        logger.info(f"Bot started by user {update.effective_user.id}")
        await update.message.reply_text('Hello! I am your simple bot. Type /help to see available commands.')