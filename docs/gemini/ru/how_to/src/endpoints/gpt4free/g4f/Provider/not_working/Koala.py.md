### Как использовать блок кода Koala.py
=========================================================================================

Описание
-------------------------
Этот код определяет асинхронного провайдера `Koala` для работы с API Koala.sh, который предоставляет доступ к моделям GPT. Класс `Koala` позволяет отправлять запросы к API Koala.sh и получать ответы в виде асинхронного генератора.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `AsyncGenerator`, `Optional`, `List`, `Dict`, `Union`, `Any` из библиотеки `typing`.
   - Импортируются `ClientSession`, `BaseConnector`, `ClientResponse` из библиотеки `aiohttp`.
   - Импортируются `AsyncResult`, `Messages` из модуля `...typing`.
   - Импортируются `AsyncGeneratorProvider`, `ProviderModelMixin` из модуля `..base_provider`.
   - Импортируются `get_random_string`, `get_connector` из модуля `..helper`.
   - Импортируется `raise_for_status` из модуля `...requests`.

2. **Определение класса `Koala`**:
   - Класс `Koala` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Определяются атрибуты класса: `url`, `api_endpoint`, `working`, `supports_message_history`, `default_model`.

3. **Метод `create_async_generator`**:
   - Метод `create_async_generator` является асинхронным классовым методом, который создает асинхронный генератор для получения ответов от API Koala.sh.
   - Принимает аргументы: `model` (строка), `messages` (список сообщений), `proxy` (опциональная строка с адресом прокси-сервера), `connector` (опциональный коннектор для `aiohttp`) и `kwargs` (дополнительные аргументы).
   - Если `model` не указана, устанавливается значение по умолчанию `gpt-4o-mini`.
   - Формируются заголовки запроса (`headers`), включающие `User-Agent`, `Accept`, `Referer` и другие необходимые параметры.
   - Создается асинхронная сессия `ClientSession` с указанными заголовками и коннектором.
   - Формируется текст запроса (`input_text`) из последних сообщений и системных сообщений.
   - Формируются данные запроса (`data`) в виде словаря, включающего `input`, `inputHistory`, `outputHistory` и `model`.
   - Отправляется POST-запрос к API Koala.sh с использованием `session.post`.
   - Обрабатывается ответ с помощью `raise_for_status` для проверки статуса ответа.
   - Полученные чанки данных из ответа передаются в асинхронный генератор `_parse_event_stream` для дальнейшей обработки и генерации.

4. **Метод `_parse_event_stream`**:
   - Метод `_parse_event_stream` является асинхронным статическим методом, который преобразует поток событий ответа в асинхронный генератор.
   - Принимает аргумент `response` (объект `ClientResponse`).
   - Итерируется по чанкам данных из содержимого ответа (`response.content`).
   - Проверяется, начинается ли чанк с `b"data: "`.
   - Если да, то извлекается JSON из чанка (начиная с 6-го байта) и преобразуется в словарь с помощью `json.loads`.
   - Сгенерированный словарь возвращается через `yield`.

Пример использования
-------------------------

```python
from typing import AsyncGenerator, Dict, Union, Any, List, Optional
from aiohttp import BaseConnector

# Assuming Koala class is defined as in the provided code
from src.endpoints.gpt4free.g4f.Provider.not_working.Koala import Koala
from src.typing import Messages

async def example_usage(messages: Messages, model: str = "gpt-4o-mini", proxy: Optional[str] = None, connector: Optional[BaseConnector] = None) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
    """
    Пример использования асинхронного генератора Koala.

    Args:
        messages (Messages): Список сообщений для отправки в API.
        model (str): Модель для использования (по умолчанию "gpt-4o-mini").
        proxy (Optional[str]): Адрес прокси-сервера (если требуется).
        connector (Optional[BaseConnector]): Коннектор aiohttp (если требуется).

    Yields:
        AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]: Асинхронный генератор с ответами от API.
    """
    async for chunk in Koala.create_async_generator(model=model, messages=messages, proxy=proxy, connector=connector):
        yield chunk

# Example messages
messages: Messages = [
    {"role": "user", "content": "Привет!"},
    {"role": "assistant", "content": "Здравствуйте! Как я могу вам помочь?"},
    {"role": "user", "content": "Расскажи мне о Python."},
]

# Using the example
async def main():
    async for response in example_usage(messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())