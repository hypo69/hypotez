### **Анализ кода модуля `api.py`**

## \file /src/suppliers/suppliers_list/aliexpress/api/api.py

Модуль предоставляет класс `AliexpressApi` для взаимодействия с AliExpress API, позволяющий получать информацию о продуктах и генерировать партнерские ссылки.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и организован в класс `AliexpressApi`.
    - Используются аннотации типов.
    - Присутствует обработка исключений.
    - Использование модуля `logger` для логирования.
- **Минусы**:
    - Не все строки документированы.
    - В некоторых местах используется `Union` вместо `|`.
    - В docstring есть английский текст.
    - Отсутствуют примеры использования в docstring.
    - Не везде соблюдается PEP8 (пробелы вокруг операторов).
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Документация модуля**:
    - Добавить заголовок и описание модуля в формате Markdown.
2.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.
3.  **Docstring**:
    - Перевести все docstring на русский язык и привести их к единому стилю.
    - Добавить примеры использования для каждой функции.
    - Уточнить описания параметров и возвращаемых значений.
4.  **Использовать `|` вместо `Union`**:
    - Заменить `Union` на `|` в аннотациях типов.
5.  **PEP8**:
    - Добавить пробелы вокруг операторов присваивания.
6.  **Обработка исключений**:
    - В блоках `except` использовать `ex` вместо `e` для обозначения исключения.
    - Указывать `exc_info=True` при логировании ошибок для получения подробной информации об исключении.
7.  **Логирование**:
    - Добавить логирование в тех местах, где оно отсутствует, чтобы упростить отладку и мониторинг.

**Оптимизированный код:**

```python
## \file /src/suppliers/suppliers_list/aliexpress/api/api.py
# -*- coding: utf-8 -*-
# <- venv win
## ~~~~~~~~~~~~

"""
Модуль для работы с API AliExpress
====================================

Этот модуль предоставляет класс `AliexpressApi`, который позволяет взаимодействовать с API AliExpress
для получения информации о продуктах и генерации партнерских ссылок.

Пример использования
----------------------

>>> from src.suppliers.suppliers_list.aliexpress.api.api import AliexpressApi
>>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
>>> product_ids = '1234567890'
>>> products = api.retrieve_product_details(product_ids)
>>> if products:
...     print(f'Название продукта: {products[0].title}')
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
    Предоставляет методы для получения информации с AliExpress, используя API credentials.
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
        Инициализирует экземпляр класса AliexpressApi.

        Args:
            key (str): Ваш API key.
            secret (str): Ваш API secret.
            language (model_Language): Код языка.
            currency (model_Currency): Код валюты.
            tracking_id (Optional[str], optional): Tracking ID для генерации ссылок. Defaults to None.
            app_signature (Optional[str], optional): Подпись приложения. Defaults to None.

        Returns:
            None
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
            product_ids (str | list[str]): Одна или несколько ссылок или ID продуктов.
            fields (Optional[str | list[str]], optional): Поля для включения в результаты. Defaults to all.
            country (Optional[str], optional): Фильтр продуктов, которые могут быть отправлены в эту страну.
                Возвращает цену в соответствии с налоговой политикой страны. Defaults to None.

        Returns:
            List[model_Product]: Список продуктов.

        Raises:
            ProductsNotFoudException: Если продукты не найдены.
            InvalidArgumentException: Если передан неверный аргумент.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> product_ids = '1234567890'
            >>> products = api.retrieve_product_details(product_ids)
            >>> if products:
            ...     print(f'Название продукта: {products[0].title}')
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
                ...
                return
        except Exception as ex:
            logger.error('Произошла ошибка при получении деталей продукта', ex, exc_info=True)
            ...
            return

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
            link_type (model_LinkType, optional): Тип ссылки: нормальная или "горячая" ссылка с повышенной комиссией.
                Defaults to model_LinkType.NORMAL.

        Returns:
            List[model_AffiliateLink]: Список партнерских ссылок.

        Raises:
            InvalidArgumentException: Если передан неверный аргумент.
            InvalidTrackingIdException: Если не указан tracking_id.
            ProductsNotFoudException: Если продукты не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> links = 'https://www.aliexpress.com/item/1234567890.html'
            >>> affiliate_links = api.get_affiliate_links(links)
            >>> if affiliate_links:
            ...     print(f'Партнерская ссылка: {affiliate_links[0]}')
        """
        if not self._tracking_id:
            logger.error('The tracking id is required for affiliate links')
            return

        links = get_list_as_string(links)

        request = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
        request.app_signature = self._app_signature
        request.source_values = links
        request.promotion_link_type = link_type
        request.tracking_id = self._tracking_id
        ...
        response = api_request(request, 'aliexpress_affiliate_link_generate_response')
        if not response:
            return
        if response.total_result_count > 0:
            return response.promotion_links.promotion_link
        else:
            logger.warning('Affiliate links not available')
            return

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
            category_ids (Optional[str | list[str]], optional): ID категорий. Defaults to None.
            delivery_days (Optional[int], optional): Количество дней доставки. Defaults to None.
            fields (Optional[str | list[str]], optional): Поля для включения в результаты. Defaults to None.
            keywords (Optional[str], optional): Ключевые слова для поиска. Defaults to None.
            max_sale_price (Optional[int], optional): Максимальная цена. Defaults to None.
            min_sale_price (Optional[int], optional): Минимальная цена. Defaults to None.
            page_no (Optional[int], optional): Номер страницы. Defaults to None.
            page_size (Optional[int], optional): Количество продуктов на странице. Defaults to None.
            platform_product_type (Optional[model_ProductType], optional): Тип продукта платформы. Defaults to None.
            ship_to_country (Optional[str], optional): Страна доставки. Defaults to None.
            sort (Optional[model_SortBy], optional): Метод сортировки. Defaults to None.

        Returns:
            model_HotProductsResponse: Ответ, содержащий информацию и список продуктов.

        Raises:
            ProductsNotFoudException: Если продукты не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> hot_products = api.get_hotproducts(keywords='phone')
            >>> if hot_products and hot_products.products:
            ...     print(f'Название первого продукта: {hot_products.products[0].title}')
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
            List[model_Category | model_ChildCategory]: Список категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> categories = api.get_categories()
            >>> if categories:
            ...     print(f'Название первой категории: {categories[0].name}')
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
            use_cache (bool, optional): Использовать кэшированные категории для уменьшения количества запросов к API.
                Defaults to True.

        Returns:
            List[model_Category]: Список родительских категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> parent_categories = api.get_parent_categories()
            >>> if parent_categories:
            ...     print(f'Название первой родительской категории: {parent_categories[0].name}')
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_parent_categories(self.categories)

    def get_child_categories(
        self,
        parent_category_id: int,
        use_cache: bool = True,
        **kwargs
    ) -> List[model_ChildCategory]:
        """
        Получает все доступные дочерние категории для указанной родительской категории.

        Args:
            parent_category_id (int): ID родительской категории.
            use_cache (bool, optional): Использовать кэшированные категории для уменьшения количества запросов к API.
                Defaults to True.

        Returns:
            List[model_ChildCategory]: Список дочерних категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при запросе к API.
            ApiRequestResponseException: Если произошла ошибка в ответе от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> child_categories = api.get_child_categories(parent_category_id=123)
            >>> if child_categories:
            ...     print(f'Название первой дочерней категории: {child_categories[0].name}')
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)