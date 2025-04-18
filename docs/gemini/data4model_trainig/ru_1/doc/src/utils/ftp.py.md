# Модуль для работы с FTP-сервером

## Обзор

Модуль `src.utils.ftp` предоставляет интерфейс для взаимодействия с FTP-серверами. Он включает функции для отправки, получения и удаления файлов с FTP-сервера.

## Подробней

Этот модуль позволяет отправлять медиафайлы (изображения, видео), электронные таблицы и другие файлы на FTP-сервер и с него. Он использует библиотеку `ftplib` для обеспечения FTP-соединения и `pathlib` для работы с путями к файлам.

## Содержание

- [Классы](#Классы)
- [Функции](#Функции)
    - [write](#write)
    - [read](#read)
    - [delete](#delete)

## Классы

В данном модуле классы отсутствуют.

## Функции

### `write`

**Назначение**: Отправляет файл на FTP-сервер.

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

- `source_file_path` (str): Путь к файлу, который необходимо отправить.
- `dest_dir` (str): Каталог назначения на FTP-сервере.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

- `bool`: `True`, если файл успешно отправлен, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанный каталог `dest_dir` на FTP-сервере.
3.  Открывает файл, расположенный по пути `source_file_path`, в бинарном режиме для чтения.
4.  Отправляет файл на FTP-сервер с именем `dest_file_name` с использованием команды `STOR`.
5.  Закрывает FTP-сессию.
6.  Логирует ошибки в случае возникновения исключений и возвращает `False`.

**Примеры**:

```python
success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(success)
```

### `read`

**Назначение**: Получает файл с FTP-сервера.

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

-   `source_file_path` (str): Путь, по которому файл будет сохранен локально.
-   `dest_dir` (str): Каталог на FTP-сервере, где расположен файл.
-   `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

-   `Union[str, bytes, None]`: Содержимое файла, если он успешно получен, `None` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанный каталог `dest_dir` на FTP-сервере.
3.  Создает и открывает файл, расположенный по пути `source_file_path`, в бинарном режиме для записи.
4.  Получает файл с FTP-сервера с именем `dest_file_name` с использованием команды `RETR` и записывает его в локальный файл.
5.  Открывает локальный файл в бинарном режиме для чтения и возвращает его содержимое.
6.  Закрывает FTP-сессию.
7.  Логирует ошибки в случае возникновения исключений и возвращает `None`.

**Примеры**:

```python
content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(content)
```

### `delete`

**Назначение**: Удаляет файл с FTP-сервера.

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

-   `source_file_path` (str): Путь, по которому файл расположен локально (не используется).
-   `dest_dir` (str): Каталог на FTP-сервере, где расположен файл.
-   `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:

-   `bool`: `True`, если файл успешно удален, `False` в противном случае.

**Как работает функция**:

1.  Устанавливает соединение с FTP-сервером, используя параметры из словаря `_connection`.
2.  Переходит в указанный каталог `dest_dir` на FTP-сервере.
3.  Удаляет файл с FTP-сервера с именем `dest_file_name` с использованием команды `DELE`.
4.  Закрывает FTP-сессию.
5.  Логирует ошибки в случае возникновения исключений и возвращает `False`.

**Примеры**:

```python
success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(success)