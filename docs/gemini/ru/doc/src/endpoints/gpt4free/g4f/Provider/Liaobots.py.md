# Модуль Liaobots

## Обзор

Модуль предоставляет класс `Liaobots` для взаимодействия с API-платформы Liaobots. Сайт предоставляет доступ к различным языковым моделям, таким как ChatGPT, Claude, Gemini, DeepSeek и Grok. 

## Классы

### `Liaobots`

**Описание**: Класс `Liaobots` реализует асинхронный генератор для взаимодействия с API Liaobots.

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Смешанный класс, обеспечивающий доступ к спискам поддерживаемых моделей и  их  алиасов.

**Атрибуты**:

- `url`:  URL-адрес платформы Liaobots.
- `working`:  Флаг, показывающий, доступна ли платформа Liaobots.
- `supports_message_history`: Флаг, указывающий, поддерживает ли платформа историю сообщений.
- `supports_system_message`: Флаг, указывающий, поддерживает ли платформа системные сообщения.
- `default_model`:  Идентификатор модели по умолчанию.
- `models`:  Список поддерживаемых моделей.
- `model_aliases`: Словарь, сопоставляющий псевдонимы моделей с их идентификаторами.
- `_auth_code`:  Строка с кодом авторизации.
- `_cookie_jar`:  Объект `CookieJar`, используемый для хранения куки.


**Методы**:

- `is_supported(model: str) -> bool`:  Проверяет, поддерживается ли указанная модель.

**Пример определения и использования**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Liaobots import Liaobots
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса Liaobots
provider = Liaobots()

# Проверка поддержки модели
supported = provider.is_supported("gpt-4o")  

# Использование класса Liaobots для запроса к API
messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(response)
        
```
### `Liaobots.create_async_generator`

**Назначение**: Метод создает асинхронный генератор для получения ответов от модели API Liaobots.

**Параметры**:

- `model: str`: Идентификатор модели.
- `messages: Messages`: Список сообщений для отправки модели.
- `proxy: str = None`:  Прокси-сервер для использования.
- `connector: BaseConnector = None`:  Объект `BaseConnector` для использования.
- `kwargs`:  Дополнительные параметры для модели.

**Возвращает**: 
- `AsyncResult`:  Асинхронный генератор ответов от модели.

**Вызывает исключения**:
- `RuntimeError`:  Если код авторизации пуст.

**Пример использования**:

```python
# Создание инстанса класса Liaobots
provider = Liaobots()

# Проверка поддержки модели
supported = provider.is_supported("gpt-4o")  

# Использование класса Liaobots для запроса к API
messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(response)
        
```

### `Liaobots.initialize_auth_code`

**Назначение**: Метод инициализирует код авторизации, выполняя необходимые запросы к API Liaobots.

**Параметры**:

- `session: ClientSession`: Объект `ClientSession` для выполнения запросов.

**Возвращает**: 
- `None`

**Вызывает исключения**:
- `RuntimeError`:  Если код авторизации пуст.

**Пример использования**:

```python
# Создание инстанса класса Liaobots
provider = Liaobots()

# Использование класса Liaobots для запроса к API
messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(response)
        
```

### `Liaobots.ensure_auth_code`

**Назначение**: Метод обеспечивает наличие инициализированного кода авторизации. Если код не инициализирован, он выполняет инициализацию.

**Параметры**:

- `session: ClientSession`: Объект `ClientSession` для выполнения запросов.

**Возвращает**: 
- `None`

**Пример использования**:

```python
# Создание инстанса класса Liaobots
provider = Liaobots()

# Использование класса Liaobots для запроса к API
messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(response)
        
```
## Параметры класса

### `model`

**Описание**: Идентификатор модели.

### `messages`

**Описание**: Список сообщений для отправки модели.

### `proxy`

**Описание**:  Прокси-сервер для использования.

### `connector`

**Описание**:  Объект `BaseConnector` для использования.

### `kwargs`

**Описание**:  Дополнительные параметры для модели.

## Примеры

```python
# Создание инстанса класса Liaobots
provider = Liaobots()

# Использование класса Liaobots для запроса к API
messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

async def main():
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(response)
        
```