# Модуль Hashnode
## Обзор

Модуль `Hashnode.py` предоставляет класс `Hashnode`, который является асинхронным провайдером для взаимодействия с API Hashnode. Он используется для получения ответов от модели, поддерживающей контекст диалога, GPT-3.5 Turbo и поиск в интернете. Этот модуль предназначен для интеграции с системой `gpt4free` в проекте `hypotez`.

## Подробней

Модуль позволяет отправлять запросы к API Hashnode для получения ответов от модели, используя предоставленные сообщения и параметры поиска. Он также поддерживает использование прокси-серверов для обхода ограничений сети.

## Классы

### `SearchTypes`

**Описание**: Класс `SearchTypes` содержит константы, определяющие типы поиска, которые могут быть использованы при запросе к API Hashnode.

**Атрибуты**:
- `quick` (str): Тип быстрого поиска.
- `code` (str): Тип поиска кода.
- `websearch` (str): Тип поиска в интернете.

### `Hashnode`

**Описание**: Класс `Hashnode` является асинхронным провайдером для взаимодействия с API Hashnode.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора провайдера.

**Атрибуты**:
- `url` (str): URL API Hashnode.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `_sources` (list): Список источников, полученных в результате поиска.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API Hashnode.
- `get_sources`: Возвращает список источников, использованных для генерации ответа.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    search_type: str = SearchTypes.websearch,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API Hashnode.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений, представляющих историю разговора.
        search_type (str): Тип поиска, который будет использоваться (по умолчанию "websearch").
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API Hashnode.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при выполнении запроса к API Hashnode.

    Как работает функция:
    - Формирует заголовки запроса, включая User-Agent, Accept и другие необходимые параметры.
    - Создает асинхронную сессию с использованием библиотеки `aiohttp`.
    - Извлекает последний запрос пользователя из истории сообщений.
    - Очищает список источников `_sources`.
    - Если указан тип поиска "websearch", выполняет поисковый запрос к API Hashnode и сохраняет результаты в `_sources`.
    - Формирует данные запроса, включая историю сообщений, запрос пользователя, тип поиска и результаты поиска.
    - Отправляет POST-запрос к API Hashnode с данными запроса.
    - Получает ответ от API Hashnode и генерирует асинхронный поток данных, возвращающий ответ частями.
    """
```

### `get_sources`

```python
@classmethod
def get_sources(cls) -> list:
    """
    Возвращает список источников, использованных для генерации ответа.

    Returns:
        list: Список словарей, содержащих заголовок и URL каждого источника.

    Как работает функция:
    - Формирует список словарей, каждый из которых содержит заголовок и URL источника.
    - Возвращает сформированный список.
    """
```

## Параметры класса

- `url` (str): URL API Hashnode.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `_sources` (list): Список источников, полученных в результате поиска.

## Примеры
```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode, SearchTypes
import asyncio

async def main():
    messages = [{"role": "user", "content": "Как создать веб-сайт?"}]
    async_generator = Hashnode.create_async_generator(model="gpt-3.5-turbo", messages=messages, search_type=SearchTypes.websearch)
    
    result = await async_generator
    async for message in result:
        print(message, end="")

    sources = Hashnode.get_sources()
    print("\nИсточники:")
    for source in sources:
        print(f"- {source['title']}: {source['url']}")

if __name__ == "__main__":
    asyncio.run(main())
```
Этот пример показывает, как использовать класс `Hashnode` для получения ответа на вопрос "Как создать веб-сайт?" с использованием поиска в интернете и последующего вывода результата и списка источников.
```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode, SearchTypes
import asyncio

async def main():
    messages = [{"role": "user", "content": "Напиши функцию на Python, которая сортирует список чисел."}]
    async_generator = Hashnode.create_async_generator(model="gpt-3.5-turbo", messages=messages, search_type=SearchTypes.code)
    
    result = await async_generator
    async for message in result:
        print(message, end="")

    sources = Hashnode.get_sources()
    print("\nИсточники:")
    for source in sources:
        print(f"- {source['title']}: {source['url']}")

if __name__ == "__main__":
    asyncio.run(main())
```
В этом примере демонстрируется запрос на создание функции сортировки списка чисел с использованием типа поиска `SearchTypes.code`.
```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode, SearchTypes
import asyncio

async def main():
    messages = [{"role": "user", "content": "Что такое машинное обучение?"}]
    async_generator = Hashnode.create_async_generator(model="gpt-3.5-turbo", messages=messages, search_type=SearchTypes.quick)
    
    result = await async_generator
    async for message in result:
        print(message, end="")

    sources = Hashnode.get_sources()
    print("\nИсточники:")
    for source in sources:
        print(f"- {source['title']}: {source['url']}")

if __name__ == "__main__":
    asyncio.run(main())
```
В данном примере показано использование быстрого поиска (`SearchTypes.quick`) для получения информации о машинном обучении.