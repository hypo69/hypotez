# Модуль Aichat

## Обзор

Этот модуль реализует класс `Aichat`, который является провайдером для получения ответов от модели `gpt-3.5-turbo`. 
Он использует сайт `chat-gpt.org` для получения ответов от модели.

## Подробей

`Aichat` наследует от базового класса `AsyncProvider` и предоставляет метод `create_async` для асинхронного 
получения ответов от модели. Метод требует параметры `model`, `messages`, `proxy` и `kwargs`. 

Класс `Aichat` использует `StreamSession` для отправки HTTP-запросов на сайт `chat-gpt.org`. 
Он передает JSON-данные с запросом на получение ответа от модели, включая `message`, `temperature`, `presence_penalty`, `top_p` и `frequency_penalty`.

## Классы

### `class Aichat(AsyncProvider)`

**Описание**:  Класс `Aichat` реализует асинхронный провайдер для получения ответов от модели `gpt-3.5-turbo` 
с использованием сайта `chat-gpt.org`.

**Наследует**: 
    - `AsyncProvider` 

**Аттрибуты**:

   - `url` (str): Базовый URL для отправки запросов.
   - `working` (bool): Флаг, указывающий, работает ли провайдер.
   - `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель `gpt-3.5-turbo`.

**Методы**:

   - `create_async(model: str, messages: Messages, proxy: str = None, **kwargs) -> str`:  
       - Этот метод выполняет асинхронный запрос к сайту `chat-gpt.org` для получения ответа от модели.
       - Принимает следующие параметры:
           - `model` (str): Имя модели (например, `gpt-3.5-turbo`).
           - `messages` (Messages): Список сообщений для запроса.
           - `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
           - `kwargs`: Дополнительные параметры для запроса.

       - Возвращает ответ от модели в виде строки.
       - Возможные исключения:
           - `RuntimeError`: Если не найдены необходимые `cookies` для сайта `chat-gpt.org`.
           - `Exception`: Если получен ошибочный ответ от сервера.

   - `format_prompt(messages: Messages) -> str`: 
       - Метод форматирует сообщения для запроса к модели.
       - Принимает список сообщений `messages`.
       - Возвращает отформатированную строку с сообщениями.


## Внутренние функции

### `format_prompt(messages: Messages) -> str`

**Назначение**: Форматирование сообщений для запроса к модели.

**Параметры**:
   - `messages` (Messages): Список сообщений для запроса.

**Возвращает**:
   - `str`: Отформатированная строка с сообщениями.

**Как работает функция**:
   - Эта функция получает список сообщений `messages` и формирует из них строку для запроса к модели.
   - Форматирование включает в себя добавление специальных символов, которые будут интерпретированы моделью.

**Примеры**:
   - `>>> format_prompt([{'role': 'user', 'content': 'Hello world!'}] )
      'Hello world!'`


### `create_async(model: str, messages: Messages, proxy: str = None, **kwargs) -> str`

**Назначение**: Выполняет асинхронный запрос к сайту `chat-gpt.org` для получения ответа от модели.

**Параметры**:
   - `model` (str): Имя модели (например, `gpt-3.5-turbo`).
   - `messages` (Messages): Список сообщений для запроса.
   - `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
   - `kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
   - `str`: Ответ от модели в виде строки.

**Вызывает исключения**:
   - `RuntimeError`: Если не найдены необходимые `cookies` для сайта `chat-gpt.org`.
   - `Exception`: Если получен ошибочный ответ от сервера.

**Как работает функция**:
   -  Функция проверяет, есть ли у пользователя необходимые `cookies` для сайта `chat-gpt.org`.
   - Создает `StreamSession` для отправки HTTP-запросов.
   - Форматирует сообщения для запроса с помощью функции `format_prompt`.
   - Отправляет JSON-запрос на сайт `chat-gpt.org` и ожидает ответ.
   - Обрабатывает ответ и возвращает его.
   -  Обрабатывает ошибки при получении ответа от сервера.

**Примеры**:
   - `>>> await create_async(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello world!'}] )
      'Hello, how can I help you today?'`


##  Примеры

**Пример использования**:

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aichat import Aichat
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

    async def main():
        aichat = Aichat()
        messages: Messages = [{'role': 'user', 'content': 'Hello world!'}]
        response = await aichat.create_async(model='gpt-3.5-turbo', messages=messages)
        print(f"Response: {response}")

    if __name__ == '__main__':
        import asyncio
        asyncio.run(main())