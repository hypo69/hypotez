# Документация для модуля `Ylokh.py`

## Описание

Модуль `Ylokh.py` предоставляет реализацию асинхронного генератора для взаимодействия с сервисом `chat.ylokh.xyz`. Он позволяет отправлять запросы к API для получения ответов в режиме стриминга или полной выдачи, поддерживая модели GPT-3.5 Turbo.

## Оглавление

- [Описание](#описание)
- [Классы](#классы)
    - [Ylokh](#ylokh)
        - [create_async_generator](#create_async_generator)

## Классы

### `Ylokh`

**Описание**:
Класс `Ylokh` является провайдером асинхронного генератора, предназначенным для взаимодействия с API `chat.ylokh.xyz`.

**Наследует**:
- `AsyncGeneratorProvider`: Класс наследует функциональность асинхронного генератора от `AsyncGeneratorProvider`.

**Атрибуты**:
- `url` (str): URL сервиса `chat.ylokh.xyz`.
- `working` (bool): Индикатор работоспособности провайдера (в данном случае `False`).
- `supports_message_history` (bool): Поддержка истории сообщений (`True`).
- `supports_gpt_35_turbo` (bool): Поддержка модели GPT-3.5 Turbo (`True`).

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    timeout: int = 120,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API `chat.ylokh.xyz`.

    Args:
        cls (Ylokh): Ссылка на класс `Ylokh`.
        model (str): Используемая модель (например, "gpt-3.5-turbo").
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Флаг для включения стриминга ответов. По умолчанию `True`.
        proxy (str, optional): Адрес прокси-сервера для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий части ответа или полный ответ.

    Raises:
        Exception: Возникает при ошибках HTTP-запроса или обработки данных.
    """
```

**Как работает функция**:

1. **Подготовка параметров**:
   - Функция извлекает или устанавливает параметры, такие как используемая модель, заголовки запроса и данные для отправки.
2. **Создание асинхронной сессии**:
   - Используется `StreamSession` для выполнения асинхронных HTTP-запросов с поддержкой стриминга.
   - Устанавливаются заголовки `Origin` и `Referer` для имитации запроса от веб-страницы.
   - Формируется полезная нагрузка (`data`) с сообщениями, моделью, параметрами температуры, штрафами и другими настройками.
3. **Отправка запроса и обработка ответа**:
   - Отправляется `POST`-запрос к API `https://chatapi.ylokh.xyz/v1/chat/completions`.
   - Если включен режим стриминга (`stream=True`), функция итерируется по строкам ответа:
     - Каждая строка декодируется.
     - Если строка начинается с `data: `, она обрабатывается как JSON.
     - Если строка `data: [DONE]`, генерация завершается.
     - Извлекается содержимое (`content`) из JSON и передается через `yield`.
   - Если режим стриминга выключен (`stream=False`), функция ожидает полный JSON-ответ:
     - Извлекается содержимое (`content`) из полного ответа и возвращается через `yield`.
4. **Обработка ошибок**:
   - `response.raise_for_status()` вызывает исключение для HTTP-кодов ошибок.

**Примеры**:

Пример использования функции `create_async_generator` для получения стримингового ответа:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Ylokh import Ylokh

async def main():
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    async for token in Ylokh.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(token, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

Пример использования функции `create_async_generator` для получения полного ответа без стриминга:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.Ylokh import Ylokh

async def main():
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    result = [token async for token in Ylokh.create_async_generator(model="gpt-3.5-turbo", messages=messages, stream=False)]
    print("".join(result))

if __name__ == "__main__":
    asyncio.run(main())