### **Анализ кода модуля `src.endpoints.prestashop.api`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и содержит подробные docstring для большинства функций и классов.
  - Используются аннотации типов.
  - Присутствует обработка исключений с использованием `logger.error`.
  - Конфигурация вынесена в отдельный класс `Config`.
- **Минусы**:
  - Встречаются смешанные стили кавычек (используются как одинарные, так и двойные кавычки).
  - Некоторые docstring написаны на английском языке.
  - Не все функции и методы имеют docstring.
  - В некоторых местах используется `...` без пояснений.
  - Некоторые переменные не имеют аннотации типов.
  - Смешанный стиль именования переменных (snake_case и camelCase).

## Рекомендации по улучшению:

1.  **Унификация кавычек**: Заменить все двойные кавычки на одинарные.
2.  **Перевод docstring**: Перевести все docstring на русский язык.
3.  **Добавление docstring**: Добавить docstring для всех функций и методов, где они отсутствуют.
4.  **Удаление `...`**: Заменить `...` конкретной реализацией или пояснением.
5.  **Аннотации типов**: Добавить аннотации типов для всех переменных, где они отсутствуют.
6.  **Унификация именования переменных**: Использовать snake_case для именования переменных и функций.
7.  **Логирование**: Улучшить логирование, добавив больше контекстной информации, где это необходимо.
8.  **Обработка ошибок**: Сделать обработку ошибок более гранулярной и информативной.
9.  **Использовать `j_loads` или `j_loads_ns`**: Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
10. **Конфигурация**: Упростить и сделать более гибкой конфигурацию API, возможно, с использованием переменных окружения.
11. **Согласованность**: Привести код в соответствие со стандартами PEP8.

## Оптимизированный код:

```python
## \file src/endpoints/prestashop/api/api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с PrestaShop API.
=========================================================================================

Этот модуль предоставляет класс `PrestaShop` для взаимодействия с PrestaShop webservice API,
используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск,
и загрузку изображений, с обработкой ошибок для ответов.

Примеры использования
---------------------

```python
from src.endpoints.prestashop.api import PrestaShop

api = PrestaShop(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    default_lang=1,
    debug=True,
    data_format='JSON',
)

api.ping()

data = {
    'tax': {
        'rate': 3.000,
        'active': '1',
        'name': {
            'language': {
                'attrs': {'id': '1'},
                'value': '3% tax'
            }
        }
    }
}

# Создание налоговой записи
rec = api.create('taxes', data)

# Обновление той же налоговой записи
update_data = {
    'tax': {
        'id': str(rec['id']),
        'rate': 3.000,
        'active': '1',
        'name': {
            'language': {
                'attrs': {'id': '1'},
                'value': '3% tax'
            }
        }
    }
}

update_rec = api.write('taxes', update_data)

# Удаление этого налога
api.unlink('taxes', str(rec['id']))

# Поиск первых 3 налогов с '5' в названии
import pprint
recs = api.search('taxes', filter='[name]=%[5]%', limit='3')

for rec in recs:
    pprint(rec)

