### **Анализ кода модуля `get_free_port.py`**

## \file /src/utils/get_free_port.py

Модуль предназначен для поиска свободного порта в заданном диапазоне или первого доступного порта, если диапазон не указан.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на отдельные функции, что облегчает его понимание и поддержку.
  - Используется логирование ошибок с помощью модуля `src.logger`.
  - Обработка исключений помогает предотвратить сбои в работе программы.
- **Минусы**:
  - Отсутствует описание модуля в формате, требуемом инструкцией.
  - Не все переменные аннотированы типами.
  - Docstring функции `get_free_port` и `_is_port_in_use`  повторяют описание. Требуется более подробное объяснение, что именно делает функция
  - В коде присуствуют комментарии на английском языке. Необходимо перевести их на русский.
  - В блоках `except` используется `e` вместо `ex`.
  - Не хватает аннотаций типов в некоторых местах.
  - Не используется `j_loads` или `j_loads_ns` для чтения конфигурационных файлов (если это применимо).

**Рекомендации по улучшению**:

1.  Добавить описание модуля в соответствии с форматом, указанным в инструкции.
2.  Перевести все комментарии и docstring на русский язык.
3.  Заменить `e` на `ex` в блоках `except`.
4.  Добавить аннотации типов для всех переменных, где это необходимо.
5.  Уточнить docstring для функций, чтобы они более детально описывали, что делает каждая функция.
6.  Добавить проверки и обработку исключений для более надежной работы кода.

**Оптимизированный код**:

```python
                ## \\file /src/utils/get_free_port.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для поиска свободного порта.
======================================

Модуль содержит функцию :func:`get_free_port`, которая используется для поиска доступного порта в заданном диапазоне или первого свободного порта, если диапазон не указан.

Пример использования
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
        host (str): Адрес хоста для проверки доступных портов.
        port_range (Optional[str | List[str]], optional): Диапазон портов, заданный строкой "min-max" или списком строк.
            Например: "3000-3999", ["3000-3999", "8000-8010"], None. По умолчанию `None`.

    Returns:
        int: Доступный номер порта.

    Raises:
        ValueError: Если не удается найти свободный порт в указанном диапазоне или если диапазон портов недействителен.

    Example:
        >>> get_free_port('localhost', '3000-3005')
        3001
    """

    def _is_port_in_use(host: str, port: int) -> bool:
        """
        Проверяет, используется ли данный порт на указанном хосте.

        Args:
            host (str): Адрес хоста.
            port (int): Номер порта для проверки.

        Returns:
            bool: `True`, если порт используется, `False` в противном случае.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return False  # Порт доступен
            except OSError:
                return True  # Порт используется

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
            parts: List[str] = port_range_str.split('-')  # Разделяем строку на части
            if len(parts) != 2:
                logger.error(f'Ошибка: Неверный формат строки диапазона портов: {port_range_str}')
                raise ValueError(f'Неверный формат строки диапазона портов: {port_range_str}')
            min_port: int = int(parts[0])  # Преобразуем минимальный порт в целое число
            max_port: int = int(parts[1])  # Преобразуем максимальный порт в целое число

            if min_port >= max_port:
                logger.error(f'Ошибка: Неверный диапазон портов {port_range_str}')
                raise ValueError(f'Неверный диапазон портов {port_range_str}')
            return min_port, max_port

        except ValueError as ex: # Обрабатываем исключение при неверном формате
            logger.error(f'Ошибка: Неверный диапазон портов {port_range_str}', ex, exc_info=True)
            raise ValueError(f'Неверный диапазон портов {port_range_str}') from ex

    if port_range:
        if isinstance(port_range, str):
            try:
                min_port: int
                max_port: int
                min_port, max_port = _parse_port_range(port_range) # Получаем минимальный и максимальный порты
            except ValueError as ex: # Обрабатываем исключение при неверном формате
                logger.error(f'Ошибка: {ex}', ex, exc_info=True)
                raise ValueError(f'Неверный диапазон портов {port_range}') from ex
            for port in range(min_port, max_port + 1): # Итерируемся по диапазону портов
                if not _is_port_in_use(host, port): # Проверяем, используется ли порт
                    return port # Возвращаем порт, если он свободен
            logger.error(f'Ошибка: Не найден свободный порт в диапазоне {port_range}')
            raise ValueError(f'Не найден свободный порт в диапазоне {port_range}')

        elif isinstance(port_range, list):
            for item in port_range:
                try:
                    if isinstance(item, str):
                        min_port: int
                        max_port: int
                        min_port, max_port = _parse_port_range(item)
                    else:
                        logger.error(f'Ошибка: Неверный элемент диапазона портов {item}')
                        raise ValueError(f'Неверный элемент диапазона портов {item}')

                    for port in range(min_port, max_port + 1):
                        if not _is_port_in_use(host, port):
                            return port
                except ValueError as ex:
                    logger.error(f'Ошибка: {ex}', ex, exc_info=True)
                    continue  # Пропускаем к следующему диапазону в списке, если какой-либо диапазон не проходит разбор или нет порта

            logger.error(f'Ошибка: Не найден свободный порт в указанных диапазонах {port_range}')
            raise ValueError(f'Не найден свободный порт в указанных диапазонах {port_range}')

        else:
            logger.error(f'Ошибка: Неверный тип диапазона портов {type(port_range)}')
            raise ValueError(f'Неверный тип диапазона портов {type(port_range)}')
    else:
        # Если диапазон не задан, находим первый доступный порт
        port: int = 1024  # начинаем с 1024, так как более низкие порты являются системными
        while True:
            if not _is_port_in_use(host, port):
                return port
            port += 1
            if port > 65535:
                logger.error(f'Ошибка: Не найден свободный порт')
                raise ValueError('Не найден свободный порт')