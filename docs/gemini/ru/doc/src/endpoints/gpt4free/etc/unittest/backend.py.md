# Модуль `backend.py`

## Обзор

Данный модуль содержит набор тестов для класса `Backend_Api`, который обеспечивает бэкенд-функциональность для GUI-приложения проекта `hypotez`. Тесты проверяют основные функции API, включая получение версии, моделей, провайдеров и поиск в интернете.

## Тесты

### Класс `TestBackendApi`

**Описание**: Класс `TestBackendApi` предоставляет тесты для проверки функциональности класса `Backend_Api`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:

- `app (MagicMock)`: Заглушка приложения, используемая в тестах.
- `api (Backend_Api)`: Экземпляр класса `Backend_Api`, созданный для тестирования.

**Методы**:

- `setUp()`: Метод настройки, вызываемый перед каждым тестом. Проверяет наличие необходимых зависимостей (GUI) и инициализирует заглушку приложения и экземпляр класса `Backend_Api`.

- `test_version()`: Тест проверки метода `get_version()`, который возвращает версию API и последнюю доступную версию.

- `test_get_models()`: Тест проверки метода `get_models()`, который возвращает список доступных моделей.

- `test_get_providers()`: Тест проверки метода `get_providers()`, который возвращает список доступных провайдеров.

- `test_search()`: Тест проверки метода `search()`, который выполняет поиск в интернете. Метод использует заглушку для функции `search` из `g4f.gui.server.internet`. Если поиск в интернете не доступен, тест пропускается.

**Примеры**:

```python
# Создание экземпляра тестового класса
test_backend_api = TestBackendApi()

# Запуск метода setUp() для настройки
test_backend_api.setUp()

# Вызов метода test_version() для проверки метода get_version()
test_backend_api.test_version()

# Вызов метода test_get_models() для проверки метода get_models()
test_backend_api.test_get_models()

# Вызов метода test_get_providers() для проверки метода get_providers()
test_backend_api.test_get_providers()

# Вызов метода test_search() для проверки метода search()
test_backend_api.test_search()
```
```python
                from __future__ import annotations

import unittest
import asyncio
from unittest.mock import MagicMock
from g4f.errors import MissingRequirementsError
try:
    from g4f.gui.server.backend_api import Backend_Api
    has_requirements = True
except:
    has_requirements = False
try:
    from duckduckgo_search.exceptions import DuckDuckGoSearchException
except ImportError:
    class DuckDuckGoSearchException:
        pass

class TestBackendApi(unittest.TestCase):

    def setUp(self):
        """
        Метод настройки, вызываемый перед каждым тестом.
        Проверяет наличие необходимых зависимостей (GUI) и инициализирует заглушку приложения и экземпляр класса `Backend_Api`.
        """
        if not has_requirements:
            self.skipTest("gui is not installed")
        self.app = MagicMock()
        self.api = Backend_Api(self.app)

    def test_version(self):
        """
        Тест проверки метода `get_version()`, который возвращает версию API и последнюю доступную версию.
        """
        response = self.api.get_version()
        self.assertIn("version", response)
        self.assertIn("latest_version", response)

    def test_get_models(self):
        """
        Тест проверки метода `get_models()`, который возвращает список доступных моделей.
        """
        response = self.api.get_models()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_get_providers(self):
        """
        Тест проверки метода `get_providers()`, который возвращает список доступных провайдеров.
        """
        response = self.api.get_providers()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_search(self):
        """
        Тест проверки метода `search()`, который выполняет поиск в интернете. 
        Метод использует заглушку для функции `search` из `g4f.gui.server.internet`. 
        Если поиск в интернете не доступен, тест пропускается.
        """
        from g4f.gui.server.internet import search
        try:
            result = asyncio.run(search("Hello"))
        except DuckDuckGoSearchException as e:
            self.skipTest(e)
        except MissingRequirementsError:
            self.skipTest("search is not installed")
        self.assertGreater(len(result), 0)

                ```