### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор функций для шифрования и дешифрования данных, используемых в Mega.co.nz. Он включает в себя функции для AES-шифрования в режиме CBC, хеширования строк, подготовки ключей и шифрования/дешифрования атрибутов.

Шаги выполнения
-------------------------
1. **Шифрование AES в режиме CBC:**
   - Используйте `aes_cbc_encrypt(data, key)` для шифрования данных с использованием AES в режиме CBC с заданным ключом.
   - Функция `aes_cbc_encrypt` принимает данные и ключ, создает объект шифрования AES, и возвращает зашифрованные данные.

2. **Дешифрование AES в режиме CBC:**
   - Используйте `aes_cbc_decrypt(data, key)` для дешифрования данных, зашифрованных с использованием AES в режиме CBC с заданным ключом.
   - Функция `aes_cbc_decrypt` принимает зашифрованные данные и ключ, создает объект дешифрования AES, и возвращает расшифрованные данные.

3. **Шифрование AES в режиме CBC для 32-битных данных:**
   - Используйте `aes_cbc_encrypt_a32(data, key)` для шифрования 32-битных данных с использованием AES в режиме CBC.
   - Функция `aes_cbc_encrypt_a32` принимает 32-битные данные и ключ, преобразует их в строки, шифрует данные, и возвращает результат в виде 32-битных данных.

4. **Дешифрование AES в режиме CBC для 32-битных данных:**
   - Используйте `aes_cbc_decrypt_a32(data, key)` для дешифрования 32-битных данных, зашифрованных с использованием AES в режиме CBC.
   - Функция `aes_cbc_decrypt_a32` принимает 32-битные зашифрованные данные и ключ, преобразует их в строки, дешифрует данные, и возвращает результат в виде 32-битных данных.

5. **Хеширование строки:**
   - Используйте `stringhash(s, aeskey)` для создания хеша строки с использованием AES-ключа.
   - Функция `stringhash` принимает строку и AES-ключ, преобразует строку в 32-битный формат, выполняет XOR-операции, шифрует результат, и возвращает хеш в формате Base64.

6. **Подготовка ключа:**
   - Используйте `prepare_key(a)` для подготовки ключа на основе заданного массива.
   - Функция `prepare_key` принимает массив, выполняет итерации и шифрует промежуточные ключи с использованием AES в режиме CBC, и возвращает подготовленный ключ.

7. **Шифрование ключа:**
   - Используйте `encrypt_key(a, key)` для шифрования массива с использованием заданного ключа.
   - Функция `encrypt_key` принимает массив и ключ, шифрует каждый блок массива с использованием AES в режиме CBC, и возвращает зашифрованный ключ.

8. **Дешифрование ключа:**
   - Используйте `decrypt_key(a, key)` для дешифрования массива с использованием заданного ключа.
   - Функция `decrypt_key` принимает массив и ключ, дешифрует каждый блок массива с использованием AES в режиме CBC, и возвращает расшифрованный ключ.

9. **Шифрование атрибутов:**
   - Используйте `enc_attr(attr, key)` для шифрования атрибутов с использованием заданного ключа.
   - Функция `enc_attr` принимает атрибуты и ключ, добавляет префикс 'MEGA', преобразует атрибуты в JSON, дополняет строку до кратной 16 байтам, шифрует строку с использованием AES в режиме CBC, и возвращает зашифрованные атрибуты.

10. **Дешифрование атрибутов:**
    - Используйте `dec_attr(attr, key)` для дешифрования атрибутов с использованием заданного ключа.
    - Функция `dec_attr` принимает зашифрованные атрибуты и ключ, дешифрует строку с использованием AES в режиме CBC, удаляет префикс 'MEGA', преобразует JSON-строку в объект, и возвращает расшифрованные атрибуты.

Пример использования
-------------------------

```python
import json

from Crypto.Cipher import AES

from mega.utils import a32_to_str, str_to_a32, a32_to_base64

def aes_cbc_encrypt(data, key):
    encryptor = AES.new(key, AES.MODE_CBC, '\\0' * 16)
    return encryptor.encrypt(data)

def aes_cbc_decrypt(data, key):
    decryptor = AES.new(key, AES.MODE_CBC, '\\0' * 16)
    return decryptor.decrypt(data)

def aes_cbc_encrypt_a32(data, key):
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))

def aes_cbc_decrypt_a32(data, key):
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))

def stringhash(s, aeskey):
    s32 = str_to_a32(s)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for _ in range(0x4000):
        h32 = aes_cbc_encrypt_a32(h32, aeskey)
    return a32_to_base64((h32[0], h32[2]))

def prepare_key(a):
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for _ in range(0x10000):
        for j in range(0, len(a), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(a):
                    key[i] = a[i + j]
            pkey = aes_cbc_encrypt_a32(pkey, key)
    return pkey

def encrypt_key(a, key):
    return sum(
        (aes_cbc_encrypt_a32(a[i:i+4], key)
            for i in range(0, len(a), 4)), ())

def decrypt_key(a, key):
    return sum(
        (aes_cbc_decrypt_a32(a[i:i+4], key)
            for i in range(0, len(a), 4)), ())

def enc_attr(attr, key):
    attr = 'MEGA' + json.dumps(attr)
    if len(attr) % 16:
        attr += '\\0' * (16 - len(attr) % 16)
    return aes_cbc_encrypt(attr, a32_to_str(key))

def dec_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key)).decode('utf-8').rstrip('\\0')
    return json.loads(attr[4:])

# Пример использования функций
key = b'\\0' * 16  # 16-байтовый ключ
data = b'This is a test'
encrypted_data = aes_cbc_encrypt(data, key)
print(f"Зашифрованные данные: {encrypted_data}")

decrypted_data = aes_cbc_decrypt(encrypted_data, key)
print(f"Расшифрованные данные: {decrypted_data.decode('utf-8')}")

# Пример использования enc_attr и dec_attr
attributes = {"name": "test", "value": 123}
key_a32 = str_to_a32(b'\\0' * 16)
encrypted_attr = enc_attr(attributes, key_a32)
print(f"Зашифрованные атрибуты: {encrypted_attr}")

decrypted_attr = dec_attr(encrypted_attr, key_a32)
print(f"Расшифрованные атрибуты: {decrypted_attr}")