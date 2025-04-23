# Документация модуля `Free2GPT.py`

## Обзор

Модуль `Free2GPT.py` предоставляет асинхронный интерфейс для взаимодействия с сервисом `chat10.free2gpt.xyz`. Он позволяет генерировать текст на основе предоставленных сообщений, используя модели, такие как `gemini-1.5-pro` и `gemini-1.5-flash`. Модуль поддерживает прокси и имеет механизм для обработки ошибок, связанных с лимитами запросов.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения доступа к моделям генерации текста через API `chat10.free2gpt.xyz`. Он включает в себя функции для создания асинхронного генератора, отправки запросов и обработки ответов от сервера, а также для генерации подписи запроса. Модуль использует библиотеки `aiohttp` для асинхронных запросов и `hashlib` для генерации подписи.

## Классы

### `Free2GPT`

**Описание**: Класс `Free2GPT` предоставляет функциональность для взаимодействия с сервисом `chat10.free2gpt.xyz`. Он наследует `AsyncGeneratorProvider` и `ProviderModelMixin` и реализует методы для создания асинхронного генератора текста на основе предоставленных сообщений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса `chat10.free2gpt.xyz`.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (List[str]): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для генерации текста на основе предоставленных сообщений.

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        connector: BaseConnector = None,
        **kwargs,
    ) -> AsyncResult:
        """Создает асинхронный генератор для генерации текста на основе предоставленных сообщений.

        Args:
            model (str): Модель для генерации текста.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            connector (BaseConnector, optional): Асинхронный коннектор. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий чанки текста.

        Raises:
            RateLimitError: Если достигнут лимит запросов.
            Exception: В случае других ошибок при выполнении запроса.

        Как работает функция:
        - Функция сначала создает заголовки запроса, включая User-Agent, Accept и Content-Type.
        - Затем она создает объект ClientSession с использованием предоставленного коннектора и заголовков.
        - Далее, генерируется timestamp и подпись запроса с использованием функции generate_signature.
        - После этого формируется тело запроса в формате JSON, включающее сообщения, timestamp и подпись.
        - Отправляется POST-запрос к API сервиса.
        - Функция обрабатывает возможные ошибки, такие как превышение лимита запросов (RateLimitError).
        - В случае успешного запроса, она возвращает асинхронный генератор, который выдает чанки текста из ответа сервера.
        """
```

**Примеры**:

Пример использования функции `create_async_generator`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.Free2GPT import Free2GPT

async def main():
    model = 'gemini-1.5-pro'
    messages = [{"role": "user", "content": "Напиши короткий стих о весне."}]
    proxy = None

    generator = await Free2GPT.create_async_generator(model=model, messages=messages, proxy=proxy)
    
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `generate_signature`

```python
def generate_signature(time: int, text: str, secret: str = ""):
    """Генерирует подпись для запроса, используя алгоритм SHA256.

    Args:
        time (int): Timestamp запроса.
        text (str): Текст сообщения.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись запроса в виде шестнадцатеричной строки.

    Как работает функция:
    - Функция принимает timestamp, текст сообщения и секретный ключ (по умолчанию пустой).
    - Формирует строку сообщения, объединяя timestamp, текст и секретный ключ через двоеточие.
    - Вычисляет SHA256-хеш от строки сообщения, используя кодировку UTF-8.
    - Возвращает хеш в виде шестнадцатеричной строки.
    """
```

**Примеры**:

Пример использования функции `generate_signature`:

```python
from src.endpoints.gpt4free.g4f.Provider.Free2GPT import generate_signature

time = 1678886400
text = "Hello, world!"
signature = generate_signature(time, text)
print(signature)