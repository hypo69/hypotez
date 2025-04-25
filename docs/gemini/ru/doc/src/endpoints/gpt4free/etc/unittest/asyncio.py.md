# Модуль `asyncio`

## Обзор

Модуль `asyncio`  предоставляет асинхронные тесты для модели `ChatCompletion` из библиотеки `g4f`.

## Подробнее

В модуле `asyncio` реализуются тесты для проверки асинхронного поведения `ChatCompletion` с использованием фреймворка `unittest` и библиотеки `asyncio`. 

Модуль включает в себя тесты для различных сценариев, таких как:

* Тесты для исключений при использовании `asyncio.run` в `ChatCompletion.create`.
* Тесты для синхронной инициализации `ChatCompletion` с различными провайдерами, включая `AsyncProviderMock` и `AsyncGeneratorProviderMock`.
* Тесты для асинхронных методов `create_async`, `create`, которые проверяют корректную работу с провайдерами.

## Классы

### `class TestChatCompletion`

**Описание**: Класс `TestChatCompletion` реализует тесты для `ChatCompletion` с использованием стандартного `unittest`, без поддержки `asyncio`. 

**Атрибуты**:
  - `run_exception`: Асинхронная функция, которая имитирует исключение при вызове `ChatCompletion.create` с `AsyncProviderMock`.

**Методы**:
  - `test_exception`: Проверяет исключение `g4f.errors.NestAsyncioError` при использовании `asyncio.run` в `run_exception`, если  `nest_asyncio` не установлен.
  - `test_create`: Тестирует синхронную инициализацию `ChatCompletion` с `AsyncProviderMock`.
  - `test_create_generator`: Тестирует синхронную инициализацию `ChatCompletion` с `AsyncGeneratorProviderMock`.
  - `test_await_callback`: Тестирует асинхронный вызов `client.chat.completions.create` с использованием `AsyncGeneratorProviderMock` и проверку возвращаемого результата.

## Классы

### `class TestChatCompletionAsync`

**Описание**: Класс `TestChatCompletionAsync` реализует асинхронные тесты для `ChatCompletion` с использованием `unittest.IsolatedAsyncioTestCase`.

**Методы**:
  - `test_base`: Асинхронный тест, который проверяет `ChatCompletion.create_async` с `ProviderMock`.
  - `test_async`: Асинхронный тест, который проверяет `ChatCompletion.create_async` с `AsyncProviderMock`.
  - `test_create_generator`: Асинхронный тест, который проверяет `ChatCompletion.create_async` с `AsyncGeneratorProviderMock`.

## Классы

### `class TestChatCompletionNestAsync`

**Описание**: Класс `TestChatCompletionNestAsync` реализует асинхронные тесты для `ChatCompletion` с использованием `unittest.IsolatedAsyncioTestCase`, с использованием `nest_asyncio` для поддержки `asyncio` в `unittest`.

**Атрибуты**: 
 - `setUp`: Метод, который устанавливает `nest_asyncio` перед выполнением тестов.

**Методы**:
  - `test_create`: Асинхронный тест, который проверяет `ChatCompletion.create_async` с `ProviderMock`, используя `nest_asyncio`.
  - `_test_nested`: Асинхронный тест, который проверяет `ChatCompletion.create` с `AsyncProviderMock`, используя `nest_asyncio`.
  - `_test_nested_generator`: Асинхронный тест, который проверяет `ChatCompletion.create` с `AsyncGeneratorProviderMock`, используя `nest_asyncio`.