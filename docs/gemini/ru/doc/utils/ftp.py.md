# Модуль для работы с FTP серверами (ftp.py)

## Обзор

Этот модуль предоставляет интерфейс для взаимодействия с FTP серверами. Он включает функции для отправки, получения и удаления файлов с FTP сервера.

## Подробней

Модуль позволяет автоматизировать операции с FTP серверами, такие как загрузка медиафайлов, электронных таблиц и других файлов. Он использует библиотеку `ftplib` для установления соединения с FTP сервером и выполнения операций с файлами. Модуль обеспечивает логирование ошибок с использованием модуля `src.logger.logger`.

## Функции

### `write`

**Назначение**: Отправляет файл на FTP сервер.

```python
def write(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool:
    """
    Sends a file to an FTP server.

    Args:
        source_file_path (str): The path of the file to be sent.
        dest_dir (str): The destination directory on the FTP server.
        dest_file_name (str): The name of the file on the FTP server.

    Returns:
        bool: True if the file is successfully sent, False otherwise.

    Example:
        >>> success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    ...
```

**Параметры**:

-   `source_file_path` (str): Путь к файлу, который нужно отправить.
-   `dest_dir` (str): Целевая директория на FTP сервере.
-   `dest_file_name` (str): Имя файла на FTP сервере.

**Возвращает**:

-   `bool`: `True`, если файл успешно отправлен, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанную директорию на FTP сервере (`dest_dir`).
3.  Открывает файл для чтения в бинарном режиме (`'rb'`).
4.  Отправляет файл на FTP сервер, используя команду `STOR`.
5.  Закрывает соединение с FTP сервером.
6.  Логирует информацию об ошибках, используя `logger.error`.

### `read`

**Назначение**: Получает файл с FTP сервера.

```python
def read(source_file_path: str, dest_dir: str, dest_file_name: str) -> Union[str, bytes, None]:
    """
    Retrieves a file from an FTP server.

    Args:
        source_file_path (str): The path where the file will be saved locally.
        dest_dir (str): The directory on the FTP server where the file is located.
        dest_file_name (str): The name of the file on the FTP server.

    Returns:
        Union[str, bytes, None]: The file content if successfully retrieved, None otherwise.

    Example:
        >>> content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(content)
        b'Some file content'
    """
    ...
```

**Параметры**:

-   `source_file_path` (str): Путь, куда будет сохранен скачанный файл.
-   `dest_dir` (str): Директория на FTP сервере, где находится файл.
-   `dest_file_name` (str): Имя файла на FTP сервере.

**Возвращает**:

-   `Union[str, bytes, None]`: Содержимое файла, если скачивание прошло успешно, `None` - в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанную директорию на FTP сервере (`dest_dir`).
3.  Получает файл с FTP сервера, используя команду `RETR`.
4.  Открывает скачанный файл для чтения в бинарном режиме (`'rb'`) и возвращает его содержимое.
5.  Закрывает соединение с FTP сервером.
6.  Логирует информацию об ошибках, используя `logger.error`.

### `delete`

**Назначение**: Удаляет файл с FTP сервера.

```python
def delete(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool:
    """
    Deletes a file from an FTP server.

    Args:
        source_file_path (str): The path where the file is located locally (not used).
        dest_dir (str): The directory on the FTP server where the file is located.
        dest_file_name (str): The name of the file on the FTP server.

    Returns:
        bool: True if the file is successfully deleted, False otherwise.

    Example:
        >>> success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    ...
```

**Параметры**:

-   `source_file_path` (str): Путь, где файл расположен локально (не используется).
-   `dest_dir` (str): Директория на FTP сервере, где находится файл.
-   `dest_file_name` (str): Имя файла на FTP сервере.

**Возвращает**:

-   `bool`: `True`, если файл успешно удален, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанную директорию на FTP сервере (`dest_dir`).
3.  Удаляет файл с FTP сервера, используя команду `DELE`.
4.  Закрывает соединение с FTP сервером.
5.  Логирует информацию об ошибках, используя `logger.error`.

## Переменные модуля

-   `_connection` (dict): Словарь, содержащий параметры подключения к FTP серверу. Этот словарь должен быть определен в другом месте и содержать ключи `'server'`, `'port'`, `'user'` и `'password'`.

## Пример использования

**Сохранение файла на FTP сервер:**

```python
from src.utils import ftp
success = ftp.write('local_file.txt', '/remote/directory', 'remote_file.txt')
if success:
    print("Файл успешно отправлен на FTP сервер.")
else:
    print("Не удалось отправить файл на FTP сервер.")
```

**Чтение файла с FTP сервера:**

```python
from src.utils import ftp
content = ftp.read('local_copy.txt', '/remote/directory', 'remote_file.txt')
if content:
    print(f"Содержимое файла: {content}")
else:
    print("Не удалось скачать файл с FTP сервера.")
```

**Удаление файла с FTP сервера:**

```python
from src.utils import ftp
success = ftp.delete('local_file.txt', '/remote/directory', 'remote_file.txt')
if success:
    print("Файл успешно удален с FTP сервера.")
else:
    print("Не удалось удалить файл с FTP сервера.")
```

## Зависимости

-   `ftplib`: Для работы с FTP серверами.
-   `pathlib.Path`: Для работы с путями к файлам.
-   `typing.Union`: Для указания типов данных.
-   `src.logger.logger`: Для логирования информации об ошибках.

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.ftp` используется другими модулями проекта для взаимодействия с FTP серверами.
-   Для логирования ошибок используется модуль `src.logger.logger`.