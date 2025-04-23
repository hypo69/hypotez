# Модуль `AI365VIP`

## Обзор

Модуль предоставляет асинхронный доступ к API AI365VIP для генерации текста на основе моделей GPT.
Он включает в себя настройки для подключения к API, выбора модели и форматирования запросов.

## Подробнее

Модуль предназначен для интеграции с AI365VIP для использования моделей GPT в асинхронном режиме.
Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет
удобный интерфейс для взаимодействия с API.

## Классы

### `AI365VIP`

**Описание**: Класс предоставляет асинхронный генератор для взаимодействия с API AI365VIP.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров.
- `ProviderModelMixin`: Добавляет поддержку выбора и управления моделями.

**Атрибуты**:
- `url` (str): URL API AI365VIP.
- `api_endpoint` (str): Endpoint API для чата.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-3.5-turbo`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:

Класс `AI365VIP` предназначен для асинхронного взаимодействия с API AI365VIP для генерации текста. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов. Основной метод `create_async_generator` отправляет запрос к API и возвращает асинхронный генератор, который выдает чанки сгенерированного текста.

## Методы класса

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
        """ Функция создает асинхронный генератор для получения ответов от API AI365VIP.

        Args:
            model (str): Название используемой модели.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий чанки текста.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

        Внутренние функции:
            Нет внутренних функций.

        
            1. Формирует HTTP-заголовки для запроса.
            2. Создает асинхронную сессию `aiohttp.ClientSession` с заданными заголовками.
            3. Формирует данные запроса в формате JSON, включая модель, сообщения и параметры.
            4. Отправляет POST-запрос к API AI365VIP.
            5. Получает ответ и проверяет статус.
            6. Возвращает асинхронный генератор, который выдает чанки текста из ответа.
        """
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = "gpt-3.5-turbo"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None

    async for chunk in AI365VIP.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())