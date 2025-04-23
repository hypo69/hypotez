# Документация для модуля `models.py`

## Обзор

Модуль `models.py` предназначен для модульного тестирования провайдеров моделей в проекте `g4f`. Он проверяет, что каждый провайдер имеет доступ к заявленным моделям и что все провайдеры работают корректно.

## Подробней

Этот модуль содержит класс `TestProviderHasModel`, который использует библиотеку `unittest` для автоматизированного тестирования. Он перебирает все модели и провайдеры, определенные в `__models__`, и проверяет, что каждый провайдер имеет модель с правильным именем в списке доступных моделей. Также проверяется свойство `working` каждого провайдера.

## Классы

### `TestProviderHasModel`

**Описание**: Класс для тестирования наличия моделей у провайдеров и их работоспособности.
**Наследует**: `unittest.TestCase`

**Атрибуты**:
- `cache` (dict): Словарь для кэширования результатов `provider.get_models()`, чтобы избежать повторных вызовов.

**Методы**:
- `test_provider_has_model()`: Основной метод для запуска тестов.
- `provider_has_model(provider: Type[BaseProvider], model: str)`: Проверяет, имеет ли указанный провайдер указанную модель.
- `test_all_providers_working()`: Проверяет, что все провайдеры помечены как работающие (`working`).

## Методы класса

### `test_provider_has_model`

```python
def test_provider_has_model(self):
    """
    Выполняет итерацию по всем моделям и провайдерам в `__models__` и проверяет,
    что каждый провайдер имеет доступ к заявленным моделям.
    """
```

**Назначение**:
Выполняет итерацию по всем моделям и провайдерам, определенным в `__models__`. Для каждой пары "модель-провайдер" проверяет, что провайдер имеет доступ к модели, используя метод `provider_has_model`.

**Как работает функция**:

1.  **Итерация по моделям и провайдерам**:
    *   Функция начинает с итерации по всем моделям и провайдерам, хранящимся в `__models__.values()`.
2.  **Проверка типа провайдера**:
    *   Для каждого провайдера проверяется, является ли он подклассом `ProviderModelMixin`. Этот класс-примесь указывает, что провайдер должен поддерживать псевдонимы моделей.
3.  **Определение имени модели**:
    *   Если провайдер поддерживает псевдонимы моделей, функция проверяет, есть ли псевдоним для текущей модели в `provider.model_aliases`. Если псевдоним существует, используется он; в противном случае используется исходное имя модели.
4.  **Вызов `provider_has_model`**:
    *   Вызывается метод `self.provider_has_model(provider, model_name)` для фактической проверки наличия модели у провайдера.

### `provider_has_model`

```python
def provider_has_model(self, provider: Type[BaseProvider], model: str):
    """
    Проверяет, имеет ли указанный провайдер указанную модель.

    Args:
        provider (Type[BaseProvider]): Тип провайдера для проверки.
        model (str): Имя модели для проверки.
    """
```

**Назначение**:
Проверяет, имеет ли указанный провайдер указанную модель в списке доступных моделей.

**Параметры**:
- `provider` (Type[BaseProvider]): Тип провайдера для проверки.
- `model` (str): Имя модели для проверки.

**Как работает функция**:

1.  **Кэширование моделей провайдера**:
    *   Функция проверяет, есть ли в `self.cache` информация о моделях для данного провайдера. Если информации нет, то делается попытка получить список моделей, вызвав `provider.get_models()`.
    *   Если при получении списка моделей возникают исключения `MissingRequirementsError` или `MissingAuthError`, функция завершается без выполнения дальнейших проверок.
    *   Полученный список моделей сохраняется в `self.cache` для дальнейшего использования.
2.  **Проверка наличия модели у провайдера**:
    *   Функция проверяет, что `self.cache[provider.__name__]` не является пустым.
    *   Используется метод `self.assertIn(model, self.cache[provider.__name__], provider.__name__)` для проверки, что указанная модель (`model`) присутствует в списке моделей, полученных от провайдера. Если модель отсутствует, тест завершится с ошибкой.

### `test_all_providers_working`

```python
def test_all_providers_working(self):
    """
    Проверяет, что все провайдеры помечены как работающие (`working`).
    """
```

**Назначение**:
Проверяет, что все провайдеры в списке моделей имеют свойство `working` установленным в `True`.

**Как работает функция**:

1.  **Итерация по моделям и провайдерам**:
    *   Функция итерируется по всем моделям и провайдерам, хранящимся в `__models__.values()`.
2.  **Проверка свойства `working`**:
    *   Для каждого провайдера используется метод `self.assertTrue(provider.working, f"{provider.__name__} in {model.name}")` для проверки, что свойство `provider.working` имеет значение `True`. Если это не так, тест завершится с ошибкой, указав имя провайдера и модели.

## Примеры

### Пример использования `TestProviderHasModel`

```python
import unittest
from typing import Type
from g4f.models import __models__
from g4f.providers.base_provider import BaseProvider, ProviderModelMixin

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

if __name__ == '__main__':
    unittest.main()
```

В этом примере создается класс `TestProviderHasModel`, который наследуется от `unittest.TestCase`. Он содержит методы для тестирования наличия моделей у провайдеров и их работоспособности. При запуске `unittest.main()` будут выполнены все тесты, определенные в классе.