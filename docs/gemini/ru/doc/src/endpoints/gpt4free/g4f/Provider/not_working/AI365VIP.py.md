# Модуль AI365VIP

## Обзор

Модуль `AI365VIP` предоставляет реализацию асинхронного генератора для работы с API AI365VIP.  Он наследует базовые классы `AsyncGeneratorProvider` и `ProviderModelMixin` и использует `aiohttp` для взаимодействия с API.

## Подробней

Этот модуль используется в проекте `hypotez` для доступа к API AI365VIP, который представляет собой сервис, предоставляющий доступ к различным моделям обработки естественного языка.  Класс `AI365VIP`  определяет основные параметры и функции для взаимодействия с API.

## Классы

### `class AI365VIP`

**Описание**: Класс `AI365VIP` реализует асинхронный генератор для работы с API AI365VIP.  Он наследует базовые классы `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Класс для асинхронного генератора, используемого для получения результатов от модели.
- `ProviderModelMixin`: Класс, который предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL API AI365VIP.
- `api_endpoint` (str):  Точка входа в API (endpoint).
- `working` (bool): Флаг, указывающий, доступен ли API для работы.
- `default_model` (str): Имя модели по умолчанию для генерации текста.
- `models` (list): Список поддерживаемых моделей для генерации текста.
- `model_aliases` (dict): Словарь для сопоставления имен моделей.

**Методы**:

#### `async def create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:

**Назначение**:  Создает асинхронный генератор для взаимодействия с API. 

**Параметры**:
- `model` (str): Имя модели для генерации текста.
- `messages` (Messages):  Список сообщений для обработки.
- `proxy` (str, optional): Прокси-сервер для соединения с API. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для `ClientSession`.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, который генерирует ответы модели.

**Как работает метод**:

1. Создает экземпляр `ClientSession` с необходимыми заголовками.
2. Формирует данные для запроса к API, включая имя модели, список сообщений и другие параметры.
3. Выполняет POST-запрос к API с использованием `session.post`.
4. Обрабатывает ответ от API и генерирует фрагменты данных (chuncks) через `response.content`. 
5. Возвращает асинхронный результат, который будет генерировать обработанные фрагменты данных.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

model_name = "gpt-3.5-turbo"
messages: Messages = [{"role": "user", "content": "Hello, world!"}]

async def main():
    async for chunk in await AI365VIP.create_async_generator(model=model_name, messages=messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Параметры класса

- `url` (str): Базовый URL API AI365VIP.
- `api_endpoint` (str): Точка входа в API (endpoint).
- `working` (bool): Флаг, указывающий, доступен ли API для работы.
- `default_model` (str): Имя модели по умолчанию для генерации текста.
- `models` (list): Список поддерживаемых моделей для генерации текста.
- `model_aliases` (dict): Словарь для сопоставления имен моделей.

## Примеры

- Создание экземпляра класса:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP

provider = AI365VIP() 
```

- Использование метода `create_async_generator`:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [{"role": "user", "content": "Hello, world!"}]
model_name = "gpt-3.5-turbo"

async def main():
    async for chunk in await AI365VIP.create_async_generator(model=model_name, messages=messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```