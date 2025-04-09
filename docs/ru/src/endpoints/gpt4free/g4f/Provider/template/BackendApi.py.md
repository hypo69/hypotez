# Документация модуля BackendApi

## Обзор

Модуль `BackendApi` предоставляет класс `BackendApi`, который является асинхронным генераторным провайдером и миксином для моделей провайдеров. Он предназначен для взаимодействия с API бэкенда для создания бесед, поддерживая отправку текстовых сообщений и медиафайлов.

## Подробней

Модуль используется для асинхронного взаимодействия с API, отправляя запросы и получая ответы в виде потока данных. Он поддерживает передачу сообщений, медиафайлов и дополнительных параметров в запросе. Класс `BackendApi` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему использовать функциональность асинхронных генераторов и моделей провайдеров.

## Классы

### `BackendApi`

**Описание**: Класс `BackendApi` является асинхронным генераторным провайдером и миксином для моделей провайдеров.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает функциональность асинхронного генератора.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями провайдеров.

**Атрибуты**:
- `ssl` (None): Определяет, использовать ли SSL (по умолчанию `None`).
- `headers` (dict): Заголовки для HTTP-запросов (по умолчанию пустой словарь).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с API.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    media: MediaListType = None,
    api_key: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API бэкенда.

    Args:
        model (str): Имя модели, используемой для генерации.
        messages (Messages): Список сообщений для отправки в API.
        media (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий объекты `RawResponse`.
    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API бэкенда. Этот генератор отправляет сообщения и медиафайлы (если есть) в API и получает ответы в виде потока данных.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Имя модели, используемой для генерации.
- `messages` (Messages): Список сообщений для отправки в API.
- `media` (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий объекты `RawResponse`.

**Как работает функция**:

1. **Логирование**: Записывает в лог имя класса и ключ API.
2. **Преобразование медиафайлов**: Если переданы медиафайлы, преобразует их в формат data URI.
3. **Создание сессии**: Открывает асинхронную сессию для отправки запросов.
4. **Отправка запроса**: Отправляет POST-запрос к API с указанными параметрами (модель, сообщения, медиафайлы, ключ API и дополнительные аргументы) в формате JSON.
5. **Получение и обработка ответов**: Итерируется по строкам ответа, преобразует каждую строку в объект `RawResponse` и выдает его через генератор.

**ASCII flowchart**:

```
A: Логирование информации о вызове
|
B: Проверка наличия медиафайлов
|
C: Преобразование медиафайлов в data URI (если есть)
|
D: Открытие асинхронной сессии
|
E: Отправка POST-запроса к API с данными
|
F: Итерация по строкам ответа
|
G: Преобразование каждой строки в RawResponse
|
H: Выдача RawResponse через генератор
```

**Примеры**:

```python
# Пример использования create_async_generator с минимальными параметрами
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
async for response in BackendApi.create_async_generator(model=model, messages=messages):
    print(response)

# Пример использования create_async_generator с медиафайлами и ключом API
model = "gpt-4"
messages = [{"role": "user", "content": "Generate a cat image."}]
media = [("path/to/image.jpg", "image/jpeg")]
api_key = "YOUR_API_KEY"
async for response in BackendApi.create_async_generator(model=model, messages=messages, media=media, api_key=api_key):
    print(response)

# Пример использования create_async_generator с дополнительными аргументами
model = "gemini-pro"
messages = [{"role": "user", "content": "Translate to Spanish: Hello"}]
kwargs = {"temperature": 0.7, "max_tokens": 100}
async for response in BackendApi.create_async_generator(model=model, messages=messages, **kwargs):
    print(response)