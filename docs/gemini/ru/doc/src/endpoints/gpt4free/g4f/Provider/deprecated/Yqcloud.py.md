# Модуль `Yqcloud`

## Обзор

Модуль предоставляет асинхронный генератор для взаимодействия с сервисом Yqcloud, который является провайдером GPT-3.5 Turbo. Он позволяет отправлять запросы к API Yqcloud и получать ответы в потоковом режиме. Модуль предназначен для использования в проекте `hypotez` для обеспечения доступа к различным моделям GPT.

## Подробней

Модуль содержит класс `Yqcloud`, который наследуется от `AsyncGeneratorProvider` и реализует метод `create_async_generator` для создания асинхронного генератора. Генератор отправляет запросы к API Yqcloud и возвращает ответы в потоковом режиме.

## Классы

### `Yqcloud`

**Описание**: Класс для взаимодействия с сервисом Yqcloud.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса Yqcloud.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку GPT-3.5 Turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API Yqcloud.

### `create_async_generator`

```python
    async def create_async_generator(
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        **kwargs,
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с API Yqcloud.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания ответа от сервера. По умолчанию `120`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API Yqcloud.
        
        Raises:
            RuntimeError: Если IP-адрес заблокирован из-за обнаружения злоупотреблений.

        Как работает функция:
        - Создает сессию StreamSession с заданными заголовками, прокси и таймаутом.
        - Формирует payload с использованием функции _create_payload.
        - Отправляет POST-запрос к API Yqcloud.
        - Итерируется по чанкам ответа и декодирует их.
        - Проверяет наличие сообщения о блокировке IP-адреса и вызывает исключение RuntimeError в случае обнаружения.
        - Возвращает чанки ответа в потоковом режиме.

        """
```

## Функции

### `_create_header`

```python
def _create_header():
    """
    Создает словарь с заголовками для HTTP-запроса.

    Returns:
        dict: Словарь с заголовками.

    Как работает функция:
    - Функция определяет набор HTTP-заголовков, необходимых для взаимодействия с API.
    - Включает заголовки, такие как "accept", "content-type", "origin" и "referer".
    """
```

### `_create_payload`

```python
def _create_payload(
    messages: Messages,
    system_message: str = "",
    user_id: int = None,
    **kwargs
):
    """
    Создает payload для отправки в API Yqcloud.

    Args:
        messages (Messages): Список сообщений для отправки.
        system_message (str, optional): Системное сообщение. По умолчанию пустая строка.
        user_id (int, optional): ID пользователя. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        dict: Словарь с данными для отправки в API.

    Как работает функция:
    - Функция формирует структуру данных (словарь), содержащую параметры запроса к API.
    - Включает параметры, такие как "prompt" (сформированный из сообщений), "network", "system", "withoutContext", "stream" и "userId".
    - Если user_id не предоставлен, генерирует случайный ID пользователя.
    """