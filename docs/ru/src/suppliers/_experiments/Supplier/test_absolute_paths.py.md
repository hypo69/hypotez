# Модуль `test_absolute_paths.py`

## Обзор

Модуль `test_absolute_paths.py` содержит набор тестов для функции `set_absolute_paths` класса `Supplier`. Эти тесты проверяют правильность формирования абсолютных путей на основе заданных префиксов и имен файлов. Модуль использует библиотеку `unittest` для организации тестов и `pathlib` для работы с путями.

## Подробней

Модуль предназначен для проверки корректности работы функции, которая формирует абсолютные пути к файлам поставщика, используя префиксы и имена файлов. Тесты охватывают различные сценарии, включая одиночные и множественные имена файлов, префиксы в виде строк и списков, а также случаи отсутствия имен файлов. Это важно для обеспечения правильной работы с файлами и каталогами в контексте поставщика.

## Классы

### `TestSetAbsolutePaths`

**Описание**: Класс `TestSetAbsolutePaths` является набором тестов для проверки функции `set_absolute_paths` класса `Supplier`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- `supplier_abs_path` (str): Абсолютный путь к каталогу поставщика, используемый в тестах.
- `function` (Callable): Ссылка на функцию `set_absolute_paths` класса `Supplier`, которую необходимо протестировать.

**Методы**:
- `setUp()`: Метод, выполняемый перед каждым тестом. Инициализирует атрибуты `supplier_abs_path` и `function`.
- `test_single_filename_with_prefix_as_string()`: Тест проверяет формирование абсолютного пути для одного имени файла с префиксом в виде строки.
- `test_single_filename_with_prefix_as_list()`: Тест проверяет формирование абсолютного пути для одного имени файла с префиксом в виде списка.
- `test_multiple_filenames_with_prefix_as_string()`: Тест проверяет формирование списка абсолютных путей для нескольких имен файлов с префиксом в виде строки.
- `test_multiple_filenames_with_prefix_as_list()`: Тест проверяет формирование списка абсолютных путей для нескольких имен файлов с префиксом в виде списка.
- `test_no_related_filenames_with_prefix_as_string()`: Тест проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде строки.
- `test_no_related_filenames_with_prefix_as_list()`: Тест проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде списка.

#### `setUp`

```python
    def setUp(self):
        self.supplier_abs_path = '/path/to/supplier'
        self.function = Supplier().set_absolute_paths
```

**Назначение**: Метод `setUp` выполняется перед каждым тестовым методом. Он инициализирует атрибуты `supplier_abs_path` и `function` для использования в тестах.

**Как работает функция**:
- Устанавливает значение `self.supplier_abs_path` в '/path/to/supplier', которое представляет собой абсолютный путь к каталогу поставщика.
- Получает ссылку на функцию `set_absolute_paths` класса `Supplier` и сохраняет ее в `self.function`.

#### `test_single_filename_with_prefix_as_string`

```python
    def test_single_filename_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = 'file.txt'
        expected_result = Path(self.supplier_abs_path, prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование абсолютного пути для одного имени файла с префиксом в виде строки.

**Как работает функция**:
- Определяет `prefix` как 'subfolder' (строка).
- Определяет `related_filenames` как 'file.txt' (строка).
- Вычисляет ожидаемый результат `expected_result` с использованием `Path` из `pathlib`, объединяя `self.supplier_abs_path`, `prefix` и `related_filenames`.
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

#### `test_single_filename_with_prefix_as_list`

```python
    def test_single_filename_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = 'file.txt'
        expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование абсолютного пути для одного имени файла с префиксом в виде списка.

**Как работает функция**:
- Определяет `prefix` как `['subfolder', 'subsubfolder']` (список строк).
- Определяет `related_filenames` как 'file.txt' (строка).
- Вычисляет ожидаемый результат `expected_result` с использованием `Path` из `pathlib`, объединяя `self.supplier_abs_path`, элементы `prefix` (распакованные с помощью `*`) и `related_filenames`.
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

#### `test_multiple_filenames_with_prefix_as_string`

```python
    def test_multiple_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование списка абсолютных путей для нескольких имен файлов с префиксом в виде строки.

**Как работает функция**:
- Определяет `prefix` как 'subfolder' (строка).
- Определяет `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']` (список строк).
- Вычисляет ожидаемый результат `expected_result` как список объектов `Path`, каждый из которых формируется объединением `self.supplier_abs_path`, `prefix` и соответствующего имени файла из `related_filenames`.
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

#### `test_multiple_filenames_with_prefix_as_list`

```python
    def test_multiple_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, *prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование списка абсолютных путей для нескольких имен файлов с префиксом в виде списка.

**Как работает функция**:
- Определяет `prefix` как `['subfolder', 'subsubfolder']` (список строк).
- Определяет `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']` (список строк).
- Вычисляет ожидаемый результат `expected_result` как список объектов `Path`, каждый из которых формируется объединением `self.supplier_abs_path`, элементов `prefix` (распакованных с помощью `*`) и соответствующего имени файла из `related_filenames`.
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

#### `test_no_related_filenames_with_prefix_as_string`

```python
    def test_no_related_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде строки.

**Как работает функция**:
- Определяет `prefix` как 'subfolder' (строка).
- Определяет `related_filenames` как `None`.
- Вычисляет ожидаемый результат `expected_result` с использованием `Path` из `pathlib`, объединяя `self.supplier_abs_path` и `prefix`.
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

#### `test_no_related_filenames_with_prefix_as_list`

```python
    def test_no_related_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, *prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тест проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде списка.

**Как работает функция**:
- Определяет `prefix` как `['subfolder', 'subsubfolder']` (список строк).
- Определяет `related_filenames` как `None`.
- Вычисляет ожидаемый результат `expected_result` с использованием `Path` из `pathlib`, объединяя `self.supplier_abs_path` и элементы `prefix` (распакованные с помощью `*`).
- Вызывает тестируемую функцию `self.function` с `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью `self.assertEqual`.

## Примеры

```python
import unittest
from pathlib import Path
from src.suppliers import Supplier

class TestSetAbsolutePaths(unittest.TestCase):
    def setUp(self):
        self.supplier_abs_path = '/path/to/supplier'
        self.function = Supplier().set_absolute_paths

    def test_single_filename_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = 'file.txt'
        expected_result = Path(self.supplier_abs_path, prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
    def test_single_filename_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = 'file.txt'
        expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
    def test_multiple_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
    def test_multiple_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, *prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
    def test_no_related_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
    def test_no_related_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, *prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```
```python
if __name__ == '__main__':
    unittest.main()