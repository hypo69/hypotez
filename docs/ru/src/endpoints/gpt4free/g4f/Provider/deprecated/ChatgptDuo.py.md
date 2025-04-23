# Документация для модуля ChatgptDuo

## Обзор

Модуль `ChatgptDuo` предоставляет асинхронный интерфейс для взаимодействия с сервисом chatgptduo.com. Он позволяет отправлять запросы к модели GPT-3.5-turbo и получать ответы. Модуль поддерживает использование прокси и предоставляет возможность получения источников, на основе которых был сформирован ответ.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения доступа к альтернативным источникам GPT-моделей через API chatgptduo.com. Он использует асинхронные запросы для неблокирующего взаимодействия с сервисом.

## Классы

### `ChatgptDuo`

**Описание**: Класс `ChatgptDuo` является асинхронным провайдером, который предоставляет доступ к модели GPT-3.5-turbo через сервис chatgptduo.com.
**Наследует**: `AsyncProvider` - базовый класс для асинхронных провайдеров.
**Атрибуты**:
- `url` (str): URL сервиса chatgptduo.com.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5-turbo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_sources` (list): Список источников, используемых для формирования ответа.

**Принцип работы**:

1.  Метод `create_async` отправляет запрос к API chatgptduo.com с использованием предоставленных сообщений и параметров.
2.  Полученный ответ преобразуется в строку и возвращается.
3.  Метод `get_sources` возвращает список источников, использованных для формирования ответа.

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
    """ Асинхронно отправляет запрос к сервису chatgptduo.com и возвращает ответ.

    Args:
        cls (ChatgptDuo): Ссылка на класс.
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
        **kwargs: Дополнительные параметры.

    Returns:
        str: Ответ от сервиса chatgptduo.com.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    
    - Функция принимает модель, список сообщений, прокси (опционально), таймаут и дополнительные параметры.
    - Cоздается сессия StreamSession с заданными параметрами, включая impersonate="chrome107" для имитации браузера Chrome 107.
    - Формируется тело запроса, включающее prompt и search на основе предоставленных messages.
    - Отправляется POST-запрос к сервису chatgptduo.com.
    - Обрабатывается ответ, извлекаются источники и сам ответ.

    Внутренние функции:
        Отсутствуют.
    """
```

### `get_sources`

```python
@classmethod
def get_sources(cls):
    """ Возвращает список источников, использованных для формирования ответа.

    Args:
        cls (ChatgptDuo): Ссылка на класс.

    Returns:
        list: Список источников, каждый из которых содержит заголовок, URL и фрагмент текста.

    
    - Функция возвращает атрибут `_sources` класса, который содержит список источников.

    Внутренние функции:
        Отсутствуют.
    """
```

## Параметры класса

- `url` (str): URL сервиса chatgptduo.com.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5-turbo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_sources` (list): Список источников, используемых для формирования ответа.

## Примеры

Пример использования класса `ChatgptDuo`:

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.ChatgptDuo import ChatgptDuo
from src.logger import logger

import asyncio

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    try:
        answer = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
        print(f"Answer: {answer}")
        sources = ChatgptDuo.get_sources()
        print(f"Sources: {sources}")
    except Exception as ex:
        logger.error(f"Error: {ex}", ex, exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())