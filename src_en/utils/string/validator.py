# # \file /src/utils/string/validator.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""The validator of the lines
==================

The module can provide functions for checking the lines for compliance with certain criteria or formats.
Validation may include checking the presence of certain characters, the length of the line, e -mail format, URL, etc.

.. Module :: src.utils.string.validator"""
...

import re, html
from urllib.parse import urlparse, parse_qs
from typing import Union
from urllib.parse import urlparse, parse_qs

from src.logger.logger import logger

class ProductFieldsValidator:
    """Stringvalidator (Validator rows):
    @details 
    - Task: Checking the line for compliance with certain criteria or templates.
    - actions: checking the presence of certain characters, string length, compliance with regular expressions and other checks.
    - Example of use: checking the correctness of e -mail, password or credit card number."""

    @staticmethod
    def validate_price(price: str) -> bool:
        """[Function's description]

        Parameters : 
            @param price : str  :  [description]
        Returns : 
            @return bool  :  [description]"""
        """Validation of prices"""
        if not price:
            return
        price = Ptrn.clear_price.sub('', price)
        price = price.replace(',', '.')
        try:
            float(price)
        except:
            return
        return True


    @staticmethod
    def validate_weight(weight: str) -> bool:
        """[Function's description]

        Parameters : 
            @param weight : str  :  [description]
        Returns : 
            @return bool  :  [description]"""
        """Validation of weight"""
        if not weight:
            return
        weight = Ptrn.clear_number.sub('', weight)
        weight = weight.replace(',', '.')
        try:
            float(weight)
        except:
            return
        return True


    @staticmethod
    def validate_sku(sku: str) -> bool:
        """[Function's description]

        Parameters : 
            @param sku : str  :  [description]
        Returns : 
            @return bool  :  [description]"""
        """VALIDATION ARTICLE"""
        if not sku:
            return
        sku = StringFormatter.remove_special_characters(sku)
        sku = StringFormatter.remove_line_breaks(sku)
        sku = sku.strip()
        if len(sku) < 3:
            return
        return True


    @staticmethod
    def validate_url(url: str) -> bool:
        """[Function's description]

        Parameters : 
            @param url : str  :  [description]
        Returns : 
            @return bool  :  [description]"""
        """Validation URL"""
        if not url:
            return

        url = url.strip()

        if not url.startswith('http'):
            url = 'http://' + url

        parsed_url = urlparse(url)

        if not parsed_url.netloc or not parsed_url.scheme:
            return

        return True

    @staticmethod
    def isint(s: str) -> bool:
        """[Function's description]

        Parameters : 
            @param s : str  :  [description]
        Returns : 
            @return bool  :  [description]"""
        try:
            s = int(s)
            return True
        except Exception as ex:
            return



