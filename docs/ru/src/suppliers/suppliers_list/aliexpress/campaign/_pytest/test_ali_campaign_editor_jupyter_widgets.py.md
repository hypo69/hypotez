# Модуль `test_ali_campaign_editor_jupyter_widgets.py`

## Обзор

Модуль содержит набор тестов для функций, связанных с файловой системой, таких как сохранение, чтение, получение имен файлов и директорий. Модуль использует `unittest.mock` для имитации операций файловой системы и логирования, что позволяет изолированно тестировать функции.

## Подробнее

Модуль предназначен для тестирования функций файлового модуля, расположенного по пути `src.utils.file.file`. В частности, тестируются функции:

- `save_text_file`: сохраняет текст в файл.
- `read_text_file`: читает текст из файла.
- `get_filenames`: получает список имен файлов из указанной директории.
- `get_directory_names`: получает список имен директорий из указанного пути.

## Классы

В данном модуле нет классов.

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

**Назначение**: Тестирует функцию `save_text_file` из модуля `src.utils.file.file`.

**Параметры**:

- `mock_logger` (`MagicMock`): Имитированный экземпляр логгера.
- `mock_mkdir` (`MagicMock`): Имитированная функция создания директории.
- `mock_file_open` (`MagicMock`): Имитированная функция открытия файла.

**Возвращает**: None

**Как работает функция**:

- Функция использует декоратор `@patch` для замены реальных функций `Path.open`, `Path.mkdir` и `logger` имитированными объектами (`MagicMock`).
- Вызывается функция `save_text_file` с именем файла "test.txt" и текстом "This is a test.".
- Проверяется, что функция `mock_file_open` была вызвана с правильными аргументами ("w" - режим записи, encoding="utf-8").
- Проверяется, что метод `write` имитированного файлового объекта был вызван с правильным текстом ("This is a test.").
- Проверяется, что функция `mock_mkdir` была вызвана один раз.

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

**Назначение**: Тестирует функцию `read_text_file` из модуля `src.utils.file.file`.

**Параметры**:

- `mock_file_open` (`MagicMock`): Имитированная функция открытия файла.

**Возвращает**: None

**Как работает функция**:

- Функция использует декоратор `@patch` для замены реальной функции `Path.open` имитированным объектом (`MagicMock`).
- Имитируется открытие файла с текстом "This is a test.".
- Вызывается функция `read_text_file` с именем файла "test.txt".
- Проверяется, что возвращаемое значение функции `read_text_file` равно "This is a test.".
- Проверяется, что функция `mock_file_open` была вызвана с правильными аргументами ("r" - режим чтения, encoding="utf-8").

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

**Назначение**: Тестирует функцию `get_filenames` из модуля `src.utils.file.file`.

**Параметры**: None

**Возвращает**: None

**Как работает функция**:

- Функция использует `patch` для имитации метода `Path.iterdir`, который возвращает список объектов `Path`, представляющих файлы "file1.txt" и "file2.txt".
- Вызывается функция `get_filenames` с путем "/some/dir".
- Проверяется, что возвращаемое значение функции `get_filenames` равно `["file1.txt", "file2.txt"]`.

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

**Назначение**: Тестирует функцию `get_directory_names` из модуля `src.utils.file.file`.

**Параметры**: None

**Возвращает**: None

**Как работает функция**:

- Функция использует `patch` для имитации метода `Path.iterdir`, который возвращает список объектов `Path`, представляющих директории "dir1" и "dir2".
- Вызывается функция `get_directory_names` с путем "/some/dir".
- Проверяется, что возвращаемое значение функции `get_directory_names` равно `["dir1", "dir2"]`.

**Примеры**:

```python
directories: list[str] = test_get_directory_names()
print(directories)