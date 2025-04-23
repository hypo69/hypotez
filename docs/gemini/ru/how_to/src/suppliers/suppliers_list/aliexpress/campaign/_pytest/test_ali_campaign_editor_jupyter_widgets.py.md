### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код содержит набор тестов для модуля `src.utils.file.file`, который предоставляет функции для работы с файлами и директориями. В частности, тестируются функции `save_text_file`, `read_text_file`, `get_filenames` и `get_directory_names`. Для изоляции тестов от реальной файловой системы используются `unittest.mock` и `patch`.

Шаги выполнения
-------------------------
1. **`test_save_text_file`**:
   - Мокирует `Path.open`, `Path.mkdir` и `logger` из модуля `src.utils.file.file`.
   - Вызывает функцию `save_text_file` с именем файла "test.txt" и содержимым "This is a test.".
   - Проверяет, что `mock_file_open` был вызван с правильными аргументами ("w" и кодировкой "utf-8").
   - Проверяет, что метод `write` мокированного файла был вызван с правильным содержимым ("This is a test.").
   - Проверяет, что `mock_mkdir` был вызван один раз.

2. **`test_read_text_file`**:
   - Мокирует `Path.open` из модуля `src.utils.file.file`, устанавливая возвращаемое значение `read_data` равным "This is a test.".
   - Вызывает функцию `read_text_file` с именем файла "test.txt".
   - Проверяет, что возвращаемое значение функции `read_text_file` равно "This is a test.".
   - Проверяет, что `mock_file_open` был вызван с правильными аргументами ("r" и кодировкой "utf-8").

3. **`test_get_filenames`**:
   - Мокирует `Path.iterdir`, чтобы возвращать список объектов `Path`, представляющих файлы "file1.txt" и "file2.txt".
   - Вызывает функцию `get_filenames` с путем "/some/dir".
   - Проверяет, что возвращаемое значение функции `get_filenames` равно `["file1.txt", "file2.txt"]`.

4. **`test_get_directory_names`**:
   - Мокирует `Path.iterdir`, чтобы возвращать список объектов `Path`, представляющих директории "dir1" и "dir2".
   - Вызывает функцию `get_directory_names` с путем "/some/dir".
   - Проверяет, что возвращаемое значение функции `get_directory_names` равно `["dir1", "dir2"]`.

Пример использования
-------------------------

```python
import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from src.utils.file.file import (
    save_text_file,
    read_text_file,
    get_filenames,
    get_directory_names,
)

# Пример использования test_save_text_file
@patch("src.utils.file.file.Path.open", new_callable=mock_open)
@patch("src.utils.file.file.Path.mkdir")
@patch("src.utils.file.file.logger")
def test_save_text_file_example(mock_logger, mock_mkdir, mock_file_open):
    """Test saving text to a file."""
    save_text_file("example.txt", "This is an example.")
    mock_file_open.assert_called_once_with("w", encoding="utf-8")
    mock_file_open().write.assert_called_once_with("This is an example.")
    mock_mkdir.assert_called_once()

# Пример использования test_read_text_file
@patch(
    "src.utils.file.file.Path.open", new_callable=mock_open, read_data="This is an example."
)
def test_read_text_file_example(mock_file_open):
    """Test reading text from a file."""
    content = read_text_file("example.txt")
    assert content == "This is an example."
    mock_file_open.assert_called_once_with("r", encoding="utf-8")

# Пример использования test_get_filenames
def test_get_filenames_example():
    """Test getting filenames from a directory."""
    with patch(
        "src.utils.file.file.Path.iterdir",
        return_value=[Path(f"file{i}.txt") for i in range(1, 3)],
    ):
        filenames = get_filenames(Path("/example/dir"))
        assert filenames == ["file1.txt", "file2.txt"]

# Пример использования test_get_directory_names
def test_get_directory_names_example():
    """Test getting directory names from a path."""
    with patch(
        "src.utils.file.file.Path.iterdir",
        return_value=[Path(f"dir{i}") for i in range(1, 3)],
    ):
        directories = get_directory_names(Path("/example/dir"))
        assert directories == ["dir1", "dir2"]