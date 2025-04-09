# Документация для модуля backend.py

## Обзор

Модуль `backend.py` содержит набор юнит-тестов для тестирования `Backend_Api` из `g4f.gui.server.backend_api`. Эти тесты проверяют различные аспекты API, такие как получение версии, моделей, провайдеров и выполнение поиска.

## Подробней

Этот модуль предназначен для автоматизированной проверки работоспособности API, предоставляемого `Backend_Api`. Он использует `unittest` для организации тестов и `asyncio` для запуска асинхронных функций. В случае отсутствия необходимых зависимостей, таких как `g4f.gui` или `duckduckgo_search`, тесты пропускаются.

## Классы

### `TestBackendApi`

**Описание**: Класс `TestBackendApi` содержит юнит-тесты для проверки функциональности `Backend_Api`.

**Наследует**:
   - `unittest.TestCase`: Класс наследует `unittest.TestCase`, предоставляя методы для написания тестов.

**Аттрибуты**:
   - `app`: `MagicMock` - Мок-объект приложения, используемый для инициализации `Backend_Api`.
   - `api`: `Backend_Api` - Экземпляр класса `Backend_Api`, который тестируется.

**Методы**:
   - `setUp()`: Подготовка к каждому тесту. Проверяет наличие необходимых зависимостей и создает мок-объект приложения, а также экземпляр `Backend_Api`.
   - `test_version()`: Тестирует метод `get_version()` класса `Backend_Api`.
   - `test_get_models()`: Тестирует метод `get_models()` класса `Backend_Api`.
   - `test_get_providers()`: Тестирует метод `get_providers()` класса `Backend_Api`.
   - `test_search()`: Тестирует функцию поиска.

#### `setUp`

```python
def setUp(self):
    """
    Подготовка к каждому тесту. Проверяет наличие необходимых зависимостей и создает мок-объект приложения,
    а также экземпляр `Backend_Api`.
    """
    ...
```

**Как работает функция**:

1. **Проверка зависимостей**: Проверяет, установлены ли необходимые зависимости для запуска GUI (`has_requirements`). Если зависимости отсутствуют, тест пропускается.
2. **Создание мок-объекта**: Создает мок-объект `MagicMock` для имитации приложения (`self.app = MagicMock()`).
3. **Инициализация API**: Создает экземпляр класса `Backend_Api`, передавая мок-объект приложения в качестве аргумента (`self.api = Backend_Api(self.app)`).

#### `test_version`

```python
def test_version(self):
    """
    Тестирует метод `get_version()` класса `Backend_Api`.
    """
    ...
```

**Как работает функция**:

1. **Вызов метода**: Вызывает метод `get_version()` у экземпляра `Backend_Api` (`response = self.api.get_version()`).
2. **Проверка результата**: Проверяет, содержит ли возвращенный словарь ключи `"version"` и `"latest_version"` с использованием `self.assertIn()`.

#### `test_get_models`

```python
def test_get_models(self):
    """
    Тестирует метод `get_models()` класса `Backend_Api`.
    """
    ...
```

**Как работает функция**:

1. **Вызов метода**: Вызывает метод `get_models()` у экземпляра `Backend_Api` (`response = self.api.get_models()`).
2. **Проверка типа**: Проверяет, является ли возвращенное значение списком с помощью `self.assertIsInstance()`.
3. **Проверка содержимого**: Проверяет, является ли длина списка больше нуля с помощью `self.assertTrue()`.

#### `test_get_providers`

```python
def test_get_providers(self):
    """
    Тестирует метод `get_providers()` класса `Backend_Api`.
    """
    ...
```

**Как работает функция**:

1. **Вызов метода**: Вызывает метод `get_providers()` у экземпляра `Backend_Api` (`response = self.api.get_providers()`).
2. **Проверка типа**: Проверяет, является ли возвращенное значение списком с помощью `self.assertIsInstance()`.
3. **Проверка содержимого**: Проверяет, является ли длина списка больше нуля с помощью `self.assertTrue()`.

#### `test_search`

```python
def test_search(self):
    """
    Тестирует функцию поиска.
    """
    ...
```

**Как работает функция**:

1. **Импорт функции**: Импортирует функцию `search` из модуля `g4f.gui.server.internet`.
2. **Вызов функции поиска**: Пытается выполнить поиск строки "Hello" асинхронно с использованием `asyncio.run(search("Hello"))`.
3. **Обработка исключений**:
   - Если возникает исключение `DuckDuckGoSearchException`, тест пропускается с помощью `self.skipTest(e)`.
   - Если возникает исключение `MissingRequirementsError`, тест пропускается с сообщением "search is not installed".
4. **Проверка результата**: Проверяет, является ли длина результата поиска больше нуля с помощью `self.assertGreater()`.

## Функции

В данном модуле функции отсутствуют, так как основная логика сосредоточена в классе `TestBackendApi` и его методах.

```python
class DuckDuckGoSearchException:
    pass
```
В данном коде определяется класс `DuckDuckGoSearchException`, если он не был импортирован из библиотеки `duckduckgo_search`. Этот класс используется для обработки исключений, связанных с поиском DuckDuckGo.
## Пример

```python
import unittest
from unittest.mock import MagicMock
import asyncio

class TestBackendApi(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.api = Backend_Api(self.app)

    def test_version(self):
        response = self.api.get_version()
        self.assertIn("version", response)
        self.assertIn("latest_version", response)

    def test_get_models(self):
        response = self.api.get_models()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)