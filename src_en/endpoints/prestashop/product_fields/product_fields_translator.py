# # \file /src/product/product_fields/product_fields_translator.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: SRC.Product.product_fields 
	: Platform: Windows, Unix
	: synopsis: a module for transferring goods of goods to a client database"""


from pathlib import Path
from typing import List
...
from src import gs
from src.utils.printer import pprint
from src.logger.logger import logger
# from src.db import ProductTranslationsManager
# from src.translator import get_translations_from_presta_translations_table
# from src.translator import insert_new_translation_to_presta_translations_table
from src.logger.exceptions import ProductFieldException
...

def rearrange_language_keys(presta_fields_dict: dict, client_langs_schema: dict | List[dict], page_lang: str) -> dict:
    """The function updates the language identifier in the Presta_fields_Dict dictionary to the corresponding identifier
    From the scheme of client languages when the page language coincides.

    Args:
        Presta_fields_Dict (DICT): Dictionary of goods fields.
        Page_lang (str): page language.
        Client_langs_Schema (List | DICT): Client's languages scheme.

    Returns:
        DICT: updated dictionary Presta_fields_dict."""
    # Find the corresponding language identifier in the client language scheme
    # Find the corresponding language identifier in the client language scheme
    client_lang_id = None
    for lang in client_langs_schema:
        if lang['locale'] == page_lang or \
        lang['iso_code'] == page_lang or  \
        lang['language_code'] == page_lang:   # <- Pts bad, but if he or il?
            client_lang_id = lang['id']
            break

    # If the language identifier is found in the client language scheme
    if client_lang_id is not None:
        # Update the value of the ID attribute in the Presta_fields_Dict dictionary
        for field in presta_fields_dict.values():
            if isinstance(field, dict) and 'language' in field:
                for lang_data in field['language']:
                    lang_data['attrs']['id'] = str(client_lang_id)   # <- These idyshniki are necessarily lines. Associated with XML Parser

    return presta_fields_dict



def translate_presta_fields_dict (presta_fields_dict: dict, 
                                  client_langs_schema: list | dict, 
                                  page_lang: str = None) -> dict:
    """@Translation of multi -language fields in accordance with the value of `ID` language in the client database
	    The function receives a filled dictionary of fields on the input. Multi -language fields sodarzhat values,
	    The supplier received from the website in the form of a dictionary 
	    `` `
	    {
		    'Language': [
					    {'attrs': {'id': '1'}, 'value': value},
					    ]
	    }
	    `` `
	    The client has a language with a key `id = 1` can be any depending on which language was in 
	    Prestashop was originally installed. Most often it is English, but this is not a rule.
	    I receive accurate correspondences in the client languages scheme 
	    Locator_description
	    The fastest way to find out the API Language Scheme is to dial in the address bar of the browser
	    https: //api_key@mypresta.com/api/languages? Display = Full & Io_Format = Json
	  
    @param client_langs_schema `dict` Dictionary of relevant languages on the client
    @param Presta_fields_dict `Dict` Dictionary of Product fields assembled from the pages of the supplier
    @param page_lang `str` The tongue of the pages of the supplier in the code En-Sus, ru-RU, he_HE. 
    If not set, the function is trying to determine the P text
    @returns Presta_fields_dict Transferred Dictionary of Product Fields"""

    """I am rechargeing the keys of the table."""

    presta_fields_dict = rearrange_language_keys (presta_fields_dict, client_langs_schema, page_lang)
    # product_translations = get_translations_from_presta_translations_table(presta_fields_dict['reference'])
    enabled_product_translations = get_translations_from_presta_translations_table(presta_fields_dict['reference'])
    ...
    if not enabled_product_translations or enabled_product_translations or len(enabled_product_translations) <1:
        """The translation table does not have such a transfer of goods. I add current as a new"""
        ...
        global record
        rec = record(presta_fields_dict)
        insert_new_translation_to_presta_translations_table(rec)
        ...
        return presta_fields_dict

    for client_lang in client_langs_schema:
        for translated_record in enabled_product_translations:
            """TRANSLATION
            Client Codes from Prestashop Table
            'ISO_CODE' 'en' str
            'Locale' 'en -us' str
            'Language_code' 'en -us' str
            I need ISO_Code"""
            try:
                if client_lang['iso_code'] in translated_record.locale: 
                    "Записываю перевод из таблицы"
                    for key in presta_fields_dict.keys():
                        if hasattr(translated_record, key):
                            presta_fields_dict[key] = {'language': [{'attrs': {'id': str(client_lang['id'])}, 'value': getattr(translated_record, key)}]}
                            # Idishniki must be lines. Associated with XML Parser
            except Exception as ex:
                logger.error(f"""Publishedly {ex}
                clint_la = {princt_la)}""")
                ...
						
    return presta_fields_dict

