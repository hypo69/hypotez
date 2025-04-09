# Модуль тестирования асинхронности для g4f
## Обзор

Модуль содержит юнит-тесты для проверки асинхронной функциональности библиотеки `g4f` (gpt4free).
Он включает тесты для `ChatCompletion.create`, `ChatCompletion.create_async` и обработки исключений, связанных с `nest_asyncio`.

## Подробней

Этот файл содержит тесты для асинхронного режима работы `ChatCompletion` в библиотеке `g4f`. Здесь проверяется корректность выполнения запросов как с синхронными, так и с асинхронными провайдерами, а также с провайдерами, возвращающими генераторы. Кроме того, проверяется корректная обработка ошибок при отсутствии установленного `nest_asyncio`.

## Классы

### `TestChatCompletion`

**Описание**:
Класс содержит тесты для синхронного режима `ChatCompletion`.

**Аттрибуты**:
- `DEFAULT_MESSAGES` (List[dict]): Список сообщений по умолчанию для использования в тестах.

**Методы**:
- `run_exception()`: Запускает `ChatCompletion.create` с асинхронным провайдером, возвращает результат.
- `test_exception()`: Проверяет возникновение исключения `g4f.errors.NestAsyncioError` при попытке запуска асинхронного кода синхронно, если не установлен `nest_asyncio`.
- `test_create()`: Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером.
- `test_create_generator()`: Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером, возвращающим генератор.
- `test_await_callback()`: Проверяет корректность вызова `client.chat.completions.create` с асинхронным провайдером, возвращающим генератор.

### `TestChatCompletionAsync`

**Описание**:
Класс содержит тесты для асинхронного режима `ChatCompletion`.

**Аттрибуты**:
- `DEFAULT_MESSAGES` (List[dict]): Список сообщений по умолчанию для использования в тестах.

**Методы**:
- `test_base()`: Проверяет корректность работы `ChatCompletion.create_async` с синхронным провайдером.
- `test_async()`: Проверяет корректность работы `ChatCompletion.create_async` с асинхронным провайдером.
- `test_create_generator()`: Проверяет корректность работы `ChatCompletion.create_async` с асинхронным провайдером, возвращающим генератор.

### `TestChatCompletionNestAsync`

**Описание**:
Класс содержит тесты для проверки работы `ChatCompletion` с установленным `nest_asyncio`.

**Аттрибуты**:
- `DEFAULT_MESSAGES` (List[dict]): Список сообщений по умолчанию для использования в тестах.

**Методы**:
- `setUp()`: Устанавливает `nest_asyncio` перед выполнением тестов, если он установлен. Если `nest_asyncio` не установлен, тест пропускается.
- `test_create()`: Проверяет корректность работы `ChatCompletion.create_async` с синхронным провайдером.
- `_test_nested()`: Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером.
- `_test_nested_generator()`: Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером, возвращающим генератор.

## Функции

### `TestChatCompletion.run_exception`

```python
    async def run_exception(self):
        """
        Запускает `ChatCompletion.create` с асинхронным провайдером.

        Returns:
            Any: результат `ChatCompletion.create`.
        """
        ...
```

**Назначение**: Функция запускает `ChatCompletion.create` с использованием модели по умолчанию, сообщений по умолчанию и асинхронного провайдера `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- Any: Результат выполнения `ChatCompletion.create`.

**Как работает функция**:

1.  Вызывает асинхронную функцию `ChatCompletion.create` с предопределенными параметрами: моделью по умолчанию, сообщениями и моком асинхронного провайдера.
2.  Возвращает результат вызова `ChatCompletion.create`.

```
A: Вызов ChatCompletion.create
|
B: Возврат результата
```

**Примеры**:

```python
async def test_run_exception(self):
    test_case = TestChatCompletion()
    result = await test_case.run_exception()
    print(result)  # Вывод: Mock
```

### `TestChatCompletion.test_exception`

```python
    def test_exception(self):
        """
        Проверяет возникновение исключения `g4f.errors.NestAsyncioError` при попытке запуска асинхронного кода синхронно, если не установлен `nest_asyncio`.
        """
        ...
```

**Назначение**: Функция проверяет, что при попытке запуска асинхронного кода синхронно, когда не установлен `nest_asyncio`, возникает исключение `g4f.errors.NestAsyncioError`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Проверяет, установлен ли `nest_asyncio`. Если установлен, тест пропускается.
2.  Если `nest_asyncio` не установлен, функция вызывает `asyncio.run` для запуска асинхронной функции `self.run_exception()` и проверяет, что было вызвано исключение `g4f.errors.NestAsyncioError`.

```
A: Проверка наличия nest_asyncio
|
B: Если nest_asyncio установлен -> Пропуск теста
|
C: Если nest_asyncio не установлен -> Вызов asyncio.run(self.run_exception()) и проверка исключения g4f.errors.NestAsyncioError
```

**Примеры**:

```python
def test_test_exception(self):
    test_case = TestChatCompletion()
    test_case.test_exception()
```

### `TestChatCompletion.test_create`

```python
    def test_create(self):
        """
        Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает функцию `ChatCompletion.create` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create с AsyncProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
def test_test_create(self):
    test_case = TestChatCompletion()
    test_case.test_create()
```

### `TestChatCompletion.test_create_generator`

```python
    def test_create_generator(self):
        """
        Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером, возвращающим генератор.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncGeneratorProviderMock`, который возвращает генератор.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает функцию `ChatCompletion.create` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncGeneratorProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create с AsyncGeneratorProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
def test_test_create_generator(self):
    test_case = TestChatCompletion()
    test_case.test_create_generator()
```

### `TestChatCompletion.test_await_callback`

