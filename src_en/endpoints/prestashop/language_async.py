# # \file /src/endpoints/prestashop/language.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.prestashop 
	:platform: Windows, Unix
	:synopsis:"""
import asyncio
from types import SimpleNamespace

import header

from src import gs
from src.endpoints.prestashop.api import PrestaShopAsync
from src.logger.exceptions import PrestaShopException
from src.utils.printer import  pprint as print
from src.logger.logger import logger

from typing import Optional

class PrestaLanguageAync(PrestaShopAsync):
    """The class responsible for setting up the languages of the Prestashop store.

    Example of class use:

    .. Code-Block :: Python

        Prestalanguage = Prestalanguage (API_Domain = API_Domain, API_KEY = API_KEY)
        Prestalaguage.add_language_prestashop ('English', 'en')
        Prestalaguage.delete_language_prestashop (3)
        Prestalaguage.update_language_prestashop (4, 'Updated Language Name')
        Print (Prestalaguage.get_language_details_prestashop (5))"""
    
    def __init__(self, *args, **kwargs):
        """Class interface interaction in Prestashop
        It is important to remember that each store has its own numbering of languages
        : Lang_string: ISO Language Names. For example: en, ru, he"""
        ...

    async def get_lang_name_by_index(self, lang_index:int|str ) -> str:
        """Returns the name of the ISO language by its index in the Prestashop table"""
        try:
            return super().get('languagaes', resource_id=str(lang_index), display='full', io_format='JSON')
        except Exception as ex:
            logger.error(f"Ошибка получения языка по индексу {lang_index=}", ex)
            return ''

        """Returns the language number from the Prestashop table by his name ISO"""
        ...
        
    async def get_languages_schema(self) -> dict:
        lang_dict = super().get_languages_schema()
        print(lang_dict) 


async def main():
    """"""
    ...
    lang_class = PrestaLanguageAync()
    languagas_schema = await  lang_class.get_languages_schema()
    print(languagas_schema)

if __name__ == '__main__':
    asyncio.run(main())

    
            

