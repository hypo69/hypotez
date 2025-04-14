# Модуль для тестирования создания шаблонов категорий из файлов

## Обзор

Модуль `test_categories_from_template.py` содержит класс `TestBuildtemplates`, который используется для тестирования функциональности создания шаблонов категорий на основе JSON-файлов. 
Этот модуль предназначен для проверки корректности работы функции `buid_templates` (код которой, к сожалению, не был предоставлен), которая должна читать JSON-файлы из указанной директории и формировать структуру шаблонов категорий.

## Подробнее

Модуль предназначен для автоматизированного тестирования функции `buid_templates`. Тесты включают проверку чтения шаблонов из директории и обработку случая, когда директория не существует.

## Классы

### `TestBuildtemplates(unittest.TestCase)`

**Описание**: Класс `TestBuildtemplates` предназначен для выполнения автоматизированных тестов функции `buid_templates`. Он наследует класс `unittest.TestCase` и содержит методы для проверки различных сценариев работы `buid_templates`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- Отсутствуют

**Методы**:
- `test_build_templates_with_existing_directory()`: Тестирует функцию `buid_templates` с существующей директорией, содержащей JSON-файлы.
- `test_build_templates_with_non_existing_directory()`: Тестирует функцию `buid_templates` с несуществующей директорией.

#### `test_build_templates_with_existing_directory(self)`

**Назначение**: Проверяет сценарий, когда функция `buid_templates` вызывается с существующей директорией, содержащей JSON-файлы.

**Параметры**:
- `self` (TestBuildtemplates): Экземпляр класса `TestBuildtemplates`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Отсутствуют

**Как работает функция**:
1. Создается временная директория с использованием `tempfile.TemporaryDirectory()`.
2. Внутри временной директории создаются два JSON-файла: `file1.json` в корне временной директории и `file2.json` во вложенной директории `subdir`. Оба файла содержат одинаковые JSON-данные, представляющие шаблоны категорий.
3. Вызывается функция `buid_templates` с путем к временной директории.
4. Результат работы функции сравнивается с ожидаемым результатом `expected_output` с использованием метода `self.assertEqual()`.

**Примеры**:
```python
import unittest
import tempfile
import os

class TestBuildtemplates(unittest.TestCase):
    def test_build_templates_with_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            json_data = '{"category1": {"template1": "some content"}, "category2": {"template2": "some content"}}'
            file1_path = os.path.join(tmpdir, 'file1.json')
            with open(file1_path, 'w') as f:
                f.write(json_data)
            file2_path = os.path.join(tmpdir, 'subdir', 'file2.json')
            os.makedirs(os.path.dirname(file2_path))
            with open(file2_path, 'w') as f:
                f.write(json_data)

            expected_output = {"category1": {
                "template1": "some content"}, "category2": {"template2": "some content"}}
            self.assertEqual(buid_templates(tmpdir), expected_output)
```

#### `test_build_templates_with_non_existing_directory(self)`

**Назначение**: Проверяет сценарий, когда функция `buid_templates` вызывается с несуществующей директорией.

**Параметры**:
- `self` (TestBuildtemplates): Экземпляр класса `TestBuildtemplates`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `FileNotFoundError`: Ожидается, что функция `buid_templates` вызовет исключение `FileNotFoundError`, если директория не существует.

**Как работает функция**:
1. Вызывается функция `buid_templates` с путем к несуществующей директории (`/non/existing/path/`).
2. Проверяется, что функция вызывает исключение `FileNotFoundError` с использованием контекстного менеджера `self.assertRaises()`.

**Примеры**:
```python
import unittest
import tempfile
import os

class TestBuildtemplates(unittest.TestCase):
    def test_build_templates_with_non_existing_directory(self):
        with self.assertRaises(FileNotFoundError):
            buid_templates('/non/existing/path/')
```