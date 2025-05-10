### **Анализ кода модуля `api_async.py`**

## \file hypotez/src/endpoints/prestashop/api/api_async.py
# -*- coding: utf-8 -*-

Асинхронный класс для взаимодействия с API PrestaShop
=====================================================

Модуль содержит асинхронтный класс `PrestaShopAsync`, который используется для взаимодействия с API PrestaShop.
Он предоставляет методы для выполнения CRUD-операций, поиска и загрузки изображений.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Асинхронный код, что позволяет выполнять неблокирующие операции.
  - Использование `aiohttp` для асинхронных запросов.
  - Поддержка форматов JSON и XML.
  - Реализация основных методов CRUD для работы с API PrestaShop.
- **Минусы**:
  - Некоторые docstring написаны на английском языке.
  - Отсутствуют примеры использования в docstring для некоторых методов.
  - Не все переменные аннотированы типами.
  - Есть закомментированный код в методе `_exec`.

**Рекомендации по улучшению**:

1.  **Документация**:
    *   Перевести все docstring на русский язык.
    *   Добавить примеры использования в docstring для всех методов, где это уместно.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
3.  **Логирование**:
    *   Улучшить логирование ошибок, добавив больше контекстной информации.
4.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках обработки исключений.
5.  **Удаление неиспользуемого кода**:
    *   Удалить закомментированный код в методе `_exec` или добавить комментарии, объясняющие его назначение.
6.  **Форматирование**:
    *   Убедиться, что код соответствует стандартам PEP8.
7.  **Использовать `j_loads` или `j_loads_ns`**:

    *   Для чтения JSON или конфигурационных файлов замени стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

**Оптимизированный код**:

