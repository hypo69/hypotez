# Модуль для тестирования image_client

## Обзор

Модуль содержит юнит-тесты для проверки функциональности асинхронного клиента, работающего с провайдерами изображений, в частности с `IterListProvider`.
Он проверяет корректность обработки различных сценариев, таких как пропуск недоступных провайдеров, получение только одного результата и обработка исключений.

## Подробнее

Модуль использует библиотеку `unittest` для создания и запуска тестов. Он также использует `asyncio` для тестирования асинхронного кода.
В модуле определен класс `TestIterListProvider`, который содержит несколько тестовых методов, проверяющих различные аспекты работы `IterListProvider` с моками провайдеров.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий юнит-тесты для проверки `IterListProvider`.

**Наследует**:

- `unittest.IsolatedAsyncioTestCase`: Предоставляет инфраструктуру для написания асинхронных тестов.

**Методы**:

- `test_skip_provider()`: Проверяет, что клиент пропускает провайдера, если он не предоставляет авторизацию.
- `test_only_one_result()`: Проверяет, что клиент возвращает только один результат, даже если есть несколько доступных провайдеров.
- `test_skip_none()`: Проверяет, что клиент пропускает провайдера, если он возвращает `None`.
- `test_raise_exception()`: Проверяет, что клиент правильно обрабатывает исключения, возникающие при работе провайдера.

## Функции

### `test_skip_provider`

```python
async def test_skip_provider(self):
    """Проверяет, что клиент пропускает провайдера, если он не предоставляет авторизацию."""
```

**Назначение**: Проверка, что асинхронный клиент корректно пропускает провайдера изображений, если тот не предоставляет авторизацию.

**Параметры**:

- `self`: Ссылка на экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Как работает функция**:

1. **Инициализация**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `MissingAuthProviderMock` (имитирует провайдера без авторизации) и `YieldImageResponseProviderMock` (имитирует провайдера, возвращающего успешный ответ).
2. **Вызов**: Вызывается метод `client.images.generate` для генерации изображения.
3. **Проверка**: Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL изображения соответствует ожидаемому значению ("Hello").

**ASCII flowchart**:

```
Инициализация AsyncClient с IterListProvider(MissingAuthProviderMock, YieldImageResponseProviderMock)
↓
Вызов client.images.generate("Hello", "", response_format="orginal")
↓
Проверка: isinstance(response, ImagesResponse) и response.data[0].url == "Hello"
```

**Примеры**:

```python
await TestIterListProvider().test_skip_provider()
```

### `test_only_one_result`

```python
async def test_only_one_result(self):
    """Проверяет, что клиент возвращает только один результат, даже если есть несколько доступных провайдеров."""
```

**Назначение**: Проверка, что асинхронный клиент возвращает только один результат, даже если в списке провайдеров указано несколько провайдеров, возвращающих результат.

**Параметры**:

- `self`: Ссылка на экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Как работает функция**:

1. **Инициализация**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит два экземпляра `YieldImageResponseProviderMock` (имитируют провайдеров, возвращающих успешный ответ).
2. **Вызов**: Вызывается метод `client.images.generate` для генерации изображения.
3. **Проверка**: Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL изображения соответствует ожидаемому значению ("Hello").

**ASCII flowchart**:

```
Инициализация AsyncClient с IterListProvider(YieldImageResponseProviderMock, YieldImageResponseProviderMock)
↓
Вызов client.images.generate("Hello", "", response_format="orginal")
↓
Проверка: isinstance(response, ImagesResponse) и response.data[0].url == "Hello"
```

**Примеры**:

```python
await TestIterListProvider().test_only_one_result()
```

### `test_skip_none`

```python
async def test_skip_none(self):
    """Проверяет, что клиент пропускает провайдера, если он возвращает `None`."""
```

**Назначение**: Проверка, что асинхронный клиент корректно пропускает провайдера изображений, если тот возвращает `None`.

**Параметры**:

- `self`: Ссылка на экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Как работает функция**:

1. **Инициализация**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` (имитирует провайдера, возвращающего `None`) и `YieldImageResponseProviderMock` (имитирует провайдера, возвращающего успешный ответ).
2. **Вызов**: Вызывается метод `client.images.generate` для генерации изображения.
3. **Проверка**: Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL изображения соответствует ожидаемому значению ("Hello").

**ASCII flowchart**:

```
Инициализация AsyncClient с IterListProvider(YieldNoneProviderMock, YieldImageResponseProviderMock)
↓
Вызов client.images.generate("Hello", "", response_format="orginal")
↓
Проверка: isinstance(response, ImagesResponse) и response.data[0].url == "Hello"
```

**Примеры**:

```python
await TestIterListProvider().test_skip_none()
```

### `test_raise_exception`

```python
def test_raise_exception(self):
    """Проверяет, что клиент правильно обрабатывает исключения, возникающие при работе провайдера."""
```

**Назначение**: Проверка, что асинхронный клиент корректно обрабатывает исключения, возникающие при работе одного из провайдеров изображений.

**Параметры**:

- `self`: Ссылка на экземпляр класса `TestIterListProvider`.

**Возвращает**:

- `None`

**Как работает функция**:

1. **Определение внутренней функции `run_exception`**: Определяется асинхронная функция `run_exception`, которая создает экземпляр `AsyncClient` с `IterListProvider`, содержащим `YieldNoneProviderMock` (имитирует провайдера, возвращающего `None`) и `AsyncRaiseExceptionProviderMock` (имитирует провайдера, выбрасывающего исключение).
2. **Вызов**: Внутренняя функция `run_exception` вызывает метод `client.images.generate` для генерации изображения.
3. **Проверка**: Проверяется, что при запуске `run_exception` с помощью `asyncio.run` выбрасывается исключение `RuntimeError`.

**Внутренние функции**:

#### `run_exception`

```python
async def run_exception():
    """Внутренняя функция, которая создает клиент и вызывает метод генерации изображений, что приводит к исключению."""
```

**Назначение**: Создание асинхронного клиента и вызов метода генерации изображений, который должен привести к возникновению исключения.

**Параметры**:

- `None`

**Возвращает**:

- `None`

**Как работает функция**:

1. **Инициализация**: Создается экземпляр `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` и `AsyncRaiseExceptionProviderMock`.
2. **Вызов**: Вызывается метод `client.images.generate` для генерации изображения. Этот вызов должен привести к исключению, так как `AsyncRaiseExceptionProviderMock` выбрасывает `RuntimeError`.

**ASCII flowchart**:

```
Определение асинхронной функции run_exception()
↓
Инициализация AsyncClient с IterListProvider(YieldNoneProviderMock, AsyncRaiseExceptionProviderMock)
↓
Вызов client.images.generate("Hello", "")
↓
AsyncRaiseExceptionProviderMock выбрасывает RuntimeError
```

**ASCII flowchart**:

```
Определение асинхронной функции run_exception()
↓
Инициализация AsyncClient с IterListProvider(YieldNoneProviderMock, AsyncRaiseExceptionProviderMock)
↓
Вызов client.images.generate("Hello", "") внутри run_exception()
↓
Проверка: asyncio.run(run_exception()) вызывает RuntimeError
```

**Примеры**:

```python
TestIterListProvider().test_raise_exception()