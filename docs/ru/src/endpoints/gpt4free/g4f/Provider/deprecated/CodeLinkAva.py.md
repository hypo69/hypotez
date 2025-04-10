# Модуль CodeLinkAva

## Обзор

Модуль `CodeLinkAva` предоставляет асинхронный генератор для взаимодействия с API CodeLinkAva. Этот модуль предназначен для работы с моделью `gpt-3.5-turbo` и позволяет получать ответы от API в режиме реального времени.

## Подробнее

Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов. Он отправляет сообщения пользователя в API CodeLinkAva и возвращает ответы в виде асинхронного генератора, что позволяет обрабатывать большие объемы данных потоково.

## Классы

### `CodeLinkAva`

**Описание**: Класс `CodeLinkAva` является асинхронным провайдером генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL API CodeLinkAva.
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-3.5-turbo`.
- `working` (bool): Указывает, работает ли провайдер.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: list[dict[str, str]],
    **kwargs
) -> AsyncGenerator:
    """
    Создает асинхронный генератор для получения ответов от API CodeLinkAva.

    Args:
        model (str): Название модели.
        messages (list[dict[str, str]]): Список сообщений для отправки в API.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncGenerator: Асинхронный генератор, возвращающий контент ответов от API.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

    """
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API CodeLinkAva и получения потоковых ответов.

**Параметры**:
- `cls`: Ссылка на класс `CodeLinkAva`.
- `model` (str): Модель, используемая для генерации ответов.
- `messages` (list[dict[str, str]]): Список сообщений, отправляемых в API. Каждое сообщение представляет собой словарь с ключами `role` и `content`.
- `**kwargs`: Дополнительные параметры, которые будут переданы в API.

**Возвращает**:
- `AsyncGenerator`: Асинхронный генератор, который предоставляет содержимое ответов от API по мере их поступления.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Вызывается в случае, если HTTP-запрос завершается с ошибкой.

**Как работает функция**:

1. **Инициализация заголовков**: Функция создает словарь `headers` с необходимыми HTTP-заголовками для запроса.

2. **Создание асинхронной сессии**: Используется `aiohttp.ClientSession` для управления HTTP-соединением.

3. **Подготовка данных**: Формируется словарь `data`, включающий сообщения, температуру и другие параметры.

4. **Отправка POST-запроса**: Функция отправляет асинхронный POST-запрос к API CodeLinkAva (`https://ava-alpha-api.codelink.io/api/chat`) с данными и заголовками.

5. **Обработка потока ответов**: Функция читает содержимое ответа построчно.

6. **Декодирование и обработка данных**: Каждая строка декодируется и проверяется на наличие префикса `data: `. Если строка содержит данные, она загружается из JSON.

7. **Извлечение контента**: Извлекается контент из поля `content` в JSON-ответе и возвращается через генератор.

8. **Завершение**: Если строка начинается с `data: [DONE]`, генератор завершает свою работу.

```
    A   Начало
    |
    |   Создание headers
    |
    B   Создание асинхронной сессии
    |
    |   Формирование data
    |
    C   Отправка POST запроса
    |
    |   Получение ответа
    |
    D   Обработка каждой строки ответа
    |
    |   Проверка префикса "data: "
    |
    E   Извлечение контента из JSON
    |
    |   Возврат контента через yield
    |
    F   Завершение при "data: [DONE]"
```

**Примеры**:

1. **Простой пример вызова**:
   ```python
   async def main():
       messages = [{"role": "user", "content": "Hello, how are you?"}]
       async for message in CodeLinkAva.create_async_generator(model="gpt-3.5-turbo", messages=messages):
           print(message, end="")

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())
   ```

2. **Пример с дополнительными параметрами**:
   ```python
   async def main():
       messages = [{"role": "user", "content": "Tell me a joke."}]
       async for message in CodeLinkAva.create_async_generator(model="gpt-3.5-turbo", messages=messages, temperature=0.8):
           print(message, end="")

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())