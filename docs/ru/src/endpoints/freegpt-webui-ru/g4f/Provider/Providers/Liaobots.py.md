# Модуль для работы с провайдером Liaobots
## Обзор

Модуль предназначен для взаимодействия с провайдером Liaobots. Он определяет параметры подключения, поддерживаемые модели, и функцию для создания запросов к API.

## Подробней

Модуль `Liaobots.py` используется для отправки запросов к сервису Liaobots, который предоставляет доступ к моделям GPT-3.5 и GPT-4. Он содержит информацию о URL, поддерживаемых моделях, необходимости аутентификации и другие параметры, необходимые для взаимодействия с API Liaobots.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к API Liaobots и возвращает ответ в виде потока токенов.

    Args:
        model (str): Идентификатор модели, которую нужно использовать (например, 'gpt-3.5-turbo', 'gpt-4').
        messages (list): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами 'role' и 'content'.
        stream (bool): Определяет, нужно ли возвращать ответ в виде потока.
        **kwargs: Дополнительные аргументы, такие как ключ аутентификации.

    Returns:
        Generator[str, None, None]: Генератор токенов, полученных из API.

    Raises:
        Exception: Если происходит ошибка при отправке запроса или обработке ответа.

    Пример использования:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, world!'}]
        >>> stream = True
        >>> kwargs = {'auth': 'your_auth_key'}
        >>> for token in _create_completion(model, messages, stream, **kwargs):
        ...     print(token, end='')
        Привет, мир!
    """
```

**Как работает функция**:

1.  **Подготовка заголовков**: Функция создает заголовки HTTP-запроса, включая `authority`, `content-type`, `origin`, `referer`, `user-agent` и `x-auth-code`. Значение `x-auth-code` берется из аргумента `kwargs` с ключом `'auth'`.
2.  **Формирование данных JSON**: Функция формирует данные JSON для отправки в API, включая `conversationId` (случайный UUID), `model` (информация о модели из словаря `models`), `messages` (список сообщений), `key` (пустая строка) и `prompt` (инструкция для модели).
3.  **Отправка POST-запроса**: Функция отправляет POST-запрос к API `https://liaobots.com/api/chat` с указанными заголовками и данными JSON. Устанавливается параметр `stream=True` для получения ответа в виде потока.
4.  **Обработка потока токенов**: Функция итерируется по содержимому ответа, полученному от API, с размером чанка 2046 байт. Каждый чанк декодируется в кодировке UTF-8 и возвращается как токен.

**ASCII Flowchart**:

```
    Начало
     |
     V
  Создание заголовков HTTP-запроса
     |
     V
  Формирование данных JSON для запроса
     |
     V
  Отправка POST-запроса к API
     |
     V
  Итерация по содержимому ответа (токены)
     |
     V
  Декодирование токена в UTF-8
     |
     V
  Возврат токена
     |
     V
    Конец
```

**Примеры**:

```python
model = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Hello, world!'}]
stream = True
kwargs = {'auth': 'your_auth_key'}

for token in _create_completion(model, messages, stream, **kwargs):
    print(token, end='')
```
```python
model = 'gpt-4'
messages = [{'role': 'user', 'content': 'Напиши стихотворение.'}]
stream = True
kwargs = {'auth': 'your_auth_key'}

for token in _create_completion(model, messages, stream, **kwargs):
    print(token, end='')
```
```python
model = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Как дела?'}]
stream = True
kwargs = {'auth': 'your_auth_key'}

for token in _create_completion(model, messages, stream, **kwargs):
    print(token, end='')
```
```python
model = 'gpt-4'
messages = [{'role': 'user', 'content': 'Translate to russian: Hello, world!'}]
stream = True
kwargs = {'auth': 'your_auth_key'}

for token in _create_completion(model, messages, stream, **kwargs):
    print(token, end='')
```

## Переменные

-   `url` (str): URL API Liaobots (`https://liaobots.com`).
-   `model` (list): Список поддерживаемых моделей (`['gpt-3.5-turbo', 'gpt-4']`).
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (`True`).
-   `needs_auth` (bool): Указывает, требуется ли аутентификация (`True`).
-   `models` (dict): словарь с информацией о моделях `gpt-4` и `gpt-3.5-turbo`.
    -   `id` (str): идентификатор модели.
    -   `name` (str): отображаемое имя модели.
    -   `maxLength` (int): максимальная длина.
    -   `tokenLimit` (int): лимит токенов.
-   `params` (str): строка, содержащая информацию о поддержке типов данных функцией `_create_completion`.