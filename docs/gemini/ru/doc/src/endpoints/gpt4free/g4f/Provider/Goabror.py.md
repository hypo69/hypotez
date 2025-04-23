# Модуль для работы с провайдером Goabror
## \file hypotez/src/endpoints/gpt4free/g4f/Provider/Goabror.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для асинхронного взаимодействия с провайдером Goabror.
==============================================================

Модуль содержит класс `Goabror`, который используется для отправки запросов к API Goabror
и получения ответов в асинхронном режиме. Поддерживает прокси и предоставляет функциональность
для форматирования запросов.

Зависимости:
    - aiohttp
    - json
    - typing
    - src.endpoints.gpt4free.g4f.Provider.base_provider
    - src.endpoints.gpt4free.g4f.requests.raise_for_status
    - src.endpoints.gpt4free.g4f.Provider.helper

 .. module:: src.endpoints.gpt4free.g4f.Provider.Goabror
"""

## Обзор

Модуль `Goabror` предоставляет класс `Goabror` для асинхронного взаимодействия с API Goabror. Он использует библиотеку `aiohttp`
для выполнения асинхронных HTTP-запросов и предоставляет методы для форматирования запросов и обработки ответов.

## Подробней

Этот модуль предназначен для использования в проекте `hypotez` для обеспечения возможности взаимодействия с API Goabror.
Он позволяет отправлять запросы к API Goabror и получать ответы в асинхронном режиме, что позволяет повысить
производительность и отзывчивость приложения.

## Классы

### `Goabror`

**Описание**: Класс для асинхронного взаимодействия с провайдером Goabror.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): URL провайдера Goabror.
- `api_endpoint` (str): URL API endpoint для взаимодействия.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list): Список поддерживаемых моделей (включает `default_model`).

**Принцип работы**:
Класс `Goabror` предназначен для отправки запросов к API Goabror и обработки ответов. Он использует `aiohttp.ClientSession`
для выполнения асинхронных запросов. Метод `create_async_generator` создает асинхронный генератор, который отправляет
запрос к API и возвращает ответ.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Goabror.

    Args:
        cls (Goabror): Класс Goabror.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        Exception: В случае ошибки при выполнении запроса.

    Внутренние функции:
        Отсутствуют.

    Как работает функция:
    - Функция устанавливает заголовки запроса, включая `accept`, `accept-language` и `user-agent`.
    - Создает асинхронную сессию `aiohttp.ClientSession` с заданными заголовками.
    - Формирует параметры запроса, включая пользовательский запрос и системное сообщение.
    - Отправляет GET-запрос к API endpoint с использованием предоставленных параметров и прокси.
    - Обрабатывает ответ, проверяет статус код и извлекает данные из JSON или возвращает текст ответа.
    - Преобразует полученный результат в асинхронный генератор, который возвращает данные.
    """
```

**Параметры**:
- `cls` (Goabror): Класс Goabror.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Примеры**:

```python
# Пример вызова функции create_async_generator
messages = [{"role": "user", "content": "Hello, world!"}]
async for message in Goabror.create_async_generator(model="gpt-4", messages=messages):
    print(message)