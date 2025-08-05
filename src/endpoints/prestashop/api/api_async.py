## \file src/endpoints/prestashop/api_async.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Асинхронный модуль для взаимодействия с PrestaShop API.
=========================================================================================

Этот модуль предоставляет класс `PrestaShopAsync` для взаимодействия с PrestaShop webservice API,
используя JSON и XML для форматирования сообщений. Он поддерживает CRUD операции, поиск,
и загрузку изображений, с обработкой ошибок для ответов в асинхронном режиме.

Примеры использования
-------------

```python
import asyncio
# Предполагается, что Config находится в этом же файле или импортируется корректно
from src.endpoints.prestashop.api_async import PrestaShopAsync, Config 
from src.logger.logger import logger # Для логирования в примере

async def main_example():
    # Замените на ваши данные или настройте Config
    api_domain = 'https://your-prestashop-domain.com'
    api_key = 'your_api_key'
    
    # Пример использования Config, если он настроен
    # api_domain = Config.API_DOMAIN 
    # api_key = Config.API_KEY

    async with PrestaShopAsync(
        api_domain=api_domain,
        api_key=api_key,
        default_lang=1,
        debug=True,
        data_format='JSON', # или 'XML'
    ) as api:

        await api.ping_async()
        logger.info(f'PrestaShop version: {api.ps_version}')


        data = {
            'tax': {
                'rate': '3.000', # Числа часто передаются как строки
                'active': '1',
                'name': {
                    'language': { # В PrestaShop часто ожидается массив, даже для одного языка
                        'attrs': {'id': '1'},
                        'value': 'Async 3% tax'
                    }
                }
            }
        }

        # Create tax record
        rec = await api.create_async('taxes', data)
        if not rec or not isinstance(rec.get('tax'), dict) or 'id' not in rec['tax']:
            logger.error(f'Failed to create tax: {rec}')
            return

        tax_id = rec['tax']['id']
        logger.info(f'Created tax with ID: {tax_id}')

        # Update the same tax record
        update_data = {
            'tax': {
                'id': str(tax_id), 
                'rate': '3.500',
                'active': '1',
                'name': {
                    'language': {
                        'attrs': {'id': '1'},
                        'value': 'Async 3.5% tax updated'
                    }
                }
            }
        }
        
        # Для PrestaShop XML API, тело PUT запроса часто оборачивается в <prestashop>
        # payload_for_update = {'prestashop': update_data} if api.data_format == 'XML' else update_data
        # В нашем _exec_async payload передается как есть, dict2xml/json.dumps делают свою работу.

        update_rec = await api.write_async('taxes', str(tax_id), update_data)
        logger.info(f'Updated tax: {update_rec}')

        # Read the tax
        read_rec = await api.read_async('taxes', str(tax_id))
        logger.info(f'Read tax: {read_rec}')

        # Search the first 3 taxes with 'Async' in the name
        # Используется from src.utils.printer import pprint as print
        recs = await api.search_async('taxes', filter={'name': '%Async%'}, limit='3') 

        if recs and recs.get('taxes'):
            # Ответ PrestaShop может быть разным: список или один объект
            taxes_found = recs['taxes'].get('tax', []) 
            if isinstance(taxes_found, dict): # Если один налог, он не в списке
                taxes_found = [taxes_found]
            for r_item in taxes_found: 
                print(r_item) # Используется print (который есть pprint)

        # Remove this tax
        success = await api.unlink_async('taxes', str(tax_id))
        logger.info(f'Deleted tax with ID {tax_id}: {success}')

if __name__ == '__main__':
    # Эта часть для запуска примера, если этот файл выполняется напрямую
    # Убедитесь, что asyncio.run вызывается только один раз на верхнем уровне
    # и что Config настроен или значения передаются напрямую.
    # Пример:
    # class Config: # Dummy Config для примера
    #     API_DOMAIN = "https://your.prestashop.com" # ЗАМЕНИТЕ
    #     API_KEY = "YOURAPIKEY" # ЗАМЕНИТЕ
    #     POST_FORMAT = "JSON"
    #     language = 1 # Добавил для согласованности
        
    asyncio.run(main_example())

```
```rst
  .. module:: src.endpoints.prestashop.api_async
```
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any # Union заменен на |

import httpx 

from xml.etree import ElementTree # Используется только ExpatError
from xml.parsers.expat import ExpatError

# Импорты по умолчанию
import header
from header import __root__
from src import gs

from src.logger.exceptions import PrestaShopAuthenticationError, PrestaShopException
from src.logger.logger import logger
from src.endpoints.prestashop.utils import dict2xml, xml2dict 
from src.utils.file import remove_file_async
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print 

from dataclasses import dataclass, field # field не используется, но оставлен для @dataclass


@dataclass
class Config:
    """
    Класс конфигурации для PrestaShop API.

    Содержит настройки по умолчанию и параметры, необходимые для подключения
    и взаимодействия с API PrestaShop.

    Attributes:
        language (int): ID языка по умолчанию, Используетсяый в запросах к API.
        ps_version (str): Версия PrestaShop. Определяется автоматически при первом подключении.
        MODE (str): Режим работы (например, 'dev', 'prod'). Влияет на выбор конечной точки API, если используется.
        POST_FORMAT (str): Формат данных ('JSON' или 'XML'), Используетсяый для тел запросов POST/PUT.
        API_DOMAIN (str): Базовый URL-адрес магазина PrestaShop (например, 'https://yourshop.com').
        API_KEY (str): Ключ доступа к API PrestaShop.
    """
    language: int = 1
    ps_version: str = ''
    MODE: str = 'dev'
    POST_FORMAT: str = 'XML' 
    API_DOMAIN: str = '' 
    API_KEY: str = '' 


