# Модуль ChatGptt
## Обзор

Модуль `ChatGptt` предоставляет асинхронный генератор для взаимодействия с моделью ChatGptt через API. Он поддерживает потоковую передачу данных и позволяет использовать системные сообщения и историю сообщений. Модуль предназначен для интеграции с другими частями проекта `hypotez` для обеспечения функциональности чат-бота.

## Подробнее

Этот модуль предназначен для работы с API ChatGptt, предоставляя функциональность для отправки сообщений и получения ответов в асинхронном режиме. Он использует `aiohttp` для выполнения HTTP-запросов и реализует логику для извлечения необходимых токенов аутентификации из HTML-страницы. Модуль поддерживает различные модели, включая `gpt-4`, `gpt-4o` и `gpt-4o-mini`.

## Классы

### `ChatGptt`

**Описание**: Класс `ChatGptt` предоставляет методы для взаимодействия с API ChatGptt. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL главной страницы ChatGptt.
- `api_endpoint` (str): URL API для отправки сообщений.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от API ChatGptt.

## Функции

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
        """Создает асинхронный генератор для получения ответов от API ChatGptt.

        Args:
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Raises:
            RuntimeError: Если не удается найти токены аутентификации в HTML-странице.

        Пример:
            >>> async for message in ChatGptt.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(message)
        """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API ChatGptt.

**Параметры**:
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `RuntimeError`: Если не удается найти токены аутентификации в HTML-странице.

**Как работает функция**:

1. **Подготовка**:
   - Получает модель, используя `cls.get_model(model)`.
   - Формирует заголовки HTTP-запроса, включая `authority`, `accept`, `origin`, `referer` и `user-agent`.

2. **Извлечение токенов аутентификации**:
   - Отправляет GET-запрос на главную страницу `cls.url` для получения HTML-содержимого.
   - Извлекает значения `nonce_` и `post_id` из HTML, используя регулярные выражения.

3. **Формирование полезной нагрузки (payload)**:
   - Создает словарь `payload` с параметрами, необходимыми для API-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message`, `bot_id`, `chatbot_identity` и `wpaicg_chat_client_id`.

4. **Отправка запроса и получение ответа**:
   - Отправляет POST-запрос на `cls.api_endpoint` с заголовками и полезной нагрузкой.
   - Получает JSON-ответ и извлекает данные из поля `data`.
   - Передает полученные данные через `yield`, делая функцию генератором.

```
    Начало работы
     │
     │ Получение модели
     │
     ▼
     Создание заголовков HTTP-запроса
     │
     │ Получение HTML-содержимого страницы
     │
     ▼
     Извлечение nonce и post_id из HTML
     │
     │  Проверка наличия nonce и post_id
     │  ├── Нет: Выброс RuntimeError
     │  └── Да:
     │
     ▼
     Формирование payload с данными для запроса
     │
     │ Отправка POST-запроса к API
     │
     ▼
     Получение JSON-ответа и извлечение данных из поля 'data'
     │
     │ Передача данных через yield
     │
     ▼
    Конец работы
```

**Примеры**:

```python
async for message in ChatGptt.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}]):
    print(message)
```

```python
async for message in ChatGptt.create_async_generator(model='gpt-4o', messages=[{'role': 'user', 'content': 'Как дела?'}], proxy='http://proxy.example.com'):
    print(message)