# Документация для модуля `Microsoft_Phi_4`

## Описание

Модуль `Microsoft_Phi_4` предназначен для взаимодействия с мультимодальной моделью Microsoft Phi-4 через Hugging Face Spaces. Он обеспечивает асинхронную генерацию текста на основе предоставленных сообщений и медиафайлов.

## Подробности

Модуль поддерживает стриминг, системные сообщения и историю сообщений. Он использует API Hugging Face Spaces для отправки запросов и получения ответов от модели Microsoft Phi-4. Включает в себя функции для форматирования промптов, обработки медиафайлов и управления сессиями.

## Содержание

- [Классы](#classes)
    - [Microsoft_Phi_4](#microsoft_phi_4)
- [Функции](#functions)
    - [create_async_generator](#create_async_generator)
    - [run](#run)

## Классы

### `Microsoft_Phi_4`

**Описание**: Класс для взаимодействия с мультимодальной моделью Microsoft Phi-4.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Microsoft Phi-4").
- `space` (str): Имя пространства Hugging Face ("microsoft/phi-4-multimodal").
- `url` (str): URL пространства Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, что провайдер работает.
- `supports_stream` (bool): Поддержка стриминга.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `default_model` (str): Модель по умолчанию ("phi-4-multimodal").
- `default_vision_model` (str): Модель vision по умолчанию.
- `model_aliases` (dict): Алиасы моделей.
- `vision_models` (list): Список vision моделей.
- `models` (list): Список моделей.

**Методы**:
- [run](#run): Выполняет HTTP-запросы к API.
- [create_async_generator](#create_async_generator): Создает асинхронный генератор для получения ответов от модели.

## Функции

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
        messages (Messages): Список сообщений для отправки.
        media (MediaListType, optional): Список медиафайлов. По умолчанию `None`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для отправки. По умолчанию `None`.
        api_key (str, optional): API ключ. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID токена zerogpu. По умолчанию "[object Object]".
        return_conversation (bool, optional): Флаг возврата объекта Conversation. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект Conversation. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Как работает функция:
    - Функция форматирует запрос на основе предоставленных сообщений или использует предоставленный запрос.
    - Создает или использует существующий объект Conversation для управления состоянием сессии.
    - Если предоставлены медиафайлы, загружает их на сервер и подготавливает метаданные.
    - Выполняет HTTP-запросы к API для получения ответов от модели, используя методы `run`.
    - Возвращает асинхронный генератор, который выдает ответы модели по мере их поступления.

    Пример:
        >>> async for message in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", messages=[{"role": "user", "content": "Hello"}]):
        ...     print(message)
    """
```

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
    """Выполняет HTTP-запросы к API.

    Args:
        cls (Microsoft_Phi_4): Класс Microsoft_Phi_4.
        method (str): HTTP метод ("predict", "post", "get").
        session (StreamSession): Объект StreamSession для выполнения запросов.
        prompt (str): Текст запроса.
        conversation (JsonConversation): Объект Conversation с данными сессии.
        media (list, optional): Список медиафайлов. По умолчанию `None`.

    Returns:
        StreamResponse: Объект StreamResponse, представляющий ответ от сервера.

    Как работает функция:
    - Функция выполняет HTTP-запросы к API в зависимости от указанного метода.
    - Для метода "predict" отправляет POST запрос с текстом запроса и медиафайлами.
    - Для метода "post" отправляет POST запрос для присоединения к очереди.
    - Для метода "get" отправляет GET запрос для получения данных из очереди.
    - Возвращает объект StreamResponse для обработки ответа.

    Пример:
        >>> session = StreamSession()
        >>> conversation = JsonConversation(session_hash="test_session")
        >>> response = Microsoft_Phi_4.run("predict", session, "Hello", conversation)
    """