# Модуль BlackForestLabs_Flux1Dev 

## Обзор

Данный модуль предоставляет реализацию класса `BlackForestLabs_Flux1Dev`, который является провайдером для модели FLUX.1-Dev от BlackForestLabs.

## Классы

### `class BlackForestLabs_Flux1Dev`

**Описание**: Класс `BlackForestLabs_Flux1Dev` является наследником `AsyncGeneratorProvider` и `ProviderModelMixin`, реализует провайдер для модели FLUX.1-Dev. 

**Наследует**:
 - `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров, предоставляющих генератор результатов.
 - `ProviderModelMixin`: Базовый класс, предоставляющий миксин для работы с моделями.

**Атрибуты**:
 - `label` (str): Описание модели, "BlackForestLabs Flux-1-Dev".
 - `url` (str): URL-адрес пространства модели, "https://black-forest-labs-flux-1-dev.hf.space".
 - `space` (str): Имя пространства модели, "black-forest-labs/FLUX.1-dev".
 - `referer` (str): URL-адрес реферера для запросов к пространству модели.
 - `working` (bool): Флаг, указывающий на доступность модели, `True`.
 - `default_model` (str): Имя модели по умолчанию, "black-forest-labs-flux-1-dev".
 - `default_image_model` (str): Имя модели по умолчанию для изображений, "black-forest-labs-flux-1-dev".
 - `model_aliases` (dict): Алиасы для модели, {"flux-dev": "black-forest-labs-flux-1-dev", "flux": "black-forest-labs-flux-1-dev"}.
 - `image_models` (list): Список имен моделей для изображений, ["flux-dev", "flux"].
 - `models` (list): Список имен всех моделей, ["flux-dev", "flux"].

**Методы**:

#### `run(method: str, session: StreamSession, conversation: JsonConversation, data: list = None)`

**Назначение**: Функция `run` отправляет запрос к пространству модели FLUX.1-Dev, используя HTTP-метод `method` и предоставляет сессию `session`, информацию о разговоре `conversation` и данные `data`.

**Параметры**:
 - `method` (str): HTTP-метод, "post" или "get".
 - `session` (StreamSession): Сессия для выполнения запроса.
 - `conversation` (JsonConversation): Информация о текущем разговоре.
 - `data` (list, optional): Данные для запроса, по умолчанию `None`.

**Возвращает**:
 - `StreamSession.post(f"{cls.url}/gradio_api/queue/join?__theme=light", ...)` или `StreamSession.get(f"{cls.url}/gradio_api/queue/data?session_hash={conversation.session_hash}", ...)`: Объект ответа от пространства модели.

**Как работает функция**: 
 - Функция `run` формирует заголовки `headers` для запроса. 
 - В зависимости от метода `method` отправляет POST-запрос на URL-адрес `/gradio_api/queue/join` для инициализации сессии или GET-запрос на URL-адрес `/gradio_api/queue/data` для получения данных из очереди.
 - Возвращает объект ответа от пространства модели.


#### `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, guidance_scale: float = 3.5, num_inference_steps: int = 28, seed: int = 0, randomize_seed: bool = True, cookies: dict = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", **kwargs) -> AsyncResult`

**Назначение**: Асинхронная функция `create_async_generator` создает асинхронный генератор, который взаимодействует с моделью FLUX.1-Dev, обрабатывает подсказку `prompt`, отправляет запрос к модели, обрабатывает ответ и возвращает результаты по частям.

**Параметры**:
 - `model` (str): Имя модели.
 - `messages` (Messages): Список сообщений разговора.
 - `prompt` (str, optional): Текстовая подсказка, по умолчанию `None`.
 - `proxy` (str, optional): Прокси-сервер, по умолчанию `None`.
 - `aspect_ratio` (str, optional): Соотношение сторон для изображений, по умолчанию "1:1".
 - `width` (int, optional): Ширина изображения, по умолчанию `None`.
 - `height` (int, optional): Высота изображения, по умолчанию `None`.
 - `guidance_scale` (float, optional): Масштаб направляющего вектора, по умолчанию 3.5.
 - `num_inference_steps` (int, optional): Количество шагов генерации, по умолчанию 28.
 - `seed` (int, optional): Семенное значение, по умолчанию 0.
 - `randomize_seed` (bool, optional): Флаг, указывающий на рандомизацию семенного значения, по умолчанию `True`.
 - `cookies` (dict, optional): Словарь с куки, по умолчанию `None`.
 - `api_key` (str, optional): API-ключ, по умолчанию `None`.
 - `zerogpu_uuid` (str, optional): UUID для соединения, по умолчанию "[object Object]".
 - `**kwargs`: Дополнительные аргументы.

