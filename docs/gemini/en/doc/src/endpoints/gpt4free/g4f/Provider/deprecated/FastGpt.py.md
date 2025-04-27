# FastGpt.py

## Overview

Этот модуль содержит класс `FastGpt`, реализующий провайдера для доступа к модели FastGPT. 

## Details

`FastGpt` реализует интерфейс `AbstractProvider`, предоставляя возможность взаимодействовать с моделью FastGPT для генерации текста, используя методы  `create_completion`. 

## Classes

### `FastGpt`

**Description**: Класс `FastGpt`  реализует провайдера для доступа к модели FastGPT. 

**Inherits**:  `AbstractProvider`

**Attributes**:

-   `url`: URL-адрес для запросов к FastGPT API.
-   `working`: Признак, указывающий, доступна ли модель FastGPT.
-   `needs_auth`: Необходимость аутентификации.
-   `supports_stream`: Поддержка потоковой передачи.
-   `supports_gpt_35_turbo`: Поддержка модели `gpt-3.5-turbo`.
-   `supports_gpt_4`: Поддержка модели `gpt-4`.


**Methods**:

-   `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`:
    Создает завершение (генерацию текста) для модели FastGPT.

## Functions

### `create_completion`

**Purpose**:  Создает завершение (генерацию текста) для модели FastGPT.

**Parameters**:

-   `model` (str): Имя модели (например, `gpt-3.5-turbo`).
-   `messages` (list[dict[str, str]]): Список сообщений, передаваемых модели для генерации.
-   `stream` (bool): Флаг, указывающий на то, должна ли генерация текста быть потоковой.
-   `**kwargs`: Дополнительные параметры для модели, такие как `temperature`, `presence_penalty`, `frequency_penalty`, `top_p`.


**Returns**:

-   `CreateResult`: Результат генерации текста, включающий текст и информацию о модели.

**How the Function Works**:

1.  `create_completion` формирует заголовок HTTP-запроса.
2.  Создает JSON-данные запроса, содержащие текст, модель, параметры, необходимые для генерации.
3.  Отправляет POST-запрос к API FastGPT с сформированными данными.
4.  Если задан параметр `stream=True`,  обрабатывает ответ в потоковом режиме, вызывая функцию `yield` для каждого полученного токена текста.
5.  Возвращает результат генерации, включающий текст и информацию о модели.

**Examples**:

```python
# Пример вызова функции create_completion с потоковой генерацией текста:
result = FastGpt.create_completion(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'Привет!'}
    ],
    stream=True,
)

for token in result:
    print(token, end='')

# Пример вызова функции create_completion без потоковой генерации текста:
result = FastGpt.create_completion(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'Привет!'}
    ],
    stream=False,
)

print(result.text)

```
```python
## \file hypotez/src/endpoints/gpt4free/g4f/Provider/deprecated/FastGpt.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3