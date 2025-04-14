### **Анализ кода модуля `ftp.py`**

## \file /src/utils/ftp.py

Модуль предоставляет интерфейс для взаимодействия с FTP-серверами. Он включает функции для отправки, получения и удаления файлов с FTP-сервера.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура функций.
    - Обработка исключений с логированием ошибок.
    - Использование `logger` для регистрации ошибок.
    - Наличие docstring для каждой функции.
- **Минусы**:
    - Конфигурация подключения к FTP-серверу (`_connection`) задана непосредственно в коде, что не является хорошей практикой.
    - Не все переменные аннотированы типами.
    - В функции `read` возвращается `Union[str, bytes, None]`. Лучше использовать только `bytes` или определить собственный тип.
    - В docstring есть английский текст, который нужно перевести на русский.
    - Параметр `source_file_path` в функции `delete` не используется, что может запутать пользователей.

**Рекомендации по улучшению:**

1.  **Вынесение конфигурации**:
    - Перенести параметры подключения к FTP-серверу в отдельный конфигурационный файл или переменные окружения.

2.  **Типизация переменных**:
    - Добавить аннотации типов для всех переменных, чтобы улучшить читаемость и предотвратить ошибки.

3.  **Улучшение функции `read`**:
    - Убедиться, что функция всегда возвращает `bytes` или `None`, чтобы избежать неоднозначности типов.

4.  **Удаление неиспользуемого параметра**:
    - Удалить неиспользуемый параметр `source_file_path` из функции `delete`.

5.  **Документирование и перевод**:
    - Перевести все docstring и комментарии на русский язык.

6.  **Обработка исключений**:
    - Сделать обработку исключений более специфичной, чтобы логировать только те ошибки, которые действительно важны.

**Оптимизированный код:**

```python
                ## \file /src/utils/ftp.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для взаимодействия с FTP-серверами.
==============================================

Модуль предоставляет интерфейс для взаимодействия с FTP-серверами.
Он включает функции для отправки, получения и удаления файлов с FTP-сервера.

**Назначение**:
Позволяет отправлять и получать медиафайлы (изображения, видео), электронные таблицы и другие файлы на/с FTP-сервера.

**Модули**:
- src.logger.logger: Локальный модуль для логирования операций FTP.
- typing: Подсказки типов для параметров функций и возвращаемых значений.
- ftplib: Предоставляет клиентские возможности протокола FTP.
- pathlib: Для обработки путей файловой системы.

Функции:
    - `write`: Отправляет файл на FTP-сервер.
    - `read`: Получает файл с FTP-сервера.
    - `delete`: Удаляет файл с FTP-сервера.
"""

from src.logger.logger import logger
from typing import Union, Optional
import ftplib
from pathlib import Path

# Параметры подключения к FTP-серверу
_connection = {
    'server': 'ftp.example.com',
    'port': 21,
    'user': 'username',
    'password': 'password'
}

def write(source_file_path: str, dest_dir: str, dest_file_name: str) -> bool:
    """
    Отправляет файл на FTP-сервер.

    Args:
        source_file_path (str): Путь к файлу, который нужно отправить.
        dest_dir (str): Каталог назначения на FTP-сервере.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        bool: True, если файл успешно отправлен, иначе False.

    Example:
        >>> success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    try:
        # Устанавливаем соединение с FTP-сервером
        session: ftplib.FTP = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)
    except Exception as ex:
        # Логируем ошибку, если не удалось подключиться к FTP-серверу
        logger.error('Не удалось подключиться к FTP-серверу', ex, exc_info=True)
        return False

    try:
        # Открываем файл и отправляем его на FTP-сервер
        with open(source_file_path, 'rb') as f:
            session.storbinary(f'STOR {dest_file_name}', f)
        return True
    except Exception as ex:
        # Логируем ошибку, если не удалось отправить файл на FTP-сервер
        logger.error('Не удалось отправить файл на FTP-сервер', ex, exc_info=True)
        return False
    finally:
        try:
            # Закрываем FTP-сессию
            session.quit()
        except Exception as ex:
            logger.error('Не удалось закрыть FTP-сессию', ex, exc_info=True)


def read(source_file_path: str, dest_dir: str, dest_file_name: str) -> Optional[bytes]:
    """
    Получает файл с FTP-сервера.

    Args:
        source_file_path (str): Путь, куда будет сохранен файл локально.
        dest_dir (str): Каталог на FTP-сервере, где находится файл.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        Optional[bytes]: Содержимое файла, если он успешно получен, иначе None.

    Example:
        >>> content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
        >>> print(content)
        b'Some file content'
    """
    try:
        # Устанавливаем соединение с FTP-сервером
        session: ftplib.FTP = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)

        # Получаем файл
        with open(source_file_path, 'wb') as f:
            session.retrbinary(f'RETR {dest_file_name}', f.write)
        with open(source_file_path, 'rb') as f:
            return f.read()
    except Exception as ex:
        # Логируем ошибку, если не удалось получить файл с FTP-сервера
        logger.error('Не удалось получить файл с FTP-сервера', ex, exc_info=True)
        return None
    finally:
        try:
            # Закрываем FTP-сессию
            session.quit()
        except Exception as ex:
            logger.error('Не удалось закрыть FTP-сессию', ex, exc_info=True)


def delete(dest_dir: str, dest_file_name: str) -> bool:
    """
    Удаляет файл с FTP-сервера.

    Args:
        dest_dir (str): Каталог на FTP-сервере, где находится файл.
        dest_file_name (str): Имя файла на FTP-сервере.

    Returns:
        bool: True, если файл успешно удален, иначе False.

    Example:
        >>> success = delete('/remote/directory', 'file.txt')
        >>> print(success)
        True
    """
    try:
        # Устанавливаем соединение с FTP-сервером
        session: ftplib.FTP = ftplib.FTP(
            _connection['server'],
            _connection['user'],
            _connection['password'])
        session.cwd(dest_dir)

        # Удаляем файл
        session.delete(dest_file_name)
        return True
    except Exception as ex:
        # Логируем ошибку, если не удалось удалить файл с FTP-сервера
        logger.error('Не удалось удалить файл с FTP-сервера', ex, exc_info=True)
        return False
    finally:
        try:
            # Закрываем FTP-сессию
            session.quit()
        except Exception as ex:
            logger.error('Не удалось закрыть FTP-сессию', ex, exc_info=True)