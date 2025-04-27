## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код демонстрирует пример использования библиотеки `iop` для работы с API AliExpress. Он создает клиента API, формирует запрос на получение аффилированной ссылки на товар и выводит полученный ответ.

Шаги выполнения
-------------------------
1. **Импортирование библиотеки `iop`**:
    -  `import iop` импортирует необходимую библиотеку для работы с API.
2. **Создание клиента API**:
    - `client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93')` создает объект `IopClient`, который будет использоваться для взаимодействия с API.
    - В качестве аргументов передаются:
        - `url`: URL API.
        - `appkey`: Ключ приложения.
        - `appSecret`: Секретный ключ приложения.
3. **Создание запроса**:
    - `request = iop.IopRequest('aliexpress.affiliate.link.generate')` создает объект `IopRequest`, который будет представлять запрос к API.
    - В качестве аргумента передается:
        - `method`: Имя метода API, который нужно вызвать.
4. **Добавление параметров запроса**:
    -  `request.add_api_param('promotion_link_type', '0')` добавляет в запрос параметр `promotion_link_type` со значением `0`.
    -  `request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')` добавляет параметр `source_values` со ссылкой на товар.
    -  `request.add_api_param('tracking_id', 'default')` добавляет параметр `tracking_id` со значением `default`.
5. **Выполнение запроса**:
    - `response = client.execute(request)` отправляет запрос к API и получает ответ.
6. **Обработка ответа**:
    - `print(response.body)` выводит содержимое ответа.
    - `print(response.type)` выводит тип ответа.
    - `print(response.code)` выводит код ответа.
    - `print(response.message)` выводит сообщение ответа.
    - `print(response.request_id)` выводит уникальный идентификатор запроса.

Пример использования
-------------------------
```python
import iop

# Создаем клиента API
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93')

# Создаем запрос на получение аффилированной ссылки
request = iop.IopRequest('aliexpress.affiliate.link.generate')

# Добавляем параметры запроса
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Выполняем запрос и получаем ответ
response = client.execute(request)

# Выводим информацию об ответе
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
```