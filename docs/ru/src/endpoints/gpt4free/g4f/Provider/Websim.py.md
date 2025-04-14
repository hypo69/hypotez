# Модуль Websim для g4f

## Обзор

Модуль `Websim` предоставляет асинхронный доступ к API Websim AI для генерации текста и изображений. Он включает в себя поддержку как чат-ориентированных запросов, так и запросов на генерацию изображений, используя различные модели, предоставляемые Websim AI. Модуль предназначен для интеграции в проекты, требующие взаимодействия с Websim AI для создания контента.

## Подробней

Модуль `Websim` является провайдером для библиотеки `g4f`, специализирующимся на взаимодействии с API Websim AI. Он поддерживает как текстовые запросы, так и запросы на генерацию изображений, предлагая выбор моделей, включая `gemini-1.5-pro` и `flux`. Модуль автоматически генерирует идентификаторы проектов и обрабатывает запросы к API Websim AI, возвращая результаты в виде асинхронных генераторов. Он также включает в себя логику повторных попыток для обработки ошибок, связанных с ограничением скорости.

## Классы

### `Websim`

**Описание**: Класс `Websim` предоставляет функциональность для взаимодействия с API Websim AI, поддерживая генерацию текста и изображений.

   **Наследует**:
   - `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
   - `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

   **Аттрибуты**:
   - `url` (str): URL веб-сайта Websim AI.
   - `login_url` (Optional[str]): URL для входа (в данном случае `None`).
   - `chat_api_endpoint` (str): URL для API чата.
   - `image_api_endpoint` (str): URL для API генерации изображений.
   - `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
   - `needs_auth` (bool): Указывает, требуется ли аутентификация (в данном случае `False`).
   - `use_nodriver` (bool): Указывает, используется ли драйвер (в данном случае `False`).
   - `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (в данном случае `False`).
   - `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (в данном случае `True`).
   - `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (в данном случае `True`).
   - `default_model` (str): Модель, используемая по умолчанию для генерации текста (`gemini-1.5-pro`).
   - `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (`flux`).
   - `image_models` (List[str]): Список поддерживаемых моделей для генерации изображений.
   - `models` (List[str]): Список всех поддерживаемых моделей (текст и изображения).

**Методы**:
   - `generate_project_id(for_image: bool = False) -> str`: Генерирует идентификатор проекта в зависимости от типа запроса (текст или изображение).
   - `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для выполнения запроса к API Websim AI.
   - `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запрос на генерацию изображения.
   - `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запрос к API чата.

## Функции

### `generate_project_id`

```python
@staticmethod
def generate_project_id(for_image: bool = False) -> str:
    """
    Generate a project ID in the appropriate format
    
    For chat: format like \'ke3_xh5gai3gjkmruomu\'
    For image: format like \'kx0m131_rzz66qb2xoy7\'
    """
```

**Назначение**: Генерирует идентификатор проекта в формате, специфичном для Websim AI, в зависимости от того, предназначен ли он для запроса изображения или чата.

**Параметры**:
   - `for_image` (bool): Если `True`, генерирует идентификатор для запроса изображения, иначе - для запроса чата. По умолчанию `False`.

**Возвращает**:
   - `str`: Сгенерированный идентификатор проекта.

**Как работает функция**:
1. Определяет набор символов для генерации идентификатора (строчные буквы и цифры).
2. Если `for_image` равно `True`, генерирует идентификатор, состоящий из двух частей, разделенных символом `_`, где первая часть состоит из 7 символов, а вторая - из 12.
3. Если `for_image` равно `False`, генерирует идентификатор, состоящий из префикса из 3 символов и суффикса из 15 символов, разделенных символом `_`.

**Примеры**:
```python
>>> Websim.generate_project_id(for_image=True)
'kx0m131_rzz66qb2xoy7'

>>> Websim.generate_project_id(for_image=False)
'ke3_xh5gai3gjkmruomu'
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
    """
    <Тут Ты пишешь что именно делает функция>
    """
```

