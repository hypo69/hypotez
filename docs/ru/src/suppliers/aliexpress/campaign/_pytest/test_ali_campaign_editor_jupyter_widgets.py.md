# Модуль `test_ali_campaign_editor_jupyter_widgets.py`

## Обзор

Модуль содержит набор тестов для функций, связанных с файловой системой, таких как сохранение текста в файл, чтение текста из файла, получение списка имен файлов и получение списка имен директорий. Модуль использует библиотеку `unittest.mock` для имитации файловых операций и логирования, что позволяет изолированно тестировать функции.

## Подробней

Этот модуль содержит тесты для функций, которые обрабатывают файловые операции. Он использует `unittest.mock` для имитации файловых операций и логирования. Это позволяет изолированно тестировать функции, не затрагивая реальную файловую систему.

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
    save_text_file("test.txt", "This is a test.")
    mock_file_open.assert_called_once_with("w", encoding="utf-8")
    mock_file_open().write.assert_called_once_with("This is a test.")
    mock_mkdir.assert_called_once()
```

**Назначение**: Тестирование функции сохранения текста в файл.

**Параметры**:
- `mock_logger` (MagicMock): Имитированный экземпляр логгера.
- `mock_mkdir` (MagicMock): Имитированная функция создания директории.
- `mock_file_open` (MagicMock): Имитированная функция открытия файла.

**Как работает функция**:
- Вызывает функцию `save_text_file` с имитированными объектами и проверяет, что методы `open`, `write` и `mkdir` вызываются с ожидаемыми аргументами.
- `mock_file_open.assert_called_once_with("w", encoding="utf-8")`: Проверяет, что метод `open` был вызван один раз с параметрами `"w"` (режим записи) и `encoding="utf-8"`.
- `mock_file_open().write.assert_called_once_with("This is a test.")`: Проверяет, что метод `write` был вызван один раз с текстом `"This is a test."`.
- `mock_mkdir.assert_called_once()`: Проверяет, что метод `mkdir` был вызван один раз.

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
    content = read_text_file("test.txt")
    assert content == "This is a test."
    mock_file_open.assert_called_once_with("r", encoding="utf-8")
```

**Назначение**: Тестирование функции чтения текста из файла.

**Параметры**:
- `mock_file_open` (MagicMock): Имитированная функция открытия файла.

**Как работает функция**:
- Вызывает функцию `read_text_file` с имитированным объектом и проверяет, что метод `open` вызывается с ожидаемыми аргументами и что возвращаемое значение соответствует ожидаемому тексту.
- `content = read_text_file("test.txt")`: Вызывает функцию `read_text_file` с именем файла `"test.txt"`.
- `assert content == "This is a test."`: Проверяет, что возвращенное значение функции равно `"This is a test."`.
- `mock_file_open.assert_called_once_with("r", encoding="utf-8")`: Проверяет, что метод `open` был вызван один раз с параметрами `"r"` (режим чтения) и `encoding="utf-8"`.

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
    with patch(
        "src.utils.file.file.Path.iterdir",
        return_value=[Path(f"file{i}.txt") for i in range(1, 3)],
    ):
        filenames = get_filenames(Path("/some/dir"))
        assert filenames == ["file1.txt", "file2.txt"]
```

**Назначение**: Тестирование функции получения списка имен файлов из директории.

**Как работает функция**:
- Имитирует метод `iterdir` класса `Path` и проверяет, что возвращаемый список имен файлов соответствует ожидаемому.
- `with patch(...)`: Имитирует метод `iterdir` класса `Path` с возвращаемым значением, представляющим собой список объектов `Path`.
- `filenames = get_filenames(Path("/some/dir"))`: Вызывает функцию `get_filenames` с указанием пути к директории.
- `assert filenames == ["file1.txt", "file2.txt"]`: Проверяет, что возвращенный список имен файлов соответствует ожидаемому.

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
    with patch(
        "src.utils.file.file.Path.iterdir",
        return_value=[Path(f"dir{i}") for i in range(1, 3)],
    ):
        directories = get_directory_names(Path("/some/dir"))
        assert directories == ["dir1", "dir2"]
```

**Назначение**: Тестирование функции получения списка имен директорий из указанного пути.

**Как работает функция**:
- Имитирует метод `iterdir` класса `Path` и проверяет, что возвращаемый список имен директорий соответствует ожидаемому.
- `with patch(...)`: Имитирует метод `iterdir` класса `Path` с возвращаемым значением, представляющим собой список объектов `Path`.
- `directories = get_directory_names(Path("/some/dir"))`: Вызывает функцию `get_directory_names` с указанием пути к директории.
- `assert directories == ["dir1", "dir2"]`: Проверяет, что возвращенный список имен директорий соответствует ожидаемому.

**Примеры**:

```python
directories: list[str] = test_get_directory_names()
print(directories)