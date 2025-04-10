### **Анализ кода модуля `api_async.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Асинхронная реализация для неблокирующих операций.
    - Использование `aiohttp` для асинхронных HTTP-запросов.
    - Обработка ошибок и логирование с использованием `logger`.
    - Разделение ответственности между методами (например, `_exec`, `_parse`, `_check_response`).
- **Минусы**:
    - Смешанный стиль документации (иногда отсутствует перевод на русский).
    - Не все методы имеют полное описание в docstring.
    - Отсутствие аннотаций типов для некоторых переменных и возвращаемых значений.
    - Не везде используется `logger.error` для логирования ошибок.
    - Некоторые участки кода закомментированы (например, в методе `_exec`).
    - Не используется `ex` в блоках `except` для логирования ошибок.
    - Не во всех функциях описаны `Raises`.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавить заголовок модуля с кратким описанием содержимого.
    *   Перевести все docstring на русский язык.
    *   Заполнить отсутствующие описания аргументов, возвращаемых значений и исключений в docstring.
    *   Добавить примеры использования для основных методов.

2.  **Обработка ошибок**:
    *   Использовать `logger.error(..., ex, exc_info=True)` для логирования ошибок с трассировкой.
    *   Убедиться, что все исключения обрабатываются и логируются.
    *   Описать возможные исключения в секции `Raises` docstring.

3.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений, где это необходимо.

4.  **Форматирование**:
    *   Использовать одинарные кавычки для строк.

5.  **Удаление неиспользуемого кода**:
    *   Удалить или пересмотреть закомментированные участки кода (например, в методе `_exec`).

6.  **Использование `j_loads`**:
    *   Убедиться, что для чтения JSON используется `j_loads`.

**Оптимизированный код:**

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

import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout


class Format(Enum):
    """Типы данных возврата (JSON, XML)

    Поддерживается только JSON

    Args:
        Enum: (int): 1 => JSON, 2 => XML
    """
    JSON = 'JSON'
    XML = 'XML'


