## \file /src/utils/port.py
# -*- coding: utf-8 -*-
# Указание кодировки файла.
#! .pyenv/bin/python3
# Шебанг: путь к интерпретатору Python.
"""
Модуль для поиска свободного сетевого порта.
===============================================

Позволяет найти свободный порт на указанном хосте либо в заданном диапазоне(ах),
либо начиная с определенного порта вверх.

Args:
    host (str): Адрес хоста для проверки доступности портов.
    port_range (Optional[str | List[str | List[int]]], optional): Диапазон(ы) портов.
           Может быть строкой "min-max", списком строк "min-max",
           списком списков чисел [min, max] или None.
           Например: "3000-3999", ["3000-3999", "8000-8010"], [[4000, 4099], [9000, 9010]], None.
           По умолчанию None.

Returns:
    int: Номер доступного порта.

Raises:
    ValueError: Если не удалось найти свободный порт в указанном диапазоне(ах)
                или если формат диапазона некорректен.

Example:
    >>> get_free_port('localhost', '3000-3005')
    3001
    >>> get_free_port('localhost', ['4000-4005', [5000, 5010]])
    5002
```rst
    ..:module:: src.utils.port
```
"""

import socket
from typing import Optional, Tuple, List, Union # Импорт Union для более точного указания типов

# Импорт локальных модулей
# import header  # Not used in this specific snippet, commented out based on original
from src.logger import logger # Настройка логгирования для приложения.

# Тип для port_range с учетом форматов  "3000-3999", ["3000-3999", "8000-8010"], [[4000, 4099], [9000, 9010]]
PortRangeType = Optional[Union[str, List[Union[str, List[int]]]]]

