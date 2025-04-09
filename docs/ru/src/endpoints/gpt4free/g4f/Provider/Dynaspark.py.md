# Модуль Dynaspark.py

## Обзор

Модуль `Dynaspark.py` предназначен для асинхронного взаимодействия с API Dynaspark, предоставляющего доступ к различным моделям генерации текста, включая Gemini. Он позволяет отправлять текстовые запросы и, при необходимости, изображения для обработки. Модуль поддерживает потоковую передачу данных и работает без необходимости использования веб-драйвера.

## Подробнее

Модуль содержит класс `Dynaspark`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он отвечает за формирование запросов к API Dynaspark и обработку ответов. Класс использует библиотеку `aiohttp` для асинхронных HTTP-запросов и `FormData` для отправки данных, включая изображения.

## Классы

### `Dynaspark`

**Описание**: Класс для взаимодействия с API Dynaspark.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса Dynaspark.
- `login_url` (Optional[str]): URL для логина (в данном случае `None`, так как аутентификация не требуется).
- `api_endpoint` (str): URL API endpoint для генерации ответа.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий на использование без веб-драйвера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-flash`).
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию.
- `vision_models` (List[str]): Список моделей, поддерживающих обработку изображений.
- `models` (List[str]): Список всех поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с псевдонимами моделей.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    media: MediaListType = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Dynaspark.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        media (MediaListType, optional): Список медиафайлов (изображений) для отправки. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API Dynaspark.

    Raises:
        Exception: В случае ошибки при отправке запроса или обработке ответа.
    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API Dynaspark.

**Параметры**:
- `cls` (Type[Dynaspark]): Ссылка на класс `Dynaspark`.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `media` (MediaListType, optional): Список медиафайлов (изображений) для отправки. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API Dynaspark.

**Как работает функция**:

1.  **Подготовка заголовков**: Функция создает заголовки HTTP-запроса, включая `user-agent`, `referer` и другие необходимые параметры.
2.  **Создание сессии `aiohttp`**: Функция создает асинхронную сессию `aiohttp` с заданными заголовками для выполнения HTTP-запросов.
3.  **Формирование данных формы**: Функция формирует объект `FormData`, добавляя в него текстовые сообщения и, если есть, медиафайлы.
4.  **Отправка запроса**: Функция отправляет POST-запрос к API Dynaspark с использованием сессии `aiohttp` и сформированных данных формы.
5.  **Обработка ответа**: Функция обрабатывает ответ от API, извлекает текстовое содержимое и преобразует его в JSON-формат.
6.  **Генерация результата**: Функция генерирует результат, извлекая текстовый ответ из JSON и возвращая его как часть асинхронного генератора.

**ASCII Flowchart**:

```
    Начало
      ↓
    [Подготовка заголовков]
      ↓
    [Создание сессии aiohttp]
      ↓
    [Формирование данных формы (текст, медиа)]
      ↓
    [Отправка POST-запроса к API Dynaspark]
      ↓
    [Обработка ответа (JSON)]
      ↓
    [Генерация результата (текстовый ответ)]
      ↓
    Конец
```

**Примеры**:

Пример 1: Отправка текстового запроса без прокси и медиафайлов.

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for response in Dynaspark.create_async_generator(model="gemini-1.5-flash", messages=messages):
    print(response)
```

Пример 2: Отправка текстового запроса с прокси.

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for response in Dynaspark.create_async_generator(model="gemini-1.5-flash", messages=messages, proxy="http://proxy.example.com:8080"):
    print(response)
```

Пример 3: Отправка текстового запроса с медиафайлом (изображением).

```python
from io import BytesIO
from PIL import Image

# Создаем пример изображения
image = Image.new('RGB', (60, 30), color='red')
image_bytes = BytesIO()
image.save(image_bytes, format='PNG')
image_bytes = image_bytes.getvalue()

media = [("image.png", image_bytes)]
messages = [{"role": "user", "content": "Describe this image."}]

async for response in Dynaspark.create_async_generator(model="gemini-1.5-flash", messages=messages, media=media):
    print(response)