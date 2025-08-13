# # \file src/endpoints/prestashop/api_async.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Asynchronous module for interacting with Prestashop API.
======================================================================================ward

This module is provided by the class `Prestashopasync` to interact with Prestashop WebService API,
Using JSON and XML to format messages. He supports Crud operations, search,
and loading images, with error processing for answers in asynchronous mode.

Examples of use
-------------

`` `python
Import Asyncio
# It is assumed that Config is in the same file or imported correctly
from src.endpoints.prestashop.api_async import Prestashopasync, config 
from src.logger.logger Import Logger # for logging in the example

Async Def Main_example ():
    # Replace your data or config
    API_Domain = 'https://your-prestashop-domain.com'
    API_KEY = 'YOUR_API_KEY'
    
    # Example of using config if it is configured
    # api_domain = config.api_domain
    # API_KEY = config.api_key

    Async with Prestashopasync (
        API_Domain = API_Domain,
        API_KEY = API_KEY,
        Default_lang = 1,
        Debug = True,
        DATA_FORMAT = 'JSON', # or 'XML'
    ) AS API:

        AWAIT API.Ping_async ()
        Logger.info (F'Prestashop Version: {API.ps_version} ')


        Data = {
            'Tax': {
                'Rate': '3000', # numbers are often transmitted as lines
                'Active': '1',
                'name': {
                    'Language': { # in Prestashop is often expected an array, even for one language
                        'attrs': {'id': '1'},
                        'Value': 'async 3% Tax'
                    }
                }
            }
        }

        # Create Tax Record
        Rec = AWAIT API.create_async ('Taxes', Data)
        IF not read or not isinStance (Rac.get ('Tax'), DICT) or 'ID' Not in REC ['TAX']:
            Logger.error (F'failed to Create Tax: {Rec} ')
            Return

        TAX_ID = REC ['TAX'] ['ID']
        Logger.info (f'creed Tax with id: {tax_id} ')

        # Update the Same Tax Record
        update_data = {
            'Tax': {
                'ID': str (TAX_ID), 
                'Rate': '3.500',
                'Active': '1',
                'name': {
                    'Language': {
                        'attrs': {'id': '1'},
                        'Value': 'async 3.5% Tax updated'
                    }
                }
            }
        }
        
        # For Prestashop XML API, the body of PUT request often turns into <sestashop>
        # Payload_for_update = {'Prestashop': update_data} run.Data_Format == 'xml' else update_data
        # In our _exec_async Payload, it is transmitted, dict2xml/json.dumps do their job.

        UPDATE_REC = AWAIT API.Write_async ('Taxes', Str (Tax_id), Update_Data)
        Logger.info (F'UPDATED TAX: {Update_REC} ')

        # Read the Tax
        Read_ReC = AWAIT API.Read_async ('Taxes', Str (Tax_id))
        Logger.info (F'Read Tax: {Read_Rec} ')

        # Search The First 3 Taxes with 'async' in the Name
        # Used from SRC.utils.Printer Import PPRINT AS Print
        Recs = AWAIT API.Search_async ('Taxes', Filter = {' Name ':'%async%}, limit = '3') 

        if read and read ('Taxes'):
            # Answer Prestashop can be different: a list or one object
            Taxes_found = read ['taxes']. Get ('Tax', []) 
            IF IsinStance (Taxes_found, Dict): # If one tax, it is not on the list
                Taxes_found = [Taxes_found]
            for r_item in taxes_found: 
                Print (R_item) # Used Print (which is PPRINT)

        # Remove this Tax
        SUCCESS = AWAIT API.unLink_async ('Taxes', Str (Tax_id))
        Logger.info (F'Deleted Tax with Id {Tax_id}: {Success} ')

run __name__ == '__main__':
    # This part for launching an example, if this file is executed directly
    # Make sure asyncio.run is called only once at the upper level
    # And that Config is configured or the values are transmitted directly.
    # Example:
    # Class Config: # Dummy Config for example
    # API_Domain = "https://your.prestashop.com" # Replace
    # API_KEY = "Yourapikey" # Replace
    # Post_Format = "json"
    # Language = 1 # added for consistency
        
    asyncio.run (mail_example ())

`` `
`` `RST
  .. Module :: src.endpoints.prestashop.api_async
`` `"""
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any # Union replaced to |

import httpx 

from xml.etree import ElementTree # Only Expateror is used
from xml.parsers.expat import ExpatError

# Default imports
import header
from header import __root__
from src import gs

from src.logger.exceptions import PrestaShopAuthenticationError, PrestaShopException
from src.logger.logger import logger
from src.endpoints.prestashop.utils import dict2xml, xml2dict 
from src.utils.file import remove_file_async
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print 

from dataclasses import dataclass, field # Field is not used, but left for @dataclass


@dataclass
class Config:
    """Configuration class for Prestashop API.

    Contains default settings and parameters necessary for connecting
    and interactions with the API Prestashop.

    Attributes:
        Language (int): ID of the default language ID used in the API requests.
        PS_version (str): version Prestashop. It is determined automatically during the first connection.
        Mode (str): mode of operation (for example, 'DEV', 'Prod'). Affects the choice of the final point of the API, if used.
        Post_Format (str): data format ('json' or 'XML') used for ties post/put requests.
        API_DOMAIN (STR): the base URL of the Prestashop store (for example, 'https://yourshop.com').
        API_KEY (str): access key to the API Prestashop."""
    language: int = 1
    ps_version: str = ''
    MODE: str = 'dev'
    POST_FORMAT: str = 'XML' 
    API_DOMAIN: str = '' 
    API_KEY: str = '' 


class PrestaShopAsync:
    """Asynchronous client for interaction with Prestashop WebService API.

    This class provides methods for performing CRUD operations, searching for resources,
    loading images and obtaining data schemes through Prestashop API,
    Using asynchronous HTTP checks.

    Args:
        API_KEY (STR): API key generated in Prestashop.
        API_DOMAIN (STR): the domain of the Prestashop store (for example, 'https://myprestashop.com').
        DATA_FORMAT (STR, Optional): Format by default data ('json' or 'XML'). By default 'json'.
        Default_lang (Int, Optional): ID of the Language by default. By default 1.
        Debug (Bool, Optional): activation of the debugging mode. By default `false`.

    RAISES:
        Prestashopouthenticationeroror: with an authentication error (incorrect key).
        Prestashopexception: with other general errors of interaction with Prestashop API.
    
    Example:
        >>> Async Def run_example ():
        ... # Replace with real data
        ... # async with prestashopasync ('your_api_key', 'https://yourshop.com') as API:
        ... # is_ok = AWAIT API.Ping_async ()
        ... # Print (F'Ping: {IS_OK} ') # Used Print (PPRINT)
        ... pass # example requires a real API to execute
        >>> # Import asyncio
        >>> # asyncio.ru (run_example ())"""

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
        """Prestashop API Client Initialization.

        Args:
            API_KEY (STR): Key API Prestashop.
            API_DOMAIN (STR): the domain of the Prestashop store (for example, 'https://shop.com'). 
                              Must be the basic URL store, `/API/` will be added automatically.
            DATA_FORMAT (STR, Optional): Format by default data ('json' or 'XML').
                                         By default, the value is used from `config.post_format`.
            Default_lang (Int, Optional): ID of the Language by default. By default 1.
            Debug (Bool, Optional): Turning on the debugging mode. By default `false`."""
        # Normalization of URL API_DOMAIN for forming API_Domain_Base
        normalized_domain: str = api_domain
        if not normalized_domain.startswith(('http://', 'https://')):
            normalized_domain = 'https://' + normalized_domain # Adding a default scheme
        if not normalized_domain.endswith('/'):
            normalized_domain += '/'
        
        # Formation of the basic URL for API
        if 'api/' not in normalized_domain.split('/')[-2:]: # Check, whether it already contains /API /
            self.api_domain_base = normalized_domain + 'api/'
        else: # If/API/already there (for example, https://shop.com/api/)
            self.api_domain_base = normalized_domain
            if not self.api_domain_base.endswith('/'): # We guarantee a slash at the end
                self.api_domain_base += '/'


        self.api_key = api_key
        self.debug = debug
        self.language = default_lang
        self.data_format = data_format.upper() 
        
        self._initialized = False 


    async def __aenter__(self) -> 'PrestaShopAsync':
        """Asynchronous entrance to the context manager.
        Initializes the HTTP client and performs the initial connection to the API.

        Returns:
            Prestashopasync: a copy of yourself, ready for use.
        
        RAISES:
            Prestashopexception: If there is an error when initializing the client or connecting."""
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
        """Initializes the connection with the API Prestashop.
        Sends a Head request to check the accessibility of the service and obtain the Prestashop version.
        This method is called automatically at the entrance to the context manager or at the first request,
        requiring active connection.
        
        RAISES:
            Prestashopouthenticationeroror: with an authentication error or if the service is not available (401, 403).
            Prestashopexception: with other errors of a network or a request (for example, timaut, DNS-leaf)."""
        # The function initializes the connection
        if self._initialized:
            return
        
        if not self.client:
            # This condition should not occur when used through async with
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
            logger.error(f'HTTP ошибка при начальном подключении: {ex.response.status_code}', ex, exc_info=True) # Exc_info = TRUE for httpstatuserror.
            await self._handle_error_response(ex.response) 
            raise PrestaShopAuthenticationError(f'Ошибка подключения или аутентификации: {ex.response.status_code}') from ex
        except httpx.RequestError as ex:
            logger.error('Ошибка запроса при начальном подключении', ex, exc_info=True)
            raise PrestaShopException('Сетевая ошибка или ошибка запроса при инициализации') from ex
        except Exception as ex: 
            logger.error('Неожиданная ошибка при инициализации соединения', ex, exc_info=True)
            raise PrestaShopException('Неожиданная ошибка при инициализации') from ex


    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None:
        """Asynchronous exit from the context manager.
        Guarantees the correct closure of the HTTP client.

        Args:
            Exc_type (Type [Baseexception] | None): Type of exception if it arose in the `Async with 'block.
            Exc_val (Baseexception | None): A copy of the exception.
            Exc_tb (Any | None): Traceback object (Traceback)."""
        if self.client: 
            await self.client.aclose()
            self.client = None
        self._initialized = False 


    async def ping_async(self) -> bool:
        """Asynchronously checks the performance of the Prestashop web service.
        Sends the HEAD request to the root endochin of the API.

        Returns:
            Bool: `true`, if the service is available and answers correctly (2xx status), otherwise` false`.
        
        RAISES:
            Prestashopexception: If the client has not been initialized (for example, `async with is not used)."""
        # The function performs the accessibility of the service
        if not self.client:
            raise PrestaShopException('Клиент не инициализирован. Используй \'async with PrestaShopAsync(...)\'.')
        if not self._initialized: 
            try:
                await self._initialize_connection()
            except PrestaShopException as ex_init: # We catch the errors of initialization
                logger.error('Ping неудачен: ошибка при инициализации соединения во время ping.', ex_init, exc_info=False) # Exc_info false, because Ex_init already contains details
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
        """Checks the state code HTTP.
        In the case of an error (not 200 and not 201 status) causes `_HANDLE_ROROR_RESPONSE to log in.

        Args:
            Response (httpx.response): HTTP response object from `httpx`.
            Method (Str | None, Optional): HTTP method of the executed request (Get, Post, etc.).
            URL (Str | None, Optional): URL, to which a request was made.
            REQ_HEADERS (DICT | NONE, OPTIONAL): headlines used in the request.
            REQ_DATA (Any | None, Optional): The body of the data sent in the request.

        Returns:
            Bool: `true`, if the status code is 200 or 201, otherwise` false`."""
        # The function performs the verification of the reply code
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
        """Processes and logs the answer with the error from Prestashop API.
        Trying to extract the details of the error from the body of the answer (json or XML).

        Args:
            Response (httpx.response): an object of http-answer with an error.
            Method (Str | None, Optional): HTTP Request method.
            URL (Str | None, Optional): URL request.
            REQ_HEADERS (DICT | NONE, OPTIONAL): Request headlines.
            REQ_DATA (Any | None, Optional): Request body."""
        # The function performs the analysis and logistics of the response with the error
        status_code: int = response.status_code
        error_content_parsed: dict = {}
        error_message_raw: str = ''
        response_text_for_log: str = '(не удалось прочитать тело ответа)' # Default value

        try:
            # Asynchronous reading of the response body for logs (limited size)
            # Response.aread () Returns bytes, decode in a line
            response_bytes: bytes = await response.aread() 
            response_text_for_log = response_bytes.decode('utf-8', errors='replace')[:1000] 
        except Exception as ex_read: # If the error when reading the body
            logger.warning(f'Ошибка при чтении тела ответа для логирования: {ex_read}')


        try:
            content_type_header: str = response.headers.get('content-type', '').lower()
            # The already read response_text_for_log for parsing is used, if possible,
            # Or allow response.json ()/response.text () read again, if necessary.
            # httpx.response.json () and .Text () can be caused only once without preliminary Stream.
            # If we have already made response.aread (), then we need to pave from bytes/text.

            if 'application/json' in content_type_header:
                try:
                    error_content_parsed = json.loads(response_bytes) # Parsing from already read bytes
                    error_message_raw = j_dumps(error_content_parsed)
                except json.JSONDecodeError: # If from bytes failed, we try response.json ()
                    error_content_parsed = await response.json() 
                    error_message_raw = j_dumps(error_content_parsed)

            elif 'application/xml' in content_type_header or 'text/xml' in content_type_header:
                xml_text: str = response_bytes.decode('utf-8', errors='replace') # Read bytes are used
                error_message_raw = xml_text
                parsed_xml_error: dict | list[Any] | None = xml2dict(xml_text)
                if isinstance(parsed_xml_error, dict):
                    error_details: Any = parsed_xml_error.get('prestashop', {}).get('errors', {}).get('error', {})
                    if isinstance(error_details, list): error_details = error_details[0] if error_details else {}
                    
                    code_val: Any = error_details.get('code') if isinstance(error_details, dict) else 'N/A'
                    message_val: Any = error_details.get('message') if isinstance(error_details, dict) else 'No message in XML error.'
                    
                    logger.debug(f'XML API Error Code: {code_val}, Message: {message_val}') # Debug, because The main message is below
                    error_content_parsed = {'code': code_val, 'message': message_val}
                else:
                    error_content_parsed = {'message': 'Структура XML ошибки не распознана или xml2dict не вернул словарь.'}
            else:
                error_message_raw = response_text_for_log # What was used to read
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

        # Formation of log-messages
        log_msg_parts: list[str] = [
            'Ошибка PrestaShop API:',
            f'  Статус код: {status_code}',
            f'  Метод: {method or response.request.method}', # The use of the actual method from the request if Method is not transferred
            f'  URL: {url or str(response.request.url)}',
            f'  Заголовки запроса: {j_dumps(req_headers or dict(response.request.headers))}',
            f'  Тело запроса: {j_dumps(req_data) if req_data else "N/A"}',
            f'  Заголовки ответа: {j_dumps(dict(response.headers))}',
            f'  Тело ответа (часть): {error_message_raw[:500] if error_message_raw else response_text_for_log[:500]}...',
            f'  Разобранная ошибка: {j_dumps(error_content_parsed)}'
        ]
        logger.error('\n'.join(log_msg_parts), None, False) # Exc_info = false, because The API error itself has already been logged in


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
        """Performs an asynchronous HTTP request to the Prestashop API.
        This is the main method for all interactions with the API.

        Args:
            Resource (StR): API resource (for example, 'Products', 'Customers', '' for root).
            Resource_id (int | str | None, Optional): ID resource.
            Method (str, Optional): HTTP method ('get', 'post', 'put', 'delete'). By default 'get'.
            Payload (dict | str | None, Optional): the body of the request (for Post, PUT) can be a dictionary or a string.
            Params (DICT [str, Any] | None, Optional): Additional URL parameters.
            REQ_HEADERS (DICT | NONE, OPTIONAL): Additional request headlines that overright standard.
            DATA_FORMAT_OVERRIDE (STR | None, Optional): Revealing the data format ('json'/'XML') for this specific request.
            ** KWARGS (ANY): additional parameters for URL, such as `Filter`,` Display`, `Schema`,` Sort`, `Limit`,` Language`.

        Returns:
            dict | None: a disassembled answer from the API in the form of a dictionary, or `none` in the case of an error.
        
        RAISES:
            Prestashopexception: If the HTTP client is not initialized or critical network/request errors arise."""
        # Announcement of variables at the beginning of the function
        url_path: str
        current_data_format: str
        query_params: dict[str, Any]
        final_headers: dict
        request_content: bytes | None = None # Httpx.request Content expects bytes
        response: httpx.Response

        if not self.client:
            raise PrestaShopException('Клиент не инициализирован. Используй \'async with PrestaShopAsync(...)\'.')
        if not self._initialized:
             await self._initialize_connection() 

        url_path = resource
        if resource_id: # Checking for NONE and an empty line, 0 is also considered true here
            url_path += f'/{resource_id}'

        current_data_format = (data_format_override or self.data_format).upper()

        # Formation of URL parameters
        query_params = {'output_format': current_data_format}
        if self.language: 
            query_params['language'] = self.language
        
        # Kwargs processing for standard Prestashop parameters
        for kwarg_key in ['filter', 'display', 'schema', 'sort', 'limit', 'language']:
            if kwarg_key in kwargs and kwargs[kwarg_key] is not None: 
                if kwarg_key == 'filter' and isinstance(kwargs[kwarg_key], dict):
                    # Converting the dictionary of filters to Prestashop: Filter [Field] = Value
                    for k, v in kwargs[kwarg_key].items():
                         query_params[f'filter[{k}]'] = v
                else:
                    query_params[kwarg_key] = kwargs[kwarg_key]
        
        if params: # Adding user parameters URL
            query_params.update(params)
        
        query_params = {k: v for k, v in query_params.items() if v is not None}


        # Formation of the headlines of the request
        final_headers = {}
        if current_data_format == 'JSON':
            final_headers['Content-Type'] = 'application/json; charset=utf-8'
            final_headers['Accept'] = 'application/json'
        elif current_data_format == 'XML':
            final_headers['Content-Type'] = 'application/xml; charset=utf-8'
            final_headers['Accept'] = 'application/xml'
        
        if req_headers: # User headlines overround standard
            final_headers.update(req_headers)

        # Request body preparation (Payload)
        if payload: 
            if isinstance(payload, dict):
                if current_data_format == 'JSON':
                    request_content = j_dumps(payload)
                elif current_data_format == 'XML':
                    xml_string: str = dict2xml(payload) # dict2xml must return the XML line
                    request_content = xml_string.encode('utf-8')
            elif isinstance(payload, str): 
                request_content = payload.encode('utf-8') # If Payload is already a line (json/xml)
            else:
                logger.warning(f'Неподдерживаемый тип payload ({type(payload)}) для формата {current_data_format}. Тело запроса не будет отправлено.')

        try:
            logger.debug(f'Выполнение {method} запроса к {self.api_domain_base}{url_path} с параметрами URL:\n\n {query_params}\n\n')
            if request_content:
                 # Logger.debug (F'Telo Requests (first 200 bytes): {Receist_content [: 200]} ... ')
                 logger.debug(f'Тело запроса : {request_content}...')

            response = await self.client.request(
                method=method,
                url=url_path,
                params=query_params, 
                content=request_content, 
                headers=final_headers,
            )

            if not await self._check_response_async(response, method, url_path, final_headers, payload):
                return None # Oshka is already entertained in _Check_resPonse_async via _handle_error_resposse

            return await self._parse_response_async(response, current_data_format)

        except httpx.HTTPStatusError as ex_http: 
            # This error should already be processed _check_response_async, but just in case
            logger.error(f'HTTPStatusError: {ex_http.response.status_code} для {ex_http.request.url}', ex_http, exc_info=True)
            # _handle_error_response could not be caused if the error arose before _check_response_async
            # Or if _Check_Response_async could not process it (unlikely)
            await self._handle_error_response(ex_http.response, method, str(ex_http.request.url), final_headers, payload)
            return None
        except httpx.RequestError as ex_req: 
            logger.error(f'RequestError при вызове API к {url_path}', ex_req, exc_info=True)
            raise PrestaShopException(f'Сетевая ошибка или ошибка запроса: {ex_req!s}') from ex_req
        except Exception as ex_gen: # Any other unexpected mistakes
            logger.error(f'Неожиданная ошибка при вызове API к {url_path}', ex_gen, exc_info=True)
            raise PrestaShopException(f'Неожиданная ошибка: {ex_gen!s}') from ex_gen


    async def _parse_response_async(self, response: httpx.Response, data_format: str) -> dict | None:
        """The XML or JSON analyzes the response from the API to the DICT structure.
        Automatically determines the format by Content-Type if it differs from the expected.

        Args:
            Response (httpx.response): Object http-answer from `httpx`.
            DATA_FORMAT (STR): the expected data format ('json' or 'XML'), used as Fallback.

        Returns:
            dict | None: disassembled data in the form of a dictionary, or `none` in case of analysis error."""
        # The function performs the analysis of the response
        parsed_data: dict | list[Any] | None = None # XML2DICT can return list
        response_content_type: str = response.headers.get('content-type', '').lower()
        response_bytes: bytes

        try:
            # First read the body of the answer once
            response_bytes = await response.aread()

            if not response_bytes: # An empty body of an answer
                 if response.status_code in [200, 201, 204]: # Successful statuses for an empty answer
                    return {'success': True, 'status_code': response.status_code}
                 else: 
                    logger.warning(f'Пустой ответ со статусом ошибки {response.status_code}')
                    return None 

            # Determination of the actual format for parsing by Content-Type
            actual_parse_format: str = data_format # The expected default format is used
            if 'application/json' in response_content_type:
                actual_parse_format = 'JSON'
            elif 'application/xml' in response_content_type or 'text/xml' in response_content_type :
                actual_parse_format = 'XML'
            
            # Parsing based on a certain format
            if actual_parse_format == 'JSON':
                parsed_data = json.loads(response_bytes) # Bait Parsing
            elif actual_parse_format == 'XML':
                xml_text: str = response_bytes.decode('utf-8', errors='replace')
                parsed_data = xml2dict(xml_text) 
            else:
                logger.error(f'Неподдерживаемый формат для разбора: {actual_parse_format}. Content-Type: {response_content_type}. Тело (часть): {response_bytes[:200]}...')
                return None
            
            # Processing the standard wrapper 'Prestashop' in response
            if isinstance(parsed_data, dict) and 'prestashop' in parsed_data and len(parsed_data) == 1:
                # If Parsed_Data is {'Prestashop': Actual_Data}, we extract Actual_Data
                return parsed_data['prestashop'] # type: ignore
            
            # If XML2DICT has returned the list (for example, for a root element that is a list)
            if isinstance(parsed_data, list):
                 # It can be specific to your XML2DICT. If the API returns a list of objects without a wrapper.
                 # We convert into the vocabulary with the default key in order to correspond to the return type DICT | None
                 logger.warning(f'Ответ API был списком, обернут в словарь с ключом "data": {parsed_data[:3]}...')
                 return {'data': parsed_data}

            return parsed_data # PARSED_DATA already DICT or NONE (if XML2DICT has returned None)

        except json.JSONDecodeError as ex_json:
            response_text_sample: str = response_bytes.decode('utf-8', errors='replace')[:500]
            logger.error(f'Ошибка разбора JSON: {ex_json}. Текст ответа (часть): {response_text_sample}...', ex_json, exc_info=True)
            return None
        except ExpatError as ex_xml: 
             response_text_sample = response_bytes.decode('utf-8', errors='replace')[:500]
             logger.error(f'Ошибка разбора XML: {ex_xml}. Текст ответа (часть): {response_text_sample}...', ex_xml, exc_info=True)
             return None
        except Exception as ex_gen: # Any other errors in parsing
            logger.error('Общая ошибка разбора ответа', ex_gen, exc_info=True)
            return None

    async def create_async(self, resource: str, data: dict, **kwargs: Any) -> dict | None:
        """Asynchronously creates a new resource in Prestashop API.

        Args:
            Resource (str): the name of the resource (for example, 'Taxes', 'Products').
            DATA (DICT): Data for creating a resource. 
                         The structure of the dictionary must correspond to the expectations of the API Prestashop 
                         For the selected `Data_Format` (json or xml).
            ** kwargs (Any): additional named arguments for transmission to `_exec_async`,
                            For example, `Language` for indicating the language of the created content.

        Returns:
            dict | None: API response with data of the created resource (usually includes ID), 
                         Or `none` in case of error.
        
        Example:
            >>> TAX_PAYLOAD = {'TAX': {'RATE': '5.000', 'Active': '1', 
            ... 'Name': {'Language': {'attrs': {'id': '1'}, 'value': 'New Tax'}}}}
            >>> # Creed_tax_info = AWAIT API.create_async ('Taxes', Tax_Payload)
            >>> # If Creed_tax_info: Print (F "Creed Tax ID: {Creed_Tax_info.get ('Tax', {}). Get ('id')}")"""
        # The function performs the creation of a resource
        return await self._exec_async(resource=resource, method='POST', payload=data, **kwargs)

    async def read_async(self, resource: str, resource_id: int | str, **kwargs: Any) -> dict | None:
        """Asynchronously reads (extracts) the data of the specified resource from the Prestashop API.

        Args:
            Resource (str): the name of the resource (for example, 'products', 'cubomers').
            Resource_id (int | str): a unique reading resource identifier.
            ** kwargs (Any): additional named arguments for transmission to `_exec_async`,
                            For example, `Display = 'Full'` to obtain all the fields of the resource.

        Returns:
            dict | None: data of the requested resource from the API in the form of a dictionary, 
                         or `none` in the case of an error (for example, the resource was not found).

        Example:
            >>> # Product_Details = AWAIT API.READ_ASYNC ('Products', 1, Display = 'Full')
            >>> # If Product_Details: Print (F "Product Name: {Product_details.get ('Product', {}). Get ('Name')}")"""
        # The function performs a resource reading
        return await self._exec_async(resource=resource, resource_id=resource_id, method='GET', **kwargs)

    async def write_async(self, resource: str, resource_id: int | str, data: dict, **kwargs: Any) -> dict | None:
        """Asynchronically updates the existing resource in Prestashop API.
        Prestashop API requires the `ID` renewed resource to be included in the` Data` body.

        Args:
            Resource (str): the name of the resource (for example, 'Customers', 'Addresses').
            Resource_id (int | str): a unique resource identifier for updating.
            DATA (DICT): Data for updating. The dictionary must contain the key with the ID resource,
                         corresponding to `resource_id`.
            ** KWARGS (ANY): additional named arguments for transmission to `_exec_async`.

        Returns:
            dict | None: API response after update (often an updated resource), 
                         Or `none` in case of error.
        
        Example:
            >>> update_payload = {'Product': {'id': '1', 'Active': '0', 'Price': '99 .99 '}}}}}
            >>> # updated_product_info = AWAIT API.Write_async ('Products', 1, Update_payload)
            >>> # if updated_product_info: print (f "Updated Product Active Status: {Updated_product_info.get ('Product', {}). Get ('Active')}") ")") """"
        # The function performs the update of the resource
        # Make sure that `Data` contains ID, as Prestashop expects, for example:
        # data = {'product': {'id': str(resource_id), 'name': 'New Name'}}
        return await self._exec_async(
            resource=resource,
            resource_id=resource_id,
            method='PUT',
            payload=data, 
            **kwargs,
        )

    async def unlink_async(self, resource: str, resource_id: int | str) -> bool:
        """Asynchronically deleys the specified resource from Prestashop API.

        Args:
            Resource (str): the name of the resource (for example, 'Orders', 'Carts').
            Resource_id (int | str): a unique resource identifier for removal.

        Returns:
            Bool: `true` in case of successful removal (API returns 200 OK or 204 No Content), 
                  `False` otherwise.
        
        Example:
            >>> # SUCCESS = AWAIT API.unLink_async ('Taxes', 10)
            >>> # If Success: Print ("Tax Successfully Deleted.")"""
        # The function performs the removal of the resource
        response_data: dict | None = await self._exec_async(resource=resource, resource_id=resource_id, method='DELETE')
        return bool(response_data and response_data.get('success', False))


    async def search_async(self, resource: str, filter: str | dict | None = None, **kwargs: Any) -> dict | None: 
        """Asynchronously looking for resources in Prestashop API according to the given criteria.

        The filter (`filter`) can be a line in the format expected Prestashop API 
        (for example, `filter [name] =%value%& filter [active] = 1`), 
        or a dictionary (for example, `{'name': '%value%', 'active': '1'}`), 
        which will be automatically transformed into the desired format of the query line.

        Args:
            Resource (str): the name of the resource for the search (for example, 'Products', 'Categories').
            Filter (str | dict | None, Optional): Filtering criteria for search.
            ** KWARGS (ANY): Additional search control parameters (for example, `Limit`,` Sort`, `Display`).

        Returns:
            dict | None: API response containing a list of resources found (or one resource, if it is so conceived by the API),
                         Or `none` in case of error. The response structure depends on the API (often it is `{'Resource_plural_name': [...]}`).
        
        Example:
            >>> # search_params = {'name': '%laptop%', 'active': '1'}
            >>> # Results = AWAIT API.Search_async ('Products', Filter = Search_params, Limit = 5, Display = '[ID, NAME]')
            >>> # If Results and Results.get ('Products'):
            ... # For Product in Results ['Products']: Print (F "ID: {Product ['id']}, NAME: {Product ['name']}")"""
        # The function is the search for resources
        return await self._exec_async(resource=resource, method='GET', filter=filter, **kwargs)

    async def create_binary_async(self, resource_path: str, file_path: str, file_name_in_request: str) -> dict | None:
        """Asynchronously uploads a binary file (for example, image) in Prestashop API.
        It is used to download files directly, for example, when creating images for goods.

        Args:
            Resource_path (str): the path to the API resource, where the file will be uploaded 
                                 (for example, 'Images/Products/22' for depicting goods with ID 22).
            File_path (str): the local path to the file that must be downloaded.
            File_name_in_request (str): the name of the file that will be indicated in the multipart/form-data request. 
                                        Prestashop can use this name or generate its own.

        Returns:
            dict | None: response from the API Prestashop after downloading the file (usually contains a loaded file metadata), 
                         Or `none` in case of error.
        
        RAISES:
            Prestashopexception: If the HTTP client is not initialized or with critical network/request errors.

        Example:
            >>> # Image_upload_Response = AWAIT API.create_ASYNC ('Images/Products/1', 'Path/to/Local_image.jpg', 'Product_Image.jpg')
            >>> # If Image_upload_Response: Print (F "Uploaded Image Info: {Image_upload_Response}")"""
        # Ads of variables
        url_path: str
        files_data: dict
        response: httpx.Response
        parsed_response: dict | None

        if not self.client:
            raise PrestaShopException('Клиент не инициализирован.')
        if not self._initialized:
             await self._initialize_connection()

        url_path = resource_path.lstrip('/') # Removing the initial slash, if any, because Base_url is used
        
        try:
            path_obj: Path = Path(file_path)
            if not path_obj.is_file(): # Check that the file exists and is a file
                logger.error(f'Файл для бинарной загрузки не найден или не является файлом: {file_path}')
                return None

            with open(path_obj, 'rb') as file_obj:
                # MIME-type 'Image/JPEG' is an example, Prestashop can require specific types
                # Or determine it yourself. For universality, you can use 'Application/Octet-Stream'
                # Or the library of MimetyPes to determine the file expanding.
                files_data = {'image': (file_name_in_request, file_obj, 'application/octet-stream')} 
                
                logger.debug(f'Загрузка бинарного файла {file_path} в {url_path} как {file_name_in_request}')
                
                response = await self.client.post(url=url_path, files=files_data)

            if not await self._check_response_async(response, 'POST', url_path, req_data=f'Бинарный файл: {file_name_in_request}'):
                return None
            
            # The response from Prestashop after loading the image often XML.
            # _parse_response_async will try to determine the format by Content-Type,
            # But you can specify a priority format, if known.
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
        """Asynchronously extracts the scheme (structure) of the specified resource from the Prestashop API.
        This is useful for understanding the fields of the resource, their types and obligation.

        Args:
            Resource (Str | None, Optional): Resource name (for example, 'Products', 'Customers'). 
                                             If `none`, the API can return the list of all available schemes.
            Resource_id (int | None, Optional): ID of a specific copy of the resource. 
                                                It is rarely used to obtain a common scheme.
            Schema (Str | None, Optional): type of requested scheme (for example, 'Blank' for an empty structure, 
                                           'synopsis' for simplified). By default 'Blank'.
            ** kwargs (Any): additional named arguments transmitted in `_exec_async`.

        Returns:
            dict | None: a resource scheme presented in the form of a dictionary (usually from XML or JSON API response),
                         Or `none` in case of error.
        
        Example:
            >>> # Tax_Schema_blank = AWAIT API.GET_SCHEMA_ASYNC ('Taxes', Schema = 'Blank')
            >>> # If Tax_Schema_blank: Print (F "Blank Schema for Taxes: {J_dumps (Tax_Schema_blank, Indent = 2)}")"""
        # The function performs the extraction of a resource scheme
        return await self._exec_async(resource=resource, resource_id=resource_id, method='GET', schema=schema, **kwargs)

    async def get_data_async(self, resource: str, **kwargs: Any) -> dict | None:
        """Asynchronously extracts general data from the specified resource Prestashop API.
        This method is a wrap over `_Exec_async` with the Get method and can be used
        For requests that do not fall under standard CRUD operations (for example, reading configurations).

        Args:
            Resource (str): the name of the API resource (for example, 'configurations', 'shop_urls').
            ** kwargs (Any): additional arguments for transmission to `_exec_async`, 
                            Such as `Filter`,` Limit`, `Display` to configure the request.

        Returns:
            dict | None: Data from the API in the form of a dictionary, or `none` in case of error.
        
        Example:
            >>> # shop_configurations = await api.get_data_async ('configurations', display = '[name, value]')
            >>> # If Shop_configurations and Shop_configurations.get ('Configurations'):
            ... # for config_item in shop_configurations ['configurations']: print (config_item)"""
        # The function performs data extraction
        return await self._exec_async(resource=resource, method='GET', **kwargs)

    async def get_apis_async(self) -> dict | None:
        """Asynchronously receives a list of all available ento entities (resources) API Prestashop.
        The answer is usually the XML document that parses into the dictionary,
        containing information about available resources and their capabilities for the current key API.

        Returns:
            dict | None: a dictionary with a list of available API resources and their description,
                         Or `none` in case of error.
        
        Example:
            >>> # AVAILABLE_API_ENDPOINTS = AWAIT API.GET_APIS_ASYNC ()
            >>> # ifilable_api_endpoints: print (f "Available Apis: {j_dumps (available_api_endpoints, indent = 2)}") ")") ")""""
        # The function performs a list of available APIs
        # Request to the root `/API/` without specifying the resource (`Resource = ''`)
        return await self._exec_async(resource='', method='GET', data_format_override=self.data_format)


    async def upload_image_from_url_async(
        self, 
        resource_images_path: str, 
        entity_id: int, 
        img_url: str, 
        img_name_prefix: str | None = None 
    ) -> dict | None:
        """Asynchronously loads the image according to the URL in Prestashop.
        The process includes downloading the image in a temporary local file,
        And then downloading this file to the Prestashop server.

        Args:
            Resource_images_path (str): the base path for images of the resource in the API Prestashop 
                                        (for example, 'Images/Products').
            Entity_id (int): ID entities (for example, goods, categories) to which will be 
                             The image is tied.
            IMG_URL (str): URL images that need to be downloaded and loaded.
            IMG_NAME_PREFIX (str | None, Optional): optional prefix that will be added 
                                                    to the file name while saving on the server Prestashop 
                                                    And in the name of the temporary file.

        Returns:
            dict | None: The answer from the API Prestashop after loading the image, 
                         Or `none` in the case of any error in the process.
        
        Example:
            >>> # Product_id = 1
            >>> # image_url = 'https://toscrape.com//path/to/image.jpg'
            >>> # upload_Response = AWAIT API.UPLOAD_IMAGE_FROM_URL_ASYNC ('images/products', product_id, image_url, 'Main_image')
            >>> # if upload_response: Print ("Image Uploeded Successfolly from url.")"""
        # Ads of variables
        url_parts: list[str]
        extension: str
        base_filename: str
        local_temp_filename: str
        filename_in_request: str
        temp_dir: Path
        local_temp_filepath: str
        downloaded_filepath: str | None
        prestashop_resource_path: str
        response_data: dict | None = None # Initialization by default value


        url_parts = img_url.rsplit('.', 1)
        extension = url_parts[1] if len(url_parts) > 1 else 'jpg' # Default extension 'jpg'
        
        base_filename = str(entity_id)
        if img_name_prefix:
            base_filename += f'_{img_name_prefix}'
        
        local_temp_filename = f'{base_filename}_temp.{extension}'
        filename_in_request = f'{base_filename}.{extension}' # File name for Prestashop

        # Directory for temporary files, can be taken to config
        temp_dir = Path('temp_images_prestashop_api') 
        temp_dir.mkdir(parents=True, exist_ok=True) 
        local_temp_filepath = str(temp_dir / local_temp_filename)

        try:
            # 1. Asynchronous download of the image to a temporary file
            downloaded_filepath = await save_image_from_url_async(img_url, local_temp_filepath)
            if not downloaded_filepath or not Path(downloaded_filepath).exists(): # Checking the result of downloading
                logger.error(f'Ошибка загрузки изображения с {img_url} во временный файл.')
                return None # None return if downloading failed

            # 2. Download downloaded file in Prestashop
            # Formation of the path for the API: Images/Products/{id}
            prestashop_resource_path = f'{resource_images_path.strip("/")}/{entity_id}'
            
            response_data = await self.create_binary_async(
                resource_path=prestashop_resource_path, 
                file_path=downloaded_filepath, 
                file_name_in_request=filename_in_request
            )
            return response_data

        except Exception as ex: # Processing of any other exceptions
            logger.error(f'Ошибка в процессе upload_image_from_url_async для {img_url}', ex, exc_info=True)
            return None
        finally:
            # 3. Removing a temporary file after surgery
            if Path(local_temp_filepath).exists():
                await remove_file_async(local_temp_filepath)


    async def get_product_images_async(self, product_id: int) -> dict | None:
        """Asynchronously receives information about the images for the specified product.
        Data is extracted from the `Associations sections in the information about the product.

        Args:
            Product_id (int): a unique product identifier.

        Returns:
            dict | None: Dictionary containing a list of information about images 
                         (for example, `{'images': [{'id': '1'}, {'id': '2'}, ...]}`),
                         Or `none`, if the images were not found or an error has occurred.
        
        Example:
            >>> # Product_images_info = AWAIT API.GET_PRODUCT_IMAGES_ASYNC (1)
            >>> # If Product_images_info and Product_images_info.get ('images'):
            ... # Print (F "Found {Len (Product_images_info ['images'])} Images for Product.")
            ... # for IMG_info in Product_images_info ['images']: Print (f "Image id: {img_info.get ('id')}")"""
        # The function performs information about the images of the goods
        product_data: dict | None
        images_assoc_data: Any # Associations type can vary
        
        # Request for complete information about access to associations
        product_data = await self.read_async('products', product_id, display='full')
        
        if product_data and 'product' in product_data: 
            images_assoc_data = product_data['product'].get('associations', {}).get('images', {})
            
            # Processing of various response structures for images
            if isinstance(images_assoc_data, dict) and 'image' in images_assoc_data : 
                 actual_image_data = images_assoc_data['image']
                 # If 'Image' contains one object, wrap it on the list
                 return {'images': actual_image_data if isinstance(actual_image_data, list) else [actual_image_data]}
            elif isinstance(images_assoc_data, list): # If associations.images is already a list of ID or objects
                 return {'images': images_assoc_data}
            elif not images_assoc_data: # If associations.images is empty (None, empty dict/list)
                 logger.info(f'Для товара {product_id} не найдено ассоциированных изображений.')
                 return {'images': []} # Return of an empty list of images for consistency
        
        logger.warning(f'Не удалось извлечь информацию об изображениях для товара {product_id} через ассоциации.')
        return None


