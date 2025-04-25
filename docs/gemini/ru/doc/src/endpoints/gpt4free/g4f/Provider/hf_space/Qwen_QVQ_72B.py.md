# Модуль Qwen_QVQ_72B

## Обзор

Этот модуль предоставляет класс `Qwen_QVQ_72B`, который используется для взаимодействия с большой языковой моделью Qwen QVQ-72B, доступной на Hugging Face Spaces. Класс реализует асинхронный генератор ответов, позволяющий получать ответы от модели по частям.

## Классы

### `class Qwen_QVQ_72B`

**Описание**:  Класс для взаимодействия с моделью Qwen QVQ-72B на Hugging Face Spaces.

**Наследует**: 
    - `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
    - `ProviderModelMixin`: Предоставляет общие функции для управления моделями.

**Атрибуты**:

- `label` (str): Имя модели - "Qwen QVQ-72B".
- `url` (str): URL адрес Hugging Face Spaces, на котором размещена модель.
- `api_endpoint` (str): Эндпоинт API для отправки запросов к модели.
- `working` (bool): Флаг, указывающий на доступность модели.
- `default_model` (str): Имя по умолчанию для модели.
- `default_vision_model` (str): Имя по умолчанию для модели, работающей с изображениями.
- `model_aliases` (dict): Словарь алиасов для модели.
- `vision_models` (list): Список имен моделей, работающих с изображениями.
- `models` (list): Список имен всех моделей.

**Методы**:

#### `create_async_generator(model: str, messages: Messages, media: MediaListType = None, api_key: str = None, proxy: str = None, **kwargs) -> AsyncResult`

**Описание**: Асинхронный генератор ответов от модели Qwen QVQ-72B. 

**Параметры**:

- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений в диалоге.
- `media` (MediaListType): Список медиафайлов (например, изображений).
- `api_key` (str): Ключ API для доступа к модели.
- `proxy` (str): Адрес прокси-сервера.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, представляющий собой генератор ответов от модели.

**Как работает**:

- Устанавливает заголовки HTTP-запроса, включая токен авторизации, если он предоставлен.
- Создает HTTP-сессию и отправляет POST-запрос на API-эндпоинт с данными запроса.
- Если в запросе присутствуют медиафайлы, они загружаются на сервер с помощью API `upload`.
- После отправки запроса, метод следит за статусом ответа модели и, при получении новых данных, выдает их через генератор.
- При возникновении ошибок, метод выбрасывает исключение `ResponseError`. 

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_QVQ_72B import Qwen_QVQ_72B
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра класса Qwen_QVQ_72B
provider = Qwen_QVQ_72B()

# Список сообщений в диалоге
messages = Messages([
    {"role": "user", "content": "Привет! Как дела?"},
])

# Получение ответа от модели 
async def main():
    async for response in provider.create_async_generator(model="qwen-qvq-72b-preview", messages=messages):
        print(f"Модель ответила: {response}")

# Запуск асинхронной функции
asyncio.run(main())
```