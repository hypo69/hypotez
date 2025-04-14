# Модуль crypto.py

## Обзор

Модуль `crypto.py` содержит функции для шифрования и дешифрования данных, используемых в MEGA. Он включает в себя реализацию AES-CBC шифрования, хеширования строк и подготовки ключей.

## Подробней

Этот модуль предоставляет набор криптографических функций, необходимых для безопасной обработки данных в контексте работы с MEGA. Он включает в себя функции для шифрования и дешифрования с использованием алгоритма AES в режиме CBC, а также функции для подготовки и обработки ключей.

## Функции

### `aes_cbc_encrypt`

```python
def aes_cbc_encrypt(data, key):
    """Шифрует данные с использованием алгоритма AES в режиме CBC.

    Args:
        data (bytes): Данные для шифрования.
        key (bytes): Ключ шифрования.

    Returns:
        bytes: Зашифрованные данные.

    Raises:
        Отсутствуют.
    """
    encryptor = AES.new(key, AES.MODE_CBC, '\\0' * 16)
    return encryptor.encrypt(data)
```

### `aes_cbc_decrypt`

```python
def aes_cbc_decrypt(data, key):
    """Дешифрует данные, зашифрованные с использованием алгоритма AES в режиме CBC.

    Args:
        data (bytes): Зашифрованные данные.
        key (bytes): Ключ шифрования.

    Returns:
        bytes: Дешифрованные данные.

    Raises:
        Отсутствуют.
    """
    decryptor = AES.new(key, AES.MODE_CBC, '\\0' * 16)
    return decryptor.decrypt(data)
```

### `aes_cbc_encrypt_a32`

```python
def aes_cbc_encrypt_a32(data, key):
    """Шифрует данные в формате a32 с использованием алгоритма AES в режиме CBC.

    Args:
        data (list[int]): Данные для шифрования в формате a32.
        key (list[int]): Ключ шифрования в формате a32.

    Returns:
        list[int]: Зашифрованные данные в формате a32.

    Raises:
        Отсутствуют.
    """
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))
```

### `aes_cbc_decrypt_a32`

```python
def aes_cbc_decrypt_a32(data, key):
    """Дешифрует данные в формате a32, зашифрованные с использованием алгоритма AES в режиме CBC.

    Args:
        data (list[int]): Зашифрованные данные в формате a32.
        key (list[int]): Ключ шифрования в формате a32.

    Returns:
        list[int]: Дешифрованные данные в формате a32.

    Raises:
        Отсутствуют.
    """
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))
```

### `stringhash`

```python
def stringhash(s, aeskey):
    """Вычисляет хеш строки с использованием AES-CBC.

    Args:
        s (str): Строка для хеширования.
        aeskey (list[int]): Ключ AES.

    Returns:
        str: Хеш строки в формате base64.

    Raises:
        Отсутствуют.
    """
    s32 = str_to_a32(s)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for _ in range(0x4000):
        h32 = aes_cbc_encrypt_a32(h32, aeskey)
    return a32_to_base64((h32[0], h32[2]))
```
**Как работает функция**:
1. Преобразует входную строку `s` в формат `a32` (список 32-битных целых чисел).
2. Инициализирует список `h32` нулями, который будет использоваться для хранения хеша.
3. Итерируется по каждому элементу в `s32` и выполняет операцию XOR между элементом и соответствующим элементом в `h32`.
4. Выполняет 0x4000 итераций AES-CBC шифрования списка `h32` с использованием ключа `aeskey`.
5. Преобразует первые два элемента списка `h32` в формат base64 и возвращает результат.

**Примеры**:
```python
aeskey = [1, 2, 3, 4]
string = "example"
stringhash(string, aeskey) # Пример вызова функции
```

### `prepare_key`

```python
def prepare_key(a):
    """Подготавливает ключ для шифрования.

    Args:
        a (list[int]): Список целых чисел для подготовки ключа.

    Returns:
        list[int]: Подготовленный ключ.

    Raises:
        Отсутствуют.
    """
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for _ in range(0x10000):
        for j in range(0, len(a), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(a):
                    key[i] = a[i + j]
            pkey = aes_cbc_encrypt_a32(pkey, key)
    return pkey
```
**Как работает функция**:
1. Инициализирует список `pkey` константами.
2. Выполняет 0x10000 итераций.
3. В каждой итерации проходит по списку `a` с шагом 4.
4. Создает список `key` из 4 элементов, беря элементы из списка `a`.
5. Шифрует `pkey` с использованием AES-CBC с ключом `key`.
6. Возвращает `pkey`.