async def main_async() -> None:
    """Asynchronous demonstration function for checking work with Prestashop API.
    Performs operations of creating, reading, updating, searching and deleting a tax rate.
    It also contains an entrusted example for testing image loading."""
    # Ads of variables used in the function
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
    searched_taxes_response: dict | None # Changed name for clarity
    delete_success: bool

    # Using Config values or their reduction for the test
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

        # 1. Creation of a tax rate
        tax_data_create = {
            'tax': {
                'rate': '9.990', # Prestashop often expects a line for numerical values
                'active': '1',
                'name': { 
                    'language': [ # Array even for one language
                        {'attrs': {'id': str(api.language)}, 'value': f'Async Tax {gs.now.strftime("%H%M%S")}'} # Unique name
                    ]
                }
            }
        }
        
        created_tax_response = await api.create_async('taxes', tax_data_create)
        
        # Checking the success of creating and extracting ID
        if created_tax_response and isinstance(created_tax_response.get('tax'), dict) and 'id' in created_tax_response['tax']:
            tax_id = created_tax_response['tax']['id']
            logger.info(f'Налоговая ставка успешно создана. ID: {tax_id}, Ответ: {j_dumps(created_tax_response)}')

            # 2. Reading the created tax rate
            read_tax_response = await api.read_async('taxes', tax_id)
            logger.info(f'Чтение налоговой ставки ID {tax_id}: {j_dumps(read_tax_response)}')

            # 3. Updating the tax rate
            tax_data_update = {
                'tax': {
                    'id': str(tax_id), # ID is required for PUT
                    'rate': '10.100',
                    'active': '0', # Deactivation for example
                    'name': {
                        'language': [
                             {'attrs': {'id': str(api.language)}, 'value': f'Async Tax Updated {gs.now.strftime("%H%M%S")}'}
                        ]
                    }
                }
            }
            updated_tax_response = await api.write_async('taxes', tax_id, tax_data_update)
            logger.info(f'Налоговая ставка успешно обновлена. ID: {tax_id}, Ответ: {j_dumps(updated_tax_response)}')
            
            # 4. Search for tax rates
            searched_taxes_response = await api.search_async('taxes', filter={'name': '%Async Tax%'}, limit='5', display='full')
            
            taxes_list_found: list = []
            if searched_taxes_response and 'taxes' in searched_taxes_response:
                taxes_data_from_search = searched_taxes_response['taxes']
                # Processing the case when 'Tax' is one object or list of objects
                if isinstance(taxes_data_from_search, dict) and 'tax' in taxes_data_from_search:
                    tax_items = taxes_data_from_search['tax']
                    taxes_list_found = [tax_items] if isinstance(tax_items, dict) else tax_items
                elif isinstance(taxes_data_from_search, list): # If Prestashop returned the list directly for 'Taxes'
                    taxes_list_found = taxes_data_from_search
            
            if taxes_list_found:
                logger.info(f'Найдено налоговых ставок: {len(taxes_list_found)}')
                # for tax_item_found in taxes_list_found: print(j_dumps(tax_item_found)) # Вывод с помощью print (pprint)
            else:
                logger.info(f'Налоговые ставки с "Async Tax" не найдены или ответ пуст: {j_dumps(searched_taxes_response)}')


            # 5. Removing the created tax rate
            delete_success = await api.unlink_async('taxes', tax_id)
            logger.info(f'Налоговая ставка ID {tax_id} успешно удалена: {delete_success}')
        
        else: # If the creation of tax failed
            logger.error(f'Ошибка создания налоговой ставки. Ответ: {j_dumps(created_tax_response)}')

if __name__ == '__main__':
    # Checking the configuration before starting
    if Config.API_DOMAIN == 'https://your.prestashop.com' or Config.API_KEY == 'YOURAPIKEY':
         print('Обнаружены значения API_DOMAIN/API_KEY по умолчанию в Config.')
         print('Пожалуйста, установите корректные значения в src/endpoints/prestashop/api_async.py (класс Config)')
         print('Или измените их непосредственно в функции main_async для тестового запуска.')
    else:
        try:
            asyncio.run(main_async())
        except KeyboardInterrupt: # User interruption processing
            logger.info('Выполнение программы прервано пользователем (Ctrl+C).')
        except Exception as main_execution_exception: # Processing of other exceptions at the upper level
            logger.error('Произошла непредвиденная ошибка при выполнении main_async', main_execution_exception, exc_info=True)