```python
    def test_await_callback(self):
        """
        Проверяет корректность вызова `client.chat.completions.create` с асинхронным провайдером, возвращающим генератор.
        """
        ...
```

**Назначение**: Функция проверяет, что `client.chat.completions.create` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncGeneratorProviderMock`, который возвращает генератор.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Создает экземпляр класса `Client` с асинхронным провайдером `AsyncGeneratorProviderMock`.
2.  Вызывает метод `client.chat.completions.create` с сообщениями по умолчанию и другими параметрами.
3.  Проверяет, что содержимое сообщения в ответе равно `"Mock"`.

```
A: Создание экземпляра Client с AsyncGeneratorProviderMock
|
B: Вызов client.chat.completions.create
|
C: Проверка, что содержимое сообщения в ответе равно "Mock"
```

**Примеры**:

```python
def test_test_await_callback(self):
    test_case = TestChatCompletion()
    test_case.test_await_callback()
```

### `TestChatCompletionAsync.test_base`

```python
    async def test_base(self):
        """
        Проверяет корректность работы `ChatCompletion.create_async` с синхронным провайдером.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create_async` возвращает ожидаемый результат при использовании синхронного провайдера `ProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает асинхронную функцию `ChatCompletion.create_async` с моделью по умолчанию, сообщениями по умолчанию и синхронным провайдером `ProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create_async с ProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_base(self):
    test_case = TestChatCompletionAsync()
    await test_case.test_base()
```

### `TestChatCompletionAsync.test_async`

```python
    async def test_async(self):
        """
        Проверяет корректность работы `ChatCompletion.create_async` с асинхронным провайдером.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create_async` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncProviderMock`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает асинхронную функцию `ChatCompletion.create_async` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create_async с AsyncProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_async(self):
    test_case = TestChatCompletionAsync()
    await test_case.test_async()
```

### `TestChatCompletionAsync.test_create_generator`

```python
    async def test_create_generator(self):
        """
        Проверяет корректность работы `ChatCompletion.create_async` с асинхронным провайдером, возвращающим генератор.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create_async` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncGeneratorProviderMock`, который возвращает генератор.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает асинхронную функцию `ChatCompletion.create_async` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncGeneratorProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create_async с AsyncGeneratorProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_create_generator(self):
    test_case = TestChatCompletionAsync()
    await test_case.test_create_generator()
```

### `TestChatCompletionNestAsync.setUp`

```python
    def setUp(self) -> None:
        """
        Устанавливает `nest_asyncio` перед выполнением тестов, если он установлен. Если `nest_asyncio` не установлен, тест пропускается.
        """
        ...
```

**Назначение**: Функция выполняет настройку перед каждым тестом. Она проверяет, установлен ли `nest_asyncio`. Если он установлен, то применяется `nest_asyncio.apply()`. Если `nest_asyncio` не установлен, то тест пропускается.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Проверяет, установлен ли `nest_asyncio`.
2.  Если `nest_asyncio` не установлен, тест пропускается с помощью `self.skipTest('"nest_asyncio" not installed')`.
3.  Если `nest_asyncio` установлен, вызывается `nest_asyncio.apply()`.

```
A: Проверка наличия nest_asyncio
|
B: Если nest_asyncio не установлен -> Пропуск теста
|
C: Если nest_asyncio установлен -> Вызов nest_asyncio.apply()
```

**Примеры**:

```python
import unittest
import nest_asyncio

class TestExample(unittest.TestCase):
    def setUp(self):
        if not hasattr(nest_asyncio, 'apply'):
            self.skipTest("nest_asyncio не установлен")
        nest_asyncio.apply()

    def test_something(self):
        self.assertTrue(True)
```

### `TestChatCompletionNestAsync.test_create`

```python
    async def test_create(self):
        """
        Проверяет корректность работы `ChatCompletion.create_async` с синхронным провайдером.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create_async` возвращает ожидаемый результат при использовании синхронного провайдера `ProviderMock` и установленном `nest_asyncio`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает асинхронную функцию `ChatCompletion.create_async` с моделью по умолчанию, сообщениями по умолчанию и синхронным провайдером `ProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create_async с ProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_create(self):
    test_case = TestChatCompletionNestAsync()
    await test_case.test_create()
```

### `TestChatCompletionNestAsync._test_nested`

```python
    async def _test_nested(self):
        """
        Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncProviderMock` и установленном `nest_asyncio`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает функцию `ChatCompletion.create` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create с AsyncProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_nested(self):
    test_case = TestChatCompletionNestAsync()
    await test_case._test_nested()
```

### `TestChatCompletionNestAsync._test_nested_generator`

```python
    async def _test_nested_generator(self):
        """
        Проверяет корректность работы `ChatCompletion.create` с асинхронным провайдером, возвращающим генератор.
        """
        ...
```

**Назначение**: Функция проверяет, что `ChatCompletion.create` возвращает ожидаемый результат при использовании асинхронного провайдера `AsyncGeneratorProviderMock`, который возвращает генератор, и установленном `nest_asyncio`.

**Параметры**:
- Нет

**Возвращает**:
- None

**Как работает функция**:

1.  Вызывает функцию `ChatCompletion.create` с моделью по умолчанию, сообщениями по умолчанию и асинхронным провайдером `AsyncGeneratorProviderMock`.
2.  Проверяет, что результат равен `"Mock"`.

```
A: Вызов ChatCompletion.create с AsyncGeneratorProviderMock
|
B: Проверка, что результат равен "Mock"
```

**Примеры**:

```python
import asyncio
async def test_test_nested_generator(self):
    test_case = TestChatCompletionNestAsync()
    await test_case._test_nested_generator()