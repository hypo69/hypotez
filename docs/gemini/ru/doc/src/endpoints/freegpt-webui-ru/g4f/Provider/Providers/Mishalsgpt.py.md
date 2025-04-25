# Mishalsgpt.py

## Обзор

Этот модуль предоставляет класс `Mishalsgpt`, который реализует провайдер для  Mishalsgpt - API, предоставляющего доступ к моделям GPT. 

## Подробнее

Этот файл реализует провайдера для Mishalsgpt, который используется в рамках проекта Hypotez для  обработки запросов к API  Mishalsgpt. 

## Классы

### `class Mishalsgpt`

**Описание**: Класс `Mishalsgpt` - провайдер для  Mishalsgpt, предоставляющий функциональность взаимодействия с API.

**Атрибуты**:

- `url` (str): URL-адрес API Mishalsgpt.
- `model` (list): Список доступных моделей.
- `supports_stream` (bool): Флаг, указывающий на поддержку потокового режима.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.

**Методы**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: 
    **Назначение**: Метод, отправляющий запрос к API Mishalsgpt для получения ответа от выбранной модели.
    **Параметры**:
        - `model` (str): Имя модели, используемой для генерации ответа.
        - `messages` (list): Список сообщений, отправляемых модели.
        - `stream` (bool): Флаг, указывающий на необходимость потокового режима.
    **Возвращает**: 
        - `dict | None`: Возвращает словарь с результатами генерации ответа или None в случае ошибки.
    **Пример**:
        ```python
        model = 'gpt-3.5-turbo'
        messages = ['Hello, world!']
        result = Mishalsgpt()._create_completion(model=model, messages=messages, stream=True)
        print(result)
        ```

## Функции

### `params`

**Назначение**: Функция формирует строку с описанием параметров, поддерживаемых провайдером.
**Возвращает**: 
    - `str`: Строка с описанием параметров.
**Пример**:
    ```python
    print(params)
    ```

## Параметры

- `url` (str): URL-адрес API Mishalsgpt.
- `model` (list): Список доступных моделей.
- `supports_stream` (bool): Флаг, указывающий на поддержку потокового режима.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.

## Примеры

**Пример использования**:
```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.Mishalsgpt import Mishalsgpt

provider = Mishalsgpt()

# Запрос к API
response = provider._create_completion(model='gpt-3.5-turbo', messages=['Hello, world!'], stream=True)
print(response)
```