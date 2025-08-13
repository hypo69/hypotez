# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
"""`` `RST
  .. Module :: src.endpoints.prestashop.api
`` `
Module for interacting with Prestashop API.
======================================================================================ward

This module is provided by the class `Prestashop` to interact with Prestashop WebService API,
Using JSON and XML to format messages. He supports Crud operations, search,
and loading images, with error processing for answers.

Examples of use
-------------

`` `python

from src.endpoints.prestashop.api importshop

API = Prestashop (
    API_Domain = 'https: //your-prestashop-domain.com',
    API_KEY = 'your_API_KEY',
    Default_lang = 1,
    Debug = True,
    Data_Format = 'json',
)

API.Ping ()

Data = {
    'Tax': {
        'Rate': 3.000,
        'Active': '1',
        'name': {
            'Language': {
                'attrs': {'id': '1'},
                'value': '3% TAX'
            }
        }
    }
}

# Create Tax Record
Rec = API.create ('Taxes', Data)

# Update the Same Tax Record
update_data = {
    'Tax': {
        'ID': str (REC ['id']),
        'Rate': 3.000,
        'Active': '1',
        'name': {
            'Language': {
                'attrs': {'id': '1'},
                'value': '3% TAX'
            }
        }
    }
}

update_rec = API.Write ('Taxes', update_Data)

# Remove this Tax
API.unLink ('TAXES', STR (REC ['ID']))

# Search The First 3 Taxes with '5' in the Name
Import PPRINT
Recs = API.Search ('Taxes', Filter = '[Name] =%[5]%', limit = '3')

for recion in rec:
    PPRINT (REC)

# Create Binary (Product Image)
API.create_BINARY ('images/products/22', 'img.jpeg', 'image')
`` `"""
from urllib.parse import urlparse, unquote
import os
import mimetypes
import uuid
import asyncio
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

from header import __root__
from src import gs
from src.logger.exceptions import PrestaShopAuthenticationError, PrestaShopException
from src.logger.logger import logger
from src.utils.convertors.base64 import base64_to_tmpfile
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
    """Configuration class for PrestaShop API."""

    language: str
    ps_version: str = ''
    MODE: str = 'dev'  # 'dev8', 'prod'
    """Mode (str) = defines the final point API
    Accepted values:
    `dev` - dev.emil_design.com Prestashop 1.7
    `dev8` - DEV8.emil_Design.com Prestashop 8
    `Prod` - emil_design.com Prestashop 1.7 < - ⚠️ Attention!  Store!"""
    POST_FORMAT = 'JSON'


