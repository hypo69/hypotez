# Модуль BlackForestLabs_Flux1Dev

## Обзор

Модуль `BlackForestLabs_Flux1Dev` предоставляет асинхронный генератор для взаимодействия с моделью BlackForestLabs Flux-1-Dev.
Он позволяет генерировать изображения на основе текстового запроса, используя API сервиса Black Forest Labs.

## Подробнее

Модуль предназначен для использования в качестве провайдера изображений.
Он реализует логику для отправки запросов к сервису Black Forest Labs и обработки полученных ответов.
Поддерживает различные параметры генерации изображений, такие как соотношение сторон, размеры изображения, seed и прочее.

## Классы

### `BlackForestLabs_Flux1Dev`

**Описание**: Класс `BlackForestLabs_Flux1Dev` является асинхронным генератором и предоставляет методы для взаимодействия с моделью BlackForestLabs Flux-1-Dev.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера, отображаемая пользователю.
- `url` (str): URL сервиса Black Forest Labs.
- `space` (str): Идентификатор пространства на Hugging Face Spaces.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель генерации изображений, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей для совместимости.
- `image_models` (list): Список поддерживаемых моделей изображений.
- `models` (list): Список поддерживаемых моделей.

#### `run`

```python
    @classmethod
    def run(cls, method: str, session: StreamSession, conversation: JsonConversation, data: list = None):
        """
        Выполняет HTTP-запрос к API Black Forest Labs.

        Args:
            method (str): HTTP-метод ("post" или "get").
            session (StreamSession): Асинхровая сессия для выполнения запросов.
            conversation (JsonConversation): Объект, содержащий данные для conversation.
            data (list, optional): Данные для отправки в теле запроса. По умолчанию `None`.

        Returns:
            AsyncResult: Асинхронный результат выполнения запроса.

        Raises:
            ResponseError: В случае ошибки при выполнении запроса.
        """
        ...
```

**Параметры**:
- `method` (str): HTTP-метод ("post" или "get").
- `session` (StreamSession): Асинхровая сессия для выполнения запросов.
- `conversation` (JsonConversation): Объект, содержащий данные для conversation.
- `data` (list, optional): Данные для отправки в теле запроса. По умолчанию `None`.

**Как работает функция**:
1. Формирует заголовки запроса, включая токен авторизации и UUID.
2. В зависимости от метода (`post` или `get`) выполняет соответствующий запрос к API.
3. Возвращает асинхронный ответ.

