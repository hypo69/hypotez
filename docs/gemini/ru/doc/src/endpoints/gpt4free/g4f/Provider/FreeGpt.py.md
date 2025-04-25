# Модуль FreeGpt

## Обзор

Модуль `FreeGpt` предоставляет реализацию асинхронного генератора для взаимодействия с бесплатным API GPT. 

## Подробнее

Этот модуль реализует класс `FreeGpt`, который наследует от базовых классов `AsyncGeneratorProvider` и `ProviderModelMixin`. `FreeGpt` предоставляет возможность отправлять запросы к API с использованием асинхронного генератора, позволяя получать ответ в виде последовательных частей.

## Классы

### `class FreeGpt`

**Описание**: Класс `FreeGpt` реализует асинхронный генератор для взаимодействия с бесплатным API GPT.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Базовый класс, предоставляющий функциональность для работы с моделями GPT.

**Атрибуты**:

- `url` (str): Базовый URL API GPT.
- `working` (bool): Флаг, указывающий на доступность API.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `default_model` (str): Название модели GPT по умолчанию.
- `models` (list): Список доступных моделей GPT.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: Optional[str] = None, timeout: int = 120, **kwargs: Any) -> AsyncGenerator[str, None]`
  - **Назначение**:  Создает асинхронный генератор, который отправляет запрос к API и возвращает части ответа.
  - **Параметры**:
    - `model` (str): Название модели GPT.
    - `messages` (list): Список сообщений для запроса.
    - `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
    - `timeout` (int): Максимальное время ожидания ответа. По умолчанию 120 секунд.
    - `**kwargs` (Any): Дополнительные параметры для запроса.
  - **Возвращает**:
    - `AsyncGenerator[str, None]`: Асинхронный генератор, возвращающий части ответа.

- `_build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]`
  - **Назначение**: Формирует данные для запроса к API GPT.
  - **Параметры**:
    - `messages` (list): Список сообщений для запроса.
    - `prompt` (str): Текст запроса.
    - `timestamp` (int): Текущее время в секундах.
    - `secret` (str, optional): Секретный ключ для подписи запроса. По умолчанию `""`.
  - **Возвращает**:
    - `Dict[str, Any]`: Словарь с данными для запроса.

## Функции

### `generate_signature(timestamp: int, message: str, secret: str = "") -> str`

**Назначение**:  Создает хэш-подпись для запроса к API GPT.

**Параметры**:

- `timestamp` (int): Текущее время в секундах.
- `message` (str): Текст запроса.
- `secret` (str, optional): Секретный ключ для подписи. По умолчанию `""`.

**Возвращает**:

- `str`: Хэш-подпись запроса.

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Использование `execute_locator`
close_banner = {
    "attribute": null,
    "by": "XPATH",
    "selector": "//button[@id = 'closeXButton']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

```python
# Пример использования FreeGpt
from hypotez.src.endpoints.gpt4free.g4f.Provider.FreeGpt import FreeGpt

async def main():
    # Создание инстанса FreeGpt
    gpt = FreeGpt()

    # Список сообщений для запроса
    messages = [
        {"role": "user", "content": "Привет! Как дела?"}
    ]

    # Отправка запроса к API
    async for chunk in gpt.create_async_generator(model="gemini-1.5-pro", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
```markdown