# Модуль CodeLinkAva - Провайдер GPT4Free

## Обзор

Модуль `CodeLinkAva` предоставляет асинхронный генератор для получения ответов от модели CodeLink Ava, которая реализует API GPT4Free.

## Подробней

**CodeLink Ava** - это один из провайдеров GPT4Free, который использует API CodeLink Ava для взаимодействия с моделью. Этот провайдер доступен в `hypotez` и предоставляет возможность генерировать текст, переводить, писать код и выполнять другие задачи с помощью модели GPT.

**P.S.**  Этот провайдер в настоящий момент **устарел** и не поддерживается.

## Классы

### `CodeLinkAva`

**Описание**: Класс `CodeLinkAva` реализует асинхронный генератор для получения ответов от модели CodeLink Ava.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API сервиса CodeLink Ava.
- `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `working (bool)`: Показывает, доступен ли провайдер для работы. 

**Методы**:

- `create_async_generator(model: str, messages: list[dict[str, str]], **kwargs) -> AsyncGenerator`: Создает асинхронный генератор для получения ответов от модели CodeLink Ava.

## Функции

### `create_async_generator(model: str, messages: list[dict[str, str]], **kwargs) -> AsyncGenerator`

**Назначение**: Создает асинхронный генератор, который позволяет по частям получать ответы от модели CodeLink Ava.

**Параметры**:

- `model (str)`: Имя модели GPT, например, `"gpt-3.5-turbo"`.
- `messages (list[dict[str, str]])`: Список сообщений, которые отправляются модели.
- `**kwargs`: Дополнительные параметры для модели.

**Возвращает**:

- `AsyncGenerator`: Асинхронный генератор, который поставляет частичные ответы от модели CodeLink Ava.

**Как работает функция**:

- Функция отправляет запрос к API CodeLink Ava с использованием библиотеки `aiohttp`.
- В запросе передаются:
    - Список сообщений `messages`.
    - Имя модели `model`.
    - Дополнительные параметры `kwargs`.
- Функция получает ответ от API и использует асинхронный генератор для передачи данных по частям.
- Генератор `yield``ит` частичные ответы от модели CodeLink Ava.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.CodeLinkAva import CodeLinkAva

async def example():
    messages = [
        {
            "role": "user",
            "content": "Привет, напиши мне короткий рассказ о коте."
        }
    ]
    async for chunk in CodeLinkAva.create_async_generator(model='gpt-3.5-turbo', messages=messages):
        print(chunk, end='')