def get_free_port(host: str, port_range: PortRangeType = None) -> int:
    """
    Находит и возвращает свободный порт в указанном диапазоне(ах),
    или первый доступный порт, если диапазон не задан.

    Args:
        host (str): Адрес хоста для проверки доступности портов.
        port_range (PortRangeType, optional): Диапазон(ы) портов.
               Может быть строкой "min-max", списком строк "min-max",
               списком списков чисел [min, max] или None.
               По умолчанию None.

    Returns:
        int: Номер доступного порта.

    Raises:
        ValueError: Если не удалось найти свободный порт в указанном диапазоне(ах)
                    или если формат диапазона некорректен.
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
        # Создаем сокет с использованием контекстного менеджера для автоматического закрытия.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Пытаемся привязать сокет к адресу и порту.
                sock.bind((host, port))
                # Если привязка удалась, порт свободен.
                return False  # Port is available
            except OSError:
                # Если произошла OSError (например, "Address already in use"), порт занят.
                return True  # Port is in use
            except Exception as e:
                # Логирование других возможных ошибок сокета.
                logger.error(f"Ошибка при проверке порта {port} на {host}: {e}")
                # В случае других ошибок, считаем порт недоступным или возникают проблемы.
                return True # Assume in use or problematic

    def _parse_port_range(port_range_str: str) -> Tuple[int, int]:
        """
        Парсит строку диапазона портов "min-max" в кортеж (min_port, max_port).

        Args:
            port_range_str (str): Строка диапазона портов.

        Returns:
            Tuple[int, int]: Кортеж, содержащий минимальный и максимальный номера портов.

        Raises:
            ValueError: Если формат строки диапазона портов некорректен.
        """
        try:
            # Разбиваем строку по символу "-".
            parts = port_range_str.split('-')
            # Проверяем, что получилось ровно две части.
            if len(parts) != 2:
                logger.error(f'Ошибка: Некорректный формат строки диапазона портов: {port_range_str}')
                raise ValueError(f'Invalid port range string format: {port_range_str}')
            # Преобразуем части в целые числа.
            min_port = int(parts[0])
            max_port = int(parts[1])

            # Проверяем корректность диапазона (минимум меньше максимума).
            if min_port >= max_port:
                logger.error(f'Ошибка: Некорректный диапазон портов {port_range_str}')
                raise ValueError(f'Invalid port range {port_range_str}')
            # Проверяем допустимость номеров портов (от 1 до 65535).
            if not (0 <= min_port <= 65535 and 0 <= max_port <= 65535):
                 logger.error(f'Ошибка: Диапазон портов вне допустимого диапазона (0-65535): {port_range_str}')
                 raise ValueError(f'Port range outside valid range (0-65535): {port_range_str}')

            return min_port, max_port

        except ValueError as e:
            # Перехватываем ошибки преобразования в int или проверки формата.
            logger.error(f'Ошибка при парсинге диапазона {port_range_str}: {e}')
            raise ValueError(f'Invalid port range {port_range_str}') from e # Привязываем исходное исключение


    # --- Основная логика поиска порта ---
    if port_range:
        # Если задан диапазон или список диапазонов.
        if isinstance(port_range, str):
            # Если задана одна строка диапазона ("min-max").
            try:
                # Парсим строку диапазона.
                min_port, max_port = _parse_port_range(port_range)
            except ValueError as e:
                # Если парсинг строки не удался, логируем и перевыбрасываем исключение.
                logger.error(f'Ошибка: Некорректный диапазон портов (строка) {port_range}: {e}')
                raise ValueError(f'Invalid port range {port_range}') from e
            # Перебираем порты в полученном диапазоне.
            for port in range(min_port, max_port + 1):
                # Если порт свободен, возвращаем его.
                if not _is_port_in_use(host, port):
                    logger.info(f"Найден свободный порт {port} в диапазоне {port_range}")
                    return port
            # Если цикл завершился, значит, ни один порт в диапазоне не свободен.
            logger.error(f'Ошибка: Не найдено свободных портов в диапазоне {port_range}')
            raise ValueError(f'No free port found in range {port_range}')

        elif isinstance(port_range, list):
            # Если задан список диапазонов (строк "min-max" или списков [min, max]).
            logger.debug(f"Проверка на диапазоны из списка: {port_range}")
            # Перебираем каждый элемент в списке.
            for item in port_range:
                min_port, max_port = -1, -1 # Инициализация для текущего диапазона
                try:
                    if isinstance(item, str):
                        # Если элемент - строка ("min-max"), парсим ее.
                        logger.debug(f"Парсим строковый диапазон: {item}")
                        min_port, max_port = _parse_port_range(item)
                    elif isinstance(item, list) and len(item) == 2:
                        # Если элемент - список из двух элементов, проверяем, что это числа.
                        logger.debug(f"Проверка на диапазон в формате списка: {item}")
                        if all(isinstance(p, int) for p in item):
                             min_port, max_port = item[0], item[1]
                             # Добавляем валидацию для формата [min, max]
                             if not (0 <= min_port <= 65535 and 0 <= max_port <= 65535):
                                 logger.warning(f'Предупреждение: Диапазон портов вне допустимого диапазона (0-65535) в элементе {item}. Пропускаем.')
                                 # Вместо raise в try-except, просто пропускаем этот элемент.
                                 continue
                             if min_port >= max_port:
                                logger.warning(f'Предупреждение: Некорректный диапазон [min, max] (min >= max) в элементе {item}. Пропускаем.')
                                # Вместо raise в try-except, просто пропускаем этот элемент.
                                continue
                        else:
                             # Если элементы списка не являются числами.
                             logger.warning(f'Предупреждение: Некорректный формат диапазона [min, max] (не целые числа) в элементе {item}. Пропускаем.')
                             continue # Пропускаем этот элемент и переходим к следующему
                    else:
                        # Если элемент списка имеет некорректный тип или формат.
                        logger.warning(f'Предупреждение: Некорректный тип или формат элемента диапазона в списке: {item}. Пропускаем.')
                        continue # Пропускаем этот элемент и переходим к следующему

                    # Если min_port и max_port были успешно определены (парсинг или валидация прошли).
                    if min_port != -1 and max_port != -1:
                        # Перебираем порты в текущем под-диапазоне.
                        for port in range(min_port, max_port + 1):
                            # Если порт свободен, возвращаем его немедленно.
                            if not _is_port_in_use(host, port):
                                logger.info(f"Найден свободный порт {port} в диапазоне из списка: {item}")
                                return port # Возвращаем найденный порт

                except ValueError as e:
                    # Перехватываем ошибки парсинга строки или валидации списка,
                    # логируем как предупреждение и переходим к следующему элементу списка диапазонов.
                    logger.warning(f'Ошибка при обработке элемента диапазона {item}: {e}. Пропускаем.')
                    continue # Продолжаем проверять следующий диапазон в списке

            # Если цикл по элементам списка завершился, и ни один порт не был возвращен,
            # значит, свободный порт не найден ни в одном из указанных диапазонов.
            logger.error(f'Ошибка: Не найдено свободных портов ни в одном из указанных диапазонов: {port_range}')
            # Убираем '...'
            raise ValueError(f'No free port found in specified ranges {port_range}')

        else:
            # Если port_range не строка, не список и не None - некорректный тип.
            logger.error(f'Ошибка: Некорректный тип параметра port_range: {type(port_range)}')
            # Убираем '...'
            raise ValueError(f'Invalid port range type {type(port_range)}')
    else:
        # Если диапазон не задан (port_range is None).
        logger.debug("Диапазон не задан, ищем первый свободный порт.")
        # Начинаем поиск с порта 1024 (порты ниже 1024 обычно зарезервированы).
        port = 1024  # start from 1024, since lower ports are system ports
        # Бесконечный цикл для поиска порта.
        while True:
            # Если порт свободен, возвращаем его.
            if not _is_port_in_use(host, port):
                logger.info(f"Найден первый свободный порт: {port}")
                return port
            # Иначе, увеличиваем номер порта.
            port += 1
            # Проверка на выход за пределы допустимых номеров портов (макс 65535).
            if port > 65535:
                # Если достигли предела, и порт не найден, выбрасываем исключение.
                logger.error(f'Ошибка: Не найдено свободных портов до {port}')
                # Убираем '...'
                raise ValueError('No free port found')