# Модуль test_absolute_paths

## Обзор

Модуль `test_absolute_paths.py` предназначен для тестирования функции `set_absolute_paths` класса `Supplier`. Он проверяет, правильно ли функция формирует абсолютные пути на основе заданного префикса и относительных имен файлов.
Расположение файла в проекте: `hypotez/src/suppliers/_experiments/Supplier/test_absolute_paths.py`.

## Подробней

Этот модуль содержит класс `TestSetAbsolutePaths`, который наследует от `unittest.TestCase`. Он использует различные тестовые случаи для проверки правильности формирования абсолютных путей функцией `set_absolute_paths` класса `Supplier`.

## Классы

### `TestSetAbsolutePaths`

**Описание**: Класс `TestSetAbsolutePaths` используется для тестирования функции `set_absolute_paths` класса `Supplier`.

**Наследует**: `unittest.TestCase`

**Атрибуты**:
- `supplier_abs_path` (str): Абсолютный путь к каталогу поставщика, используемый в тестах.
- `function` (Callable): Функция `set_absolute_paths` класса `Supplier`, которая тестируется.

**Методы**:
- `setUp()`: Метод, который вызывается перед каждым тестовым методом.
- `test_single_filename_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имя файла - строкой.
- `test_single_filename_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имя файла - строкой.
- `test_multiple_filenames_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имена файлов - списком.
- `test_multiple_filenames_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имена файлов - списком.
- `test_no_related_filenames_with_prefix_as_string()`: Тестирует случай, когда префикс задан строкой, а имена файлов отсутствуют.
- `test_no_related_filenames_with_prefix_as_list()`: Тестирует случай, когда префикс задан списком, а имена файлов отсутствуют.

### `setUp`

```python
    def setUp(self):
        self.supplier_abs_path = \'/path/to/supplier\'
        self.function = Supplier().set_absolute_paths
```

**Назначение**: Инициализирует переменные, необходимые для тестов.

**Как работает функция**:
- Устанавливает значение `self.supplier_abs_path` в `/path/to/supplier`.
- Получает функцию `set_absolute_paths` из экземпляра класса `Supplier` и присваивает её `self.function`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
print(test_case.supplier_abs_path)  # Вывод: /path/to/supplier
print(test_case.function)  # Вывод: <bound method Supplier.set_absolute_paths of <src.suppliers.Supplier object at ...>>
```

### `test_single_filename_with_prefix_as_string`

```python
    def test_single_filename_with_prefix_as_string(self):
        prefix = \'subfolder\'
        related_filenames = \'file.txt\'
        expected_result = Path(self.supplier_abs_path, prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан строкой, а имя файла - строкой.

**Как работает функция**:
- Устанавливает `prefix` в `'subfolder'`.
- Устанавливает `related_filenames` в `'file.txt'`.
- Формирует ожидаемый результат `expected_result` с использованием `Path`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_single_filename_with_prefix_as_string()
```

### `test_single_filename_with_prefix_as_list`

```python
    def test_single_filename_with_prefix_as_list(self):
        prefix = [\'subfolder\', \'subsubfolder\']
        related_filenames = \'file.txt\'
        expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан списком, а имя файла - строкой.

**Как работает функция**:
- Устанавливает `prefix` в `['subfolder', 'subsubfolder']`.
- Устанавливает `related_filenames` в `'file.txt'`.
- Формирует ожидаемый результат `expected_result` с использованием `Path` и распаковки списка `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_single_filename_with_prefix_as_list()
```

### `test_multiple_filenames_with_prefix_as_string`

```python
    def test_multiple_filenames_with_prefix_as_string(self):
        prefix = \'subfolder\'
        related_filenames = [\'file1.txt\', \'file2.txt\', \'file3.txt\']
        expected_result = [\n            Path(self.supplier_abs_path, prefix, filename)\n            for filename in related_filenames\n        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан строкой, а имена файлов - списком.

**Как работает функция**:
- Устанавливает `prefix` в `'subfolder'`.
- Устанавливает `related_filenames` в `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` с использованием генератора списков и `Path`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_multiple_filenames_with_prefix_as_string()
```

### `test_multiple_filenames_with_prefix_as_list`

```python
    def test_multiple_filenames_with_prefix_as_list(self):
        prefix = [\'subfolder\', \'subsubfolder\']
        related_filenames = [\'file1.txt\', \'file2.txt\', \'file3.txt\']
        expected_result = [\n            Path(self.supplier_abs_path, *prefix, filename)\n            for filename in related_filenames\n        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан списком, а имена файлов - списком.

**Как работает функция**:
- Устанавливает `prefix` в `['subfolder', 'subsubfolder']`.
- Устанавливает `related_filenames` в `['file1.txt', 'file2.txt', 'file3.txt']`.
- Формирует ожидаемый результат `expected_result` с использованием генератора списков, `Path` и распаковки списка `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_multiple_filenames_with_prefix_as_list()
```

### `test_no_related_filenames_with_prefix_as_string`

```python
    def test_no_related_filenames_with_prefix_as_string(self):
        prefix = \'subfolder\'
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан строкой, а имена файлов отсутствуют.

**Как работает функция**:
- Устанавливает `prefix` в `'subfolder'`.
- Устанавливает `related_filenames` в `None`.
- Формирует ожидаемый результат `expected_result` с использованием `Path`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_no_related_filenames_with_prefix_as_string()
```

### `test_no_related_filenames_with_prefix_as_list`

```python
    def test_no_related_filenames_with_prefix_as_list(self):
        prefix = [\'subfolder\', \'subsubfolder\']
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, *prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)
```

**Назначение**: Тестирует случай, когда префикс задан списком, а имена файлов отсутствуют.

**Как работает функция**:
- Устанавливает `prefix` в `['subfolder', 'subsubfolder']`.
- Устанавливает `related_filenames` в `None`.
- Формирует ожидаемый результат `expected_result` с использованием `Path` и распаковки списка `prefix`.
- Вызывает тестируемую функцию `self.function` с параметрами `prefix` и `related_filenames`.
- Проверяет, что полученный результат `result` соответствует ожидаемому результату `expected_result` с использованием `self.assertEqual`.

**Примеры**:
```python
test_case = TestSetAbsolutePaths()
test_case.setUp()
test_case.test_no_related_filenames_with_prefix_as_list()
```