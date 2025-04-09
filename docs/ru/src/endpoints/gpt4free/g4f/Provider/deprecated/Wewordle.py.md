# Модуль для взаимодействия с Wewordle API
## Обзор

Модуль `Wewordle` предоставляет асинхронный интерфейс для взаимодействия с API Wewordle, в частности, для получения ответов от GPT-3.5 Turbo. Этот модуль предназначен для использования в асинхронных приложениях и поддерживает работу через прокси.

## Подробней

Модуль содержит класс `Wewordle`, который наследуется от `AsyncProvider` и реализует метод `create_async` для отправки запросов к API Wewordle. Он генерирует случайные идентификаторы пользователя и приложения, формирует JSON-данные для запроса и отправляет их на конечную точку `/gptapi/v1/android/turbo`.

## Классы

### `Wewordle`

**Описание**: Класс для взаимодействия с API Wewordle.

**Наследует**:
- `AsyncProvider`: Обеспечивает асинхронное взаимодействие с API.

**Атрибуты**:
- `url` (str): URL API Wewordle (`https://wewordle.org`).
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (в данном случае `True`).

**Методы**:
- `create_async`: Асинхронный метод для отправки запроса к API и получения ответа.

## Функции

### `create_async`

```python
    async def create_async(
        cls,
        model: str,
        messages: list[dict[str, str]],
        proxy: str = None,
        **kwargs
    ) -> str:
        """
        Асинхронно отправляет запрос к API Wewordle и возвращает ответ.

        Args:
            cls: Ссылка на класс.
            model (str): Модель для использования (не используется в данной реализации).
            messages (list[dict[str, str]]): Список сообщений для отправки в API.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Ответ от API Wewordle.

        Raises:
            aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

        """
```

**Назначение**: Отправляет асинхронный запрос к API Wewordle и возвращает полученный контент.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования (фактически не используется в данной реализации).
- `messages` (list[dict[str, str]]): Список сообщений, отправляемых в API.
- `proxy` (str, optional): Адрес прокси-сервера для использования при отправке запроса. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы.

**Возвращает**:
- `str`: Контент, полученный от API Wewordle.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Возникает, если HTTP-запрос завершается с ошибкой.

**Как работает функция**:

1. **Формирование заголовков**: Создаются HTTP-заголовки, включающие `accept`, `pragma`, `Content-Type` и `Connection`.
2. **Генерация идентификаторов**: Генерируются случайные идентификаторы пользователя (`_user_id`) и приложения (`_app_id`).
3. **Формирование данных запроса**: Создается словарь `data`, включающий идентификаторы, сообщения и информацию о подписчике.
4. **Отправка запроса**: Используется `aiohttp.ClientSession` для отправки POST-запроса к API Wewordle.
5. **Обработка ответа**: Извлекается контент из JSON-ответа и возвращается.

```
   Формирование заголовков и ID
   │
   ├── Генерация _user_id
   │
   ├── Генерация _app_id
   │
   └── Формирование _request_date
   │
   Формирование данных запроса (data)
   │
   └── Создание структуры JSON
   │
   Отправка POST-запроса к API
   │
   └── Обработка ответа API
   │
   Извлечение контента
   │
   └── Возврат контента
```

**Примеры**:

```python
import asyncio

async def main():
    messages = [{"role": "user", "content": "Hello, Wewordle!"}]
    response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

Этот пример показывает базовый способ использования `create_async` для отправки сообщения и печати ответа.

```python
import asyncio

async def main():
    messages = [{"role": "user", "content": "Как дела?"}]
    response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages, proxy="http://your-proxy:8080")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

В этом примере показано, как использовать прокси-сервер при отправке запроса.