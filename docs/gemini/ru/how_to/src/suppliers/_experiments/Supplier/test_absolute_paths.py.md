## \file /src/suppliers/_experiments/Supplier/test_absolute_paths.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.suppliers._experiments.Supplier 
\t:platform: Windows, Unix
\t:synopsis:

"""


"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers._experiments.Supplier """


import unittest
from pathlib import Path


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

    def test_single_filename_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = 'file.txt'
        expected_result = Path(self.supplier_abs_path, *prefix, related_filenames)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)

    def test_multiple_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)

    def test_multiple_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = ['file1.txt', 'file2.txt', 'file3.txt']
        expected_result = [
            Path(self.supplier_abs_path, *prefix, filename)
            for filename in related_filenames
        ]

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)

    def test_no_related_filenames_with_prefix_as_string(self):
        prefix = 'subfolder'
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)

    def test_no_related_filenames_with_prefix_as_list(self):
        prefix = ['subfolder', 'subsubfolder']
        related_filenames = None
        expected_result = Path(self.supplier_abs_path, *prefix)

        result = self.function(prefix, related_filenames)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода содержит набор тестов для функции `set_absolute_paths` класса `Supplier`.
Функция принимает префикс (в виде строки или списка) и связанные имена файлов, и возвращает абсолютный путь к файлам, объединяя префикс с базовым путем поставщика.
Тесты охватывают различные сценарии, включая один файл, несколько файлов, префикс в виде строки или списка, а также случаи отсутствия связанных имен файлов.

Шаги выполнения
-------------------------
1. **Инициализация**: Создается класс `TestSetAbsolutePaths`, который наследуется от `unittest.TestCase`.
2. **Настройка (setUp)**: Определяется метод `setUp`, который устанавливает базовый абсолютный путь поставщика (`supplier_abs_path`) и получает функцию `set_absolute_paths` из класса `Supplier`.
3. **Тестирование одного файла с префиксом в виде строки**: Определяется метод `test_single_filename_with_prefix_as_string`, который проверяет, что функция правильно формирует абсолютный путь для одного файла, когда префикс задан в виде строки.
4. **Тестирование одного файла с префиксом в виде списка**: Определяется метод `test_single_filename_with_prefix_as_list`, который проверяет, что функция правильно формирует абсолютный путь для одного файла, когда префикс задан в виде списка.
5. **Тестирование нескольких файлов с префиксом в виде строки**: Определяется метод `test_multiple_filenames_with_prefix_as_string`, который проверяет, что функция правильно формирует список абсолютных путей для нескольких файлов, когда префикс задан в виде строки.
6. **Тестирование нескольких файлов с префиксом в виде списка**: Определяется метод `test_multiple_filenames_with_prefix_as_list`, который проверяет, что функция правильно формирует список абсолютных путей для нескольких файлов, когда префикс задан в виде списка.
7. **Тестирование отсутствия файлов с префиксом в виде строки**: Определяется метод `test_no_related_filenames_with_prefix_as_string`, который проверяет, что функция правильно формирует абсолютный путь, когда имена файлов не предоставлены, а префикс задан в виде строки.
8. **Тестирование отсутствия файлов с префиксом в виде списка**: Определяется метод `test_no_related_filenames_with_prefix_as_list`, который проверяет, что функция правильно формирует абсолютный путь, когда имена файлов не предоставлены, а префикс задан в виде списка.
9. **Запуск тестов**: Блок `if __name__ == '__main__'` запускает тесты при запуске скрипта.

Пример использования
-------------------------

```python
import unittest
from pathlib import Path

class Supplier:
    def set_absolute_paths(self, prefix, related_filenames):
        supplier_abs_path = '/path/to/supplier'
        if related_filenames is None:
            if isinstance(prefix, str):
                return Path(supplier_abs_path, prefix)
            else:
                return Path(supplier_abs_path, *prefix)
        if isinstance(related_filenames, str):
            related_filenames = [related_filenames]
        if isinstance(prefix, str):
            return [Path(supplier_abs_path, prefix, filename) for filename in related_filenames]
        else:
            return [Path(supplier_abs_path, *prefix, filename) for filename in related_filenames]

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

if __name__ == '__main__':
    unittest.main()