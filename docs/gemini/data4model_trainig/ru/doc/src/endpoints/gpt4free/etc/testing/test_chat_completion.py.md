# Модуль тестирования `test_chat_completion.py`

## Обзор

Этот модуль предназначен для тестирования функциональности `ChatCompletion` из библиотеки `g4f` (gpt4free). Он демонстрирует, как использовать `g4f.ChatCompletion.create` для генерации текста в режиме потока и `g4f.ChatCompletion.create_async` для асинхронного создания текста.

## Подробней

Модуль использует библиотеку `g4f` для взаимодействия с моделями генерации текста. Он содержит примеры синхронного и асинхронного вызова функций `ChatCompletion.create` и `ChatCompletion.create_async` соответственно. Код демонстрирует, как отправлять запросы к моделям и получать ответы.

## Функции

### `run_async`

```python
async def run_async():
    """ Асинхронно отправляет запрос к g4f.ChatCompletion и печатает ответ.

    Args:
        Нет

    Returns:
        None

    Пример:
        >>> asyncio.run(run_async())
        create_async: Hello! How can I assist you today?
    """
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        #provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)
```

**Назначение**: Асинхронная функция для отправки запроса к `g4f.ChatCompletion.create_async` и печати полученного ответа.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:
- Функция использует `g4f.ChatCompletion.create_async` для отправки асинхронного запроса к модели.
- В качестве модели используется `g4f.models.default`.
- Отправляется сообщение с ролью "user" и содержанием "hello!".
- Полученный ответ печатается в консоль с префиксом "create_async:".
- `asyncio.run(run_async())` запускает асинхронную функцию.

**Примеры**:
```python
asyncio.run(run_async())
```
## Запуск асинхронной функции

```python
asyncio.run(run_async())
```

**Назначение**: Запускает асинхронную функцию `run_async`.

**Параметры**:
- Нет

**Возвращает**:
- Нет

**Как работает**:
- Использует `asyncio.run()` для запуска корутины `run_async()`.