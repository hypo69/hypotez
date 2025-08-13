# # \file /src/fast_api/routes.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. Module :: SRC.FAST_API.ROUTES
	: Platform: Windows, Unix
	: synopsis: manipulating routes in the server"""

import header
from src.endpoints.bots.telegram.bot_handlers import BotHandler
class Routes:

	def tegram_message_handler(self):
		""""""
		bot_nahdlers = BotHandler()
		telega_message_handler = bot_nahdlers.handle_message
