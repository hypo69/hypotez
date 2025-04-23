# Модуль Websim

## Обзор

Модуль `Websim` предоставляет асинхронный интерфейс для взаимодействия с сервисом Websim AI, включая функциональность для генерации текста и изображений. Он поддерживает использование прокси, настройку заголовков запросов и обработку ошибок, таких как превышение лимита запросов.

## Подробнее

Модуль содержит класс `Websim`, который наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`. Это позволяет ему асинхронно генерировать ответы на запросы, а также предоставляет возможности для работы с различными моделями, поддерживаемыми Websim AI. Класс поддерживает как текстовые запросы к чат-моделям, так и запросы на генерацию изображений.

## Классы

### `Websim`

**Описание**: Класс для взаимодействия с Websim AI для генерации текста и изображений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с различными моделями.

**Атрибуты**:
- `url` (str): Базовый URL сервиса Websim AI (`https://websim.ai`).
- `login_url` (Optional[str]): URL для логина (в данном случае `None`, так как аутентификация не требуется).
- `chat_api_endpoint` (str): URL для отправки запросов на генерацию текста (`https://websim.ai/api/v1/inference/run_chat_completion`).
- `image_api_endpoint` (str): URL для отправки запросов на генерацию изображений (`https://websim.ai/api/v1/inference/run_image_generation`).
- `working` (bool): Указывает, что провайдер работает (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
- `use_nodriver` (bool): Указывает, нужно ли использовать драйвер (False).
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (False).
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию для генерации текста (`gemini-1.5-pro`).
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (`flux`).
- `image_models` (List[str]): Список поддерживаемых моделей для генерации изображений (`[default_image_model]`).
- `models` (List[str]): Список всех поддерживаемых моделей (текстовых и графических).

**Методы**:
- `generate_project_id(for_image: bool = False) -> str`: Генерирует ID проекта в зависимости от типа запроса (текст или изображение).
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для обработки запросов к Websim AI.
- `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запросы на генерацию изображений.
- `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запросы на генерацию текста.

## Методы класса

### `generate_project_id`

```python
@staticmethod
def generate_project_id(for_image=False):
    """
    Generate a project ID in the appropriate format
    
    For chat: format like \'ke3_xh5gai3gjkmruomu\'
    For image: format like \'kx0m131_rzz66qb2xoy7\'
    """
```

**Назначение**: Генерирует идентификатор проекта в формате, требуемом Websim AI, в зависимости от того, предназначен ли он для запроса изображения или чата.

**Параметры**:
- `for_image` (bool): Если `True`, генерируется идентификатор проекта для запроса изображения, иначе - для чата.

**Возвращает**:
- `str`: Сгенерированный идентификатор проекта.

**Как работает функция**:
- Функция `generate_project_id` генерирует строку, которая служит идентификатором проекта для Websim AI. Формат идентификатора зависит от того, предназначен ли он для запроса изображения или для чата.
- Если `for_image` равно `True`, то генерируется идентификатор для запроса изображения, который состоит из двух частей, разделенных символом "_". Первая часть содержит 7 случайных символов, вторая - 12.
- Если `for_image` равно `False` (по умолчанию), то генерируется идентификатор для запроса чата, который состоит из префикса из 3 случайных символов и суффикса из 15 случайных символов, разделенных символом "_".
- Функция использует модуль `random` и строку `string.ascii_lowercase + string.digits` для генерации случайных символов.

**Примеры**:
```python
project_id_chat = Websim.generate_project_id(for_image=False)
print(f"ID проекта для чата: {project_id_chat}")

project_id_image = Websim.generate_project_id(for_image=True)
print(f"ID проекта для изображения: {project_id_image}")
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    aspect_ratio: str = "1:1",
    project_id: str = None,
    **kwargs
) -> AsyncResult:
    """ """
```

**Назначение**: Создает асинхронный генератор для обработки запросов к Websim AI.

**Параметры**:
- `model` (str): Модель для использования (например, 'gemini-1.5-pro' или 'flux').
- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str, optional): Дополнительный промпт для запроса. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон для запроса изображения. По умолчанию `"1:1"`.
- `project_id` (str, optional): ID проекта для использования. Если не указан, будет сгенерирован автоматически. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в запросы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса.

**Как работает функция**:
- Функция `create_async_generator` является асинхронным методом класса `Websim`, который создает генератор для выполнения запросов к API Websim AI.
- Сначала функция определяет, является ли запрос запросом изображения, проверяя, входит ли указанная модель (`model`) в список моделей изображений (`cls.image_models`).
- Если `project_id` не указан, он генерируется с использованием метода `cls.generate_project_id` в зависимости от типа запроса (изображение или чат).
- Далее устанавливаются заголовки (`headers`) для HTTP-запроса, включая `accept`, `accept-language`, `content-type`, `origin`, `user-agent` и `websim-flags`. Заголовки `referer` устанавливаются в зависимости от типа запроса.
- В зависимости от типа запроса (изображение или чат) вызывается соответствующий метод для обработки запроса:
  - Если это запрос изображения, вызывается `cls._handle_image_request` с соответствующими параметрами.
  - Если это запрос чата, вызывается `cls._handle_chat_request` с соответствующими параметрами.
- Результаты, возвращаемые этими методами, передаются через `yield`, что делает функцию генератором.

**Примеры**:
```python
async def process_message(model_name: str, chat_messages: Messages):
    async for result in Websim.create_async_generator(model=model_name, messages=chat_messages):
        print(result)

# Пример вызова для текстового запроса
asyncio.run(process_message(model_name="gemini-1.5-pro", chat_messages=[{"role": "user", "content": "Hello!"}]))

# Пример вызова для запроса изображения
asyncio.run(process_message(model_name="flux", chat_messages=[{"role": "user", "content": "A cat"}]))
```

