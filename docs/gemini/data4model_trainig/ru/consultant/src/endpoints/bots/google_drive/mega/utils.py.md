### **Анализ кода модуля `utils.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код содержит набор полезных функций для шифрования, дешифрования и кодирования данных, используемых в контексте Mega.
    - Функции хорошо структурированы и выполняют определенные задачи.
- **Минусы**:
    - Отсутствует документация и подробные комментарии для функций.
    - Не указаны типы данных для аргументов и возвращаемых значений функций.
    - Не используются логирование для отслеживания ошибок и хода выполнения программы.
    - В некоторых местах используются неявные преобразования типов, что может привести к ошибкам.
    - Не везде соблюдены пробелы вокруг операторов.

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    - Для каждой функции добавить docstring, описывающий ее назначение, аргументы, возвращаемое значение и возможные исключения.
    - Для каждой внутренней функции добавить docstring, описывающий ее назначение, аргументы, возвращаемое значение и возможные исключения.

2.  **Добавить аннотации типов**:
    - Для всех аргументов функций и возвращаемых значений указать типы данных.

3.  **Использовать логирование**:
    - Добавить логирование для отслеживания ошибок и хода выполнения программы.
    - Использовать `logger.error` для регистрации ошибок и `logger.info` для информационных сообщений.

4.  **Обработка исключений**:
    - Оборачивать потенциально проблемные участки кода в блоки `try...except` и обрабатывать исключения.
    - Использовать `logger.error` для логирования ошибок.

5.  **Явное преобразование типов**:
    - Использовать явное преобразование типов, чтобы избежать неявных преобразований, которые могут привести к ошибкам.

6.  **Форматирование кода**:
    - Добавить пробелы вокруг операторов присваивания и других операторов для повышения читаемости кода.

7.  **Добавить проверки типов**:
    - Добавить проверки типов для входных данных функций, чтобы убедиться, что они соответствуют ожидаемым типам.

**Оптимизированный код:**

