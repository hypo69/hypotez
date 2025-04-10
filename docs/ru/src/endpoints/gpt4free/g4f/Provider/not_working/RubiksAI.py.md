# Модуль для работы с RubiksAI
=================================================

Модуль содержит класс `RubiksAI`, который используется для взаимодействия с API Rubiks AI для генерации текста на основе предоставленных сообщений. Поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Обзор

Этот модуль предоставляет асинхронный интерфейс для взаимодействия с API Rubiks AI. Он позволяет отправлять запросы на генерацию текста с использованием различных моделей, поддерживаемых Rubiks AI, и получать ответы в потоковом режиме. Модуль также поддерживает использование прокси-серверов и веб-поиск.

## Подробнее

Модуль `RubiksAI` предназначен для интеграции с другими частями проекта `hypotez`, требующими взаимодействия с API Rubiks AI. Он обеспечивает удобный и гибкий интерфейс для отправки запросов и обработки ответов. Класс поддерживает различные модели, включая `gpt-4o-mini`, `gpt-4o`, `o1-mini`, `claude-3.5-sonnet`, `grok-beta`, `gemini-1.5-pro`, `nova-pro`, "llama-3.1-70b-versatile", а также позволяет использовать веб-поиск для улучшения качества ответов.

## Классы

### `RubiksAI`

**Описание**: Класс для взаимодействия с API Rubiks AI.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("Rubiks AI").
- `url` (str): URL провайдера ("https://rubiks.ai").
- `api_endpoint` (str): URL API провайдера ("https://rubiks.ai/search/api/").
- `working` (bool): Указывает, работает ли провайдер (True).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель по умолчанию ('gpt-4o-mini').
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Псевдонимы моделей.

**Методы**:
- `generate_mid()`: Генерирует строку 'mid'.
- `create_referer(q: str, mid: str, model: str = '') -> str`: Создает URL Referer с динамическими значениями q и mid.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, web_search: bool = False, temperature: float = 0.6, **kwargs) -> AsyncResult`: Создает асинхронный генератор, отправляющий запросы к API Rubiks AI и возвращающий ответы.

## Функции

### `generate_mid`

```python
    @staticmethod
    def generate_mid() -> str:
        """
        Generates a 'mid' string following the pattern:
        6 characters - 4 characters - 4 characters - 4 characters - 12 characters
        Example: 0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4
        """
        ...
```

**Назначение**: Генерирует случайную строку `mid` определенного формата.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `str`: Случайная строка, состоящая из нескольких частей, разделенных дефисами.

**Как работает функция**:

1.  **Инициализация частей**: Функция начинает с подготовки списка, в котором будут храниться отдельные части генерируемой строки.
2.  **Генерация каждой части**:
    *   Для каждой части используется `''.join(random.choices(string.ascii_lowercase + string.digits, k=N))`, где `N` — длина генерируемой подстроки.
    *   `random.choices(string.ascii_lowercase + string.digits, k=N)` выбирает `N` случайных символов из букв нижнего регистра и цифр.
    *   `''.join()` объединяет выбранные символы в одну строку.
3.  **Объединение частей**: Функция объединяет все сгенерированные части в одну строку, разделяя их дефисом `-`.

```
    Генерация частей строки mid
    │
    ├──> Выбор 6 случайных символов (буквы нижнего регистра и цифры)
    │
    ├──> Выбор 4 случайных символов (буквы нижнего регистра и цифры)
    │
    ├──> Выбор 4 случайных символов (буквы нижнего регистра и цифры)
    │
    ├──> Выбор 4 случайных символов (буквы нижнего регистра и цифры)
    │
    └──> Выбор 12 случайных символов (буквы нижнего регистра и цифры)
    │
    Объединение частей в строку, разделенных дефисом
    │
    Возврат строки mid
```

**Примеры**:
```python
mid = RubiksAI.generate_mid()
print(mid)  # Пример: 'a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5'
```

### `create_referer`

```python
    @staticmethod
    def create_referer(q: str, mid: str, model: str = '') -> str:
        """
        Creates a Referer URL with dynamic q and mid values, using urlencode for safe parameter encoding.
        """
        ...
