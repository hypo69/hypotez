# Модуль `test_absolute_paths`

## Обзор

Модуль `test_absolute_paths.py` предназначен для тестирования функциональности установки абсолютных путей в контексте поставщика (Supplier) в проекте `hypotez`. Он содержит класс `TestSetAbsolutePaths`, который использует библиотеку `unittest` для проверки правильности формирования абсолютных путей на основе предоставленных префиксов и связанных имен файлов.

## Подробней

Этот модуль выполняет набор тестов, чтобы убедиться, что функция `set_absolute_paths` правильно обрабатывает различные сценарии, такие как:

- Префикс задан строкой или списком.
- Имена связанных файлов заданы строкой, списком или отсутствуют.

Тесты охватывают все эти комбинации, чтобы гарантировать надежность функции `set_absolute_paths`.

## Классы

### `TestSetAbsolutePaths`

**Описание**: Класс `TestSetAbsolutePaths` наследуется от `unittest.TestCase` и содержит набор тестовых методов для проверки функции `set_absolute_paths` класса `Supplier`.

**Наследует**:

- `unittest.TestCase`

**Атрибуты**:

- `supplier_abs_path` (str): Абсолютный путь к директории поставщика.
- `function` (method): Ссылка на метод `set_absolute_paths` класса `Supplier`, который будет тестироваться.

**Методы**:

- `setUp()`: Метод, выполняемый перед каждым тестовым методом. Инициализирует атрибуты `supplier_abs_path` и `function`.
- `test_single_filename_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имя файла одно.
- `test_single_filename_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имя файла одно.
- `test_multiple_filenames_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имена файлов представлены списком.
- `test_multiple_filenames_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имена файлов представлены списком.
- `test_no_related_filenames_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имена файлов отсутствуют.
- `test_no_related_filenames_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имена файлов отсутствуют.

## Методы класса

### `setUp`

```python
def setUp(self):
    self.supplier_abs_path = '/path/to/supplier'
    self.function = Supplier().set_absolute_paths
```

**Назначение**:
Метод `setUp` выполняется перед каждым тестовым методом. Он инициализирует атрибуты `supplier_abs_path` и `function`, которые используются в тестовых методах для проверки функции `set_absolute_paths`.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Устанавливает значение атрибута `supplier_abs_path` как '/path/to/supplier'.
- Устанавливает значение атрибута `function` как метод `set_absolute_paths` экземпляра класса `Supplier`.

### `test_single_filename_with_prefix_as_string`

```python
def test_single_filename_with_prefix_as_string(self):
    prefix = 'subfolder'
    related_filenames = 'file.txt'
    expected_result = Path(self.supplier_abs_path, prefix, related_filenames)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**:
Тестирует случай, когда префикс задан строкой, а имя файла одно.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как 'subfolder' и `related_filenames` как 'file.txt'.
- Формирует ожидаемый результат `expected_result` с использованием `Path` и переданных значений.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

### `test_single_filename_with_prefix_as_list`

```python
def test_single_filename_with_prefix_as_list(self):
    prefix = ['subfolder', 'subsubfolder']
    related_filenames = 'file.txt'
    expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**:
Тестирует случай, когда префикс задан списком, а имя файла одно.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как `['subfolder', 'subsubfolder']` и `related_filenames` как 'file.txt'.
- Формирует ожидаемый результат `expected_result` с использованием `Path`, распаковывая список `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

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

**Назначение**:
Тестирует случай, когда префикс задан строкой, а имена файлов представлены списком.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как 'subfolder' и `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` как список объектов `Path`, используя генератор списка.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

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

**Назначение**:
Тестирует случай, когда префикс задан списком, а имена файлов представлены списком.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как `['subfolder', 'subsubfolder']` и `related_filenames` как `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` как список объектов `Path`, используя генератор списка и распаковывая список `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

### `test_no_related_filenames_with_prefix_as_string`

```python
def test_no_related_filenames_with_prefix_as_string(self):
    prefix = 'subfolder'
    related_filenames = None
    expected_result = Path(self.supplier_abs_path, prefix)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**:
Тестирует случай, когда префикс задан строкой, а имена файлов отсутствуют.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как 'subfolder' и `related_filenames` как `None`.
- Формирует ожидаемый результат `expected_result` с использованием `Path` и `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

### `test_no_related_filenames_with_prefix_as_list`

```python
def test_no_related_filenames_with_prefix_as_list(self):
    prefix = ['subfolder', 'subsubfolder']
    related_filenames = None
    expected_result = Path(self.supplier_abs_path, *prefix)

    result = self.function(prefix, related_filenames)

    self.assertEqual(result, expected_result)
```

**Назначение**:
Тестирует случай, когда префикс задан списком, а имена файлов отсутствуют.

**Параметры**:

- `self` (TestSetAbsolutePaths): Ссылка на экземпляр класса `TestSetAbsolutePaths`.

**Как работает функция**:

- Определяет переменные `prefix` как `['subfolder', 'subsubfolder']` и `related_filenames` как `None`.
- Формирует ожидаемый результат `expected_result` с использованием `Path`, распаковывая список `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Сравнивает полученный результат `result` с ожидаемым `expected_result` с помощью метода `assertEqual`.

## Параметры класса

- `supplier_abs_path` (str): Абсолютный путь к директории поставщика.
- `function` (method): Ссылка на метод `set_absolute_paths` класса `Supplier`, который будет тестироваться.