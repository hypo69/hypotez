## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_get.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.iop.test_get
    :platform: Windows, Unix
    :synopsis: Example of a GET request to the AliExpress IOP API.

This module demonstrates how to make a GET request to the AliExpress IOP API
using the `iop` library, including setting up the client, creating a request,
and processing the response.

Example usage
-------------

```python
    import iop

    # Example of making a GET request
    # client = iop.IopClient('https://api-pre.aliexpress_com.com/sync', '33505222', 'e1fed6b34feb26aabc391d187732af93')
    # request = iop.IopRequest('aliexpress_com.logistics.redefining.getlogisticsselleraddresses', 'POST')
    # request.set_simplify()
    # request.add_api_param('seller_address_query','pickup')
    # response = client.execute(request,"50000001a27l15rndYBjw6PrtFFHPGZfy09k1Cp1bd8597fsduP0RStringNormalizery0jhF6FL")
    # print(response.body)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_get.py
"""

import iop

# params 1 : gateway url
# params 2 : appkey
# params 3 : appSecret
client = iop.IopClient('https://api-pre.aliexpress_com.com/sync', '33505222', 'e1fed6b34feb26aabc391d187732af93')

# create a api request set GET mehotd
# default http method is POST
request = iop.IopRequest('aliexpress_com.logistics.redefining.getlogisticsselleraddresses', 'POST')
request.set_simplify()
# simple type params ,Number ,String
request.add_api_param('seller_address_query','pickup')

response = client.execute(request,"50000001a27l15rndYBjw6PrtFFHPGZfy09k1Cp1bd8597fsduP0RStringNormalizery0jhF6FL")

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