class PrestaShopAsync:
    """
    Асинхронный клиент для взаимодействия с PrestaShop webservice API.

    Этот класс предоставляет методы для выполнения CRUD операций, поиска ресурсов,
    загрузки изображений и получения схем данных через PrestaShop API,
    используя асинхронные HTTP-запросы.

    Args:
        api_key (str): Ключ API, сгенерированный в PrestaShop.
        api_domain (str): Домен магазина PrestaShop (например, 'https://myPrestaShop.com').
        data_format (str, optional): Формат данных по умолчанию ('JSON' или 'XML'). По умолчанию 'JSON'.
        default_lang (int, optional): ID языка по умолчанию. По умолчанию 1.
        debug (bool, optional): Активация режима отладки. По умолчанию `False`.

    Raises:
        PrestaShopAuthenticationError: При ошибке аутентификации (неверный ключ).
        PrestaShopException: При других общих ошибках взаимодействия с PrestaShop API.
    
    Example:
        >>> async def run_example():
        ...     # Замените на реальные данные
        ...     # async with PrestaShopAsync('YOUR_API_KEY', 'https://yourshop.com') as api:
        ...     #     is_ok = await api.ping_async()
        ...     #     print(f'Ping: {is_ok}') # Используется print (pprint)
        ...     pass # Пример требует реального API для выполнения
        >>> # import asyncio
        >>> # asyncio.run(run_example())
    """

    client: httpx.AsyncClient | None = None
    debug: bool = False
    language: int | None = None 
    data_format: str = Config.POST_FORMAT
    ps_version: str | None = None
    api_domain_base: str
    api_key: str
    _initialized: bool = False

    def __init__(
        self,
        api_key: str,
        api_domain: str, 
        data_format: str = Config.POST_FORMAT,
        default_lang: int = 1,
        debug: bool = False,
    ) -> None:
        """
        Инициализация клиента PrestaShop API.

        Args:
            api_key (str): Ключ API PrestaShop.
            api_domain (str): Домен магазина PrestaShop (например, 'https://shop.com'). 
                              Должен быть базовым URL магазина, `/api/` будет добавлено автоматически.
            data_format (str, optional): Формат данных по умолчанию ('JSON' или 'XML').
                                         По умолчанию используется значение из `Config.POST_FORMAT`.
            default_lang (int, optional): ID языка по умолчанию. По умолчанию 1.
            debug (bool, optional): Включение режима отладки. По умолчанию `False`.
        """
        # Нормализация URL api_domain для формирования api_domain_base
        normalized_domain: str = api_domain
        if not normalized_domain.startswith(('http://', 'https://')):
            normalized_domain = 'https://' + normalized_domain # Добавление схемы по умолчанию
        if not normalized_domain.endswith('/'):
            normalized_domain += '/'
        
        # Формирование базового URL для API
        if 'api/' not in normalized_domain.split('/')[-2:]: # Проверка, не содержит ли уже /api/
            self.api_domain_base = normalized_domain + 'api/'
        else: # Если /api/ уже есть (например, https://shop.com/api/)
            self.api_domain_base = normalized_domain
            if not self.api_domain_base.endswith('/'): # Гарантируем слеш в конце
                self.api_domain_base += '/'


        self.api_key = api_key
        self.debug = debug
        self.language = default_lang
        self.data_format = data_format.upper() 
        
        self._initialized = False 


    async def __aenter__(self) -> 'PrestaShopAsync':
        """
        Асинхронный вход в контекстный менеджер.
        Инициализирует HTTP-клиент и выполняет начальное подключение к API.

        Returns:
            PrestaShopAsync: Экземпляр самого себя, готовый к использованию.
        
        Raises:
            PrestaShopException: Если возникает ошибка при инициализации клиента или подключении.
        """
        if not self.client: 
            self.client = httpx.AsyncClient(
                auth=(self.api_key, ''),
                base_url=self.api_domain_base,
                timeout=30.0 
            )
        if not self._initialized:
            await self._initialize_connection()
        return self

    async def _initialize_connection(self) -> None:
        """
        Инициализирует соединение с API PrestaShop.
        Отправляет HEAD-запрос для проверки доступности сервиса и получения версии PrestaShop.
        Этот метод вызывается автоматически при входе в контекстный менеджер или при первом запросе,
        требующем активного соединения.
        
        Raises:
            PrestaShopAuthenticationError: При ошибке аутентификации или если сервис недоступен (401, 403).
            PrestaShopException: При других ошибках сети или запроса (например, таймаут, DNS-ошибка).
        """
        # Функция выполняет инициализацию соединения
        if self._initialized:
            return
        
        if not self.client:
            # Это состояние не должно возникать при использовании через async with
            logger.error('HTTP клиент не инициализирован перед _initialize_connection.')
            raise PrestaShopException('HTTP клиент не инициализирован.')

        try:
            logger.debug(f'Попытка начального HEAD-запроса к {self.api_domain_base}')
            response: httpx.Response = await self.client.head('') 
            response.raise_for_status() 
            self.ps_version = response.headers.get('psws-version')
            logger.info(f'Успешное подключение к PrestaShop. Версия: {self.ps_version}')
            self._initialized = True
        except httpx.HTTPStatusError as ex:
            logger.error(f'HTTP ошибка при начальном подключении: {ex.response.status_code}', ex, exc_info=True) # exc_info=True для HTTPStatusError полезно
            await self._handle_error_response(ex.response) 
            raise PrestaShopAuthenticationError(f'Ошибка подключения или аутентификации: {ex.response.status_code}') from ex
        except httpx.RequestError as ex:
            logger.error('Ошибка запроса при начальном подключении', ex, exc_info=True)
            raise PrestaShopException('Сетевая ошибка или ошибка запроса при инициализации') from ex
        except Exception as ex: 
            logger.error('Неожиданная ошибка при инициализации соединения', ex, exc_info=True)
            raise PrestaShopException('Неожиданная ошибка при инициализации') from ex


    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None:
        """
        Асинхронный выход из контекстного менеджера.
        Гарантирует корректное закрытие HTTP-клиента.

        Args:
            exc_type (type[BaseException] | None): Тип исключения, если оно возникло в блоке `async with`.
            exc_val (BaseException | None): Экземпляр исключения.
            exc_tb (Any | None): Объект трассировки (traceback).
        """
        if self.client: 
            await self.client.aclose()
            self.client = None
        self._initialized = False 


    async def ping_async(self) -> bool:
        """
        Асинхронно проверяет работоспособность веб-сервиса PrestaShop.
        Отправляет HEAD-запрос к корневому эндпоинту API.

        Returns:
            bool: `True`, если сервис доступен и отвечает корректно (статус 2xx), иначе `False`.
        
        Raises:
            PrestaShopException: Если клиент не был инициализирован (например, не используется `async with`).
        """
        # Функция выполняет проверку доступности сервиса
        if not self.client:
            raise PrestaShopException('Клиент не инициализирован. Используй \'async with PrestaShopAsync(...)\'.')
        if not self._initialized: 
            try:
                await self._initialize_connection()
            except PrestaShopException as ex_init: # Ловим ошибки инициализации
                logger.error('Ping неудачен: ошибка при инициализации соединения во время ping.', ex_init, exc_info=False) # exc_info False, т.к. ex_init уже содержит детали
                return False


        try:
            response: httpx.Response = await self.client.head('') 
            return await self._check_response_async(response)
        except httpx.RequestError as ex:
            logger.error('Ping неудачен: ошибка запроса.', ex, exc_info=True)
            return False


    async def _check_response_async(
        self,
        response: httpx.Response,
        method: str | None = None,
        url: str | None = None,
        req_headers: dict | None = None,
        req_data: Any | None = None,
    ) -> bool:
        """
        Проверяет код состояния HTTP-ответа.
        В случае ошибки (статус не 200 и не 201) вызывает `_handle_error_response` для логирования.

        Args:
            response (httpx.Response): Объект ответа HTTP от `httpx`.
            method (str | None, optional): HTTP-метод выполненного запроса (GET, POST, etc.).
            url (str | None, optional): URL-адрес, к которому был выполнен запрос.
            req_headers (dict | None, optional): Заголовки, использованные в запросе.
            req_data (Any | None, optional): Тело данных, отправленное в запросе.

        Returns:
            bool: `True`, если код состояния ответа 200 или 201, иначе `False`.
        """
        # Функция выполняет проверку кода состояния ответа
        if response.status_code in (200, 201):
            return True
        else:
            await self._handle_error_response(response, method, str(url), req_headers, req_data)
            return False

    async def _handle_error_response(
        self,
        response: httpx.Response,
        method: str | None = None,
        url: str | None = None,
        req_headers: dict | None = None,
        req_data: Any | None = None,
    ) -> None:
        """
        Обрабатывает и логирует ответ с ошибкой от PrestaShop API.
        Пытается извлечь детали ошибки из тела ответа (JSON или XML).

        Args:
            response (httpx.Response): Объект HTTP-ответа с ошибкой.
            method (str | None, optional): HTTP-метод запроса.
            url (str | None, optional): URL-адрес запроса.
            req_headers (dict | None, optional): Заголовки запроса.
            req_data (Any | None, optional): Тело запроса.
        """
        # Функция выполняет разбор и логирование ответа с ошибкой
        status_code: int = response.status_code
        error_content_parsed: dict = {}
        error_message_raw: str = ''
        response_text_for_log: str = '(не удалось прочитать тело ответа)' # Значение по умолчанию

        try:
            # Асинхронное чтение тела ответа для лога (ограниченного размера)
            # response.aread() возвращает bytes, декодируем в строку
            response_bytes: bytes = await response.aread() 
            response_text_for_log = response_bytes.decode('utf-8', errors='replace')[:1000] 
        except Exception as ex_read: # Если ошибка при чтении тела
            logger.warning(f'Ошибка при чтении тела ответа для логирования: {ex_read}')


        try:
            content_type_header: str = response.headers.get('content-type', '').lower()
            # Используется уже прочитанный response_text_for_log для парсинга, если это возможно,
            # или позволяем response.json()/response.text() прочитать снова, если нужно.
            # httpx.Response.json() и .text() могут быть вызваны только один раз без предварительного stream.
            # Если мы уже сделали response.aread(), то нужно парсить из полученных байт/текста.

            if 'application/json' in content_type_header:
                try:
                    error_content_parsed = json.loads(response_bytes) # Парсинг из уже прочитанных байт
                    error_message_raw = j_dumps(error_content_parsed)
                except json.JSONDecodeError: # Если из байт не удалось, пробуем response.json()
                    error_content_parsed = await response.json() 
                    error_message_raw = j_dumps(error_content_parsed)

            elif 'application/xml' in content_type_header or 'text/xml' in content_type_header:
                xml_text: str = response_bytes.decode('utf-8', errors='replace') # Используется прочитанные байты
                error_message_raw = xml_text
                parsed_xml_error: dict | list[Any] | None = xml2dict(xml_text)
                if isinstance(parsed_xml_error, dict):
                    error_details: Any = parsed_xml_error.get('prestashop', {}).get('errors', {}).get('error', {})
                    if isinstance(error_details, list): error_details = error_details[0] if error_details else {}
                    
                    code_val: Any = error_details.get('code') if isinstance(error_details, dict) else 'N/A'
                    message_val: Any = error_details.get('message') if isinstance(error_details, dict) else 'No message in XML error.'
                    
                    logger.debug(f'XML API Error Code: {code_val}, Message: {message_val}') # Debug, т.к. основное сообщение ниже
                    error_content_parsed = {'code': code_val, 'message': message_val}
                else:
                    error_content_parsed = {'message': 'Структура XML ошибки не распознана или xml2dict не вернул словарь.'}
            else:
                error_message_raw = response_text_for_log # Используется то, что смогли прочитать
                error_content_parsed = {'message': f'Неизвестный формат ответа или пустой ответ. Content-Type: {content_type_header}'}

        except json.JSONDecodeError as ex_json:
            logger.warning('Ошибка декодирования JSON из ответа с ошибкой.', ex_json)
            error_message_raw = response_text_for_log 
            error_content_parsed = {'message': 'Non-JSON error response received.'}
        except ExpatError as ex_xml: 
            logger.warning('Ошибка разбора XML из ответа с ошибкой.', ex_xml)
            error_message_raw = response_text_for_log
            error_content_parsed = {'message': 'Invalid XML error response received.'}
        except Exception as ex_parse: 
            logger.error('Неожиданная ошибка при разборе ответа с ошибкой', ex_parse, exc_info=True)
            error_message_raw = response_text_for_log
            error_content_parsed = {'message': 'Unexpected error during parsing of error response.'}

        # Формирование лог-сообщения
        log_msg_parts: list[str] = [
            'Ошибка PrestaShop API:',
            f'  Статус код: {status_code}',
            f'  Метод: {method or response.request.method}', # Использование фактического метода из запроса, если method не передан
            f'  URL: {url or str(response.request.url)}',
            f'  Заголовки запроса: {j_dumps(req_headers or dict(response.request.headers))}',
            f'  Тело запроса: {j_dumps(req_data) if req_data else "N/A"}',
            f'  Заголовки ответа: {j_dumps(dict(response.headers))}',
            f'  Тело ответа (часть): {error_message_raw[:500] if error_message_raw else response_text_for_log[:500]}...',
            f'  Разобранная ошибка: {j_dumps(error_content_parsed)}'
        ]
        logger.error('\n'.join(log_msg_parts), None, False) # exc_info=False, т.к. сама ошибка API уже залогирована


    async def _exec_async(
        self,
        resource: str,
        resource_id: int | str | None = None,
        method: str = 'GET',
        payload: dict | str | None = None, 
        params: dict[str, Any] | None = None,
        req_headers: dict | None = None,
        data_format_override: str | None = 'XML',
        **kwargs: Any, 
    ) -> dict | None:
        """
        Выполняет асинхронный HTTP-запрос к PrestaShop API.
        Это основной метод для всех взаимодействий с API.

        Args:
            resource (str): Ресурс API (например, 'products', 'customers', '' для корневого).
            resource_id (int | str | None, optional): ID ресурса.
            method (str, optional): HTTP-метод ('GET', 'POST', 'PUT', 'DELETE'). По умолчанию 'GET'.
            payload (dict | str | None, optional): Тело запроса (для POST, PUT), может быть словарем или строкой.
            params (dict[str, Any] | None, optional): Дополнительные параметры URL.
            req_headers (dict | None, optional): Дополнительные заголовки запроса, переопределяющие стандартные.
            data_format_override (str | None, optional): Переопределение формата данных ('JSON'/'XML') для этого конкретного запроса.
            **kwargs (Any): Дополнительные параметры для URL, такие как `filter`, `display`, `schema`, `sort`, `limit`, `language`.

        Returns:
            dict | None: Разобранный ответ от API в виде словаря, или `None` в случае ошибки.
        
        Raises:
            PrestaShopException: Если HTTP-клиент не инициализирован или возникают критические ошибки сети/запроса.
        """
        # Объявление переменных в начале функции
        url_path: str
        current_data_format: str
        query_params: dict[str, Any]
        final_headers: dict
        request_content: bytes | None = None # httpx.request content ожидает bytes
        response: httpx.Response

        if not self.client:
            raise PrestaShopException('Клиент не инициализирован. Используй \'async with PrestaShopAsync(...)\'.')
        if not self._initialized:
             await self._initialize_connection() 

        url_path = resource
        if resource_id: # Проверка на None и пустую строку, 0 также считается True здесь
            url_path += f'/{resource_id}'

        current_data_format = (data_format_override or self.data_format).upper()

        # Формирование параметров URL
        query_params = {'output_format': current_data_format}
        if self.language: 
            query_params['language'] = self.language
        
        # Обработка kwargs для стандартных параметров PrestaShop
        for kwarg_key in ['filter', 'display', 'schema', 'sort', 'limit', 'language']:
            if kwarg_key in kwargs and kwargs[kwarg_key] is not None: 
                if kwarg_key == 'filter' and isinstance(kwargs[kwarg_key], dict):
                    # Преобразование словаря фильтров в формат PrestaShop: filter[field]=value
                    for k, v in kwargs[kwarg_key].items():
                         query_params[f'filter[{k}]'] = v
                else:
                    query_params[kwarg_key] = kwargs[kwarg_key]
        
        if params: # Добавление пользовательских параметров URL
            query_params.update(params)
        
        query_params = {k: v for k, v in query_params.items() if v is not None}


        # Формирование заголовков запроса
        final_headers = {}
        if current_data_format == 'JSON':
            final_headers['Content-Type'] = 'application/json; charset=utf-8'
            final_headers['Accept'] = 'application/json'
        elif current_data_format == 'XML':
            final_headers['Content-Type'] = 'application/xml; charset=utf-8'
            final_headers['Accept'] = 'application/xml'
        
        if req_headers: # Пользовательские заголовки переопределяют стандартные
            final_headers.update(req_headers)

        # Подготовка тела запроса (payload)
        if payload: 
            if isinstance(payload, dict):
                if current_data_format == 'JSON':
                    request_content = j_dumps(payload)
                elif current_data_format == 'XML':
                    xml_string: str = dict2xml(payload) # dict2xml должен вернуть строку XML
                    request_content = xml_string.encode('utf-8')
            elif isinstance(payload, str): 
                request_content = payload.encode('utf-8') # Если payload уже строка (JSON/XML)
            else:
                logger.warning(f'Неподдерживаемый тип payload ({type(payload)}) для формата {current_data_format}. Тело запроса не будет отправлено.')

        try:
            logger.debug(f'Выполнение {method} запроса к {self.api_domain_base}{url_path} с параметрами URL:\n\n {query_params}\n\n')
            if request_content:
                 #logger.debug(f'Тело запроса (первые 200 байт): {request_content[:200]}...')
                 logger.debug(f'Тело запроса : {request_content}...')

            response = await self.client.request(
                method=method,
                url=url_path,
                params=query_params, 
                content=request_content, 
                headers=final_headers,
            )

            if not await self._check_response_async(response, method, url_path, final_headers, payload):
                return None # Ошибка уже залогирована в _check_response_async через _handle_error_response

            return await self._parse_response_async(response, current_data_format)

        except httpx.HTTPStatusError as ex_http: 
            # Эта ошибка уже должна быть обработана _check_response_async, но на всякий случай
            logger.error(f'HTTPStatusError: {ex_http.response.status_code} для {ex_http.request.url}', ex_http, exc_info=True)
            # _handle_error_response мог быть не вызван, если ошибка возникла до _check_response_async
            # или если _check_response_async не смог её обработать (маловероятно)
            await self._handle_error_response(ex_http.response, method, str(ex_http.request.url), final_headers, payload)
            return None
        except httpx.RequestError as ex_req: 
            logger.error(f'RequestError при вызове API к {url_path}', ex_req, exc_info=True)
            raise PrestaShopException(f'Сетевая ошибка или ошибка запроса: {ex_req!s}') from ex_req
        except Exception as ex_gen: # Любые другие неожиданные ошибки
            logger.error(f'Неожиданная ошибка при вызове API к {url_path}', ex_gen, exc_info=True)
            raise PrestaShopException(f'Неожиданная ошибка: {ex_gen!s}') from ex_gen


    async def _parse_response_async(self, response: httpx.Response, data_format: str) -> dict | None:
        """
        Разбирает XML или JSON ответ от API в структуру dict.
        Автоматически определяет формат по Content-Type, если он отличается от ожидаемого.

        Args:
            response (httpx.Response): Объект HTTP-ответа от `httpx`.
            data_format (str): Ожидаемый формат данных ('JSON' или 'XML'), Используетсяый как fallback.

        Returns:
            dict | None: Разобранные данные в виде словаря, или `None` в случае ошибки разбора.
        """
        # Функция выполняет разбор ответа
        parsed_data: dict | list[Any] | None = None # xml2dict может вернуть list
        response_content_type: str = response.headers.get('content-type', '').lower()
        response_bytes: bytes

        try:
            # Сначала читаем тело ответа один раз
            response_bytes = await response.aread()

            if not response_bytes: # Пустое тело ответа
                 if response.status_code in [200, 201, 204]: # Успешные статусы для пустого ответа
                    return {'success': True, 'status_code': response.status_code}
                 else: 
                    logger.warning(f'Пустой ответ со статусом ошибки {response.status_code}')
                    return None 

            # Определение фактического формата для парсинга по Content-Type
            actual_parse_format: str = data_format # Используется ожидаемый формат по умолчанию
            if 'application/json' in response_content_type:
                actual_parse_format = 'JSON'
            elif 'application/xml' in response_content_type or 'text/xml' in response_content_type :
                actual_parse_format = 'XML'
            
            # Парсинг на основе определенного формата
            if actual_parse_format == 'JSON':
                parsed_data = json.loads(response_bytes) # Парсинг из прочитанных байт
            elif actual_parse_format == 'XML':
                xml_text: str = response_bytes.decode('utf-8', errors='replace')
                parsed_data = xml2dict(xml_text) 
            else:
                logger.error(f'Неподдерживаемый формат для разбора: {actual_parse_format}. Content-Type: {response_content_type}. Тело (часть): {response_bytes[:200]}...')
                return None
            
            # Обработка стандартной обертки 'prestashop' в ответе
            if isinstance(parsed_data, dict) and 'prestashop' in parsed_data and len(parsed_data) == 1:
                # Если parsed_data это {'prestashop': ACTUAL_DATA}, извлекаем ACTUAL_DATA
                return parsed_data['prestashop'] # type: ignore
            
            # Если xml2dict вернул список (например, для корневого элемента, который является списком)
            if isinstance(parsed_data, list):
                 # Это может быть специфично для вашего xml2dict. Если API возвращает список объектов без обертки.
                 # Преобразуем в словарь с ключом по умолчанию, чтобы соответствовать Возвратому типу dict | None
                 logger.warning(f'Ответ API был списком, обернут в словарь с ключом "data": {parsed_data[:3]}...')
                 return {'data': parsed_data}

            return parsed_data # parsed_data уже dict или None (если xml2dict вернул None)

        except json.JSONDecodeError as ex_json:
            response_text_sample: str = response_bytes.decode('utf-8', errors='replace')[:500]
            logger.error(f'Ошибка разбора JSON: {ex_json}. Текст ответа (часть): {response_text_sample}...', ex_json, exc_info=True)
            return None
        except ExpatError as ex_xml: 
             response_text_sample = response_bytes.decode('utf-8', errors='replace')[:500]
             logger.error(f'Ошибка разбора XML: {ex_xml}. Текст ответа (часть): {response_text_sample}...', ex_xml, exc_info=True)
             return None
        except Exception as ex_gen: # Любые другие ошибки при парсинге
            logger.error('Общая ошибка разбора ответа', ex_gen, exc_info=True)
            return None

    async def create_async(self, resource: str, data: dict, **kwargs: Any) -> dict | None:
        """
        Асинхронно создает новый ресурс в PrestaShop API.

        Args:
            resource (str): Имя ресурса (например, 'taxes', 'products').
            data (dict): Данные для создания ресурса. 
                         Структура словаря должна соответствовать ожиданиям API PrestaShop 
                         для выбранного `data_format` (JSON или XML).
            **kwargs (Any): Дополнительные именованные аргументы для передачи в `_exec_async`,
                            например, `language` для указания языка создаваемого контента.

        Returns:
            dict | None: Ответ от API с данными созданного ресурса (обычно включает ID), 
                         или `None` в случае ошибки.
        
        Example:
            >>> tax_payload = {'tax': {'rate': '5.000', 'active': '1', 
            ...                        'name': {'language': {'attrs': {'id': '1'}, 'value': 'New Tax'}}}}
            >>> # created_tax_info = await api.create_async('taxes', tax_payload)
            >>> # if created_tax_info: print(f"Created Tax ID: {created_tax_info.get('tax', {}).get('id')}")
        """
        # Функция выполняет создание ресурса
        return await self._exec_async(resource=resource, method='POST', payload=data, **kwargs)

    async def read_async(self, resource: str, resource_id: int | str, **kwargs: Any) -> dict | None:
        """
        Асинхронно читает (извлекает) данные указанного ресурса из PrestaShop API.

        Args:
            resource (str): Имя ресурса (например, 'products', 'customers').
            resource_id (int | str): Уникальный идентификатор ресурса для чтения.
            **kwargs (Any): Дополнительные именованные аргументы для передачи в `_exec_async`,
                            например, `display='full'` для получения всех полей ресурса.

        Returns:
            dict | None: Данные запрошенного ресурса от API в виде словаря, 
                         или `None` в случае ошибки (например, ресурс не найден).

        Example:
            >>> # product_details = await api.read_async('products', 1, display='full')
            >>> # if product_details: print(f"Product Name: {product_details.get('product', {}).get('name')}")
        """
        # Функция выполняет чтение ресурса
        return await self._exec_async(resource=resource, resource_id=resource_id, method='GET', **kwargs)

    async def write_async(self, resource: str, resource_id: int | str, data: dict, **kwargs: Any) -> dict | None:
        """
        Асинхронно обновляет существующий ресурс в PrestaShop API.
        PrestaShop API требует, чтобы `id` обновляемого ресурса был включен в тело `data`.

        Args:
            resource (str): Имя ресурса (например, 'customers', 'addresses').
            resource_id (int | str): Уникальный идентификатор ресурса для обновления.
            data (dict): Данные для обновления. Словарь должен содержать ключ с ID ресурса,
                         соответствующий `resource_id`.
            **kwargs (Any): Дополнительные именованные аргументы для передачи в `_exec_async`.

        Returns:
            dict | None: Ответ от API после обновления (часто это обновленный ресурс), 
                         или `None` в случае ошибки.
        
        Example:
            >>> update_payload = {'product': {'id': '1', 'active': '0', 'price': '99.99'}}
            >>> # updated_product_info = await api.write_async('products', 1, update_payload)
            >>> # if updated_product_info: print(f"Updated product active status: {updated_product_info.get('product',{}).get('active')}")
        """
        # Функция выполняет обновление ресурса
        # Убедитесь, что `data` содержит ID, как ожидает PrestaShop, например:
        # data = {'product': {'id': str(resource_id), 'name': 'New Name'}}
        return await self._exec_async(
            resource=resource,
            resource_id=resource_id,
            method='PUT',
            payload=data, 
            **kwargs,
        )

    async def unlink_async(self, resource: str, resource_id: int | str) -> bool:
        """
        Асинхронно удаляет указанный ресурс из PrestaShop API.

        Args:
            resource (str): Имя ресурса (например, 'orders', 'carts').
            resource_id (int | str): Уникальный идентификатор ресурса для удаления.

        Returns:
            bool: `True` в случае успешного удаления (API возвращает 200 OK или 204 No Content), 
                  `False` в противном случае.
        
        Example:
            >>> # success = await api.unlink_async('taxes', 10)
            >>> # if success: print("Tax successfully deleted.")
        """
        # Функция выполняет удаление ресурса
        response_data: dict | None = await self._exec_async(resource=resource, resource_id=resource_id, method='DELETE')
        return bool(response_data and response_data.get('success', False))


    async def search_async(self, resource: str, filter: str | dict | None = None, **kwargs: Any) -> dict | None: 
        """
        Асинхронно ищет ресурсы в PrestaShop API по заданным критериям.

        Фильтр (`filter`) может быть строкой в формате, ожидаемом PrestaShop API 
        (например, `filter[name]=%value%&filter[active]=1`), 
        или словарем (например, `{'name': '%value%', 'active': '1'}`), 
        который будет автоматически преобразован в нужный формат строки запроса.

        Args:
            resource (str): Имя ресурса для поиска (например, 'products', 'categories').
            filter (str | dict | None, optional): Критерии фильтрации для поиска.
            **kwargs (Any): Дополнительные параметры для управления поиском (например, `limit`, `sort`, `display`).

        Returns:
            dict | None: Ответ API, содержащий список найденных ресурсов (или один ресурс, если это так задумано API),
                         или `None` в случае ошибки. Структура ответа зависит от API (часто это `{'resource_plural_name': [...]}`).
        
        Example:
            >>> # search_params = {'name': '%laptop%', 'active': '1'}
            >>> # results = await api.search_async('products', filter=search_params, limit=5, display='[id,name]')
            >>> # if results and results.get('products'):
            ... #     for product in results['products']: print(f"ID: {product['id']}, Name: {product['name']}")
        """
        # Функция выполняет поиск ресурсов
        return await self._exec_async(resource=resource, method='GET', filter=filter, **kwargs)

    async def create_binary_async(self, resource_path: str, file_path: str, file_name_in_request: str) -> dict | None:
        """
        Асинхронно загружает бинарный файл (например, изображение) в PrestaShop API.
        Используется для загрузки файлов напрямую, например, при создании изображений для товаров.

        Args:
            resource_path (str): Путь к ресурсу API, куда будет загружен файл 
                                 (например, 'images/products/22' для изображения товара с ID 22).
            file_path (str): Локальный путь к файлу, который необходимо загрузить.
            file_name_in_request (str): Имя файла, которое будет указано в multipart/form-data запросе. 
                                        PrestaShop может использовать это имя или сгенерировать свое.

        Returns:
            dict | None: Ответ от API PrestaShop после загрузки файла (обычно содержит метаданные загруженного файла), 
                         или `None` в случае ошибки.
        
        Raises:
            PrestaShopException: Если HTTP-клиент не инициализирован или при критических ошибках сети/запроса.

        Example:
            >>> # image_upload_response = await api.create_binary_async('images/products/1', 'path/to/local_image.jpg', 'product_image.jpg')
            >>> # if image_upload_response: print(f"Uploaded image info: {image_upload_response}")
        """
        # Объявление переменных
        url_path: str
        files_data: dict
        response: httpx.Response
        parsed_response: dict | None

        if not self.client:
            raise PrestaShopException('Клиент не инициализирован.')
        if not self._initialized:
             await self._initialize_connection()

        url_path = resource_path.lstrip('/') # Удаление начального слеша, если есть, т.к. используется base_url
        
        try:
            path_obj: Path = Path(file_path)
            if not path_obj.is_file(): # Проверка, что файл существует и является файлом
                logger.error(f'Файл для бинарной загрузки не найден или не является файлом: {file_path}')
                return None

            with open(path_obj, 'rb') as file_obj:
                # MIME-тип 'image/jpeg' является примером, PrestaShop может требовать конкретные типы
                # или определять его сам. Для универсальности можно использовать 'application/octet-stream'
                # или библиотеку mimetypes для определения по расширению файла.
                files_data = {'image': (file_name_in_request, file_obj, 'application/octet-stream')} 
                
                logger.debug(f'Загрузка бинарного файла {file_path} в {url_path} как {file_name_in_request}')
                
                response = await self.client.post(url=url_path, files=files_data)

            if not await self._check_response_async(response, 'POST', url_path, req_data=f'Бинарный файл: {file_name_in_request}'):
                return None
            
            # Ответ от PrestaShop после загрузки изображения часто XML.
            # _parse_response_async попытается определить формат по Content-Type,
            # но можно указать приоритетный формат, если известно.
            parsed_response = await self._parse_response_async(response, data_format='XML') 
            return parsed_response

        except FileNotFoundError: 
            logger.error(f'Файл не найден для бинарной загрузки (повторная проверка): {file_path}', None, exc_info=True)
            return None
        except httpx.RequestError as ex:
            logger.error(f'RequestError при бинарной загрузке в {url_path}', ex, exc_info=True)
            raise PrestaShopException('Сетевая ошибка или ошибка запроса при бинарной загрузке') from ex
        except Exception as ex:
            logger.error(f'Ошибка при бинарной загрузке файла {file_path}', ex, exc_info=True)
            return None


    async def get_schema_async(
        self, resource: str | None = None, resource_id: int | None = None, schema: str | None = 'blank', **kwargs: Any
    ) -> dict | None:
        """
        Асинхронно извлекает схему (структуру) указанного ресурса из PrestaShop API.
        Это полезно для понимания полей ресурса, их типов и обязательности.

        Args:
            resource (str | None, optional): Имя ресурса (например, 'products', 'customers'). 
                                             Если `None`, API может вернуть список всех доступных схем.
            resource_id (int | None, optional): ID конкретного экземпляра ресурса. 
                                                Редко используется для получения общей схемы.
            schema (str | None, optional): Тип запрашиваемой схемы (например, 'blank' для пустой структуры, 
                                           'synopsis' для упрощенной). По умолчанию 'blank'.
            **kwargs (Any): Дополнительные именованные аргументы, передаваемые в `_exec_async`.

        Returns:
            dict | None: Схема ресурса, представленная в виде словаря (обычно из XML или JSON ответа API),
                         или `None` в случае ошибки.
        
        Example:
            >>> # tax_schema_blank = await api.get_schema_async('taxes', schema='blank')
            >>> # if tax_schema_blank: print(f"Blank schema for taxes: {j_dumps(tax_schema_blank, indent=2)}")
        """
        # Функция выполняет извлечение схемы ресурса
        return await self._exec_async(resource=resource, resource_id=resource_id, method='GET', schema=schema, **kwargs)

    async def get_data_async(self, resource: str, **kwargs: Any) -> dict | None:
        """
        Асинхронно извлекает общие данные из указанного ресурса PrestaShop API.
        Этот метод является оберткой над `_exec_async` с методом GET и может использоваться
        для запросов, не подпадающих под стандартные CRUD операции (например, чтение конфигураций).

        Args:
            resource (str): Имя ресурса API (например, 'configurations', 'shop_urls').
            **kwargs (Any): Дополнительные аргументы для передачи в `_exec_async`, 
                            такие как `filter`, `limit`, `display` для настройки запроса.

        Returns:
            dict | None: Данные от API в виде словаря, или `None` в случае ошибки.
        
        Example:
            >>> # shop_configurations = await api.get_data_async('configurations', display='[name,value]')
            >>> # if shop_configurations and shop_configurations.get('configurations'):
            ... #     for config_item in shop_configurations['configurations']: print(config_item)
        """
        # Функция выполняет извлечение данных
        return await self._exec_async(resource=resource, method='GET', **kwargs)

    async def get_apis_async(self) -> dict | None:
        """
        Асинхронно получает список всех доступных эндпоинтов (ресурсов) API PrestaShop.
        Ответ обычно представляет собой XML-документ, который парсится в словарь,
        содержащий информацию о доступных ресурсах и их возможностях для текущего API ключа.

        Returns:
            dict | None: Словарь со списком доступных API ресурсов и их описанием,
                         или `None` в случае ошибки.
        
        Example:
            >>> # available_api_endpoints = await api.get_apis_async()
            >>> # if available_api_endpoints: print(f"Available APIs: {j_dumps(available_api_endpoints, indent=2)}")
        """
        # Функция выполняет получение списка доступных API
        # Запрос к корневому `/api/` без указания ресурса (`resource=''`)
        return await self._exec_async(resource='', method='GET', data_format_override=self.data_format)


    async def upload_image_from_url_async(
        self, 
        resource_images_path: str, 
        entity_id: int, 
        img_url: str, 
        img_name_prefix: str | None = None 
    ) -> dict | None:
        """
        Асинхронно загружает изображение по URL в PrestaShop.
        Процесс включает скачивание изображения во временный локальный файл,
        а затем загрузку этого файла на сервер PrestaShop.

        Args:
            resource_images_path (str): Базовый путь для изображений ресурса в API PrestaShop 
                                        (например, 'images/products').
            entity_id (int): ID сущности (например, товара, категории), к которой будет 
                             привязано изображение.
            img_url (str): URL-адрес изображения, которое необходимо скачать и загрузить.
            img_name_prefix (str | None, optional): Необязательный префикс, который будет добавлен 
                                                    к имени файла при сохранении на сервере PrestaShop 
                                                    и в имени временного файла.

        Returns:
            dict | None: Ответ от API PrestaShop после загрузки изображения, 
                         или `None` в случае какой-либо ошибки в процессе.
        
        Example:
            >>> # product_id = 1
            >>> # image_url = 'https://example.com/path/to/image.jpg'
            >>> # upload_response = await api.upload_image_from_url_async('images/products', product_id, image_url, 'main_image')
            >>> # if upload_response: print("Image uploaded successfully from URL.")
        """
        # Объявление переменных
        url_parts: list[str]
        extension: str
        base_filename: str
        local_temp_filename: str
        filename_in_request: str
        temp_dir: Path
        local_temp_filepath: str
        downloaded_filepath: str | None
        prestashop_resource_path: str
        response_data: dict | None = None # Инициализация значением по умолчанию


        url_parts = img_url.rsplit('.', 1)
        extension = url_parts[1] if len(url_parts) > 1 else 'jpg' # Расширение по умолчанию 'jpg'
        
        base_filename = str(entity_id)
        if img_name_prefix:
            base_filename += f'_{img_name_prefix}'
        
        local_temp_filename = f'{base_filename}_temp.{extension}'
        filename_in_request = f'{base_filename}.{extension}' # Имя файла для PrestaShop

        # Директория для временных файлов, можно вынести в Config
        temp_dir = Path('temp_images_prestashop_api') 
        temp_dir.mkdir(parents=True, exist_ok=True) 
        local_temp_filepath = str(temp_dir / local_temp_filename)

        try:
            # 1. Асинхронное скачивание изображения во временный файл
            downloaded_filepath = await save_image_from_url_async(img_url, local_temp_filepath)
            if not downloaded_filepath or not Path(downloaded_filepath).exists(): # Проверка результата скачивания
                logger.error(f'Ошибка загрузки изображения с {img_url} во временный файл.')
                return None # Возврат None, если скачивание не удалось

            # 2. Загрузка скачанного файла в PrestaShop
            # Формирование пути для API: images/products/{id}
            prestashop_resource_path = f'{resource_images_path.strip("/")}/{entity_id}'
            
            response_data = await self.create_binary_async(
                resource_path=prestashop_resource_path, 
                file_path=downloaded_filepath, 
                file_name_in_request=filename_in_request
            )
            return response_data

        except Exception as ex: # Обработка любых других исключений
            logger.error(f'Ошибка в процессе upload_image_from_url_async для {img_url}', ex, exc_info=True)
            return None
        finally:
            # 3. Удаление временного файла после операции
            if Path(local_temp_filepath).exists():
                await remove_file_async(local_temp_filepath)


    async def get_product_images_async(self, product_id: int) -> dict | None:
        """
        Асинхронно получает информацию об изображениях для указанного товара.
        Данные извлекаются из секции `associations` в информации о товаре.

        Args:
            product_id (int): Уникальный идентификатор товара.

        Returns:
            dict | None: Словарь, содержащий список информации об изображениях 
                         (например, `{'images': [{'id': '1'}, {'id': '2'}, ...]}`),
                         или `None`, если изображения не найдены или произошла ошибка.
        
        Example:
            >>> # product_images_info = await api.get_product_images_async(1)
            >>> # if product_images_info and product_images_info.get('images'):
            ... #     print(f"Found {len(product_images_info['images'])} images for product.")
            ... #     for img_info in product_images_info['images']: print(f"Image ID: {img_info.get('id')}")
        """
        # Функция выполняет получение информации об изображениях товара
        product_data: dict | None
        images_assoc_data: Any # Тип данных из associations может варьироваться
        
        # Запрос полной информации о товаре для доступа к associations
        product_data = await self.read_async('products', product_id, display='full')
        
        if product_data and 'product' in product_data: 
            images_assoc_data = product_data['product'].get('associations', {}).get('images', {})
            
            # Обработка различной структуры ответа для изображений
            if isinstance(images_assoc_data, dict) and 'image' in images_assoc_data : 
                 actual_image_data = images_assoc_data['image']
                 # Если 'image' содержит один объект, оборачиваем в список
                 return {'images': actual_image_data if isinstance(actual_image_data, list) else [actual_image_data]}
            elif isinstance(images_assoc_data, list): # Если associations.images это уже список ID или объектов
                 return {'images': images_assoc_data}
            elif not images_assoc_data: # Если associations.images пусто (None, пустой dict/list)
                 logger.info(f'Для товара {product_id} не найдено ассоциированных изображений.')
                 return {'images': []} # Возврат пустого списка изображений для консистентности
        
        logger.warning(f'Не удалось извлечь информацию об изображениях для товара {product_id} через ассоциации.')
        return None


