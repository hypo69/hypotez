# Модуль обработки статуса ответа

## Обзор

Модуль содержит асинхронную функцию `raise_for_status`, предназначенную для проверки статуса HTTP-ответа и генерации исключения в случае неуспешного статуса.

## Подробнее

Этот модуль используется для обработки ответов от HTTP-запросов, особенно при взаимодействии с внешними API. Функция `raise_for_status` проверяет, успешен ли запрос, и, если нет, пытается извлечь сообщение об ошибке из тела ответа (JSON или HTML) перед тем, как сгенерировать исключение `ResponseStatusError`.

## Функции

### `raise_for_status`

```python
async def raise_for_status(response: Union[StreamResponse, ClientResponse], message: str = None):
    """
    Проверяет статус HTTP-ответа и вызывает исключение, если статус не является успешным.

    Args:
        response (Union[StreamResponse, ClientResponse]): Объект HTTP-ответа от aiohttp.
        message (str, optional): Пользовательское сообщение об ошибке. По умолчанию `None`.

    Raises:
        ResponseStatusError: Если статус ответа не является успешным (response.ok == False).

    Внутренние функции:
        Отсутствуют.
    """
```

**Назначение**: Проверяет статус HTTP-ответа и вызывает исключение, если статус не является успешным.

**Параметры**:
- `response` (Union[StreamResponse, ClientResponse]): Объект HTTP-ответа от aiohttp.
- `message` (str, optional): Пользовательское сообщение об ошибке. По умолчанию `None`.

**Возвращает**:
- `None`: Если статус ответа успешен (response.ok == True).

**Вызывает исключения**:
- `ResponseStatusError`: Если статус ответа не является успешным (response.ok == False).

**Как работает функция**:

1. Проверяет, является ли статус ответа успешным (`response.ok`). Если да, функция завершает свою работу.
2. Если статус ответа не является успешным, функция пытается извлечь сообщение об ошибке из тела ответа.
3. Сначала проверяется тип содержимого (`content-type`) ответа. Если это `application/json`, функция пытается разобрать JSON и извлечь сообщение об ошибке из полей `error` или `message`.
4. Если тип содержимого не `application/json` или не удалось извлечь сообщение об ошибке из JSON, функция пытается получить текстовое содержимое ответа.
5. Если тип содержимого `text/html` или текст начинается с `<!DOCTYPE`, функция устанавливает сообщение об ошибке как `"HTML content"`. В противном случае сообщением об ошибке становится текстовое содержимое ответа.
6. Функция вызывает исключение `ResponseStatusError` с сообщением об ошибке, включающим статус ответа и извлеченное или предоставленное сообщение.

**Примеры**:

```python
from aiohttp import ClientSession

async def example():
    async with ClientSession() as session:
        # Пример успешного ответа
        async with session.get('https://example.com') as response:
            try:
                await raise_for_status(response)
                print('Запрос успешен')
            except ResponseStatusError as ex:
                print(f'Ошибка: {ex}')

        # Пример неуспешного ответа
        async with session.get('https://example.com/nonexistent') as response:
            try:
                await raise_for_status(response)
            except ResponseStatusError as ex:
                print(f'Ошибка: {ex}')