# Модуль Copilot для работы с GPT-4 Free

## Обзор

Данный модуль реализует класс `Copilot`, представляющий собой провайдера, который позволяет использовать GPT-4 Free для генерации текста, перевода, кода и создания изображений. Модуль `Copilot` использует библиотеку `curl_cffi` для работы с WebSockets и `nodriver` для доступа к браузеру. 

## Подробнее

Модуль `Copilot` предоставляет возможность использовать модель GPT-4 Free, доступную через интерфейс Copilot Microsoft. Он использует WebSocket-соединение для общения с моделью и предоставляет следующие функции:

- Генерация текста:  создание текста, переводы, написание стихов и т.д.
- Генерация кода: создание программного кода на различных языках программирования.
- Генерация изображений: создание изображений на основе текстового описания.

## Классы

### `class Copilot`

**Описание**:  Класс, реализующий провайдера GPT-4 Free.

**Наследует**: 
    - `AbstractProvider`: Базовый класс для провайдеров.
    - `ProviderModelMixin`:  Mixin для работы с моделями.

**Атрибуты**:

- `label`: Имя провайдера (в данном случае "Microsoft Copilot").
- `url`: Базовый URL-адрес.
- `working`: Указывает, доступен ли провайдер (в данном случае `True`).
- `supports_stream`: Указывает, поддерживает ли провайдер потоковую передачу (в данном случае `True`).
- `default_model`:  Название модели по умолчанию (в данном случае "Copilot").
- `models`: Список доступных моделей.
- `model_aliases`: Словарь для сопоставления псевдонимов моделей с их реальными названиями.
- `websocket_url`: URL-адрес для WebSocket-соединения.
- `conversation_url`: URL-адрес для создания новых бесед.
- `_access_token`:  Токен доступа для аутентификации.
- `_cookies`:  Словарь с куки.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool = False, proxy: str = None, timeout: int = 900, prompt: str = None, media: MediaListType = None, conversation: BaseConversation = None, return_conversation: bool = False, api_key: str = None, **kwargs) -> CreateResult`: 
    - **Назначение**: Создает новую беседу с GPT-4 Free и отправляет запросы для генерации ответов. 
    - **Параметры**:
        - `model (str)`:  Название используемой модели.
        - `messages (Messages)`:  Список сообщений для контекста.
        - `stream (bool)`:  Указывает, необходимо ли использовать потоковую передачу.
        - `proxy (str)`:  Адрес прокси-сервера.
        - `timeout (int)`:  Таймаут соединения в секундах.
        - `prompt (str)`:  Текст запроса для модели.
        - `media (MediaListType)`:  Список медиа-файлов.
        - `conversation (BaseConversation)`:  Существующая беседа.
        - `return_conversation (bool)`:  Возвращает объект беседы.
        - `api_key (str)`:  Ключ API.
    - **Возвращает**:
        - `CreateResult`:  Генератор с ответами модели.
    - **Вызывает исключения**:
        - `MissingRequirementsError`:  Если не установлены необходимые пакеты.
        - `NoValidHarFileError`:  Если не найдены файлы HAR с токеном доступа.
        - `MissingAuthError`:  Если отсутствует токен доступа.
    - **Как работает**:
        1. Проверяет наличие необходимых пакетов.
        2. Извлекает токен доступа и куки из файлов HAR или через браузер (если файлы HAR не найдены).
        3. Соединяется с WebSocket-сервером.
        4. Создает новую беседу (если она не была передана в качестве параметра).
        5. Отправляет сообщение с запросом модели.
        6. Получает и возвращает ответы модели.
        7. Закрывает WebSocket-соединение.
    - **Примеры**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot
        from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
        
        messages: Messages = [
            {"role": "user", "content": "Привет! Как дела?"},
            {"role": "assistant", "content": "Привет! У меня все отлично, а у тебя?"},
        ]
        provider = Copilot()
        for response in provider.create_completion(model="Copilot", messages=messages, stream=True):
            print(response)
        ```
- `get_access_token_and_cookies(url: str, proxy: str = None, target: str = "ChatAI",):`: 
    - **Назначение**:  Извлекает токен доступа и куки из браузера. 
    - **Параметры**:
        - `url (str)`:  URL-адрес для доступа к данным.
        - `proxy (str)`:  Адрес прокси-сервера.
        - `target (str)`:  Целевой объект для токена доступа.
    - **Возвращает**:
        - `tuple`:  Кортеж из токена доступа и словаря с куки.
    - **Как работает**:
        1. Инициализирует браузер с помощью `nodriver`.
        2. Загружает страницу по указанному URL-адресу.
        3. Извлекает токен доступа из localStorage браузера.
        4. Извлекает куки из браузера.
        5. Закрывает браузер.
        6. Возвращает токен доступа и куки.
    - **Примеры**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import get_access_token_and_cookies
        
        access_token, cookies = await get_access_token_and_cookies(url="https://copilot.microsoft.com")
        print(access_token)
        print(cookies)
        ```
- `readHAR(url: str)`: 
    - **Назначение**:  Читает файлы HAR и извлекает из них токен доступа и куки.
    - **Параметры**:
        - `url (str)`:  URL-адрес для поиска токена доступа.
    - **Возвращает**:
        - `tuple`:  Кортеж из токена доступа и словаря с куки.
    - **Вызывает исключения**:
        - `NoValidHarFileError`:  Если не найдены файлы HAR с токеном доступа.
    - **Как работает**:
        1. Проходит по всем найденным файлам HAR.
        2. Для каждого файла HAR:
            - Извлекает записи из HAR-файла.
            - Ищет в записях запрос с URL-адресом, начинающимся с `url`.
            - Извлекает заголовок "Authorization" и куки из записи.
        3. Если найден токен доступа, возвращает его и куки.
        4. Если токен доступа не найден, выбрасывает исключение `NoValidHarFileError`.
    - **Примеры**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import readHAR
        
        access_token, cookies = readHAR(url="https://copilot.microsoft.com")
        print(access_token)
        print(cookies)
        ```

