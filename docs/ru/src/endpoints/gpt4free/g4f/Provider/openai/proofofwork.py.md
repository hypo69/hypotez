# Модуль `proofofwork.py`

## Обзор

Модуль `proofofwork.py` предназначен для генерации proof-of-work токенов, которые используются для подтверждения выполнения вычислительной работы. Этот механизм применяется для защиты от злоупотреблений и автоматизированных запросов. В частности, он используется в контексте взаимодействия с API OpenAI через g4f (gpt4free).

## Подробней

Основная задача модуля - сгенерировать токен, который удовлетворяет определенным требованиям сложности (difficulty). Это достигается путем итеративного изменения части данных (nonce) и вычисления хеша до тех пор, пока хеш не будет соответствовать заданной сложности. Если за определенное количество итераций токен не сгенерирован, возвращается fallback токен.

## Функции

### `generate_proof_token`

```python
def generate_proof_token(required: bool, seed: str = "", difficulty: str = "", user_agent: str = None, proof_token: str = None):
    """Функция генерирует proof-of-work токен для подтверждения вычислительной работы.

    Args:
        required (bool): Указывает, требуется ли генерация токена. Если `False`, функция не выполняет никаких действий.
        seed (str, optional): Зерно (seed), используемое при хешировании. По умолчанию "".
        difficulty (str, optional): Строка, определяющая сложность proof-of-work. Токен должен содержать хеш, начинающийся с этой строки. По умолчанию "".
        user_agent (str, optional): User-agent для включения в токен. По умолчанию `None`.
        proof_token (str, optional): Предопределенный токен для использования вместо генерации нового. По умолчанию `None`.

    Returns:
        str | None: Сгенерированный proof-of-work токен в формате "gAAAAAB" + base64 encoded data или fallback токен, если не удалось сгенерировать токен за 100000 итераций. Возвращает `None`, если `required` is `False`.

    Как работает функция:
    - Если `required` равно `False`, функция не выполняет никаких действий и возвращает `None`.
    - Если `proof_token` не передан, создается случайный `proof_token`.
    - В цикле до 100000 раз:
        - Итерируется значение `proof_token[3]`.
        - Данные `proof_token` преобразуются в JSON, кодируются в base64.
        - Вычисляется SHA3-512 хеш от комбинации `seed` и base64 строки.
        - Если хеш начинается с подстроки, равной `difficulty`, возвращается сгенерированный токен.
    - Если за 100000 итераций токен не сгенерирован, возвращается fallback токен.

    Примеры:
        >>> generate_proof_token(required=False)
        None

        >>> token = generate_proof_token(required=True, seed="test_seed", difficulty="0000")
        >>> if token:
        ...     print(token[:10])  # Вывод первых 10 символов токена
        gAAAAAB...

        >>> token = generate_proof_token(required=True, seed="another_seed", difficulty="0000", user_agent="Mozilla/5.0")
        >>> if token:
        ...     print(token[:10])  # Вывод первых 10 символов токена
        gAAAAAB...
    """
    if not required:
        return

    if proof_token is None:
        screen = random.choice([3008, 4010, 6000]) * random.choice([1, 2, 4])
        # Функция получает текущее время в формате UTC
        now_utc = datetime.now(timezone.utc)
        # Функция форматирует время в строку
        parse_time = now_utc.strftime('%a, %d %b %Y %H:%M:%S GMT')
        proof_token = [
            screen, parse_time,
            None, 0, user_agent,
            "https://tcr9i.chat.openai.com/v2/35536E1E-65B4-4D96-9D97-6ADB7EFF8147/api.js",
            "dpl=1440a687921de39ff5ee56b92807faaadce73f13","en","en-US",
            None,
            "plugins−[object PluginArray]",
            random.choice(["_reactListeningcfilawjnerp", "_reactListening9ne2dfo1i47", "_reactListening410nzwhan2a"]),
            random.choice(["alert", "ontransitionend", "onprogress"])
        ]

    diff_len = len(difficulty)
    for i in range(100000):
        proof_token[3] = i
        # Функция преобразует структуру данных в JSON-строку
        json_data = json.dumps(proof_token)
        # Функция кодирует JSON-строку в base64
        base = base64.b64encode(json_data.encode()).decode()
        # Функция вычисляет SHA3-512 хеш
        hash_value = hashlib.sha3_512((seed + base).encode()).digest()

        if hash_value.hex()[:diff_len] <= difficulty:
            return "gAAAAAB" + base

    # Функция кодирует seed в base64 в случае неудачи
    fallback_base = base64.b64encode(f'"{seed}"'.encode()).decode()
    return "gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D" + fallback_base