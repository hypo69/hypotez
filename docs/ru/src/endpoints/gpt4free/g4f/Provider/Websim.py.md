# Модуль Websim

## Обзор

Модуль Websim предоставляет асинхронный интерфейс для взаимодействия с AI-платформой Websim.ai. Он поддерживает как генерацию текста (чат), так и генерацию изображений через API Websim. Этот модуль предназначен для использования в асинхронных приложениях и предоставляет функциональность для создания запросов к Websim AI и обработки ответов.
Модуль включает в себя функции для создания уникальных project ID, обработки запросов чата и изображений, а также обработки ошибок и повторных попыток при возникновении проблем с API.

## Подробней

Этот модуль позволяет интегрировать функциональность Websim AI в проект `hypotez`. Он может использоваться для создания чат-ботов, генерации изображений на основе текстовых запросов и других задач, связанных с AI. Модуль предоставляет удобный интерфейс для взаимодействия с API Websim, обрабатывая детали реализации запросов и ответов.

## Классы

### `Websim`

**Описание**: Класс `Websim` является асинхронным провайдером и предоставляет методы для взаимодействия с API Websim.ai. Он поддерживает как текстовые запросы (чат), так и запросы на генерацию изображений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL главной страницы Websim.ai.
- `login_url` (Optional[str]): URL для логина (в данном случае `None`, так как не требуется).
- `chat_api_endpoint` (str): URL для API чата.
- `image_api_endpoint` (str): URL для API генерации изображений.
- `working` (bool): Указывает, что провайдер в рабочем состоянии (`True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (`False`).
- `use_nodriver` (bool): Указывает, требуется ли использование драйвера (`False`).
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (`False`).
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (`True`).
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (`True`).
- `default_model` (str): Модель, используемая по умолчанию для чата (`'gemini-1.5-pro'`).
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (`'flux'`).
- `image_models` (List[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (List[str]): Список всех поддерживаемых моделей (чат и изображения).

**Методы**:
- `generate_project_id(for_image: bool = False) -> str`: Генерирует уникальный project ID.
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", project_id: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для обработки запросов.
- `_handle_image_request(project_id: str, messages: Messages, prompt: str, aspect_ratio: str, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запрос на генерацию изображения.
- `_handle_chat_request(project_id: str, messages: Messages, headers: dict, proxy: str = None, **kwargs) -> AsyncResult`: Обрабатывает запрос чата.

## Функции

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

**Назначение**: Генерирует уникальный идентификатор проекта (project ID) в зависимости от того, предназначен ли он для запроса изображения или для запроса чата.

**Параметры**:
- `for_image` (bool): Определяет, генерируется ли ID для запроса изображения. По умолчанию `False`.

**Возвращает**:
- `str`: Уникальный идентификатор проекта в формате, специфичном для Websim.

**Как работает функция**:

1.  **Определение набора символов**: Определяет набор символов, включающий строчные буквы ASCII и цифры, из которого будет генерироваться ID.
2.  **Генерация ID для изображения**: Если `for_image` равен `True`, генерирует ID в формате `xxx_xxxxxxxxxxxx`, где `xxx` - 7 случайных символов, а `xxxxxxxxxxxx` - 12 случайных символов.
3.  **Генерация ID для чата**: Если `for_image` равен `False`, генерирует ID в формате `xxx_xxxxxxxxxxxxxxxxx`, где `xxx` - 3 случайных символа, а `xxxxxxxxxxxxxxxxx` - 15 случайных символов.
4.  **Возврат ID**: Возвращает сгенерированный ID.

**ASCII flowchart**:

```
    Начало
    │
    │ for_image == True?
    ├─Да─►  Генерация ID для изображения (7 + "_" + 12 символов)
    │   │
    │   └─►  Возврат ID
    │
    └─Нет─►  Генерация ID для чата (3 + "_" + 15 символов)
        │
        └─►  Возврат ID
    │
    Конец
```

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
        Создает асинхронный генератор для обработки запросов.
        """
```

**Назначение**: Создает асинхронный генератор для обработки запросов к API Websim, будь то запросы на генерацию изображений или текстовые запросы (чат).

**Параметры**:
- `model` (str): Модель для использования (например, `'gemini-1.5-pro'` или `'flux'`).
- `messages` (Messages): Список сообщений для отправки в API.
- `prompt` (Optional[str]): Текст запроса (может быть `None`). По умолчанию `None`.
- `proxy` (Optional[str]): URL прокси-сервера для использования (может быть `None`). По умолчанию `None`.
- `aspect_ratio` (str): Соотношение сторон изображения (например, `"1:1"`). По умолчанию `"1:1"`.
- `project_id` (Optional[str]): Уникальный идентификатор проекта (если `None`, генерируется автоматически). По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса.

**Как работает функция**:

1.  **Определение типа запроса**: Проверяет, является ли запрос запросом на изображение, сравнивая значение `model` со списком `cls.image_models`.
2.  **Генерация `project_id`**: Если `project_id` не предоставлен, генерирует его с помощью `cls.generate_project_id()` в зависимости от типа запроса.
3.  **Определение заголовков**: Устанавливает заголовки для HTTP-запроса, включая `content-type`, `origin`, `user-agent` и другие. Заголовки могут отличаться в зависимости от типа запроса.
4.  **Обработка запроса изображения**: Если запрос является запросом на изображение, вызывает `cls._handle_image_request()` для обработки запроса.
5.  **Обработка запроса чата**: Если запрос является запросом чата, вызывает `cls._handle_chat_request()` для обработки запроса.
6.  **Возврат результатов**: Возвращает результаты, полученные от `_handle_image_request` или `_handle_chat_request`, как асинхронный генератор.

**ASCII flowchart**:

```
    Начало
    │
    │ model in cls.image_models?
    ├─Да─►  Генерация project_id (если отсутствует)
    │   │
    │   └─►  Установка заголовков для запроса изображения
    │   │
    │   └─►  Вызов cls._handle_image_request()
    │   │
    │   └─►  Возврат результатов из _handle_image_request()
    │
    └─Нет─►  Генерация project_id (если отсутствует)
        │
        └─►  Установка заголовков для запроса чата
        │
        └─►  Вызов cls._handle_chat_request()
        │
        └─►  Возврат результатов из _handle_chat_request()
    │
    Конец
```

**Примеры**:

```python
#Пример создания асинхронного генератора для запроса изображения:
messages = [{"role": "user", "content": "A cat"}]
async for result in Websim.create_async_generator(model='flux', messages=messages, aspect_ratio='16:9'):
    print(result)

#Пример создания асинхронного генератора для запроса чата:
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for result in Websim.create_async_generator(model='gemini-1.5-pro', messages=messages):
    print(result)
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
        """
        Обрабатывает запрос на генерацию изображения.
        """
```

**Назначение**: Отправляет запрос на генерацию изображения в API Websim и обрабатывает ответ.

**Параметры**:
- `project_id` (str): Уникальный идентификатор проекта.
- `messages` (Messages): Список сообщений для отправки в API.
- `prompt` (str): Текст запроса для генерации изображения.
- `aspect_ratio` (str): Соотношение сторон изображения.
- `headers` (dict): Заголовки HTTP-запроса.
- `proxy` (Optional[str]): URL прокси-сервера для использования (может быть `None`). По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса (URL изображения).

**Как работает функция**:

1.  **Форматирование запроса**: Форматирует запрос изображения с использованием `format_image_prompt`.
2.  **Создание сессии**: Создает асинхронную HTTP-сессию с заданными заголовками.
3.  **Отправка запроса**: Отправляет POST-запрос к API `cls.image_api_endpoint` с данными `project_id`, `prompt` и `aspect_ratio` в формате JSON.
4.  **Обработка ответа**: Проверяет статус ответа и вызывает `raise_for_status` для обработки ошибок.
5.  **Извлечение URL изображения**: Извлекает URL изображения из JSON-ответа.
6.  **Возврат URL изображения**: Создает объект `ImageResponse` с URL изображения и возвращает его через генератор.

**ASCII flowchart**:

```
    Начало
    │
    │ Форматирование запроса изображения (format_image_prompt)
    │
    │ Создание асинхронной HTTP-сессии
    │
    │ Отправка POST-запроса к API (cls.image_api_endpoint)
    │
    │ Проверка статуса ответа (raise_for_status)
    │
    │ Извлечение URL изображения из JSON-ответа
    │
    │ Создание и возврат объекта ImageResponse
    │
    Конец
```

**Примеры**:

```python
#Пример использования _handle_image_request:
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
messages = [{"role": "user", "content": "A cat"}]
prompt = "A cat"
async for result in Websim._handle_image_request(project_id='test_id', messages=messages, prompt=prompt, aspect_ratio='1:1', headers=headers):
    print(result)
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
        """
        Обрабатывает запрос чата.
        """
```

**Назначение**: Отправляет запрос чата в API Websim и обрабатывает ответ.

**Параметры**:
- `project_id` (str): Уникальный идентификатор проекта.
- `messages` (Messages): Список сообщений для отправки в API.
- `headers` (dict): Заголовки HTTP-запроса.
- `proxy` (Optional[str]): URL прокси-сервера для использования (может быть `None`). По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты запроса (текст ответа).

**Как работает функция**:

1.  **Инициализация повторных попыток**: Устанавливает максимальное количество повторных попыток (`max_retries`) и счетчик текущих попыток (`retry_count`).
2.  **Цикл повторных попыток**: Выполняет цикл, пока `retry_count` меньше `max_retries`.
3.  **Создание сессии**: Создает асинхронную HTTP-сессию с заданными заголовками.
4.  **Отправка запроса**: Отправляет POST-запрос к API `cls.chat_api_endpoint` с данными `project_id` и `messages` в формате JSON.
5.  **Обработка ответа**:
    - Проверяет статус ответа. Если статус равен 429 (слишком много запросов), увеличивает `retry_count`, ждет некоторое время и повторяет попытку.
    - Если статус не равен 429, вызывает `raise_for_status` для обработки ошибок.
    - Извлекает текст ответа.
    - Пытается извлечь содержимое ответа из JSON. Если успешно, возвращает содержимое. Если происходит ошибка JSONDecodeError, возвращает текст ответа.
6.  **Обработка ошибок**:
    - Обрабатывает исключение `ResponseStatusError` (ошибка статуса ответа).
    - Обрабатывает другие исключения.
7.  **Возврат результатов**: Возвращает текст ответа через генератор.

**ASCII flowchart**:

```
    Начало
    │
    │ Инициализация повторных попыток (retry_count = 0)
    │
    │ Цикл: пока retry_count < max_retries
    ├──► Создание асинхронной HTTP-сессии
    │   │
    │   │ Отправка POST-запроса к API (cls.chat_api_endpoint)
    │   │
    │   │ Проверка статуса ответа (response.status == 429?)
    │   ├──Да──► Увеличение retry_count
    │   │   │
    │   │   │ Ожидание (asyncio.sleep)
    │   │   │
    │   │   └──► Продолжение цикла
    │   │
    │   └──Нет──► Проверка статуса ответа (raise_for_status)
    │       │
    │       │ Извлечение текста ответа
    │       │
    │       │ Попытка извлечения содержимого из JSON
    │       │
    │       │ Возврат содержимого или текста ответа через генератор
    │
    └── Обработка исключений (ResponseStatusError, Exception)
    │
    Конец
```

**Примеры**:

```python
#Пример использования _handle_chat_request:
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://websim.ai',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'websim-flags;': ''
}
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for result in Websim._handle_chat_request(project_id='test_id', messages=messages, headers=headers):
    print(result)