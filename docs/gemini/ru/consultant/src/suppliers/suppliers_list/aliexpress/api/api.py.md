### **Анализ кода модуля `api.py`**

## \file /src/suppliers/suppliers_list/aliexpress/api/api.py

Модуль содержит класс `AliexpressApi`, который предоставляет методы для взаимодействия с API AliExpress.

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разбит на отдельные функции, что облегчает чтение и понимание.
    - Присутствуют docstring для большинства функций, что упрощает использование API.
    - Используется модуль `logger` для логирования ошибок и предупреждений.
    - Есть обработка исключений.
- **Минусы**:
    - Некоторые docstring написаны на английском языке.
    - Не все переменные аннотированы типами.
    - Местами используются не совсем корректные конструкции `Union`.
    - Не везде используется `logger.error` с передачей `ex` и `exc_info=True`.
    - В `__init__` не все параметры аннотированы типами.
    - Отсутствует описание модуля.
    - В некоторых местах присутствует `...`

**Рекомендации по улучшению**:

1.  Добавить описание модуля в начале файла.
2.  Перевести все docstring на русский язык.
3.  Добавить аннотации типов для всех переменных и параметров функций.
4.  Использовать `|` вместо `Union`.
5.  Использовать `logger.error(ex, exc_info=True)` для логирования ошибок, чтобы получить полную информацию об исключении.
6.  В блоках `except` использовать переменную `ex` вместо `e`.
7.  Удалить `...` из кода, заменив их конкретной реализацией или заглушкой с комментарием.
8.  Изменить способ указания типов `str | list` на `str | list[str]`.
9.  Всегда использовать одинарные кавычки (`'`) в Python-коде.
10. Добавить примеры использования в docstring функций.

**Оптимизированный код**:

