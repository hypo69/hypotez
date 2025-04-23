# Модуль `test_absolute_paths`

## Обзор

Модуль `test_absolute_paths.py` предназначен для тестирования функциональности установки абсолютных путей в контексте работы с поставщиками (Suppliers) в проекте `hypotez`. Он содержит набор тестов, проверяющих правильность формирования абсолютных путей на основе заданных префиксов и имен файлов.

## Подробнее

Модуль использует библиотеку `unittest` для организации тестового набора и библиотеку `pathlib` для работы с путями в файловой системе. Класс `TestSetAbsolutePaths` содержит методы, проверяющие различные сценарии формирования абсолютных путей, включая случаи с одиночными и множественными именами файлов, строковыми и списочными префиксами, а также отсутствие имен файлов.

## Классы

### `TestSetAbsolutePaths`

**Описание**: Класс `TestSetAbsolutePaths` наследуется от `unittest.TestCase` и содержит методы для тестирования функции `set_absolute_paths` класса `Supplier`.

**Наследует**:
- `unittest.TestCase`

**Атрибуты**:
- `supplier_abs_path` (str): Абсолютный путь к директории поставщика, используемый в тестах.
- `function` (Callable): Функция `set_absolute_paths` класса `Supplier`, которая тестируется.

**Методы**:
- `setUp()`: Метод, выполняемый перед каждым тестом. Инициализирует атрибуты `supplier_abs_path` и `function`.
- `test_single_filename_with_prefix_as_string()`: Тест проверяет случай с одиночным именем файла и строковым префиксом.
- `test_single_filename_with_prefix_as_list()`: Тест проверяет случай с одиночным именем файла и списочным префиксом.
- `test_multiple_filenames_with_prefix_as_string()`: Тест проверяет случай с множественными именами файлов и строковым префиксом.
- `test_multiple_filenames_with_prefix_as_list()`: Тест проверяет случай с множественными именами файлов и списочным префиксом.
- `test_no_related_filenames_with_prefix_as_string()`: Тест проверяет случай отсутствия имен файлов и строкового префикса.
- `test_no_related_filenames_with_prefix_as_list()`: Тест проверяет случай отсутствия имен файлов и списочного префикса.

## Методы класса

### `setUp`

```python
def setUp(self):
    self.supplier_abs_path = '/path/to/supplier'
    self.function = Supplier().set_absolute_paths
```

**Назначение**: Инициализирует тестовое окружение перед каждым тестом.

**Как работает функция**:

- Устанавливает значение атрибута `supplier_abs_path` в `/path/to/supplier`.
- Устанавливает значение атрибута `function` в метод `set_absolute_paths` экземпляра класса `Supplier`.

### `test_single_filename_with_prefix_as_string`

```python
def test_single_filename_with_prefix_as_string(self):
    prefix = 'subfolder'
    related_filenames = 'file.txt'
    expected_result = Path(self.supplier_abs_path, prefix, related_filenames)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**: Проверяет формирование абсолютного пути с одиночным именем файла и префиксом в виде строки.

**Как работает функция**:

- Определяет префикс `prefix` как `'subfolder'`.
- Определяет имя файла `related_filenames` как `'file.txt'`.
- Формирует ожидаемый результат `expected_result` с помощью `Path`.
- Вызывает функцию `self.function` с префиксом и именем файла.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

### `test_single_filename_with_prefix_as_list`

```python
def test_single_filename_with_prefix_as_list(self):
    prefix = ['subfolder', 'subsubfolder']
    related_filenames = 'file.txt'
    expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**: Проверяет формирование абсолютного пути с одиночным именем файла и префиксом в виде списка.

**Как работает функция**:

- Определяет префикс `prefix` как `['subfolder', 'subsubfolder']`.
- Определяет имя файла `related_filenames` как `'file.txt'`.
- Формирует ожидаемый результат `expected_result` с помощью `Path` и распаковки списка префиксов.
- Вызывает функцию `self.function` с префиксом и именем файла.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

### `test_multiple_filenames_with_prefix_as_string`

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

**Назначение**: Проверяет формирование абсолютных путей с множественными именами файлов и префиксом в виде строки.

**Как работает функция**:

- Определяет префикс `prefix` как `'subfolder'`.
- Определяет список имен файлов `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` с помощью списочного включения и `Path`.
- Вызывает функцию `self.function` с префиксом и списком имен файлов.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

### `test_multiple_filenames_with_prefix_as_list`

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

**Назначение**: Проверяет формирование абсолютных путей с множественными именами файлов и префиксом в виде списка.

**Как работает функция**:

- Определяет префикс `prefix` как `['subfolder', 'subsubfolder']`.
- Определяет список имен файлов `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` с помощью списочного включения, `Path` и распаковки списка префиксов.
- Вызывает функцию `self.function` с префиксом и списком имен файлов.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

### `test_no_related_filenames_with_prefix_as_string`

```python
def test_no_related_filenames_with_prefix_as_string(self):
    prefix = 'subfolder'
    related_filenames = None
    expected_result = Path(self.supplier_abs_path, prefix)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**: Проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде строки.

**Как работает функция**:

- Определяет префикс `prefix` как `'subfolder'`.
- Определяет `related_filenames` как `None`.
- Формирует ожидаемый результат `expected_result` с помощью `Path`.
- Вызывает функцию `self.function` с префиксом и `None` в качестве имен файлов.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

### `test_no_related_filenames_with_prefix_as_list`

```python
def test_no_related_filenames_with_prefix_as_list(self):
    prefix = ['subfolder', 'subsubfolder']
    related_filenames = None
    expected_result = Path(self.supplier_abs_path, *prefix)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**: Проверяет формирование абсолютного пути при отсутствии имен файлов и префиксе в виде списка.

**Как работает функция**:

- Определяет префикс `prefix` как `['subfolder', 'subsubfolder']`.
- Определяет `related_filenames` как `None`.
- Формирует ожидаемый результат `expected_result` с помощью `Path` и распаковки списка префиксов.
- Вызывает функцию `self.function` с префиксом и `None` в качестве имен файлов.
- Проверяет, что результат `result` совпадает с ожидаемым результатом `expected_result`.

## Запуск тестов

```python
if __name__ == '__main__':
    unittest.main()
```

**Назначение**: Запускает тесты при запуске модуля.

**Как работает функция**:

- Проверяет, является ли текущий модуль главным.
- Если да, запускает тесты с помощью `unittest.main()`.