## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_internal.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.iop.test_internal
    :platform: Windows, Unix
    :synopsis: Example of an internal GET request to the AliExpress IOP API.

This module demonstrates how to make an internal GET request to the AliExpress IOP API
using the `iop` library, including setting up the client, creating a request,
and processing the response.

Example usage
-------------

```python
    import iop
    import time

    # Example of making an internal GET request
    # client = iop.IopClient('https://api-pre.taobao.tw/rest', '100240', 'hLeciS15d7UsmXKoND76sBVPpkzepxex')
    # request = iop.IopRequest('/product/item/get', 'GET')
    # request.add_api_param('itemId','157432005')
    # request.add_api_param('authDO', '{\"sellerId\":2000000016002}')
    # response = client.execute(request)
    # print(response.body)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_internal.py
"""

"""   [File's Description]

 
 @section libs imports:
  - iop 
  - time 
Author(s):
  - Created by Davidka on 09.11.2023 .
"""


import iop
import time

# params 1 : gateway url
# params 2 : appkey
# params 3 : appSecret
client = iop.IopClient('https://api-pre.taobao.tw/rest', '100240', 'hLeciS15d7UsmXKoND76sBVPpkzepxex')
# client.log_level = iop.P_LOG_LEVEL_DEBUG
# create a api request set GET mehotd
# default http method is POST
request = iop.IopRequest('/product/item/get', 'GET')

# simple type params ,Number ,String
request.add_api_param('itemId','157432005')
request.add_api_param('authDO', '{\"sellerId\":2000000016002}')

response = client.execute(request)
#response = client.execute(request,access_token)

# response type nil,ISP,ISV,SYSTEM
# nil :no error
# ISP : API Service Provider Error
# ISV : API Request Client Error
# SYSTEM : Iop platform Error
print(response.type)

# response code, 0 is no error
print(response.code)

# response error message
print(response.message)

# response unique id
print(response.request_id)

# full response
print(response.body)

print(str(round(time.time())) + '000')
