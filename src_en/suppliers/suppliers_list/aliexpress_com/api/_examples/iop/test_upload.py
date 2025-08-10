## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_upload.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.iop.test_upload
    :platform: Windows, Unix
    :synopsis: Example of file upload to the AliExpress IOP API.

This module provides a commented-out example of how to upload a file to the AliExpress IOP API
using the `iop` library. It demonstrates setting up the client, creating a request with file parameters,
and executing the upload.

Example usage
-------------

```python
    # import iop

    # # Example of uploading a file
    # # client = iop.IopClient('https://api.taobao.tw/rest', '${appKey}', '${appSecret}')
    # # request = iop.IopRequest('/xiaoxuan/mockfileupload')
    # # request.add_api_param('file_name','pom.xml')
    # # request.add_file_param('file_bytes',open('/Users/xt/Documents/work/tasp/tasp/pom.xml').read())
    # # response = client.execute(request)
    # # print(response.body)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/iop/test_upload.py
"""
# # -*- coding: utf-8 -*-
#
# import iop
#
# # params 1 : gateway url
# # params 2 : appkey
# # params 3 : appSecret
# client = iop.IopClient('https://api.taobao.tw/rest', '${appKey}', '${appSecret}')
#
# # create a api request
# request = iop.IopRequest('/xiaoxuan/mockfileupload')
#
# # simple type params ,Number ,String
# request.add_api_param('file_name','pom.xml')
#
# # file params, value should be file content
# request.add_file_param('file_bytes',open('/Users/xt/Documents/work/tasp/tasp/pom.xml').read())
#
# response = client.execute(request)
# #response = client.execute(request,access_token)
#
#
# # response type nil,ISP,ISV,SYSTEM
# # nil ：no error
# # ISP : API Service Provider Error
# # ISV : API Request Client Error
# # SYSTEM : Iop platform Error
# print(response.type)
#
# # response code, 0 is no error
# # print(response.code)
#
# # response error message
# # print(response.message)
#
# # response unique id
# # print(response.request_id)
#
# # full response
# # print(response.body)
#
#
