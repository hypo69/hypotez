### **Анализ кода модуля `get_free_port.py`**

## \file /src/utils/get_free_port.py

Модуль предназначен для поиска свободного порта в системе. Он предоставляет функциональность для определения доступного порта либо в заданном диапазоне, либо начиная с определенного порта, если диапазон не указан.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован, с использованием внутренних функций для проверки и парсинга портов.
  - Используется логирование ошибок через модуль `src.logger`.
  - Обработка исключений присутствует.
- **Минусы**:
  - Отсутствует docstring для модуля.
  - Есть импорт `header`, который не используется.
  - В docstring используются двойные кавычки вместо одинарных.
  - В блоках `except` используется `e` вместо `ex` для обозначения исключения.
  - Нет аннотаций типов для внутренних функций.
  - В docstring английский язык.

**Рекомендации по улучшению**:

- Добавить docstring для модуля с описанием его назначения и примерами использования.
- Убрать неиспользуемый импорт `header`.
- Исправить использование двойных кавычек в docstring на одинарные.
- Переименовать переменную исключения `e` в `ex` в блоках `except`.
- Добавить аннотации типов для параметров и возвращаемых значений внутренних функций `_is_port_in_use` и `_parse_port_range`.
- Перевести docstring на русский язык.
- Заменить `Union` на `|`.
- Для логирования добавить `exc_info=True`.

**Оптимизированный код**:

```python
## \file /src/utils/get_free_port.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для поиска свободного порта.
=====================================

Модуль предоставляет функцию :func:`get_free_port`, которая позволяет найти свободный порт в системе.
Функция может искать порт в заданном диапазоне или начиная с определенного порта, если диапазон не указан.

Пример использования:
----------------------

>>> get_free_port('localhost', '3000-3005')
3001
"""

import socket
from typing import Optional, Tuple, List

from src.logger import logger


def get_free_port(host: str, port_range: Optional[str | List[str]] = None) -> int:
    """
    Находит и возвращает свободный порт в указанном диапазоне или первый доступный порт, если диапазон не задан.

    Args:
        host (str): Адрес хоста для проверки доступности портов.
        port_range (Optional[str | List[str]], optional): Диапазон портов, заданный строкой "min-max" или списком строк.
            Например: "3000-3999", ["3000-3999", "8000-8010"], None. По умолчанию None.

    Returns:
        int: Доступный номер порта.

    Raises:
        ValueError: Если не удается найти свободный порт в указанном диапазоне или если диапазон портов недействителен.
    """

    def _is_port_in_use(host: str, port: int) -> bool:
        """
        Проверяет, используется ли данный порт на указанном хосте.

        Args:
            host (str): Адрес хоста.
            port (int): Номер порта для проверки.

        Returns:
            bool: True, если порт используется, False в противном случае.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return False  # Port is available
            except OSError:
                return True  # Port is in use

    def _parse_port_range(port_range_str: str) -> Tuple[int, int]:
        """
        Преобразует строку диапазона портов "min-max" в кортеж (min_port, max_port).

        Args:
            port_range_str (str): Строка диапазона портов.

        Returns:
            Tuple[int, int]: Кортеж, содержащий минимальный и максимальный номера портов.

        Raises:
            ValueError: Если формат строки диапазона портов недействителен.
        """
        try:
            parts = port_range_str.split('-')
            if len(parts) != 2:
                logger.error(f'Ошибка: Неверный формат строки диапазона портов: {port_range_str}', exc_info=True)
                raise ValueError(f'Неверный формат строки диапазона портов: {port_range_str}')
            min_port = int(parts[0])
            max_port = int(parts[1])

            if min_port >= max_port:
                logger.error(f'Ошибка: Неверный диапазон портов {port_range_str}', exc_info=True)
                raise ValueError(f'Неверный диапазон портов {port_range_str}')
            return min_port, max_port

        except ValueError as ex:
            logger.error(f'Ошибка: Неверный диапазон портов {port_range_str}', ex, exc_info=True)
            raise ValueError(f'Неверный диапазон портов {port_range_str}')

    if port_range:
        if isinstance(port_range, str):
            try:
                min_port, max_port = _parse_port_range(port_range)
            except ValueError as ex:
                logger.error(f'Ошибка: {ex}', ex, exc_info=True)
                raise ValueError(f'Неверный диапазон портов {port_range}')
            for port in range(min_port, max_port + 1):
                if not _is_port_in_use(host, port):
                    return port
            logger.error(f'Ошибка: Нет свободного порта в диапазоне {port_range}', exc_info=True)
            raise ValueError(f'Нет свободного порта в диапазоне {port_range}')

        elif isinstance(port_range, list):
            for item in port_range:
                try:
                    if isinstance(item, str):
                        min_port, max_port = _parse_port_range(item)
                    else:
                        logger.error(f'Ошибка: Неверный элемент диапазона портов {item}', exc_info=True)
                        raise ValueError(f'Неверный элемент диапазона портов {item}')

                    for port in range(min_port, max_port + 1):
                        if not _is_port_in_use(host, port):
                            return port
                except ValueError as ex:
                    logger.error(f'Ошибка: {ex}', ex, exc_info=True)
                    continue  # Skip to the next range in the list if any range fails parsing or no port

            logger.error(f'Ошибка: Нет свободного порта в указанных диапазонах {port_range}', exc_info=True)
            raise ValueError(f'Нет свободного порта в указанных диапазонах {port_range}')

        else:
            logger.error(f'Ошибка: Неверный тип диапазона портов {type(port_range)}', exc_info=True)
            raise ValueError(f'Неверный тип диапазона портов {type(port_range)}')
    else:
        # If no range given, find first available port
        port = 1024  # start from 1024, since lower ports are system ports
        while True:
            if not _is_port_in_use(host, port):
                return port
            port += 1
            if port > 65535:
                logger.error(f'Ошибка: Нет свободного порта', exc_info=True)
                raise ValueError('Нет свободного порта')