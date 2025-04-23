# Документация для `test_chat_completion.py`

## Обзор

Файл `test_chat_completion.py` предназначен для тестирования функциональности чат-завершений в контексте библиотеки `g4f`. Он содержит примеры синхронного и асинхронного использования `g4f.ChatCompletion.create` и `g4f.ChatCompletion.create_async` соответственно.

## Более подробная информация

Этот файл демонстрирует, как можно использовать библиотеку `g4f` для создания чат-завершений с использованием модели по умолчанию. Он показывает, как выполнять запросы в синхронном и асинхронном режимах, а также как обрабатывать потоковые ответы.

## Функции

### `run_async`

```python
async def run_async():
    """Асинхронное создание чат-завершения.

    Args:
        model (g4f.models.default): Модель, используемая для создания чат-завершения.
        messages (list): Список сообщений, отправляемых модели.

    Returns:
        str: Ответ от модели.

    Пример:
        >>> asyncio.run(run_async())
        create_async: hello!
    """
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        #provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)
```

**Описание**: Функция `run_async` асинхронно создает чат-завершение с использованием `g4f.ChatCompletion.create_async`. Она отправляет сообщение "hello!" и выводит полученный ответ.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `None`

**Примеры**:

```python
asyncio.run(run_async())
```

## Примеры использования

Пример синхронного создания чат-завершения:

```python
for response in g4f.ChatCompletion.create(
    model=g4f.models.default,
    #provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True
):
    print(response, end="", flush=True)
print()
```

Пример асинхронного создания чат-завершения:

```python
asyncio.run(run_async())
```