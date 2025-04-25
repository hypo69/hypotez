# Серверный бэкенд для свободного API ChatGPT

## Обзор

Модуль `backend.py`  предоставляет API-интерфейс для доступа к модели ChatGPT. 
Он обрабатывает входящие запросы, формирует контекст для модели, отправляет запросы модели ChatGPT и возвращает ответы. 
API использует `Flask` для создания сервера и обработки запросов.

## Подробности

Модуль обеспечивает доступ к модели ChatGPT через API-интерфейс, реализованный на `Flask`. 
Он принимает запросы, преобразует их в формат, понятный модели ChatGPT, отправляет запросы 
и возвращает ответы в нужном формате. 

## Классы

### `Backend_Api`

**Описание**: Класс `Backend_Api` реализует серверную часть API для взаимодействия с моделью ChatGPT.

**Наследует**: 
    - Класс не наследует другие классы.

**Атрибуты**:
    - `app`: Экземпляр `Flask`-приложения.
    - `use_auto_proxy`: Логическая переменная, указывающая, использовать ли автоматический прокси.
    - `routes`: Словарь, содержащий информацию о маршрутах API, включая функции обработки и HTTP-методы.

**Методы**:
    - `__init__(self, app, config: dict) -> None`: Инициализирует экземпляр класса. Принимает `Flask`-приложение и 
      конфигурационный словарь. Запускает поток для обновления прокси (если `use_auto_proxy` установлен в `True`).
    - `_conversation()`: Обрабатывает запросы к `/backend-api/v2/conversation`. Извлекает информацию из 
      запроса, строит контекст для модели ChatGPT, отправляет запрос и возвращает ответ в формате потока.

## Функции

### `build_messages`

**Назначение**: Функция `build_messages` формирует контекст для модели ChatGPT, собирая информацию из 
запроса и создавая список сообщений для отправки модели.

**Параметры**:
    - `jailbreak`: Строка, указывающая режим работы модели (например, "Default", "Bard").

**Возвращает**:
    - `list`: Список сообщений, которые будут отправлены модели ChatGPT.

**Как работает функция**:
    - Извлекает информацию из запроса, включая контекст разговора, настройки доступа к 
      интернету, запрос пользователя.
    - Собирает системное сообщение, включающее информацию о дате, языке ответа, 
      специальных инструкциях (если они есть).
    - Добавляет сообщения из существующего контекста разговора.
    - Добавляет результаты веб-поиска (если доступ к интернету включен).
    - Добавляет инструкции для "Jailbreak", если режим "Jailbreak" активирован.
    - Добавляет запрос пользователя.
    - Ограничивает количество сообщений в контексте (не более 13) для избежания 
      ошибок в количестве токенов API.

**Примеры**:
    ```python
    >>> build_messages("Default")
    [{'role': 'system', 'content': 'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. Strictly follow the users instructions. Current date: 2023-10-27. You will respond in the language: en. '}, {'role': 'user', 'content': 'Hello, world!'}]

    >>> build_messages("Bard")
    [{'role': 'system', 'content': 'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. Strictly follow the users instructions. Current date: 2023-10-27. You will respond in the language: en. '}, {'role': 'user', 'content': 'Hello, world!'}, {'role': 'system', 'content': 'ACT:Bard'}]
    ```

### `fetch_search_results`

**Назначение**: Функция `fetch_search_results` извлекает результаты веб-поиска по 
запросу пользователя.

**Параметры**:
    - `query`: Строка, содержащая текст запроса.

**Возвращает**:
    - `list`: Список результатов веб-поиска в формате, подходящем для отправки 
      модели ChatGPT.

**Как работает функция**:
    - Делает запрос к API DuckDuckGo (через `ddg-api.herokuapp.com`) для получения 
      результатов поиска.
    - Формирует список сообщений, содержащих ссылки на найденные ресурсы 
      и их краткие описания.

