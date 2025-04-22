## \file /src/utils/ftp.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.utils 
\t:platform: Windows, Unix
\t:synopsis: interface for interacting with FTP servers
This module provides an interface for interacting with FTP servers. It includes functions to send, receive, and delete files from an FTP server.

** Purpose **:
Allows for sending media files (images, videos), spreadsheets, and other files to and from an FTP server. 

** Modules **:
- helpers (local): Local helper utilities for FTP operations.
- typing: Type hints for function parameters and return values.
- ftplib: Provides FTP protocol client capabilities.
- pathlib: For handling file system paths.

Functions:
    - `write`: Sends a file to an FTP server.
    - `read`: Retrieves a file from an FTP server.
    - `delete`: Deletes a file from an FTP server.
"""

from src.logger.logger import logger
from typing import Union
import ftplib
from pathlib import Path

# Connection configuration (assumed to be defined elsewhere)
_connection = {
    'server': 'ftp.example.com',
    'port': 21,
    'user': 'username',
    'password': 'password'
}

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
    try:
        # Establish connection to FTP server
        session = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)
    except Exception as ex:
        # Log error if connection to FTP server fails
        logger.error(f"Failed to connect to FTP server. Error: {ex}")
        return False

    try:
        # Open the file and send it to the FTP server
        with open(source_file_path, 'rb') as f:
            session.storbinary(f'STOR {dest_file_name}', f)
        return True
    except Exception as ex:
        # Log error if file transfer to FTP server fails
        logger.error(f"Failed to send file to FTP server. Error: {ex}")
        return False
    finally:
        try:
            # Close the FTP session
            session.quit()
        except Exception as ex:
            logger.error(f"Failed to close FTP session. Error: {ex}")

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
    try:
        # Establish connection to FTP server
        session = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)

        # Retrieve the file
        with open(source_file_path, 'wb') as f:
            session.retrbinary(f'RETR {dest_file_name}', f.write)
        with open(source_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        # Log error if file retrieval from FTP server fails
        logger.error(f"Failed to retrieve file from FTP server. Error: {ex}")
        return
    finally:
        try:
            # Close the FTP session
            session.quit()
        except Exception as ex:
            logger.error(f"Failed to close FTP session. Error: {ex}")

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
    try:
        # Establish connection to FTP server
        session = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)

        # Delete the file
        session.delete(dest_file_name)
        return True
    except Exception as ex:
        # Log error if file deletion from FTP server fails
        logger.error(f"Failed to delete file from FTP server. Error: {ex}")
        return False
    finally:
        try:
            # Close the FTP session
            session.quit()
        except Exception as ex:
            logger.error(f"Failed to close FTP session. Error: {ex}")
```

### **1. Блок-схема**

#### Функция `write` (Отправка файла на FTP-сервер):

```mermaid
graph LR
    A[Начало] --> B{Установить соединение с FTP-сервером}
    B -- Успешно --> C{Открыть локальный файл для чтения (rb)}
    B -- Ошибка --> E[Запись ошибки в лог]
    C --> D{Отправить файл на FTP-сервер (storbinary)}
    D -- Успешно --> F[Возврат True]
    D -- Ошибка --> G[Запись ошибки в лог]
    F --> H{Закрыть FTP-сессию}
    G --> H
    H -- Успешно --> I[Конец]
    H -- Ошибка --> J[Запись ошибки в лог]
    E --> H
    J --> I
```

Пример:
1.  `A`: Начало выполнения функции.
2.  `B`: Функция пытается установить соединение с FTP-сервером, используя параметры из `_connection`. Если соединение установить не удалось, записывается ошибка в лог (`E`).
3.  `C`: Если соединение установлено, открывается локальный файл, указанный в `source_file_path`, для чтения в бинарном режиме (`rb`).
4.  `D`: Файл отправляется на FTP-сервер с использованием команды `storbinary`. Если отправка завершается неудачно, записывается ошибка в лог (`G`).
5.  `F`: В случае успешной отправки файла функция возвращает `True`.
6.  `H`: Независимо от результата отправки файла, функция пытается закрыть FTP-сессию. Если закрытие завершается неудачно, записывается ошибка в лог (`J`).
7.  `I`: Конец выполнения функции.

#### Функция `read` (Чтение файла с FTP-сервера):

```mermaid
graph LR
    A[Начало] --> B{Установить соединение с FTP-сервером}
    B -- Успешно --> C{Открыть локальный файл для записи (wb)}
    B -- Ошибка --> E[Запись ошибки в лог]
    C --> D{Получить файл с FTP-сервера (retrbinary)}
    D -- Успешно --> F{Открыть локальный файл для чтения (rb)}
    D -- Ошибка --> G[Запись ошибки в лог]
    F --> H[Возврат содержимого файла]
    G --> I{Закрыть FTP-сессию}
    H --> I
    I -- Успешно --> J[Конец]
    I -- Ошибка --> K[Запись ошибки в лог]
    E --> I
    K --> J
```

Пример:
1.  `A`: Начало выполнения функции.
2.  `B`: Функция пытается установить соединение с FTP-сервером, используя параметры из `_connection`. Если соединение установить не удалось, записывается ошибка в лог (`E`).
3.  `C`: Если соединение установлено, открывается локальный файл, указанный в `source_file_path`, для записи в бинарном режиме (`wb`).
4.  `D`: Функция пытается получить файл с FTP-сервера с использованием команды `retrbinary`. Если получение завершается неудачно, записывается ошибка в лог (`G`).
5.  `F`: В случае успешного получения файла, функция открывает этот файл для чтения в бинарном режиме (`rb`).
6.  `H`: Возвращается содержимое файла.
7.  `I`: Независимо от результата получения файла, функция пытается закрыть FTP-сессию. Если закрытие завершается неудачно, записывается ошибка в лог (`K`).
8.  `J`: Конец выполнения функции.

#### Функция `delete` (Удаление файла с FTP-сервера):

```mermaid
graph LR
    A[Начало] --> B{Установить соединение с FTP-сервером}
    B -- Успешно --> C{Удалить файл с FTP-сервера (delete)}
    B -- Ошибка --> E[Запись ошибки в лог]
    C -- Успешно --> F[Возврат True]
    C -- Ошибка --> G[Запись ошибки в лог]
    F --> H{Закрыть FTP-сессию}
    G --> H
    H -- Успешно --> I[Конец]
    H -- Ошибка --> J[Запись ошибки в лог]
    E --> H
    J --> I
```

Пример:
1.  `A`: Начало выполнения функции.
2.  `B`: Функция пытается установить соединение с FTP-сервером, используя параметры из `_connection`. Если соединение установить не удалось, записывается ошибка в лог (`E`).
3.  `C`: Если соединение установлено, функция пытается удалить файл с FTP-сервера с использованием команды `delete`. Если удаление завершается неудачно, записывается ошибка в лог (`G`).
4.  `F`: В случае успешного удаления файла функция возвращает `True`.
5.  `H`: Независимо от результата удаления файла, функция пытается закрыть FTP-сессию. Если закрытие завершается неудачно, записывается ошибка в лог (`J`).
6.  `I`: Конец выполнения функции.

### **2. Диаграмма**

```mermaid
flowchart TD
    A[write(source_file_path, dest_dir, dest_file_name)] --> B{ftplib.FTP(_connection['server'], _connection['user'], _connection['password'])}
    B --> C{session.cwd(dest_dir)}
    C --> D{open(source_file_path, 'rb')}
    D --> E{session.storbinary(f'STOR {dest_file_name}', f)}
    E --> F[session.quit()]
    
    G[read(source_file_path, dest_dir, dest_file_name)] --> H{ftplib.FTP(_connection['server'], _connection['user'], _connection['password'])}
    H --> I{session.cwd(dest_dir)}
    I --> J{open(source_file_path, 'wb')}
    J --> K{session.retrbinary(f'RETR {dest_file_name}', f.write)}
    K --> L{open(source_file_path, 'rb')}
    L --> M[return f.read()]
    M --> N[session.quit()]

    O[delete(source_file_path, dest_dir, dest_file_name)] --> P{ftplib.FTP(_connection['server'], _connection['user'], _connection['password'])}
    P --> Q{session.cwd(dest_dir)}
    Q --> R{session.delete(dest_file_name)}
    R --> S[session.quit()]
```

**Зависимости и пояснения:**

*   **ftplib**: Модуль `ftplib` используется для установления соединения с FTP-сервером и выполнения операций, таких как отправка, получение и удаление файлов.
*   **pathlib**: Модуль `pathlib` используется для представления путей к файлам в файловой системе.

### **3. Объяснение**

#### **Импорты:**

*   `from src.logger.logger import logger`: Импортируется объект `logger` из модуля `src.logger.logger` для логирования ошибок и другой важной информации. Это необходимо для отслеживания проблем при работе с FTP-сервером.
*   `from typing import Union`: Импортируется `Union` для указания, что функция может возвращать значения разных типов (строку, байты или None).
*   `import ftplib`: Импортируется модуль `ftplib`, который предоставляет классы и функции для реализации FTP-клиента.
*   `from pathlib import Path`: Импортируется класс `Path` из модуля `pathlib` для работы с путями к файлам.

#### **Переменные:**

*   `_connection`: Словарь, содержащий параметры подключения к FTP-серверу (сервер, порт, пользователь, пароль). Эти параметры используются для установления соединения с FTP-сервером в функциях `write`, `read` и `delete`.

#### **Функции:**

*   `write(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool`:
    *   **Аргументы:**
        *   `source_file_path`: Путь к локальному файлу, который необходимо отправить на FTP-сервер.
        *   `dest_dir`: Директория на FTP-сервере, в которую будет помещен файл.
        *   `dest_file_name`: Имя файла на FTP-сервере.
    *   **Возвращаемое значение:**
        *   `True`, если файл успешно отправлен.
        *   `False`, если произошла ошибка.
    *   **Назначение:**
        Отправляет файл на FTP-сервер. Функция сначала устанавливает соединение с FTP-сервером, затем открывает локальный файл для чтения в бинарном режиме и отправляет его на сервер. В случае ошибки записывает информацию в лог.
    *   **Пример:**
        `success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')`
*   `read(source_file_path: str, dest_dir: str, dest_file_name: str) -> Union[str, bytes, None]`:
    *   **Аргументы:**
        *   `source_file_path`: Путь, по которому будет сохранен файл, скачанный с FTP-сервера.
        *   `dest_dir`: Директория на FTP-сервере, в которой находится файл.
        *   `dest_file_name`: Имя файла на FTP-сервере.
    *   **Возвращаемое значение:**
        *   Содержимое файла (строка или байты), если файл успешно скачан.
        *   `None`, если произошла ошибка.
    *   **Назначение:**
        Скачивает файл с FTP-сервера. Функция устанавливает соединение с FTP-сервером, скачивает файл и сохраняет его локально. Возвращает содержимое скачанного файла. В случае ошибки записывает информацию в лог.
    *   **Пример:**
        `content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')`
*   `delete(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool`:
    *   **Аргументы:**
        *   `source_file_path`: Путь к локальному файлу (не используется).
        *   `dest_dir`: Директория на FTP-сервере, в которой находится файл.
        *   `dest_file_name`: Имя файла на FTP-сервере.
    *   **Возвращаемое значение:**
        *   `True`, если файл успешно удален.
        *   `False`, если произошла ошибка.
    *   **Назначение:**
        Удаляет файл с FTP-сервера. Функция устанавливает соединение с FTP-сервером и удаляет указанный файл. В случае ошибки записывает информацию в лог.
    *   **Пример:**
        `success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')`

#### **Потенциальные ошибки и области для улучшения:**

1.  **Обработка исключений:**
    *   В блоках `try...finally` каждой функции, если `session.quit()` вызывает исключение, это логируется, но не обрабатывается дальше. В зависимости от требований, может потребоваться дополнительная обработка таких исключений (например, повторная попытка закрытия соединения или другие действия).
2.  **Конфигурация FTP-соединения:**
    *   Параметры FTP-соединения хранятся в словаре `_connection`. Было бы лучше, если бы эти параметры загружались из конфигурационного файла или передавались как аргументы функций, чтобы повысить гибкость и безопасность.
3.  **Отсутствие обработки кодировки:**
    *   При чтении файла с FTP-сервера не учитывается кодировка файла. Это может привести к проблемам при работе с файлами, содержащими символы, отличные от ASCII.
4.  **Параметр `source_file_path` в функции `delete`:**
    *   Аргумент `source_file_path` в функции `delete` не используется. Его следует удалить, чтобы не вводить в заблуждение пользователей API.
5.  **Типизация `Union`:**
    *   В аннотации возвращаемого типа функции `read` используется `Union[str, bytes, None]`. Лучше использовать `str | bytes | None`.

#### **Взаимосвязи с другими частями проекта:**

*   `src.logger.logger`: Модуль используется для логирования ошибок и другой информации о работе с FTP-сервером. Это позволяет отслеживать состояние операций и выявлять проблемы.

```mermaid
flowchart TD
    subgraph src.utils.ftp
        A[write]
        B[read]
        C[delete]
    end

    D[src.logger.logger] --> A
    D --> B
    D --> C