## \file /src/utils/port.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module for finding a free network port.
============================================

Allows you to find a free port on a specified host either in a given range(s),
or starting from a certain port upwards.

```rst
    .. module:: src.utils.port
```
"""

import socket
from typing import Optional, Union, List, Tuple, TypeVar

import header
from header import __root__
from src.logger import logger

T = TypeVar("T")
PortRangeType = Optional[Union[str, List[Union[str, List[int]]]]]

def get_free_port(port_range: PortRangeType = None, host: str = '127.0.0.1') -> int:
    """!
    Finds and returns a free port in the specified range(s),
    or the first available port if no range is specified.

    Args:
        port_range (PortRangeType, optional): Port range(s).
            Can be a string "min-max", a list of strings "min-max",
            a list of lists of numbers [min, max], or None.
            For example: "3000-3999", ["3000-3999", "8000-8010"], [[4000, 4099], [9000, 9010]].
        host (str, optional): The host's IP address. Defaults to '127.0.0.1'.

    Returns:
        int: The first free port.

    Raises:
        ValueError: If a free port cannot be found or the range format is incorrect.

    Examples:
        >>> get_free_port()  # Finds the first free port from 1024 to 65535
        51023

        >>> get_free_port("3000-3010")
        3002

        >>> get_free_port(["3000-3010", "5000-5010"])
        3001

        >>> get_free_port([[4000, 4010], [6000, 6010]])
        4000
    """

    ranges: List[range] = []

    def _is_port_in_use(port: int) -> bool:
        """Checks if a port is in use on the specified host.

        Args:
            port (int): The port to check.

        Returns:
            bool: True if the port is in use, False if it is free.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return False
            except OSError:
                return True
            except Exception as ex:
                logger.error(f"Error checking port {port} on host {host}", ex, exc_info=True)
                return True

    def _parse_range(r: Union[str, List[int]]) -> Optional[range]:
        """Converts a "min-max" string or [min, max] list to a range.

        Args:
            r (Union[str, List[int]]): The input range.

        Returns:
            Optional[range]: A range object if successful; otherwise None.
        """
        try:
            if isinstance(r, str):
                parts = r.strip().split("-")
                if len(parts) != 2:
                    return None
                start, end = int(parts[0]), int(parts[1])
            elif isinstance(r, list) and len(r) == 2 and all(isinstance(x, int) for x in r):
                start, end = r
            else:
                return None

            if start < 1 or end > 65535 or start >= end:
                return None

            return range(start, end + 1)
        except Exception as ex:
            logger.error(f"Error parsing range: {r}", ex, exc_info=True)
            return None

    match port_range:
        case None:
            port_range:list = [1024,65535]

        case str():
            if not _is_port_in_use(int(port_range)):
                return int(port_range)

            raise ValueError(f"Invalid range format: {port_range}")

        case list():
            for port in port_range:
                if not _is_port_in_use(port):
                    return port
            logger.error(f"Free port not found in range(s): {port_range}")
            return -1
        case _:
            raise ValueError(f"Unsupported port_range type: {type(port_range)}")