**Примеры**:
    ```python
    >>> fetch_search_results("What is the capital of France?")
    [{'role': 'system', 'content': '[1] "Paris is the capital and most populous city of France.  ...  As of 2022, it is estimated to have a population of 2,175,601 ... " URL:https://en.wikipedia.org/wiki/Paris. [2] "Paris is the capital and most populous city of France, with an estimated population of 2,175,601 residents in 2022.  ...  The city is situated on the Seine river, in the Ile-de-France region, and is the centre and heart of ... " URL:https://www.britannica.com/place/Paris. [3] "Paris is the capital and most populous city of France, as well as one of the world's leading ... " URL:https://www.tripadvisor.com/Tourism-g187147-Paris-Vacations. [4] "Paris, the capital of France, is one of the most popular tourist destinations in the world.  ...  Known for its iconic landmarks such as the Eiffel Tower and the Louvre Museum ... " URL:https://www.lonelyplanet.com/france/paris. [5] "Paris, the capital of France, is a bustling metropolis famous for its art, fashion, and food. ... " URL:https://www.timeout.com/paris.'}]
    ```

### `generate_stream`

**Назначение**: Функция `generate_stream` обрабатывает ответ модели ChatGPT и 
возвращает его в формате потока.

**Параметры**:
    - `response`: Ответ модели ChatGPT.
    - `jailbreak`: Строка, указывающая режим работы модели (например, "Default", "Bard").

**Возвращает**:
    - `generator`: Генератор, возвращающий части ответа модели ChatGPT.

**Как работает функция**:
    - Проверяет, активирован ли режим "Jailbreak".
    - Если да, то ищет в ответе модели маркеры "ACT:" и "GPT:". 
      Если маркеры найдены, то возвращает ответ модели в обычном режиме. 
      Если маркеры не найдены, то возвращает пустой ответ.
    - Если режим "Jailbreak" не активирован, то возвращает ответ модели 
      в обычном режиме.

**Примеры**:
    ```python
    >>> generate_stream([{'role': 'assistant', 'content': 'Hello, world!'}] "Default")
    <generator object generate_stream at 0x7f8a23453b20>
    ```

### `response_jailbroken_success`

**Назначение**: Функция `response_jailbroken_success` проверяет, успешно ли 
выполнен "Jailbreak" для модели ChatGPT.

**Параметры**:
    - `response`: Ответ модели ChatGPT.

**Возвращает**:
    - `bool`: `True`, если "Jailbreak" успешно выполнен, иначе `False`.

**Как работает функция**:
    - Ищет в ответе модели маркер "ACT:". 
    - Если маркер найден, то возвращает `True`, иначе `False`.

**Примеры**:
    ```python
    >>> response_jailbroken_success("ACT: Bard")
    True
    ```

### `response_jailbroken_failed`

**Назначение**: Функция `response_jailbroken_failed` проверяет, произошла ли ошибка 
при выполнении "Jailbreak" для модели ChatGPT.

**Параметры**:
    - `response`: Ответ модели ChatGPT.

**Возвращает**:
    - `bool`: `True`, если произошла ошибка, иначе `False`.

**Как работает функция**:
    - Проверяет, начинается ли ответ модели с "GPT:" или "ACT:". 
    - Если да, то возвращает `False`, иначе `True`.

**Примеры**:
    ```python
    >>> response_jailbroken_failed("GPT: Bard")
    False
    ```

### `set_response_language`

**Назначение**: Функция `set_response_language` определяет язык запроса пользователя 
и возвращает сообщение, указывающее язык ответа модели ChatGPT.

**Параметры**:
    - `prompt`: Словарь, содержащий текст запроса пользователя.

**Возвращает**:
    - `str`: Сообщение с указанием языка ответа.

**Как работает функция**:
    - Использует `googletrans` для определения языка текста запроса.
    - Формирует сообщение с указанием языка ответа.

**Примеры**:
    ```python
    >>> set_response_language({'content': 'Hello, world!'})
    'You will respond in the language: en. '
    ```

### `isJailbreak`

**Назначение**: Функция `isJailbreak` проверяет, активирован ли режим "Jailbreak" для 
модели ChatGPT.

**Параметры**:
    - `jailbreak`: Строка, указывающая режим работы модели.

**Возвращает**:
    - `list | None`: Список специальных инструкций для "Jailbreak" 
      (если режим активирован), иначе `None`.

**Как работает функция**:
    - Проверяет, не является ли значение `jailbreak` равным "Default".
    - Если нет, то извлекает инструкции из словаря `special_instructions` 
      (если они есть). 
    - Если режим "Jailbreak" не активирован, то возвращает `None`.

**Примеры**:
    ```python
    >>> isJailbreak("Default")
    None
    ```