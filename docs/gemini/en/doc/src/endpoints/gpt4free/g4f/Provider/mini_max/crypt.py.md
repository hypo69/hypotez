# Модуль шифрования для GPT4Free

## Обзор

Этот модуль содержит функции, которые отвечают за шифрование запросов к GPT4Free API.  Модуль реализует логику, которая позволяет обеспечить безопасность взаимодействия между клиентом и сервером GPT4Free.

## Детали

Этот модуль реализует шифрование запросов к GPT4Free API.  Модуль реализует логику, которая позволяет обеспечить безопасность взаимодействия между клиентом и сервером GPT4Free.

## Классы

### `CallbackResults`

**Описание**: Класс, который хранит результаты обратного вызова. 

**Атрибуты**:

- `token` (str): Токен аутентификации.
- `path_and_query` (str): Путь и параметры запроса.
- `timestamp` (int): Время запроса.

## Функции

### `hash_function`

**Назначение**:  Вычисляет хэш-сумму строки, используя MD5.

**Параметры**:

- `base_string` (str): Строка, для которой требуется вычислить хэш.

**Возвращает**:

- `str`: Хэш-сумма строки.

**Пример**:

```python
>>> hash_function("test")
'098f6bcd4621d373cade4e832627b4f6'
```

### `generate_yy_header`

**Назначение**:  Генерирует заголовок YY для запроса GPT4Free API.

**Параметры**:

- `has_search_params_path` (str): Путь к API с параметрами запроса.
- `body_to_yy` (dict): Тело запроса, преобразованное в строку.
- `time` (int): Время запроса.

**Возвращает**:

- `str`: Заголовок YY.

**Пример**:

```python
>>> generate_yy_header("/v4/api/chat/msg?a=1&b=2", "{'key':'value'}", 1688853522)
'a84203e4f0814044b203d1509b17a5e5'
```

### `get_body_to_yy`

**Назначение**:  Преобразует тело запроса в строку, используемую для генерации заголовка YY.

**Параметры**:

- `l` (dict): Тело запроса.

**Возвращает**:

- `str`: Тело запроса, преобразованное в строку.

**Пример**:

```python
>>> get_body_to_yy({"msgContent": "Hello, world!", "characterID": "123", "chatID": "456"})
'd41d8cd98f00b204e9800998ecf8427e72c203907255664718c8505f79d3912594e875d3703c5a4599f79532f6d2e496733752495cf4097ac96070e27e2b628609b784203e4f0814044b203d1509b17a5e5d41d8cd98f00b204e9800998ecf8427e7'
```

### `get_body_json`

**Назначение**:  Преобразует объект Python в строку JSON.

**Параметры**:

- `s` (dict): Объект Python.

**Возвращает**:

- `str`: Строка JSON.

**Пример**:

```python
>>> get_body_json({"key": "value"})
'{"key": "value"}'
```

### `get_browser_callback`

**Назначение**:  Создает функцию обратного вызова, которая извлекает токен аутентификации, путь и параметры запроса из браузера.

**Параметры**:

- `auth_result` (CallbackResults): Объект, который хранит результаты обратного вызова.

**Возвращает**:

- `function`: Функция обратного вызова, которая выполняется в браузере.

**Пример**:

```python
>>> auth_result = CallbackResults()
>>> callback = get_browser_callback(auth_result)
>>> # Вызываем callback в браузере
>>> callback(page)
```

**Описание**:

- `get_browser_callback` -  Эта функция создает функцию обратного вызова, которая будет выполняться в браузере для получения токена аутентификации, пути и параметров запроса. 

-  `callback` -  Функция обратного вызова. Она циклически проверяет наличие токена аутентификации в localStorage браузера.

- `await page.evaluate(...)` -  Выполняет JavaScript код в контексте страницы браузера. В коде получают данные о браузере, устройства и пользователя. Формируется строка с параметрами для запроса API. 

**Как работает функция**:

1. Функция `get_browser_callback` создает функцию обратного вызова, которая будет выполняться в браузере. 
2.  Функция обратного вызова циклически проверяет наличие токена аутентификации в localStorage браузера.
3. После получения токена функция извлекает данные о браузере, устройстве и пользователе.
4. Формирует строку с параметрами для запроса API и устанавливает атрибуты `auth_result.path_and_query`  и  `auth_result.timestamp`.

**Пример использования**:

```python
from src.endpoints.gpt4free.g4f.Provider.mini_max.crypt import get_browser_callback, CallbackResults
from src.webdirver import Driver, Chrome
from src.logger import logger

driver = Driver(Chrome)

async def get_auth_data():
    auth_result = CallbackResults()
    callback = get_browser_callback(auth_result)
    await driver.execute_locator({"event": "await callback(page)"})
    logger.info(f"Auth result: {auth_result.token}, {auth_result.path_and_query}, {auth_result.timestamp}")

if __name__ == "__main__":
    asyncio.run(get_auth_data())

```