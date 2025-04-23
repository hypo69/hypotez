# Документация для модуля `Aichat`

## Обзор

Модуль `Aichat` предназначен для асинхронного взаимодействия с провайдером `chat-gpt.org` для генерации текста на основе предоставленных сообщений. Он использует `StreamSession` для выполнения HTTP-запросов и обрабатывает полученные ответы в формате JSON. Модуль поддерживает модель `gpt-3.5-turbo` и требует наличия cookies для работы.

## Подробнее

Модуль `Aichat` является частью системы `gpt4free` и предоставляет возможность взаимодействия с сервисом `chat-gpt.org`. Он отправляет запросы к API этого сервиса и возвращает сгенерированный текст. Для работы требуется наличие cookies, которые можно получить, посетив сайт `chat-gpt.org` в браузере Chrome.

## Классы

### `Aichat`

**Описание**: Класс `Aichat` представляет собой асинхронного провайдера для взаимодействия с `chat-gpt.org`.

**Наследует**:
- `AsyncProvider`: Асинхронный базовый класс провайдера.

**Атрибуты**:
- `url` (str): URL-адрес сервиса `chat-gpt.org`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживается ли модель `gpt-3.5-turbo`.

## Методы

### `create_async`

```python
    @staticmethod
    async def create_async(
        model: str,
        messages: Messages,
        proxy: str = None, **kwargs) -> str:
```

**Назначение**: Асинхронно создает запрос к `chat-gpt.org` и возвращает сгенерированный текст.

**Параметры**:
- `model` (str): Идентификатор используемой модели.
- `messages` (Messages): Список сообщений, используемых для генерации текста.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `cookies`, `temperature` и `top_p`.

**Возвращает**:
- `str`: Сгенерированный текст.

**Вызывает исключения**:
- `RuntimeError`: Если cookies не предоставлены.
- `Exception`: Если получен ошибочный ответ от сервера.

**Как работает функция**:
1. **Извлекает cookies**: Функция пытается извлечь cookies из аргументов `kwargs`. Если cookies не предоставлены, она пытается получить их с сайта `chat-gpt.org`.
2. **Формирует заголовки**: Функция создает заголовки HTTP-запроса, включая `User-Agent`, `Content-Type` и другие необходимые параметры.
3. **Создает сессию**: Функция создает асинхронную сессию с использованием `StreamSession`, передавая заголовки, cookies, прокси и параметры таймаута.
4. **Формирует JSON-данные**: Функция формирует JSON-данные для отправки в запросе, включая сообщения, температуру, `top_p` и другие параметры.
5. **Отправляет запрос**: Функция отправляет POST-запрос к API `chat-gpt.org` с JSON-данными.
6. **Обрабатывает ответ**: Функция обрабатывает полученный ответ, проверяет статус и извлекает сгенерированный текст из JSON-ответа.
7. **Обрабатывает ошибки**: Если получен ошибочный ответ или cookies не предоставлены, функция вызывает исключение.

**Примеры**:

```python
# Пример вызова функции create_async с cookies и прокси
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
proxy = "http://your_proxy:8080"
cookies = {"cookie_name": "cookie_value"}
try:
    result = await Aichat.create_async(model, messages, proxy=proxy, cookies=cookies, temperature=0.7, top_p=0.9)
    print(result)
except Exception as ex:
    logger.error(f"Ошибка при вызове Aichat.create_async: {ex}", ex, exc_info=True)

# Пример вызова функции create_async без прокси
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Как дела?"}]
try:
    result = await Aichat.create_async(model, messages, cookies=cookies)
    print(result)
except Exception as ex:
    logger.error(f"Ошибка при вызове Aichat.create_async: {ex}", ex, exc_info=True)