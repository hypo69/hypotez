# Модуль тестирования асинхронных функций для `gpt4free`

## Обзор

Этот модуль содержит юнит-тесты для проверки корректной работы асинхронных функций, используемых в библиотеке `gpt4free`.

##  Таблица Содержания

- [Классы](#классы)
    - [`TestChatCompletion`](#testchatcompletion)
    - [`TestChatCompletionAsync`](#testchatcompletionasync)
    - [`TestChatCompletionNestAsync`](#testchatcompletionnestasync)
- [Функции](#функции)
    - [`run_exception`](#run_exception)

## Классы

### `TestChatCompletion`

**Описание**: Класс для тестирования класса `ChatCompletion`.

**Inherits**:  `unittest.TestCase`

**Атрибуты**:
- `has_nest_asyncio` (bool): Флаг, указывающий на наличие библиотеки `nest_asyncio`.

**Методы**:

- `test_exception()`: Проверка возникновения ошибки `g4f.errors.NestAsyncioError`, если `nest_asyncio` не установлено.
- `test_create()`: Проверка создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.
- `test_create_generator()`: Проверка создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.
- `test_await_callback()`: Проверка асинхронного вызова метода `create` класса `ChatCompletion`.


#### `run_exception()`

**Описание**: Функция для запуска асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_exception()`

**Описание**: Проверка возникновения ошибки `g4f.errors.NestAsyncioError`, если `nest_asyncio` не установлено.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_create()`

**Описание**: Проверка создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_create_generator()`

**Описание**: Проверка создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_await_callback()`

**Описание**: Проверка асинхронного вызова метода `create` класса `ChatCompletion`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


### `TestChatCompletionAsync`

**Описание**: Класс для тестирования асинхронных функций класса `ChatCompletion`.

**Inherits**:  `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:
- Нет

**Методы**:

- `test_base()`: Проверка базового асинхронного создания экземпляра `ChatCompletion` с использованием `ProviderMock`.
- `test_async()`: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.
- `test_create_generator()`: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.


#### `test_base()`

**Описание**: Проверка базового асинхронного создания экземпляра `ChatCompletion` с использованием `ProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_async()`

**Описание**: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_create_generator()`

**Описание**: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


### `TestChatCompletionNestAsync`

**Описание**: Класс для тестирования асинхронных функций класса `ChatCompletion` с использованием `nest_asyncio`.

**Inherits**:  `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:
- Нет

**Методы**:

- `setUp()`: Настройка тестовой среды.
- `test_create()`: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `ProviderMock`.
- `_test_nested()`: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.
- `_test_nested_generator()`: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.


#### `setUp()`

**Описание**: Настройка тестовой среды.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `test_create()`

**Описание**: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `ProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `_test_nested()`

**Описание**: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


#### `_test_nested_generator()`

**Описание**: Проверка асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncGeneratorProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


## Функции

### `run_exception()`

**Описание**: Функция для запуска асинхронного создания экземпляра `ChatCompletion` с использованием `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- `None`


**Как работает**:

- Эта функция используется в `test_exception()` для запуска асинхронной функции `ChatCompletion.create()` внутри тестового контекста.

**Примеры**:

```python
if __name__ == '__main__':
    unittest.main()
```