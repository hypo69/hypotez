# Модуль тестирования клиента изображений для GPT4Free

## Обзор

Этот модуль содержит тесты для клиента изображений GPT4Free.

## Детали

Тесты проверяют корректность работы клиента при использовании различных типов провайдеров, включая:

- `YieldImageResponseProviderMock`: Провайдер, который возвращает данные изображения.
- `MissingAuthProviderMock`: Провайдер, который не имеет провайдера аутентификации.
- `AsyncRaiseExceptionProviderMock`: Провайдер, который генерирует исключение.
- `YieldNoneProviderMock`: Провайдер, который возвращает `None`.

## Классы

### `TestIterListProvider`

**Описание**: Тестовый класс для `IterListProvider`.

**Наследует**:  `unittest.IsolatedAsyncioTestCase`

**Методы**:

- `test_skip_provider()`: Проверяет, что `IterListProvider` пропускает провайдера, который не имеет провайдера аутентификации.
- `test_only_one_result()`: Проверяет, что `IterListProvider` возвращает только один результат.
- `test_skip_none()`: Проверяет, что `IterListProvider` пропускает провайдера, который возвращает `None`.
- `test_raise_exception()`: Проверяет, что `IterListProvider` генерирует исключение, если провайдер генерирует исключение.

##  Функции

### `test_raise_exception()`

**Цель**: Тестирует исключение, которое генерируется при использовании `AsyncRaiseExceptionProviderMock`.

**Параметры**:  Отсутствуют.

**Возвращает**:  Отсутствует.

**Поднимает исключения**:  `RuntimeError`.

**Как работает функция**: 
- Создает экземпляр `AsyncClient` с провайдером `IterListProvider`, который содержит `AsyncRaiseExceptionProviderMock`.
- Вызывает метод `generate()` клиента для генерации изображения.
- Использует `assertRaises()` для проверки, что `RuntimeError` генерируется.

**Пример**:

```python
    def test_raise_exception(self):
        async def run_exception():
            client = AsyncClient(image_provider=IterListProvider([YieldNoneProviderMock, AsyncRaiseExceptionProviderMock], False))
            await client.images.generate("Hello", "")
        self.assertRaises(RuntimeError, asyncio.run, run_exception())
```


## Примеры

```python
    async def test_skip_provider(self):
        client = AsyncClient(image_provider=IterListProvider([MissingAuthProviderMock, YieldImageResponseProviderMock], False))
        response = await client.images.generate("Hello", "", response_format="orginal")
        self.assertIsInstance(response, ImagesResponse)
        self.assertEqual("Hello", response.data[0].url)
```