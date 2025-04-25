# Модуль Bard.py

## Обзор

Модуль `Bard.py` предоставляет функциональность для взаимодействия с моделью Google Bard через API. Он реализует класс `_create_completion` для генерации ответов от модели.

## Подробнее

Модуль `Bard.py` предназначен для использования в проекте `hypotez` в качестве провайдера для модели Google Bard. Он позволяет пользователям получать ответы от модели Bard через API.

## Классы

### `_create_completion`

**Описание**: Класс `_create_completion` реализует логику генерации ответов от модели Google Bard.

**Атрибуты**:

- `url` (str): URL-адрес для доступа к API Google Bard.
- `model` (list): Список поддерживаемых моделей. В данном случае, `Palm2`.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов. В данном случае, `False`.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации. В данном случае, `True`.


**Методы**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: 
    - **Назначение**: Функция, которая отправляет запрос к API Google Bard для генерации ответа модели.
    - **Параметры**:
        - `model` (str): Имя модели.
        - `messages` (list): Список сообщений в контексте диалога.
        - `stream` (bool): Флаг, указывающий на использование потоковой передачи.
        - `kwargs` (dict): Дополнительные параметры.
    - **Возвращает**: Генератор, который возвращает фрагменты ответа модели по мере их получения.
    - **Как работает**:
        - Функция извлекает идентификатор сессии (`psid`) из cookies браузера Google Chrome.
        - Форматирует список сообщений в текстовый формат, подходящий для отправки в API.
        - Создает запрос к API Google Bard с использованием библиотеки `requests`.
        - Извлекает данные из ответа API и возвращает их в виде генератора, который позволяет получать фрагменты ответа по мере их поступления.

## Функции

### `params`

**Назначение**:  Создает строку с описанием параметров, поддерживаемых в `_create_completion`.

**Параметры**:  None

**Возвращает**:  `str`:  Строка с описанием параметров.

**Как работает**:
-  С помощью `os.path.basename(__file__)[:-3]` получаем имя файла без расширения.
-  Получаем список параметров `_create_completion` с помощью `_create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]`.
-  Получаем типы параметров с помощью `get_type_hints(_create_completion)`.
-  Формируем строку с описанием параметров.

**Пример**:

```python
>>> print(params)
g4f.Providers.Bard supports: (model: str, messages: list, stream: bool, proxy: Any, snlm0e: Any, conversation_id: Any, response_id: Any, choice_id: Any)
```

## Примеры

```python
from ...typing import Dict, get_type_hints
import os

# Получение списка параметров 
parameters = [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]

# Печать информации о параметрах
print(f"g4f.Providers.{os.path.basename(__file__)[:-3]} supports: " + " ".join(parameters)) 

# Пример вызова функции _create_completion
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
for response in _create_completion(model="Palm2", messages=messages, stream=False, proxy="your_proxy_here"):
    print(response)
```