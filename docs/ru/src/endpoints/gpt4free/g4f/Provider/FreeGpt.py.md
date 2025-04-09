# Модуль `FreeGpt.py`

## Обзор

Модуль `FreeGpt.py` предоставляет асинхронтный генератор для взаимодействия с сервисом FreeGpt, используя API для генерации текста на основе предоставленных сообщений. Он поддерживает как историю сообщений, так и системные сообщения, а также предоставляет возможность выбора модели.

## Подробней

Этот модуль предназначен для интеграции с API FreeGpt, обеспечивая функциональность для генерации текста на основе заданных сообщений. Модуль включает в себя асинхронный генератор, который позволяет обрабатывать ответы от API FreeGpt частями, что полезно для больших объемов данных. Он также включает в себя функции для формирования запросов и обработки ответов от API.

## Классы

### `FreeGpt`

**Описание**: Класс `FreeGpt` предоставляет асинхронный генератор для взаимодействия с сервисом FreeGpt.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`:  Миксин, добавляющий поддержку выбора модели.

**Атрибуты**:
- `url` (str): URL для доступа к API FreeGpt.
- `working` (bool):  Указывает, работает ли провайдер.
- `supports_message_history` (bool):  Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `default_model` (str):  Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

#### `create_async_generator`

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
        """
        Создает асинхронный генератор для получения ответов от API FreeGpt.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            AsyncGenerator[str, None]: Асинхронный генератор, возвращающий части ответа.

        Raises:
            RateLimitError: Если достигнут лимит запросов.

        """
```

**Как работает функция**:

1. **Подготовка данных**:
   - Извлекает последнее сообщение из списка `messages` и присваивает его переменной `prompt`.
   - Получает текущее время в формате timestamp и сохраняет его в переменной `timestamp`.
   - Вызывает метод `_build_request_data` для создания тела запроса, передавая `messages`, `prompt` и `timestamp`.

2. **Выбор домена**:
   - Случайным образом выбирает один из доступных доменов из списка `DOMAINS`.

3. **Отправка запроса и обработка ответа**:
   - Использует `StreamSession` для отправки асинхронного POST-запроса к выбранному домену с телом запроса `data`.
   - Проверяет статус ответа с помощью `raise_for_status`, чтобы убедиться, что запрос выполнен успешно.
   - Итерируется по содержимому ответа, получая данные небольшими частями (chunks).
   - Декодирует каждую часть, игнорируя ошибки кодирования, и присваивает результат переменной `chunk_decoded`.
   - Проверяет, не является ли декодированная часть сообщения об ошибке, связанной с ограничением скорости (`RATE_LIMIT_ERROR_MESSAGE`). Если это так, вызывает исключение `RateLimitError`.
   - Передает декодированную часть как результат генератора с помощью `yield chunk_decoded`.

```ascii
    Начало
      ↓
    Извлечение prompt и timestamp
      ↓
    data = _build_request_data(messages, prompt, timestamp)
      ↓
    Выбор domain из DOMAINS
      ↓
    POST запрос к {domain}/api/generate с data
      ↓
    Обработка ответа (по частям)
      ├── chunk_decoded == RATE_LIMIT_ERROR_MESSAGE?
      │   └── Да: raise RateLimitError
      └── Нет: yield chunk_decoded
      ↓
    Конец
```

#### `_build_request_data`

```python
    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
        """
        Создает словарь с данными для запроса к API FreeGpt.

        Args:
            messages (Messages): Список сообщений для отправки.
            prompt (str): Последнее сообщение пользователя.
            timestamp (int):  Временная метка запроса.
            secret (str, optional): Секретный ключ для подписи запроса. По умолчанию "".

        Returns:
            Dict[str, Any]: Словарь с данными для запроса.

        """
```

**Как работает функция**:
Функция `_build_request_data` создает словарь с данными, необходимыми для отправки запроса к API FreeGpt. Она принимает список сообщений, последнее сообщение пользователя, временную метку и секретный ключ в качестве аргументов.

1. **Формирование данных запроса**:
   - Создает словарь, содержащий следующие ключи:
     - `"messages"`: Список сообщений для отправки.
     - `"time"`: Временная метка запроса.
     - `"pass"`: Устанавливается в `None`.
     - `"sign"`: Подпись запроса, сгенерированная с помощью функции `generate_signature`.

```ascii
    Начало
      ↓
    Формирование словаря data
      │
      ├── "messages": messages
      ├── "time": timestamp
      ├── "pass": None
      └── "sign": generate_signature(timestamp, prompt, secret)
      ↓
    Конец (возвращает словарь data)
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello"}]
prompt = "Hello"
timestamp = int(time.time())
data = FreeGpt._build_request_data(messages, prompt, timestamp)
print(data)
# {'messages': [{'role': 'user', 'content': 'Hello'}], 'time': ..., 'pass': None, 'sign': ...}
```

## Функции

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "") -> str:\n    """\n    Генерирует подпись для запроса к API FreeGpt.\n\n    Args:\n        timestamp (int): Временная метка запроса.\n        message (str): Сообщение для подписи.\n        secret (str, optional): Секретный ключ для подписи. По умолчанию "".\n\n    Returns:\n        str:  Подпись запроса.\n\n    """
```

**Как работает функция**:

1. **Формирование строки данных**:
   - Создает строку, объединяя `timestamp`, `message` и `secret` через двоеточие.

2. **Генерация SHA256 хеша**:
   - Кодирует строку данных в байты.
   - Вычисляет SHA256 хеш от закодированной строки.
   - Преобразует хеш в шестнадцатеричное представление.

```ascii
    Начало
      ↓
    data = f"{timestamp}:{message}:{secret}"
      ↓
    SHA256(data.encode()).hexdigest()
      ↓
    Конец
```

**Примеры**:

```python
timestamp = int(time.time())
message = "Hello"
signature = generate_signature(timestamp, message)
print(signature)
#  Пример вывода: '...'
```