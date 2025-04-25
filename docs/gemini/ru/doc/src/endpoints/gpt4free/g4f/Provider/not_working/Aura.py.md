# Aura - Провайдер для Aura API 

## Обзор

Этот файл содержит класс `Aura`, который реализует асинхронный генератор для взаимодействия с Aura API, предоставляя возможности для общения с моделями искусственного интеллекта.

## Подробней

Класс `Aura` наследует от `AsyncGeneratorProvider` и реализует асинхронный генератор для взаимодействия с Aura API. Он отправляет запросы с данными о модели, сообщениями, настройками (температура, максимальное количество токенов) и прокси-сервером. В ответ Aura API возвращает поток данных, который преобразуется в асинхронный генератор.

## Классы

### `class Aura`

**Описание**: Класс `Aura` реализует асинхронный генератор для работы с Aura API.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API Aura.
- `working (bool)`: Флаг, указывающий на работоспособность провайдера (в данном случае `False`, поскольку Aura API не работает).

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, temperature: float = 0.5, max_tokens: int = 8192, webdriver = None, **kwargs) -> AsyncResult`: 
    - **Назначение**: Создает асинхронный генератор для взаимодействия с Aura API. 
    - **Параметры**:
        - `model (str)`: Идентификатор модели.
        - `messages (Messages)`: Список сообщений.
        - `proxy (str, optional)`: Прокси-сервер. По умолчанию `None`.
        - `temperature (float, optional)`: Температура модели. По умолчанию `0.5`.
        - `max_tokens (int, optional)`: Максимальное количество токенов. По умолчанию `8192`.
        - `webdriver (Optional[Driver], optional)`: Веб-драйвер для получения аргументов. По умолчанию `None`.
        - `**kwargs`: Дополнительные аргументы.
    - **Возвращает**: `AsyncResult`: Асинхронный результат, который может быть преобразован в текст ответа.
    - **Как работает функция**:
        -  Извлекает аргументы (куки, заголовки) из веб-драйвера, если он предоставлен.
        -  Создает сессию `aiohttp.ClientSession` с полученными аргументами.
        -  Разделяет сообщения на системные (role: "system") и обычные.
        -  Формирует данные для запроса в формате JSON, включая модель, сообщения, ключ API (который не используется), системные сообщения, температуру и максимальное количество токенов.
        -  Отправляет POST-запрос на `https://openchat.team/api/chat` с данными.
        -  Перехватывает ошибки с использованием `response.raise_for_status()`.
        -  Использует `async for` для итерации по частям ответа и декодирования их в строки.
        -  Возвращает асинхронный генератор, который может быть использован для получения текста ответа.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Aura import Aura
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages([
    {"role": "system", "content": "Ты ассистент, помогающий людям"},
    {"role": "user", "content": "Привет!"},
])

async def main():
    async for chunk in Aura.create_async_generator(model='openchat_3.6', messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())