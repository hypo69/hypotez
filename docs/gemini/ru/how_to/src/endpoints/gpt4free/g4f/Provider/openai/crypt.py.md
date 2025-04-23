### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный блок кода реализует функции шифрования и дешифрования данных с использованием алгоритма AES и хеширования MD5 для генерации ключей и векторов инициализации (IV). Он также включает функции для дополнения и удаления дополнения, чтобы обеспечить правильную длину данных для шифрования.

Шаги выполнения
-------------------------
1. **`pad(data: str) -> bytes`**:
   - Функция принимает строку (`data`) в качестве входных данных.
   - Преобразует строку в байты.
   - Вычисляет, сколько байтов необходимо добавить, чтобы длина данных была кратна 16 (размер блока AES).
   - Добавляет байты заполнения в конец данных, где каждый байт заполнения имеет значение, равное количеству добавленных байтов.
   - Возвращает дополненные байты.

2. **`encrypt(data: str, key: str) -> str`**:
   - Функция принимает строку (`data`) для шифрования и ключ (`key`) в виде строки.
   - Генерирует случайную "соль" (`salt`) длиной 8 символов.
   - Использует MD5 хеширование в цикле для создания `salted` ключа и IV.
   - Дополняет данные с помощью функции `pad`.
   - Инициализирует объект AES с использованием сгенерированного ключа и IV.
   - Шифрует дополненные данные с использованием AES в режиме CBC.
   - Кодирует зашифрованные данные в base64.
   - Формирует JSON-объект, содержащий зашифрованные данные (`ct`), IV и соль (`s`).
   - Возвращает JSON-строку.

3. **`unpad(data: bytes) -> bytes`**:
   - Функция принимает байты (`data`) в качестве входных данных.
   - Извлекает значение последнего байта, которое указывает на количество байтов заполнения.
   - Удаляет байты заполнения с конца данных.
   - Возвращает очищенные от заполнения байты.

4. **`decrypt(data: str, key: str) -> str`**:
   - Функция принимает строку (`data`) в формате JSON (зашифрованные данные) и ключ (`key`) в виде строки.
   - Декодирует строку `data` из base64.
   - Извлекает зашифрованные данные (`ct`), IV и соль (`s`) из JSON.
   - Использует MD5 хеширование в цикле для создания `salted` ключа и IV на основе ключа и соли.
   - Инициализирует объект AES с использованием сгенерированного ключа и IV.
   - Дешифрует данные с использованием AES в режиме CBC.
   - Удаляет дополнение с помощью функции `unpad`.
   - Декодирует байты в строку и возвращает её.

Пример использования
-------------------------

```python
import json
import base64
import hashlib
import random
from Crypto.Cipher import AES

def pad(data: str) -> bytes:
    data_bytes = data.encode()
    padding = 16 - (len(data_bytes) % 16)
    return data_bytes + bytes([padding] * padding)

def encrypt(data, key):
    salt = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(8))
    salted = ""
    dx = bytes()

    for x in range(3):
        dx = hashlib.md5(dx + key.encode() + salt.encode()).digest()
        salted += dx.hex()

    data = pad(data)

    aes = AES.new(
        bytes.fromhex(salted[:64]), AES.MODE_CBC, bytes.fromhex(salted[64:96])
    )

    return json.dumps(
        {
            "ct": base64.b64encode(aes.encrypt(data)).decode(),
            "iv": salted[64:96],
            "s": salt.encode().hex(),
        }
    )

def unpad(data: bytes) -> bytes:
    padding_value = data[-1]
    return data[:-padding_value]

def decrypt(data: str, key: str):
    parsed_data = json.loads(base64.b64decode(data))
    ct = base64.b64decode(parsed_data["ct"])
    iv = bytes.fromhex(parsed_data["iv"])
    salt = bytes.fromhex(parsed_data["s"])

    salted = ''
    dx = b''
    for x in range(3):
        dx = hashlib.md5(dx + key.encode() + salt).digest()
        salted += dx.hex()
        
    aes = AES.new(
        bytes.fromhex(salted[:64]), AES.MODE_CBC, iv
    )

    data = aes.decrypt(ct)
    if data.startswith(b'[{"key":'):
        return unpad(data).decode()

# Пример использования
key = "my_secret_key"
data = '[{"key": "value"}]'

encrypted_data = encrypt(data, key)
print(f"Зашифрованные данные: {encrypted_data}")

decrypted_data = decrypt(encrypted_data, key)
print(f"Расшифрованные данные: {decrypted_data}")