```python
## \file /src/suppliers/suppliers_list/aliexpress/api/api.py
# -*- coding: utf-8 -*-\n
# <- venv win
## ~~~~~~~~~~~~~\
"""
Модуль для работы с API AliExpress
====================================

Модуль содержит класс :class:`AliexpressApi`, который используется для взаимодействия с API AliExpress
и получения информации о товарах и партнерских ссылках.

Пример использования
----------------------

>>> from src.suppliers.suppliers_list.aliexpress.api import AliexpressApi
>>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
>>> products = api.retrieve_product_details(product_ids=['1234567890'])
>>> if products:
...     print(products[0].title)
"""

from typing import List, Optional

from src.logger.logger import logger
from src.utils.printer import pprint

from .models import (
    AffiliateLink as model_AffiliateLink,
    Category as model_Category,
    ChildCategory as model_ChildCategory,
    Currency as model_Currency,
    HotProductsResponse as model_HotProductsResponse,
    Language as model_Language,
    LinkType as model_LinkType,
    Product as model_Product,
    ProductType as model_ProductType,
    SortBy as model_SortBy
)

from .errors.exceptions import CategoriesNotFoudException
from .helpers.categories import filter_child_categories, filter_parent_categories
from .skd import setDefaultAppInfo
from .skd import api as aliapi
from .errors import ProductsNotFoudException, InvalidTrackingIdException
from .helpers import api_request, parse_products, get_list_as_string, get_product_ids


class AliexpressApi:
    """
    Предоставляет методы для получения информации из AliExpress с использованием API credentials.
    """

    def __init__(
            self,
            key: str,
            secret: str,
            language: model_Language,
            currency: model_Currency,
            tracking_id: Optional[str] = None,
            app_signature: Optional[str] = None,
            **kwargs
    ) -> None:
        """
        Args:
            key (str): Your API key.
            secret (str): Your API secret.
            language (str): Language code. Defaults to EN.
            currency (str): Currency code. Defaults to USD.
            tracking_id (str, optional): The tracking id for link generator. Defaults to None.
        """
        self._key: str = key
        self._secret: str = secret
        self._tracking_id: Optional[str] = tracking_id
        self._language: model_Language = language
        self._currency: model_Currency = currency
        self._app_signature: Optional[str] = app_signature
        self.categories: Optional[List[model_Category | model_ChildCategory]] = None
        setDefaultAppInfo(self._key, self._secret)

    def retrieve_product_details(
            self,
            product_ids: str | list[str],
            fields: Optional[str | list[str]] = None,
            country: Optional[str] = None,
            **kwargs
    ) -> List[model_Product]:
        """
        Получает информацию о продуктах.

        Args:
            product_ids (str | list[str]): Одна или несколько ссылок или идентификаторов продуктов.
            fields (str | list[str], optional): Поля для включения в результаты. По умолчанию все.
            country (str, optional): Фильтр продуктов, которые могут быть отправлены в эту страну. Возвращает цену
                в соответствии с налоговой политикой страны.

        Returns:
            list[model_Product]: Список продуктов.

        Raises:
            ProductsNotFoudException: Если продукты не найдены.
            InvalidArgumentException: Если предоставлены неверные аргументы.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> products = api.retrieve_product_details(product_ids=['1234567890'])
            >>> if products:
            ...     print(products[0].title)
        """
        product_ids = get_product_ids(product_ids)
        product_ids = get_list_as_string(product_ids)

        request = aliapi.rest.AliexpressAffiliateProductdetailGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.product_ids = product_ids
        request.country = country
        request.target_currency = self._currency.upper()
        request.target_language = self._language.upper()
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_productdetail_get_response')
        try:
            if response.current_record_count > 0:
                response = parse_products(response.products.product)
                return response
            else:
                logger.warning('No products found with current parameters')
                #raise ProductsNotFoudException('No products found with current parameters')
                return  # TODO: what return ?
        except Exception as ex:
            logger.error('Error while retrieving product details', ex, exc_info=True)
            return  # TODO: what return ?

    def get_affiliate_links(
            self,
            links: str | list[str],
            link_type: model_LinkType = model_LinkType.NORMAL,
            **kwargs
    ) -> List[model_AffiliateLink]:
        """
        Преобразует список ссылок в партнерские ссылки.

        Args:
            links (str | list[str]): Одна или несколько ссылок для преобразования.
            link_type (model_LinkType, optional): Выберите между обычной ссылкой со стандартной комиссией
                или горячей ссылкой с горячей комиссией продукта. По умолчанию NORMAL.

        Returns:
            list[model_AffiliateLink]: Список, содержащий партнерские ссылки.

        Raises:
            InvalidArgumentException: Если предоставлены неверные аргументы.
            InvalidTrackingIdException: Если не указан tracking_id.
            ProductsNotFoudException: Если продукты не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> affiliate_links = api.get_affiliate_links(links=['https://www.aliexpress.com/item/1234567890.html'])
            >>> if affiliate_links:
            ...     print(affiliate_links[0].affiliate_link)
        """
        if not self._tracking_id:
            logger.error('The tracking id is required for affiliate links')
            #raise InvalidTrackingIdException('The tracking id is required for affiliate links')
            return  # TODO: what return ?

        links = get_list_as_string(links)

        request = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
        request.app_signature = self._app_signature
        request.source_values = links
        request.promotion_link_type = link_type
        request.tracking_id = self._tracking_id
        # ...
        response = api_request(request, 'aliexpress_affiliate_link_generate_response')
        if not response:
            return  # TODO: what return ?
        if response.total_result_count > 0:
            return response.promotion_links.promotion_link
        else:
            #raise ProductsNotFoudException('Affiliate links not available')
            logger.warning('Affiliate links not available')
            return  # TODO: what return ?

    def get_hotproducts(
            self,
            category_ids: Optional[str | list[str]] = None,
            delivery_days: Optional[int] = None,
            fields: Optional[str | list[str]] = None,
            keywords: Optional[str] = None,
            max_sale_price: Optional[int] = None,
            min_sale_price: Optional[int] = None,
            page_no: Optional[int] = None,
            page_size: Optional[int] = None,
            platform_product_type: Optional[model_ProductType] = None,
            ship_to_country: Optional[str] = None,
            sort: Optional[model_SortBy] = None,
            **kwargs
    ) -> model_HotProductsResponse:
        """
        Ищет партнерские продукты с высокой комиссией.

        Args:
            category_ids (str | list[str], optional): Один или несколько идентификаторов категорий.
            delivery_days (int, optional): Предполагаемое количество дней доставки.
            fields (str | list[str], optional): Поля для включения в список результатов. По умолчанию все.
            keywords (str, optional): Поиск продуктов на основе ключевых слов.
            max_sale_price (int, optional): Фильтрует продукты с ценой ниже указанного значения.
                Цены указываются в наименьшей валютной деноминации. Так, $31.41 следует указывать как 3141.
            min_sale_price (int, optional): Фильтрует продукты с ценой выше указанного значения.
                Цены указываются в наименьшей валютной деноминации. Так, $31.41 следует указывать как 3141.
            page_no (int, optional): Номер страницы.
            page_size (int, optional): Количество продуктов на каждой странице. Должно быть между 1 и 50.
            platform_product_type (model_ProductType, optional): Укажите тип продукта платформы.
            ship_to_country (str, optional): Фильтрует продукты, которые могут быть отправлены в эту страну.
                Возвращает цену в соответствии с налоговой политикой страны.
            sort (model_SortBy, optional): Указывает метод сортировки.

        Returns:
            model_HotProductsResponse: Содержит информацию об ответе и список продуктов.

        Raises:
            ProductsNotFoudException: Если продукты не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> hot_products = api.get_hotproducts(category_ids=['123'], keywords='phone')
            >>> if hot_products and hot_products.products:
            ...     print(hot_products.products[0].title)
        """
        request = aliapi.rest.AliexpressAffiliateHotproductQueryRequest()
        request.app_signature = self._app_signature
        request.category_ids = get_list_as_string(category_ids)
        request.delivery_days = str(delivery_days)
        request.fields = get_list_as_string(fields)
        request.keywords = keywords
        request.max_sale_price = max_sale_price
        request.min_sale_price = min_sale_price
        request.page_no = page_no
        request.page_size = page_size
        request.platform_product_type = platform_product_type
        request.ship_to_country = ship_to_country
        request.sort = sort
        request.target_currency = self._currency
        request.target_language = self._language
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_hotproduct_query_response')

        if response.current_record_count > 0:
            response.products = parse_products(response.products.product)
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')

    def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]:
        """
        Получает все доступные категории, как родительские, так и дочерние.

        Returns:
            list[model_Category | model_ChildCategory]: Список категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> categories = api.get_categories()
            >>> if categories:
            ...     print(categories[0].name)
        """
        request = aliapi.rest.AliexpressAffiliateCategoryGetRequest()
        request.app_signature = self._app_signature

        response = api_request(request, 'aliexpress_affiliate_category_get_response')

        if response.total_result_count > 0:
            self.categories = response.categories.category
            return self.categories
        else:
            raise CategoriesNotFoudException('No categories found')

    def get_parent_categories(self, use_cache: bool = True, **kwargs) -> List[model_Category]:
        """
        Получает все доступные родительские категории.

        Args:
            use_cache (bool, optional): Использует кэшированные категории для уменьшения количества запросов к API.

        Returns:
            list[model_Category]: Список родительских категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> parent_categories = api.get_parent_categories()
            >>> if parent_categories:
            ...     print(parent_categories[0].name)
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_parent_categories(self.categories)

    def get_child_categories(self, parent_category_id: int, use_cache: bool = True, **kwargs) -> List[model_ChildCategory]:
        """
        Получает все доступные дочерние категории для определенной родительской категории.

        Args:
            parent_category_id (int): Идентификатор родительской категории.
            use_cache (bool, optional): Использует кэшированные категории для уменьшения количества запросов к API.

        Returns:
            list[model_ChildCategory]: Список дочерних категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе API.

        Example:
            >>> api = AliexpressApi(key='YOUR_API_KEY', secret='YOUR_API_SECRET', language='RU', currency='USD', tracking_id='YOUR_TRACKING_ID')
            >>> child_categories = api.get_child_categories(parent_category_id=123)
            >>> if child_categories:
            ...     print(child_categories[0].name)
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)