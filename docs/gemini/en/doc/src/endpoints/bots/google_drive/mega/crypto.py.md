# Модуль `crypto`

## Обзор

Модуль `crypto` предоставляет функции для шифрования и дешифрования данных с использованием алгоритма AES в режиме CBC. 

## Детали

Модуль используется для шифрования и дешифрования данных, связанных с Google Drive, в Mega. Он содержит функции для шифрования и дешифрования ключей, атрибутов и других данных, используя алгоритм AES в режиме CBC.

## Функции

### `aes_cbc_encrypt(data, key)`

**Описание**: Функция шифрует данные с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `data` (bytes): Данные, которые необходимо зашифровать.
- `key` (bytes): Ключ для шифрования.

**Возвращает**:

- bytes: Зашифрованные данные.

### `aes_cbc_decrypt(data, key)`

**Описание**: Функция дешифрует данные, зашифрованные с помощью `aes_cbc_encrypt`.

**Параметры**:

- `data` (bytes): Зашифрованные данные.
- `key` (bytes): Ключ для дешифрования.

**Возвращает**:

- bytes: Дешифрованные данные.

### `aes_cbc_encrypt_a32(data, key)`

**Описание**: Функция шифрует данные в формате `a32` с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `data` (list): Данные, которые необходимо зашифровать в формате `a32`.
- `key` (list): Ключ для шифрования в формате `a32`.

**Возвращает**:

- list: Зашифрованные данные в формате `a32`.

### `aes_cbc_decrypt_a32(data, key)`

**Описание**: Функция дешифрует данные в формате `a32`, зашифрованные с помощью `aes_cbc_encrypt_a32`.

**Параметры**:

- `data` (list): Зашифрованные данные в формате `a32`.
- `key` (list): Ключ для дешифрования в формате `a32`.

**Возвращает**:

- list: Дешифрованные данные в формате `a32`.

### `stringhash(s, aeskey)`

**Описание**: Функция вычисляет хэш-сумму строки с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `s` (str): Строка, для которой необходимо вычислить хэш-сумму.
- `aeskey` (list): Ключ для шифрования в формате `a32`.

**Возвращает**:

- str: Хэш-сумма строки в формате Base64.

### `prepare_key(a)`

**Описание**: Функция подготавливает ключ для шифрования, выполняя серию операций шифрования с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `a` (list): Исходный ключ в формате `a32`.

**Возвращает**:

- list: Подготовленный ключ в формате `a32`.

### `encrypt_key(a, key)`

**Описание**: Функция шифрует ключ с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `a` (list): Ключ, который необходимо зашифровать в формате `a32`.
- `key` (list): Ключ для шифрования в формате `a32`.

**Возвращает**:

- list: Зашифрованный ключ в формате `a32`.

### `decrypt_key(a, key)`

**Описание**: Функция дешифрует ключ, зашифрованный с помощью `encrypt_key`.

**Параметры**:

- `a` (list): Зашифрованный ключ в формате `a32`.
- `key` (list): Ключ для дешифрования в формате `a32`.

**Возвращает**:

- list: Дешифрованный ключ в формате `a32`.

### `enc_attr(attr, key)`

**Описание**: Функция шифрует атрибуты с использованием алгоритма AES в режиме CBC.

**Параметры**:

- `attr` (dict): Словарь, содержащий атрибуты, которые необходимо зашифровать.
- `key` (list): Ключ для шифрования в формате `a32`.

**Возвращает**:

- bytes: Зашифрованные атрибуты.

### `dec_attr(attr, key)`

**Описание**: Функция дешифрует атрибуты, зашифрованные с помощью `enc_attr`.

**Параметры**:

- `attr` (bytes): Зашифрованные атрибуты.
- `key` (list): Ключ для дешифрования в формате `a32`.

**Возвращает**:

- dict: Дешифрованные атрибуты.