async def main_async() -> None:
    """
    Асинхронная демонстрационная функция для проверки работы с PrestaShop API.
    Выполняет операции создания, чтения, обновления, поиска и удаления налоговой ставки.
    Содержит также закомментированный пример для тестирования загрузки изображения.
    """
    # Объявление переменных, Используетсяых в функции
    api_domain_val: str
    api_key_val: str
    data_format_val: str
    pong: bool
    tax_data_create: dict
    created_tax_response: dict | None
    tax_id: str | int 
    read_tax_response: dict | None
    tax_data_update: dict
    updated_tax_response: dict | None
    searched_taxes_response: dict | None # Изменено имя для ясности
    delete_success: bool

    # Использование значений из Config или их переопределение для теста
    api_domain_val = Config.API_DOMAIN 
    api_key_val = Config.API_KEY      
    data_format_val = Config.POST_FORMAT 

    if 'your.prestashop.com' in api_domain_val or 'YOURAPIKEY' == api_key_val: 
        logger.error("Обнаружены значения API_DOMAIN/API_KEY по умолчанию. "
                     "Пожалуйста, настройте их в классе Config или непосредственно в main_async для запуска.")
        return

    async with PrestaShopAsync(
        api_domain=api_domain_val,
        api_key=api_key_val,
        default_lang=Config.language, 
        debug=True, 
        data_format=data_format_val,
    ) as api:
        
        pong = await api.ping_async()
        logger.info(f'Результат Ping: {pong}. Версия PrestaShop: {api.ps_version}')
        if not pong:
            logger.error('Ping неудачен. Прерывание дальнейших операций.')
            return

        # 1. Создание налоговой ставки
        tax_data_create = {
            'tax': {
                'rate': '9.990', # PrestaShop часто ожидает строки для числовых значений
                'active': '1',
                'name': { 
                    'language': [ # Массив даже для одного языка
                        {'attrs': {'id': str(api.language)}, 'value': f'Async Tax {gs.now.strftime("%H%M%S")}'} # Уникальное имя
                    ]
                }
            }
        }
        
        created_tax_response = await api.create_async('taxes', tax_data_create)
        
        # Проверка успешности создания и извлечение ID
        if created_tax_response and isinstance(created_tax_response.get('tax'), dict) and 'id' in created_tax_response['tax']:
            tax_id = created_tax_response['tax']['id']
            logger.info(f'Налоговая ставка успешно создана. ID: {tax_id}, Ответ: {j_dumps(created_tax_response)}')

            # 2. Чтение созданной налоговой ставки
            read_tax_response = await api.read_async('taxes', tax_id)
            logger.info(f'Чтение налоговой ставки ID {tax_id}: {j_dumps(read_tax_response)}')

            # 3. Обновление налоговой ставки
            tax_data_update = {
                'tax': {
                    'id': str(tax_id), # ID обязателен для PUT-запроса
                    'rate': '10.100',
                    'active': '0', # Деактивация для примера
                    'name': {
                        'language': [
                             {'attrs': {'id': str(api.language)}, 'value': f'Async Tax Updated {gs.now.strftime("%H%M%S")}'}
                        ]
                    }
                }
            }
            updated_tax_response = await api.write_async('taxes', tax_id, tax_data_update)
            logger.info(f'Налоговая ставка успешно обновлена. ID: {tax_id}, Ответ: {j_dumps(updated_tax_response)}')
            
            # 4. Поиск налоговых ставок
            searched_taxes_response = await api.search_async('taxes', filter={'name': '%Async Tax%'}, limit='5', display='full')
            
            taxes_list_found: list = []
            if searched_taxes_response and 'taxes' in searched_taxes_response:
                taxes_data_from_search = searched_taxes_response['taxes']
                # Обработка случая, когда 'tax' это один объект или список объектов
                if isinstance(taxes_data_from_search, dict) and 'tax' in taxes_data_from_search:
                    tax_items = taxes_data_from_search['tax']
                    taxes_list_found = [tax_items] if isinstance(tax_items, dict) else tax_items
                elif isinstance(taxes_data_from_search, list): # Если PrestaShop вернул список напрямую под 'taxes'
                    taxes_list_found = taxes_data_from_search
            
            if taxes_list_found:
                logger.info(f'Найдено налоговых ставок: {len(taxes_list_found)}')
                # for tax_item_found in taxes_list_found: print(j_dumps(tax_item_found)) # Вывод с помощью print (pprint)
            else:
                logger.info(f'Налоговые ставки с "Async Tax" не найдены или ответ пуст: {j_dumps(searched_taxes_response)}')


            # 5. Удаление созданной налоговой ставки
            delete_success = await api.unlink_async('taxes', tax_id)
            logger.info(f'Налоговая ставка ID {tax_id} успешно удалена: {delete_success}')
        
        else: # Если создание налога не удалось
            logger.error(f'Ошибка создания налоговой ставки. Ответ: {j_dumps(created_tax_response)}')

if __name__ == '__main__':
    # Проверка конфигурации перед запуском
    if Config.API_DOMAIN == 'https://your.prestashop.com' or Config.API_KEY == 'YOURAPIKEY':
         print('Обнаружены значения API_DOMAIN/API_KEY по умолчанию в Config.')
         print('Пожалуйста, установите корректные значения в src/endpoints/prestashop/api_async.py (класс Config)')
         print('Или измените их непосредственно в функции main_async для тестового запуска.')
    else:
        try:
            asyncio.run(main_async())
        except KeyboardInterrupt: # Обработка прерывания пользователем
            logger.info('Выполнение программы прервано пользователем (Ctrl+C).')
        except Exception as main_execution_exception: # Обработка других исключений на верхнем уровне
            logger.error('Произошла непредвиденная ошибка при выполнении main_async', main_execution_exception, exc_info=True)