### `_handle_image_request`

```python
@classmethod
async def _handle_image_request(
    cls,
    project_id: str,
    messages: Messages,
    prompt: str,
    aspect_ratio: str,
    headers: dict,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """ """
```

**Назначение**: Обрабатывает запросы на генерацию изображений.

**Параметры**:
- `project_id` (str): ID проекта.
- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str): Промпт для генерации изображения.
- `aspect_ratio` (str): Соотношение сторон изображения.
- `headers` (dict): Заголовки для HTTP-запроса.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в запросе.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса (объект `ImageResponse`).

**Как работает функция**:
- Функция `_handle_image_request` обрабатывает запросы на генерацию изображений с использованием API Websim AI.
- Сначала формируется используемый промпт (`used_prompt`) с использованием функции `format_image_prompt`, которая принимает список сообщений (`messages`) и основной промпт (`prompt`).
- Затем создается асинхронная сессия `ClientSession` с передачей заголовков (`headers`).
- Формируется словарь `data`, который содержит `project_id`, `prompt` (использованный) и `aspect_ratio`.
- Выполняется POST-запрос к API `cls.image_api_endpoint` с использованием асинхронной сессии. В запросе передаются данные (`data`) в формате JSON и, при необходимости, прокси-сервер (`proxy`).
- После получения ответа проверяется статус с помощью `raise_for_status`, чтобы убедиться, что запрос выполнен успешно (код 200).
- Текст ответа преобразуется в JSON-формат, и извлекается URL изображения (`image_url`).
- Если URL изображения получен, он передается в виде объекта `ImageResponse`, который содержит список URL изображений (`images`) и альтернативный текст (`alt`), в данном случае используемый промпт.
- Результат возвращается с использованием `yield`, что позволяет функции быть асинхронным генератором.

**Примеры**:
```python
async def generate_image(project_id: str, messages: Messages, prompt: str, aspect_ratio: str):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://websim.ai',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'websim-flags;': '',
        'referer': 'https://websim.ai/@ISWEARIAMNOTADDICTEDTOPILLOW/ai-image-prompt-generator'
    }
    async for result in Websim._handle_image_request(
        project_id=project_id,
        messages=messages,
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        headers=headers
    ):
        print(result)

# Пример вызова
asyncio.run(generate_image(
    project_id="test_image_123",
    messages=[{"role": "user", "content": "Generate an image of a cat"}],
    prompt="A cat",
    aspect_ratio="1:1"
))
```

### `_handle_chat_request`

```python
@classmethod
async def _handle_chat_request(
    cls,
    project_id: str,
    messages: Messages,
    headers: dict,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """ """
```

**Назначение**: Обрабатывает запросы на генерацию текста (чат).

**Параметры**:
- `project_id` (str): ID проекта.
- `messages` (Messages): Список сообщений для отправки.
- `headers` (dict): Заголовки для HTTP-запроса.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в запросе.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса (текст ответа).

**Как работает функция**:
- Функция `_handle_chat_request` обрабатывает запросы к чат-API Websim AI. Она отправляет сообщения и получает ответы, а также обрабатывает возможные ошибки и повторные попытки при превышении лимита запросов.
- Устанавливается максимальное количество повторных попыток (`max_retries`) равным 3.
- В цикле `while` выполняются попытки отправки запроса до тех пор, пока не будет достигнуто максимальное количество попыток или не будет получен успешный ответ.
- Внутри цикла создается асинхронная сессия `ClientSession` с передачей заголовков (`headers`).
- Формируется словарь `data`, который содержит `project_id` и `messages`.
- Выполняется POST-запрос к API `cls.chat_api_endpoint` с использованием асинхронной сессии. В запросе передаются данные (`data`) в формате JSON и, при необходимости, прокси-сервер (`proxy`).
- Обрабатываются возможные ошибки:
  - Если получен статус 429 (превышение лимита запросов), извлекается текст ответа, создается исключение `ResponseStatusError`, увеличивается счетчик повторных попыток (`retry_count`) и выполняется ожидание (`asyncio.sleep`) в течение времени, зависящего от количества попыток (2 в степени `retry_count`). Если достигнуто максимальное количество попыток, исключение поднимается выше.
  - Если получен любой другой статус ошибки, выполняется `raise_for_status`, чтобы вызвать исключение для данного статуса.
- После получения успешного ответа извлекается текст ответа (`response_text`) и попытка его преобразования в JSON-формат.
  - Если преобразование в JSON успешно, извлекается содержимое (`content`) из JSON-ответа, удаляются начальные и конечные пробелы (`strip`) и результат передается с использованием `yield`. После этого цикл прерывается (`break`).
  - Если преобразование в JSON вызывает ошибку `json.JSONDecodeError`, текст ответа передается как есть с использованием `yield`, и цикл прерывается (`break`).
- Если в процессе выполнения запроса возникает исключение `ResponseStatusError` и это связано с превышением лимита запросов, выполняется ожидание и повторная попытка, как описано выше. Если достигнуто максимальное количество попыток, исключение поднимается выше.
- Если возникает любое другое исключение, оно поднимается выше.

**Примеры**:
```python
async def send_chat_message(project_id: str, messages: Messages):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://websim.ai',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'websim-flags;': '',
        'referer': 'https://websim.ai/@ISWEARIAMNOTADDICTEDTOPILLOW/zelos-ai-assistant'
    }
    async for result in Websim._handle_chat_request(
        project_id=project_id,
        messages=messages,
        headers=headers
    ):
        print(result)

# Пример вызова
asyncio.run(send_chat_message(
    project_id="test_chat_123",
    messages=[{"role": "user", "content": "Hello!"}]
))