# src.suppliers.aliexpress.campaign._pytest.test_ali_campaign_editor_jupyter_widgets.py

## Обзор

Файл содержит набор тестов для функций, работающих с файловой системой, таких как сохранение, чтение файлов, получение имен файлов и директорий. В тестах используются `unittest.mock` для изоляции тестируемых функций и проверки их поведения.

## Подробнее

Этот файл содержит тесты, предназначенные для проверки корректности работы функций, находящихся в модуле `src.utils.file.file`. Для изоляции тестов от реальной файловой системы используются моки из библиотеки `unittest.mock`. Это позволяет убедиться, что функции правильно взаимодействуют с файловой системой, не затрагивая реальные файлы и директории.

## Классы

В этом файле нет классов.

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

**Назначение**: Тестирует функцию `save_text_file` из модуля `src.utils.file.file`. Функция проверяет, что при вызове `save_text_file` с определенными аргументами правильно вызываются методы мок-объектов, имитирующих файловую систему.

**Параметры**:
- `mock_logger` (MagicMock): Мок-объект для логгера.
- `mock_mkdir` (MagicMock): Мок-объект для создания директории.
- `mock_file_open` (MagicMock): Мок-объект для открытия файла.

**Возвращает**:
- `None`

**Как работает функция**:
1. Вызывается функция `save_text_file` с именем файла `"test.txt"` и текстом `"This is a test."`.
2. Проверяется, что метод `open` мок-объекта `mock_file_open` был вызван один раз с аргументами `"w"` и `encoding="utf-8"`.
3. Проверяется, что метод `write` мок-объекта, возвращенного при вызове `mock_file_open()`, был вызван один раз с аргументом `"This is a test."`.
4. Проверяется, что метод `mkdir` мок-объекта `mock_mkdir` был вызван один раз.

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

**Назначение**: Тестирует функцию `read_text_file` из модуля `src.utils.file.file`. Функция проверяет, что при вызове `read_text_file` возвращается ожидаемый контент и правильно вызываются методы мок-объекта, имитирующего файловую систему.

**Параметры**:
- `mock_file_open` (MagicMock): Мок-объект для открытия файла.

**Возвращает**:
- `None`

**Как работает функция**:
1. Вызывается функция `read_text_file` с именем файла `"test.txt"`.
2. Проверяется, что возвращаемое значение равно `"This is a test."`.
3. Проверяется, что метод `open` мок-объекта `mock_file_open` был вызван один раз с аргументами `"r"` и `encoding="utf-8"`.

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

**Назначение**: Тестирует функцию `get_filenames` из модуля `src.utils.file.file`. Функция проверяет, что при вызове `get_filenames` возвращается ожидаемый список имен файлов.

**Возвращает**:
- `None`

**Как работает функция**:
1. Используется `patch` для замены метода `iterdir` класса `Path` мок-объектом.
2. Мок-объект `iterdir` возвращает список объектов `Path`, представляющих файлы `"file1.txt"` и `"file2.txt"`.
3. Вызывается функция `get_filenames` с путем `Path("/some/dir")`.
4. Проверяется, что возвращаемое значение равно `["file1.txt", "file2.txt"]`.

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

**Назначение**: Тестирует функцию `get_directory_names` из модуля `src.utils.file.file`. Функция проверяет, что при вызове `get_directory_names` возвращается ожидаемый список имен директорий.

**Возвращает**:
- `None`

**Как работает функция**:
1. Используется `patch` для замены метода `iterdir` класса `Path` мок-объектом.
2. Мок-объект `iterdir` возвращает список объектов `Path`, представляющих директории `"dir1"` и `"dir2"`.
3. Вызывается функция `get_directory_names` с путем `Path("/some/dir")`.
4. Проверяется, что возвращаемое значение равно `["dir1", "dir2"]`.

**Примеры**:

```python
directories: list[str] = test_get_directory_names()
print(directories)