# Создание бинарного файла (изображение товара)
api.create_binary('images/products/22', 'img.jpeg', 'image')
```
"""

import os
import sys
import json
from enum import Enum
from http.client import HTTPConnection
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from xml.etree import ElementTree
from xml.parsers.expat import ExpatError

from httpx import Response
import requests
from requests import Session
from requests.models import PreparedRequest
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects

import header
from src import gs
from src.logger.exceptions import PrestaShopAuthenticationError, PrestaShopException
from src.logger.logger import logger
from src.utils.convertors.base64 import base64_to_tmpfile
# from src.utils.convertors.dict import dict2xml
# from src.utils.convertors.xml2dict import xml2dict
from src.endpoints.prestashop.utils import dict2xml, xml2dict
from src.utils.xml import save_xml
from src.utils.file import save_text_file
from src.utils.image import save_image_from_url_async
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint as print
from src import USE_ENV

from dataclasses import dataclass, field

@dataclass
class Config:
    """Конфигурационный класс для PrestaShop API."""

    language: str
    ps_version: str = ''
    MODE: str = 'dev'  # 'dev8', 'prod'
    """
    MODE (str) = определяет конечную точку API
    принимаемые значения:
    `dev` - dev.emil_design.com prestashop 1.7
    `dev8` - dev8.emil_design.com prestashop 8
    `prod` - emil_design.com prestashop 1.7 <- ⚠️ Внимание!  Рабочий магазин!
    """
    POST_FORMAT = 'JSON'
    API_DOMAIN: str = ''
    API_KEY: str = ''

    if USE_ENV:
        from dotenv import load_dotenv

        load_dotenv()
        API_DOMAIN = os.getenv('HOST')
        API_KEY = os.getenv('API_KEY')

    elif MODE == 'dev':
        API_DOMAIN = gs.credentials.presta.client.dev_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev_emil_design.api_key

    elif MODE == 'dev8':
        API_DOMAIN = gs.credentials.presta.client.dev8_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev8_emil_design.api_key

    elif MODE == 'prod':
        API_DOMAIN = gs.credentials.presta.client.emil_design.api_domain
        API_KEY = gs.credentials.presta.client.emil_design.api_key

    else:
        # `DEV` для API устанавливается если MODE пустой или имеет невалидное значение
        MODE = 'dev'
        API_DOMAIN = gs.credentials.presta.client.dev_emil_design.api_domain
        API_KEY = gs.credentials.presta.client.dev_emil_design.api_key


class PrestaShop:
    """
    Класс для взаимодействия с PrestaShop webservice API, используя JSON и XML для сообщений.

    Этот класс предоставляет методы для взаимодействия с PrestaShop API, позволяя выполнять CRUD
    операции, поиск и загрузку изображений. Он также обеспечивает обработку ошибок для ответов
    и методы для обработки данных API.

    Args:
        api_key (str): API ключ, сгенерированный в PrestaShop.
        api_domain (str): Домен магазина PrestaShop (например, https://myPrestaShop.com).
        data_format (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
        default_lang (int): ID языка по умолчанию. По умолчанию 1.
        debug (bool): Активировать режим отладки. По умолчанию True.

    Raises:
        PrestaShopAuthenticationError: Если API ключ неверный или не существует.
        PrestaShopException: Для общих ошибок PrestaShop WebServices.
    """

    client: Session = Session()
    debug: bool = True
    language: Optional[int] = None
    data_format: str = Config.POST_FORMAT  # Формат данных по умолчанию ('JSON' или 'XML')
    ps_version: str = ''
    api_domain: str
    api_key: str

    def __init__(
        self,
        api_key: str,
        api_domain: str,
        data_format: str = Config.POST_FORMAT,
        default_lang: int = 1,
        debug: bool = False,
    ) -> None:
        """
        Инициализация класса PrestaShop.

        Args:
            data_format (str): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
            default_lang (int): ID языка по умолчанию. По умолчанию 1.
            debug (bool): Активировать режим отладки. По умолчанию True.
        """
        self.api_domain = api_domain + '/api/'
        self.api_key = api_key
        self.debug = debug
        self.language = default_lang
        self.data_format = data_format

        if not self.client.auth:
            self.client.auth = (self.api_key, '')

        response: requests.Response = self.client.request(method='HEAD', url=self.api_domain)
        if not response.ok:
            logger.error(f'Нет соединения. {response.reason=}')
            ...
        self.ps_version = response.headers.get('psws-version')

    def ping(self) -> bool:
        """
        Проверка работоспособности веб-сервиса.

        Returns:
            bool: Результат проверки. Возвращает `True`, если веб-сервис работает, иначе `False`.
        """
        response: requests.Response = self.client.request(method='HEAD', url=self.api_domain)

        return self._check_response(response.status_code, response)

    def _check_response(
        self,
        status_code: int,
        response: requests.Response,
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> bool:
        """
        Проверка статус кода ответа и обработка ошибок.

        Args:
            status_code (int): HTTP статус код ответа.
            response (requests.Response): Объект HTTP ответа.
            method (Optional[str]): HTTP метод, использованный для запроса.
            url (Optional[str]): URL запроса.
            headers (Optional[dict]): Заголовки, использованные в запросе.
            data (Optional[dict]): Данные, отправленные в запросе.

        Returns:
            bool: `True`, если статус код 200 или 201, иначе `False`.
        """
        if status_code in (200, 201):
            return True
        else:
            self._parse_response_error(response, method, url, headers, data)
            return False

    def _parse_response_error(
        self,
        response: requests.Response,
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> None:
        """
        Обработка ошибки в ответе от PrestaShop API.

        Args:
            response (requests.Response): Объект HTTP ответа от сервера.
        """

        if Config.POST_FORMAT == 'JSON':
            status_code: int = response.status_code
            if not status_code in (200, 201):
                j_dumps(response.json())

                logger.error(
                    f"""
                response status code: {status_code}
                    {response.request.url=}
                    --------------
                    response.headers {print(response.headers)}
                    --------------
                    response: {print(response)}
                    --------------
                    response text: {print(response.json())}""",
                    None,
                    False,
                )
            return response
        else:
            error_answer: dict | ElementTree.Element = self._parse_response(response)
            if isinstance(error_answer, dict):
                error_content: dict = (
                    error_answer.get('PrestaShop', {}).get('errors', {}).get('error', {})
                )
                if isinstance(error_content, list):
                    error_content = error_content[0]
                code: str = error_content.get('code')
                message: str = error_content.get('message')
            elif isinstance(error_answer, ElementTree.Element):
                error: ElementTree.Element = error_answer.find('errors/error')
                code: str = error.find('code').text
                message: str = error.find('message').text
            logger.error(f'XML response error: {message} \n Code: {code}')
            return code, message

    def _prepare_url(self, url: str, params: dict) -> str:
        """
        Подготовка URL для запроса.

        Args:
            url (str): Базовый URL.
            params (dict): Параметры для запроса.

        Returns:
            str: Подготовленный URL с параметрами.
        """
        req: PreparedRequest = PreparedRequest()
        req.prepare_url(url, params)
        return req.url

    def _exec(
        self,
        resource: str,
        resource_id: Optional[int | str] = None,
        resource_ids: Optional[int | Tuple[int]] = None,
        method: str = 'GET',
        data: Optional[dict | str] = None,
        headers: Optional[dict] = None,
        search_filter: Optional[str | dict] = None,
        display: Optional[str | list] = 'full',
        schema: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[str] = None,
        language: Optional[int] = None,
        data_format: str = Config.POST_FORMAT,
        **kwargs,
    ) -> Optional[dict]:
        """Выполнение HTTP запроса к PrestaShop API."""

        try:
            HTTPConnection.debuglevel = self.debug  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ debug
            url: str = self._prepare_url(
                f'{self.api_domain}{resource}/{resource_id}' if resource_id else f'{self.api_domain}{resource}',
                {
                    'filter': search_filter,
                    'display': display,
                    'schema': schema,
                    'sort': sort,
                    'limit': limit,
                    'language': language,
                    'output_format': data_format,
                },
            )

            # устанавливаем Content-Type: application/json
            request_headers: dict = (
                {'Content-Type': 'application/json', 'Accept': 'application/json'}
                if data_format == 'JSON'
                else {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
            )

            if headers:
                request_headers.update(headers)

            response: requests.Response = self.client.request(
                method=method,
                url=url,
                data=data,
                headers=request_headers,  # Как минимум заголовок Content-Type JSON/XML
            )

            if not self._check_response(
                response.status_code, response, method, url, request_headers, data
            ):
                logger.error(
                    f"""Ошибка ответа: {response.status_code}
                response = 
                {print(response.headers)}
                {print(response.text)}"""
                )
                ...
                return False

            return self._parse_response(response)

        except Exception as ex:
            logger.error(f'Error:', ex)
            return

    def _parse_response(self, response: Response) -> dict | None:
        """
        Преобразование XML или JSON ответа от API в структуру dict.

        Args:
            text (str): Текст ответа.

        Returns:
            dict: Преобразованные данные или `False` в случае неудачи.
        """

        try:
            data: dict = response.json()  # if self.data_format == 'JSON' else xml2dict(response.text)
            return data.get('prestashop', {}) if 'prestashop' in data else data

        except Exception as ex:
            logger.error(f'Parsing Error:', ex)
            ...
            return {}

    def create(self, resource: str, data: dict, *args, **kwargs) -> Optional[dict]:
        """
        Создание нового ресурса в PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'products').
            data (dict): Данные для нового ресурса.

        Returns:
            dict: Ответ от API.
        """
        # data  = {'prestashop' : data}
        return self._exec(resource=resource, method='POST', data=data, *args, **kwargs)

    def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
        """
        Чтение ресурса из PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            dict: Ответ от API.
        """
        return self._exec(resource=resource, resource_id=resource_id, method='GET', **kwargs)

    def write(self, resource: str, resource_id: int | str, data: dict, **kwargs) -> Optional[dict]:
        """
        Обновление существующего ресурса в PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'products').
            data (dict): Данные для ресурса.

        Returns:
            dict: Ответ от API.
        """
        return self._exec(
            resource=resource,
            resource_id=resource_id,
            method='PUT',
            data=data,
            **kwargs,
        )

    def unlink(self, resource: str, resource_id: int | str) -> bool:
        """
        Удаление ресурса из PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            bool: `True`, если успешно, `False` иначе.
        """
        return self._exec(resource=resource, resource_id=resource_id, method='DELETE')

    def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
        """
        Поиск ресурсов в PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'products').
            filter (Optional[str  |  dict]): Фильтр для поиска.

        Returns:
            List[dict]: Список ресурсов, соответствующих критериям поиска.
        """
        return self._exec(resource=resource, search_filter=filter, method='GET', **kwargs)

    def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
        """Загрузка бинарного файла в ресурс PrestaShop API."""

        try:
            with open(file_path, 'rb') as file:
                files: dict = {
                    'image': (file_name, file, 'image/jpeg')
                }  # Замените 'image/jpeg' на правильный MIME-тип
                response: requests.Response = self.client.post(
                    url=f'{self.api_domain}/images/{resource}',
                    files=files,
                    auth=self.client.auth,  # Важно передавать аутентификацию,
                )

                response.raise_for_status()  # Проверка на HTTP-ошибки

                # return response.json()
                return self._parse_response(response=response, data_format='XML')

        except RequestException as ex:
            logger.error(f'Ошибка при загрузке изображения:', ex)
            return {'error': str(ex)}

        except Exception as ex:
            logger.error(f'Error:', ex)
            return {'error': str(ex)}

    def get_schema(
        self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwargs
    ) -> dict | None:
        """
        Получение схемы заданного ресурса из PrestaShop API.

        Args:
            resource (str): Имя ресурса (например, 'products', 'customers').
                Если не указано - вернется список всех схем сущностей доступных для API ключа
            resource_id (Optinal[str]):
            schema (Optional[str]): обычно подразумеваются следующие опции:
                - blank: (Самая распространенная опция, как и в вашем коде)
                    Возвращает пустую схему ресурса. Это полезно для определения минимального набора полей,
                    необходимых для создания нового объекта. То есть возвращает структуру XML или JSON с пустыми полями,
                    которые можно заполнить данными.
                - synopsis (или simplified): В некоторых версиях и для некоторых ресурсов может существовать опция,
                    возвращающая упрощенную схему. Она может содержать только основные поля ресурса и их типы.
                    Это может быть удобнее, чем полная схема, если вам не нужны все детали.
                - full (или без указания schema): Часто, если параметр schema не указан,
                    или если он указан как full, возвращается полная схема ресурса. Она включает все поля, их типы,
                    возможные значения, описания и другие метаданные. Это самый подробный вид схемы.
                - form (или что-то подобное): Реже, но может быть опция, возвращающая схему,
                    оптимизированную для отображения в форме редактирования. Она может включать информацию о валидации
                    полей, порядке отображения и т.п.

        Returns:
            dict  |  None: Схема запрошенного ресурса или `None` в случае ошибки.
        """
        return self._exec(resource=resource, resource_id=resource_id, schema=schema, method="GET", **kwargs)

    def get_data(self, resource: str, **kwargs) -> Optional[dict]:
        """
        Получение данных из ресурса PrestaShop API и их сохранение.

        Args:
            resource (str): API ресурс (например, 'products').
            **kwargs: Дополнительные аргументы для API запроса.

        Returns:
            dict | None: Данные из API или `False` в случае неудачи.
        """
        return self._exec(resource=resource, method='GET', **kwargs)

    def get_apis(self) -> Optional[dict]:
        """
        Получение списка всех доступных API.

        Returns:
            dict: Список доступных API.
        """
        return self._exec('apis', method='GET', data_format=self.data_format)

    def upload_image_async(
        self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
    ) -> Optional[dict]:
        """
        Асинхронная загрузка изображения в PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (Optional[str]): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае неудачи.
        """
        url_parts: List[str] = img_url.rsplit('.', 1)
        url_without_extension: str = url_parts[0]
        extension: str = url_parts[1] if len(url_parts) > 1 else ''
        filename: str = str(resource_id) + f'_{img_name}.{extension}'
        png_file_path: str = save_image_from_url(img_url, filename)
        response: dict = self.create_binary(resource, png_file_path, img_name)
        self.remove_file(png_file_path)
        return response

    def upload_image_from_url(
        self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
    ) -> Optional[dict]:
        """
        Загрузка изображения в PrestaShop API.

        Args:
            resource (str): API ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (Optional[str]): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае неудачи.
        """
        url_parts: List[str] = img_url.rsplit('.', 1)
        url_without_extension: str = url_parts[0]
        extension: str = url_parts[1] if len(url_parts) > 1 else ''
        filename: str = str(resource_id) + f'_{img_name}.{extension}'
        png_file_path: str = save_image_from_url(img_url, filename)
        response: dict = self.create_binary(resource, png_file_path, img_name)
        self.remove_file(png_file_path)
        return response

    def get_product_images(self, product_id: int) -> Optional[dict]:
        """
        Получение изображений для товара.

        Args:
            product_id (int): ID товара.

        Returns:
            dict | None: Список изображений товара или `False` в случае неудачи.
        """
        return self._exec(f'products/{product_id}/images', method='GET', data_format=self.data_format)



    ####################################################################################################################################





def main() -> None:
    """Проверка сущностей Prestashop"""
    data: dict = {
        'tax': {
            'rate': 3.000,
            'active': '1',
            'name': {
                'language': {
                    'attrs': {'id': '1'},
                    'value': '3% tax',
                }
            },
        }
    }
    api: PrestaShop = PrestaShop(
        api_domain=Config.API_DOMAIN,
        api_key=Config.API_KEY,
        default_lang=1,
        debug=True,
        data_format=Config.POST_FORMAT,
    )
    api.create('taxes', data)
    api.write('taxes', data)

if __name__ == '__main__':
    main()