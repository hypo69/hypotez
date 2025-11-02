## \file /src/suppliers/morlevi/graber (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.morlevi 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.morlevi """


""" morlevi
"""

import os, sys, asyncio
from pathlib import Path
from typing import List, Union, Dict, Any, Optional, Callable
from types import SimpleNamespace
from urllib import response
from langdetect import detect
from functools import wraps


...
from src import gs

from src.endpoints.prestashop.product_fields import ProductFields
from src.category import Category
from src.webdriver.selenium.driver import Driver
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import save_image_from_url
from src.utils.printer import pprint 
from src.utils.image import save_image_from_url
from src.logger.logger import logger 
from src.logger.exceptions import ExecuteLocatorException
from src.endpoints.PrestaShop import PrestaShop

...
supplier_prefix = 'morlevi'

s: Supplier = Supplier(supplier_prefix=supplier_prefix)
l: SimpleNamespace
l = j_loads_ns(gs.path.src / 'suppliers' / self.supplier_prefix / 'locators' / 'product.json')
if not l:
    logger.debug(f"Не определились локаторы - ошибка в файле  {gs.path.src}/suppliers/{supplier_prefix}/locators/product.json")
    ...

f: ProductFields
d: Driver

def close_pop_up(value: Any = None):
    """
    Decorator to call `d.execute_locator` before the actual function logic.
    
    Args:
        value (Any): Optional value for the decorator.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute locator before the original function logic
            try:
                result = d.execute_locator(l.close_pop_up)  # Await here for async function
                ...
            except ExecuteLocatorException as e:
                logger.debug(f"Ошибка выполнения локатора: {e}")
                # Handle error as needed

            # Continue with the original function logic
            return await func(*args, **kwargs)  # Await the original function call
        return wrapper
    return decorator

async def grab_page(driver: Driver) -> ProductFields:
    """Asynchronous function to grab product fields."""
    
    d = driver

    async def fetch_specific_data(value: Any = None):
        """Place for special operations with fields."""
        return True

    async def fetch_all_data(**kwargs):
        global f
        f = ProductFields()
        # Uncomment the following lines to fetch specific data
        await id_product(kwargs.get("id_product", ''))
        await additional_shipping_cost(kwargs.get("additional_shipping_cost", ''))
        # Add more await calls as needed...

    # Call the function to fetch all data
    await fetch_all_data()
    return f

def error(field: str):
    """Error handler for fields."""
    logger.debug(f"Ошибка заполнения поля {field}")
    ...

async def set_field_value(
    value: Any, 
    locator_func: Callable[[], Any], 
    field_name: str, 
    default: Any = ''
) -> Any:
    """Universal function for setting field values with error handling.

    Args:
        value (Any): Provided value to set.
        locator_func (Callable[[], Any]): Function to get the locator's value.
        field_name (str): Name of the field for error handling.
        default (Any, optional): Default value if both value and locator fail. Defaults to ''.

    Returns:
        Any: The value to be assigned to the field.
    """
    return (
        value if value else
        await asyncio.to_thread(locator_func) if locator_func() else
        error(field_name) or default
    )

@close_pop_up()
async def additional_shipping_cost(value: Any = None):
    """Fetch and set additional shipping cost."""
    f.additional_shipping_cost = await set_field_value(
        value, 
        lambda: ''.join( d.execute_locator(l.additional_shipping_cost) or []), 
        'additional_shipping_cost'
    )

@close_pop_up()
async def delivery_in_stock(value: Any = None):
    """Fetch and set delivery in stock status."""
    f.delivery_in_stock = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.delivery_in_stock) or []), 
        'delivery_in_stock'
    )

@close_pop_up()
async def active(value: Any = None):
    """Fetch and set active status."""
    f.active = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.active) or []), 
        'active'
    )


@close_pop_up()
async def additional_delivery_times(value: Any = None):
    f.additional_delivery_times = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.additional_delivery_times) or []), 
        'additional_delivery_times'
    )


        
@close_pop_up()
async def advanced_stock_management(value:Any = None):
        f.advanced_stock_management = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.advanced_stock_management) or []), 
        'advanced_stock_management'
    )

@close_pop_up()
async def affiliate_short_link(value: Any = None):
    f.affiliate_short_link = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_short_link) or []), 
        'affiliate_short_link'
    )

@close_pop_up()
async def affiliate_summary(value: Any = None):
    f.affiliate_summary = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_summary) or []), 
        'affiliate_summary'
    )

@close_pop_up()
async def affiliate_summary_2(value: Any = None):
    f.affiliate_summary_2 = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_summary_2) or []), 
        'affiliate_summary_2'
    )

@close_pop_up()
async def affiliate_text(value: Any = None):
    f.affiliate_text = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_text) or []), 
        'affiliate_text'
    )

@close_pop_up()
async def affiliate_image_large(value: Any = None):
    f.affiliate_image_large = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_image_large) or []), 
        'affiliate_image_large'
    )

@close_pop_up()
async def affiliate_image_medium(value: Any = None):
    f.affiliate_image_medium = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_image_medium) or []), 
        'affiliate_image_medium'
    )
@close_pop_up()
async def affiliate_image_small(value: Any = None):
    f.affiliate_image_small = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.affiliate_image_small) or []), 
        'affiliate_image_small'
    )

@close_pop_up()
async def available_date(value: Any = None):
    f.available_date = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.available_date) or []), 
        'available_date'
    )

@close_pop_up()
async def available_for_order(value: Any = None):
    f.available_for_order = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.available_for_order) or []), 
        'available_for_order'
    )

@close_pop_up()
async def available_later(value: Any = None):
    f.available_later = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.available_later) or []), 
        'available_later'
    )

@close_pop_up()
async def available_now(value: Any = None):
    f.available_now = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.available_now) or []), 
        'available_now'
    )

@close_pop_up()
async def additional_categories(value: str | list = None) -> dict:
    f.additional_categories = value if value else ''

@close_pop_up()
async def cache_default_attribute(value: Any = None):
    f.cache_default_attribute = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.cache_default_attribute) or []), 
        'cache_default_attribute'
    )

@close_pop_up()
async def cache_has_attachments(value: Any = None):
    f.cache_has_attachments = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.cache_default_attribute) or []), 
        'cache_has_attachments'
    )

@close_pop_up()
async def cache_is_pack(value: Any = None):
    f.cache_is_pack = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.cache_is_pack) or []), 
        'cache_is_pack'
    )

@close_pop_up()
async def condition(value: Any = None):
    f.condition = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.condition) or []), 
        'condition'
    )

@close_pop_up()
async def condition(value: Any = None):
    f.condition = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.condition) or []), 
        'condition'
    )

@close_pop_up()
async def customizable(value: Any = None):
    f.customizable = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.customizable) or []), 
        'customizable'
    )

@close_pop_up()
async def date_add(value: Any = None):
    f.date_add = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.date_add) or []), 
        'date_add'
    )

@close_pop_up()
async def date_upd(value: Any = None):
    f.date_upd = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.date_upd) or []), 
        'date_upd'
    )

@close_pop_up()
async def delivery_out_stock(value: Any = None):
    f.delivery_out_stock = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.delivery_out_stock) or []), 
        'delivery_out_stock'
    )

@close_pop_up()
async def depth(value: Any = None):
    f.depth = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.depth) or []), 
        'depth'
    )

@close_pop_up()
async def description(value: Any = None):
    f.description = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.description) or []), 
        'description'
    )

@close_pop_up()
async def description_short(value: Any = None):
    f.description_short = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.description_short) or []), 
        'description_short'
    )

@close_pop_up()
async def id_category_default(value: Any = None):
    f.id_category_default = value

@close_pop_up()
async def id_default_combination(value: Any = None):
    f.id_default_combination = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_default_combination) or []), 
        'id_default_combination'
    )

@close_pop_up()
async def id_product(value: Any = None):
    if value:
        f.id_product = value
        return
    f.id_supplier = f.id_supplier or d.execute_locator(l.id_supplier)
    f.id_product = f"{supplier_prefix}-{f.id_supplier}" if f.id_supplier else None

@close_pop_up()
async def locale(value: Any = None):
    i18n = value or d.locale
    if not i18n and f.name['language'][0]['value']:
        text = f.name['language'][0]['value']
        i18n = detect(text)
    f.locale = i18n

@close_pop_up()
async def id_default_image(value: Any = None):
    f.id_default_image = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_default_image) or []), 
        'id_default_image'
    )

@close_pop_up()
async def ean13(value: Any = None):
    f.ean13 = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.ean13) or []), 
        'ean13'
    )

@close_pop_up()
async def ecotax(value: Any = None):
    f.ecotax = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.ecotax) or []), 
        'ecotax'
    )

@close_pop_up()
async def height(value: Any = None):
    f.height = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.height) or []), 
        'height'
    )

@close_pop_up()
async def how_to_use(value: Any = None):
    f.how_to_use = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.how_to_use) or []), 
        'how_to_use'
    )

@close_pop_up()
async def id_manufacturer(value: Any = None):
    f.id_manufacturer = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_manufacturer) or []), 
        'id_manufacturer'
    )

@close_pop_up()
async def id_supplier(value: Any = None):
    f.id_supplier = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_supplier) or []), 
        'id_supplier'
    )

@close_pop_up()
async def id_tax(value: Any = None):
    f.id_tax = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_tax) or []), 
        'id_tax'
    )

@close_pop_up()
async def id_type_redirected(value: Any = None):
    f.id_type_redirected = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.id_type_redirected) or []), 
        'id_type_redirected'
    )

@close_pop_up()
async def images_urls(value: Any = None):
    f.images_urls = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.images_urls) or []), 
        'images_urls'
    )
@close_pop_up()
async def indexed(value: Any = None):
    f.indexed = await set_field_value(
        value, 
        lambda: ''.join(d.execute_locator(l.indexed) or []), 
        'indexed'
    )


@close_pop_up()
async def ingredients(value: Any = None):
    f.images_urls = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.images_urls) or []),
        'images_urls'
    )

@close_pop_up()
async def meta_description(value: Any = None):
    f.meta_description = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.meta_description) or []),
        'meta_description'
    )

@close_pop_up()
async def meta_keywords(value: Any = None):
    f.meta_keywords = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.meta_keywords) or []),
        'meta_keywords'
    )

@close_pop_up()
async def meta_title(value: Any = None):
    f.meta_title = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.meta_title) or []),
        'meta_title'
    )

@close_pop_up()
async def is_virtual(value: Any = None):
    f.is_virtual = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.is_virtual) or []),
        'is_virtual'
    )

@close_pop_up()
async def isbn(value: Any = None):
    f.isbn = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.isbn) or []),
        'isbn'
    )


@close_pop_up()
async def link_rewrite(value: Any = None) -> str:
    f.link_rewrite = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.link_rewrite) or []),
        'link_rewrite'
    )

@close_pop_up()
async def location(value: Any = None):
    f.location = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.location) or []),
        'location'
    )

@close_pop_up()
async def low_stock_alert(value: Any = None):
    f.low_stock_alert = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.low_stock_alert) or []),
        'low_stock_alert'
    )

@close_pop_up()
async def low_stock_threshold(value: Any = None):
    f.low_stock_threshold = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.low_stock_threshold) or []),
        'low_stock_threshold'
    )

@close_pop_up()
async def minimal_quantity(value: Any = None):
    f.minimal_quantity = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.minimal_quantity) or []),
        'minimal_quantity'
    )

@close_pop_up()
async def mpn(value: Any = None):
    f.mpn = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.mpn) or []),
        'mpn'
    )

@close_pop_up()
async def name(value: Any = None):
    f.name = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.name) or []),
        'name'
    )

@close_pop_up()
async def online_only(value: Any = None):
    f.online_only = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.online_only) or []),
        'online_only'
    )

@close_pop_up()
async def on_sale(value: Any = None):
    f.on_sale = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.on_sale) or []),
        'on_sale'
    )

@close_pop_up()
async def out_of_stock(value: Any = None):
    f.out_of_stock = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.out_of_stock) or []),
        'out_of_stock'
    )

@close_pop_up()
async def pack_stock_type(value: Any = None):
    f.pack_stock_type = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.pack_stock_type) or []),
        'pack_stock_type'
    )

@close_pop_up()
async def price(value: Any = None):
    f.price = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.price) or []),
        'price'
    )

@close_pop_up()
async def product_type(value: Any = None):
    f.product_type = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.product_type) or []),
        'product_type'
    )

@close_pop_up()
async def quantity(value: Any = None):
    f.quantity = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.quantity) or []),
        'quantity'
    )

@close_pop_up()
async def quantity_discount(value: Any = None):
    f.quantity_discount = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.quantity_discount) or []),
        'quantity_discount'
    )

@close_pop_up()
async def redirect_type(value: Any = None):
    f.redirect_type = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.redirect_type) or []),
        'redirect_type'
    )

@close_pop_up()
async def reference(value: Any = None):
    f.reference = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.reference) or []),
        'reference'
    )

@close_pop_up()
async def show_condition(value: Any = None):
    f.show_condition = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.show_condition) or []),
        'show_condition'
    )

@close_pop_up()
async def show_price(value: Any = None):
    f.show_price = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.show_price) or []),
        'show_price'
    )

@close_pop_up()
async def state(value: Any = None):
    f.state = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.state) or []),
        'state'
    )

@close_pop_up()
async def text_fields(value: Any = None):
    f.text_fields = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.text_fields) or []),
        'text_fields'
    )

@close_pop_up()
async def unit_price_ratio(value: Any = None):
    f.unit_price_ratio = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.unit_price_ratio) or []),
        'unit_price_ratio'
    )


@close_pop_up()
async def unity(value: Any = None):
    f.unity = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.unity) or []),
        'unity'
    )

@close_pop_up()
async def upc(value: Any = None):
    f.upc = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.upc) or []),
        'upc'
    )

@close_pop_up()
async def uploadable_files(value: Any = None):
    f.uploadable_files = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.uploadable_files) or []),
        'uploadable_files'
    )

@close_pop_up()
async def default_image_url(value: Any = None):
    f.default_image_url = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.default_image_url) or []),
        'default_image_url'
    )

@close_pop_up()
async def visibility(value: Any = None):
    f.visibility = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.visibility) or []),
        'visibility'
    )

@close_pop_up()
async def weight(value: Any = None):
    f.weight = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.weight) or []),
        'weight'
    )

@close_pop_up()
async def wholesale_price(value: Any = None):
    f.wholesale_price = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.wholesale_price) or []),
        'wholesale_price'
    )

@close_pop_up()
async def width(value: Any = None):
    f.width = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.width) or []),
        'width'
    )

@close_pop_up()
async def specification(value: Any = None):
    f.specification = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.specification) or []),
        'specification'
    )

@close_pop_up()
async def link(value: Any = None):
    f.link = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.link) or []),
        'link'
    )

@close_pop_up()
async def byer_protection(value: Any = None):
    f.byer_protection = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.byer_protection) or []),
        'byer_protection'
    )

@close_pop_up()
async def customer_reviews(value: Any = None):
    f.customer_reviews = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.customer_reviews) or []),
        'customer_reviews'
    )

@close_pop_up()
async def link_to_video(value: Any = None):
    f.link_to_video = await set_field_value(
        value,
        lambda: ''.join(d.execute_locator(l.link_to_video) or []),
        'link_to_video'
    )

@close_pop_up()
async def local_image_path(value: Any = None):
    f.local_image_path = await set_field_value(
        value,
        lambda: save_image_from_url( d.execute_locator(l.default_image_url), f.id_product),
        'local_image_path'
    )

@close_pop_up()
async def local_video_path(value: Any = None):
    f.local_video_path = await set_field_value(
        value,
        lambda: d.execute_locator(l.local_video_path),
        'local_video_path'
    )
