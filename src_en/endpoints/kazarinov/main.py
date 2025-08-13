# # \file /src/endpoints/kazarinov/main.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""`` `RST
.. Module :: src.endpoints.kazarinov 
`` `

Service module for Sergey Kazarinov
==========================================================
Kazarinov collects components for assembly of company from suppliers' sites,
Combines them in Onetab and sends a bottle of created link.
The bot launches the script for collecting information from webstraks.
The script connects quotation_builder to create the final price -item


[Documentation `minibot`] (https://github.com/hypo69/hypotez/blob/master/docs/ru/src/endpoints/kazarinov/minibot.py.py.md)
[Documentation `Scenario`] (https://github.com/hypo69/hypotez/blob/master/docs/en/src/enpoints/kazarinov/scenarios/scenario.py.md)
[Documentation `quotation_Builder`] (https://github.com/hypo69/hypotez/blob/master/docs/src/Sendpoints/kazarinov/scenarios/quotation_builder.py.py.py.md)"""
import asyncio
import header
from src.endpoints.kazarinov.minibot import main

if __name__ == "__main__":
	main()