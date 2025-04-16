# Модуль для работы с ReplicateHome
========================================

Модуль предоставляет асинхронный интерфейс для взаимодействия с API ReplicateHome для генерации текста и изображений с использованием различных моделей машинного обучения.

## Обзор

Этот модуль предназначен для асинхронного взаимодействия с сервисом ReplicateHome, который предоставляет API для запуска моделей машинного обучения, таких как `google-deepmind/gemma-2b-it` для текста и `stability-ai/stable-diffusion-3` для изображений. Модуль включает поддержку стриминга ответов и обработки ошибок.

## Подробнее

Модуль содержит класс `ReplicateHome`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет URL, API endpoint, поддерживает стриминг, устанавливает модели по умолчанию и предоставляет методы для асинхронной генерации контента.

## Классы

### `ReplicateHome`

**Описание**: Класс для взаимодействия с API ReplicateHome.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет асинхронный интерфейс генератора.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сайта ReplicateHome.
- `api_endpoint` (str): URL API endpoint для создания prediction.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг.
- `default_model` (str): Модель по умолчанию для генерации текста.
- `default_image_model` (str): Модель по умолчанию для генерации изображений.
- `image_models` (List[str]): Список моделей для генерации изображений.
- `text_models` (List[str]): Список моделей для генерации текста.
- `models` (List[str]): Объединенный список моделей для текста и изображений.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.
- `model_versions` (Dict[str, str]): Словарь версий моделей.

**Принцип работы**:
Класс `ReplicateHome` предназначен для асинхронного взаимодействия с API ReplicateHome. Он поддерживает как генерацию текста, так и генерацию изображений, используя различные модели машинного обучения. Класс позволяет отправлять запросы к API, опрашивать статус выполнения задачи и возвращать результаты в виде асинхронного генератора.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API ReplicateHome.

    Args:
        cls (ReplicateHome): Ссылка на класс.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор результатов.

    Raises:
        Exception: Если prediction не удался или истекло время ожидания.

    Как работает функция:
    1.  Получает модель из `model_aliases`, если указан псевдоним.
    2.  Формирует заголовки запроса, включая User-Agent, Referer и Content-Type.
    3.  Создает асинхронную сессию `ClientSession` с заданными заголовками и прокси.
    4.  Если `prompt` не передан, формирует его из `messages`, используя `format_prompt` для текстовых моделей и последнее сообщение для моделей изображений.
    5.  Создает JSON-данные для запроса, включая модель, версию модели и входной `prompt`.
    6.  Отправляет POST-запрос к `api_endpoint` с JSON-данными.
    7.  Извлекает `prediction_id` из результата ответа.
    8.  Запускает цикл опроса API для получения статуса prediction.
    9.  В цикле отправляет GET-запросы к `poll_url` с `prediction_id`.
    10. Обрабатывает ответ, проверяя статус prediction:
        *   Если статус `'succeeded'`:
            *   Для моделей изображений возвращает URL изображения в `ImageResponse`.
            *   Для текстовых моделей возвращает чанки текста.
        *   Если статус `'failed'`: вызывает исключение с сообщением об ошибке.
    11. Если превышено максимальное количество попыток опроса и статус не `'succeeded'`, вызывает исключение о превышении времени ожидания.
    """
```

## Параметры класса

- `url` (str): URL сайта ReplicateHome.
- `api_endpoint` (str): URL API endpoint для создания prediction.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг.
- `default_model` (str): Модель по умолчанию для генерации текста.
- `default_image_model` (str): Модель по умолчанию для генерации изображений.
- `image_models` (List[str]): Список моделей для генерации изображений.
- `text_models` (List[str]): Список моделей для генерации текста.
- `models` (List[str]): Объединенный список моделей для текста и изображений.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.
- `model_versions` (Dict[str, str]): Словарь версий моделей.

**Примеры**

```python
# Пример использования create_async_generator для текстовой модели
model = "google-deepmind/gemma-2b-it"
messages = [{"role": "user", "content": "Напиши короткое стихотворение."}]
async for chunk in ReplicateHome.create_async_generator(model=model, messages=messages):
    print(chunk)

# Пример использования create_async_generator для модели изображений
model = "stability-ai/stable-diffusion-3"
messages = [{"role": "user", "content": "Собака в космосе."}]
async for image_response in ReplicateHome.create_async_generator(model=model, messages=messages):
    print(image_response.image_url)