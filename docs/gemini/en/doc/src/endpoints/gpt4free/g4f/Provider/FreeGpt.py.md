# Module src.endpoints.gpt4free.g4f.Provider.FreeGpt

## Обзор

Модуль `FreeGpt` предоставляет асинхронный генератор для взаимодействия с API FreeGpt. Он поддерживает историю сообщений, системные сообщения и предоставляет функциональность для обхода ограничений скорости.

## More details

Этот модуль предназначен для использования с API FreeGpt для генерации текста на основе предоставленных сообщений. Он включает в себя механизмы для обработки ограничений скорости и построения правильных запросов к API. Модуль использует асинхронные запросы для обеспечения неблокирующего взаимодействия.

## Classes

### `FreeGpt`

**Описание**: Класс `FreeGpt` реализует асинхронный генератор для взаимодействия с API FreeGpt.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `url` (str): URL для API FreeGpt.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (list[str]): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Working principle**:
Класс `FreeGpt` использует асинхронные запросы для взаимодействия с API FreeGpt. Он строит запросы на основе предоставленных сообщений и временной метки, подписывая их для обеспечения безопасности. Класс также обрабатывает ответы от API, проверяя наличие ошибок, связанных с ограничением скорости, и генерирует текст по частям.

**Methods**:
- `create_async_generator`: Создает асинхронный генератор для получения текста от API FreeGpt.
- `_build_request_data`: Строит данные запроса для API FreeGpt.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: Optional[str] = None,
    timeout: int = 120,
    **kwargs: Any
) -> AsyncGenerator[str, None]:
    """Создает асинхронный генератор для получения текста от API FreeGpt.

    Args:
        cls (FreeGpt): Ссылка на класс.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса. По умолчанию 120.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        AsyncGenerator[str, None]: Асинхронный генератор текста.

    Raises:
        RateLimitError: Если достигнуто ограничение скорости.

    How the function works:
        Функция `create_async_generator` создает асинхронный генератор для получения текста от API FreeGpt.
        1. Извлекает последний элемент из списка сообщений и присваивает его переменной `prompt`.
        2. Генерируется временная метка.
        3. Строятся данные запроса с помощью метода `_build_request_data`.
        4. Выбирается случайный домен из списка `DOMAINS`.
        5. Отправляется асинхронный POST-запрос к API с использованием `StreamSession`.
        6. Обрабатываются чанки ответа, проверяется наличие сообщения об ограничении скорости, и генерируется текст.

    """
    ...
```

#### Class Parameters
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса. По умолчанию 120.
- `**kwargs` (Any): Дополнительные аргументы.
    
#### Examples
Пример вызова функции `create_async_generator`:

```python
async def main():
    messages = [{"role": "user", "content": "Hello, FreeGpt!"}]
    generator = FreeGpt.create_async_generator(model="gemini-1.5-pro", messages=messages)
    async for chunk in generator:
        print(chunk, end="")
```

### `_build_request_data`

```python
    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
        """Строит данные запроса для API FreeGpt.

        Args:
            messages (Messages): Список сообщений для отправки.
            prompt (str): Последнее сообщение пользователя.
            timestamp (int): Временная метка запроса.
            secret (str, optional): Секретный ключ для подписи запроса. По умолчанию "".

        Returns:
            Dict[str, Any]: Словарь с данными запроса.

        How the function works:
            Функция `_build_request_data` строит словарь с данными запроса, который включает сообщения, временную метку,
            отсутствующий параметр `pass` и подпись, сгенерированную функцией `generate_signature`.

        """
        return {
            "messages": messages,
            "time": timestamp,
            "pass": None,
            "sign": generate_signature(timestamp, prompt, secret)
        }
```

#### Class Parameters

- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str): Последнее сообщение пользователя.
- `timestamp` (int): Временная метка запроса.
- `secret` (str, optional): Секретный ключ для подписи запроса. По умолчанию "".

#### Examples

Пример вызова функции `_build_request_data`:

```python
messages = [{"role": "user", "content": "Hello, FreeGpt!"}]
timestamp = int(time.time())
data = FreeGpt._build_request_data(messages=messages, prompt="Hello, FreeGpt!", timestamp=timestamp)
print(data)
```

## Functions

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "") -> str:
    """Генерирует подпись для запроса к API FreeGpt.

    Args:
        timestamp (int): Временная метка запроса.
        message (str): Сообщение для подписи.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись запроса в виде шестнадцатеричной строки.

    How the function works:
        Функция `generate_signature` генерирует подпись для запроса к API FreeGpt.
        1. Формируется строка данных, включающая временную метку, сообщение и секретный ключ.
        2. Вычисляется SHA256-хеш от строки данных.
        3. Возвращается шестнадцатеричное представление хеша.

    """
    data = f"{timestamp}:{message}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()
```

#### Parameters

- `timestamp` (int): Временная метка запроса.
- `message` (str): Сообщение для подписи.
- `secret` (str, optional): Секретный ключ. По умолчанию "".

#### Examples
Пример вызова функции `generate_signature`:

```python
timestamp = int(time.time())
signature = generate_signature(timestamp=timestamp, message="Hello, FreeGpt!", secret="secret")
print(signature)
```