## Методы класса

### `get_clarity() -> bytes`: 
    - **Назначение**: Возвращает зашифрованный текст для аутентификации.
    - **Параметры**: 
        - Нет.
    - **Возвращает**:
        - `bytes`:  Зашифрованный текст.
    - **Как работает**:
        - Декодирует базовый64-строку, представляющую зашифрованный текст.
        - Возвращает декодированный текст.
    - **Примеры**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import get_clarity
        
        clarity_text = get_clarity()
        print(clarity_text)
        ```
### `create_completion(model: str, messages: Messages, stream: bool = False, proxy: str = None, timeout: int = 900, prompt: str = None, media: MediaListType = None, conversation: BaseConversation = None, return_conversation: bool = False, api_key: str = None, **kwargs) -> CreateResult`: 
    - **Назначение**: Создает новую беседу с GPT-4 Free и отправляет запросы для генерации ответов. 
    - **Параметры**:
        - `model (str)`:  Название используемой модели.
        - `messages (Messages)`:  Список сообщений для контекста.
        - `stream (bool)`:  Указывает, необходимо ли использовать потоковую передачу.
        - `proxy (str)`:  Адрес прокси-сервера.
        - `timeout (int)`:  Таймаут соединения в секундах.
        - `prompt (str)`:  Текст запроса для модели.
        - `media (MediaListType)`:  Список медиа-файлов.
        - `conversation (BaseConversation)`:  Существующая беседа.
        - `return_conversation (bool)`:  Возвращает объект беседы.
        - `api_key (str)`:  Ключ API.
    - **Возвращает**:
        - `CreateResult`:  Генератор с ответами модели.
    - **Вызывает исключения**:
        - `MissingRequirementsError`:  Если не установлены необходимые пакеты.
        - `NoValidHarFileError`:  Если не найдены файлы HAR с токеном доступа.
        - `MissingAuthError`:  Если отсутствует токен доступа.
    - **Как работает**:
        1. Проверяет наличие необходимых пакетов.
        2. Извлекает токен доступа и куки из файлов HAR или через браузер (если файлы HAR не найдены).
        3. Соединяется с WebSocket-сервером.
        4. Создает новую беседу (если она не была передана в качестве параметра).
        5. Отправляет сообщение с запросом модели.
        6. Получает и возвращает ответы модели.
        7. Закрывает WebSocket-соединение.
    - **Примеры**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot
        from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
        
        messages: Messages = [
            {"role": "user", "content": "Привет! Как дела?"},
            {"role": "assistant", "content": "Привет! У меня все отлично, а у тебя?"},
        ]
        provider = Copilot()
        for response in provider.create_completion(model="Copilot", messages=messages, stream=True):
            print(response)
        ```


## Параметры класса

- `label (str)`: Имя провайдера (в данном случае "Microsoft Copilot").
- `url (str)`: Базовый URL-адрес.
- `working (bool)`: Указывает, доступен ли провайдер (в данном случае `True`).
- `supports_stream (bool)`: Указывает, поддерживает ли провайдер потоковую передачу (в данном случае `True`).
- `default_model (str)`:  Название модели по умолчанию (в данном случае "Copilot").
- `models (list[str])`: Список доступных моделей.
- `model_aliases (dict[str, str])`: Словарь для сопоставления псевдонимов моделей с их реальными названиями.
- `websocket_url (str)`: URL-адрес для WebSocket-соединения.
- `conversation_url (str)`: URL-адрес для создания новых бесед.
- `_access_token (str)`:  Токен доступа для аутентификации.
- `_cookies (dict)`:  Словарь с куки.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня все отлично, а у тебя?"},
]
provider = Copilot()
for response in provider.create_completion(model="Copilot", messages=messages, stream=True):
    print(response)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import get_access_token_and_cookies

access_token, cookies = await get_access_token_and_cookies(url="https://copilot.microsoft.com")
print(access_token)
print(cookies)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import readHAR

access_token, cookies = readHAR(url="https://copilot.microsoft.com")
print(access_token)
print(cookies)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import get_clarity

clarity_text = get_clarity()
print(clarity_text)
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Copilot import Copilot
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня все отлично, а у тебя?"},
]
provider = Copilot()
for response in provider.create_completion(model="Copilot", messages=messages, stream=True):
    print(response)
```

## Твое поведение при анализе кода:

- внутри кода ты можешь встретить выражение между `<` `>`. Например: `<инструкция для модели gemini:Загрузка описаний товаров в PrestaShop.>, <далее, если есть>. Это заготовки, куда ты вставляешь релевантное значение
- всегда смотри системную инструкцию для обработки кода проекта `hypotez`;
- анализируй расположение файла в проекте. Это поможет понять его назначение и взаимосвязь с другими файлами. Расположение файла ты найдешь в самой превой строке кода, начинающейся с `## \\file /...`;
- запоминай предоставленный код и анализируй его связь с другими частями проекта;
- В этой инструкции не надо предлагать улучшение кода. Четко следуй пункту 5. **Пример файла** при составлении ответа 

```markdown