```

**Назначение**: Создает URL Referer с динамическими значениями `q`, `mid` и `model`, используя `urlencode` для безопасного кодирования параметров.

**Параметры**:
- `q` (str): Параметр запроса для URL.
- `mid` (str): Идентификатор запроса.
- `model` (str, optional): Модель для использования в запросе. По умолчанию ''.

**Возвращает**:
- `str`: Сформированный URL Referer.

**Как работает функция**:

1.  **Создание словаря параметров**: Функция создает словарь, содержащий параметры `q`, `model` и `mid`.
2.  **Кодирование параметров**: Функция кодирует параметры с помощью `urlencode`, чтобы обеспечить их безопасную передачу в URL.
3.  **Формирование URL**: Функция формирует URL, объединяя базовый URL (`https://rubiks.ai/search/?`) с закодированными параметрами.

```
    Создание словаря параметров
    │
    ├──> Добавление 'q' в словарь
    │
    ├──> Добавление 'model' в словарь
    │
    └──> Добавление 'mid' в словарь
    │
    Кодирование параметров с помощью urlencode
    │
    Формирование URL
    │
    Возврат URL Referer
```

**Примеры**:
```python
referer_url = RubiksAI.create_referer(q='test query', mid='unique_id', model='gpt-4o-mini')
print(referer_url)  # Пример: 'https://rubiks.ai/search/?q=test+query&model=gpt-4o-mini&mid=unique_id'
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        web_search: bool = False,
        temperature: float = 0.6,
        **kwargs
    ) -> AsyncResult:
        """
        Creates an asynchronous generator that sends requests to the Rubiks AI API and yields the response.

        Parameters:
        - model (str): The model to use in the request.
        - messages (Messages): The messages to send as a prompt.
        - proxy (str, optional): Proxy URL, if needed.
        - web_search (bool, optional): Indicates whether to include search sources in the response. Defaults to False.
        """
        ...
```

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API Rubiks AI и возвращает ответы в потоковом режиме.

**Параметры**:
- `model` (str): Модель для использования в запросе.
- `messages` (Messages): Сообщения для отправки в качестве запроса.
- `proxy` (str, optional): URL прокси-сервера, если необходимо. По умолчанию `None`.
- `web_search` (bool, optional): Указывает, следует ли включать источники поиска в ответ. По умолчанию `False`.
- `temperature` (float): Температура для генерации текста. По умолчанию 0.6.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текст ответа.

**Как работает функция**:

1.  **Подготовка данных**:
    *   Выбирает модель с помощью `cls.get_model(model)`.
    *   Генерирует `mid_value` с помощью `cls.generate_mid()`.
    *   Создает `referer` с помощью `cls.create_referer()`.
    *   Формирует словарь `data` с сообщениями, моделью, параметрами поиска и потоковой передачи.
    *   Определяет заголовки запроса, включая `Referer` и `User-Agent`.

2.  **Отправка запроса**:
    *   Использует `aiohttp.ClientSession` для отправки асинхронного POST-запроса к `cls.api_endpoint`.
    *   Обрабатывает ответ, проверяя статус код с помощью `raise_for_status(response)`.

3.  **Обработка потока данных**:
    *   Читает ответ построчно в асинхронном режиме.
    *   Извлекает данные из каждой строки, декодирует их из UTF-8 и удаляет лишние пробелы.
    *   Проверяет начало строки на `data: `.
    *   Прекращает обработку, если получает сообщения `[DONE]` или `{"done": ""}`.
    *   Пытается распарсить JSON из данных.

4.  **Обработка JSON данных**:
    *   Если `web_search` включен и в JSON есть `url` и `title`, добавляет источник в список `sources`.
    *   Если в JSON есть `choices`, извлекает содержимое из каждого выбора и возвращает его через `yield`.

5.  **Возврат источников поиска**:
    *   Если `web_search` включен и есть источники, возвращает их через `yield Sources(sources)`.

**Внутренние функции**:
- Внутри данной функции нет внутренних функций.

```
    Подготовка данных
    │
    ├──> Выбор модели
    │
    ├──> Генерация mid_value
    │
    ├──> Создание referer
    │
    └──> Формирование словаря data
    │
    Отправка запроса
    │
    ├──> Создание ClientSession
    │
    └──> Отправка POST запроса
    │
    Обработка потока данных
    │
    ├──> Чтение ответа построчно
    │
    ├──> Декодирование и очистка данных
    │
    ├──> Проверка начала строки
    │
    └──> Прекращение обработки при получении [DONE]
    │
    Обработка JSON данных
    │
    ├──> Проверка наличия url и title (для web_search)
    │
    └──> Извлечение содержимого из choices
    │
    Возврат источников поиска
    │
    └──> Возврат sources (если web_search включен)
```

**Примеры**:
```python
async def example():
    messages = [{"role": "user", "content": "Tell me a joke."}]
    async for response in RubiksAI.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(response, end="")

import asyncio
asyncio.run(example())