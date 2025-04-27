# OpenaiTemplate.py

## Overview

Этот модуль предоставляет класс `OpenaiTemplate`, который реализует базовый шаблон для взаимодействия с API OpenAI.

## Details

Класс `OpenaiTemplate` наследует от `AsyncGeneratorProvider`, `ProviderModelMixin` и `RaiseErrorMixin`. Он предоставляет методы для получения списка доступных моделей OpenAI, отправки запросов к API и обработки ответов.

## Classes

### `OpenaiTemplate`

**Description**: Класс, который реализует базовый шаблон для взаимодействия с API OpenAI.

**Inherits**:
  - `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
  - `ProviderModelMixin`: Предоставляет методы для работы с моделями.
  - `RaiseErrorMixin`: Предоставляет методы для обработки ошибок.

**Attributes**:
  - `api_base` (str): Базовый URL API OpenAI.
  - `api_key` (str): Ключ API OpenAI.
  - `api_endpoint` (str): Конечная точка API OpenAI.
  - `supports_message_history` (bool): Поддерживает ли модель историю сообщений.
  - `supports_system_message` (bool): Поддерживает ли модель системные сообщения.
  - `default_model` (str): Имя модели по умолчанию.
  - `fallback_models` (list[str]): Список резервных моделей.
  - `sort_models` (bool): Нужно ли сортировать модели.
  - `ssl` (bool): Нужно ли использовать SSL.
  - `models` (list[str]): Список доступных моделей OpenAI.
  - `image_models` (list[str]): Список моделей, поддерживающих генерацию изображений.

**Methods**:
  - `get_models()`: Возвращает список доступных моделей OpenAI.
  - `create_async_generator()`: Создает асинхронный генератор для отправки запросов к API OpenAI.
  - `get_headers()`: Возвращает заголовки для запросов к API OpenAI.

## Class Methods

### `get_models`

**Purpose**: Получение списка доступных моделей OpenAI.

**Parameters**:
  - `api_key` (str): Ключ API OpenAI.
  - `api_base` (str): Базовый URL API OpenAI.

**Returns**:
  - `list[str]`: Список доступных моделей OpenAI.

**How the Function Works**:
  - Метод `get_models` отправляет запрос к API OpenAI для получения списка доступных моделей.
  - Он проверяет, был ли задан ключ API и базовый URL API.
  - Если ключ API и базовый URL API не были заданы, он использует значения по умолчанию из `api_key` и `api_base`.
  - Он отправляет запрос GET к `/models` конечной точки API OpenAI с авторизацией Bearer.
  - Он обрабатывает ответ API и извлекает список моделей.
  - Он фильтрует модели, чтобы получить только модели, поддерживающие генерацию изображений.
  - Он сортирует модели в алфавитном порядке, если `sort_models` установлен в `True`.
  - Он возвращает список моделей.

**Examples**:
  - `OpenaiTemplate.get_models(api_key='your_api_key', api_base='https://api.openai.com')`

### `create_async_generator`

**Purpose**: Создание асинхронного генератора для отправки запросов к API OpenAI.

**Parameters**:
  - `model` (str): Имя модели OpenAI.
  - `messages` (Messages): Список сообщений для отправки в API.
  - `proxy` (str): Прокси-сервер для отправки запросов.
  - `timeout` (int): Время ожидания для отправки запросов.
  - `media` (MediaListType): Список медиа-файлов.
  - `api_key` (str): Ключ API OpenAI.
  - `api_endpoint` (str): Конечная точка API OpenAI.
  - `api_base` (str): Базовый URL API OpenAI.
  - `temperature` (float): Температура генерации.
  - `max_tokens` (int): Максимальное количество токенов в ответе.
  - `top_p` (float): Вероятность выборки для токенов.
  - `stop` (Union[str, list[str]]): Стоп-слова.
  - `stream` (bool): Нужно ли использовать потоковый режим.
  - `prompt` (str): Текстовый запрос.
  - `headers` (dict): Дополнительные заголовки для запросов.
  - `impersonate` (str): Имя пользователя для имитации.
  - `extra_parameters` (list[str]): Список дополнительных параметров.
  - `extra_data` (dict): Дополнительные данные для запроса.

**Returns**:
  - `AsyncResult`: Асинхронный генератор для отправки запросов к API OpenAI.

**How the Function Works**:
  - Метод `create_async_generator` создает асинхронный генератор, который отправляет запросы к API OpenAI.
  - Он проверяет, был ли задан ключ API.
  - Если ключ API не был задан, он вызывает исключение `MissingAuthError`.
  - Он создает экземпляр `StreamSession` с заданными параметрами.
  - Он выбирает модель OpenAI для запроса.
  - Он отправляет запрос POST к `api_endpoint` с заданными параметрами.
  - Он обрабатывает ответ API и возвращает данные в виде асинхронного генератора.

**Examples**:
  - `async def send_request(model: str, messages: Messages) -> AsyncResult:`
  - `result = await OpenaiTemplate.create_async_generator(model='text-davinci-003', messages=messages)`

### `get_headers`

**Purpose**: Возвращает заголовки для запросов к API OpenAI.

**Parameters**:
  - `stream` (bool): Нужно ли использовать потоковый режим.
  - `api_key` (str): Ключ API OpenAI.
  - `headers` (dict): Дополнительные заголовки для запросов.

**Returns**:
  - `dict`: Заголовки для запросов к API OpenAI.

**How the Function Works**:
  - Метод `get_headers` формирует заголовки для запросов к API OpenAI.
  - Он устанавливает заголовок `Accept` в `text/event-stream`, если `stream` установлен в `True`, или в `application/json` в противном случае.
  - Он устанавливает заголовок `Content-Type` в `application/json`.
  - Он добавляет заголовок `Authorization` с ключом API, если он был задан.
  - Он добавляет дополнительные заголовки, если они были заданы в параметре `headers`.
  - Он возвращает словарь с заголовками.

**Examples**:
  - `headers = OpenaiTemplate.get_headers(stream=True, api_key='your_api_key')`

## Parameter Details

- `api_key` (str): Ключ API OpenAI, необходимый для аутентификации в API.
- `api_base` (str): Базовый URL API OpenAI, используется для формирования запросов.
- `api_endpoint` (str): Конечная точка API OpenAI, используется для определения конкретного метода API.
- `model` (str): Имя модели OpenAI, например, "text-davinci-003" или "gpt-3.5-turbo".
- `messages` (Messages): Список сообщений для отправки в API, включает историю диалога.
- `proxy` (str): Прокси-сервер для отправки запросов, если требуется.
- `timeout` (int): Время ожидания для отправки запросов, по умолчанию 120 секунд.
- `media` (MediaListType): Список медиа-файлов для отправки в API.
- `temperature` (float): Температура генерации, значение от 0 до 1, 0 - самый консервативный, 1 - самый творческий.
- `max_tokens` (int): Максимальное количество токенов в ответе.
- `top_p` (float): Вероятность выборки для токенов, значение от 0 до 1, определяет насколько предсказуемым будет ответ.
- `stop` (Union[str, list[str]]): Стоп-слова, которые сигнализируют модели о завершении генерации ответа.
- `stream` (bool): Нужно ли использовать потоковый режим для получения ответа, по умолчанию `False`.
- `prompt` (str): Текстовый запрос для модели OpenAI.
- `headers` (dict): Дополнительные заголовки для запросов, например, `User-Agent` или `X-Forwarded-For`.
- `impersonate` (str): Имя пользователя для имитации, используется для персонализации запросов.
- `extra_parameters` (list[str]): Список дополнительных параметров для запроса.
- `extra_data` (dict): Дополнительные данные для запроса, могут быть использованы для передачи дополнительной информации модели.

## Examples

```python
# Инициализация класса
openai_template = OpenaiTemplate()

# Получение списка доступных моделей
models = openai_template.get_models()

# Отправка запроса с использованием асинхронного генератора
async def send_request(model: str, messages: Messages) -> AsyncResult:
    result = await openai_template.create_async_generator(model=model, messages=messages)
    async for data in result:
        print(data)

# Пример использования асинхронного генератора
async def main():
    messages = [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
    await send_request(model="gpt-3.5-turbo", messages=messages)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```