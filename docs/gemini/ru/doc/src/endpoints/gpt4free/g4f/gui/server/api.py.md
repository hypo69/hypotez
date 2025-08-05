# Модуль API для GPT4Free 

## Обзор

Данный модуль предоставляет API для взаимодействия с сервером GPT4Free. Он включает в себя функции для получения информации о доступных моделях, провайдерах, версиях, а также для обработки запросов к GPT4Free. 

## Подробней

Модуль `api.py` в проекте `hypotez`  предназначен для работы с сервисом GPT4Free. Он содержит функции для взаимодействия с сервером GPT4Free и предоставляет API для других модулей проекта. 

## Классы

### `class Api`

**Описание**: Класс `Api` содержит методы для обработки запросов к GPT4Free.

**Методы**:

#### `get_models()`

**Назначение**: Функция возвращает список доступных моделей в GPT4Free.

**Возвращает**:
- `list`: Список словарей с описанием моделей. Каждый словарь содержит следующие ключи:
    - `name` (str): Имя модели.
    - `image` (bool): Флаг, указывающий, является ли модель  моделью для генерации изображений.
    - `vision` (bool): Флаг, указывающий, является ли модель моделью для обработки изображений.
    - `providers` (list): Список провайдеров, поддерживающих данную модель.

**Пример**:
```python
>>> Api.get_models()
[
    {'name': 'gpt-4', 'image': False, 'vision': False, 'providers': ['OpenAI']},
    {'name': 'text-davinci-003', 'image': False, 'vision': False, 'providers': ['OpenAI']},
    {'name': 'DALL-E 2', 'image': True, 'vision': False, 'providers': ['OpenAI']},
    ...
]
```

#### `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`

**Назначение**: Функция возвращает список моделей, доступных для указанного провайдера.

**Параметры**:

- `provider` (str): Имя провайдера.
- `api_key` (str, optional): API-ключ для провайдера. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL для API провайдера. По умолчанию `None`.

**Возвращает**:
- `list`: Список словарей с описанием моделей для указанного провайдера. 

**Пример**:
```python
>>> Api.get_provider_models("OpenAI", api_key="YOUR_API_KEY")
[
    {'model': 'gpt-4', 'default': True, 'vision': False, 'image': False, 'task': None},
    {'model': 'text-davinci-003', 'default': False, 'vision': False, 'image': False, 'task': None},
    {'model': 'DALL-E 2', 'default': False, 'vision': False, 'image': True, 'task': None},
    ...
]
```

#### `get_providers()`

**Назначение**: Функция возвращает список доступных провайдеров для GPT4Free.

**Возвращает**:
- `list`: Список словарей с описанием провайдеров. Каждый словарь содержит следующие ключи:
    - `name` (str): Имя провайдера.
    - `label` (str): Отображаемое имя провайдера.
    - `parent` (str): Название родительского провайдера, если он есть.
    - `image` (bool): Флаг, указывающий, поддерживает ли провайдер модели для генерации изображений.
    - `vision` (bool): Флаг, указывающий, поддерживает ли провайдер модели для обработки изображений.
    - `nodriver` (bool): Флаг, указывающий, требует ли провайдер использования вебдрайвера.
    - `hf_space` (bool): Флаг, указывающий, является ли провайдер пространством Hugging Face.
    - `auth` (bool): Флаг, указывающий, требуется ли аутентификация для использования провайдера.
    - `login_url` (str): URL для входа в систему провайдера.

**Пример**:
```python
>>> Api.get_providers()
[
    {'name': 'OpenAI', 'label': 'OpenAI', 'parent': None, 'image': True, 'vision': True, 'nodriver': False, 'hf_space': False, 'auth': True, 'login_url': None},
    {'name': 'GoogleGemini', 'label': 'Google Gemini', 'parent': None, 'image': False, 'vision': False, 'nodriver': False, 'hf_space': False, 'auth': False, 'login_url': None},
    {'name': 'HuggingFace', 'label': 'Hugging Face', 'parent': None, 'image': True, 'vision': True, 'nodriver': True, 'hf_space': True, 'auth': False, 'login_url': None},
    ...
]
```

#### `get_version()`

**Назначение**: Функция возвращает информацию о текущей и последней версии GPT4Free.

