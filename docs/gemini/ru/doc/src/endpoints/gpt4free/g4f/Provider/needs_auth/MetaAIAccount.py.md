# Модуль MetaAIAccount

## Обзор

Модуль содержит класс `MetaAIAccount`, который является подклассом `MetaAI` и предоставляет функциональность для работы с учетной записью Meta AI.

## Подробней

Модуль обеспечивает доступ к моделям Meta AI, таким как `meta` (модель генерации изображений). 

## Классы

### `class MetaAIAccount`

**Описание**: Класс `MetaAIAccount` представляет собой модель для работы с учетной записью Meta AI, предоставляя функциональность для аутентификации и вызова API Meta AI. 
**Наследует**: `MetaAI`

**Атрибуты**:
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация для работы с моделью. По умолчанию установлен в `True`, поскольку доступ к Meta AI требует авторизацию.
- `parent` (str): Указывает родительский класс. В данном случае - `MetaAI`.
- `image_models` (list): Список моделей, поддерживаемых классом. Включает только `meta` (модель генерации изображений).

**Методы**:
- `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, **kwargs) -> AsyncResult` 

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAI import Messages

messages = Messages(
    role = "user", 
    content = "some text"
)

# Создание инстанса модели MetaAIAccount для вызова API Meta AI
meta_ai_account = MetaAIAccount()
async for chunk in meta_ai_account.create_async_generator(model='meta', messages=messages):
    print(chunk)
```

### `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, **kwargs) -> AsyncResult`

**Назначение**: 
- Функция создает асинхронный генератор для работы с моделью Meta AI.
- Генератор позволяет обрабатывать результаты от API Meta AI по частям, что эффективно при работе с большими объемами данных. 

**Параметры**:
- `model` (str): Название модели Meta AI.
- `messages` (Messages): Список сообщений для отправки в API Meta AI.
- `proxy` (str, optional): Прокси-сервер для подключения к API Meta AI. По умолчанию `None`.
- `cookies` (Cookies, optional): Куки-файлы для авторизации в Meta AI. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут передаваться в API Meta AI.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает результаты от API Meta AI. 

**Вызывает исключения**:
- `Exception`: В случае возникновения ошибок при работе с API Meta AI.

**Как работает функция**:
- Функция получает необходимые параметры для вызова API Meta AI, такие как модель, сообщения, прокси-сервер и куки-файлы.
- Проверяет наличие куки-файлов. Если они не предоставлены, извлекает их из браузера.
- Форматирует сообщения для отправки в API Meta AI.
- Использует метод `prompt` родительского класса `MetaAI` для отправки запроса к API Meta AI.
- Возвращает асинхронный генератор, который выдает результаты от API Meta AI.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAI import Messages

messages = Messages(
    role = "user", 
    content = "some text"
)

# Создание инстанса модели MetaAIAccount для вызова API Meta AI
meta_ai_account = MetaAIAccount()
async for chunk in meta_ai_account.create_async_generator(model='meta', messages=messages):
    print(chunk)
```

**Внутренние функции**:

- Нет.

## Параметры класса

- Нет.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAI import Messages

messages = Messages(
    role = "user", 
    content = "some text"
)

# Создание инстанса модели MetaAIAccount для вызова API Meta AI
meta_ai_account = MetaAIAccount()
async for chunk in meta_ai_account.create_async_generator(model='meta', messages=messages):
    print(chunk)
```