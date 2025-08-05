# Модуль `Microsoft_Phi_4`

## Обзор

Модуль `Microsoft_Phi_4` предоставляет асинхронный интерфейс для взаимодействия с моделью Microsoft Phi-4 Multimodal, размещенной на платформе Hugging Face Spaces. Он позволяет генерировать текст на основе предоставленных сообщений и медиа-контента, используя API Hugging Face.

## Подробнее

Модуль обеспечивает возможность отправки текстовых и мультимедийных запросов к модели Microsoft Phi-4, а также получения потоковых ответов. Он включает в себя функции для форматирования запросов, обработки мультимедийных данных и управления сессиями.

## Классы

### `Microsoft_Phi_4`

**Описание**: Класс `Microsoft_Phi_4` является асинхронным провайдером, который реализует взаимодействие с моделью Microsoft Phi-4 Multimodal.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет миксин для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера - "Microsoft Phi-4".
- `space` (str): Имя пространства на Hugging Face - "microsoft/phi-4-multimodal".
- `url` (str): URL пространства на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, что провайдер в рабочем состоянии.
- `supports_stream` (bool): Указывает, что провайдер поддерживает потоковую передачу.
- `supports_system_message` (bool): Указывает, что провайдер поддерживает системные сообщения.
- `supports_message_history` (bool): Указывает, что провайдер поддерживает историю сообщений.
- `default_model` (str): Модель по умолчанию - "phi-4-multimodal".
- `default_vision_model` (str): Модель для обработки изображений по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `vision_models` (list): Список моделей для обработки изображений.
- `models` (list): Список поддерживаемых моделей.

**Принцип работы**:
Класс `Microsoft_Phi_4` использует асинхронные запросы для взаимодействия с API Hugging Face Spaces. Он предоставляет методы для отправки запросов с текстом и изображениями, а также для получения потоковых ответов. Класс также обрабатывает ошибки и исключения, которые могут возникнуть в процессе взаимодействия с API.

## Методы класса

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
        """ Функция выполняет HTTP-запросы к API Hugging Face Spaces для взаимодействия с моделью Microsoft Phi-4 Multimodal.

        Args:
            method (str): HTTP-метод для выполнения ("predict", "post" или "get").
            session (StreamSession): Асинхровая сессия для выполнения HTTP-запросов.
            prompt (str): Текстовый запрос для отправки в модель.
            conversation (JsonConversation): Объект, содержащий информацию о текущем сеансе разговора.
            media (list, optional): Список медиа-файлов (например, изображений) для отправки в модель. По умолчанию `None`.

        Returns:
            aiohttp.ClientResponse: Объект ответа от HTTP-запроса.

        Raises:
            ResponseError: Если возникает ошибка при выполнении HTTP-запроса.

        
        Функция `run` выполняет HTTP-запросы к API Hugging Face Spaces в зависимости от указанного метода.
        Если метод "predict", отправляется POST-запрос с текстовым запросом и медиа-файлами.
        Если метод "post", отправляется POST-запрос для добавления запроса в очередь.
        Если метод "get", отправляется GET-запрос для получения данных из очереди.
        В каждом случае, функция возвращает объект ответа от HTTP-запроса.

        Внутренние функции:
        - Отсутствуют

        Примеры:
        >>> # Пример вызова метода "predict"
        >>> response = Microsoft_Phi_4.run("predict", session, "Hello, world!", conversation, media=[...])
        >>> # Пример вызова метода "post"
        >>> response = Microsoft_Phi_4.run("post", session, "Hello, world!", conversation, media=[...])
        >>> # Пример вызова метода "get"
        >>> response = Microsoft_Phi_4.run("get", session, "Hello, world!", conversation)
        """
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType = None,
        prompt: str = None,
        proxy: str = None,
        cookies: Cookies = None,
        api_key: str = None,
        zerogpu_uuid: str = "[object Object]",
        return_conversation: bool = False,
        conversation: JsonConversation = None,
        **kwargs
    ) -> AsyncResult:
        """ Асинхронно создает генератор для взаимодействия с моделью Microsoft Phi-4 Multimodal.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки в модель.
            media (MediaListType, optional): Список медиа-файлов для отправки в модель. По умолчанию `None`.
            prompt (str, optional): Текстовый запрос для отправки в модель. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
            cookies (Cookies, optional): Cookie для отправки с запросами. По умолчанию `None`.
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг, указывающий, следует ли возвращать объект `conversation`. По умолчанию `False`.
            conversation (JsonConversation, optional): Объект, содержащий информацию о текущем сеансе разговора. По умолчанию `None`.
            **kwargs: Дополнительные аргументы для передачи в модель.

        Yields:
            str: Части ответа от модели в потоковом режиме.
            JsonConversation: Объект `JsonConversation`, если `return_conversation` установлен в `True`.

        Raises:
            ResponseError: Если возникает ошибка при взаимодействии с API.

        
        Функция `create_async_generator` создает асинхронный генератор для взаимодействия с моделью Microsoft Phi-4 Multimodal.
        Сначала она форматирует запрос на основе предоставленных сообщений и медиа-контента.
        Затем она устанавливает сессию и получает токен ZeroGPU, если он не предоставлен.
        После этого она загружает медиа-файлы на сервер, если они есть.
        Наконец, она отправляет запросы к API и получает потоковые ответы, которые возвращаются через генератор.

        Внутренние функции:
        - Отсутствуют

        Примеры:
        >>> async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", messages=[...], media=[...]):
        ...     print(response)
        """