**Возвращает**:
- `dict`: Словарь с информацией о версиях. 

**Пример**:
```python
>>> Api.get_version()
{'version': '1.2.3', 'latest_version': '1.2.4'}
```

#### `serve_images(self, name)`

**Назначение**: Функция обслуживает изображения, хранящиеся в директории `images_dir`.

**Параметры**:

- `name` (str): Имя файла изображения.

**Возвращает**:
- `flask.Response`: Ответ Flask с изображением.

**Пример**:
```python
>>> Api.serve_images("image.png") 
```

#### `_prepare_conversation_kwargs(self, json_data: dict)`

**Назначение**: Функция подготавливает аргументы для создания нового разговора.

**Параметры**:

- `json_data` (dict): Данные из JSON.

**Возвращает**:
- `dict`: Словарь с аргументами для создания нового разговора.

**Пример**:
```python
>>> Api._prepare_conversation_kwargs({'model': 'gpt-3.5-turbo', 'provider': 'OpenAI', 'messages': [{'role': 'user', 'content': 'Привет!'}]})
{'model': 'gpt-3.5-turbo', 'provider': 'OpenAI', 'messages': [{'role': 'user', 'content': 'Привет!'}], 'tool_calls': [{'function': {'name': 'bucket_tool'}, 'type': 'function'}], 'conversation': None}
```

#### `_create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator`

**Назначение**: Функция создает поток ответов для GPT4Free.

**Параметры**:

- `kwargs` (dict): Словарь с аргументами для GPT4Free.
- `conversation_id` (str): ID разговора.
- `provider` (str): Имя провайдера.
- `download_media` (bool, optional): Флаг, указывающий, следует ли загружать медиафайлы. По умолчанию `True`.

**Возвращает**:
- `Iterator`: Итератор, возвращающий частичные ответы от GPT4Free.

**Пример**:
```python
>>> Api._create_response_stream({'model': 'gpt-3.5-turbo', 'provider': 'OpenAI', 'messages': [{'role': 'user', 'content': 'Привет!'}]}, 'conversation_id': '12345', 'provider': 'OpenAI')
<generator object Api._create_response_stream.<locals>.<genexpr> at 0x7f8800000000>
```

#### `_yield_logs()`

**Назначение**: Функция выдает лог-сообщения в формате JSON.

**Возвращает**:
- `Iterator`: Итератор, возвращающий лог-сообщения в формате JSON.

**Пример**:
```python
>>> Api._yield_logs()
<generator object Api._yield_logs at 0x7f8800000000>
```

#### `_format_json(self, response_type: str, content = None, **kwargs)`

**Назначение**: Функция форматирует ответ в JSON.

**Параметры**:

- `response_type` (str): Тип ответа.
- `content` (Any, optional): Содержимое ответа. По умолчанию `None`.
- `kwargs` (dict): Дополнительные параметры.

**Возвращает**:
- `dict`: Форматированный ответ в JSON.

**Пример**:
```python
>>> Api._format_json("content", "Привет!", urls=["https://example.com/image.png"], alt="Пример изображения")
{'type': 'content', 'content': 'Привет!', 'urls': ['https://example.com/image.png'], 'alt': 'Пример изображения'}
```

#### `handle_provider(self, provider_handler, model)`

**Назначение**: Функция обрабатывает провайдера и возвращает информацию о нем.

**Параметры**:

- `provider_handler` (BaseRetryProvider): Обработчик провайдера.
- `model` (str): Имя модели.

**Возвращает**:
- `dict`: Словарь с информацией о провайдере.

**Пример**:
```python
>>> Api.handle_provider(OpenAI, 'gpt-3.5-turbo')
{'type': 'provider', 'provider': {'name': 'OpenAI', 'label': 'OpenAI', 'parent': None, 'image': True, 'vision': True, 'nodriver': False, 'hf_space': False, 'auth': True, 'login_url': None}, 'model': 'gpt-3.5-turbo'}
```

## Функции

### `get_error_message(exception: Exception) -> str`

**Назначение**: Функция получает сообщение об ошибке из исключения.

**Параметры**:

- `exception` (Exception): Исключение.

**Возвращает**:
- `str`: Сообщение об ошибке.

**Пример**:
```python
>>> get_error_message(ValueError("Ошибка"))
'ValueError: Ошибка'