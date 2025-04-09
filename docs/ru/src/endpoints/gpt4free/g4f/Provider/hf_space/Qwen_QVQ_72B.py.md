# Модуль `Qwen_QVQ_72B`

## Обзор

Модуль `Qwen_QVQ_72B` предоставляет асинхронный интерфейс для взаимодействия с моделью Qwen QVQ-72B через API, размещенный на платформе Hugging Face Space. Он поддерживает как текстовые запросы, так и запросы с использованием изображений.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими доступа к мультимодальной модели Qwen QVQ-72B. Он обеспечивает удобный способ отправки запросов к модели и получения результатов в асинхронном режиме. Модуль включает в себя функциональность для загрузки изображений, форматирования запросов и обработки ответов от API.

## Классы

### `Qwen_QVQ_72B`

**Описание**: Класс `Qwen_QVQ_72B` предоставляет методы для взаимодействия с моделью Qwen QVQ-72B.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:

- `label` (str): Метка провайдера, `"Qwen QVQ-72B"`.
- `url` (str): URL API, `"https://qwen-qvq-72b-preview.hf.space"`.
- `api_endpoint` (str): Эндпоинт API для генерации, `"/gradio_api/call/generate"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `default_model` (str): Модель по умолчанию, `"qwen-qvq-72b-preview"`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `"qwen-qvq-72b-preview"`.
- `model_aliases` (dict): Псевдонимы моделей, `{"qvq-72b": default_vision_model}`.
- `vision_models` (list): Список моделей для обработки изображений.
- `models` (list): Список поддерживаемых моделей.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для отправки запросов к модели.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model: str, messages: Messages,
    media: MediaListType = None,
    api_key: str = None, 
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с моделью Qwen QVQ-72B.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        ResponseError: Если происходит ошибка при запросе к API.
        RuntimeError: Если не удается прочитать ответ от API.
    """
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор для отправки запросов к API Qwen QVQ-72B. Она обрабатывает как текстовые запросы, так и запросы с изображениями, а также обеспечивает аутентификацию и проксирование запросов.

**Параметры**:

- `cls`: Ссылка на класс `Qwen_QVQ_72B`.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки в запросе.
- `media` (MediaListType, optional): Список медиафайлов (например, изображений) для отправки. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для использования при отправке запросов. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в функцию.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который выдает части ответа от модели.

**Вызывает исключения**:

- `ResponseError`: Вызывается, когда API возвращает ошибку (например, превышен лимит токенов GPU).
- `RuntimeError`: Вызывается, когда не удается декодировать ответ от API.

**Как работает функция**:

1.  **Инициализация**: Функция устанавливает заголовки, включая `Accept: application/json` и, если предоставлен, токен авторизации.
2.  **Обработка медиафайлов**: Если в запросе есть медиафайлы (изображения), они кодируются и отправляются на специальный эндпоинт для загрузки файлов. Полученный путь к изображению включается в данные запроса.
3.  **Форматирование запроса**: Форматирует сообщения, используя функцию `format_prompt`.
4.  **Отправка запроса**: Отправляет POST-запрос на эндпоинт `cls.api_endpoint` с данными запроса.
5.  **Обработка ответа**: Получает `event_id` из ответа и использует его для получения событий от сервера.
6.  **Генерация чанков**: Асинхронно получает чанки данных из потока событий. Если событие указывает на ошибку, выбрасывается исключение `ResponseError`. Если событие указывает на генерацию (`generating`), извлекает текст из данных и выдает его через генератор. Если событие указывает на завершение (`complete`), цикл завершается.
7.  **Обработка ошибок**: Если происходит ошибка при чтении или декодировании ответа, выбрасывается исключение `RuntimeError`.

**ASCII flowchart**:

```
Начало
  ↓
Установка заголовков (headers)
  ↓
Проверка наличия media
  ├── Нет media ──→ Форматирование запроса (format_prompt) → Отправка запроса (POST)
  │
  └── Есть media ──→ Кодирование и отправка media (POST upload) → Получение пути к изображению → Форматирование запроса с изображением → Отправка запроса (POST)
  ↓
Получение event_id из ответа
  ↓
Асинхронное получение чанков данных (GET event)
  ↓
Проверка типа события (event)
  ├── error ──→ Выброс исключения ResponseError
  │
  ├── generating ──→ Извлечение текста из данных → Выдача текста через yield
  │
  └── complete ──→ Завершение цикла
  ↓
Конец
```

**Примеры**:

1.  **Текстовый запрос**:

```python
async for chunk in Qwen_QVQ_72B.create_async_generator(model="qwen-qvq-72b-preview", messages=[{"role": "user", "content": "Hello, how are you?"}]):
    print(chunk, end="")
```

2.  **Запрос с изображением**:

```python
from pathlib import Path
from typing import List, Tuple

MediaListType = List[Tuple[bytes, str]] # fix typing

async def read_image(path: str | Path) -> bytes:
    with open(path, "rb") as f:
        return f.read()

async def main():
    image_path = Path("path/to/your/image.jpg")
    image_bytes = await read_image(image_path)
    media:MediaListType = [(image_bytes, image_path.name)]
    async for chunk in Qwen_QVQ_72B.create_async_generator(model="qwen-qvq-72b-preview", messages=[{"role": "user", "content": "What is in this picture?"}], media=media):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())