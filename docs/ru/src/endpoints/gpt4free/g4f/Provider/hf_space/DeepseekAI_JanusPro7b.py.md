# Модуль DeepseekAI_JanusPro7b

## Обзор

Модуль `DeepseekAI_JanusPro7b` предоставляет асинхронный интерфейс для взаимодействия с моделью DeepseekAI Janus-Pro-7B, размещенной на Hugging Face Spaces. Он поддерживает генерацию текста и изображений, стриминг ответов и работу с историей сообщений.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, использующими AI-модели для обработки текста и изображений. Он использует асинхронные запросы для взаимодействия с API Hugging Face Spaces и предоставляет удобный интерфейс для отправки запросов и получения ответов в режиме реального времени.

## Классы

### `DeepseekAI_JanusPro7b`

**Описание**: Класс предоставляет методы для взаимодействия с моделью DeepseekAI Janus-Pro-7B.
**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Отображаемое имя провайдера - "DeepseekAI Janus-Pro-7B".
- `space` (str): Имя пространства на Hugging Face - "deepseek-ai/Janus-Pro-7B".
- `url` (str): URL пространства на Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга ответов.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста - "janus-pro-7b".
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений - "janus-pro-7b-image".
- `default_vision_model` (str): Модель, используемая по умолчанию для обработки изображений - "janus-pro-7b".
- `image_models` (List[str]): Список моделей, поддерживающих генерацию изображений.
- `vision_models` (List[str]): Список моделей, поддерживающих обработку изображений.
- `models` (List[str]): Полный список поддерживаемых моделей.

**Методы**:
- `run`: Выполняет HTTP-запрос к API.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

#### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, prompt: str, conversation: JsonConversation, image: dict = None, seed: int = 0):
    """ Выполняет HTTP-запрос к API Hugging Face Spaces.

    Args:
        method (str): HTTP-метод ("post" или "get").
        session (StreamSession): Асинхронная сессия для выполнения запросов.
        prompt (str): Текст запроса.
        conversation (JsonConversation): Объект, содержащий информацию о сессии.
        image (dict, optional): Информация об изображении для генерации. По умолчанию `None`.
        seed (int): Зерно для генерации случайных чисел.

    Returns:
        StreamResponse: Объект ответа от сервера.

    Как работает функция:
    1.  Функция `run` подготавливает заголовки запроса, включая токены и идентификаторы сессии.
    2.  В зависимости от значения параметра `method`, функция отправляет `POST` или `GET` запрос к API Hugging Face Spaces.
    3.  Если `method` равен `"post"`, отправляется запрос на генерацию текста. Если `method` равен `"image"`, отправляется запрос на генерацию изображения. Если `method` равен `"get"`, отправляется запрос для получения данных в формате `event-stream`.

    ASCII flowchart:
    ```
    Начало --> Проверка method --> method == "post"?
                 |               |
                 |               Да --> POST запрос (текст) --> Конец
                 |               |
                 |               Нет --> method == "image"?
                 |                               |
                 |                               Да --> POST запрос (изображение) --> Конец
                 |                               |
                 |                               Нет --> GET запрос (event-stream) --> Конец
                 |
                 Нет (ошибка)
    ```
    """
    ...
```

#### `create_async_generator`

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
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """ Создает асинхронный генератор для получения ответов от модели DeepseekAI Janus-Pro-7B.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            prompt (str, optional): Текст запроса. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            cookies (Cookies, optional): Cookies для отправки. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
            return_conversation (bool, optional): Флаг, указывающий на необходимость возврата объекта `JsonConversation`. По умолчанию `False`.
            conversation (JsonConversation, optional): Объект `JsonConversation` для продолжения сессии. По умолчанию `None`.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты от модели.

        Как работает функция:
        1.  Функция `create_async_generator` определяет метод запроса (`"post"` или `"image"`) в зависимости от выбранной модели и наличия запроса.
        2.  Если зерно (`seed`) не указано, генерируется случайное число.
        3.  Создается или используется существующий `session_hash` для идентификации сессии.
        4.  Создается асинхронная сессия `StreamSession` для выполнения запросов.
        5.  Получает `zerogpu_uuid` и `api_key` с помощью функции `get_zerogpu_token`, если они не предоставлены.
        6.  Создается или обновляется объект `JsonConversation` с информацией о сессии и токенах.
        7.  Если `return_conversation` установлен в `True`, возвращается объект `JsonConversation`.
        8.  Если есть медиафайлы, они загружаются на сервер.
        9.  Выполняется запрос к API с помощью метода `cls.run` и обрабатывается ответ, который возвращается в виде асинхронного генератора.

        ASCII flowchart:
        ```
        Начало --> Определение method --> Генерация seed --> Создание session_hash --> Создание StreamSession
                 |
                 --> Получение zerogpu_uuid и api_key --> Создание/обновление JsonConversation
                 |
                 --> return_conversation? --> Да --> Возврат JsonConversation --> Конец
                 |                       |
                 |                       Нет --> Загрузка медиафайлов (если есть) --> Выполнение запроса cls.run
                 |
                 --> Обработка ответа и возврат в виде асинхронного генератора --> Конец
        ```
        """
        ...
```

## Функции

### `get_zerogpu_token`

```python
async def get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: Cookies = None):
    """ Получает токен ZeroGPU для доступа к API Hugging Face Spaces.

    Args:
        space (str): Имя пространства на Hugging Face.
        session (StreamSession): Асинхронная сессия для выполнения запросов.
        conversation (JsonConversation): Объект, содержащий информацию о сессии.
        cookies (Cookies, optional): Cookies для отправки. По умолчанию `None`.

    Returns:
        Tuple[str, str]: Кортеж, содержащий UUID и токен ZeroGPU.

    Как работает функция:
    1.  Функция `get_zerogpu_token` пытается получить `zerogpu_uuid` из объекта `conversation`.
    2.  Если `zerogpu_uuid` отсутствует, функция выполняет GET-запрос к странице пространства на Hugging Face и извлекает `zerogpu_token` и `zerogpu_uuid` из HTML-кода страницы с использованием регулярных выражений.
    3.  Затем функция выполняет GET-запрос к API Hugging Face для получения JWT-токена, используя текущее время UTC + 10 минут в качестве срока действия.
    4.  Если токен успешно получен, он возвращается вместе с `zerogpu_uuid`.

    ASCII flowchart:
    ```
    Начало --> Проверка zerogpu_uuid в conversation --> zerogpu_uuid существует?
             |                                       |
             |                                       Нет --> GET запрос к странице пространства --> Извлечение zerogpu_token и zerogpu_uuid из HTML
             |                                       |
             |                                       Да
             |
             --> GET запрос к API для получения JWT-токена --> Возврат zerogpu_uuid и zerogpu_token --> Конец
    ```
    """
    ...
```