```python
import os
import sys
from enum import Enum
from http.client import HTTPConnection
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError

from requests import Session
from requests.models import PreparedRequest

import header
from src import gs
from src.logger.exceptions import PrestaShopAuthenticationError, PrestaShopException
from src.logger.logger import logger
from src.utils.convertors.base64 import base64_to_tmpfile
from src.utils.convertors.dict import dict2xml
from src.utils.convertors.xml2dict import xml2dict
from src.utils.file import save_text_file
from src.utils.image import save_image_from_url_async
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint

import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout


class Format(Enum):
    """Типы данных, возвращаемые API (JSON, XML).

    Args:
        Enum: (int): 1 => JSON, 2 => XML
    """
    JSON = 'JSON'
    XML = 'XML'


class PrestaShopAsync:
    """Асинхронный класс для взаимодействия с API PrestaShop с использованием JSON и XML.

    Этот класс предоставляет асинхронные методы для взаимодействия с API PrestaShop,
    позволяя выполнять CRUD-операции, поиск и загрузку изображений. Он также предоставляет
    обработку ошибок для ответов и методы для обработки данных API.

    Пример использования:

    .. code-block:: python

        async def main():
            api = PrestaShopAsync(
                API_DOMAIN='https://your-prestashop-domain.com',
                API_KEY='your_api_key',
                data_format='JSON',
                debug=True,
            )

            await api.ping()

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

            # Создание записи налога
            rec = await api.create('taxes', data)

            # Обновление той же записи налога
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

            update_rec = await api.write('taxes', update_data)

            # Удаление этого налога
            await api.unlink('taxes', str(rec['id']))

            # Поиск первых 3 налогов с '5' в названии
            import pprint
            recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')

            for rec in recs:
                pprint(rec)

            # Создание бинарного файла (изображение товара)
            await api.create_binary('images/products/22', 'img.jpeg', 'image')

        if __name__ == "__main__":
            asyncio.run(main())

    """
    client: ClientSession = None
    debug: bool = False
    lang_index: Optional[int] = 1
    data_format: str = 'JSON'
    ps_version: str = ''
    API_DOMAIN: str = None
    API_KEY: str = None

    def __init__(
        self,
        api_domain: str,
        api_key: str,
        data_format: str = 'JSON',
        debug: bool = True
    ) -> None:
        """Инициализация класса PrestaShopAsync.

        Args:
            api_domain (str): Домен API PrestaShop.
            api_key (str): Ключ API PrestaShop.
            data_format (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). Defaults to 'JSON'.
            debug (bool, optional): Активировать режим отладки. Defaults to True.

        Raises:
            PrestaShopAuthenticationError: Если API-ключ неверен или не существует.
            PrestaShopException: Для общих ошибок веб-сервисов PrestaShop.
        """
        self.API_DOMAIN = api_domain
        self.API_KEY = api_key
        self.debug = debug
        self.data_format = data_format

        self.client = ClientSession(
            auth=aiohttp.BasicAuth(self.API_KEY, ''),
            timeout=ClientTimeout(total=60)
        )

    async def ping(self) -> bool:
        """Проверка работоспособности веб-сервиса асинхронно.

        Returns:
            bool: Результат проверки. Возвращает `True`, если веб-сервис работает, иначе `False`.
        """
        async with self.client.request(
            method='HEAD',
            url=self.API_DOMAIN
        ) as response:
            return await self._check_response(response.status, response)

    def _check_response(
        self,
        status_code: int,
        response: aiohttp.ClientResponse,
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None
    ) -> bool:
        """Проверка кода состояния ответа и обработка ошибок асинхронно.

        Args:
            status_code (int): Код состояния HTTP-ответа.
            response (aiohttp.ClientResponse): Объект HTTP-ответа.
            method (str, optional): HTTP-метод, использованный для запроса.
            url (str, optional): URL запроса.
            headers (dict, optional): Заголовки, использованные в запросе.
            data (dict, optional): Данные, отправленные в запросе.

        Returns:
            bool: `True`, если код состояния 200 или 201, иначе `False`.
        """
        if status_code in (200, 201):
            return True
        else:
            self._parse_response_error(response, method, url, headers, data)
            return False

    def _parse_response_error(
        self,
        response: aiohttp.ClientResponse,
        method: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
        data: Optional[dict] = None
    ):
        """Разбор ответа об ошибке от API PrestaShop асинхронно.

        Args:
            response (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
            method (str, optional): HTTP-метод, использованный для запроса.
            url (str, optional): URL запроса.
            headers (dict, optional): Заголовки, использованные в запросе.
            data (dict, optional): Данные, отправленные в запросе.
        """
        if self.data_format == 'JSON':
            status_code = response.status
            if not status_code in (200, 201):
                text = await response.text()
                logger.critical(
                    f'response status code: {status_code}\n'
                    f'url: {response.request_info.url}\n'
                    f'--------------\n'
                    f'headers: {response.headers}\n'
                    f'--------------\n'
                    f'response text: {text}'
                )
            return response
        else:
            error_answer = self._parse(await response.text())
            if isinstance(error_answer, dict):
                error_content = (
                    error_answer
                    .get('PrestaShop', {})
                    .get('errors', {})
                    .get('error', {})
                )
                if isinstance(error_content, list):
                    error_content = error_content[0]
                code = error_content.get('code')
                message = error_content.get('message')
            elif isinstance(error_answer, ElementTree.Element):
                error = error_answer.find('errors/error')
                code = error.find('code').text
                message = error.find('message').text
            logger.error(f'XML response error: {message} \n Code: {code}')
            return code, message

    def _prepare(self, url: str, params: dict) -> str:
        """Подготовка URL для запроса.

        Args:
            url (str): Базовый URL.
            params (dict): Параметры для запроса.

        Returns:
            str: Подготовленный URL с параметрами.
        """
        req = PreparedRequest()
        req.prepare_url(url, params)
        return req.url

    async def _exec(
        self,
        resource: str,
        resource_id: Optional[Union[int, str]] = None,
        resource_ids: Optional[Union[int, Tuple[int]]] = None,
        method: str = 'GET',
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        search_filter: Optional[Union[str, dict]] = None,
        display: Optional[Union[str, list]] = 'full',
        schema: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[str] = None,
        language: Optional[int] = None,
        io_format: str = 'JSON'
    ) -> Optional[dict]:
        """Выполнение HTTP-запроса к API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products', 'categories').
            resource_id (int | str, optional): ID ресурса.
            resource_ids (int | tuple, optional): ID нескольких ресурсов.
            method (str, optional): HTTP-метод (GET, POST, PUT, DELETE).
            data (dict, optional): Данные для отправки с запросом.
            headers (dict, optional): Дополнительные заголовки для запроса.
            search_filter (str | dict, optional): Фильтр для запроса.
            display (str | list, optional): Поля для отображения в ответе.
            schema (str, optional): Схема данных.
            sort (str, optional): Параметр сортировки для запроса.
            limit (str, optional): Лимит результатов для запроса.
            language (int, optional): ID языка для запроса.
            io_format (str, optional): Формат данных ('JSON' или 'XML').

        Returns:
            dict | None: Ответ от API или `False` в случае неудачи.
        """
        self.debug = False
        if self.debug:
            # import sys
            # original_stderr = sys.stderr
            # f = open('stderr.log', 'w')
            # sys.stderr = f
            
            # prepared_url = self._prepare(f'{self.API_DOMAIN}/api/{resource}/{resource_id}' if resource_id else f'{self.API_DOMAIN}/api/{resource}',
            #                       {'filter': search_filter,
            #                        'display': display,
            #                        'schema': schema,
            #                        'sort': sort,
            #                        'limit': limit,
            #                        'language': language,
            #                        'output_format': io_format})
            
            # request_data = dict2xml(data) if data and io_format == 'XML' else data
            
            # with self.client.request(
            #     method=method,
            #     url=prepared_url,
            #     data=request_data,
            #     headers=headers,
            # ) as response:

            #     sys.stderr = original_stderr

            #     if not self._check_response(response.status, response, method, prepared_url, headers, request_data):
            #         return False

            #     if io_format == 'JSON':
            #         return response.json()
            #     else:
            #         return self._parse(await response.text())
            ...
        else:
            prepared_url = self._prepare(
                f'{self.API_DOMAIN}{resource}/{resource_id}' if resource_id else f'{self.API_DOMAIN}{resource}',
                {
                    'filter': search_filter,
                    'display': display,
                    'schema': schema,
                    'sort': sort,
                    'limit': limit,
                    'language': language,
                    'output_format': io_format
                }
            )
            
            request_data = dict2xml(data) if data and io_format == 'XML' else data
            
            async with self.client.request(
                method=method,
                url=prepared_url,
                data=request_data,
                headers=headers,
            ) as response:

                if not self._check_response(response.status, response, method, prepared_url, headers, request_data):
                    return False

                if io_format == 'JSON':
                    return await response.json()
                else:
                    return self._parse(await response.text())

    def _parse(self, text: str) -> dict | ElementTree.Element | bool:
        """Разбор XML или JSON ответа от API асинхронно.

        Args:
            text (str): Текст ответа.

        Returns:
            dict | ElementTree.Element | bool: Разобранные данные или `False` в случае неудачи.
        """
        try:
            if self.data_format == 'JSON':
                data = j_loads(text)
                return data.get('PrestaShop', {}) if 'PrestaShop' in data else data
            else:
                tree = ElementTree.fromstring(text)
                return tree
        except (ExpatError, ValueError) as ex:
            logger.error(f'Parsing Error: {str(ex)}', ex, exc_info=True)
            return False

    async def create(self, resource: str, data: dict) -> Optional[dict]:
        """Создание нового ресурса в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            data (dict): Данные для нового ресурса.

        Returns:
            dict: Ответ от API.
        """
        return await self._exec(resource=resource, method='POST', data=data, io_format=self.data_format)

    async def read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]:
        """Чтение ресурса из API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            dict: Ответ от API.
        """
        return await self._exec(resource=resource, resource_id=resource_id, method='GET', io_format=self.data_format, **kwargs)

    async def write(self, resource: str, data: dict) -> Optional[dict]:
        """Обновление существующего ресурса в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            data (dict): Данные для ресурса.

        Returns:
            dict: Ответ от API.
        """
        return await self._exec(resource=resource, resource_id=data.get('id'), method='PUT', data=data,
                          io_format=self.data_format)

    async def unlink(self, resource: str, resource_id: Union[int, str]) -> bool:
        """Удаление ресурса из API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            bool: `True` в случае успеха, `False` в противном случае.
        """
        return await self._exec(resource=resource, resource_id=resource_id, method='DELETE', io_format=self.data_format)

    async def search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]:
        """Поиск ресурсов в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            filter (str | dict, optional): Фильтр для поиска.

        Returns:
            List[dict]: Список ресурсов, соответствующих критериям поиска.
        """
        return await self._exec(resource=resource, search_filter=filter, method='GET', io_format=self.data_format, **kwargs)

    async def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
        """Загрузка бинарного файла в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'images/products/22').
            file_path (str): Путь к бинарному файлу.
            file_name (str): Имя файла.

        Returns:
            dict: Ответ от API.
        """
        with open(file_path, 'rb') as file:
            headers = {'Content-Type': 'application/octet-stream'}
            async with self.client.post(
                url=f'{self.API_DOMAIN}{resource}',
                headers=headers,
                data=file.read()
            ) as response:

                return await response.json()

    def _save(self, file_name: str, data: dict):
        """Сохранение данных в файл.

        Args:
            file_name (str): Имя файла.
            data (dict): Данные для сохранения.
        """
        save_text_file(file_name, j_dumps(data, indent=4, ensure_ascii=False))

    async def get_data(self, resource: str, **kwargs) -> Optional[dict]:
        """Получение данных из API PrestaShop и сохранение их асинхронно.

        Args:
            resource (str): API ресурс (например, 'products').
            **kwargs: Дополнительные аргументы для API-запроса.

        Returns:
            dict | None: Данные из API или `False` в случае неудачи.
        """
        data = await self._exec(resource=resource, method='GET', io_format=self.data_format, **kwargs)
        if data:
            self._save(f'{resource}.json', data)
            return data
        return False

    def remove_file(self, file_path: str):
        """Удаление файла из файловой системы.

        Args:
            file_path (str): Путь к файлу.
        """
        try:
            os.remove(file_path)
        except Exception as ex:
            logger.error(f'Error removing file {file_path}: {ex}', ex, exc_info=True)

    async def get_apis(self) -> Optional[dict]:
        """Получение списка всех доступных API асинхронно.

        Returns:
            dict: Список доступных API.
        """
        return await self._exec('apis', method='GET', io_format=self.data_format)

    async def get_languages_schema(self) -> Optional[dict]:
        """Получение схемы для языков асинхронно.

        Returns:
            dict: Схема языков или `None` в случае неудачи.
        """
        try:
            response = await self._exec('languages', display='full', io_format='JSON')
            return response
        except Exception as ex:
            logger.error(f'Error: {ex}', ex, exc_info=True)
            return

    async def upload_image_async(self, resource: str, resource_id: int, img_url: str,
                           img_name: Optional[str] = None) -> Optional[dict]:
        """Загрузка изображения в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (str, optional): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае неудачи.
        """
        url_parts = img_url.rsplit('.', 1)
        url_without_extension = url_parts[0]
        extension = url_parts[1] if len(url_parts) > 1 else ''
        filename = str(resource_id) + f'_{img_name}.{extension}'
        png_file_path = await save_image_from_url_async(img_url, filename)
        response = await self.create_binary(resource, png_file_path, img_name)
        self.remove_file(png_file_path)
        return response

    async def upload_image(self, resource: str, resource_id: int, img_url: str,
                     img_name: Optional[str] = None) -> Optional[dict]:
        """Загрузка изображения в API PrestaShop асинхронно.

        Args:
            resource (str): API ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (str, optional): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае неудачи.
        """
        url_parts = img_url.rsplit('.', 1)
        url_without_extension = url_parts[0]
        extension = url_parts[1] if len(url_parts) > 1 else ''
        filename = str(resource_id) + f'_{img_name}.{extension}'
        png_file_path = await save_image_from_url_async(img_url, filename)
        response = await self.create_binary(resource, png_file_path, img_name)
        self.remove_file(png_file_path)
        return response

    async def get_product_images(self, product_id: int) -> Optional[dict]:
        """Получение изображений товара асинхронно.

        Args:
            product_id (int): ID товара.

        Returns:
            dict | None: Список изображений товара или `False` в случае неудачи.
        """
        return await self._exec(f'products/{product_id}/images', method='GET', io_format=self.data_format)