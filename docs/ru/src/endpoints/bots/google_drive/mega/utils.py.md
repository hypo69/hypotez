# Модуль утилит для работы с MEGA

## Обзор

Модуль содержит набор утилитных функций, используемых для шифрования, дешифрования, кодирования и декодирования данных, необходимых для взаимодействия с сервисом MEGA. Модуль предоставляет функции для преобразования данных между различными форматами, такими как целые числа, строки, массивы 32-битных целых чисел и base64url.

## Подробней

Этот модуль предоставляет инструменты для работы с криптографическими операциями и кодированием данных, специфичными для сервиса MEGA. Он включает функции для шифрования и дешифрования AES, преобразования данных между различными форматами и работы с base64url кодированием.
Модуль используется для подготовки данных к передаче в MEGA и обработки данных, полученных из MEGA.

## Функции

### `a32_to_str`

```python
def a32_to_str(a):
    """Преобразует массив 32-битных целых чисел в строку байтов.

    Args:
        a (list[int]): Массив 32-битных целых чисел.

    Returns:
        str: Строка байтов, полученная из массива `a`.
    """
    ...
```

**Назначение**: Преобразует массив 32-битных целых чисел в строку байтов, используя структуру данных для упаковки.

**Параметры**:
- `a` (list[int]): Массив 32-битных целых чисел, которые необходимо преобразовать в строку.

**Возвращает**:
- `str`: Строка байтов, полученная из массива `a`.

**Как работает функция**:
- Функция использует `struct.pack` для упаковки каждого 32-битного целого числа из массива `a` в строку байтов.
- `>%dI` указывает формат упаковки: `>` означает big-endian порядок байтов, `%d` - количество целых чисел, `I` - 32-битное целое число без знака.

**Примеры**:

```python
>>> a32_to_str([1, 2, 3])
b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x03'
```

### `aes_cbc_encrypt`

```python
def aes_cbc_encrypt(data, key):
    """Шифрует данные с использованием AES в режиме CBC.

    Args:
        data (bytes): Данные для шифрования.
        key (bytes): Ключ шифрования.

    Returns:
        bytes: Зашифрованные данные.
    """
    ...
```

**Назначение**: Шифрует данные с использованием алгоритма AES в режиме CBC (Cipher Block Chaining).

**Параметры**:
- `data` (bytes): Данные для шифрования.
- `key` (bytes): Ключ шифрования.

**Возвращает**:
- `bytes`: Зашифрованные данные.

**Как работает функция**:
- Создается объект шифрования AES с использованием ключа `key`, режима CBC и вектора инициализации (IV), заполненного нулями.
- Функция `encrypt` объекта шифрования используется для шифрования входных данных `data`.

**Примеры**:

```python
>>> key = b'\\x00' * 16
>>> data = b'some_data'
>>> aes_cbc_encrypt(data, key)
b'J\\xb7\\xa5\\x07\\xbb\\x84\\xbb\\xf6\\xdb\\xe2\\xcd\\xbb\\x8b\\x1b\\x9b\\x08'
```

### `aes_cbc_encrypt_a32`

```python
def aes_cbc_encrypt_a32(data, key):
    """Шифрует массив 32-битных целых чисел с использованием AES в режиме CBC.

    Args:
        data (list[int]): Массив 32-битных целых чисел для шифрования.
        key (list[int]): Ключ шифрования в виде массива 32-битных целых чисел.

    Returns:
        list[int]: Зашифрованный массив 32-битных целых чисел.
    """
    ...
```

**Назначение**: Шифрует данные, представленные в виде массива 32-битных целых чисел, используя AES в режиме CBC.

**Параметры**:
- `data` (list[int]): Массив 32-битных целых чисел для шифрования.
- `key` (list[int]): Ключ шифрования в виде массива 32-битных целых чисел.

**Возвращает**:
- `list[int]`: Зашифрованный массив 32-битных целых чисел.

**Как работает функция**:
- Преобразует входные массивы `data` и `key` в строки байтов с помощью `a32_to_str`.
- Шифрует полученную строку байтов с помощью `aes_cbc_encrypt`.
- Преобразует зашифрованную строку байтов обратно в массив 32-битных целых чисел с помощью `str_to_a32`.

**Примеры**:

```python
>>> key = [0] * 4
>>> data = [1, 2, 3]
>>> aes_cbc_encrypt_a32(data, key)
(2344967756, 3182882717, 3254461372)
```

### `str_to_a32`

