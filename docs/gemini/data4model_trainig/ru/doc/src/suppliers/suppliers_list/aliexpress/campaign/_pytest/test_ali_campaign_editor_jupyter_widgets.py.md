# Модуль тестирования виджетов редактора кампаний AliExpress в Jupyter

## Обзор

Модуль содержит тесты для функций, связанных с файловой системой, таких как сохранение, чтение и получение имен файлов и директорий. Используются mock-объекты для изоляции тестов от реальной файловой системы.

## Подробнее

Модуль использует библиотеку `unittest.mock` для замены реальных объектов файловой системы mock-объектами. Это позволяет тестировать логику работы с файлами без необходимости создания и изменения файлов на диске.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `test_save_text_file`

```python
def test_save_text_file(mock_logger, mock_mkdir, mock_file_open):
    """Test saving text to a file.

    Args:
        mock_logger (MagicMock): Mocked logger instance.
        mock_mkdir (MagicMock): Mocked mkdir instance.
        mock_file_open (MagicMock): Mocked file open instance.

    Example:
        >>> test_save_text_file()
    """
```

**Назначение**: Тестирует функцию сохранения текста в файл.

**Параметры**:

-   `mock_logger` (MagicMock): Mock-объект для логирования.
-   `mock_mkdir` (MagicMock): Mock-объект для создания директорий.
-   `mock_file_open` (MagicMock): Mock-объект для открытия файла.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Вызывает функцию `save_text_file` с фиктивными данными имени файла и содержимого.
2.  Проверяет, что метод `open` mock-объекта `mock_file_open` был вызван с правильными аргументами (`"w"` для записи и кодировкой `"utf-8"`).
3.  Проверяет, что метод `write` mock-объекта `mock_file_open` был вызван с правильным содержимым (`"This is a test."`).
4.  Проверяет, что метод `mkdir` mock-объекта `mock_mkdir` был вызван.

**Примеры**:

```python
test_save_text_file()
```

### `test_read_text_file`

```python
def test_read_text_file(mock_file_open):
    """Test reading text from a file.

    Args:
        mock_file_open (MagicMock): Mocked file open instance.

    Returns:
        None

    Example:
        >>> content: str = test_read_text_file()
        >>> print(content)
        'This is a test.'
    """
```

**Назначение**: Тестирует функцию чтения текста из файла.

**Параметры**:

-   `mock_file_open` (MagicMock): Mock-объект для открытия файла.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Вызывает функцию `read_text_file` с фиктивным именем файла.
2.  Проверяет, что метод `open` mock-объекта `mock_file_open` был вызван с правильными аргументами (`"r"` для чтения и кодировкой `"utf-8"`).
3.  Проверяет, что возвращаемое значение функции `read_text_file` соответствует ожидаемому содержимому (`"This is a test."`).

**Примеры**:

```python
content: str = test_read_text_file()
print(content)
```

### `test_get_filenames`

```python
def test_get_filenames():
    """Test getting filenames from a directory.

    Returns:
        None

    Example:
        >>> filenames: list[str] = test_get_filenames()
        >>> print(filenames)
        ['file1.txt', 'file2.txt']
    """
```

**Назначение**: Тестирует функцию получения списка имен файлов из директории.

**Параметры**:

-   Нет.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Использует `patch` для замены метода `iterdir` класса `Path` mock-объектом, возвращающим список фиктивных объектов `Path`.
2.  Вызывает функцию `get_filenames` с фиктивным путем к директории.
3.  Проверяет, что возвращаемое значение функции `get_filenames` соответствует ожидаемому списку имен файлов (`["file1.txt", "file2.txt"]`).

**Примеры**:

```python
filenames: list[str] = test_get_filenames()
print(filenames)
```

### `test_get_directory_names`

```python
def test_get_directory_names():
    """Test getting directory names from a path.

    Returns:
        None

    Example:
        >>> directories: list[str] = test_get_directory_names()
        >>> print(directories)
        ['dir1', 'dir2']
    """
```

**Назначение**: Тестирует функцию получения списка имен директорий из пути.

**Параметры**:

-   Нет.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Использует `patch` для замены метода `iterdir` класса `Path` mock-объектом, возвращающим список фиктивных объектов `Path`.
2.  Вызывает функцию `get_directory_names` с фиктивным путем к директории.
3.  Проверяет, что возвращаемое значение функции `get_directory_names` соответствует ожидаемому списку имен директорий (`["dir1", "dir2"]`).

**Примеры**:

```python
directories: list[str] = test_get_directory_names()
print(directories)