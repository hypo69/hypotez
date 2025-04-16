### Анализ кода `hypotez/src/utils/ftp.py.md`

## Обзор

Модуль предоставляет интерфейс для взаимодействия с FTP-серверами, позволяющий отправлять, получать и удалять файлы с FTP-сервера.

## Подробнее

Этот модуль содержит набор функций для выполнения основных операций с FTP-сервером, таких как загрузка файлов на сервер, скачивание файлов с сервера и удаление файлов с сервера. Он использует библиотеку `ftplib` для установления соединения и выполнения команд FTP.

## Функции

### `write`

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

**Назначение**:
Отправляет файл на FTP-сервер.

**Параметры**:

*   `source_file_path` (str): Путь к файлу, который нужно отправить.
*   `dest_dir` (str): Целевая директория на FTP-сервере.
*   `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

*   `bool`: `True`, если файл успешно отправлен, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из глобальной переменной `_connection`.
2.  Переходит в указанную директорию на FTP-сервере (`dest_dir`).
3.  Открывает файл для чтения в бинарном режиме (`'rb'`).
4.  Отправляет файл на FTP-сервер, используя команду `STOR`.
5.  Закрывает FTP-сессию в блоке `finally`, чтобы гарантировать закрытие соединения даже в случае ошибки.
6.  Логирует ошибки с использованием модуля `src.logger.logger`.

### `read`

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

**Назначение**:
Получает файл с FTP-сервера.

**Параметры**:

*   `source_file_path` (str): Путь, где файл будет сохранен локально.
*   `dest_dir` (str): Директория на FTP-сервере, где расположен файл.
*   `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

*   `Union[str, bytes, None]`: Содержимое файла в случае успешного получения, `None` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из глобальной переменной `_connection`.
2.  Переходит в указанную директорию на FTP-сервере (`dest_dir`).
3.  Открывает файл для записи в бинарном режиме (`'wb'`).
4.  Получает файл с FTP-сервера, используя команду `RETR`.
5.  Открывает скачанный файл для чтения в бинарном режиме (`'rb'`).
6.  Возвращает содержимое файла.
7.  Закрывает FTP-сессию в блоке `finally`, чтобы гарантировать закрытие соединения даже в случае ошибки.
8.  Логирует ошибки с использованием модуля `src.logger.logger`.

### `delete`

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

**Назначение**:
Удаляет файл с FTP-сервера.

**Параметры**:

*   `source_file_path` (str): Путь, где файл расположен локально (не используется).
*   `dest_dir` (str): Директория на FTP-сервере, где расположен файл.
*   `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

*   `bool`: `True`, если файл успешно удален, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из глобальной переменной `_connection`.
2.  Переходит в указанную директорию на FTP-сервере (`dest_dir`).
3.  Удаляет файл с FTP-сервера, используя команду `DELE`.
4.  Возвращает `True` в случае успеха, `False` в случае ошибки.
5.  Закрывает FTP-сессию в блоке `finally`, чтобы гарантировать закрытие соединения даже в случае ошибки.
6.  Логирует ошибки с использованием модуля `src.logger.logger`.

## Переменные

### `_connection`

**Назначение**:
Конфигурация подключения к FTP-серверу.

**Значение**:
Словарь, содержащий параметры подключения к FTP-серверу:
* `'server'`: Адрес FTP-сервера.
* `'port'`: Порт FTP-сервера.
* `'user'`: Имя пользователя для подключения.
* `'password'`: Пароль для подключения.

## Примеры использования

```python
from src.utils import ftp

# Отправка файла на FTP-сервер
success = ftp.write('local_file.txt', '/remote/directory', 'remote_file.txt')
if success:
    print("Файл успешно отправлен")
else:
    print("Ошибка при отправке файла")

# Получение файла с FTP-сервера
content = ftp.read('local_file.txt', '/remote/directory', 'remote_file.txt')
if content:
    print("Файл успешно получен")
else:
    print("Ошибка при получении файла")

# Удаление файла с FTP-сервера
success = ftp.delete('local_file.txt', '/remote/directory', 'remote_file.txt')
if success:
    print("Файл успешно удален")
else:
    print("Ошибка при удалении файла")
```

## Зависимости

*   `ftplib`: Для работы с FTP-сервером.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Union`:  Для объявления, что переменная может принимать один из нескольких типов.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

Модуль `ftp.py` предоставляет функциональность для работы с FTP-серверами, которая может использоваться в других частях проекта `hypotez`, где требуется автоматическая загрузка или выгрузка файлов на FTP-сервер.