```python
def str_to_a32(b):
    """Преобразует строку байтов в массив 32-битных целых чисел.

    Args:
        b (bytes): Строка байтов для преобразования.

    Returns:
        tuple[int]: Массив 32-битных целых чисел.
    """
    ...
```

**Назначение**: Преобразует строку байтов в массив 32-битных целых чисел.

**Параметры**:
- `b` (bytes): Строка байтов для преобразования.

**Возвращает**:
- `tuple[int]`: Массив 32-битных целых чисел.

**Как работает функция**:
- Дополняет строку `b` нулями, если её длина не кратна 4.
- Если тип `b` является строкой, преобразует её в байты, используя кодировку UTF-8.
- Использует `struct.unpack` для преобразования строки байтов в массив 32-битных целых чисел.

**Примеры**:

```python
>>> str_to_a32(b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02')
(1, 2)
```

### `mpi2int`

```python
def mpi2int(s):
    """Преобразует строку, содержащую MPI (Multi-Precision Integer), в целое число.

    Args:
        s (bytes): Строка, содержащая MPI.

    Returns:
        int: Целое число, полученное из MPI.
    """
    ...
```

**Назначение**: Преобразует строку, содержащую MPI (Multi-Precision Integer), в целое число. MPI - это формат представления больших целых чисел, используемый в криптографии.

**Параметры**:
- `s` (bytes): Строка, содержащая MPI. Первые два байта строки указывают длину числа.

**Возвращает**:
- `int`: Целое число, полученное из MPI.

**Как работает функция**:
- Извлекает данные, начиная с третьего байта (`s[2:]`).
- Преобразует строку байтов в шестнадцатеричное представление с помощью `binascii.hexlify`.
- Преобразует шестнадцатеричное представление в целое число с помощью `int(..., 16)`.

**Примеры**:

```python
>>> mpi2int(b'\\x00\\x04\\x01\\x02\\x03\\x04')
16909060
```

### `aes_cbc_decrypt`

```python
def aes_cbc_decrypt(data, key):
    """Дешифрует данные с использованием AES в режиме CBC.

    Args:
        data (bytes): Данные для дешифрования.
        key (bytes): Ключ дешифрования.

    Returns:
        bytes: Дешифрованные данные.
    """
    ...
```

**Назначение**: Дешифрует данные с использованием алгоритма AES в режиме CBC (Cipher Block Chaining).

**Параметры**:
- `data` (bytes): Данные для дешифрования.
- `key` (bytes): Ключ дешифрования.

**Возвращает**:
- `bytes`: Дешифрованные данные.

**Как работает функция**:
- Создает объект дешифрования AES с использованием ключа `key`, режима CBC и вектора инициализации (IV), заполненного нулями.
- Функция `decrypt` объекта дешифрования используется для дешифрования входных данных `data`.

**Примеры**:

```python
>>> key = b'\\x00' * 16
>>> data = b'J\\xb7\\xa5\\x07\\xbb\\x84\\xbb\\xf6\\xdb\\xe2\\xcd\\xbb\\x8b\\x1b\\x9b\\x08'
>>> aes_cbc_decrypt(data, key)
b'some_data\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10'
```

### `aes_cbc_decrypt_a32`

```python
def aes_cbc_decrypt_a32(data, key):
    """Дешифрует массив 32-битных целых чисел с использованием AES в режиме CBC.

    Args:
        data (list[int]): Массив 32-битных целых чисел для дешифрования.
        key (list[int]): Ключ дешифрования в виде массива 32-битных целых чисел.

    Returns:
        list[int]: Дешифрованный массив 32-битных целых чисел.
    """
    ...
```

**Назначение**: Дешифрует данные, представленные в виде массива 32-битных целых чисел, используя AES в режиме CBC.

**Параметры**:
- `data` (list[int]): Массив 32-битных целых чисел для дешифрования.
- `key` (list[int]): Ключ дешифрования в виде массива 32-битных целых чисел.

**Возвращает**:
- `list[int]`: Дешифрованный массив 32-битных целых чисел.

**Как работает функция**:
- Преобразует входные массивы `data` и `key` в строки байтов с помощью `a32_to_str`.
- Дешифрует полученную строку байтов с помощью `aes_cbc_decrypt`.
- Преобразует дешифрованную строку байтов обратно в массив 32-битных целых чисел с помощью `str_to_a32`.

**Примеры**:

```python
>>> key = [0] * 4
>>> data = (2344967756, 3182882717, 3254461372)
>>> aes_cbc_decrypt_a32(data, key)
(1, 2, 3, 0)
```

### `base64urldecode`

