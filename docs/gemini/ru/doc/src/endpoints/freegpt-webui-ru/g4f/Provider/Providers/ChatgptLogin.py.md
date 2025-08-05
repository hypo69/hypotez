# Модуль ChatgptLogin

## Обзор

Модуль `ChatgptLogin`  - это провайдер для использования модели `gpt-3.5-turbo` от OpenAI, реализующий бесплатный доступ к этой модели через веб-сайт `https://chatgptlogin.ac`. Модуль позволяет отправлять запросы к модели и получать ответы в текстовом формате.

## Подробней

Модуль использует библиотеку `requests` для отправки запросов к веб-сайту `https://chatgptlogin.ac`. Запросы  формируются  с помощью метода `_create_completion`, который принимает параметры: `model` (имя модели), `messages` (список сообщений), `stream` (флаг, указывающий, нужно ли использовать потоковую передачу данных) и дополнительные аргументы, передаваемые в метод  `_create_completion`  как ключевые слова. 

## Функции

### `_create_completion`

**Назначение**: Функция `_create_completion` отправляет запрос к модели `gpt-3.5-turbo` на веб-сайт `https://chatgptlogin.ac`.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (list): Список сообщений, которые будут отправлены модели.
- `stream` (bool): Флаг, указывающий, нужно ли использовать потоковую передачу данных.
- **kwargs**: Дополнительные аргументы, передаваемые в метод  `_create_completion`  как ключевые слова.

**Возвращает**:

- str: Ответ модели в текстовом формате.

**Вызывает исключения**:

- `requests.exceptions.RequestException`:  Если возникает ошибка при отправке запроса.

**Как работает**:

1.  Функция `_create_completion`  инициализирует  HTTP-запрос к веб-сайту `https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat`  с помощью библиотеки `requests`.
2.  Функция `_create_completion`  преобразовывает список сообщений  `messages`  в формат JSON, используя внутреннюю функцию  `transform`. 
3.  Функция  `_create_completion`  формирует  HTTP-заголовок  `headers`,  включая  `x-wp-nonce`,  который  получается  с  помощью  внутренней  функции  `get_nonce`.
4.  Функция  `_create_completion`  отправляет  HTTP-запрос  `POST`  на  веб-сайт  `https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat`  с  помощью  библиотеки  `requests`.
5.  Функция  `_create_completion`  анализирует  полученный  ответ  в  формате  JSON  и  извлекает  ответ  модели  `gpt-3.5-turbo`  из  ключа  `reply`.
6.  Функция  `_create_completion`  возвращает  ответ  модели  в  текстовом  формате.

**Внутренние функции**:

-  `get_nonce`:  Функция  `get_nonce`  извлекает  токен  `x-wp-nonce`  с  веб-сайта  `https://chatgptlogin.ac`.
-  `transform`:  Функция  `transform`  преобразовывает  список  сообщений  `messages`  в  формат  JSON,  сохраняя  информацию  о  роли  `role`,  текстовом  содержании  `content`  и  HTML-разметке  `html`.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
    {'role': 'assistant', 'content': 'У меня все отлично, а у тебя?'},
]

response = _create_completion(model='gpt-3.5-turbo', messages=messages)
print(response)
```

## Параметры модуля

- `url` (str): Базовый URL-адрес для отправки запросов.
- `model` (list): Список поддерживаемых моделей.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли модуль потоковую передачу данных.
- `needs_auth` (bool): Флаг, указывающий, требуется ли авторизация для использования модуля.

## Примеры

```python
# Пример использования:

# Список сообщений
messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
    {'role': 'assistant', 'content': 'У меня все отлично, а у тебя?'},
]

# Отправка запроса к модели
response = _create_completion(model='gpt-3.5-turbo', messages=messages)

# Вывод ответа модели
print(response)
```