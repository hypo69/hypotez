# Модуль для работы с FTP-сервером
======================================

Модуль `src.utils.ftp` предоставляет интерфейс для взаимодействия с FTP-серверами. Он включает функции для отправки, получения и удаления файлов с FTP-сервера.

**Назначение**:

Позволяет отправлять медиафайлы (изображения, видео), электронные таблицы и другие файлы на FTP-сервер и обратно.

**Модули**:

- helpers (локальный): Локальные вспомогательные утилиты для операций FTP.
- typing: Подсказки типов для параметров функций и возвращаемых значений.
- ftplib: Предоставляет возможности FTP протокола клиента.
- pathlib: Для работы с путями файловой системы.

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Функции](#функции)
    - [write](#write)
    - [read](#read)
    - [delete](#delete)

## Обзор

Модуль `ftp.py` предоставляет набор функций для работы с FTP-сервером, включая отправку, получение и удаление файлов. Он использует библиотеку `ftplib` для установления соединения и выполнения операций с FTP-сервером.

## Подробнее

Модуль предназначен для упрощения взаимодействия с FTP-серверами, предоставляя удобный интерфейс для выполнения основных операций. Он включает функции для записи (отправки) файлов на сервер, чтения (получения) файлов с сервера и удаления файлов на сервере.
Конфигурация подключения к FTP-серверу хранится в словаре `_connection`.
Каждая функция модуля обрабатывает исключения и логирует ошибки с помощью модуля `logger` из `src.logger.logger`.

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
- `source_file_path` (str): Путь к файлу, который нужно отправить.
- `dest_dir` (str): Каталог назначения на FTP-сервере.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:
- `bool`: `True`, если файл успешно отправлен, `False` в противном случае.

**Как работает функция**:
1. Функция пытается установить соединение с FTP-сервером, используя данные из словаря `_connection` (сервер, пользователь, пароль).
2. После успешного подключения переходит в указанный каталог `dest_dir` на сервере.
3. Открывает файл, расположенный по пути `source_file_path`, в бинарном режиме для чтения.
4. Отправляет содержимое файла на FTP-сервер, используя команду `STOR` и имя файла `dest_file_name`.
5. В случае успеха возвращает `True`. Если в процессе возникают ошибки, функция логирует их и возвращает `False`.
6. В блоке `finally` закрывает FTP-сессию.

```ascii
Начало
  │
  │ Установить соединение с FTP-сервером
  │
  └── Успех?
      │  Да: Перейти в каталог `dest_dir`
      │  Нет: Записать ошибку в лог, вернуть `False`
      │
      │ Открыть файл `source_file_path` в бинарном режиме
      │
      └── Успех?
          │  Да: Отправить файл на FTP-сервер с именем `dest_file_name`
          │  Нет: Записать ошибку в лог, вернуть `False`
          │
          │ Закрыть FTP-сессию
          │
          └── Успех?
              │  Да: Вернуть `True`
              │  Нет: Записать ошибку в лог
              │
Конец
```

**Примеры**:
```python
success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(success)
# True
```

---

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
- `source_file_path` (str): Путь, по которому файл будет сохранен локально.
- `dest_dir` (str): Каталог на FTP-сервере, где находится файл.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:
- `Union[str, bytes, None]`: Содержимое файла, если он успешно получен, `None` в противном случае.

**Как работает функция**:
1. Функция пытается установить соединение с FTP-сервером, используя данные из словаря `_connection` (сервер, пользователь, пароль).
2. После успешного подключения переходит в указанный каталог `dest_dir` на сервере.
3. Открывает файл, расположенный по пути `source_file_path`, в бинарном режиме для записи.
4. Получает содержимое файла с FTP-сервера, используя команду `RETR` и имя файла `dest_file_name`, и записывает его в локальный файл.
5. Открывает сохраненный локальный файл в бинарном режиме для чтения и возвращает его содержимое.
6. В случае успеха возвращает содержимое файла. Если в процессе возникают ошибки, функция логирует их и возвращает `None`.
7. В блоке `finally` закрывает FTP-сессию.

```ascii
Начало
  │
  │ Установить соединение с FTP-сервером
  │
  └── Успех?
      │  Да: Перейти в каталог `dest_dir`
      │  Нет: Записать ошибку в лог, вернуть `None`
      │
      │ Открыть файл `source_file_path` в бинарном режиме для записи
      │
      │ Получить файл с FTP-сервера с именем `dest_file_name` и записать в локальный файл
      │
      │ Открыть файл `source_file_path` в бинарном режиме для чтения
      │
      │ Вернуть содержимое файла
      │
      └── Ошибка?
          │  Да: Записать ошибку в лог, вернуть `None`
          │  Нет: Продолжить
          │
          │ Закрыть FTP-сессию
          │
Конец
```

**Примеры**:
```python
content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(content)
# b'Some file content'
```

---

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
- `source_file_path` (str): Путь, по которому файл расположен локально (не используется).
- `dest_dir` (str): Каталог на FTP-сервере, где находится файл.
- `dest_file_name` (str): Имя файла на FTP-сервере.

**Возвращает**:
- `bool`: `True`, если файл успешно удален, `False` в противном случае.

**Как работает функция**:
1. Функция пытается установить соединение с FTP-сервером, используя данные из словаря `_connection` (сервер, пользователь, пароль).
2. После успешного подключения переходит в указанный каталог `dest_dir` на сервере.
3. Удаляет файл с FTP-сервера, используя команду `DELE` и имя файла `dest_file_name`.
4. В случае успеха возвращает `True`. Если в процессе возникают ошибки, функция логирует их и возвращает `False`.
5. В блоке `finally` закрывает FTP-сессию.

```ascii
Начало
  │
  │ Установить соединение с FTP-сервером
  │
  └── Успех?
      │  Да: Перейти в каталог `dest_dir`
      │  Нет: Записать ошибку в лог, вернуть `False`
      │
      │ Удалить файл с FTP-сервера с именем `dest_file_name`
      │
      └── Успех?
          │  Да: Вернуть `True`
          │  Нет: Записать ошибку в лог, вернуть `False`
          │
          │ Закрыть FTP-сессию
          │
Конец
```

**Примеры**:
```python
success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')
print(success)
# True