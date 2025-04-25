# Модуль G4F

## Обзор

Модуль `G4F` предоставляет класс `G4F`, который реализует взаимодействие с моделью Janus-Pro-7B  через Hugging Face Spaces. Класс обеспечивает функциональность для работы с различными моделями, включая `flux`, `flux-dev`, `flux-schnell`, `Janus-Pro-7B`, и  другие модели изображений. 

## Классы

### `class G4F(DeepseekAI_JanusPro7b)`

**Описание**: Класс  `G4F`  наследует от `DeepseekAI_JanusPro7b`, который реализует функциональность для работы с моделью Janus-Pro-7B. Предоставляет методы для создания асинхронных генераторов, работы с моделями и отправки запросов к API. 

**Наследует**: `DeepseekAI_JanusPro7b`

**Атрибуты**:

- `label` (str): Метка для  G4F.
- `space` (str):  Имя Hugging Face Spaces.
- `url` (str): URL  Hugging Face Spaces.
- `api_url` (str): URL API Janus-Pro-7B.
- `url_flux` (str):  URL  для отправки запросов модели  Flux.
- `referer` (str): URL для заголовка Referer.
- `default_model` (str):  Название модели по умолчанию.
- `model_aliases` (dict):  Словарь, сопоставляющий псевдонимы  модели  с её названием. 
- `image_models` (list):  Список моделей для работы с изображениями.
- `models` (list):  Список всех доступных  моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: int = None, cookies: dict = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", **kwargs) -> AsyncResult`: Асинхронный метод, который создает  генератор  результатов для модели Janus-Pro-7B.
- `get_model(model: str) -> str`: Метод для  получения  настоящего  названия модели на основе  псевдонима.

#### `async def create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: int = None, cookies: dict = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", **kwargs) -> AsyncResult`

**Описание**:  Метод  `create_async_generator` создает асинхронный генератор, который используется для получения результатов обработки данных от модели  Janus-Pro-7B.  В зависимости от выбранной  модели  перенаправляет  запросы к модели `FluxDev` (для  `flux` и `flux-dev`) или к  `DeepseekAI_JanusPro7b` (для остальных моделей). 

**Параметры**:

- `model` (str):  Название модели.
- `messages` (Messages):  Список сообщений для модели.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `prompt` (str, optional):  Текст запроса. По умолчанию `None`.
- `aspect_ratio` (str, optional):  Соотношение сторон изображения. По умолчанию `1:1`.
- `width` (int, optional): Ширина изображения. По умолчанию `None`.
- `height` (int, optional): Высота изображения. По умолчанию `None`.
- `seed` (int, optional):  Случайное число для генерации  результата. По умолчанию `None`.
- `cookies` (dict, optional):  Словарь  куки  для аутентификации. По умолчанию `None`.
- `api_key` (str, optional):  API ключ для аутентификации. По умолчанию `None`.
- `zerogpu_uuid` (str, optional):  UUID  для работы с  GPU. По умолчанию `[object Object]`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**: 
- `AsyncResult`:  Асинхронный  генератор  результатов.


#### `get_model(model: str) -> str`

**Описание**:  Метод  `get_model` получает  настоящее  имя  модели  из  `model_aliases` (если  введенный  `model`  является  псевдонимом).  

**Параметры**: 

- `model` (str):  Название модели.

**Возвращает**: 
- `str`:  Настоящее  имя модели.

## Функции

### `async def get_zerogpu_token(space: str, session: ClientSession, conversation: JsonConversation, cookies: dict) -> Tuple[str, str]`

**Описание**:  Асинхронная  функция, которая получает  токен  для  GPU  из  Hugging Face Spaces.

**Параметры**:

- `space` (str):  Имя  Hugging Face Spaces.
- `session` (ClientSession): Сессия  `aiohttp`.
- `conversation` (JsonConversation):  Объект  `JsonConversation`.
- `cookies` (dict):  Словарь  куки  для аутентификации.

**Возвращает**: 

- `Tuple[str, str]`:  Кортеж, содержащий UUID  для  GPU  и  токен.