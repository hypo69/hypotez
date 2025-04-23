# Модуль `Grok.py`

## Обзор

Модуль предоставляет класс `Grok`, который является асинхронным аутентифицированным провайдером для взаимодействия с Grok AI. Он поддерживает работу с различными моделями Grok AI, аутентификацию через cookies или логин, создание новых бесед и получение ответов в реальном времени.

## Подробней

Этот модуль позволяет интегрировать взаимодействие с Grok AI в проект `hypotez`. Он обеспечивает аутентификацию, подготовку запросов и обработку ответов от Grok AI.

## Классы

### `Conversation`

**Описание**: Представляет собой класс для хранения информации о беседе с Grok AI.
**Атрибуты**:
- `conversation_id` (str): Идентификатор беседы.

```python
class Conversation(JsonConversation):
    """
    Класс для представления беседы с Grok AI.

    Args:
        conversation_id (str): Уникальный идентификатор беседы.
    """
    def __init__(self, conversation_id: str) -> None:
        """
        Конструктор класса Conversation.

        Args:
            conversation_id (str): Уникальный идентификатор беседы.
        """
        self.conversation_id = conversation_id
```

### `Grok`

**Описание**: Класс, реализующий асинхронного аутентифицированного провайдера для Grok AI.
**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`
**Атрибуты**:
- `label` (str): Метка провайдера ("Grok AI").
- `url` (str): URL главной страницы Grok AI ("https://grok.com").
- `cookie_domain` (str): Домен для cookies (".grok.com").
- `assets_url` (str): URL для статических ресурсов ("https://assets.grok.com").
- `conversation_url` (str): URL для управления беседами ("https://grok.com/rest/app-chat/conversations").
- `needs_auth` (bool): Требуется ли аутентификация (True).
- `working` (bool): Работоспособность провайдера (True).
- `default_model` (str): Модель по умолчанию ("grok-3").
- `models` (list): Список поддерживаемых моделей (["grok-3", "grok-3-thinking", "grok-2"]).
- `model_aliases` (dict): Псевдонимы моделей ({"grok-3-r1": "grok-3-thinking"}).

```python
class Grok(AsyncAuthedProvider, ProviderModelMixin):
    """
    Асинхронный аутентифицированный провайдер для Grok AI.

    Inherits:
        AsyncAuthedProvider: Базовый класс для асинхронных провайдеров с аутентификацией.
        ProviderModelMixin: Миксин для работы с моделями.

    Attributes:
        label (str): Метка провайдера ("Grok AI").
        url (str): URL главной страницы Grok AI ("https://grok.com").
        cookie_domain (str): Домен для cookies (".grok.com").
        assets_url (str): URL для статических ресурсов ("https://assets.grok.com").
        conversation_url (str): URL для управления беседами ("https://grok.com/rest/app-chat/conversations").
        needs_auth (bool): Требуется ли аутентификация (True).
        working (bool): Работоспособность провайдера (True).
        default_model (str): Модель по умолчанию ("grok-3").
        models (list): Список поддерживаемых моделей (["grok-3", "grok-3-thinking", "grok-2"]).
        model_aliases (dict): Псевдонимы моделей ({"grok-3-r1": "grok-3-thinking"}).
    """
```

## Методы класса

### `on_auth_async`

**Назначение**: Асинхронно аутентифицирует пользователя с использованием cookies или логина.
**Параметры**:
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.
**Возвращает**:
- `AsyncIterator`: Асинхронный итератор, возвращающий результаты аутентификации (`AuthResult`) или запрос на логин (`RequestLogin`).
**Как работает функция**:

1.  Проверяется наличие cookies. Если `cookies` не переданы, пытается получить их, используя `cookie_domain`.
2.  Если `cookies` найдены и содержат "sso", возвращает `AuthResult` с этими `cookies`, указывая на необходимость "impersonate" как "chrome", и `DEFAULT_HEADERS`.
3.  Если `cookies` отсутствуют или не содержат "sso", возвращает `RequestLogin`, запрашивая URL для логина из переменной окружения `G4F_LOGIN_URL` или пустой строки.
4.  После запроса на логин возвращает `AuthResult` с аргументами, полученными из веб-драйвера, ожидая появления элемента `[href="/chat#private"]`.
**Примеры**:

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Асинхронно аутентифицирует пользователя с использованием cookies или логина.

        Args:
            cookies (Cookies, optional): Cookies для аутентификации. Defaults to None.
            proxy (str, optional): Прокси-сервер для использования. Defaults to None.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncIterator: Асинхронный итератор, возвращающий результаты аутентификации (AuthResult) или запрос на логин (RequestLogin).
        """
```

### `_prepare_payload`

