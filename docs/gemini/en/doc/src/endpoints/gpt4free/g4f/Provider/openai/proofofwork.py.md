# Module for generating Proof-of-Work tokens
## Overview

This module provides functionality for generating Proof-of-Work tokens, used to verify the client's computational effort. It includes functions for creating tokens based on provided seeds, difficulty levels, and user agents. The module is designed to be used in systems requiring verification of client-side processing, such as preventing abuse or ensuring fair resource allocation.

## More details

This module is essential for systems that need to verify the computational work done by the client. Proof-of-Work tokens are generated based on parameters such as seed, difficulty, and user agent. The tokens are generated using a hashing algorithm (SHA3-512) and are validated based on the specified difficulty. If the required number of iterations is reached without finding a suitable hash, a fallback token is generated.

## Functions

### `generate_proof_token`

```python
def generate_proof_token(required: bool, seed: str = "", difficulty: str = "", user_agent: str = None, proof_token: str = None) -> str | None:
    """ Функция генерирует Proof-of-Work токен для подтверждения вычислительной работы клиента.

    Args:
        required (bool): Указывает, требуется ли генерация токена. Если `False`, функция не выполняет никаких действий и возвращает `None`.
        seed (str, optional): Исходная строка, используемая для генерации токена. По умолчанию "".
        difficulty (str, optional): Строка, определяющая сложность вычисления.  Хэш должен начинаться с этой строки. По умолчанию "".
        user_agent (str, optional): User agent клиента, который включается в токен. По умолчанию `None`.
        proof_token (str, optional): Если предоставлен, используется как основа для генерации нового токена. По умолчанию `None`.

    Returns:
        str | None: Возвращает Proof-of-Work токен в виде строки, если `required` истинно. Если `required` ложно, возвращает `None`.

    Raises:
        Нет особых исключений.

    Example:
        >>> generate_proof_token(required=True, seed="test_seed", difficulty="000")
        'gAAAAAB...'
    """
    ...
```

#### Parameters:

- `required` (bool): Определяет, необходимо ли генерировать токен. Если `False`, функция не выполняет генерацию.
- `seed` (str): Исходная строка, используемая в процессе хеширования для генерации токена.
- `difficulty` (str): Строка, определяющая сложность. Чем длиннее строка, тем сложнее задача PoW.
- `user_agent` (str): User agent клиента, включаемый в структуру токена.
- `proof_token` (str): Если передан, используется как шаблон для создания нового токена.

#### How the function works:

1. **Проверка необходимости**:
   - Функция начинает с проверки параметра `required`. Если `required` равен `False`, функция немедленно возвращает `None`.
2. **Инициализация `proof_token`**:
   - Если `proof_token` не передан, он генерируется случайным образом. В противном случае используется переданный `proof_token`.
3. **Цикл вычислений**:
   - Функция выполняет цикл до 100000 итераций.
   - На каждой итерации:
     - Устанавливается значение `proof_token[3]` равным текущему индексу итерации `i`.
     - Преобразует массив `proof_token` в JSON-строку, кодирует её в Base64 и декодирует обратно в строку.
     - Вычисляет SHA3-512 хэш от конкатенации `seed` и полученной строки Base64.
     - Проверяет, начинается ли шестнадцатеричное представление хэша с заданной `difficulty`.
     - Если условие выполнено, возвращает строку, начинающуюся с "gAAAAAB", за которой следует строка Base64.
4. **Обработка неудачи**:
   - Если после 100000 итераций подходящий хэш не найден, функция кодирует `seed` в Base64 и возвращает строку, начинающуюся с "gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D", за которой следует строка Base64.

#### Examples:

```python
# Пример вызова функции с обязательным требованием и параметрами
result = generate_proof_token(required=True, seed="test_seed", difficulty="000", user_agent="TestAgent")
print(result)
# Пример вызова функции без обязательного требования
result = generate_proof_token(required=False)
print(result)
# Пример вызова функции с предоставленным proof_token
result = generate_proof_token(required=True, seed="test_seed", difficulty="000", proof_token="custom_token")
print(result)