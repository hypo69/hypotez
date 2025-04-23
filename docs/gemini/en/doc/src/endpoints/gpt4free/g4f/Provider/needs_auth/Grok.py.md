# Модуль `Grok.py`

## Обзор

Модуль `Grok.py` предоставляет асинхронный интерфейс для взаимодействия с Grok AI, включая поддержку аутентификации, создания бесед и генерации ответов. Он поддерживает модели Grok-3, Grok-3-thinking и Grok-2.

## Более детально

Этот модуль содержит класс `Grok`, который наследуется от `AsyncAuthedProvider` и `ProviderModelMixin`. Он предназначен для обеспечения асинхронного взаимодействия с сервисом Grok AI. Класс `Grok` реализует методы для аутентификации, подготовки полезной нагрузки запроса и создания авторизованных сессий для обмена сообщениями. Модуль также включает класс `Conversation` для управления идентификаторами бесед.

## Классы

### `Conversation`

```python
class Conversation(JsonConversation):
    """Представляет беседу с Grok AI.

    Inherits:
        JsonConversation: Предоставляет базовую структуру для управления беседой в формате JSON.

    Attributes:
        conversation_id (str): Уникальный идентификатор беседы.
    """
```

### `Grok`

```python
class Grok(AsyncAuthedProvider, ProviderModelMixin):
    """Обеспечивает асинхронный интерфейс для взаимодействия с Grok AI.

    Inherits:
        AsyncAuthedProvider: Предоставляет механизмы для асинхронной аутентификации.
        ProviderModelMixin: Предоставляет общие методы для работы с моделями.

    Attributes:
        label (str): Метка провайдера ("Grok AI").
        url (str): URL сервиса Grok AI ("https://grok.com").
        cookie_domain (str): Домен для cookie (".grok.com").
        assets_url (str): URL для ресурсов ("https://assets.grok.com").
        conversation_url (str): URL для управления беседами ("https://grok.com/rest/app-chat/conversations").
        needs_auth (bool): Флаг, указывающий на необходимость аутентификации (True).
        working (bool): Флаг, указывающий на работоспособность провайдера (True).
        default_model (str): Модель, используемая по умолчанию ("grok-3").
        models (list): Список поддерживаемых моделей (["grok-3", "grok-3-thinking", "grok-2"]).
        model_aliases (dict): Псевдонимы моделей ({"grok-3-r1": "grok-3-thinking"}).
    """
```

## Методы класса `Grok`

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """Асинхронно аутентифицирует провайдера, используя cookie или запрашивая URL для входа.

        Args:
            cookies (Cookies, optional): Cookie для аутентификации. По умолчанию None.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.

        Yields:
            AuthResult: Результат аутентификации с cookie, proxy и заголовками.
            RequestLogin: Запрос на URL для входа, если cookie отсутствуют.
        """
```

### `_prepare_payload`

```python
    @classmethod
    async def _prepare_payload(cls, model: str, message: str) -> Dict[str, Any]:
        """Подготавливает полезную нагрузку (payload) для запроса к Grok AI.

        Args:
            model (str): Название модели, используемой для генерации ответа.
            message (str): Сообщение пользователя.

        Returns:
            Dict[str, Any]: Словарь с данными для отправки в запросе.
        """
```

### `create_authed`

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
        """Создает авторизованную сессию для взаимодействия с Grok AI и генерирует ответ.

        Args:
            model (str): Название модели, используемой для генерации ответа.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            cookies (Cookies, optional): Cookie для использования в сессии. По умолчанию None.
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект Conversation. По умолчанию False.
            conversation (Conversation, optional): Объект Conversation для продолжения существующей беседы. По умолчанию None.

        Yields:
            ImagePreview: Предварительный просмотр изображения.
            Reasoning: Промежуточные результаты размышлений модели.
            token: Части сгенерированного текста.
            ImageResponse: Сгенерированные изображения.
            TitleGeneration: Сгенерированный заголовок.
            Conversation: Объект Conversation, если `return_conversation` имеет значение True.
        """