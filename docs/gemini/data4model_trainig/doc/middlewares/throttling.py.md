# Модуль промежуточного слоя для управления троттлингом

## Обзор

Модуль `src.endpoints.bots.telegram.movie_bot-main/middlewares/throttling.py` предоставляет промежуточное программное обеспечение (middleware) для управления троттлингом сообщений в Telegram-боте.

## Подробней

Модуль содержит класс `ThrottlingMiddleware`, который использует библиотеку `cachetools` для ограничения частоты отправки сообщений пользователями.

## Классы

### `ThrottlingMiddleware`

**Описание**: Мидлварь для управления троттлингом сообщений.

**Атрибуты**:

*   `limit` (TTLCache): Кэш для хранения информации о пользователях и времени их последнего сообщения.

**Методы**:

*   `__init__(self, time_limit: int = 2) -> None`: Инициализирует мидлварь с заданным временным ограничением.
*   `__call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any`: Основной метод мидлвари, вызываемый для обработки сообщения.

## Методы класса `ThrottlingMiddleware`

### `__init__`

```python
def __init__(self, time_limit: int = 2) -> None:
```

**Назначение**: Инициализирует мидлварь с заданным временным ограничением.

**Параметры**:

*   `time_limit` (int, optional): Временное ограничение в секундах (по умолчанию 2).

**Как работает функция**:

1.  Инициализирует атрибут `limit` с экземпляром класса `TTLCache`, устанавливая максимальный размер кэша и время жизни (TTL).

### `__call__`

```python
async def __call__(
    self,
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    event: Message,
    data: Dict[str, Any]
) -> Any:
```

**Назначение**: Обрабатывает входящие сообщения и применяет троттлинг.

**Параметры**:

*   `handler` (Callable): Функция-обработчик, которая будет вызвана.
*   `event` (Message): Объект сообщения Telegram.
*   `data` (Dict[str, Any]): Словарь данных.

**Возвращает**:

*   Результат выполнения обработчика.

**Как работает функция**:

1.  Проверяет, находится ли ID чата в кэше `limit`.
2.  Если ID чата находится в кэше, функция завершается, и сообщение не обрабатывается (троттлинг).
3.  Если ID чата отсутствует в кэше, добавляет ID чата в кэш и вызывает функцию-обработчик.