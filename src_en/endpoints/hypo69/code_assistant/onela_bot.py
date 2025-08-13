# # \file /src/endpoints/hypo69/code_assistant/onela_bot.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

"""Module: src.endpoints.hypo69.code_assistant.onela_bot
	: Platform: Windows, Unix
	: synopsis: a dialogue module with a model of an assistant programmer through a telegram chat. 

Module for interacting with the model of the assistant programmer through the Telegram chat
======================================================================================ward

The module contains the class: Class: `ONELABOT`, which is used to process text messages and documents."""

import header
import asyncio
from pathlib import Path
from typing import List, Optional, Dict
from types import SimpleNamespace
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from src import gs
from src.llm.openai import OpenAIModel
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.bots.telegram import TelegramBot
from src.logger.logger import logger


class OnelaBot(TelegramBot):
    """Interaction with the model of the assistant programmer."""

    model: GoogleGenerativeAi = GoogleGenerativeAi(
        api_key = gs.credentials.gemini.onela,
        generation_config = {'response_mime_type': 'text/plain'}
    )

    def __init__(self) -> None:
        """Initialization of the ONELABOT object."""
        super().__init__(gs.credentials.telegram.onela_bot)

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Processing of text messages.

        Args:
            Update (Update): Telegram updates data.
            CONTEXT (CallbackContext): Context of execution."""
        q: str = update.message.text
        user_id: int = update.effective_user.id
        try:
            # Get a response from the model
            answer: str = await self.model.chat(q)
            await update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки текстового сообщения: ', ex)
            ...

    async def handle_document(self, update: Update, context: CallbackContext) -> None:
        """Processing of loaded documents.

        Args:
            Update (Update): Telegram updates data.
            CONTEXT (CallbackContext): Context of execution."""
        try:
            file = await update.message.document.get_file()
            tmp_file_path: Path = await file.download_to_drive()  # The file is locally saving
            answer: str = await update.message.reply_text(file)
            update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки документа: ', ex)
            ...


if __name__ == '__main__':
    bot = OnelaBot()
    asyncio.run(bot.application.run_polling())