**Назначение**: Подготавливает полезную нагрузку (payload) для запроса к Grok AI.
**Параметры**:
- `model` (str): Название модели Grok AI.
- `message` (str): Сообщение пользователя.
**Возвращает**:
- `Dict[str, Any]`: Словарь с данными payload для запроса.
**Как работает функция**:

1.  Определяет, какую модель использовать (grok-latest для "grok-2" или "grok-3" для других).
2.  Создает словарь с параметрами запроса, такими как сообщение, вложения файлов и изображений, флаги для отключения поиска, включения генерации изображений и т.д.
3.  Устанавливает флаг `isReasoning` в зависимости от того, заканчивается ли название модели на "-thinking" или "-r1".
**Примеры**:

```python
    @classmethod
    async def _prepare_payload(cls, model: str, message: str) -> Dict[str, Any]:
        """
        Подготавливает payload для запроса к Grok AI.

        Args:
            model (str): Название модели Grok AI.
            message (str): Сообщение пользователя.

        Returns:
            Dict[str, Any]: Словарь с данными payload для запроса.
        """
```

### `create_authed`

**Назначение**: Создает аутентифицированный запрос к Grok AI для получения ответа.
**Параметры**:
- `model` (str): Название модели Grok AI.
- `messages` (Messages): Список сообщений для отправки.
- `auth_result` (AuthResult): Результат аутентификации.
- `cookies` (Cookies, optional): Cookies для запроса. По умолчанию `None`.
- `return_conversation` (bool, optional): Возвращать ли объект Conversation. По умолчанию `False`.
- `conversation` (Conversation, optional): Объект Conversation для продолжения беседы. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.
**Возвращает**:
- `AsyncResult`: Асинхронный итератор, возвращающий результаты ответа, включая текст, изображения и метаданные.
**Как работает функция**:

1.  Определяет `conversation_id` из объекта `conversation`, если он предоставлен.
2.  Форматирует запрос с использованием `format_prompt` или `get_last_user_message` в зависимости от наличия `conversation_id`.
3.  Использует `StreamSession` для выполнения POST-запроса к Grok AI.
4.  Подготавливает `payload` с помощью `_prepare_payload`.
5.  Отправляет запрос на новый разговор (если `conversation_id` отсутствует) или на продолжение существующего.
6.  Обрабатывает ответ построчно, извлекая данные о тексте, изображениях, статусе "размышления" и метаданных.
7.  Возвращает объекты `ImagePreview`, `Reasoning`, текст, `ImageResponse` и `TitleGeneration` по мере их поступления.
8.  Если `return_conversation` установлен в `True`, возвращает объект `Conversation` с `conversation_id` в конце итерации.
**Примеры**:

```python
    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        cookies: Cookies = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает аутентифицированный запрос к Grok AI для получения ответа.

        Args:
            model (str): Название модели Grok AI.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            cookies (Cookies, optional): Cookies для запроса. Defaults to None.
            return_conversation (bool, optional): Возвращать ли объект Conversation. Defaults to False.
            conversation (Conversation, optional): Объект Conversation для продолжения беседы. Defaults to None.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Асинхронный итератор, возвращающий результаты ответа, включая текст, изображения и метаданные.
        """
```
```markdown
## Внутренние функции

Внутри методов классов `Grok` используются внутренние функции, которые помогают реализовать логику работы с Grok AI.

### В классе `Grok` -> `create_authed` -> `response.iter_lines()` ->  `json.loads(line)`

**Назначение**:  Преобразует строку JSON в объект Python.
**Как работает функция**:

Принимает строку `line`, содержащую JSON-данные, и пытается преобразовать её в Python-словарь.
**Примеры**:
Предположим, `line` содержит строку `'{"key": "value"}'`. В этом случае функция вернет словарь `{"key": "value"}`.
```python
    try:
        json_data = json.loads(line)
```

## Параметры класса

- `label` (str): Метка провайдера ("Grok AI").
- `url` (str): URL главной страницы Grok AI ("https://grok.com").
- `cookie_domain` (str): Домен для cookies (".grok.com").
- `assets_url` (str): URL для статических ресурсов ("https://assets.grok.com").
- `conversation_url` (str): URL для управления беседами ("https://grok.com/rest/app-chat/conversations").
- `needs_auth` (bool): Требуется ли аутентификация (True).
- `working` (bool): Работоспособность провайдера (True).
- `default_model` (str): Модель по умолчанию ("grok-3").
- `models` (list): Список поддерживаемых моделей (\["grok-3", "grok-3-thinking", "grok-2"]).
- `model_aliases` (dict): Псевдонимы моделей ({"grok-3-r1": "grok-3-thinking"}).

## Примеры

Пример аутентификации и создания запроса:

```python
#  Пример использования можно посмотреть в тестах.