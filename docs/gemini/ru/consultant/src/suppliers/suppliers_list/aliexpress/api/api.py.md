### **Анализ кода модуля `api.py`**

## \file /src/suppliers/aliexpress/api/api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с API AliExpress
======================================

Модуль предоставляет класс :class:`AliexpressApi`, который позволяет взаимодействовать с API AliExpress
для получения информации о товарах и генерации партнерских ссылок.

Пример использования
----------------------

>>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
>>> products = api.retrieve_product_details(product_ids=['1234567890'])
"""

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на функции, что облегчает его понимание и поддержку.
  - Используются аннотации типов, что улучшает читаемость и облегчает отладку.
  - Присутствует обработка исключений, что делает код более устойчивым к ошибкам.
  - Используется модуль `logger` для логирования.
- **Минусы**:
  - Docstring написаны на английском языке.
  - Не все исключения обрабатываются с передачей `exc_info=True` в `logger.error`.
  - В некоторых местах используется `Union`, можно заменить на `|`.

**Рекомендации по улучшению**:

1.  **Документация**:
    *   Перевести все docstring на русский язык, следуя требованиям оформления.
    *   Добавить примеры использования для основных функций.
    *   Улучшить описание исключений, указав, в каких случаях они возникают.

2.  **Обработка исключений**:
    *   В блоках `except` добавить `exc_info=True` при вызове `logger.error`, чтобы получить полную трассировку стека.

3.  **Использование `Union`**:
    *   Заменить `Union[str, list]` на `str | list`.

4.  **Логирование**:
    *   Улучшить сообщения логирования, сделав их более информативными.
    *   Удалить закомментированные строки `raise ProductsNotFoudException(...)`.

5.  **Общее**:
    *   Проверить и унифицировать стиль кодирования в соответствии с PEP8.
    *   Избавиться от `...`

**Оптимизированный код**:

```python
## \file /src/suppliers/aliexpress/api/api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с API AliExpress
======================================

Модуль предоставляет класс :class:`AliexpressApi`, который позволяет взаимодействовать с API AliExpress
для получения информации о товарах и генерации партнерских ссылок.

Пример использования
----------------------

>>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
>>> products = api.retrieve_product_details(product_ids=['1234567890'])
"""


from typing import List
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
    SortBy as model_SortBy,
)
from .errors import ProductsNotFoudException, InvalidTrackingIdException