ASCII flowchart:
```
    Начало
    │
    │   method, session, conversation, data
    │
    │   Формирование заголовков (headers)
    │
    │   method == "post"?
    ├───ДА──────
    │   │
    │   │   POST-запрос к API
    │   │
    └───НЕТ─────
    │   │
    │   │   GET-запрос к API
    │   │
    │   Возврат ответа
    │
    Конец
```

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls, 
        model: str, 
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        aspect_ratio: str = "1:1",
        width: int = None,
        height: int = None,
        guidance_scale: float = 3.5,
        num_inference_steps: int = 28,
        seed: int = 0,
        randomize_seed: bool = True,
        cookies: dict = None,
        api_key: str = None,
        zerogpu_uuid: str = "[object Object]",
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (str, optional): Текстовый запрос. По умолчанию `None`.
            proxy (str, optional): Proxy для выполнения запросов. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            width (int, optional): Ширина изображения. По умолчанию `None`.
            height (int, optional): Высота изображения. По умолчанию `None`.
            guidance_scale (float, optional): Guidance scale для генерации. По умолчанию 3.5.
            num_inference_steps (int, optional): Количество шагов inference. По умолчанию 28.
            seed (int, optional): Seed для генерации. По умолчанию 0.
            randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
            cookies (dict, optional): Cookies для выполнения запросов. По умолчанию `None`.
            api_key (str, optional): API ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
            **kwargs: Дополнительные аргументы.

        Yields:
            Reasoning: Промежуточные статусы генерации.
            ImagePreview: Предварительный просмотр изображения.
            ImageResponse: Сгенерированное изображение.

        Raises:
            RuntimeError: Если не удается обработать сообщение из ответа.
            ResponseError: Если API возвращает ошибку.
        """
        ...
```

**Параметры**:
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Текстовый запрос. По умолчанию `None`.
- `proxy` (str, optional): Proxy для выполнения запросов. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
- `width` (int, optional): Ширина изображения. По умолчанию `None`.
- `height` (int, optional): Высота изображения. По умолчанию `None`.
- `guidance_scale` (float, optional): Guidance scale для генерации. По умолчанию 3.5.
- `num_inference_steps` (int, optional): Количество шагов inference. По умолчанию 28.
- `seed` (int, optional): Seed для генерации. По умолчанию 0.
- `randomize_seed` (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
- `cookies` (dict, optional): Cookies для выполнения запросов. По умолчанию `None`.
- `api_key` (str, optional): API ключ. По умолчанию `None`.
- `zerogpu_uuid` (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:

1.  **Инициализация**:
    *   Создается асинхронная сессия с использованием `StreamSession`.
    *   Формируется текстовый запрос (`prompt`) из списка сообщений (`messages`).
    *   Определяются размеры изображения (`width`, `height`) на основе соотношения сторон (`aspect_ratio`).
    *   Создается объект `JsonConversation` для хранения данных сессии.
2.  **Авторизация**:
    *   Если `api_key` (он же `zerogpu_token`) не передан, то происходит попытка получить `zerogpu_uuid` и `zerogpu_token` с использованием функции `get_zerogpu_token`.
3.  **Запрос к API**:
    *   Выполняется `POST` запрос к API с передачей сформированных данных.
    *   Проверяется успешность запроса с помощью `raise_for_status`.
4.  **Обработка ответа**:
    *   Выполняется `GET` запрос для получения данных о процессе генерации изображения.
    *   Ответ обрабатывается построчно, каждая строка проверяется на префикс `data: `.
    *   JSON-данные извлекаются из каждой строки и обрабатываются в зависимости от значения ключа `msg`:
        *   `log`: Извлекается статус генерации (`status`) и передается как `Reasoning`.
        *   `progress`: Извлекается информация о прогрессе генерации и передается как `Reasoning`.
        *   `process_generating`: Извлекаются URL превью изображений (`ImagePreview`).
        *   `process_completed`: Извлекается результат генерации:
            *   Если в ответе есть ошибка (`error`), выбрасывается исключение `ResponseError`.
            *   Если в ответе есть данные (`data`), извлекается URL сгенерированного изображения (`ImageResponse`).
5.  **Обработка ошибок**:
    *   В случае ошибок при парсинге JSON или других ошибок обработки данных, выбрасывается исключение `RuntimeError`.

ASCII flowchart:

```
Начало
│
│ model, messages, prompt, proxy, aspect_ratio, width, height, guidance_scale, num_inference_steps, seed, randomize_seed, cookies, api_key, zerogpu_uuid, kwargs
│
│ Создание StreamSession
│
│ prompt = format_image_prompt(messages, prompt)
│ data = use_aspect_ratio({"width": width, "height": height}, aspect_ratio)
│ data = [prompt, seed, randomize_seed, data.get("width"), data.get("height"), guidance_scale, num_inference_steps]
│ conversation = JsonConversation(zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid, session_hash=uuid.uuid4().hex)
│
│ api_key is None?
├──ДА
│  │  Получение zerogpu_uuid и zerogpu_token через get_zerogpu_token
│  └──НЕТ
│
│ POST-запрос к API (cls.run)
│ Обработка ответа (event_response.iter_lines())
│
│ Для каждой строки (chunk) в ответе:
│   chunk.startswith(b"data: ")?
│   ├──ДА
│   │  │ json_data = json.loads(chunk[6:])
│   │  │ msg = json_data.get('msg')
│   │  │
│   │  │ msg == 'log'?
│   │  ├──ДА
│   │  │  │  yield Reasoning(status=json_data["log"])
│   │  │  └──НЕТ
│   │  │
│   │  │ msg == 'progress'?
│   │  ├──ДА
│   │  │  │  yield Reasoning(status=f"{progress['desc']} {progress['index']}/{progress['length']}")
│   │  │  └──НЕТ
│   │  │
│   │  │ msg == 'process_generating'?
│   │  ├──ДА
│   │  │  │  yield ImagePreview(item["url"], prompt) или yield ImagePreview(item[2], prompt)
│   │  │  └──НЕТ
│   │  │
│   │  │ msg == 'process_completed'?
│   │  ├──ДА
│   │  │  │  if 'error' in json_data['output']: raise ResponseError
│   │  │  │  yield Reasoning(status="Finished")
│   │  │  │  yield ImageResponse(json_data['output']['data'][0]["url"], prompt)
│   │  │  └──НЕТ
│   │  │
│   │  └──Конец цикла обработки строк
│   └──НЕТ
│
│ Обработка ошибок (json.JSONDecodeError, KeyError, TypeError) -> RuntimeError
│
Конец
```

**Примеры**:

```python
# Пример использования create_async_generator
model = "black-forest-labs-flux-1-dev"
messages = [{"role": "user", "content": "A futuristic cityscape"}]

async def generate_image():
    async for item in BlackForestLabs_Flux1Dev.create_async_generator(model=model, messages=messages):
        if isinstance(item, ImageResponse):
            print(f"Image URL: {item.url}")
        elif isinstance(item, Reasoning):
            print(f"Status: {item.status}")

# Запуск асинхронной функции
import asyncio
asyncio.run(generate_image())
```

## Функции

### `get_zerogpu_token`

Эта функция импортируется из модуля `DeepseekAI_JanusPro7b` и используется для получения токена ZeroGPU.
Описание этой функции находится в документации для модуля `DeepseekAI_JanusPro7b`.

### `raise_for_status`

Эта функция импортируется из модуля `raise_for_status` и используется для проверки статуса ответа HTTP.
Описание этой функции находится в документации для модуля `raise_for_status`.