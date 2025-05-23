# Модуль GPROChat

## Обзор

Модуль `GPROChat.py` предназначен для взаимодействия с сервисом GPROChat для генерации ответов на основе предоставленных сообщений. Он использует асинхронные запросы для обмена данными с API GPROChat и предоставляет функциональность для работы с различными моделями, поддерживаемыми сервисом. Модуль также включает методы для создания подписи запросов, необходимой для аутентификации.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с сервисом GPROChat. Он содержит класс `GPROChat`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет использовать его для асинхронной генерации ответов и управления моделями. Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов к API GPROChat.

## Классы

### `GPROChat`

**Описание**: Класс `GPROChat` предоставляет функциональность для взаимодействия с сервисом GPROChat. Он позволяет генерировать ответы на основе предоставленных сообщений, используя асинхронные запросы.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса GPROChat.
- `api_endpoint` (str): URL API для генерации ответов.
- `working` (bool): Указывает, работает ли сервис.
- `supports_stream` (bool): Указывает, поддерживает ли сервис потоковую передачу данных.
- `supports_message_history` (bool): Указывает, поддерживает ли сервис историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.

**Принцип работы**:
Класс `GPROChat` использует асинхронные HTTP-запросы для взаимодействия с API GPROChat. Он предоставляет метод `create_async_generator`, который принимает сообщения, модель и другие параметры, и возвращает асинхронный генератор, который выдает ответы от сервиса. Класс также включает метод `generate_signature`, который генерирует подпись запроса для аутентификации.

## Методы класса

### `generate_signature`

```python
    @staticmethod
    def generate_signature(timestamp: int, message: str) -> str:
        """ Функция генерирует подпись для запроса к API GPROChat.

        Args:
            timestamp (int): Временная метка запроса.
            message (str): Сообщение запроса.

        Returns:
            str: Подпись запроса.
        """
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """ Функция создает асинхронный генератор для получения ответов от API GPROChat.

        Args:
            model (str): Модель для генерации ответа.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от API.
        """
```

## Параметры класса

- `url` (str): URL сервиса GPROChat. Используется для указания базового URL сервиса.
- `api_endpoint` (str): URL API для генерации ответов. Используется для указания конечной точки API, к которой отправляются запросы.
- `working` (bool): Указывает, работает ли сервис. Используется для определения доступности сервиса.
- `supports_stream` (bool): Указывает, поддерживает ли сервис потоковую передачу данных. Используется для определения, можно ли получать ответы от сервиса в режиме реального времени.
- `supports_message_history` (bool): Указывает, поддерживает ли сервис историю сообщений. Используется для определения, можно ли отправлять в сервис историю сообщений для получения более релевантных ответов.
- `default_model` (str): Модель, используемая по умолчанию. Используется для указания модели, которая будет использоваться, если не указана другая модель.

## Примеры

**Пример создания подписи запроса:**

```python
timestamp = int(time.time() * 1000)
message = "Hello, GPROChat!"
signature = GPROChat.generate_signature(timestamp, message)
print(signature)
```

**Пример создания асинхронного генератора:**

```python
messages = [{"role": "user", "content": "Hello, GPROChat!"}]
async_generator = GPROChat.create_async_generator(model="gemini-1.5-pro", messages=messages)