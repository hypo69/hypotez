# Модуль для асинхронных тестов GPT4Free

## Обзор

Этот модуль предоставляет асинхронные тесты для GPT4Free. Он использует библиотеку asyncio для параллельного выполнения запросов к различным API-провайдерам, таким как g4f.

## Детали

Модуль содержит функции для создания асинхронных запросов к GPT4Free, а также для запуска тестов с использованием `asyncio.gather`. Он также использует `log_time_async` для измерения времени выполнения асинхронных операций.

## Классы

###  `None`

## Функции

### `create_async`

**Цель**: Функция выполняет асинхронный запрос к GPT4Free с использованием заданного провайдера.

**Параметры**:

- `provider`: Объект провайдера для запроса к GPT4Free.

**Возвращает**:

- `None`

**Исключения**:

- `Exception`: Если возникает ошибка при выполнении запроса.

**Пример**:

```python
async def create_async(provider):
    try:
        response = await log_time_async(
            provider.create_async,
            model=g4f.models.default.name,
            messages=[{"role": "user", "content": "Hello, are you GPT 3.5?"}]
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
```


### `run_async`

**Цель**: Функция запускает асинхронные тесты для всех доступных провайдеров GPT4Free.

**Параметры**:

- `None`

**Возвращает**:

- `None`

**Пример**:

```python
async def run_async():
  responses: list = [
      create_async(provider)
      for provider in get_providers()
      if provider.working
  ]
  await asyncio.gather(*responses)
```

### `log_time_async`

**Цель**: Функция измеряет время выполнения асинхронной функции.

**Параметры**:

- `func`: Асинхронная функция для выполнения.
- `*args`: Дополнительные аргументы, которые нужно передать функции `func`.
- `**kwargs`: Дополнительные ключевые аргументы, которые нужно передать функции `func`.

**Возвращает**:

- `None`

**Пример**:

```python
async def log_time_async(func, *args, **kwargs):
    start_time = time.time()
    result = await func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{func.__name__} took {elapsed_time:.2f} seconds.")
    return result
```

## Примеры

###  Запуск асинхронных тестов

```python
print("Total:", asyncio.run(log_time_async(run_async)))
```

## Как работает код

Этот код использует библиотеку `asyncio` для параллельного выполнения асинхронных запросов к GPT4Free. Функция `create_async` выполняет асинхронный запрос к GPT4Free с использованием заданного провайдера. Функция `run_async` собирает все доступные провайдеры и запускает асинхронные тесты с использованием `asyncio.gather`. Функция `log_time_async` измеряет время выполнения асинхронных операций.

## Дополнительная информация

Этот модуль предназначен для тестирования GPT4Free API с использованием различных провайдеров. Он предоставляет удобный способ выполнения асинхронных запросов и измерения их времени выполнения.