**Возвращает**:
 - `AsyncResult`: Объект `AsyncResult`, представляющий асинхронный результат.

**Как работает функция**: 
 - Создает экземпляр `StreamSession` для асинхронного HTTP-запроса.
 - Форматирует текст подсказки `prompt` с использованием `format_image_prompt`.
 - Подготавливает данные `data` для запроса.
 - Создает экземпляр `JsonConversation` для текущего разговора.
 - Проверяет наличие API-ключа `api_key` и, если он отсутствует, получает его с помощью `get_zerogpu_token`.
 - Отправляет POST-запрос к пространству модели.
 - Проверяет статус ответа.
 - Получает данные из очереди.
 - Обрабатывает ответы от модели.
 - Возвращает асинхронный генератор `AsyncResult`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from hypotez.src.endpoints.gpt4free.g4f.requests import StreamSession
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.conversation import JsonConversation

model = "flux-dev"
messages: Messages = [
    {"role": "user", "content": "Нарисуй кота"},
]
prompt = None
proxy = None
aspect_ratio = "1:1"
width = None
height = None
guidance_scale = 3.5
num_inference_steps = 28
seed = 0
randomize_seed = True
cookies = None
api_key = None
zerogpu_uuid = "[object Object]"

async with StreamSession(impersonate="chrome", proxy=proxy) as session:
    conversation = JsonConversation(zerogpu_token=api_key, zerogpu_uuid=zerogpu_uuid, session_hash=uuid.uuid4().hex)
    async with BlackForestLabs_Flux1Dev.create_async_generator(
        model=model,
        messages=messages,
        prompt=prompt,
        proxy=proxy,
        aspect_ratio=aspect_ratio,
        width=width,
        height=height,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        seed=seed,
        randomize_seed=randomize_seed,
        cookies=cookies,
        api_key=api_key,
        zerogpu_uuid=zerogpu_uuid,
    ) as async_generator:
        async for result in async_generator:
            print(result)
```

## Внутренние функции

#### `get_zerogpu_token(space: str, session: StreamSession, conversation: JsonConversation, cookies: dict = None)`

**Назначение**: Функция `get_zerogpu_token` получает токен ZeroGPU для пространства модели `space`.

**Параметры**:
 - `space` (str): Имя пространства модели.
 - `session` (StreamSession): Сессия для выполнения запроса.
 - `conversation` (JsonConversation): Информация о текущем разговоре.
 - `cookies` (dict, optional): Словарь с куки, по умолчанию `None`.

**Возвращает**:
 - `tuple[str, str]`: Кортеж, содержащий UUID и токен ZeroGPU.

**Как работает функция**: 
 - Функция отправляет POST-запрос к URL-адресу `/gradio_api/queue/join`, предоставляя UUID, токен ZeroGPU, пространство модели и куки.
 - Обрабатывает ответ от пространства модели и извлекает UUID и токен ZeroGPU.
 - Возвращает кортеж с UUID и токен ZeroGPU.

#### `raise_for_status(response: StreamSession.post(...))`

**Назначение**: Функция `raise_for_status` проверяет статус ответа от пространства модели.

**Параметры**:
 - `response` (StreamSession.post(...)): Объект ответа от пространства модели.

**Возвращает**:
 - `None`

**Как работает функция**: 
 - Проверяет статус ответа. 
 - Если статус ответа не является 200, то вызывается исключение `ResponseError` с сообщением об ошибке.

## Параметры класса

 - `label` (str): Описание модели, "BlackForestLabs Flux-1-Dev".
 - `url` (str): URL-адрес пространства модели, "https://black-forest-labs-flux-1-dev.hf.space".
 - `space` (str): Имя пространства модели, "black-forest-labs/FLUX.1-dev".
 - `referer` (str): URL-адрес реферера для запросов к пространству модели.
 - `working` (bool): Флаг, указывающий на доступность модели, `True`.
 - `default_model` (str): Имя модели по умолчанию, "black-forest-labs-flux-1-dev".
 - `default_image_model` (str): Имя модели по умолчанию для изображений, "black-forest-labs-flux-1-dev".
 - `model_aliases` (dict): Алиасы для модели, {"flux-dev": "black-forest-labs-flux-1-dev", "flux": "black-forest-labs-flux-1-dev"}.
 - `image_models` (list): Список имен моделей для изображений, ["flux-dev", "flux"].
 - `models` (list): Список имен всех моделей, ["flux-dev", "flux"].

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev

# Создание экземпляра класса
provider = BlackForestLabs_Flux1Dev()

# Получение списка доступных моделей
print(provider.models)

# Использование метода create_async_generator
# ...
```