class PrestaShop:
    """Interact with PrestaShop webservice API, using JSON and XML for message

    This class provides methods to interact with the PrestaShop API, allowing for CRUD
    operations, searching, and uploading images. It also provides error handling
    for responses and methods to handle the API's data.

    Args:
        api_key (str): The API key generated from PrestaShop.
        api_domain (str): The domain of the PrestaShop shop (e.g., https://myPrestaShop.com).
        data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
        default_lang (int): Default language ID. Defaults to 1.
        debug (bool): Activate debug mode. Defaults to True.

    Raises:
        PrestaShopAuthenticationError: When the API key is wrong or does not exist.
        PrestaShopException: For generic PrestaShop WebServices errors."""

    client: Session = Session()
    debug: bool = True
    language: Optional[int] = None
    data_format: str = Config.POST_FORMAT  # Default data format ('JSON' or 'XML')
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
        """Initialize the PrestaShop class.

        Args:
            data_format (str): Default data format ('JSON' or 'XML'). Defaults to 'JSON'.
            default_lang (int): Default language ID. Defaults to 1.
            debug (bool): Activate debug mode. Defaults to True."""
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
        """Test if the webservice is working perfectly.

        Returns:
            bool: Result of the ping test. Returns `True` if the webservice is working, otherwise `False`."""
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
        """Check the response status code and handle errors.

        Args:
            status_code (int): HTTP response status code.
            response (requests.Response): HTTP response object.
            method (Optional[str]): HTTP method used for the request.
            url (Optional[str]): The URL of the request.
            headers (Optional[dict]): The headers used in the request.
            data (Optional[dict]): The data sent in the request.

        Returns:
            bool: `True` if the status code is 200 or 201, otherwise `False`."""
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
        """Parse the error response from PrestaShop API.

        Args:
            response (requests.Response): HTTP response object from the server."""

        if Config.POST_FORMAT == 'JSON':
            status_code: int = response.status_code
            if not status_code in (200, 201):
                j_dumps(response.json())

                logger.error(
                    f"""response status code: {status_code}
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
        """Prepare the URL for the request.

        Args:
            url (str): The base URL.
            params (dict): The parameters for the request.

        Returns:
            str: The prepared URL with parameters."""
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
        """Execute an HTTP request to the PrestaShop API."""

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

            # Installation Content-Type: Application/JSON
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
                headers=request_headers,  # At least the Content-Type Json/XML title
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
        """Parse XML or JSON response from the API to dict structure

        Args:
            text (str): Response text.

        Returns:
            dict: Parsed data or `False` on failure."""

        try:
            data: dict = response.json() # if self.data_format == 'JSON' else xml2dict(response.text)
            return data.get('prestashop', {}) if 'prestashop' in data else data

        except Exception as ex:
            logger.error(f'Parsing Error:', ex)
            ...
            return {}

    async def create_async(self, resource: str, data: dict, *args, **kwargs) -> Optional[dict]:
        """Asynchronously create a new resource in PrestaShop API.
        Args:
            resource (str): API resource (e.g., 'products').
            data (dict): Data for the new resource.
        Returns:
            dict: Response from the API."""
        return self._exec(resource=resource, method='POST', data=data, *args, **kwargs)

    def create(self, resource: str, data: dict, *args, **kwargs) -> Optional[dict]:
        """Create a new resource in PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'products').
            data (dict): Data for the new resource.

        Returns:
            dict: Response from the API."""
        # data  = {'prestashop' : data}
        return self._exec(resource=resource, method='POST', data=data, *args, **kwargs)

    def read(self, resource: str, resource_id: int | str, **kwargs) -> Optional[dict]:
        """Read a resource from the PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'products').
            resource_id (int | str): Resource ID.

        Returns:
            dict: Response from the API."""
        return self._exec(resource=resource, resource_id=resource_id, method='GET', **kwargs)

    def write(self, resource: str, resource_id:int|str, data: dict, **kwargs) -> Optional[dict]:
        """Update an existing resource in the PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'products').
            data (dict): Data for the resource.

        Returns:
            dict: Response from the API."""
        return self._exec(
            resource=resource,
            resource_id=resource_id,
            method='PUT',
            data=data,
            **kwargs,
        )

    def unlink(self, resource: str, resource_id: int | str) -> bool:
        """Delete a resource from the PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'products').
            resource_id (int | str): Resource ID.

        Returns:
            bool: `True` if successful, `False` otherwise."""
        return self._exec(resource=resource, resource_id=resource_id, method='DELETE')

    def search(self, resource: str, filter: Optional[str | dict] = None, **kwargs) -> List[dict]:
        """Search for resources in the PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'products').
            filter (Optional[str  |  dict]): Filter for the search.

        Returns:
            List[dict]: List of resources matching the search criteria."""
        return self._exec(resource=resource, search_filter=filter, method='GET', **kwargs)

    def create_binary(self, resource: str, file_path: str, file_name: str) -> dict:
        """Upload a binary file to a PrestaShop API resource."""

        try:
            with open(file_path, 'rb') as file:
                files: dict = {
                    'image': (file_name, file, 'image/jpeg')
                }  # Replace 'Image/JPEG' with the correct MIME-type
                response: requests.Response = self.client.post(
                    url=f'{self.api_domain}images/{resource}',
                    files=files,
                    auth=self.client.auth,  # It is important to transmit authentication,
                )

                response.raise_for_status()  # Checking for http-losecons

                # return response.json()
                return self._parse_response(response=response)

        except RequestException as ex:
            logger.error(f'Ошибка при загрузке изображения:', ex)
            return {'error': str(ex)}

        except Exception as ex:
            logger.error(f'Error:', ex)
            return {'error': str(ex)}

    def get_schema(
        self, resource: Optional[str] = None, resource_id: Optional[int] = None, schema: Optional[str] = 'blank', **kwargs
    ) -> dict | None:
        """Retrieve the Schema of a Given Resource from Prestashop API.

        Args:
            Resource (str): The Name of the Resource (E.G., 'Products', 'Customers').
                If not indicated, the list of all the entities of the key available for the API will return
            Resource_id (Optinal [str]):
            Schema (Optional [str]): The following options are usually implied:
                - Blank: (The most common option, as in your code)
                    Returns an empty resource scheme. This is useful for determining the minimum set of fields,
                    necessary to create a new object. That is, returns the structure of XML or JSON with empty fields,
                    which can be filled with data.
                - Synopsis (or Simplified): In some versions and for some resources, an option may exist,
                    Returning a simplified scheme. It can contain only the main fields of the resource and their types.
                    It can be more convenient than a full scheme if you do not need all the details.
                - Full (or without Schema): Often, if the Schema parameter is not indicated,
                    Or if it is indicated as Full, the full resource scheme is returned. She includes all the fields, their types,
                    Possible values, descriptions and other metadata. This is the most detailed type of scheme.
                - Form (or something similar): less often, but there may be an option that returns the scheme,
                    optimized for display in the form of editing. She may include validation information
                    fields, display, etc.

        Returns:
            dict |  None: The Schema of the Requested Resource or None` in Case of Anerror."""
        return self._exec(resource=resource, resource_id=resource_id, schema=schema, method="GET", **kwargs)

    def get_data(self, resource: str, **kwargs) -> Optional[dict]:
        """Fetch data from a PrestaShop API resource and save it.

        Args:
            resource (str): API resource (e.g., 'products').
            **kwargs: Additional arguments for the API request.

        Returns:
            dict | None: Data from the API or `False` on failure."""
        return self._exec(resource=resource, method='GET', **kwargs)

    def get_apis(self) -> Optional[dict]:
        """Get a list of all available APIs.

        Returns:
            dict: List of available APIs."""
        return self._exec('apis', method='GET', data_format=self.data_format)

    async def upload_image_from_url_async(
        self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
    ) -> Optional[dict]:
        """Upload an image to PrestaShop API asynchronously.

        Args:
            resource (str): API resource (e.g., 'images/products/22').
            resource_id (int): Resource ID.
            img_url (str): URL of the image.
            img_name (Optional[str]): Name of the image file, defaults to None.

        Returns:
            dict | None: Response from the API or `False` on failure."""
        asyncio.run(self.upload_image_from_url(resource, resource_id, img_url, img_name))



    def upload_image_from_url(
        self, resource: str, resource_id: int, img_url: str, img_name: Optional[str] = None
    ) -> Optional[dict]:
        """Upload an image to PrestaShop API.

        Args:
            resource (str): API resource (e.g., 'images/products/22').
            resource_id (int): Resource ID.
            img_url (str): URL of the image.
            img_name (Optional[str]): Optional desired base name for the file.

        Returns:
            dict | None: Response from the API or None on failure."""
        # Extracting expansion from URLs
        path = urlparse(img_url).path
        filename_from_url = os.path.basename(path)
        name_part, ext = os.path.splitext(filename_from_url)

        # An attempt to guess MIME-type if the extension is not found
        if not ext:
            mime_type, _ = mimetypes.guess_type(img_url)
            ext = mimetypes.guess_extension(mime_type) or '.jpg'  # By default .jpg

        # Cleaning and Formation File name
        safe_img_name = img_name or name_part or str(uuid.uuid4())
        safe_img_name = safe_img_name.strip().replace(' ', '_')
        filename = f"{resource_id}_{safe_img_name}{ext}"

        # Loading the image
        file_path = save_image_from_url(img_url, filename)
        response = self.create_binary(resource, file_path, safe_img_name)
        self.remove_file(file_path)

        return response


    def get_product_images(self, product_id: int) -> Optional[dict]:
        """Get images for a product.

        Args:
            product_id (int): Product ID.

        Returns:
            dict | None: List of product images or `False` on failure."""
        return self._exec(f'products/{product_id}/images', method='GET', data_format=self.data_format)












    # None


def main() -> None:
    """Checking the entities Prestashop"""
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
        api_domain = Config.API_DOMAIN,
        api_key = Config.API_KEY,
        default_lang = 1,
        debug = True,
        data_format = Config.POST_FORMAT,
    )
    api.create('taxes', data)
    api.write('taxes', data)

if __name__ == '__main__':
    main()
