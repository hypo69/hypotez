# Модуль `test_categories_from_template.py`

## Обзор

Модуль содержит класс `TestBuildtemplates`, используемый для тестирования функциональности создания шаблонов категорий. Этот модуль содержит тесты, которые проверяют правильность обработки JSON-файлов в директориях и поддиректориях, а также обрабатывает ситуации, когда указанная директория не существует.

## Подробней

Этот модуль предназначен для автоматизированного тестирования процесса создания шаблонов категорий на основе JSON-файлов. Он использует библиотеку `unittest` для определения тестовых случаев и временные директории для изоляции тестов. Модуль проверяет, что шаблоны правильно строятся из существующих директорий с JSON-файлами и обрабатывают исключения, когда директория не существует.

## Классы

### `TestBuildtemplates`

**Описание**: Класс `TestBuildtemplates` предназначен для тестирования функции `buid_templates`. Он содержит два метода: `test_build_templates_with_existing_directory` и `test_build_templates_with_non_existing_directory`, которые тестируют различные сценарии работы функции `buid_templates`.

**Наследует**:
- `unittest.TestCase`

**Атрибуты**:
- Отсутствуют

**Методы**:
- `test_build_templates_with_existing_directory()`: Тестирует случай, когда функция `buid_templates` вызывается с существующей директорией.
- `test_build_templates_with_non_existing_directory()`: Тестирует случай, когда функция `buid_templates` вызывается с несуществующей директорией.

**Принцип работы**:
Класс использует методы `unittest.TestCase` для определения тестовых случаев. В методе `test_build_templates_with_existing_directory` создается временная директория, в которой создаются JSON-файлы. Затем вызывается функция `buid_templates` с этой директорией, и результат сравнивается с ожидаемым результатом. В методе `test_build_templates_with_non_existing_directory` вызывается функция `buid_templates` с несуществующей директорией, и проверяется, что возникает исключение `FileNotFoundError`.

## Методы класса

### `test_build_templates_with_existing_directory`

```python
def test_build_templates_with_existing_directory(self):
    """
    Тестирует создание шаблонов категорий с существующей директорией.

    Создает временную директорию и добавляет в неё несколько JSON-файлов.
    Затем вызывает функцию `buid_templates` с этой директорией и проверяет,
    что возвращаемый результат соответствует ожидаемому.
    """
    # Создание временной директории и добавление JSON-файлов
    with tempfile.TemporaryDirectory() as tmpdir:
        json_data = '{"category1": {"template1": "some content"}, "category2": {"template2": "some content"}}'
        file1_path = os.path.join(tmpdir, 'file1.json')
        with open(file1_path, 'w') as f:
            f.write(json_data)
        file2_path = os.path.join(tmpdir, 'subdir', 'file2.json')
        os.makedirs(os.path.dirname(file2_path))
        with open(file2_path, 'w') as f:
            f.write(json_data)

        # Вызов функции и проверка результата
        expected_output = {"category1": {
            "template1": "some content"}, "category2": {"template2": "some content"}}
        self.assertEqual(buid_templates(tmpdir), expected_output)
```

**Назначение**:
Тестирование функции `buid_templates` с существующей директорией.

**Параметры**:
- `self` (TestBuildtemplates): Экземпляр класса `TestBuildtemplates`.

**Возвращает**:
- None

**Вызывает исключения**:
- Отсутствуют

**Как работает функция**:
1. Создаёт временную директорию с помощью `tempfile.TemporaryDirectory()`.
2. Определяет строковую переменную `json_data`, содержащую JSON-данные для записи в файлы.
3. Создаёт файл `file1.json` в корне временной директории и записывает в него `json_data`.
4. Создаёт поддиректорию `subdir` во временной директории и файл `file2.json` в этой поддиректории, записывая в него `json_data`.
5. Определяет ожидаемый результат `expected_output`.
6. Вызывает функцию `buid_templates` с путем к временной директории.
7. Использует метод `self.assertEqual` для сравнения результата, возвращённого функцией `buid_templates`, с ожидаемым результатом `expected_output`.

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

### `test_build_templates_with_non_existing_directory`

```python
def test_build_templates_with_non_existing_directory(self):
    """
    Тестирует создание шаблонов категорий с несуществующей директорией.

    Вызывает функцию `buid_templates` с путём к несуществующей директории и проверяет,
    что возникает исключение `FileNotFoundError`.
    """
    # Вызов функции с несуществующей директорией и проверка исключения
    with self.assertRaises(FileNotFoundError):
        buid_templates('/non/existing/path/')
```

**Назначение**:
Тестирование функции `buid_templates` с несуществующей директорией.

**Параметры**:
- `self` (TestBuildtemplates): Экземпляр класса `TestBuildtemplates`.

**Возвращает**:
- None

**Вызывает исключения**:
- `FileNotFoundError`: Ожидается, что функция `buid_templates` вызовет это исключение при передаче несуществующей директории.

**Как работает функция**:
1. Использует менеджер контекста `self.assertRaises(FileNotFoundError)` для проверки, что при вызове функции `buid_templates` с несуществующим путём `/non/existing/path/` будет возбуждено исключение `FileNotFoundError`.

**Примеры**:
```python
import unittest

class TestBuildtemplates(unittest.TestCase):
    def test_build_templates_with_non_existing_directory(self):
        with self.assertRaises(FileNotFoundError):
            buid_templates('/non/existing/path/')