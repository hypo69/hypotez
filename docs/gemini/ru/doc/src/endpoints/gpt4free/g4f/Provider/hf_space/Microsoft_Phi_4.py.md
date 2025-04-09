# Модуль Microsoft_Phi_4

## Обзор

Модуль `Microsoft_Phi_4` предназначен для взаимодействия с моделью Microsoft Phi-4 Multimodal через Hugging Face Spaces. Он предоставляет асинхронный генератор для получения ответов от модели, поддерживает потоковую передачу данных, системные сообщения и историю сообщений. Модуль также обеспечивает работу с изображениями.

## Подробней

Модуль использует Hugging Face Spaces для доступа к модели Microsoft Phi-4 Multimodal. Он поддерживает текстовые и визуальные запросы, а также загрузку и обработку изображений. Для аутентификации используется токен `zerogpu_token`.

## Классы

### `Microsoft_Phi_4`

**Описание**: Класс `Microsoft_Phi_4` является асинхронным провайдером и миксином для работы с моделью Microsoft Phi-4 Multimodal.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:

- `label` (str): Метка провайдера (Microsoft Phi-4).
- `space` (str): Название пространства Hugging Face (microsoft/phi-4-multimodal).
- `url` (str): URL пространства Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий, что провайдер работает.
- `supports_stream` (bool): Флаг, указывающий, что провайдер поддерживает потоковую передачу.
- `supports_system_message` (bool): Флаг, указывающий, что провайдер поддерживает системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, что провайдер поддерживает историю сообщений.
- `default_model` (str): Модель по умолчанию (phi-4-multimodal).
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию.
- `model_aliases` (dict): Алиасы моделей.
- `vision_models` (list): Список моделей для работы с изображениями.
- `models` (list): Список поддерживаемых моделей.

**Методы**:

- `run`: Выполняет HTTP-запросы к API Hugging Face Space.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

## Функции

### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None):
        """ Выполняет HTTP-запросы к API Hugging Face Space.

        Args:
            method (str): HTTP-метод ("predict", "post" или "get").
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текстовый запрос.
            conversation (JsonConversation): Объект, содержащий информацию о сессии и токены.
            media (list, optional): Список медиафайлов (изображений). По умолчанию `None`.

        Returns:
            StreamResponse: Объект ответа от сервера.

        Как работает функция:
        1.  Формирует заголовки запроса, включая `content-type`, `x-zerogpu-token` и `x-zerogpu-uuid`.
        2.  В зависимости от значения `method` выполняет соответствующий HTTP-запрос (`POST` или `GET`) к API Hugging Face Space.
        3.  Формирует данные запроса в формате JSON, включая текстовый запрос (`prompt`) и медиафайлы (`media`).
        4.  Возвращает объект ответа от сервера.

        ```mermaid
        graph TD
        A[Начало] --> B{Выбор HTTP-метода};
        B -- predict --> C[Выполнение POST-запроса к /gradio_api/run/predict];
        B -- post --> D[Выполнение POST-запроса к /gradio_api/queue/join];
        B -- get --> E[Выполнение GET-запроса к /gradio_api/queue/data];
        C --> F[Возврат объекта ответа];
        D --> F;
        E --> F;
        ```

        Примеры:
            Запрос на предсказание:
            ```python
            response = Microsoft_Phi_4.run("predict", session, "Hello", conversation, [])
            ```

            Запрос на отправку данных:
            ```python
            response = Microsoft_Phi_4.run("post", session, "Hello", conversation, [])
            ```

            Запрос на получение данных:
            ```python
            response = Microsoft_Phi_4.run("get", session, "Hello", conversation)
            ```
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
        """ Создает асинхронный генератор для получения ответов от модели.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для формирования запроса.
            media (MediaListType, optional): Список медиафайлов (изображений). По умолчанию `None`.
            prompt (str, optional): Текстовый запрос. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            cookies (Cookies, optional): HTTP-куки. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект Conversation. По умолчанию `False`.
            conversation (JsonConversation, optional): Объект Conversation. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор для получения ответов от модели.

        Raises:
            ResponseError: Если возникает ошибка при получении ответа от сервера.

        Как работает функция:
        1.  Формирует текстовый запрос (`prompt`) на основе списка сообщений (`messages`).
        2.  Инициализирует UUID сессии (`session_hash`).
        3.  Получает токен `zerogpu_token` и API-ключ, если они не были предоставлены.
        4.  Создает или обновляет объект `JsonConversation`.
        5.  Загружает медиафайлы на сервер, если они предоставлены.
        6.  Выполняет последовательность HTTP-запросов (`predict`, `post`, `get`) к API Hugging Face Space.
        7.  Обрабатывает ответы от сервера, извлекая данные из JSON-ответа.
        8.  Генерирует ответы от модели в асинхронном режиме.

        ```mermaid
        graph TD
        A[Начало] --> B{Формирование запроса};
        B --> C{Инициализация UUID сессии};
        C --> D{Получение zerogpu_token и API-ключа};
        D --> E{Создание/обновление JsonConversation};
        E --> F{Загрузка медиафайлов (если есть)};
        F --> G{Выполнение запроса predict};
        G --> H{Выполнение запроса post};
        H --> I{Выполнение запроса get};
        I --> J{Обработка ответа};
        J --> K{Генерация ответа};
        K --> L[Конец];
        ```

        Примеры:
            Создание асинхронного генератора без медиафайлов:
            ```python
            async for response in Microsoft_Phi_4.create_async_generator(
                model="phi-4-multimodal",
                messages=[{"role": "user", "content": "Hello"}]
            ):
                print(response)
            ```

            Создание асинхронного генератора с медиафайлами:
            ```python
            async for response in Microsoft_Phi_4.create_async_generator(
                model="phi-4-multimodal",
                messages=[{"role": "user", "content": "Hello"}],
                media=[(b"...", "image.jpg")]
            ):
                print(response)
            ```
        """