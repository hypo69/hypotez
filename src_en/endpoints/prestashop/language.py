# # \file /src/endpoints/prestashop/language.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""`` `RST
    ..: modlue: src.endpoints.prestashop.language
`` `
Module for working with languages in Prestashop.
============================================================
The module represents the interface of interaction with the essence of `Language` in CMS` Prestashop` through `API Prestashop`"""
import asyncio
from types import SimpleNamespace

import header

from src import gs
from src.endpoints.prestashop.api import PrestaShop
from src.logger.exceptions import PrestaShopException
from src.utils.printer import pprint as print
from src.logger.logger import logger

from typing import Optional


class PrestaLanguage(PrestaShop):
    """The class responsible for setting up the languages of the Prestashop store.

    Example:
        >>> Prestalanguage = Prestalanguage (API_Domain = API_Domain, API_KEY = API_KEY)
        >>> PRESTALANGUAGE.Add_language_prestashop ('English', 'en')
        >>> PRESTALANGUAGE.DELETE_LANGUAGE_PRESTASHOP (3)
        >>> PRESTALANGUAGE.UPDATE_LANGUAGE_PRESTASHOP (4, 'Updated Language Name')
        >>> Print (Prestalaguage.get_language_details_prestashop (5))"""
    
    def __init__(self, *args, **kwargs):
        """Args:
            *Args: arbitrary arguments.
            ** kwargs: arbitrary named arguments.

        Note:
            It is important to remember that each store has its own numbering of languages.
            I define languages in my bases in this order:
            `en` - 1;
            `he` - 2;
            `ru` - 3."""
        ...

    def get_lang_name_by_index(self, lang_index: int | str) -> str:
        """The function extracts ISO Azika code from the store `Prestashop`

        Args:
            Lang_index: language index in the Prestashop table.

        Returns:
            ISO language name for its index in the Prestashop table."""
        try:
            return super().get('languagaes', resource_id=str(lang_index), display='full', io_format='JSON')
        except Exception as ex:
            logger.error(f'Ошибка получения языка по индексу {lang_index=}', ex)
            return ''

    def get_languages_schema(self) -> Optional[dict]:
        """The function extracts a dictionary of relevant languages of the DL of this store.

        Returns:
            Language Schema or `None` On Failure.

        Examples:
            # Return dictionary:
            {
                "Languages": {
                        "Language": [
                                        {
                                        "attrs": {
                                            "ID": "1"
                                        }
                                        "Value": ""
                                        }
                                        {
                                        "attrs": {
                                            "ID": "2"
                                        }
                                        "Value": ""
                                        }
                                        {
                                        "attrs": {
                                            "ID": "3"
                                        }
                                        "Value": ""
                                        }
                                    ]
                }
            }"""
        try:
            response = self._exec('languages', display='full', io_format='JSON')
            return response
        except Exception as ex:
            logger.error(f'Error:', ex)
            return


async def main():
    """Example:
        >>> asyncio.run(main())"""
    ...
    lang_class = PrestaLanguage()
    languagas_schema = await lang_class.get_languages_schema()
    print(languagas_schema)


if __name__ == '__main__':
    asyncio.run(main())