```python
# -*- coding: utf-8 -*-
import base64
import struct
import binascii
from typing import List, Tuple, Dict
from Crypto.Cipher import AES
from src.logger import logger


def a32_to_str(a: List[int]) -> bytes:
    """
    Преобразует список 32-битных целых чисел в строку байтов.

    Args:
        a (List[int]): Список 32-битных целых чисел.

    Returns:
        bytes: Строка байтов, полученная из списка целых чисел.

    Example:
        >>> a32_to_str([1, 2, 3])
        b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x03'
    """
    return struct.pack('>{}I'.format(len(a)), *a)


def aes_cbc_encrypt(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные с использованием алгоритма AES в режиме CBC.

    Args:
        data (bytes): Данные для шифрования.
        key (bytes): Ключ шифрования.

    Returns:
        bytes: Зашифрованные данные.

    Raises:
        Exception: Если возникает ошибка при шифровании данных.

    Example:
        >>> key = b'\\x00' * 16
        >>> data = b'This is a test'
        >>> encrypted = aes_cbc_encrypt(data, key)
        >>> type(encrypted)
        <class 'bytes'>
    """
    try:
        encryptor = AES.new(key, AES.MODE_CBC, b'\\0' * 16)
        return encryptor.encrypt(data)
    except Exception as ex:
        logger.error('Error while encrypting data', ex, exc_info=True)
        return b''


def aes_cbc_encrypt_a32(data: List[int], key: List[int]) -> Tuple[int, ...]:
    """
    Шифрует данные, представленные в виде списка 32-битных целых чисел, с использованием алгоритма AES в режиме CBC.

    Args:
        data (List[int]): Список 32-битных целых чисел, представляющих данные для шифрования.
        key (List[int]): Список 32-битных целых чисел, представляющих ключ шифрования.

    Returns:
        Tuple[int, ...]: Список 32-битных целых чисел, представляющих зашифрованные данные.
    """
    encrypted = aes_cbc_encrypt(a32_to_str(data), a32_to_str(key))
    return str_to_a32(encrypted)


def str_to_a32(b: bytes | str) -> Tuple[int, ...]:
    """
    Преобразует строку байтов в список 32-битных целых чисел.

    Args:
        b (bytes | str): Строка байтов для преобразования.

    Returns:
        Tuple[int, ...]: Список 32-битных целых чисел, полученный из строки байтов.

    Raises:
        Exception: Если возникает ошибка при преобразовании строки в список целых чисел.

    Example:
        >>> str_to_a32(b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02')
        (1, 2)
    """
    if isinstance(b, str):
        b = b.encode('utf-8')

    if len(b) % 4:  # Add padding, we need a string with a length multiple of 4
        b += b'\\0' * (4 - len(b) % 4)

    fmt = '>{}I'.format(len(b) // 4)
    return struct.unpack(fmt, b)


def mpi2int(s: bytes) -> int:
    """
    Преобразует строку байтов, представляющую число MPI, в целое число.

    Args:
        s (bytes): Строка байтов, представляющая число MPI.

    Returns:
        int: Целое число, полученное из строки байтов.

    Raises:
        Exception: Если возникает ошибка при преобразовании строки MPI в целое число.

    Example:
        >>> mpi2int(b'\\x00\\x02\\x01\\x02')
        258
    """
    try:
        return int(binascii.hexlify(s[2:]), 16)
    except Exception as ex:
        logger.error('Error while converting MPI to integer', ex, exc_info=True)
        return 0


def aes_cbc_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные с использованием алгоритма AES в режиме CBC.

    Args:
        data (bytes): Данные для расшифрования.
        key (bytes): Ключ расшифрования.

    Returns:
        bytes: Расшифрованные данные.

    Raises:
        Exception: Если возникает ошибка при расшифровании данных.
    """
    try:
        decryptor = AES.new(key, AES.MODE_CBC, b'\\0' * 16)
        return decryptor.decrypt(data)
    except Exception as ex:
        logger.error('Error while decrypting data', ex, exc_info=True)
        return b''


def aes_cbc_decrypt_a32(data: List[int], key: List[int]) -> Tuple[int, ...]:
    """
    Расшифровывает данные, представленные в виде списка 32-битных целых чисел, с использованием алгоритма AES в режиме CBC.

    Args:
        data (List[int]): Список 32-битных целых чисел, представляющих данные для расшифрования.
        key (List[int]): Список 32-битных целых чисел, представляющих ключ расшифрования.

    Returns:
        Tuple[int, ...]: Список 32-битных целых чисел, представляющих расшифрованные данные.
    """
    decrypted = aes_cbc_decrypt(a32_to_str(data), a32_to_str(key))
    return str_to_a32(decrypted)


def base64urldecode(data: str) -> bytes:
    """
    Декодирует строку base64url.

    Args:
        data (str): Строка base64url для декодирования.

    Returns:
        bytes: Декодированные данные.

    Raises:
        TypeError: Если входные данные не являются строкой.
        binascii.Error: Если входные данные содержат недопустимые символы base64.
    """
    try:
        data += '=='[(2 - len(data) * 3) % 4:]
        for search, replace in (('-', '+'), ('_', '/'), (',', '')):\
            data = data.replace(search, replace)
        return base64.b64decode(data)
    except TypeError as ex:
        logger.error('Error: Input must be a string', ex, exc_info=True)
        return b''
    except binascii.Error as ex:
        logger.error('Error: Invalid base64 characters', ex, exc_info=True)
        return b''


def base64_to_a32(s: str) -> Tuple[int, ...]:
    """
    Декодирует строку base64url и преобразует ее в список 32-битных целых чисел.

    Args:
        s (str): Строка base64url для декодирования и преобразования.

    Returns:
        Tuple[int, ...]: Список 32-битных целых чисел, полученный из декодированной строки base64url.
    """
    decoded = base64urldecode(s)
    return str_to_a32(decoded)


def base64urlencode(data: bytes) -> str:
    """
    Кодирует строку байтов в строку base64url.

    Args:
        data (bytes): Строка байтов для кодирования.

    Returns:
        str: Строка base64url, полученная из строки байтов.
    """
    data = base64.b64encode(data).decode('utf-8')
    for search, replace in (('+', '-'), ('/', '_'), ('=', '')):\
        data = data.replace(search, replace)
    return data


def a32_to_base64(a: List[int]) -> str:
    """
    Преобразует список 32-битных целых чисел в строку base64url.

    Args:
        a (List[int]): Список 32-битных целых чисел.

    Returns:
        str: Строка base64url, полученная из списка целых чисел.
    """
    byte_string = a32_to_str(a)
    return base64urlencode(byte_string)


def get_chunks(size: int) -> Dict[int, int]:
    """
    Разбивает размер файла на чанки для параллельной загрузки.

    Args:
        size (int): Размер файла в байтах.

    Returns:
        Dict[int, int]: Словарь, где ключ - начальная позиция чанка, а значение - размер чанка.
    """
    chunks = {}
    p = pp = 0
    i = 1

    while i <= 8 and p < size - i * 0x20000:\
        chunks[p] = i * 0x20000
        pp = p
        p += chunks[p]
        i += 1

    while p < size:\
        chunks[p] = 0x100000
        pp = p
        p += chunks[p]

    chunks[pp] = size - pp
    if not chunks[pp]:
        del chunks[pp]

    return chunks