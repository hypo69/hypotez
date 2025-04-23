# Модуль `Aichat.py`

## Обзор

Модуль `Aichat.py` предоставляет асинхронный провайдер для взаимодействия с сервисом `chat-gpt.org`. Он позволяет отправлять сообщения и получать ответы, используя cookies для аутентификации. Модуль поддерживает модель `gpt-3.5-turbo`.

## Подробнее

Этот модуль предназначен для интеграции с сервисом `chat-gpt.org` через асинхронные запросы. Он использует cookies для аутентификации и поддерживает настройку параметров, таких как температура и top_p. Важно отметить, что для работы модуля требуются актуальные cookies, полученные с сайта `chat-gpt.org`.

## Классы

### `Aichat`

**Описание**: Класс `Aichat` является асинхронным провайдером для `chat-gpt.org`.

**Наследует**:
- `AsyncProvider`: базовый класс для асинхронных провайдеров.

**Атрибуты**:
- `url` (str): URL адрес сервиса `chat-gpt.org`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.

**Принцип работы**:
Класс `Aichat` использует асинхронные запросы для взаимодействия с `chat-gpt.org`. Он получает cookies для аутентификации, формирует JSON-запрос с сообщением и параметрами, отправляет запрос и обрабатывает ответ. В случае ошибки выбрасывает исключение.

## Методы класса

### `create_async`

```python
    @staticmethod
    async def create_async(
        model: str,
        messages: Messages,
        proxy: str = None, **kwargs) -> str:
        """Асинхронно отправляет сообщение и возвращает ответ от chat-gpt.org.

        Args:
            model (str): Модель, используемая для генерации ответа.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы, такие как cookies, temperature, top_p и т.д.

        Returns:
            str: Ответ от `chat-gpt.org`.

        Raises:
            RuntimeError: Если не удалось получить cookies.
            Exception: Если получен ошибочный ответ от сервера.

        Пример:
            >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
            >>> Aichat.create_async(model="gpt-3.5-turbo", messages=messages, cookies={"cookie_name": "cookie_value"})
            "I am doing well, thank you for asking!"
        """
```

**Параметры**:
- `model` (str): Модель, используемая для генерации ответа.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `cookies`, `temperature`, `top_p` и т.д.

**Как работает функция**:
1. Функция `create_async` асинхронно отправляет сообщение и возвращает ответ от `chat-gpt.org`.
2. Сначала функция пытается получить cookies. Если cookies не переданы в `kwargs`, то функция вызывает `get_cookies('chat-gpt.org')`.
3. Если cookies не получены, выбрасывается исключение `RuntimeError`.
4. Формируются заголовки запроса, включая User-Agent и Referer.
5. Создается асинхронная сессия с использованием `StreamSession`.
6. Формируется JSON-данные для отправки, включая сообщение, температуру, top_p и другие параметры.
7. Отправляется POST-запрос на `https://chat-gpt.org/api/text` с JSON-данными.
8. Обрабатывается ответ от сервера. Если ответ содержит ошибку, выбрасывается исключение `Exception`.
9. Возвращается сообщение из ответа.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
Aichat.create_async(model="gpt-3.5-turbo", messages=messages, cookies={"cookie_name": "cookie_value"})
```
```python
messages = [{"role": "user", "content": "Как дела?"}]
Aichat.create_async(model="gpt-3.5-turbo", messages=messages, cookies={"cookie_name": "cookie_value"})
```