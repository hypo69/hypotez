# ReplicateHome Provider

## Обзор

Модуль содержит класс `ReplicateHome`, реализующий асинхронный генератор для получения ответов от модели Replicate.  Replicate - это платформа для работы с машинным обучением, предоставляющая доступ к широкому спектру моделей для различных задач, в том числе для генерации текста и изображений.

## Подробней

`ReplicateHome` - это асинхронный генератор, который позволяет получать ответы от моделей Replicate в виде потока данных. Он используется для работы с различными моделями, в том числе текстовыми (например, `google-deepmind/gemma-2b-it`) и моделями генерации изображений (например, `stability-ai/stable-diffusion-3`).

## Классы

### `class ReplicateHome`

**Описание**:  Класс `ReplicateHome` представляет собой асинхронный генератор для получения ответов от моделей Replicate.

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Класс, предоставляющий функционал для работы с моделями.

**Атрибуты**:

- `url (str)`: Базовый URL Replicate.
- `api_endpoint (str)`: Эндпоинт API для получения предсказаний.
- `working (bool)`: Флаг, указывающий на готовность к работе.
- `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи данных.
- `default_model (str)`: Название модели по умолчанию.
- `default_image_model (str)`: Название модели для генерации изображений по умолчанию.
- `image_models (List[str])`: Список поддерживаемых моделей для генерации изображений.
- `text_models (List[str])`: Список поддерживаемых текстовых моделей.
- `models (List[str])`: Объединенный список всех поддерживаемых моделей.
- `model_aliases (dict)`: Словарь с псевдонимами моделей.
- `model_versions (dict)`: Словарь с версиями моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, **kwargs) -> AsyncResult`:  Создает асинхронный генератор для получения ответов от модели Replicate.

#### `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, **kwargs) -> AsyncResult`

**Назначение**:  Создает асинхронный генератор для получения ответов от модели Replicate.

**Параметры**:

- `model (str)`: Название модели.
- `messages (Messages)`: Список сообщений для обработки.
- `prompt (str, optional)`: Текст запроса. По умолчанию `None`.
- `proxy (str, optional)`: Прокси-сервер. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный результат.

**Как работает функция**:

- Получает название модели, список сообщений и текст запроса.
- Проверяет, есть ли модель в списке поддерживаемых.
- Формирует запрос к API Replicate.
- Отправляет запрос к API с помощью `ClientSession`.
- Получает результат от API и извлекает `prediction_id`.
- Инициализирует цикл опроса состояния предсказания.
- В цикле выполняет запрос к API для получения статуса предсказания.
- Если статус предсказания `'succeeded'`, то выдает результат в виде потока данных.
- Если статус предсказания `'failed'`, то выбрасывает исключение.
- Если предсказание не завершено в течение заданного времени, то выбрасывает исключение.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.ReplicateHome import ReplicateHome

async def example():
    messages = [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
    async for chunk in ReplicateHome.create_async_generator(model='google-deepmind/gemma-2b-it', messages=messages):
        print(chunk)

asyncio.run(example())
```

## Внутренние функции

В коде класса `ReplicateHome` нет внутренних функций.