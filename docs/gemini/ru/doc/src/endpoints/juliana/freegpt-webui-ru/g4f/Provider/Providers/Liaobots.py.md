# Модуль Liaobots

## Обзор

Модуль предоставляет API для взаимодействия с моделью Liaobots, которая является бесплатным аналогом ChatGPT.  Liaobots позволяет использовать языковые модели GPT-3.5 и GPT-4 без подписки, но требует авторизации.

## Подробней

Этот файл содержит код, который реализует провайдера для Liaobots. Внутри модуля определены следующие элементы:

 - Переменные `url`, `model`, `supports_stream`, `needs_auth`, `models` - содержат информацию о модели и её параметрах, а также о том, поддерживается ли она.
 - Функция `_create_completion` - отправляет запросы к API Liaobots и возвращает результат.

## Классы

### `class None` 

 **Описание**:  В данном файле нет классов.

## Функции

### `_create_completion`

**Назначение**: Отправляет запрос к API Liaobots для генерации текста.

**Параметры**:

 - `model` (str): Название модели, например 'gpt-3.5-turbo' или 'gpt-4'.
 - `messages` (list): Список сообщений в чате, которые будут отправлены модели.
 - `stream` (bool): Указывает, нужно ли отправлять ответ модели по частям.
 - `**kwargs`: Дополнительные параметры, такие как `auth` для авторизации.

**Возвращает**:

 - `Generator[str, None, None]`: Генератор, который выдает части ответа модели по мере его получения.

**Как работает функция**:

 - `_create_completion` формирует JSON-запрос к API Liaobots, используя предоставленные параметры.
 - Запрос отправляется с помощью библиотеки `requests`, а ответ обрабатывается для выдачи частями.
 - В функцию `_create_completion`  предаются значения, которые определяются в других частях проекта, а также значения, полученные в результате работы других функций.

**Примеры**:

```python
from ...typing import sha256, Dict, get_type_hints
import os, uuid, requests
#  Пример вызова функции _create_completion
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
response = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth="YOUR_AUTH_TOKEN")
for token in response:
    print(token)
```


## Параметры

 - `url` (str): URL-адрес API Liaobots.
 - `model` (list): Список поддерживаемых моделей Liaobots.
 - `supports_stream` (bool): Указывает, поддерживает ли модель поток.
 - `needs_auth` (bool): Указывает, требуется ли авторизация для использования модели.
 - `models` (dict): Словарь с информацией о моделях, доступных в Liaobots.

## Примеры

```python
# Пример использования функции _create_completion
from ...typing import sha256, Dict, get_type_hints
import os, uuid, requests
#  Пример вызова функции _create_completion
messages = [
    {"role": "user", "content": "Привет, как дела?"},
]
response = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth="YOUR_AUTH_TOKEN")
for token in response:
    print(token)
```
```markdown