from .helpers.categories import filter_child_categories, filter_parent_categories
from .skd import setDefaultAppInfo
from .skd import api as aliapi
from .helpers import api_request, parse_products, get_list_as_string, get_product_ids
from .errors.exceptions import CategoriesNotFoudException


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
        tracking_id: str = None,
        app_signature: str = None,
        **kwargs,
    ) -> None:
        """
        Инициализирует экземпляр класса AliexpressApi.

        Args:
            key (str): Ваш API ключ.
            secret (str): Ваш API secret.
            language (model_Language): Код языка.
            currency (model_Currency): Код валюты.
            tracking_id (str, optional): Tracking ID для генерации ссылок. По умолчанию None.
            app_signature (str, optional): Подпись приложения. По умолчанию None.

        Returns:
            None

        """
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        self._app_signature = app_signature
        self.categories = None
        setDefaultAppInfo(self._key, self._secret)

    def retrieve_product_details(
        self,
        product_ids: str | list[str],
        fields: str | list[str] = None,
        country: str = None,
        **kwargs,
    ) -> List[model_Product]:
        """
        Получает информацию о товарах.

        Args:
            product_ids (str | list[str]): Один или несколько ID товаров или ссылок.
            fields (str | list[str], optional): Список полей для включения в результаты. По умолчанию все поля.
            country (str, optional): Фильтр товаров, доступных для отправки в указанную страну.
                Возвращает цену с учетом налоговой политики страны. По умолчанию None.

        Returns:
            list[model_Product]: Список товаров.

        Raises:
            ProductsNotFoudException: Если товары не найдены.
            InvalidArgumentException: Если переданы неверные аргументы.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> product = api.retrieve_product_details(product_ids=['1234567890'])
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
                logger.warning('Товары не найдены с указанными параметрами')
                return
        except Exception as ex:
            logger.error('Ошибка при получении деталей товара', ex, exc_info=True)
            return

    def get_affiliate_links(
        self,
        links: str | list[str],
        link_type: model_LinkType = model_LinkType.NORMAL,
        **kwargs,
    ) -> List[model_AffiliateLink]:
        """
        Преобразует список ссылок в партнерские ссылки.

        Args:
            links (str | list[str]): Одна или несколько ссылок для преобразования.
            link_type (model_LinkType, optional): Тип ссылки: NORMAL (стандартная комиссия) или HOTLINK (повышенная комиссия).
                По умолчанию NORMAL.

        Returns:
            list[model_AffiliateLink]: Список партнерских ссылок.

        Raises:
            InvalidArgumentException: Если переданы неверные аргументы.
            InvalidTrackingIdException: Если не указан tracking ID.
            ProductsNotFoudException: Если товары не найдены.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> affiliate_links = api.get_affiliate_links(links=['https://aliexpress.com/item/1234567890.html'])
        """
        if not self._tracking_id:
            logger.error('Не указан tracking ID, необходимый для получения партнерских ссылок')
            return

        links = get_list_as_string(links)

        request = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
        request.app_signature = self._app_signature
        request.source_values = links
        request.promotion_link_type = link_type
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_link_generate_response')
        if not response:
            return

        if response.total_result_count > 0:
            return response.promotion_links.promotion_link
        else:
            logger.warning('Партнерские ссылки не найдены')
            return

    def get_hotproducts(
        self,
        category_ids: str | list[str] = None,
        delivery_days: int = None,
        fields: str | list[str] = None,
        keywords: str = None,
        max_sale_price: int = None,
        min_sale_price: int = None,
        page_no: int = None,
        page_size: int = None,
        platform_product_type: model_ProductType = None,
        ship_to_country: str = None,
        sort: model_SortBy = None,
        **kwargs,
    ) -> model_HotProductsResponse:
        """
        Ищет партнерские товары с высокой комиссией.

        Args:
            category_ids (str | list[str], optional): ID категорий товаров.
            delivery_days (int, optional): Предполагаемое количество дней доставки.
            fields (str | list[str], optional): Список полей для включения в результаты. По умолчанию все поля.
            keywords (str, optional): Ключевые слова для поиска товаров.
            max_sale_price (int, optional): Максимальная цена товара (в минимальных единицах валюты, например, копейках).
            min_sale_price (int, optional): Минимальная цена товара (в минимальных единицах валюты, например, копейках).
            page_no (int, optional): Номер страницы.
            page_size (int, optional): Количество товаров на странице (от 1 до 50).
            platform_product_type (model_ProductType, optional): Тип платформы товара.
            ship_to_country (str, optional): Страна доставки.
            sort (model_SortBy, optional): Метод сортировки результатов.

        Returns:
            model_HotProductsResponse: Ответ API, содержащий информацию о запросе и список товаров.

        Raises:
            ProductsNotFoudException: Если товары не найдены.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> hot_products = api.get_hotproducts(category_ids=['123'], keywords='phone', page_size=10)
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
            raise ProductsNotFoudException('Товары не найдены с указанными параметрами')

    def get_categories(self, **kwargs) -> List[model_Category | model_ChildCategory]:
        """
        Получает список всех доступных категорий (родительских и дочерних).

        Returns:
            list[model_Category | model_ChildCategory]: Список категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> categories = api.get_categories()
        """
        request = aliapi.rest.AliexpressAffiliateCategoryGetRequest()
        request.app_signature = self._app_signature

        response = api_request(request, 'aliexpress_affiliate_category_get_response')

        if response.total_result_count > 0:
            self.categories = response.categories.category
            return self.categories
        else:
            raise CategoriesNotFoudException('Категории не найдены')

    def get_parent_categories(self, use_cache=True, **kwargs) -> List[model_Category]:
        """
        Получает список родительских категорий.

        Args:
            use_cache (bool, optional): Использовать ли кэшированные категории для уменьшения количества запросов к API. По умолчанию True.

        Returns:
            list[model_Category]: Список родительских категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> parent_categories = api.get_parent_categories()
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_parent_categories(self.categories)

    def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[model_ChildCategory]:
        """
        Получает список дочерних категорий для указанной родительской категории.

        Args:
            parent_category_id (int): ID родительской категории.
            use_cache (bool, optional): Использовать ли кэшированные категории для уменьшения количества запросов к API. По умолчанию True.

        Returns:
            list[model_ChildCategory]: Список дочерних категорий.

        Raises:
            CategoriesNotFoudException: Если категории не найдены.
            ApiRequestException: Если произошла ошибка при выполнении запроса к API.
            ApiRequestResponseException: Если получен некорректный ответ от API.

        Example:
            >>> api = AliexpressApi(key='your_key', secret='your_secret', language='RU', currency='RUB', tracking_id='your_tracking_id')
            >>> child_categories = api.get_child_categories(parent_category_id=123)
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)