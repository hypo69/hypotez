# Модуль Vitalentum (устаревший)

## Обзор

Модуль `Vitalentum` предоставляет асинхронный генератор для взаимодействия с API Vitalentum.io. 

**Важно:** Этот модуль устарел и больше не поддерживается. Используйте другие провайдеры GPT4Free.

## Классы

### `Vitalentum`

**Описание**: 
Класс `Vitalentum` реализует асинхронный генератор для работы с API Vitalentum.io. 

**Наследует**: 
 - `AsyncGeneratorProvider` - базовый класс для асинхронных генераторов GPT4Free.

**Атрибуты**:
 - `url (str)`: URL-адрес API Vitalentum.io.
 - `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.

**Методы**:
 - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:
    - Создание асинхронного генератора для взаимодействия с API.

## Функции

### `create_async_generator`

**Назначение**: 
 - Создание асинхронного генератора для взаимодействия с API.

**Параметры**:
 - `model (str)`: Имя модели.
 - `messages (Messages)`: Список сообщений в истории диалога.
 - `proxy (str, optional)`: Прокси-сервер для запросов. По умолчанию - `None`.
 - `kwargs`: Дополнительные аргументы для запроса.

**Возвращает**:
 - `AsyncResult`: Асинхронный результат, содержащий генератор, который будет выдавать сообщения ответа от API.

**Вызывает исключения**:
 - `Exception`: Если произошла ошибка при обработке запроса.

**Как работает функция**:

 - Функция `create_async_generator` создает запрос к API Vitalentum.io с заданными параметрами.
 - Запрос включает в себя историю диалога, модель и дополнительные параметры.
 - В теле функции `create_async_generator` используется `ClientSession` для отправки HTTP-запроса к API.
 - Ответ API обрабатывается с помощью `async for` цикла для получения всех сообщений ответа.
 - Каждый полученный ответ добавляется в список `messages`.
 - В итоге, функция возвращает `AsyncResult` с генератором, который будет выдавать все полученные сообщения в истории диалога.

**Примеры**:

```python
# Пример использования
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vitalentum import Vitalentum

messages = [
    {"role": "user", "content": "Привет!"},
    {"role": "assistant", "content": "Привет!"},
]

async def main():
    async for response in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```