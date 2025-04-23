# Модуль `CohereForAI_C4AI_Command.py`

## Обзор

Модуль предоставляет класс `CohereForAI_C4AI_Command`, который является асинхронным генератором для взаимодействия с моделями CohereForAI C4AI Command. Он позволяет вести диалоги, генерировать заголовки и обрабатывать ответы от API.

## Подробнее

Модуль предназначен для интеграции с моделями CohereForAI для обработки и генерации текста. Он использует `aiohttp` для асинхронных HTTP-запросов, `FormData` для отправки данных и `JsonConversation` для управления состоянием диалога.

## Классы

### `CohereForAI_C4AI_Command`

**Описание**: Класс предоставляет функциональность асинхронного взаимодействия с моделями CohereForAI C4AI Command.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("CohereForAI C4AI Command").
- `url` (str): URL API ("https://cohereforai-c4ai-command.hf.space").
- `conversation_url` (str): URL для ведения диалогов (`f"{url}/conversation"`).
- `working` (bool): Указывает, что провайдер работает (True).
- `default_model` (str): Модель по умолчанию ("command-a-03-2025").
- `model_aliases` (dict): Псевдонимы моделей (например, `"command-a": default_model`).
- `models` (list): Список доступных моделей.

**Принцип работы**:
Класс использует асинхронные запросы к API CohereForAI для отправки и получения данных. Он поддерживает ведение диалогов, генерацию заголовков и обработку ошибок.
Состояние диалога сохраняется в объекте `JsonConversation`, который содержит информацию о cookies, идентификаторе диалога и других параметрах.

## Методы класса

### `get_model`

```python
@classmethod
def get_model(cls, model: str, **kwargs) -> str:
    """ Функция возвращает модель, если она есть в псевдонимах, или вызывает родительский метод.

    Args:
        model (str): Имя модели.
        **kwargs: Дополнительные параметры.

    Returns:
        str: Имя модели.
    """
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, model: str, messages: Messages,
        api_key: str = None, 
        proxy: str = None,
        conversation: JsonConversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        """ Функция создает асинхронный генератор для взаимодействия с API.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер. По умолчанию `None`.
            conversation (JsonConversation, optional): Объект диалога. По умолчанию `None`.
            return_conversation (bool, optional): Возвращать ли объект диалога. По умолчанию `False`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор.

        Raises:
            RuntimeError: Если не удалось прочитать ответ или произошла ошибка на сервере.

        **Внутренние функции**:
        Внутри данной функции нету внутренних функций
        
        **Как работает функция**:
        - Функция принимает имя модели, список сообщений и опциональные параметры (API-ключ, прокси, объект диалога).
        - Функция извлекает модель с помощью `cls.get_model(model)`.
        - Функция подготавливает заголовки для HTTP-запроса, включая Origin, User-Agent и Accept.
        - Если предоставлен API-ключ, он добавляется в заголовок Authorization.
        - Функция создает асинхронную сессию с помощью `ClientSession`.
        - Функция определяет системный промпт, объединяя содержимое сообщений с ролью "system".
        - Функция форматирует промпт, если диалог отсутствует, иначе извлекает последнее сообщение пользователя.
        - Если диалог отсутствует или модель или системный промпт отличаются от текущих, функция создает новый диалог, отправляя POST-запрос к `cls.conversation_url`.
        - Функция извлекает идентификатор сообщения из ответа сервера.
        - Функция подготавливает данные для отправки в формате FormData, включая входные данные, идентификатор сообщения и флаги.
        - Функция отправляет POST-запрос к `f"{cls.conversation_url}/{conversation.conversationId}"` с данными FormData.
        - Функция обрабатывает чанки ответа, преобразуя их в JSON.
        - Если тип чанка "stream", функция извлекает токен и возвращает его.
        - Если тип чанка "title", функция извлекает заголовок и возвращает его.
        - Если тип чанка "finalAnswer", функция завершает генерацию.
        - Функция обрабатывает возможные ошибки, такие как `json.JSONDecodeError` и `RuntimeError`.

        Example:
            ```python
            messages = [{"role": "user", "content": "Hello, how are you?"}]
            async for chunk in CohereForAI_C4AI_Command.create_async_generator(model="command-a", messages=messages):
                print(chunk)
            ```
        """