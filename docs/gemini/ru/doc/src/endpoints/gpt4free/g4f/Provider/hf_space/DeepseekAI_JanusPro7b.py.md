# Модуль `DeepseekAI_JanusPro7b`

## Обзор

Модуль `DeepseekAI_JanusPro7b` предназначен для взаимодействия с моделью DeepseekAI Janus-Pro-7B, размещенной на платформе Hugging Face Spaces. Он предоставляет асинхронный генератор для обработки текстовых и графических запросов к модели. Модуль поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Подробнее

Модуль реализует класс `DeepseekAI_JanusPro7b`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует асинхронные запросы для взаимодействия с API Hugging Face Spaces и предоставляет методы для создания и обработки запросов к модели Janus-Pro-7B.

## Классы

### `DeepseekAI_JanusPro7b`

**Описание**: Класс для взаимодействия с моделью DeepseekAI Janus-Pro-7B.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("DeepseekAI Janus-Pro-7B").
- `space` (str): Имя пространства на Hugging Face ("deepseek-ai/Janus-Pro-7B").
- `url` (str): URL пространства на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию ("janus-pro-7b").
- `default_image_model` (str): Модель для генерации изображений по умолчанию ("janus-pro-7b-image").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию (совпадает с `default_model`).
- `image_models` (list[str]): Список моделей для генерации изображений.
- `vision_models` (list[str]): Список моделей для обработки изображений.
- `models` (list[str]): Объединенный список моделей для текста и изображений.

**Методы**:
- `run(method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0)`
- `create_async_generator(model: str, messages: Messages, media: MediaListType = None, prompt: str = None, proxy: str = None, cookies: Cookies = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", return_conversation: bool = False, conversation: JsonConversation = None, seed: int = None, **kwargs)`

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
```

**Назначение**: Выполняет HTTP-запрос к API Hugging Face Spaces.

**Параметры**:
- `method` (str): HTTP-метод ("post" или "get").
- `session` (StreamSession): Асинхронная сессия для выполнения запросов.
- `prompt` (str): Текстовый запрос.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге.
- `image` (dict, optional): Информация об изображении. По умолчанию `None`.
- `seed` (int): Зерно для генерации случайных чисел.

**Возвращает**:
- `StreamResponse`: Объект ответа от API.

**Как работает функция**:
Функция `run` отправляет запросы к API Hugging Face Spaces в зависимости от указанного метода (`method`). Она поддерживает два основных метода: `post` для отправки текстовых запросов и `image` для отправки запросов на генерацию изображений. Функция также обрабатывает заголовки запросов, включая токен `zerogpu_token`, `zerogpu_uuid` и `session_hash`.

В зависимости от метода, функция выполняет следующие действия:
- Если `method` равен `"post"`, отправляется POST-запрос к `/gradio_api/queue/join` с данными, включающими изображение, запрос, зерно и параметры генерации.
- Если `method` равен `"image"`, отправляется POST-запрос к `/gradio_api/queue/join` с данными, включающими запрос, зерно и параметры генерации изображения.
- Если `method` не равен `"post"` и `"image"`, отправляется GET-запрос к `/gradio_api/queue/data` для получения данных о сессии.

**Примеры**:

Пример отправки POST-запроса:

```python
# Пример отправки POST-запроса
session = StreamSession()
conversation = JsonConversation(session_hash="test_session")
response = DeepseekAI_JanusPro7b.run("post", session, "Hello", conversation, seed=123)
```

Пример отправки GET-запроса:

```python
# Пример отправки GET-запроса
session = StreamSession()
conversation = JsonConversation(session_hash="test_session")
response = DeepseekAI_JanusPro7b.run("get", session, "Hello", conversation, seed=123)
```

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
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
```

**Назначение**: Создает асинхронный генератор для обработки запросов к модели.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для формирования запроса.
- `media` (MediaListType, optional): Список медиафайлов (изображений). По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для HTTP-запросов. По умолчанию `None`.
- `api_key` (str, optional): API-ключ. По умолчанию `None`.
- `zerogpu_uuid` (str, optional): UUID для zerogpu. По умолчанию `"[object Object]"`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект `JsonConversation`. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект, содержащий информацию о текущем диалоге. По умолчанию `None`.
- `seed` (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты от API.

**Как работает функция**:
Функция `create_async_generator` создает асинхронный генератор для взаимодействия с моделью DeepseekAI Janus-Pro-7B. Она определяет, какой метод (`post` или `image`) следует использовать в зависимости от указанной модели и наличия запроса. Функция формирует запрос на основе переданных сообщений и медиафайлов, а также устанавливает необходимые заголовки и параметры для запроса.

Основные шаги работы функции:
1. Определение метода запроса (`method`) в зависимости от модели и наличия запроса.
2. Формирование запроса (`prompt`) на основе сообщений.
3. Инициализация случайного зерна (`seed`), если оно не было передано.
4. Создание или использование существующей сессии (`session_hash`) и объекта `JsonConversation`.
5. Загрузка медиафайлов, если они предоставлены.
6. Отправка запроса к API с использованием метода `cls.run`.
7. Обработка потоковых ответов от API и извлечение полезной информации, такой как сообщения о ходе выполнения, сгенерированные изображения и текстовые ответы.
8. Возвращение результатов в виде асинхронного генератора.

**Внутренние функции**:
- `get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None)`: Асинхронная функция, предназначенная для получения токена `zerogpu_token` и `zerogpu_uuid`.

**Примеры**:

Пример создания асинхронного генератора для текстового запроса:

```python
# Пример создания асинхронного генератора для текстового запроса
messages = [{"role": "user", "content": "Hello"}]
async_generator = DeepseekAI_JanusPro7b.create_async_generator(model="janus-pro-7b", messages=messages)
```

Пример создания асинхронного генератора для запроса изображения:

```python
# Пример создания асинхронного генератора для запроса изображения
messages = [{"role": "user", "content": "Generate a cat image"}]
async_generator = DeepseekAI_JanusPro7b.create_async_generator(model="janus-pro-7b-image", messages=messages)
```

## Функции

### `get_zerogpu_token`

```python
async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
```

**Назначение**: Получает токен zerogpu и UUID сессии.

**Параметры**:
- `space` (str): Имя пространства на Hugging Face.
- `session` (StreamSession): Асинхронная сессия для выполнения запросов.
- `conversation` (JsonConversation): Объект, содержащий информацию о текущем диалоге.
- `cookies` (Cookies, optional): Cookies для HTTP-запросов. По умолчанию `None`.

**Возвращает**:
- `tuple[str | None, str]`: Кортеж, содержащий UUID и токен zerogpu.

**Как работает функция**:
Функция `get_zerogpu_token` получает токен `zerogpu_token` и UUID сессии, необходимые для аутентификации и авторизации при использовании API Hugging Face Spaces.

Основные шаги работы функции:
1. Получение UUID из объекта `conversation`, если он существует.
2. Получение cookies из домена `huggingface.co`, если они не были переданы.
3. Если UUID не был получен, функция выполняет GET-запрос к пространству Hugging Face для извлечения токена и UUID из HTML-кода страницы.
4. Функция выполняет GET-запрос к API Hugging Face для получения JWT (JSON Web Token), который используется в качестве токена zerogpu.
5. Функция возвращает UUID и токен zerogpu.

**Примеры**:

Пример вызова функции:

```python
# Пример вызова функции
session = StreamSession()
conversation = JsonConversation(session_hash="test_session")
uuid, token = await get_zerogpu_token("deepseek-ai/Janus-Pro-7B", session, conversation)