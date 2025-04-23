# Модуль `ChatgptDuo.py`

## Обзор

Модуль предоставляет асинхронный класс `ChatgptDuo`, который является провайдером для взаимодействия с моделью, расположенной по адресу "https://chatgptduo.com". Он поддерживает модель `gpt-3.5-turbo` и предназначен для обработки запросов к этой модели.

## Подробнее

Этот модуль интегрируется с асинхронными запросами через `StreamSession` для отправки запросов к API `ChatgptDuo`. Он форматирует сообщения, отправляет их на сервер и извлекает ответы, а также информацию об источниках, использованных для формирования ответа.

## Классы

### `ChatgptDuo`

**Описание**: Асинхронный провайдер для взаимодействия с моделью `ChatgptDuo`.

**Наследует**:
- `AsyncProvider`: Этот класс наследует функциональность асинхронного провайдера.

**Атрибуты**:
- `url` (str): URL-адрес сервиса `ChatgptDuo` ("https://chatgptduo.com").
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo` (`True`).
- `working` (bool): Указывает, находится ли провайдер в рабочем состоянии (`False`).
- `_sources` (list): Список источников, используемых для формирования ответа.

**Методы**:
- `create_async`: Асинхронный метод для создания запроса и получения ответа от `ChatgptDuo`.
- `get_sources`: Метод для получения источников, использованных при формировании ответа.

## Методы класса

### `create_async`

```python
@classmethod
async def create_async(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    **kwargs
) -> str:
    """
    Асинхронно создает запрос к ChatgptDuo и возвращает ответ.

    Args:
        cls (ChatgptDuo): Ссылка на класс.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Ответ от ChatgptDuo.
    """
```

**Описание**:
Метод `create_async` является асинхронным методом класса, который отправляет запрос к `ChatgptDuo` и возвращает ответ. Он использует `StreamSession` для выполнения HTTP-запроса с заданными параметрами, такими как прокси и таймаут.

**Параметры**:
- `cls` (ChatgptDuo): Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
- `**kwargs`: Дополнительные аргументы.

**Как работает функция**:
1. Создается асинхронная сессия с использованием `StreamSession` с заданными параметрами, такими как `impersonate`, `proxies` и `timeout`.
2. Форматируется запрос из списка сообщений с использованием `format_prompt`.
3. Подготавливаются данные для отправки в теле запроса, включающие `prompt`, `search` и `purpose`.
4. Отправляется POST-запрос на URL-адрес `ChatgptDuo` с подготовленными данными.
5. Проверяется статус ответа и генерируется исключение, если статус не 200.
6. Извлекается JSON-ответ из ответа сервера.
7. Извлекаются источники, использованные для формирования ответа, и сохраняются в `cls._sources`.
8. Возвращается текст ответа из JSON-данных.

**Примеры**:

```python
# Пример асинхронного вызова create_async
import asyncio
from typing import List, Dict, Any, Optional

class ChatgptDuo:
    url: str = "https://chatgptduo.com"
    supports_gpt_35_turbo: bool = True
    working: bool = False
    _sources: List[Dict[str, str]] = []

    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: List[Dict[str, str]],
        proxy: Optional[str] = None,
        timeout: int = 120,
        **kwargs: Any,
    ) -> str:
        """
        Асинхронно создает запрос к ChatgptDuo и возвращает ответ.

        Args:
            cls (ChatgptDuo): Ссылка на класс.
            model (str): Имя используемой модели.
            messages (List[Dict[str, str]]): Список сообщений для отправки.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Ответ от ChatgptDuo.
        """
        return "Пример ответа от ChatgptDuo"  # Заглушка для примера

    @classmethod
    def get_sources(cls) -> List[Dict[str, str]]:
        """
        Возвращает источники, использованные при формировании ответа.

        Returns:
            List[Dict[str, str]]: Список источников.
        """
        return cls._sources  # Заглушка для примера

async def main():
    messages = [{"role": "user", "content": "Hello, ChatgptDuo!"}]
    answer = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
```

### `get_sources`

```python
@classmethod
def get_sources(cls):
    """
    Возвращает источники, использованные при формировании ответа.

    Returns:
        list: Список источников.
    """
```

**Описание**:
Метод `get_sources` является методом класса, который возвращает список источников, использованных при формировании ответа.

**Параметры**:
- `cls` (ChatgptDuo): Ссылка на класс.

**Как работает функция**:
Функция просто возвращает значение атрибута `cls._sources`.

**Примеры**:

```python
# Пример вызова get_sources
class ChatgptDuo:
    _sources: list = [{"title": "Example", "url": "http://example.com", "snippet": "Example snippet"}]

    @classmethod
    def get_sources(cls):
        """
        Возвращает источники, использованные при формировании ответа.

        Returns:
            list: Список источников.
        """
        return cls._sources

sources = ChatgptDuo.get_sources()
print(sources)
# Вывод: [{'title': 'Example', 'url': 'http://example.com', 'snippet': 'Example snippet'}]
```