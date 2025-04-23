# Модуль `G4F.py`

## Обзор

Модуль `G4F.py` предоставляет класс `G4F`, который является частью фреймворка G4F (G4F framework) и предназначен для работы с моделями, размещенными на платформе Hugging Face Spaces. Класс `G4F` наследуется от `DeepseekAI_JanusPro7b` и `BlackForestLabs_Flux1Dev`, что позволяет ему использовать функциональность обоих этих классов. Модуль содержит методы для генерации изображений с использованием различных моделей, включая `flux` и `DeepseekAI_JanusPro7b`.

## Более подробная информация

Этот модуль используется для взаимодействия с различными моделями генерации изображений, размещенными на Hugging Face Spaces. Он предоставляет удобный интерфейс для генерации изображений на основе текстовых запросов, поддерживая различные параметры, такие как размеры изображения, seed для воспроизводимости и прокси для обхода ограничений сети. Класс `G4F` расширяет возможности базовых классов `DeepseekAI_JanusPro7b` и `BlackForestLabs_Flux1Dev`, добавляя специфическую логику для работы с моделями G4F.

## Классы

### `FluxDev`

**Описание**:
Класс `FluxDev` является подклассом `BlackForestLabs_Flux1Dev` и предназначен для работы с моделью Flux.1-dev, размещенной на Hugging Face Spaces.

**Наследует**:
- `BlackForestLabs_Flux1Dev`

**Атрибуты**:
- `url` (str): URL пространства Hugging Face, где размещена модель.
- `space` (str): Имя пространства Hugging Face.
- `referer` (str): Referer URL для HTTP-запросов.

**Принцип работы**:
Класс `FluxDev` предоставляет доступ к модели Flux.1-dev через Hugging Face Spaces. Он определяет URL и другие параметры, необходимые для взаимодействия с этой моделью.

### `G4F`

**Описание**:
Класс `G4F` является основным классом модуля и предназначен для работы с фреймворком G4F. Он наследуется от `DeepseekAI_JanusPro7b` и расширяет его функциональность, добавляя поддержку модели `flux`.

**Наследует**:
- `DeepseekAI_JanusPro7b`

**Атрибуты**:
- `label` (str): Метка для класса.
- `space` (str): Имя пространства Hugging Face.
- `url` (str): URL пространства Hugging Face.
- `api_url` (str): URL API для взаимодействия с моделью.
- `url_flux` (str): URL для запуска предсказаний модели `flux`.
- `referer` (str): Referer URL для HTTP-запросов.
- `default_model` (str): Модель по умолчанию.
- `model_aliases` (dict): Алиасы для моделей.
- `image_models` (list): Список моделей для генерации изображений.
- `models` (list): Список всех поддерживаемых моделей.

**Принцип работы**:
Класс `G4F` предоставляет интерфейс для генерации изображений с использованием различных моделей, размещенных на Hugging Face Spaces. Он поддерживает как модель `DeepseekAI_JanusPro7b`, так и модель `flux`, а также предоставляет возможность использовать прокси и API-ключи для доступа к моделям.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    prompt: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    seed: int = None,
    cookies: dict = None,
    api_key: str = None,
    zerogpu_uuid: str = "[object Object]",
    **kwargs
) -> AsyncResult:
    """
    Асинхронный генератор для создания изображений на основе текстовых запросов.

    Args:
        cls (type[G4F]): Класс `G4F`.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        seed (int, optional): Seed для воспроизводимости генерации. По умолчанию `None`.
        cookies (dict, optional): Cookie для HTTP-запросов. По умолчанию `None`.
        api_key (str, optional): API-ключ для доступа к модели. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncResult: Частичные результаты генерации изображения.

    Raises:
        Exception: Если возникает ошибка при генерации изображения.
    """
    ...
```

**Внутренние функции**:

Функция `create_async_generator` содержит внутреннюю функцию `generate`, которая выполняет HTTP-запрос к API для генерации изображения.

```python
async def generate():
    """
    Выполняет HTTP-запрос к API для генерации изображения.

    Args:
        Нет.

    Returns:
        ImageResponse: Объект `ImageResponse`, содержащий URL сгенерированного изображения.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.
    """
    ...
```

**Как работает функция**:

1. **Обработка модели `flux`**: Если указана модель `flux` или `flux-dev`, функция перенаправляет запрос в `FluxDev.create_async_generator`.
2. **Обработка других моделей**: Если модель не `flux`, функция вызывает метод `create_async_generator` из суперкласса (`DeepseekAI_JanusPro7b`).
3. **Подготовка параметров**: Функция подготавливает параметры для запроса, такие как размеры изображения, seed и текстовый запрос.
4. **Формирование запроса**: Функция формирует payload для HTTP-запроса к API.
5. **Получение токена GPU**: Если `api_key` не предоставлен, функция пытается получить токен GPU.
6. **Выполнение запроса**: Функция выполняет асинхронный HTTP-запрос к API и обрабатывает ответ.
7. **Генерация изображения**: Функция извлекает URL сгенерированного изображения из ответа и возвращает объект `ImageResponse`.
8. **Асинхронная обработка**: Функция использует `asyncio` для асинхронной генерации изображения и отслеживания статуса.

**Примеры**:

Пример вызова функции для генерации изображения с использованием модели `flux`:

```python
async for chunk in G4F.create_async_generator(
    model="flux",
    messages=[{"role": "user", "content": "A cat"}],
    width=512,
    height=512
):
    print(chunk)
```

Пример вызова функции для генерации изображения с использованием модели `DeepseekAI_JanusPro7b`:

```python
async for chunk in G4F.create_async_generator(
    model="deepseekai",
    messages=[{"role": "user", "content": "A dog"}],
    width=512,
    height=512
):
    print(chunk)
```