# Документация для модуля `backend.py`

## Обзор

Модуль `backend.py` содержит юнит-тесты для backend API, используемого в графическом интерфейсе (GUI) проекта `g4f`. Он проверяет корректность работы API, включая получение версий, моделей, провайдеров и выполнение поисковых запросов.

## Подробней

Этот модуль важен для обеспечения стабильности и надежности backend API, используемого в GUI. Он включает в себя тесты для основных функций API, гарантируя, что они работают правильно и возвращают ожидаемые результаты. Модуль использует `unittest` для организации тестов и `MagicMock` для имитации объектов приложения.

## Классы

### `TestBackendApi`

**Описание**: Класс `TestBackendApi` содержит набор тестов для проверки функциональности backend API.

**Наследует**:
- `unittest.TestCase`: Класс наследует от `unittest.TestCase`, предоставляя базовый функционал для написания и запуска тестов.

**Аттрибуты**:
- `app` (MagicMock): Мок-объект приложения, используемый для имитации взаимодействия с приложением.
- `api` (Backend_Api): Экземпляр класса `Backend_Api`, который тестируется.
- `has_requirements` (bool): Флаг, указывающий, установлены ли все необходимые зависимости для GUI.

**Методы**:
- `setUp()`: Метод для подготовки к каждому тесту, инициализирует `MagicMock` для `app` и создает экземпляр `Backend_Api`.
- `test_version()`: Тест для проверки корректности возвращаемой версии API.
- `test_get_models()`: Тест для проверки получения списка доступных моделей.
- `test_get_providers()`: Тест для проверки получения списка доступных провайдеров.
- `test_search()`: Тест для проверки функции поиска.

### `TestBackendApi.setUp`

```python
    def setUp(self):
        if not has_requirements:
            self.skipTest("gui is not installed")
        self.app = MagicMock()
        self.api = Backend_Api(self.app)
```

**Назначение**: Подготовка к каждому тесту.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. **Проверка зависимостей**: Проверяет, установлены ли все необходимые зависимости (`has_requirements`). Если нет, тест пропускается.
2. **Инициализация мок-объекта**: Создает мок-объект `app` с использованием `MagicMock()`.
3. **Создание экземпляра API**: Создает экземпляр класса `Backend_Api`, передавая мок-объект `app`.

```
Проверка зависимостей --> Инициализация мок-объекта --> Создание экземпляра API
```

**Примеры**:

```python
# Пример использования в unittest (не вызывается напрямую)
class TestBackendApi(unittest.TestCase):
    def setUp(self):
        # Вызывается перед каждым тестом
        if not has_requirements:
            self.skipTest("gui is not installed")
        self.app = MagicMock()
        self.api = Backend_Api(self.app)
```

### `TestBackendApi.test_version`

```python
    def test_version(self):
        response = self.api.get_version()
        self.assertIn("version", response)
        self.assertIn("latest_version", response)
```

**Назначение**: Тест для проверки корректности возвращаемой версии API.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. **Вызов метода API**: Вызывает метод `get_version()` экземпляра `Backend_Api` и сохраняет результат в `response`.
2. **Проверка наличия ключей**: Проверяет, содержит ли `response` ключи `"version"` и `"latest_version"` с использованием `self.assertIn()`.

```
Вызов метода API --> Проверка наличия ключей
```

**Примеры**:

```python
# Пример использования в unittest (не вызывается напрямую)
class TestBackendApi(unittest.TestCase):
    def test_version(self):
        response = self.api.get_version()
        self.assertIn("version", response)
        self.assertIn("latest_version", response)
```

### `TestBackendApi.test_get_models`

```python
    def test_get_models(self):
        response = self.api.get_models()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)
```

**Назначение**: Тест для проверки получения списка доступных моделей.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. **Вызов метода API**: Вызывает метод `get_models()` экземпляра `Backend_Api` и сохраняет результат в `response`.
2. **Проверка типа данных**: Проверяет, является ли `response` списком с использованием `self.assertIsInstance()`.
3. **Проверка непустоты списка**: Проверяет, что длина списка `response` больше 0 с использованием `self.assertTrue()`.

```
Вызов метода API --> Проверка типа данных --> Проверка непустоты списка
```

**Примеры**:

```python
# Пример использования в unittest (не вызывается напрямую)
class TestBackendApi(unittest.TestCase):
    def test_get_models(self):
        response = self.api.get_models()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)
```

### `TestBackendApi.test_get_providers`

```python
    def test_get_providers(self):
        response = self.api.get_providers()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)
```

**Назначение**: Тест для проверки получения списка доступных провайдеров.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. **Вызов метода API**: Вызывает метод `get_providers()` экземпляра `Backend_Api` и сохраняет результат в `response`.
2. **Проверка типа данных**: Проверяет, является ли `response` списком с использованием `self.assertIsInstance()`.
3. **Проверка непустоты списка**: Проверяет, что длина списка `response` больше 0 с использованием `self.assertTrue()`.

```
Вызов метода API --> Проверка типа данных --> Проверка непустоты списка
```

**Примеры**:

```python
# Пример использования в unittest (не вызывается напрямую)
class TestBackendApi(unittest.TestCase):
    def test_get_providers(self):
        response = self.api.get_providers()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)
```

### `TestBackendApi.test_search`

```python
    def test_search(self):
        from g4f.gui.server.internet import search
        try:
            result = asyncio.run(search("Hello"))
        except DuckDuckGoSearchException as e:
            self.skipTest(e)
        except MissingRequirementsError:
            self.skipTest("search is not installed")
        self.assertGreater(len(result), 0)
```

**Назначение**: Тест для проверки функции поиска.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает функция**:
1. **Импорт функции поиска**: Импортирует функцию `search` из модуля `g4f.gui.server.internet`.
2. **Выполнение поиска**: Выполняет асинхронный поиск строки `"Hello"` с использованием `asyncio.run()` и сохраняет результат в `result`.
3. **Обработка исключений**:
   - Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.
   - Если возникает исключение `MissingRequirementsError`, тест пропускается.
4. **Проверка результата поиска**: Проверяет, что длина результата поиска `result` больше 0 с использованием `self.assertGreater()`.

```
Импорт функции поиска --> Выполнение поиска --> Обработка исключений --> Проверка результата поиска
```

**Примеры**:

```python
# Пример использования в unittest (не вызывается напрямую)
class TestBackendApi(unittest.TestCase):
    def test_search(self):
        from g4f.gui.server.internet import search
        try:
            result = asyncio.run(search("Hello"))
        except DuckDuckGoSearchException as e:
            self.skipTest(e)
        except MissingRequirementsError:
            self.skipTest("search is not installed")
        self.assertGreater(len(result), 0)
```

## Функции

В данном модуле нет отдельных функций, только методы класса `TestBackendApi`.