class PrestaShopAsync:
    """Асинхронный класс для взаимодействия с API PrestaShop с использованием JSON и XML.

    Этот класс предоставляет асинхронные методы для взаимодействия с API PrestaShop,
    обеспечивая CRUD-операции, поиск и загрузку изображений. Он также обеспечивает
    обработку ошибок для ответов и методы для обработки данных API.

    Пример использования:

    .. code-block:: python

        async def main():
            api = PrestaShopAsync(
                API_DOMAIN='https://your-prestashop-domain.com',
                API_KEY='your_api_key',
                default_lang=1,
                debug=True,
                data_format='JSON',
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

            # Create tax record
            rec = await api.create('taxes', data)

            # Update the same tax record
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

            # Remove this tax
            await api.unlink('taxes', str(rec['id']))

            # Search the first 3 taxes with '5' in the name
            import pprint
            recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')

            for rec in recs:
                pprint(rec)

            # Create binary (product image)
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

    def __init__(self,
                 api_domain: str,
                 api_key: str,
                 data_format: str = 'JSON',
                 debug: bool = True) -> None:
        """Инициализирует класс PrestaShopAsync.

        Args:
            api_domain (str): Домен API PrestaShop.
            api_key (str): Ключ API PrestaShop.
            data_format (str, optional): Формат данных ('JSON' или 'XML'). Defaults to 'JSON'.
            debug (bool, optional): Активировать режим отладки. Defaults to True.

        Raises:
            PrestaShopAuthenticationError: Если API-ключ неверный или не существует.
            PrestaShopException: Для общих ошибок PrestaShop WebServices.
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
        """Проверяет, работает ли веб-сервис асинхронно.

        Returns:
            bool: Результат проверки связи. Возвращает `True`, если веб-сервис работает, иначе `False`.
        """
        async with self.client.request(
            method='HEAD',
            url=self.API_DOMAIN
        ) as response:
            return await self._check_response(response.status, response)

    def _check_response(self, status_code: int, response, method: Optional[str] = None, url: Optional[str] = None,
                        headers: Optional[dict] = None, data: Optional[dict] = None) -> bool:
        """Проверяет код состояния ответа и обрабатывает ошибки асинхронно.

        Args:
            status_code (int): Код состояния HTTP-ответа.
            response (aiohttp.ClientResponse): Объект HTTP-ответа.
            method (str, optional): HTTP-метод, используемый для запроса.
            url (str, optional): URL запроса.
            headers (dict, optional): Заголовки, используемые в запросе.
            data (dict, optional): Данные, отправленные в запросе.

        Returns:
            bool: `True`, если код состояния равен 200 или 201, иначе `False`.
        """
        if status_code in (200, 201):
            return True
        else:
            self._parse_response_error(response, method, url, headers, data)
            return False

    def _parse_response_error(self, response, method: Optional[str] = None, url: Optional[str] = None,
                              headers: Optional[dict] = None, data: Optional[dict] = None):
        """Разбирает ответ об ошибке от API PrestaShop асинхронно.

        Args:
            response (aiohttp.ClientResponse): Объект HTTP-ответа от сервера.
            method (str, optional): HTTP-метод, используемый для запроса.
            url (str, optional): URL запроса.
            headers (dict, optional): Заголовки, используемые в запросе.
            data (dict, optional): Данные, отправленные в запросе.
        """
        if self.data_format == 'JSON':
            status_code = response.status
            if not status_code in (200, 201):
                text = response.text()
                logger.critical(f'response status code: {status_code}\n'
                                f'url: {response.request_info.url}\n'
                                f'--------------\n'
                                f'headers: {response.headers}\n'
                                f'--------------\n'
                                f'response text: {text}')
            return response
        else:
            error_answer = self._parse(response.text())
            if isinstance(error_answer, dict):
                error_content = (error_answer
                                 .get('PrestaShop', {})
                                 .get('errors', {})
                                 .get('error', {}))
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
        """Подготавливает URL для запроса.

        Args:
            url (str): Базовый URL.
            params (dict): Параметры для запроса.

        Returns:
            str: Подготовленный URL с параметрами.
        """
        req = PreparedRequest()
        req.prepare_url(url, params)
        return req.url

    async def _exec(self,
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
              io_format: str = 'JSON') -> Optional[dict]:
        """Выполняет HTTP-запрос к API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products', 'categories').
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
            dict | None: Ответ от API или `False` в случае ошибки.

        Raises:
            aiohttp.ClientError: При ошибках, связанных с HTTP-клиентом.
            PrestaShopException: При других ошибках API PrestaShop.
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
            prepared_url = self._prepare(f'{self.API_DOMAIN}{resource}/{resource_id}' if resource_id else f'{self.API_DOMAIN}{resource}',
                                  {'filter': search_filter,
                                   'display': display,
                                   'schema': schema,
                                   'sort': sort,
                                   'limit': limit,
                                   'language': language,
                                   'output_format': io_format})
            
            request_data = dict2xml(data) if data and io_format == 'XML' else data
            
            try:
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
            except aiohttp.ClientError as ex:
                logger.error(f'Ошибка при выполнении запроса: {ex}', exc_info=True)
                return None
            except Exception as ex:
                logger.error(f'Неожиданная ошибка: {ex}', exc_info=True)
                return None

    def _parse(self, text: str) -> dict | ElementTree.Element | bool:
        """Разбирает XML или JSON-ответ от API асинхронно.

        Args:
            text (str): Текст ответа.

        Returns:
            dict | ElementTree.Element | bool: Разобранные данные или `False` в случае ошибки.

        Raises:
            ExpatError: При ошибке парсинга XML.
            ValueError: При ошибке парсинга JSON.
        """
        try:
            if self.data_format == 'JSON':
                data = j_loads(text)
                return data.get('PrestaShop', {}) if 'PrestaShop' in data else data
            else:
                tree = ElementTree.fromstring(text)
                return tree
        except (ExpatError, ValueError) as ex:
            logger.error(f'Ошибка парсинга: {str(ex)}', exc_info=True)
            return False

    async def create(self, resource: str, data: dict) -> Optional[dict]:
        """Создает новый ресурс в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            data (dict): Данные для нового ресурса.

        Returns:
             dict: Ответ от API.

        Raises:
            PrestaShopException: При ошибке создания ресурса.
        """
        return await self._exec(resource=resource, method='POST', data=data, io_format=self.data_format)

    async def read(self, resource: str, resource_id: Union[int, str], **kwargs) -> Optional[dict]:
        """Читает ресурс из API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            dict: Ответ от API.

        Raises:
            PrestaShopException: При ошибке чтения ресурса.
        """
        return await self._exec(resource=resource, resource_id=resource_id, method='GET', io_format= self.data_format)

    async def write(self, resource: str, data: dict) -> Optional[dict]:
        """Обновляет существующий ресурс в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            data (dict): Данные для ресурса.

        Returns:
            dict: Ответ от API.

        Raises:
            PrestaShopException: При ошибке обновления ресурса.
        """
        return await self._exec(resource=resource, resource_id=data.get('id'), method='PUT', data=data,
                          io_format=self.data_format)

    async def unlink(self, resource: str, resource_id: Union[int, str]) -> bool:
        """Удаляет ресурс из API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            resource_id (int | str): ID ресурса.

        Returns:
            bool: `True` в случае успеха, `False` в противном случае.

        Raises:
            PrestaShopException: При ошибке удаления ресурса.
        """
        return await self._exec(resource=resource, resource_id=resource_id, method='DELETE', io_format=self.data_format)

    async def search(self, resource: str, filter: Optional[Union[str, dict]] = None, **kwargs) -> List[dict]:
        """Ищет ресурсы в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            filter (str | dict, optional): Фильтр для поиска.

        Returns:
             List[dict]: Список ресурсов, соответствующих критериям поиска.

        Raises:
            PrestaShopException: При ошибке поиска ресурсов.
        """
        return await self._exec(resource=resource, search_filter=filter, method='GET', io_format=self.data_format, **kwargs)

    async def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
        """Загружает двоичный файл в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'images/products/22').
            file_path (str): Путь к двоичному файлу.
            file_name (str): Имя файла.

        Returns:
            dict: Ответ от API.

        Raises:
            PrestaShopException: При ошибке загрузки двоичного файла.
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
        """Сохраняет данные в файл.

        Args:
            file_name (str): Имя файла.
            data (dict): Данные для сохранения.
        """
        save_text_file(file_name, j_dumps(data, indent=4, ensure_ascii=False))

    async def get_data(self, resource: str, **kwargs) -> Optional[dict]:
        """Получает данные из API PrestaShop и сохраняет их асинхронно.

        Args:
            resource (str): API-ресурс (например, 'products').
            **kwargs: Дополнительные аргументы для API-запроса.

        Returns:
            dict | None: Данные из API или `False` в случае ошибки.

        Raises:
            PrestaShopException: При ошибке получения данных.
        """
        data = await self._exec(resource=resource, method='GET', io_format=self.data_format, **kwargs)
        if data:
            self._save(f'{resource}.json', data)
            return data
        return False

    def remove_file(self, file_path: str):
        """Удаляет файл из файловой системы.

        Args:
            file_path (str): Путь к файлу.
        """
        try:
            os.remove(file_path)
        except Exception as ex:
            logger.error(f'Ошибка при удалении файла {file_path}: {ex}', exc_info=True)

    async def get_apis(self) -> Optional[dict]:
        """Получает список всех доступных API асинхронно.

        Returns:
             dict: Список доступных API.

        Raises:
            PrestaShopException: При ошибке получения списка API.
        """
        return await self._exec('apis', method='GET', io_format=self.data_format)

    async def get_languages_schema(self) -> Optional[dict]:
        """Получает схему для языков асинхронно.

        Returns:
            dict: Схема языка или `None` в случае ошибки.

        Raises:
            PrestaShopException: При ошибке получения схемы языка.
        """
        try:
            response = await self._exec('languages', display='full', io_format='JSON')
            return response
        except Exception as ex:
            logger.error(f'Ошибка: {ex}', exc_info=True)
            return None

    async def upload_image_async(self, resource: str, resource_id: int, img_url: str,
                           img_name: Optional[str] = None) -> Optional[dict]:
        """Загружает изображение в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (str, optional): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае ошибки.

        Raises:
            PrestaShopException: При ошибке загрузки изображения.
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
        """Загружает изображение в API PrestaShop асинхронно.

        Args:
            resource (str): API-ресурс (например, 'images/products/22').
            resource_id (int): ID ресурса.
            img_url (str): URL изображения.
            img_name (str, optional): Имя файла изображения, по умолчанию None.

        Returns:
            dict | None: Ответ от API или `False` в случае ошибки.

        Raises:
            PrestaShopException: При ошибке загрузки изображения.
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
        """Получает изображения для продукта асинхронно.

        Args:
            product_id (int): ID продукта.

        Returns:
            dict | None: Список изображений продукта или `False` в случае ошибки.

        Raises:
            PrestaShopException: При ошибке получения изображений продукта.
        """
        return await self._exec(f'products/{product_id}/images', method='GET', io_format=self.data_format)