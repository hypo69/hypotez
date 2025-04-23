# Документация для модуля `models.py`

## Обзор

Файл `models.py` содержит модульные тесты для проверки наличия моделей у различных провайдеров в проекте `hypotez`. Он проверяет, что каждый провайдер, связанный с определенной моделью, действительно имеет эту модель в своем списке доступных моделей. Также проверяется, что все провайдеры находятся в рабочем состоянии.

## Более подробно

Этот модуль используется для автоматизированной проверки соответствия между моделями и провайдерами, а также для контроля работоспособности провайдеров. Это важно для обеспечения корректной работы системы, использующей различные AI-модели и провайдеров для их доступа.

## Классы

### `TestProviderHasModel`

**Описание**: Класс `TestProviderHasModel` является модульным тестом, который проверяет наличие моделей у различных провайдеров.

**Наследует**:
- `unittest.TestCase`: Класс наследуется от `unittest.TestCase` и предоставляет инфраструктуру для написания тестов.

**Атрибуты**:
- `cache` (dict): Словарь, используемый для кэширования списка моделей каждого провайдера, чтобы избежать повторных вызовов `provider.get_models()`.

**Методы**:
- `test_provider_has_model()`: Проверяет, что каждый провайдер из списка провайдеров для каждой модели действительно имеет эту модель в своем списке доступных моделей.
- `provider_has_model(provider: Type[BaseProvider], model: str)`: Проверяет, что указанный провайдер имеет указанную модель в своем списке доступных моделей.
- `test_all_providers_working()`: Проверяет, что все провайдеры находятся в рабочем состоянии.

#### Принцип работы:

Класс `TestProviderHasModel` выполняет следующие действия:
1. Итерируется по всем моделям и провайдерам, определенным в `__models__`.
2. Для каждого провайдера проверяет, является ли он подклассом `ProviderModelMixin`.
3. Если провайдер является подклассом `ProviderModelMixin`, проверяет, имеет ли он модель в своем списке доступных моделей, вызывая метод `provider_has_model()`.
4. Метод `provider_has_model()` кэширует список моделей для каждого провайдера, чтобы избежать повторных вызовов `provider.get_models()`.
5. Метод `test_all_providers_working()` проверяет, что все провайдеры находятся в рабочем состоянии, проверяя атрибут `working`.

## Методы класса

### `test_provider_has_model`

```python
def test_provider_has_model(self):
    """Функция выполняет итерацию по всем моделям и провайдерам из `__models__` и проверяет, что каждый провайдер имеет соответствующую модель.

    Args:
        self: Экземпляр класса `TestProviderHasModel`.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не имеет ожидаемую модель.

    Как работает функция:
    - Функция итерируется по всем моделям и провайдерам, определенным в `__models__.values()`.
    - Для каждой пары модель-провайдер проверяется, является ли провайдер подклассом `ProviderModelMixin`.
    - Если провайдер является подклассом `ProviderModelMixin`, функция проверяет, есть ли у провайдера псевдоним для имени модели.
    - Затем вызывается `self.provider_has_model` для проверки, присутствует ли модель в списке моделей провайдера.

    Пример:
    >>> test_instance = TestProviderHasModel()
    >>> test_instance.test_provider_has_model()
    """
    ...
```

### `provider_has_model`

```python
def provider_has_model(self, provider: Type[BaseProvider], model: str):
    """Функция проверяет, имеет ли указанный провайдер указанную модель.

    Args:
        provider (Type[BaseProvider]): Тип провайдера для проверки.
        model (str): Имя модели для проверки.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не имеет указанную модель.

    Как работает функция:
    - Функция проверяет, есть ли в кэше информация о моделях для данного провайдера.
    - Если информации нет в кэше, пытается получить список моделей, вызывая `provider.get_models()`.
    - Если возникает исключение `MissingRequirementsError` или `MissingAuthError`, функция завершается без дальнейших действий.
    - Если список моделей получен успешно, он сохраняется в кэше.
    - Затем функция проверяет, присутствует ли указанная модель в списке моделей провайдера.

    Пример:
    >>> test_instance = TestProviderHasModel()
    >>> from g4f.providers import Ails
    >>> test_instance.provider_has_model(Ails, "gpt-3.5-turbo")
    """
    ...
```

### `test_all_providers_working`

```python
def test_all_providers_working(self):
    """Функция проверяет, что все провайдеры находятся в рабочем состоянии.

    Args:
        self: Экземпляр класса `TestProviderHasModel`.

    Returns:
        None

    Raises:
        AssertionError: Если провайдер не находится в рабочем состоянии.

    Как работает функция:
    - Функция итерируется по всем моделям и провайдерам, определенным в `__models__.values()`.
    - Для каждой пары модель-провайдер проверяется атрибут `working` провайдера.
    - Если `working` имеет значение `False`, тест завершается с ошибкой.

    Пример:
    >>> test_instance = TestProviderHasModel()
    >>> test_instance.test_all_providers_working()
    """
    ...
```

## Параметры класса

- `cache` (dict): Словарь, используемый для кэширования списка моделей каждого провайдера, чтобы избежать повторных вызовов `provider.get_models()`.

**Примеры**

Пример использования класса `TestProviderHasModel`:

```python
import unittest
from typing import Type
import asyncio

from g4f.models import __models__
from g4f.providers.base_provider import BaseProvider, ProviderModelMixin
from g4f.errors import MissingRequirementsError, MissingAuthError

class TestProviderHasModel(unittest.TestCase):
    cache: dict = {}

    def test_provider_has_model(self):
        for model, providers in __models__.values():
            for provider in providers:
                if issubclass(provider, ProviderModelMixin):
                    if model.name in provider.model_aliases:
                        model_name = provider.model_aliases[model.name]
                    else:
                        model_name = model.name
                    self.provider_has_model(provider, model_name)

    def provider_has_model(self, provider: Type[BaseProvider], model: str):
        if provider.__name__ not in self.cache:
            try:
                self.cache[provider.__name__] = provider.get_models()
            except (MissingRequirementsError, MissingAuthError):
                return
        if self.cache[provider.__name__]:
            self.assertIn(model, self.cache[provider.__name__], provider.__name__)

    def test_all_providers_working(self):
        for model, providers in __models__.values():
            for provider in providers:
                self.assertTrue(provider.working, f"{provider.__name__} in {model.name}")