# Модуль `Microsoft_Phi_4`

## Обзор

Модуль `Microsoft_Phi_4` предоставляет асинхронный генератор для взаимодействия с моделью Microsoft Phi-4, размещенной на платформе Hugging Face Spaces. Он поддерживает отправку текстовых и медиа-сообщений, а также потоковую передачу ответов.

## Подробнее

Модуль предназначен для работы с мультимодальной моделью `phi-4-multimodal` от Microsoft, обеспечивая возможность отправки текстовых запросов вместе с изображениями. Он использует API Hugging Face Spaces для взаимодействия с моделью, поддерживая как стандартные текстовые запросы, так и запросы с изображениями.
Ключевым аспектом работы модуля является использование токенов `zerogpu`, необходимых для аутентификации и авторизации запросов к API.

## Классы

### `Microsoft_Phi_4`

**Описание**: Класс `Microsoft_Phi_4` предоставляет методы для взаимодействия с моделью Microsoft Phi-4.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера.
- `space` (str): Имя пространства Hugging Face, где размещена модель.
- `url` (str): URL пространства Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель по умолчанию.
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `vision_models` (list): Список моделей для работы с изображениями.
- `models` (list): Список поддерживаемых моделей.

**Методы**:
- `run()`: Выполняет HTTP-запрос к API модели.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели.

## Методы класса

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
    """Выполняет HTTP-запрос к API модели.

    Args:
        cls (Microsoft_Phi_4): Класс Microsoft_Phi_4.
        method (str): HTTP-метод (`predict`, `post` или `get`).
        session (StreamSession): Асинхровая HTTP-сессия.
        prompt (str): Текст запроса.
        conversation (JsonConversation): Объект разговора, содержащий метаданные сессии.
        media (list, optional): Список медиафайлов для отправки. По умолчанию `None`.

    Returns:
        Awaitable: Объект, представляющий асинхронный HTTP-запрос.
    """
    ...
```

**Как работает функция**:

Функция `run` выполняет HTTP-запросы к API модели в зависимости от указанного метода (`predict`, `post` или `get`). Она формирует заголовки запроса, включая токены `zerogpu` и UUID, а также данные запроса в формате JSON. В зависимости от метода, запрос отправляется на разные конечные точки API.

- Если `method` равен `"predict"`, функция отправляет POST-запрос на `/gradio_api/run/predict` с текстом запроса и медиафайлами.
- Если `method` равен `"post"`, функция отправляет POST-запрос на `/gradio_api/queue/join` с текстом запроса и медиафайлами, структурированными как сообщения пользователя.
- Если `method` равен `"get"`, функция отправляет GET-запрос на `/gradio_api/queue/data` для получения потоковых данных ответа.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    media: MediaListType = None,
    prompt: str = None,
    proxy: str = None,
    cookies: Cookies = None,
    api_key: str = None,
    zerogpu_uuid: str = "[object Object]",
    return_conversation: bool = False,
    conversation: JsonConversation = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от модели.

    Args:
        cls (Microsoft_Phi_4): Класс Microsoft_Phi_4.
        model (str): Имя модели.
        messages (Messages): Список сообщений для формирования запроса.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для HTTP-запросов. По умолчанию `None`.
        api_key (str, optional): API-ключ для доступа к модели. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
        return_conversation (bool, optional): Возвращать ли объект разговора. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект разговора. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Yields:
        str | JsonConversation: Части ответа модели или объект разговора (если `return_conversation` равен `True`).

    Raises:
        ResponseError: Если в ответе от API содержится сообщение об ошибке.
    """
    ...
```

**Как работает функция**:

Функция `create_async_generator` создает и возвращает асинхронный генератор, который используется для получения ответов от модели Microsoft Phi-4.

1. **Подготовка запроса**:
   - Форматирует промпт на основе переданных сообщений (`messages`) или использует предоставленный промпт напрямую.
   - Генерирует уникальный `session_hash` для идентификации сессии, если он не был передан в объекте `conversation`.
   
2. **Создание HTTP-сессии**:
   - Создает асинхронную HTTP-сессию (`StreamSession`) с использованием указанного прокси-сервера и имитацией браузера Chrome.

3. **Получение токена zerogpu**:
   - Если `api_key` не предоставлен, пытается получить токен `zerogpu` и UUID, используя функцию `get_zerogpu_token`.
   - Обновляет или создает объект `JsonConversation` с полученными токенами и UUID.
   - Если `return_conversation` установлен в `True`, возвращает объект `conversation` как первый элемент генератора.
   
4. **Обработка медиафайлов**:
   - Если предоставлены медиафайлы (`media`):
     - Формирует `FormData` объект для отправки файлов.
     - Определяет MIME-типы для каждого файла.
     - Загружает файлы на сервер с использованием POST-запроса на `/gradio_api/upload`.
     - Получает список загруженных файлов и формирует структуру данных `media` с информацией о файлах.

5. **Взаимодействие с API модели**:
   - Вызывает метод `run` с параметром `"predict"` для отправки начального запроса.
   - Вызывает метод `run` с параметром `"post"` для отправки данных.
   - Вызывает метод `run` с параметром `"get"` для получения потоковых данных ответа.

6. **Обработка потоковых данных**:
   - Читает ответ построчно и ищет строки, начинающиеся с `b'data: '`.
   - Извлекает JSON-данные из этих строк и пытается их распарсить.
   - Если JSON содержит сообщение об ошибке (`'msg' == 'process_completed'` и `'error' in json_data['output']`), выбрасывает исключение `ResponseError`.
   - Если JSON содержит данные ответа (`'msg' == 'process_completed'` и `'data' in json_data['output']`), извлекает контент и возвращает его как элемент генератора.

**Пример**:

```python
async for part in Microsoft_Phi_4.create_async_generator(
    model="phi-4-multimodal",
    messages=[{"role": "user", "content": "Нарисуй кошку"}],
    api_key="your_api_key"
):
    print(part)