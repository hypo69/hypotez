# Модуль Acytoo

## Обзор

Модуль `Acytoo.py` предоставляет асинхронный генератор для взаимодействия с провайдером Acytoo, который является одним из поставщиков GPT-3.5 Turbo. Модуль предназначен для работы с чат-сервисом Acytoo через его API. Он поддерживает ведение истории сообщений.

## Подробней

Модуль содержит класс `Acytoo`, который наследуется от `AsyncGeneratorProvider` и реализует асинхронную генерацию ответов от Acytoo API. В модуле определены функции для создания заголовков и полезной нагрузки (payload) запроса к API.

## Классы

### `Acytoo`

**Описание**: Класс `Acytoo` представляет собой асинхронный провайдер генератора для взаимодействия с сервисом Acytoo.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора.

**Атрибуты**:
- `url` (str): URL-адрес сервиса Acytoo (`https://chat.acytoo.com`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (по умолчанию `True`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo (по умолчанию `True`).

**Методы**:
- `create_async_generator`: Асинхронный метод для создания генератора, который отправляет запросы к Acytoo API и возвращает ответы.

#### `create_async_generator`

**Описание**: Асинхронный метод для создания генератора, который взаимодействует с Acytoo API.

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
    Создает асинхронный генератор для взаимодействия с Acytoo API.

    Args:
        cls: Ссылка на класс.
        model (str): Модель для использования (в данном случае всегда 'gpt-3.5-turbo').
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        aiohttp.ClientResponseError: Если возникает HTTP ошибка при запросе к API.
    """
    ...
```

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если возникает HTTP ошибка при запросе к API.

**Как работает функция**:

1.  **Инициализация сессии**: Создается асинхронная сессия `aiohttp.ClientSession` с заголовками, полученными из функции `_create_header`.
2.  **Отправка запроса**: Отправляется POST-запрос к адресу `f'{cls.url}/api/completions'` с использованием указанного прокси (если он есть) и с данными в формате JSON, полученными из функции `_create_payload`.
3.  **Обработка ответа**: Для каждого чанка данных, полученного из ответа, выполняется декодирование и передача в генератор.
4.  **Обработка ошибок**: Если возникает HTTP ошибка, вызывается исключение `aiohttp.ClientResponseError`.

**ASCII Flowchart**:

```
Начало
   |
   v
Создание асинхронной сессии (ClientSession)
   |
   v
Отправка POST-запроса к Acytoo API
   |
   v
Получение ответа от API
   |
   v
Итерация по содержимому ответа (stream)
   |
   v
Декодирование содержимого (stream.decode())
   |
   v
Выдача декодированного содержимого через yield
   |
   v
Конец
```

**Примеры**:

Пример использования `create_async_generator`:

```python
async def main():
    messages = [{"role": "user", "content": "Hello"}]
    async for message in Acytoo.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Функции

### `_create_header`

```python
def _create_header():
    """
    Создает заголовки для HTTP-запроса.

    Args:
        None

    Returns:
        dict: Словарь с заголовками запроса.
    """
    ...
```

**Описание**: Создает заголовки для HTTP-запроса.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `dict`: Словарь с заголовками запроса, содержащий `accept` и `content-type`.

**Как работает функция**:

Функция создает и возвращает словарь с заголовками, необходимыми для выполнения HTTP-запроса к API. В частности, устанавливается `accept` в значение `'*/*'` и `content-type` в значение `'application/json'`.

**ASCII Flowchart**:

```
Начало
   |
   v
Создание словаря с заголовками
   |
   v
Установка accept в '*/*'
   |
   v
Установка content-type в 'application/json'
   |
   v
Возврат словаря с заголовками
   |
   v
Конец
```

**Примеры**:

```python
headers = _create_header()
print(headers)
# {'accept': '*/*', 'content-type': 'application/json'}
```

### `_create_payload`

```python
def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs):
    """
    Создает полезную нагрузку (payload) для HTTP-запроса.

    Args:
        messages (Messages): Список сообщений для отправки.
        temperature (float, optional): Температура для генерации текста. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        dict: Словарь с полезной нагрузкой для запроса.
    """
    ...
```

**Описание**: Создает полезную нагрузку (payload) для HTTP-запроса к API.

**Параметры**:
- `messages` (Messages): Список сообщений для отправки.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 0.5.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `dict`: Словарь с полезной нагрузкой для запроса.

**Как работает функция**:

Функция создает словарь, представляющий собой полезную нагрузку для запроса к API. Включает в себя ключ API (`key`), модель (`model`), список сообщений (`messages`), температуру (`temperature`) и пароль (`password`).

**ASCII Flowchart**:

```
Начало
   |
   v
Создание словаря payload
   |
   v
Установка key в ''
   |
   v
Установка model в 'gpt-3.5-turbo'
   |
   v
Установка messages из аргумента
   |
   v
Установка temperature из аргумента
   |
   v
Установка password в ''
   |
   v
Возврат словаря payload
   |
   v
Конец
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello"}]
payload = _create_payload(messages=messages, temperature=0.7)
print(payload)
# {'key': '', 'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello'}], 'temperature': 0.7, 'password': ''}