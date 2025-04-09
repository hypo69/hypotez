# Документация модуля `models.py`

## Обзор

Модуль `models.py` содержит набор юнит-тестов для проверки совместимости моделей с различными провайдерами в библиотеке `g4f`. Он проверяет, что каждый провайдер поддерживает заявленные модели и что все провайдеры находятся в рабочем состоянии.

## Подробнее

Этот модуль предназначен для автоматической проверки соответствия между моделями и провайдерами, а также для выявления неработающих провайдеров. Он использует библиотеку `unittest` для создания тестовых случаев и асинхронные вызовы для ускорения процесса тестирования.

## Классы

### `TestProviderHasModel`

**Описание**: Класс `TestProviderHasModel` наследуется от `unittest.TestCase` и содержит методы для тестирования наличия моделей у провайдеров и проверки их работоспособности.

**Принцип работы**:
Класс выполняет итерацию по всем моделям и провайдерам, определенным в `__models__`, и проверяет, что каждый провайдер поддерживает соответствующие модели. Также проверяется свойство `working` каждого провайдера, чтобы убедиться, что он находится в рабочем состоянии.

**Аттрибуты**:
- `cache` (dict): Словарь, используемый для кэширования результатов метода `get_models()` каждого провайдера.

**Методы**:
- `test_provider_has_model()`: Проходит по всем моделям и провайдерам и вызывает `provider_has_model()` для каждой пары.
- `provider_has_model(provider: Type[BaseProvider], model: str)`: Проверяет, что указанный провайдер поддерживает указанную модель.
- `test_all_providers_working()`: Проверяет, что все провайдеры находятся в рабочем состоянии.

## Функции

### `test_provider_has_model`

```python
def test_provider_has_model(self):
    """
    Проходит по всем моделям и провайдерам и вызывает `provider_has_model()` для каждой пары.
    """
    ...
```

**Назначение**: Метод `test_provider_has_model` выполняет итерацию по всем моделям и провайдерам, определенным в `__models__.values()`, и для каждой пары вызывает метод `provider_has_model` для проверки, что провайдер поддерживает данную модель. Если провайдер является подклассом `ProviderModelMixin`, метод проверяет наличие модели в атрибуте `model_aliases` провайдера.

**Как работает функция**:

```
Начало
|
Итерация по моделям и провайдерам (__models__.values())
|
Проверка, является ли провайдер подклассом ProviderModelMixin
|
Да → Проверка наличия model.name в provider.model_aliases
|   |
|   Да → model_name = provider.model_aliases[model.name]
|   Нет → model_name = model.name
|
Нет → model_name = model.name
|
Вызов self.provider_has_model(provider, model_name)
|
Конец
```

**Примеры**:

```python
import unittest
from unittest.mock import MagicMock

class TestProviderHasModelExample(unittest.TestCase):
    def test_provider_has_model_example(self):
        # Моделируем структуру __models__ для теста
        mock_model = MagicMock(name="TestModel")
        mock_provider = MagicMock(__name__="TestProvider", model_aliases={"TestModel": "TestModelAlias"})
        __models__ = {"TestModel": (mock_model, [mock_provider])}

        test_instance = TestProviderHasModel()
        test_instance.provider_has_model = MagicMock()  # Мокируем provider_has_model для проверки вызова

        test_instance.test_provider_has_model()

        # Проверяем, что provider_has_model был вызван с ожидаемыми аргументами
        test_instance.provider_has_model.assert_called_with(mock_provider, "TestModelAlias")

```

### `provider_has_model`

```python
def provider_has_model(self, provider: Type[BaseProvider], model: str):
    """
    Проверяет, что указанный провайдер поддерживает указанную модель.
    """
    ...
```

**Назначение**: Метод `provider_has_model` проверяет, поддерживает ли указанный провайдер указанную модель. Он использует кэш `self.cache` для хранения результатов вызова `provider.get_models()`, чтобы избежать повторных вызовов. Если провайдер не найден в кэше, метод пытается получить список моделей от провайдера и сохраняет его в кэше. Затем метод проверяет, что указанная модель присутствует в списке моделей, полученном от провайдера.

**Параметры**:
- `provider` (Type[BaseProvider]): Тип провайдера, который нужно проверить.
- `model` (str): Название модели, наличие которой нужно проверить у провайдера.

**Как работает функция**:

```
Начало
|
Проверка наличия provider.__name__ в self.cache
|
Да → Получение списка моделей из кэша
|
Нет → Попытка получения списка моделей от провайдера (provider.get_models())
|   |
|   Успех → Сохранение списка моделей в self.cache[provider.__name__]
|   |
|   Неудача (MissingRequirementsError, MissingAuthError) → Выход из функции
|
Проверка наличия model в списке моделей
|
Да → Успешное завершение
|
Нет → Вывод сообщения об ошибке (AssertionError)
|
Конец
```

**Примеры**:

```python
import unittest
from unittest.mock import MagicMock

class TestProviderHasModelExample(unittest.TestCase):
    def test_provider_has_model_example(self):
        test_instance = TestProviderHasModel()
        test_instance.cache = {}

        mock_provider = MagicMock(__name__="TestProvider")
        mock_provider.get_models.return_value = ["TestModel"]
        model_name = "TestModel"

        test_instance.provider_has_model(mock_provider, model_name)

        self.assertIn("TestProvider", test_instance.cache)
        self.assertEqual(test_instance.cache["TestProvider"], ["TestModel"])
        mock_provider.get_models.assert_called_once()
```

### `test_all_providers_working`

```python
def test_all_providers_working(self):
    """
    Проверяет, что все провайдеры находятся в рабочем состоянии.
    """
    ...
```

**Назначение**: Метод `test_all_providers_working` проверяет, что все провайдеры, перечисленные в `__models__.values()`, находятся в рабочем состоянии. Он выполняет итерацию по всем провайдерам и проверяет значение атрибута `working`. Если атрибут `working` имеет значение `False`, метод генерирует ошибку, указывающую, что провайдер не работает.

**Как работает функция**:

```
Начало
|
Итерация по моделям и провайдерам (__models__.values())
|
Проверка значения provider.working
|
True → Продолжение итерации
|
False → Вывод сообщения об ошибке (AssertionError)
|
Конец
```

**Примеры**:

```python
import unittest
from unittest.mock import MagicMock

class TestProviderHasModelExample(unittest.TestCase):
    def test_all_providers_working_example(self):
        test_instance = TestProviderHasModel()

        mock_model = MagicMock(name="TestModel")
        mock_provider = MagicMock(__name__="TestProvider", working=True)
        __models__ = {"TestModel": (mock_model, [mock_provider])}

        test_instance.test_all_providers_working()

        mock_provider.working = False
        with self.assertRaises(AssertionError):
            test_instance.test_all_providers_working()