**Примеры**:
```python
key_data = [1, 2, 3, 4, 5, 6, 7, 8]
prepare_key(key_data) # Пример вызова функции
```

### `encrypt_key`

```python
def encrypt_key(a, key):
    """Шифрует ключ с использованием AES-CBC.

    Args:
        a (list[int]): Ключ для шифрования.
        key (list[int]): Ключ шифрования.

    Returns:
        list[int]: Зашифрованный ключ.

    Raises:
        Отсутствуют.
    """
    return sum(
        (aes_cbc_encrypt_a32(a[i:i+4], key)
            for i in range(0, len(a), 4)), ())\
```
**Как работает функция**:
1. Использует генератор списков для шифрования каждой 4-байтовой части списка `a` с помощью AES-CBC и ключа `key`.
2. Суммирует результаты шифрования в один список и возвращает его.

**Примеры**:
```python
key_to_encrypt = [1, 2, 3, 4, 5, 6, 7, 8]
encryption_key = [9, 10, 11, 12]
encrypt_key(key_to_encrypt, encryption_key) # Пример вызова функции
```

### `decrypt_key`

```python
def decrypt_key(a, key):
    """Дешифрует ключ с использованием AES-CBC.

    Args:
        a (list[int]): Зашифрованный ключ.
        key (list[int]): Ключ шифрования.

    Returns:
        list[int]: Дешифрованный ключ.

    Raises:
        Отсутствуют.
    """
    return sum(
        (aes_cbc_decrypt_a32(a[i:i+4], key)
            for i in range(0, len(a), 4)), ())
```
**Как работает функция**:
1. Использует генератор списков для дешифрования каждой 4-байтовой части списка `a` с помощью AES-CBC и ключа `key`.
2. Суммирует результаты дешифрования в один список и возвращает его.

**Примеры**:
```python
encrypted_key = [1, 2, 3, 4, 5, 6, 7, 8]
decryption_key = [9, 10, 11, 12]
decrypt_key(encrypted_key, decryption_key) # Пример вызова функции
```

### `enc_attr`

```python
def enc_attr(attr, key):
    """Шифрует атрибуты с использованием AES-CBC.

    Args:
        attr (dict): Атрибуты для шифрования.
        key (list[int]): Ключ шифрования.

    Returns:
        bytes: Зашифрованные атрибуты.

    Raises:
        Отсутствуют.
    """
    attr = 'MEGA' + json.dumps(attr)
    if len(attr) % 16:
        attr += '\\0' * (16 - len(attr) % 16)
    return aes_cbc_encrypt(attr, a32_to_str(key))
```
**Как работает функция**:
1. Преобразует атрибуты `attr` в JSON-строку и добавляет префикс 'MEGA'.
2. Дополняет строку нулями до кратной длины 16 байтам.
3. Шифрует строку с использованием AES-CBC и ключа `key`.

**Примеры**:
```python
attributes = {'name': 'example', 'size': 1024}
encryption_key = [1, 2, 3, 4]
enc_attr(attributes, encryption_key) # Пример вызова функции
```

### `dec_attr`

```python
def dec_attr(attr, key):
    """Дешифрует атрибуты, зашифрованные с использованием AES-CBC.

    Args:
        attr (bytes): Зашифрованные атрибуты.
        key (list[int]): Ключ шифрования.

    Returns:
        dict: Дешифрованные атрибуты.

    Raises:
        Отсутствуют.
    """
    attr = aes_cbc_decrypt(attr, a32_to_str(key)).decode('utf-8').rstrip('\\0')
    return json.loads(attr[4:])
```
**Как работает функция**:
1. Дешифрует атрибуты `attr` с использованием AES-CBC и ключа `key`.
2. Удаляет добавленные нули и префикс 'MEGA'.
3. Преобразует JSON-строку в словарь и возвращает его.

**Примеры**:
```python
encrypted_attributes = b'...'  # Зашифрованные атрибуты
decryption_key = [1, 2, 3, 4]
dec_attr(encrypted_attributes, decryption_key) # Пример вызова функции