# Документация для модуля `BackendApi`

## Обзор

Модуль `BackendApi` предоставляет класс `BackendApi`, который является асинхронным генератором для взаимодействия с API-интерфейсами бэкенда. Этот класс позволяет отправлять запросы к API, получать ответы в режиме реального времени и обрабатывать медиафайлы.

## Подробнее

Модуль `BackendApi` предназначен для асинхронного взаимодействия с API бэкенда. Он поддерживает отправку сообщений, медиафайлов и других параметров в запросах, а также получение ответов в режиме реального времени с использованием асинхронного генератора.
Этот модуль использует `StreamSession` для асинхронной отправки запросов и обработки ответов, а также `to_data_uri` для преобразования медиафайлов в формат URI.

## Классы

### `BackendApi`

**Описание**: Класс `BackendApi` предоставляет асинхронный генератор для взаимодействия с API бэкенда.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `ssl` (Optional[bool]): Определяет, использовать ли SSL для подключения. По умолчанию `None`.
- `headers` (dict): Заголовки, используемые в запросах к API. По умолчанию пустой словарь `{}`.
- `url` (str): URL-адрес API бэкенда.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для отправки запросов к API.

#### Принцип работы:

Класс `BackendApi` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему использовать функциональность асинхронных генераторов и моделей провайдеров.

1. **Инициализация**:
   - При создании экземпляра класса можно указать параметры SSL и заголовки запросов.

2. **Создание асинхронного генератора**:
   - Метод `create_async_generator()` создает асинхронный генератор, который отправляет запросы к API бэкенда и возвращает ответы в режиме реального времени.

3. **Обработка медиафайлов**:
   - Если в запросе есть медиафайлы, они преобразуются в формат URI с использованием функции `to_data_uri()`.

4. **Отправка запроса**:
   - Используется `StreamSession` для асинхронной отправки POST-запроса к API.

5. **Получение ответов**:
   - Ответы от API возвращаются в виде асинхронного генератора, который выдает объекты `RawResponse` для каждой строки ответа.

## Методы класса

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
        """ Функция создает асинхронный генератор для отправки запросов к API.

        Args:
            cls (BackendApi): Класс `BackendApi`.
            model (str): Имя модели, используемой для генерации ответа.
            messages (Messages): Список сообщений для отправки в запросе.
            media (MediaListType, optional): Список медиафайлов для отправки в запросе. По умолчанию `None`.
            api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные параметры для отправки в запросе.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий объекты `RawResponse` для каждой строки ответа от API.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или обработке ответа.

        Внутренние функции:
            Отсутствуют.

        
            1. Логгирует информацию об API-ключе.
            2. Преобразует медиафайлы в формат URI с использованием функции `to_data_uri()`.
            3. Отправляет POST-запрос к API с использованием `StreamSession`.
            4. Получает ответы от API в виде асинхронного генератора.
            5. Возвращает объекты `RawResponse` для каждой строки ответа.

        Примеры:
            Примеры использования функции `create_async_generator()`:

            >>> async for response in BackendApi.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(response)

            >>> async for response in BackendApi.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Image this'}], media=[('image.png', 'image/png')]):
            ...     print(response)
        """
```

## Параметры класса

- `ssl` (Optional[bool]): Определяет, использовать ли SSL для подключения.
- `headers` (dict): Заголовки, используемые в запросах к API.

## Примеры

Примеры использования класса `BackendApi`:

```python
async for response in BackendApi.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
    print(response)

async for response in BackendApi.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Image this'}], media=[('image.png', 'image/png')]):
    print(response)