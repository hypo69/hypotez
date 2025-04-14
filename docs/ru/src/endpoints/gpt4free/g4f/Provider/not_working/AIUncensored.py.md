# Модуль AIUncensored
## Обзор

Модуль `AIUncensored` предоставляет асинхронный интерфейс для взаимодействия с моделью AIUncensored.info. Он позволяет генерировать текст на основе предоставленных сообщений, поддерживает потоковую передачу данных и работу с историей сообщений.

## Подробней

Этот модуль предназначен для интеграции с сервисом AIUncensored, который предоставляет доступ к различным моделям генерации текста. Модуль использует асинхронные запросы (`aiohttp`) для взаимодействия с сервером, обеспечивая неблокирующий ввод-вывод.

Модуль определяет следующие основные компоненты:

- URL: `https://www.aiuncensored.info/ai_uncensored` - основной URL для доступа к сервису.
- API Key: `62852b00cb9e44bca86f0ec7e7455dc6` - ключ API для аутентификации.
- Поддержка потоковой передачи: `supports_stream = True`.
- Поддержка системных сообщений: `supports_system_message = True`.
- Поддержка истории сообщений: `supports_message_history = True`.

Модуль включает методы для:

- Вычисления подписи запроса (`calculate_signature`).
- Получения URL сервера (`get_server_url`).
- Создания асинхронного генератора для обработки ответов от сервера (`create_async_generator`).

## Классы

### `AIUncensored`

**Описание**:
Класс `AIUncensored` является асинхронным провайдером и предоставляет методы для взаимодействия с AIUncensored API. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных провайдеров, работающих с генераторами.
- `ProviderModelMixin`: Предоставляет вспомогательные методы для работы с моделями, такие как получение модели по умолчанию или alias.

**Атрибуты**:
- `url` (str): URL для доступа к AIUncensored API.
- `api_key` (str): Ключ API для аутентификации.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `calculate_signature(timestamp: str, json_dict: dict) -> str`: Вычисляет подпись для запроса к API.
- `get_server_url() -> str`: Возвращает случайный URL сервера из списка доступных серверов.
- `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.

## Функции

### `calculate_signature`

```python
@staticmethod
def calculate_signature(timestamp: str, json_dict: dict) -> str:
    """
    Вычисляет подпись для запроса к API на основе временной метки и данных запроса.

    Args:
        timestamp (str): Временная метка запроса.
        json_dict (dict): Словарь с данными запроса.

    Returns:
        str: Подпись запроса в виде шестнадцатеричной строки.
    """
    ...
```

**Назначение**:
Функция `calculate_signature` генерирует HMAC-подпись для обеспечения безопасности запросов к API AIUncensored. Подпись вычисляется на основе временной метки и JSON-представления данных запроса с использованием секретного ключа.

**Параметры**:
- `timestamp` (str): Временная метка (timestamp) запроса в виде строки. Используется для предотвращения повторных атак.
- `json_dict` (dict): Словарь, содержащий параметры запроса, такие как сообщения, модель и настройки потоковой передачи.

**Возвращает**:
- `str`: HMAC-подпись запроса в виде шестнадцатеричной строки.

**Как работает функция**:
1. Формируется сообщение путем объединения временной метки и JSON-представления данных запроса.
2. Секретный ключ `your-super-secret-key-replace-in-production` используется для создания HMAC-подписи. *Важно*: В production-среде этот ключ должен быть заменен на надежный секретный ключ.
3. Вычисляется SHA256-хеш сообщения с использованием секретного ключа.
4. Возвращается шестнадцатеричное представление вычисленной подписи.

```ascii
Timestamp + JSON Data --> Message
|
Secret Key
|
HMAC-SHA256 Hash
|
Hexadecimal Representation --> Signature
```

**Примеры**:
```python
timestamp = "1678886400"
json_data = {"messages": [{"role": "user", "content": "Hello"}], "model": "hermes3-70b", "stream": False}
signature = AIUncensored.calculate_signature(timestamp, json_data)
print(signature)
```

### `get_server_url`

```python
@staticmethod
def get_server_url() -> str:
    """
    Возвращает случайный URL сервера из списка доступных серверов.

    Returns:
        str: URL сервера.
    """
    ...
```

**Назначение**:
Функция `get_server_url` выбирает случайный URL из списка доступных серверов AIUncensored. Это позволяет распределить нагрузку между серверами и повысить отказоустойчивость.

**Возвращает**:
- `str`: Случайно выбранный URL сервера.

**Как работает функция**:
1. Определяется список серверов: `"https://llm-server-nov24-ibak.onrender.com"`,`"https://llm-server-nov24-qv2w.onrender.com"`, `"https://llm-server-nov24.onrender.com"`.
2. Используется `random.choice` для случайного выбора одного из URL.
3. Возвращается выбранный URL.

```ascii
List of Servers --> Random Choice --> Server URL
```

**Примеры**:
```python
server_url = AIUncensored.get_server_url()
print(server_url)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    proxy: str = None,
    api_key: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Включить потоковую передачу данных.
        proxy (str): Прокси для использования.
        api_key (str): Ключ API.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.
    """
    ...
```

**Назначение**:
Функция `create_async_generator` создает асинхронный генератор, который отправляет запросы к API AIUncensored и возвращает ответы в виде потока данных (если `stream=True`) или полного ответа (если `stream=False`).

**Параметры**:
- `model` (str): Идентификатор используемой модели.
- `messages` (Messages): Список сообщений, отправляемых в запросе.
- `stream` (bool, optional): Флаг, указывающий, использовать ли потоковый режим. По умолчанию `False`.
- `proxy` (str, optional): URL прокси-сервера для использования при отправке запроса. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. Если не указан, используется значение по умолчанию из атрибута класса.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в запрос.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, предоставляющий ответы от API.

**Как работает функция**:
1. Определяется модель на основе входного параметра `model` и псевдонимов моделей.
2. Генерируется временная метка (timestamp) для запроса.
3. Формируется словарь `json_dict` с данными запроса, включающий сообщения, модель и флаг потоковой передачи.
4. Вычисляется подпись запроса с использованием временной метки и данных запроса.
5. Формируются заголовки запроса, включающие API-ключ, временную метку и подпись.
6. Отправляется асинхронный POST-запрос к API с использованием `aiohttp.ClientSession`.
7. Если включен потоковый режим (`stream=True`):
   - Ответ обрабатывается построчно.
   - Каждая строка декодируется и проверяется на наличие маркера `[DONE]`, указывающего на завершение потока.
   - Извлекаются данные из JSON-объектов и передаются в генератор.
8. Если потоковый режим выключен (`stream=False`):
   - Полученный JSON-ответ возвращается как результат работы генератора.
9. В случае возникновения ошибок при декодировании или обработке JSON, ошибки логируются с использованием `logger.error`.

```ascii
Model + Messages + Stream --> JSON Payload
|
Timestamp --> Signature
|
Headers (API Key, Timestamp, Signature)
|
Async POST Request --> Response
|
Stream Mode: Line-by-Line Processing, JSON Parsing, Data Extraction
|
Non-Stream Mode: JSON Response Extraction
|
Yield Data or FinishReason
```

**Примеры**:
```python
async def main():
    messages = [{"role": "user", "content": "Напиши стихотворение о весне."}]
    async for chunk in AIUncensored.create_async_generator(model="hermes3-70b", messages=messages, stream=True):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())