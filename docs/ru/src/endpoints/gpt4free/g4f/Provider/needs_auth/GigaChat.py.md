# Модуль GigaChat

## Обзор

Модуль `GigaChat.py` предоставляет асинхронный интерфейс для взаимодействия с API GigaChat от Сбербанка. Он обеспечивает поддержку стриминга, истории сообщений и системных сообщений. Модуль требует аутентификации через API-ключ и поддерживает несколько моделей GigaChat.

## Подробней

Модуль предназначен для интеграции в проекты, требующие взаимодействия с GigaChat API. Он автоматически обновляет токен доступа и поддерживает работу через прокси-серверы. Для безопасного соединения используется SSL-контекст с доверенным сертификатом.

## Классы

### `GigaChat`

**Описание**: Класс `GigaChat` является асинхронным провайдером для работы с API GigaChat. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Аттрибуты**:
- `url` (str): URL API GigaChat (`"https://developers.sber.ru/gigachat"`).
- `working` (bool): Указывает, что провайдер в рабочем состоянии (`True`).
- `supports_message_history` (bool): Поддержка истории сообщений (`True`).
- `supports_system_message` (bool): Поддержка системных сообщений (`True`).
- `supports_stream` (bool): Поддержка потоковой передачи данных (`True`).
- `needs_auth` (bool): Требуется аутентификация (`True`).
- `default_model` (str): Модель по умолчанию (`"GigaChat:latest"`).
- `models` (list): Список поддерживаемых моделей (`["GigaChat:latest", "GigaChat-Plus", "GigaChat-Pro"]`).

**Методы**:
- `create_async_generator()`: Асинхронный генератор для взаимодействия с API GigaChat.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            stream: bool = True,
            proxy: str = None,
            api_key: str = None,
            connector: BaseConnector = None,
            scope: str = "GIGACHAT_API_PERS",
            update_interval: float = 0,
            **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для взаимодействия с API GigaChat.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг потоковой передачи данных. По умолчанию `True`.
            proxy (str): URL прокси-сервера. По умолчанию `None`.
            api_key (str): API-ключ для аутентификации. По умолчанию `None`.
            connector (BaseConnector): Асинхронный коннектор. По умолчанию `None`.
            scope (str): Область действия для токена доступа. По умолчанию `"GIGACHAT_API_PERS"`.
            update_interval (float): Интервал обновления. По умолчанию `0`.
            **kwargs: Дополнительные аргументы для API GigaChat.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API GigaChat.

        Raises:
            MissingAuthError: Если отсутствует API-ключ.

        """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API GigaChat.

**Параметры**:
- `cls`: Ссылка на класс `GigaChat`.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool): Флаг потоковой передачи данных. По умолчанию `True`.
- `proxy` (str): URL прокси-сервера. По умолчанию `None`.
- `api_key` (str): API-ключ для аутентификации. По умолчанию `None`.
- `connector` (BaseConnector): Асинхронный коннектор. По умолчанию `None`.
- `scope` (str): Область действия для токена доступа. По умолчанию `"GIGACHAT_API_PERS"`.
- `update_interval` (float): Интервал обновления. По умолчанию `0`.
- `**kwargs`: Дополнительные аргументы для API GigaChat.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API GigaChat.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует API-ключ.

**Как работает функция**:

1. **Проверка наличия API-ключа**: Проверяет, передан ли `api_key`. Если ключ отсутствует, вызывает исключение `MissingAuthError`.
2. **Создание файла сертификата**: Создает файл `russian_trusted_root_ca.crt` в каталоге cookies, если он еще не существует.
3. **Создание SSL-контекста**: Если `has_ssl` и `connector` равны `None`, создает SSL-контекст с использованием сертификата.
4. **Создание асинхронной сессии**: Создает асинхронную сессию с использованием `ClientSession` и переданного коннектора (или созданного на основе прокси).
5. **Обновление токена доступа**: Проверяет, истек ли срок действия текущего токена доступа. Если токен истек или скоро истечет, отправляет запрос на обновление токена.
6. **Отправка запроса в API GigaChat**: Отправляет POST-запрос к API GigaChat с использованием обновленного токена доступа.
7. **Обработка потоковых данных**: Если `stream` равен `True`, обрабатывает потоковые данные, возвращаемые API. Если `stream` равен `False`, возвращает полный ответ после завершения запроса.

**Внутренние функции**: Нет

```
    A: Проверка API-ключа
    |
    B: Создание SSL-контекста
    |
    C: Создание асинхронной сессии
    |
    D: Проверка срока действия токена
    |
    E: Обновление токена доступа
    |
    F: Отправка запроса в API GigaChat
    |
    G: Обработка потоковых данных
```

**Примеры**:

```python
# Пример использования create_async_generator
api_key = "your_api_key"
messages = [{"role": "user", "content": "Hello, GigaChat!"}]
model = "GigaChat:latest"

async def main():
    generator = await GigaChat.create_async_generator(model=model, messages=messages, api_key=api_key)
    async for message in generator:
        print(message, end="")

# Запуск примера
# asyncio.run(main())