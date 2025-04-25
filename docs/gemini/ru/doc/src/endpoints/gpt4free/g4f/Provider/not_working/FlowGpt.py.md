# Модуль FlowGpt
## Обзор
Модуль `FlowGpt` предоставляет класс `FlowGpt`, который является асинхронным генератором ответов от модели FlowGPT. 

## Классы
### `class FlowGpt`
**Описание**: Класс `FlowGpt` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin` и предоставляет асинхронную генерацию ответов от модели FlowGPT.

**Наследует**:
   - `AsyncGeneratorProvider`
   - `ProviderModelMixin`

**Атрибуты**:
   - `url (str)`: Базовый URL для взаимодействия с FlowGPT.
   - `working (bool)`: Флаг, указывающий, работает ли поставщик.
   - `supports_message_history (bool)`: Флаг, указывающий, поддерживает ли поставщик историю сообщений.
   - `supports_system_message (bool)`: Флаг, указывающий, поддерживает ли поставщик системные сообщения.
   - `default_model (str)`: Имя модели по умолчанию.
   - `models (list)`: Список поддерживаемых моделей.
   - `model_aliases (dict)`: Словарь для сопоставления псевдонимов моделей с их фактическими именами.

**Методы**:
   - `create_async_generator(model: str, messages: Messages, proxy: str = None, temperature: float = 0.7, **kwargs) -> AsyncResult` : Создает асинхронный генератор ответов от модели FlowGPT.
   - `get_model(model: str) -> str`: Получает фактическое имя модели по ее псевдониму.

**Пример использования**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.FlowGpt import FlowGpt

async def main():
    flowgpt = FlowGpt()
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Follow the user\'s instructions carefully."},
        {"role": "user", "content": "Hello, how can I help you today?"}
    ]
    async for response in flowgpt.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Методы класса
### `create_async_generator(model: str, messages: Messages, proxy: str = None, temperature: float = 0.7, **kwargs) -> AsyncResult`
**Назначение**: Создает асинхронный генератор ответов от модели FlowGPT.

**Параметры**:
   - `model (str)`: Имя модели.
   - `messages (Messages)`: Список сообщений для модели.
   - `proxy (str, optional)`: Прокси-сервер для запроса. По умолчанию `None`.
   - `temperature (float, optional)`: Параметр температуры для модели. По умолчанию `0.7`.
   - `**kwargs`: Дополнительные аргументы для модели.

**Возвращает**:
   - `AsyncResult`: Асинхронный генератор ответов.

**Вызывает исключения**:
   - `Exception`: В случае ошибки при взаимодействии с FlowGPT.

**Как работает**:
   - Получает фактическое имя модели по ее псевдониму.
   - Создает заголовки для запроса.
   - Формирует данные для запроса.
   - Выполняет POST-запрос к FlowGPT API.
   - Обрабатывает ответ, декодирует полученные данные и генерирует асинхронный генератор ответов.

**Примеры**:
   - `flowgpt.create_async_generator(model="gpt-3.5-turbo", messages=messages)`
   - `flowgpt.create_async_generator(model="gemini", messages=messages, temperature=0.5)`

### `get_model(model: str) -> str`:
**Назначение**: Получает фактическое имя модели по ее псевдониму.

**Параметры**:
   - `model (str)`: Псевдоним модели.

**Возвращает**:
   - `str`: Фактическое имя модели.

**Как работает**:
   - Проверяет, есть ли псевдоним модели в словаре `model_aliases`.
   - Возвращает фактическое имя модели, если псевдоним найден.
   - Возвращает исходный псевдоним, если он не найден в словаре.

**Примеры**:
   - `flowgpt.get_model("gemini")` - Возвращает "google-gemini".
   - `flowgpt.get_model("gpt-3.5-turbo")` - Возвращает "gpt-3.5-turbo".