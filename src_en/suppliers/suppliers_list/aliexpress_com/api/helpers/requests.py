## \file /src/suppliers/suppliers_list/aliexpress_com/api/helpers/requests.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.helpers.requests
    :platform: Windows, Unix
    :synopsis: Helper functions for making requests to the AliExpress API.

This module provides utility functions for making requests to the AliExpress API,
handling responses, and managing potential errors.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.helpers.requests import api_request
    from types import SimpleNamespace

    # Mock request object
    # class MockRequest:
    #     def getResponse(self):
    #         return {"aliexpress_affiliate_link_generate_response": {"resp_result": {"resp_code": 200, "result": "some_result"}}}

    # request = MockRequest()
    # response = api_request(request, "aliexpress_affiliate_link_generate_response")
    # print(response)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/helpers/requests.py
"""
from types import SimpleNamespace
from time import sleep
from src.logger.logger import logger
from src.utils.printer import pprint
import json

from ..errors import ApiRequestException, ApiRequestResponseException


def api_request(request, response_name, attemps:int = 1):
    try:
        response = request.getResponse()
    except Exception as error:
        if hasattr(error, 'message'):
            #raise ApiRequestException(error.message) from error
            #logger.critical(error.message,pprint(error))
            ...
            return

    try:
        response = response[response_name]['resp_result']
        response = json.dumps(response)
        response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    except Exception as error:
        #raise ApiRequestResponseException(error) from error
        logger.critical(error.message, pprint(error), exc_info=False)
        return
    try:
        if response.resp_code == 200:
            return response.result
        else:
            #raise ApiRequestResponseException(f'Response code {response.resp_code} - {response.resp_msg}')
            logger.warning(f'Response code {response.resp_code} - {response.resp_msg}',exc_info=False)
            return
    except Exception as ex:
        logger.error(None, ex, exc_info=False)
        return
