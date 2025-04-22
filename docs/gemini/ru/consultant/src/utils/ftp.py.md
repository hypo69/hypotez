### **Анализ кода модуля `src.utils.ftp`**

## \file /src/utils/ftp.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура модуля и функций.
    - Наличие docstring для каждой функции с описанием аргументов, возвращаемых значений и возможных исключений.
    - Использование `logger` для регистрации ошибок.
    - Обработка исключений при подключении, передаче и закрытии FTP-соединения.
- **Минусы**:
    - Параметры подключения к FTP-серверу заданы как глобальная переменная `_connection`, что не рекомендуется.
    - Функция `delete` принимает `source_file_path`, который не используется.
    - Жестко закодированные параметры подключения (сервер, порт, пользователь, пароль).
    - Не все типы данных аннотированы.

**Рекомендации по улучшению:**

1.  **Перенести параметры соединения в класс Config**:
    Рекомендуется создать класс `Config` и перенести туда параметры соединения с FTP сервером. Это позволит избежать использования глобальных переменных и упростит управление конфигурацией.
2.  **Использовать `j_loads` или `j_loads_ns` для загрузки параметров соединения**:
    Если параметры соединения хранятся в файле, использовать `j_loads` или `j_loads_ns` для их загрузки.
3.  **Удалить неиспользуемый аргумент**:
    Удалить аргумент `source_file_path` из функции `delete`, так как он не используется.
4.  **Добавить аннотации типов**:
    Добавить аннотации типов для всех переменных и возвращаемых значений, где это необходимо.
5.  **Рефакторинг обработки исключений**:
    Упростить блоки `try...finally`, чтобы гарантировать закрытие соединения.
6. **Добавить docstring для внутренних функций**:\
Добавить docstring для внутренних функций, если они есть.

**Оптимизированный код:**

```python
## \file /src/utils/ftp.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с FTP-серверами
===========================================

Модуль предоставляет интерфейс для взаимодействия с FTP-серверами,
включая функции для отправки, получения и удаления файлов.

**Назначение:**
Позволяет отправлять и получать медиафайлы (изображения, видео),
электронные таблицы и другие файлы на/с FTP-сервера.

**Модули:**
- src.logger.logger: Для логирования операций.
- typing: Для аннотаций типов.
- ftplib: Для работы с FTP протоколом.
- pathlib: Для работы с путями к файлам.

Функции:
    - write: Отправляет файл на FTP-сервер.
    - read: Получает файл с FTP-сервера.
    - delete: Удаляет файл с FTP-сервера.

.. module:: src.utils.ftp
"""

from src.logger.logger import logger
from typing import Union, Optional
import ftplib
from pathlib import Path


class Config:
    """
    Конфигурация для подключения к FTP-серверу.
    """
    server: str = 'ftp.example.com'
    port: int = 21
    user: str = 'username'
    password: str = 'password'


def write(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool:
    """
    Отправляет файл на FTP-сервер.

    Args:
        source_file_path (str): Путь к локальному файлу для отправки.
        dest_dir (str): Целевой каталог на FTP-сервере.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        bool: True, если файл успешно отправлен, иначе False.
    
    Raises:
        Exception: Если не удалось подключиться к FTP-серверу или отправить файл.

    Example:
        >>> success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    session: Optional[ftplib.FTP] = None
    try:
        # Функция устанавливает соединение с FTP-сервером
        session = ftplib.FTP(
            Config.server,
            Config.user,
            Config.password
        )
        # Функция переходит в указанный каталог на FTP-сервере
        session.cwd(dest_dir)

        # Функция открывает и отправляет файл на FTP-сервер
        with open(source_file_path, 'rb') as f:
            session.storbinary(f'STOR {dest_file_name}', f)
        # Функция возвращает True, если файл был успешно отправлен
        return True
    except Exception as ex:
        # Логирует ошибку, если не удалось отправить файл на FTP-сервер
        logger.error(f"Не удалось отправить файл на FTP-сервер. Ошибка: {ex}", ex, exc_info=True)
        # Функция возвращает False, если произошла ошибка при отправке файла
        return False
    finally:
        if session:
            try:
                # Функция закрывает FTP-сессию
                session.quit()
            except Exception as ex:
                # Логирует ошибку, если не удалось закрыть FTP-сессию
                logger.error(f"Не удалось закрыть FTP-сессию. Ошибка: {ex}", ex, exc_info=True)


def read(source_file_path: str, dest_dir: str, dest_file_name: str) -> Union[str, bytes, None]:
    """
    Получает файл с FTP-сервера.

    Args:
        source_file_path (str): Путь для сохранения файла локально.
        dest_dir (str): Каталог на FTP-сервере, где находится файл.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        Union[str, bytes, None]: Содержимое файла, если успешно получен, иначе None.
    
    Raises:
        Exception: Если не удалось подключиться к FTP-серверу или получить файл.

    Example:
        >>> content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(content)
        b'Some file content'
    """
    session: Optional[ftplib.FTP] = None
    try:
        # Функция устанавливает соединение с FTP-сервером
        session = ftplib.FTP(
            Config.server,
            Config.user,
            Config.password
        )
        # Функция переходит в указанный каталог на FTP-сервере
        session.cwd(dest_dir)

        # Функция получает файл с FTP-сервера
        with open(source_file_path, 'wb') as f:
            session.retrbinary(f'RETR {dest_file_name}', f.write)
        # Функция открывает полученный файл и возвращает его содержимое
        with open(source_file_path, 'rb') as f:
            # Функция возвращает содержимое файла
            return f.read()
    except Exception as ex:
        # Логирует ошибку, если не удалось получить файл с FTP-сервера
        logger.error(f"Не удалось получить файл с FTP-сервера. Ошибка: {ex}", ex, exc_info=True)
        # Функция возвращает None, если произошла ошибка при получении файла
        return None
    finally:
        if session:
            try:
                # Функция закрывает FTP-сессию
                session.quit()
            except Exception as ex:
                # Логирует ошибку, если не удалось закрыть FTP-сессию
                logger.error(f"Не удалось закрыть FTP-сессию. Ошибка: {ex}", ex, exc_info=True)


def delete(dest_dir: str, dest_file_name: str) -> bool:
    """
    Удаляет файл с FTP-сервера.

    Args:
        dest_dir (str): Каталог на FTP-сервере, где находится файл.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        bool: True, если файл успешно удален, иначе False.
    
    Raises:
        Exception: Если не удалось подключиться к FTP-серверу или удалить файл.

    Example:
        >>> success = delete('/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    session: Optional[ftplib.FTP] = None
    try:
        # Функция устанавливает соединение с FTP-сервером
        session = ftplib.FTP(
            Config.server,
            Config.user,
            Config.password
        )
        # Функция переходит в указанный каталог на FTP-сервере
        session.cwd(dest_dir)

        # Функция удаляет файл с FTP-сервера
        session.delete(dest_file_name)
        # Функция возвращает True, если файл был успешно удален
        return True
    except Exception as ex:
        # Логирует ошибку, если не удалось удалить файл с FTP-сервера
        logger.error(f"Не удалось удалить файл с FTP-сервера. Ошибка: {ex}", ex, exc_info=True)
        # Функция возвращает False, если произошла ошибка при удалении файла
        return False
    finally:
        if session:
            try:
                # Функция закрывает FTP-сессию
                session.quit()
            except Exception as ex:
                # Логирует ошибку, если не удалось закрыть FTP-сессию
                logger.error(f"Не удалось закрыть FTP-сессию. Ошибка: {ex}", ex, exc_info=True)