**Назначение**: Создает асинхронный генератор для выполнения запроса к API Websim AI. Он определяет, является ли запрос запросом изображения или чата, генерирует идентификатор проекта (если он не предоставлен) и вызывает соответствующий обработчик запроса.

**Параметры**:
   - `model` (str): Модель, используемая для генерации.
   - `messages` (Messages): Список сообщений для отправки в API.
   - `prompt` (str, optional): Промпт для генерации изображения. По умолчанию `None`.
   - `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
   - `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
   - `project_id` (str, optional): Идентификатор проекта. Если не указан, генерируется автоматически. По умолчанию `None`.
   - `**kwargs`: Дополнительные параметры для передачи в API.

**Возвращает**:
   - `AsyncResult`: Асинхронный генератор, возвращающий результаты от API.

**Как работает функция**:
1. Определяет, является ли запрос запросом изображения, проверяя, входит ли модель в список `image_models`.
2. Генерирует идентификатор проекта, если он не был предоставлен.
3. Устанавливает заголовки для запроса, включая `referer` в зависимости от типа запроса.
4. Вызывает `_handle_image_request` или `_handle_chat_request` в зависимости от типа запроса и возвращает результаты, полученные от этих функций.

**Внутренние функции**:

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
    """
    <Тут Ты пишешь что именно делает функция>
    """
```

**Назначение**: Обрабатывает запрос на генерацию изображения, отправляя запрос к API Websim AI и возвращая URL изображения.

**Параметры**:
   - `project_id` (str): Идентификатор проекта.
   - `messages` (Messages): Список сообщений для отправки в API.
   - `prompt` (str): Промпт для генерации изображения.
   - `aspect_ratio` (str): Соотношение сторон изображения.
   - `headers` (dict): Заголовки для запроса.
   - `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
   - `**kwargs`: Дополнительные параметры для передачи в API.

**Возвращает**:
   - `AsyncResult`: Асинхронный генератор, возвращающий объект `ImageResponse` с URL изображения и альтернативным текстом.

**Как работает функция**:
1. Форматирует промпт, используя функцию `format_image_prompt`.
2. Отправляет POST-запрос к `image_api_endpoint` с идентификатором проекта, промптом и соотношением сторон в теле запроса.
3. Проверяет статус ответа и вызывает исключение, если произошла ошибка.
4. Извлекает URL изображения из JSON-ответа и возвращает объект `ImageResponse`.

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
    """
    <Тут Ты пишешь что именно делает функция>
    """
```

**Назначение**: Обрабатывает запрос к API чата, отправляя сообщения и возвращая ответ от Websim AI.

**Параметры**:
   - `project_id` (str): Идентификатор проекта.
   - `messages` (Messages): Список сообщений для отправки в API.
   - `headers` (dict): Заголовки для запроса.
   - `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
   - `**kwargs`: Дополнительные параметры для передачи в API.

**Возвращает**:
   - `AsyncResult`: Асинхронный генератор, возвращающий контент ответа от API.

**Как работает функция**:
1. Выполняет повторные попытки отправки запроса в случае получения ответа со статусом 429 (слишком много запросов).
2. Отправляет POST-запрос к `chat_api_endpoint` с идентификатором проекта и сообщениями в теле запроса.
3. Проверяет статус ответа и вызывает исключение, если произошла ошибка.
4. Извлекает контент из JSON-ответа и возвращает его.
5. Обрабатывает ошибки, связанные с лимитом запросов, выполняя повторные попытки с экспоненциальной задержкой.

     A
     ↓
     B → C
     ↓
     D

     Где:
     A - Начало обработки запроса
     B - Отправка POST запроса к Websim AI API
     C - Извлечение контента из JSON ответа
     D - Завершение обработки запроса

**Примеры**:
```python
# Пример использования create_async_generator для запроса чата
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for response in Websim.create_async_generator(model="gemini-1.5-pro", messages=messages):
    print(response)

# Пример использования create_async_generator для запроса изображения
messages = [{"role": "user", "content": "A futuristic cityscape"}]
async for response in Websim.create_async_generator(model="flux", messages=messages, prompt="futuristic cityscape"):
    print(response)