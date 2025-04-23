# Документация для модуля `text_completions_demo_async.py`

## Обзор

Модуль представляет собой демонстрационный асинхронный пример использования библиотеки `g4f` для получения текстовых завершений (text completions) с использованием модели `gpt-4o`. Он показывает, как создать асинхронного клиента и отправить запрос к модели для получения ответа на заданный вопрос.

## Более детально

Этот модуль демонстрирует простое взаимодействие с моделью `gpt-4o` через асинхронный клиент `AsyncClient` из библиотеки `g4f`. Он создает клиент, отправляет запрос с системным сообщением и вопросом пользователя, а затем выводит полученный ответ. Этот код полезен для понимания базового асинхронного запроса к API для получения текстовых завершений.

## Функции

### `main`

```python
async def main():
    """
    Асинхронная функция для демонстрации получения текстовых завершений от модели gpt-4o.

    Args:
        None

    Returns:
        None

    Пример:
        >>> asyncio.run(main())
    """
```

**Описание**: Асинхронная функция `main` создает экземпляр асинхронного клиента `AsyncClient`, отправляет запрос к модели `gpt-4o` с системным сообщением и вопросом пользователя, а затем выводит полученный ответ.

**Как работает функция**:

1.  Создается экземпляр `AsyncClient`.
2.  Отправляется асинхронный запрос к модели `gpt-4o` через метод `client.chat.completions.create`. Запрос включает системное сообщение ("You are a helpful assistant.") и вопрос пользователя ("how does a court case get to the Supreme Court?").
3.  Полученный ответ извлекается из объекта ответа (`response.choices[0].message.content`) и выводится в консоль.

**Примеры**:

```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "how does a court case get to the Supreme Court?"}
        ]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())
```