# Модуль Qwen_Qwen_2_5M

## Обзор

Этот модуль предоставляет реализацию провайдера для модели Qwen Qwen-2.5M, доступной через Hugging Face Spaces. 
Модуль обеспечивает асинхронный генератор, поддерживающий поток вывода, системные сообщения и историю сообщений.

## Подробнее

Модуль `Qwen_Qwen_2_5M` использует API Hugging Face Spaces для взаимодействия с моделью Qwen-2.5M. 
Он предоставляет  асинхронный генератор, который позволяет получить ответ модели в потоке. 
Модуль также поддерживает системные сообщения и историю сообщений, позволяя устанавливать контекст для модели.

## Классы

### `class Qwen_Qwen_2_5M`

**Описание**: 
Класс, представляющий провайдера для модели Qwen Qwen-2.5M.
**Наследует**: 
    - `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
    - `ProviderModelMixin`: Миксин для моделей, предоставляющий общие методы для обработки моделей и их алиасов.

**Атрибуты**:

- `label` (str): Метка провайдера, "Qwen Qwen-2.5M".
- `url` (str): URL-адрес API Hugging Face Spaces для модели.
- `api_endpoint` (str):  Конечная точка API для отправки запросов на предсказание.
- `working` (bool): Индикатор доступности модели.
- `supports_stream` (bool): Флаг, указывающий на поддержку потока вывода.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Имя модели по умолчанию.
- `model_aliases` (dict): Словарь для алиасов модели.
- `models` (list): Список доступных моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, return_conversation: bool = False, conversation: JsonConversation = None, **kwargs) -> AsyncResult`:
    - **Назначение**: Создает асинхронный генератор для модели, который отправляет запросы на предсказание и генерирует ответы в потоке.
    - **Параметры**:
        - `model` (str): Имя модели.
        - `messages` (Messages): Список сообщений для модели.
        - `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        - `return_conversation` (bool, optional): Флаг, указывающий на необходимость вернуть JsonConversation. По умолчанию `False`.
        - `conversation` (JsonConversation, optional): JsonConversation, хранящая предыдущие сообщения. По умолчанию `None`.
        - `**kwargs`: Дополнительные ключевые слова, передаваемые в API.
    - **Возвращает**: 
        - `AsyncResult`: Асинхронный генератор, возвращающий ответы модели в потоке.
    - **Пример**:
        ```python
        async def main():
            messages = [
                {"role": "user", "content": "Привет! Как дела?"}
            ]
            async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m", messages=messages):
                print(response)

        if __name__ == "__main__":
            import asyncio
            asyncio.run(main())
        ```


### **Внутренние функции**:
- `generate_session_hash()` 
    - **Назначение**:  Генерирует уникальный идентификатор сессии.
    - **Параметры**: 
        - Нет
    - **Возвращает**: 
        - str: Уникальный идентификатор сессии.
    - **Пример**:
        ```python
        session_hash = generate_session_hash()
        print(session_hash) # Вывод: "a3b4c5d6e7f8"
        ```
    
## Параметры класса
- `model` (str):  Имя модели, используемой для генерации текста. 
- `messages` (Messages): Список сообщений для модели. 
- `proxy` (str, optional):  Прокси-сервер для использования. По умолчанию `None`. 
- `return_conversation` (bool, optional):  Флаг, указывающий на необходимость вернуть JsonConversation. По умолчанию `False`. 
- `conversation` (JsonConversation, optional):  JsonConversation, хранящая предыдущие сообщения. По умолчанию `None`. 

## Примеры

### Вызов функции `create_async_generator`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5M import Qwen_Qwen_2_5M

async def main():
    messages = [
        {"role": "user", "content": "Привет! Как дела?"}
    ]
    async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())