# Провайдер GitHub Copilot

## Обзор

Этот модуль предоставляет класс `GithubCopilot`, который реализует асинхронный генератор для взаимодействия с сервисом GitHub Copilot. 

## Подробней

Модуль `GithubCopilot` предоставляет асинхронный генератор для получения ответов от модели GitHub Copilot. Он также обеспечивает поддержку аутентификации и потоковой передачи ответов.

**Функциональность:**

- Предоставляет асинхронный генератор `create_async_generator` для получения ответов от модели GitHub Copilot.
- Поддерживает различные модели GitHub Copilot, такие как `gpt-4o`, `o1-mini`, `o1-preview` и `claude-3.5-sonnet`.
- Обеспечивает поддержку потоковой передачи ответов.
- Использует библиотеку `aiohttp` для асинхронных запросов.
- Поддерживает аутентификацию с использованием токена доступа GitHub.
- Использует класс `Conversation` для хранения информации о сессии.

**Использование:**

- Создайте экземпляр класса `GithubCopilot` для использования сервиса GitHub Copilot.
- Вызовите метод `create_async_generator` для получения асинхронного генератора.
- Передайте в метод `create_async_generator` модель, список сообщений и другие параметры.
- Итерация по генератору вернет вам ответы от модели GitHub Copilot.


## Классы

### `class Conversation`

**Описание**:
    Класс `Conversation` хранит информацию о сессии с GitHub Copilot.

**Атрибуты**:
    - `conversation_id`:  ID сессии GitHub Copilot

**Методы**:
    - `__init__(conversation_id: str)`:  Инициализирует экземпляр класса `Conversation` с заданным `conversation_id`.


### `class GithubCopilot`

**Описание**:
    Класс `GithubCopilot` реализует асинхронный генератор для получения ответов от модели GitHub Copilot. 

**Наследует**:
    - `AsyncGeneratorProvider`: Интерфейс для асинхронных генераторов.
    - `ProviderModelMixin`: Интерфейс для управления моделями.

**Атрибуты**:
    - `label`:  Название провайдера.
    - `url`:  URL провайдера.
    - `working`:  Флаг, указывающий, работает ли провайдер.
    - `needs_auth`: Флаг, указывающий, требуется ли аутентификация.
    - `supports_stream`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу.
    - `default_model`:  Модель по умолчанию.
    - `models`:  Список поддерживаемых моделей.

**Методы**:
    - `create_async_generator(model: str, messages: Messages, stream: bool = False, api_key: str = None, proxy: str = None, cookies: Cookies = None, conversation_id: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult:`:  Асинхронный генератор для получения ответов от модели GitHub Copilot.

**Параметры**:
    - `model` (str):  Имя модели GitHub Copilot.
    - `messages` (Messages): Список сообщений для модели.
    - `stream` (bool):  Флаг, указывающий, следует ли использовать потоковую передачу.
    - `api_key` (str):  Токен доступа GitHub.
    - `proxy` (str):  Прокси-сервер для подключения.
    - `cookies` (Cookies):  Куки-файлы для аутентификации.
    - `conversation_id` (str):  ID сессии GitHub Copilot.
    - `conversation` (Conversation):  Экземпляр класса `Conversation`.
    - `return_conversation` (bool):  Флаг, указывающий, следует ли возвращать экземпляр класса `Conversation`.

**Возвращает**:
    - `AsyncResult`: Асинхронный результат.

**Вызывает исключения**:
    - `RequestError`: Если возникает ошибка при отправке запроса.

**Принцип работы**:
    Метод `create_async_generator` создает асинхронный генератор, который использует `aiohttp` для отправки запросов к API GitHub Copilot.
    Вначале метод проверяет наличие модели и токена доступа. Если токен доступа отсутствует, он получает его с помощью запроса к серверу GitHub.
    Далее метод отправляет запрос к API GitHub Copilot с использованием полученного токена доступа.
    Если сессия GitHub Copilot уже существует, метод использует ее ID.
    В противном случае, метод создает новую сессию и получает ее ID.
    Затем метод формирует JSON-объект с запросом и отправляет его к API GitHub Copilot.
    Метод использует потоковую передачу для получения ответов от модели.
    Каждый полученный ответ обрабатывается и возвращается как элемент генератора.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

# Создание экземпляра класса GithubCopilot
copilot = GithubCopilot()

# Получение асинхронного генератора для модели "gpt-4o"
async_generator = copilot.create_async_generator(
    model="gpt-4o",
    messages=["Привет, Copilot! Можешь написать мне код функции, которая суммирует два числа?"],
    api_key="YOUR_GITHUB_API_KEY"
)

# Итерация по генератору для получения ответов от модели
async for response in async_generator:
    print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

# Создание экземпляра класса GithubCopilot
copilot = GithubCopilot()

# Создание экземпляра класса Conversation
conversation = Conversation(conversation_id="YOUR_CONVERSATION_ID")

# Получение асинхронного генератора для модели "gpt-4o" с использованием существующей сессии
async_generator = copilot.create_async_generator(
    model="gpt-4o",
    messages=["Продолжи предыдущий код."],
    api_key="YOUR_GITHUB_API_KEY",
    conversation=conversation
)

# Итерация по генератору для получения ответов от модели
async for response in async_generator:
    print(response)
