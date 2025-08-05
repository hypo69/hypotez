### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_free_port` ищет и возвращает свободный порт в заданном диапазоне или первый доступный порт, если диапазон не указан. Функция проверяет, занят ли порт, используя сокеты, и может принимать диапазон портов в виде строки или списка строк.

Шаги выполнения
-------------------------
1. Функция `get_free_port` принимает хост (host) в виде строки и необязательный диапазон портов (port_range), который может быть строкой (например, "3000-3999") или списком строк (например, ["3000-3999", "8000-8010"]).
2. Если `port_range` указан:
   - Если это строка, функция `_parse_port_range` разбивает строку на минимальный и максимальный порты.
   - Функция итерируется по диапазону портов и проверяет каждый порт с помощью `_is_port_in_use`.
   - Если порт свободен, функция возвращает этот порт.
   - Если `port_range` является списком, функция перебирает элементы списка, каждый из которых должен быть строкой, представляющей диапазон портов.
   - Если ни один свободный порт не найден в указанных диапазонах, вызывается исключение `ValueError`.
3. Если `port_range` не указан:
   - Функция начинает поиск с порта 1024 и увеличивает его до тех пор, пока не найдет свободный порт.
   - Если порт найден, функция возвращает этот порт.
   - Если ни один свободный порт не найден в диапазоне 1024-65535, вызывается исключение `ValueError`.

Пример использования
-------------------------

```python
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
                return False  # Порт доступен
            except OSError:
                return True  # Порт используется

    def _parse_port_range(port_range_str: str) -> Tuple[int, int]:
        """
        Разбирает строку диапазона портов "min-max" в кортеж (min_port, max_port).

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
                logger.error(f'Error: Invalid port range string format: {port_range_str}')
                raise ValueError(f'Invalid port range string format: {port_range_str}')
            min_port = int(parts[0])
            max_port = int(parts[1])

            if min_port >= max_port:
                logger.error(f'Error: Invalid port range {port_range_str}')
                raise ValueError(f'Invalid port range {port_range_str}')
            return min_port, max_port

        except ValueError:
            logger.error(f'Error: Invalid port range {port_range_str}')
            raise ValueError(f'Invalid port range {port_range_str}')

    if port_range:
        if isinstance(port_range, str):
            try:
                min_port, max_port = _parse_port_range(port_range)
            except ValueError as e:
                logger.error(f'Error: {e}')
                raise ValueError(f'Invalid port range {port_range}')
            for port in range(min_port, max_port + 1):
                if not _is_port_in_use(host, port):
                    return port
            logger.error(f'Error: No free port found in range {port_range}')
            raise ValueError(f'No free port found in range {port_range}')

        elif isinstance(port_range, list):
            for item in port_range:
                try:
                    if isinstance(item, str):
                        min_port, max_port = _parse_port_range(item)
                    else:
                        logger.error(f'Error: Invalid port range item {item}')
                        raise ValueError(f'Invalid port range item {item}')

                    for port in range(min_port, max_port + 1):
                        if not _is_port_in_use(host, port):
                            return port
                except ValueError as e:
                    logger.error(f'Error: {e}')
                    continue  # Пропуск к следующему диапазону в списке, если какой-либо диапазон не удалось разобрать или нет порта

            logger.error(f'Error: No free port found in specified ranges {port_range}')
            raise ValueError(f'No free port found in specified ranges {port_range}')

        else:
            logger.error(f'Error: Invalid port range type {type(port_range)}')
            raise ValueError(f'Invalid port range type {type(port_range)}')
    else:
        # Если диапазон не задан, поиск первого доступного порта
        port = 1024  # начать с 1024, так как более низкие порты являются системными
        while True:
            if not _is_port_in_use(host, port):
                return port
            port += 1
            if port > 65535:
                logger.error(f'Error: No free port found')
                raise ValueError('No free port found')

# Пример использования:
try:
    free_port = get_free_port('localhost', '3000-3005')
    print(f'Свободный порт: {free_port}')
except ValueError as e:
    print(f'Ошибка: {e}')

try:
    free_port = get_free_port('localhost')
    print(f'Свободный порт: {free_port}')
except ValueError as e:
    print(f'Ошибка: {e}')