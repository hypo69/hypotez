### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой набор тестов для функции `buid_templates`, предназначенной для обработки шаблонов из JSON-файлов, находящихся в указанной директории. Тесты проверяют, как функция обрабатывает существующие и несуществующие директории, а также корректность извлечения данных из JSON-файлов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `unittest` для создания и запуска тестов, `tempfile` для создания временных директорий и файлов, и `os` для работы с файловой системой.
   ```python
   import unittest
   import tempfile
   import os
   ```

2. **Определение класса `TestBuildtemplates`**:
   - Создается класс `TestBuildtemplates`, наследующий от `unittest.TestCase`. Этот класс содержит методы для тестирования функции `buid_templates`.
   ```python
   class TestBuildtemplates(unittest.TestCase):
   ```

3. **Тест `test_build_templates_with_existing_directory`**:
   - Этот метод тестирует функцию `buid_templates` с существующей директорией, содержащей JSON-файлы.
   - **Создание временной директории**: Используется `tempfile.TemporaryDirectory()` для создания временной директории, которая будет автоматически удалена после завершения теста.
   ```python
   with tempfile.TemporaryDirectory() as tmpdir:
   ```
   - **Создание JSON-данных**: Определяется строка `json_data`, содержащая JSON-объект с шаблонами категорий.
   ```python
   json_data = '{"category1": {"template1": "some content"}, "category2": {"template2": "some content"}}'
   ```
   - **Создание файлов**:
     - Создается файл `file1.json` в корне временной директории и записываются JSON-данные.
     ```python
     file1_path = os.path.join(tmpdir, 'file1.json')
     with open(file1_path, 'w') as f:
         f.write(json_data)
     ```
     - Создается поддиректория `subdir` и файл `file2.json` в ней, также записываются JSON-данные.
     ```python
     file2_path = os.path.join(tmpdir, 'subdir', 'file2.json')
     os.makedirs(os.path.dirname(file2_path))
     with open(file2_path, 'w') as f:
         f.write(json_data)
     ```
   - **Вызов функции и проверка результата**:
     - Вызывается функция `buid_templates` с путем к временной директории.
     - Сравнивается возвращаемое значение функции с ожидаемым результатом `expected_output` с помощью `self.assertEqual`.
     ```python
     expected_output = {"category1": {"template1": "some content"}, "category2": {"template2": "some content"}}
     self.assertEqual(buid_templates(tmpdir), expected_output)
     ```

4. **Тест `test_build_templates_with_non_existing_directory`**:
   - Этот метод тестирует функцию `buid_templates` с несуществующей директорией.
   - **Проверка исключения**: Используется `self.assertRaises(FileNotFoundError)` для проверки того, что функция вызывает исключение `FileNotFoundError` при передаче несуществующего пути.
   ```python
   with self.assertRaises(FileNotFoundError):
       buid_templates('/non/existing/path/')
   ```

Пример использования
-------------------------

```python
import unittest
import tempfile
import os

class TestBuildtemplates(unittest.TestCase):
    def test_build_templates_with_existing_directory(self):
        # Создание временной директории и добавление JSON файлов
        with tempfile.TemporaryDirectory() as tmpdir:
            json_data = '{"category1": {"template1": "some content"}, "category2": {"template2": "some content"}}'
            file1_path = os.path.join(tmpdir, 'file1.json')
            with open(file1_path, 'w') as f:
                f.write(json_data)
            file2_path = os.path.join(tmpdir, 'subdir', 'file2.json')
            os.makedirs(os.path.dirname(file2_path))
            with open(file2_path, 'w') as f:
                f.write(json_data)

            # Вызов функции и проверка вывода
            expected_output = {"category1": {
                "template1": "some content"}, "category2": {"template2": "some content"}}
            self.assertEqual(buid_templates(tmpdir), expected_output)

    def test_build_templates_with_non_existing_directory(self):
        # Вызов функции с несуществующей директорией и проверка, что она вызывает исключение
        with self.assertRaises(FileNotFoundError):
            buid_templates('/non/existing/path/')