## \file /src/suppliers/aliexpress/.ipynb_checkpoints/affiliated_products_generator-checkpoint.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
module: src.suppliers.aliexpress..ipynb_checkpoints 
	:platform: Windows, Unix
	:synopsis:

"""
MODE = 'dev'

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""MODE = 'dev'
  
""" module: src.suppliers.aliexpress..ipynb_checkpoints """


""" Класс создает товары с ссылками 'promotion_link' для товара"""


import header   # <- используется при запуске модуля через main(). Содержит установку корня модулей в `src`
import asyncio
from datetime import datetime
import json
import time
import requests
from itertools import count
from pathlib import Path
from typing import List, Optional
from types import SimpleNamespace
from urllib.parse import urlparse
import html  # For decoding HTML escape sequences
import re  # For removing special characters
from src import gs
from src.suppliers.aliexpress import AliApi
from src.suppliers.aliexpress import Aliexpress
from src.suppliers.aliexpress.affiliate_links_shortener_via_webdriver import AffiliateLinksShortener
from src.suppliers.aliexpress.utils.extract_product_id import extract_prod_ids
from src.suppliers.aliexpress.utils.set_full_https import ensure_https
from src.utils import StringNormalizer as SN
from src.utils.convertors.csv import csv2dict
from src.utils import j_dumps, j_loads, j_loads_ns
from src.utils import save_image_from_url, save_video_from_url, save_text_file, pprint
from src.utils.file import read_text_file, save_text_file, get_directory_names, get_filenames
from src.logger import logger
import pytest
from unittest.mock import patch, MagicMock


class AliAffiliatedProducts(AliApi):
    """ Class to collect full product data from URLs or product IDs.
    For more details on how to create templates for ad campaigns, see the section `Managing Aliexpress Ad Campaigns`.
    """

    def __init__(self,
                 language: str | dict = 'EN',
                 currency: str = 'USD',
                 *args, **kwargs):
        """
        Initializes the AliAffiliatedProducts class.

        @param language: Language for the campaign (default 'EN').
        @param currency: Currency for the campaign (default 'USD').
        """
        super().__init__(language, currency)

    def process_affiliate_products(self, prod_ids: list[str] | str, category_path: str | Path, locale: str) -> list[SimpleNamespace]:
        """
        Processes a list of URLs and returns a list of products with affiliate links and saved images.

        @param prod_ids: List of product URLs or IDs.
        @param category_path: Path to save images and promotion links.
        @return: List of processed products.
        """
        def get_page_content(url: str) -> str | None:
            """ Fetch the content of the page from the given URL.

            @param url: The URL of the page to fetch.
            @return: The content of the page as a string, or None if an error occurs.
            """
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP request errors
                return response.text
            except requests.RequestException as ex:
                logger.error(f"Error fetching {url}:", ex)
                return

        _promotion_links: list = []
        _prod_urls: list = []
        promotional_prod_urls = ensure_https(prod_ids)
        print_flag = 'new_line'
        for prod_url in promotional_prod_urls:
            _link = super().get_affiliate_links(prod_url)
            if _link:
                _link = _link[0]
            if hasattr(_link, 'promotion_link'):
                _promotion_links.append(_link.promotion_link)
                _prod_urls.append(prod_url)

                pprint(
                    f'found affiliate for: {_link.promotion_link}', end=print_flag)
                print_flag = 'inline'
            else:
                continue

        if not _promotion_links:
            logger.warning(
                f'No affiliate products returned \n path={category_path} \n prod_ids={prod_ids}', None, None)

        _affiliate_products: List[SimpleNamespace] = self.retrieve_product_details(
            _prod_urls)
        if not _affiliate_products:
            return []

        # Save promotion links to a file
        
        affiliated_products_list: list[SimpleNamespace] = []
        print_flag = 'new_line'
        for product, promotion_link in zip(_affiliate_products, _promotion_links):
            product.promotion_link = promotion_link
            image_path = Path(category_path) / 'images' / \
                f"{product.product_id}.png"
            save_image_from_url(product.product_main_image_url,
                              image_path, exc_info=False)
            product.local_image_path = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url = urlparse(product.product_video_url)
                suffix = Path(parsed_url.path).suffix

                video_path = Path(category_path) / 'videos' / \
                    f'{product.product_id}{suffix}'
                save_video_from_url(product.product_video_url,
                                    video_path, exc_info=False)
                product.local_video_path = str(video_path)

            product.tags = f"#{SN.simplify_string(product.first_level_category_name)}, #{SN.simplify_string(product.second_level_category_name)}"
            # page_content = get_page_content(product.product_detail_url)
            ...
            affiliated_products_list.append(product)
            pprint(f'caught product - {product.product_id}', end=print_flag)
        print_flag = 'new_line'

        asyncio.run(self.generate_output(affiliated_products_list, category_path))
        return affiliated_products_list

    async def generate_output(self, products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Saves product data in various formats:
        <product_id>.json - all product parameters, one file per product
        ai_{timestamp}.json - a common file for all products with specific keys
        `promotion_links.txt` - a list of only product links (created in the `save_promotion_links()` function)

        @param products_list: List of products to save.
        @param category_path: Path to save the files.
        """
        ...
        timestamp = datetime.now().strftime("%Y-%m-%d %H%M%S")
        openai_file = Path(category_path) / f"ai_{timestamp}.json"
        products_list = products_list if isinstance(
            products_list, list) else [products_list]
        _data_for_openai: dict = {}
        _promotion_links_list: list = []

        for product in products_list:
            j_dumps(product, Path(category_path) /
                    f"{product.product_id}.json", exc_info=False)

            _promotion_links_list.append(product.product_id)

            _data_for_openai[str(product.product_id)] = {
                "product_title": product.product_title,
                "second_level_category_name": product.second_level_category_name,
                "first_level_category_name": product.first_level_category_name,
                "promotion_link": product.promotion_link,
                "target_original_price": product.target_original_price,
                "target_original_price_currency": product.target_original_price_currency,
                "target_sale_price": product.target_sale_price,
                "target_sale_price_currency": product.target_sale_price_currency,
                "evaluate_rate": getattr(product, 'evaluate_rate', None),
                "product_main_image_url": getattr(product, 'product_main_image_url', None),

            }

        j_dumps(_data_for_openai, openai_file)
        await self.save_promotion_links(
            promotion_links=_promotion_links_list, category_path=category_path)
        await self.generate_html(products_list=products_list, category_path=category_path)

    async def save_promotion_links(self, promotion_links: str | list[str], category_path: str | Path) -> str | list[str]:
        """
        Save the list of promotion links to a file and return the saved links.

        @param promotion_links: List of promotion links or a single promotion link to save.
        @param category_path: Path to save the file.
        @return: The saved promotion links as a single string if input was a single string, or as a list of strings if input was a list.
        """
        if isinstance(promotion_links, str):
            promotion_links = [promotion_links]

        promotion_links_path = Path(category_path) / 'promotion_links.txt'
        try:
            with open(promotion_links_path, 'a') as file:
                for link in promotion_links:
                    file.write(f"{link}\n")
        except IOError as ex:
            logger.error(
                f"Error saving promotion links to {promotion_links_path}:", ex)

    async def generate_html(self, products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Creates an HTML file for the category.
        
        @param products_list: List of products to include in the HTML.
        @param category_path: Path to save the HTML file.
        """
        ...
        products_list = products_list if isinstance(
            products_list, list) else [products_list]

        html_path:Path = Path(category_path / 'html')
        
        html_content = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product List</title>
        <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        <div class="product-grid">
        """

        for product in products_list:
            html_content += f"""
            <div class="product-card">
            <img src="{product.product_main_image_url}" alt="{html.escape(product.product_title)}" class="product-image">
            <div class="product-info">
            <h2 class="product-title">{html.escape(product.product_title)}</h2>
            <p class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</p>
            <p class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</p>
            <p class="product-category">Category: {product.second_level_category_name}</p>
            <a href="{product.promotion_link}" class="product-link">Buy Now</a>
            </div>
            </div>
            """

        html_content += """
        </div>
        </body>
        </html>
        """


            
        save_text_file(html_content, html_path)