```python
def base64urldecode(data):
    """Декодирует строку в формате base64url.

    Args:
        data (str): Строка для декодирования.

    Returns:
        bytes: Декодированные данные.
    """
    ...
```

**Назначение**: Декодирует строку, закодированную в формате base64url. Base64url - это вариант base64, в котором символы `+` и `/` заменены на `-` и `_` соответственно, а символ `=` (padding) удален.

**Параметры**:
- `data` (str): Строка для декодирования.

**Возвращает**:
- `bytes`: Декодированные данные.

**Как работает функция**:
- Добавляет padding (`=`) к строке `data`, чтобы её длина была кратна 4.
- Заменяет символы `-`, `_` и `,` на `+`, `/` и `''` соответственно.
- Декодирует полученную строку с помощью `base64.b64decode`.

**Примеры**:

```python
>>> base64urldecode('AQAB')
b'\\x01\\x00\\x01'
```

### `base64_to_a32`

```python
def base64_to_a32(s):
    """Декодирует строку base64url и преобразует её в массив 32-битных целых чисел.

    Args:
        s (str): Строка base64url для преобразования.

    Returns:
        tuple[int]: Массив 32-битных целых чисел.
    """
    ...
```

**Назначение**: Декодирует строку, закодированную в формате base64url, и преобразует её в массив 32-битных целых чисел.

**Параметры**:
- `s` (str): Строка base64url для преобразования.

**Возвращает**:
- `tuple[int]`: Массив 32-битных целых чисел.

**Как работает функция**:
- Декодирует входную строку `s` из формата base64url с помощью `base64urldecode`.
- Преобразует полученную строку байтов в массив 32-битных целых чисел с помощью `str_to_a32`.

**Примеры**:

```python
>>> base64_to_a32('AQAB')
(167772161,)
```

### `base64urlencode`

```python
def base64urlencode(data):
    """Кодирует данные в формат base64url.

    Args:
        data (bytes): Данные для кодирования.

    Returns:
        str: Строка, закодированная в формате base64url.
    """
    ...
```

**Назначение**: Кодирует данные в формат base64url.

**Параметры**:
- `data` (bytes): Данные для кодирования.

**Возвращает**:
- `str`: Строка, закодированная в формате base64url.

**Как работает функция**:
- Кодирует входные данные `data` в base64 с помощью `base64.b64encode`.
- Декодирует полученную строку байтов в строку UTF-8.
- Заменяет символы `+`, `/` и `=` на `-`, `_` и `''` соответственно.

**Примеры**:

```python
>>> base64urlencode(b'\\x01\\x00\\x01')
'AQAB'
```

### `a32_to_base64`

```python
def a32_to_base64(a):
    """Преобразует массив 32-битных целых чисел в строку base64url.

    Args:
        a (list[int]): Массив 32-битных целых чисел для преобразования.

    Returns:
        str: Строка base64url.
    """
    ...
```

**Назначение**: Преобразует массив 32-битных целых чисел в строку, закодированную в формате base64url.

**Параметры**:
- `a` (list[int]): Массив 32-битных целых чисел для преобразования.

**Возвращает**:
- `str`: Строка base64url.

**Как работает функция**:
- Преобразует входной массив `a` в строку байтов с помощью `a32_to_str`.
- Кодирует полученную строку байтов в base64url с помощью `base64urlencode`.

**Примеры**:

```python
>>> a32_to_base64((167772161,))
'AQAB'
```

### `get_chunks`

```python
def get_chunks(size):
    """Разбивает размер файла на чанки для скачивания.

    Args:
        size (int): Размер файла в байтах.

    Returns:
        dict[int, int]: Словарь, где ключ - начальная позиция чанка, а значение - его размер.
    """
    ...
```

**Назначение**: Разбивает размер файла на чанки для скачивания, оптимизируя процесс скачивания больших файлов.

**Параметры**:
- `size` (int): Размер файла в байтах.

**Возвращает**:
- `dict[int, int]`: Словарь, где ключ - начальная позиция чанка, а значение - его размер.

**Как работает функция**:
- Функция разбивает файл на чанки разных размеров, чтобы оптимизировать процесс скачивания.
- Сначала создаются чанки размером, кратным `0x20000`, до максимального размера `8 * 0x20000`.
- Затем создаются чанки размером `0x100000` до тех пор, пока не будет достигнут конец файла.
- Последний чанк содержит оставшуюся часть файла.
- Возвращается словарь, где ключи - начальные позиции чанков, а значения - их размеры.

**Примеры**:

```python
>>> get_chunks(500000)
{0: 131072, 131072: 262144, 393216: 106784}