```

## Внутренние функции

**Внутренняя функция `get_cookies`**:

**Описание**:
    Функция `get_cookies` извлекает куки-файлы для аутентификации с сервера GitHub.

**Параметры**:
    - `domain` (str):  Домен для извлечения куки-файлов.

**Возвращает**:
    - `Cookies`:  Словарь куки-файлов.

**Принцип работы**:
    Функция `get_cookies` использует библиотеку `requests` для отправки запроса к серверу GitHub.
    Она извлекает куки-файлы из ответа сервера и возвращает их в виде словаря.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, get_cookies

# Получение куки-файлов для домена GitHub
cookies = get_cookies("github.com")

# Вывод куки-файлов
print(cookies)
```

**Внутренняя функция `format_prompt`**:

**Описание**:
    Функция `format_prompt` форматирует список сообщений для отправки к модели GitHub Copilot.

**Параметры**:
    - `messages` (Messages): Список сообщений.

**Возвращает**:
    - `str`:  Сформированный текст запроса.

**Принцип работы**:
    Функция `format_prompt`  соединяет сообщения из списка, разделяя их специальным разделителем.
    Она добавляет в начало текста запроса специальный префикс.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, format_prompt

# Список сообщений
messages = [
    "Привет, Copilot!",
    "Можешь написать мне код функции, которая суммирует два числа?",
]

# Форматирование запроса
prompt = format_prompt(messages)

# Вывод запроса
print(prompt)
```

**Внутренняя функция `get_last_user_message`**:

**Описание**:
    Функция `get_last_user_message` извлекает последнее сообщение пользователя из списка сообщений.

**Параметры**:
    - `messages` (Messages):  Список сообщений.

**Возвращает**:
    - `str`:  Текст последнего сообщения пользователя.

**Принцип работы**:
    Функция `get_last_user_message`  ищет последнее сообщение пользователя в списке сообщений.
    Она возвращает текст этого сообщения.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, get_last_user_message

# Список сообщений
messages = [
    "Привет, Copilot!",
    "Можешь написать мне код функции, которая суммирует два числа?",
    "Ты можешь сделать это?"
]

# Извлечение последнего сообщения пользователя
last_message = get_last_user_message(messages)

# Вывод последнего сообщения пользователя
print(last_message)
```

**Внутренняя функция `raise_for_status`**:

**Описание**:
    Функция `raise_for_status` проверяет статус ответа и вызывает исключение, если статус не является успешным.

**Параметры**:
    - `response` (Response):  Ответ от сервера.
    - `message` (str):  Сообщение об ошибке.

**Возвращает**:
    - `None`

**Вызывает исключения**:
    - `RequestError`: Если статус ответа не является успешным.

**Принцип работы**:
    Функция `raise_for_status`  проверяет статус ответа `response`.
    Если статус не является успешным, функция вызывает исключение `RequestError` с указанным сообщением `message`.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, raise_for_status

# Ответ от сервера
response = # ...

# Проверка статуса ответа
raise_for_status(response, "Ошибка при получении ответа от сервера.")
```

## Параметры класса

- `label` (str):  Название провайдера.
- `url` (str):  URL провайдера.
- `working` (bool):  Флаг, указывающий, работает ли провайдер.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу.
- `default_model` (str):  Модель по умолчанию.
- `models` (list):  Список поддерживаемых моделей.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

# Создание экземпляра класса GithubCopilot
copilot = GithubCopilot()

# Создание экземпляра класса Conversation
conversation = Conversation(conversation_id="YOUR_CONVERSATION_ID")

# Получение асинхронного генератора для модели "gpt-4o" с использованием существующей сессии
async_generator = copilot.create_async_generator(
    model="gpt-4o",
    messages=["Продолжи предыдущий код."],
    api_key="YOUR_GITHUB_API_KEY",
    conversation=conversation
)

# Итерация по генератору для получения ответов от модели
async for response in async_generator:
    print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

# Создание экземпляра класса GithubCopilot
copilot = GithubCopilot()

# Получение асинхронного генератора для модели "gpt-4o"
async_generator = copilot.create_async_generator(
    model="gpt-4o",
    messages=["Привет, Copilot! Можешь написать мне код функции, которая суммирует два числа?"],
    api_key="YOUR_GITHUB_API_KEY"
)

# Итерация по генератору для получения ответов от модели
async for response in async_generator:
    print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, get_cookies

# Получение куки-файлов для домена GitHub
cookies = get_cookies("github.com")

# Вывод куки-файлов
print(cookies)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, format_prompt

# Список сообщений
messages = [
    "Привет, Copilot!",
    "Можешь написать мне код функции, которая суммирует два числа?",
]

# Форматирование запроса
prompt = format_prompt(messages)

# Вывод запроса
print(prompt)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, get_last_user_message

# Список сообщений
messages = [
    "Привет, Copilot!",
    "Можешь написать мне код функции, которая суммирует два числа?",
    "Ты можешь сделать это?"
]

# Извлечение последнего сообщения пользователя
last_message = get_last_user_message(messages)

# Вывод последнего сообщения пользователя
print(last_message)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, raise_for_status

# Ответ от сервера
response = # ...

# Проверка статуса ответа
raise_for_status(response, "Ошибка при получении ответа от сервера.")
```
```markdown