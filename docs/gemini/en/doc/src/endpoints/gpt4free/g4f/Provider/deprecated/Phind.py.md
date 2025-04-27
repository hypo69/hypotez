# Provider Phind

## Overview

Этот модуль предоставляет класс `Phind`, который реализует асинхронный генератор для взаимодействия с API Phind. Phind - это поисковая система, предоставляющая доступ к модели GPT-4. 

## Details

Класс `Phind` реализует интерфейс `AsyncGeneratorProvider`, позволяя использовать его с фреймворком `hypotez` для обработки запросов к модели GPT-4 через API Phind. 

## Classes

### `class Phind`

**Description**:  Класс `Phind` реализует асинхронный генератор для взаимодействия с API Phind. 

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `url`: URL API Phind.
- `working`: Флаг, указывающий на доступность API (по умолчанию `False`).
- `lockdown`: Флаг, указывающий на блокировку доступа к API (по умолчанию `True`).
- `supports_stream`: Флаг, указывающий на поддержку потоковой передачи данных (по умолчанию `True`).
- `supports_message_history`: Флаг, указывающий на поддержку истории сообщений (по умолчанию `True`).

**Methods**:
- `create_async_generator()`: Асинхронный метод, создающий генератор для обработки запросов к API Phind.

## Class Methods

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        creative_mode: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронный метод, создающий генератор для обработки запросов к API Phind.

        Args:
            model (str): Название модели (например, "gpt-4").
            messages (Messages): Список сообщений в диалоге.
            proxy (str, optional): Прокси-сервер для запроса. Defaults to None.
            timeout (int, optional): Таймаут запроса в секундах. Defaults to 120.
            creative_mode (bool, optional): Флаг, указывающий на включение творческого режима. Defaults to False.

        Returns:
            AsyncResult: Объект `AsyncResult`, который представляет собой асинхронный результат генератора.

        Raises:
            RuntimeError: Если возникла ошибка на стороне сервера Phind.
        """
        headers = {
            "Accept": "*/*",
            "Origin": cls.url,
            "Referer": f"{cls.url}/search",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        async with StreamSession(
            headers=headers,
            impersonate="chrome",
            proxies={"https": proxy},
            timeout=timeout
        ) as session:
            url = "https://www.phind.com/search?home=true"
            async with session.get(url) as response:
                text = await response.text()
                match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(?P<json>[\\S\\s]+?)</script>', text)
                data = json.loads(match.group("json"))
                challenge_seeds = data["props"]["pageProps"]["challengeSeeds"]

            prompt = messages[-1]["content"]
            data = {
                "question": prompt,
                "question_history": [
                    message["content"] for message in messages[:-1] if message["role"] == "user"
                ],
                "answer_history": [
                    message["content"] for message in messages if message["role"] == "assistant"
                ],
                "webResults": [],
                "options": {
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "language": "en-US",
                    "detailed": True,
                    "anonUserId": "",
                    "answerModel": "GPT-4" if model.startswith("gpt-4") else "Phind-34B",
                    "creativeMode": creative_mode,
                    "customLinks": []
                },
                "context": "\n".join([message["content"] for message in messages if message["role"] == "system"]),
            }
            data["challenge"] = generate_challenge(data, **challenge_seeds)
            async with session.post(f"https://https.api.phind.com/infer/", headers=headers, json=data) as response:
                new_line = False
                async for line in response.iter_lines():
                    if line.startswith(b"data: "):
                        chunk = line[6:]
                        if chunk.startswith(b'<PHIND_DONE/>'):
                            break
                        if chunk.startswith(b'<PHIND_BACKEND_ERROR>\'):
                            raise RuntimeError(f"Response: {chunk.decode()}")
                        if chunk.startswith(b'<PHIND_WEBRESULTS>\') or chunk.startswith(b'<PHIND_FOLLOWUP>\'):
                            pass
                        elif chunk.startswith(b"<PHIND_METADATA>") or chunk.startswith(b"<PHIND_INDICATOR>"):
                            pass
                        elif chunk.startswith(b"<PHIND_SPAN_BEGIN>") or chunk.startswith(b"<PHIND_SPAN_END>"):
                            pass
                        elif chunk:
                            yield chunk.decode()
                        elif new_line:
                            yield "\n"
                            new_line = False
                        else:
                            new_line = True

```

**Purpose**:  Этот метод создает асинхронный генератор для обработки запросов к API Phind. 

**Parameters**:
- `model` (str): Название модели (например, "gpt-4").
- `messages` (Messages): Список сообщений в диалоге.
- `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
- `timeout` (int, optional): Таймаут запроса в секундах. По умолчанию `120`.
- `creative_mode` (bool, optional): Флаг, указывающий на включение творческого режима. По умолчанию `False`.

**Returns**:
- `AsyncResult`: Объект `AsyncResult`, который представляет собой асинхронный результат генератора.

**Raises Exceptions**:
- `RuntimeError`: Если возникла ошибка на стороне сервера Phind.

**How the Function Works**:
- Метод `create_async_generator()`  использует класс `StreamSession` для выполнения HTTP-запросов к API Phind.
-  Метод создает запрос POST к API Phind с использованием URL `https://https.api.phind.com/infer/`. 
-  В запросе передаются следующие данные:
    - `question`: текст запроса (последнее сообщение в диалоге).
    - `question_history`: история запросов пользователя в диалоге.
    - `answer_history`: история ответов модели в диалоге.
    - `webResults`: список веб-результатов поиска (по умолчанию пустой).
    - `options`: словарь с параметрами запроса (дата, язык, подробность, идентификатор пользователя, модель, творческий режим, список пользовательских ссылок).
    - `context`: контекст диалога (системные сообщения).
    - `challenge`: значение вызова для проверки запроса.
-  Метод обрабатывает ответ от сервера Phind, который передается в виде потока данных (стековый ответ), и формирует ответ модели GPT-4.

**Examples**:
```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Phind import Phind
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.Provider import Messages
>>> messages = Messages(
...     [
...         {"role": "system", "content": "You are a helpful assistant."},
...         {"role": "user", "content": "What is the meaning of life?"},
...     ]
... )
>>> async_result = await Phind.create_async_generator(
...     model="gpt-4",
...     messages=messages,
...     proxy=None,
...     timeout=120,
...     creative_mode=False
... )
>>> async for chunk in async_result:
...     print(chunk, end="")
The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one answer that everyone agrees on, but some common themes include finding purpose, meaning, and fulfillment in life. Some believe that the meaning of life is to be happy, while others believe that it is to serve a higher purpose. Ultimately, the meaning of life is up to each individual to decide.
```

## Parameter Details

- `model` (str): Название модели (например, "gpt-4").
- `messages` (Messages): Список сообщений в диалоге.
- `proxy` (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
- `timeout` (int, optional): Таймаут запроса в секундах. По умолчанию `120`.
- `creative_mode` (bool, optional): Флаг, указывающий на включение творческого режима. По умолчанию `False`.

## Inner Functions

### `deterministic_stringify(obj)`

```python
def deterministic_stringify(obj):
    """
    Преобразует объект в строку, сохраняя порядок элементов.

    Args:
        obj (Any): Объект для преобразования.

    Returns:
        str: Строка, представляющая объект.
    """
    def handle_value(value):
        """
        Преобразует значение в строку.

        Args:
            value (Any): Значение для преобразования.

        Returns:
            str: Строка, представляющая значение.
        """
        if isinstance(value, (dict, list)):
            if isinstance(value, list):
                return '[' + ','.join(sorted(map(handle_value, value))) + ']'
            else:  # It's a dict
                return '{' + deterministic_stringify(value) + '}'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return format(value, '.8f').rstrip('0').rstrip('.')
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return 'null'

    items = sorted(obj.items(), key=lambda x: x[0])
    return ','.join([f'{k}:{handle_value(v)}' for k, v in items if handle_value(v) is not None])

```

**Purpose**:  Функция `deterministic_stringify()`  преобразует объект в строку, сохраняя порядок элементов. 

**Parameters**:
- `obj` (Any): Объект для преобразования.

**Returns**:
- `str`: Строка, представляющая объект.

**How the Function Works**:
- Функция `deterministic_stringify()`  использует рекурсивную функцию `handle_value()` для преобразования значений в строку. 
-  Функция `handle_value()`  преобразует значения в строку, сохраняя порядок элементов, при этом:
    - Для списков (list) значения преобразуются в строку, сортируются по алфавиту и соединяются запятыми.
    - Для словарей (dict) значения преобразуются в строку рекурсивно.
    - Для булевых значений (bool) значения преобразуются в строки `'true'` или `'false'`.
    - Для целых чисел (int) и чисел с плавающей запятой (float) значения преобразуются в строки с использованием форматирования `'.8f'`, обрезая лишние нули.
    - Для строк (str) значения преобразуются в строки, заключенные в кавычки.
    - Для всех остальных типов данных возвращается строка `'null'`.
-  В функции `deterministic_stringify()`  элементы объекта сортируются по ключу, после чего преобразуются в строку с помощью функции `handle_value()`. 
-  Полученные строки соединяются запятыми.

### `prng_general(seed, multiplier, addend, modulus)`

```python
def prng_general(seed, multiplier, addend, modulus):
    """
    Генератор псевдослучайных чисел.

    Args:
        seed (int): Начальное значение.
        multiplier (int): Множитель.
        addend (int): Добавляемое значение.
        modulus (int): Модуль.

    Returns:
        float: Псевдослучайное число.
    """
    a = seed * multiplier + addend
    if a < 0:
        return ((a%modulus)-modulus)/modulus
    else:
        return a%modulus/modulus

```

**Purpose**:  Функция `prng_general()`  генерирует псевдослучайное число. 

**Parameters**:
- `seed` (int): Начальное значение.
- `multiplier` (int): Множитель.
- `addend` (int): Добавляемое значение.
- `modulus` (int): Модуль.

**Returns**:
- `float`: Псевдослучайное число.

**How the Function Works**:
-  Функция `prng_general()`  выполняет линейный конгруэнтный генератор (LCG) для генерации псевдослучайных чисел. 
-  Функция использует формулу `a = seed * multiplier + addend`. 
-  Если полученное значение `a` меньше 0,  то функция вычисляет остаток от деления `a` на `modulus` и вычитает `modulus` из результата.
-  В противном случае функция вычисляет остаток от деления `a` на `modulus`.
-  Результат делится на `modulus`, чтобы получить псевдослучайное число в диапазоне от 0 до 1.

### `generate_challenge_seed(l)`

```python
def generate_challenge_seed(l):
    """
    Генерирует начальное значение для генератора псевдослучайных чисел.

    Args:
        l (Any): Объект, используемый для генерации начального значения.

    Returns:
        int: Начальное значение для генератора псевдослучайных чисел.
    """
    I = deterministic_stringify(l)
    d = parse.quote(I, safe='')
    return simple_hash(d)

```

**Purpose**:  Функция `generate_challenge_seed()`  генерирует начальное значение для генератора псевдослучайных чисел. 

**Parameters**:
- `l` (Any): Объект, используемый для генерации начального значения.

**Returns**:
- `int`: Начальное значение для генератора псевдослучайных чисел.

**How the Function Works**:
- Функция `generate_challenge_seed()`  преобразует объект `l` в строку с помощью функции `deterministic_stringify()`. 
-  Затем функция кодирует строку с помощью функции `parse.quote()`, заменяя нестандартные символы.
-  Функция `simple_hash()`  вычисляет хеш-значение кодированной строки, которое используется в качестве начального значения для генератора псевдослучайных чисел.

### `simple_hash(s)`

```python
def simple_hash(s):
    """
    Вычисляет простое хеш-значение строки.

    Args:
        s (str): Строка для вычисления хеша.

    Returns:
        int: Хеш-значение строки.
    """
    d = 0
    for char in s:
        if len(char) > 1 or ord(char) >= 256:
            continue
        d = ((d << 5) - d + ord(char[0])) & 0xFFFFFFFF
        if d > 0x7FFFFFFF: # 2147483647
            d -= 0x100000000 # Subtract 2**32
    return d

```

**Purpose**:  Функция `simple_hash()`  вычисляет простое хеш-значение строки. 

**Parameters**:
- `s` (str): Строка для вычисления хеша.

**Returns**:
- `int`: Хеш-значение строки.

**How the Function Works**:
-  Функция `simple_hash()`  проходит по строке и для каждого символа вычисляет хеш-значение с помощью битового сдвига влево, вычитания исходного значения и добавления кода символа. 
-  Результат операции AND  с числом `0xFFFFFFFF`  ограничивает результат хеширования 32 битами.
-  Если хеш-значение превышает максимальное значение для целого числа с 32 битами ( `0x7FFFFFFF` ), то из него вычитается `0x100000000`  (2**32).

### `generate_challenge(obj, **kwargs)`

```python
def generate_challenge(obj, **kwargs):
    """
    Генерирует значение вызова для проверки запроса.

    Args:
        obj (Any): Объект, используемый для генерации значения вызова.
        **kwargs: Дополнительные аргументы для генератора псевдослучайных чисел.

    Returns:
        float: Значение вызова для проверки запроса.
    """
    return prng_general(
        seed=generate_challenge_seed(obj),
        **kwargs
    )

```

**Purpose**:  Функция `generate_challenge()`  генерирует значение вызова для проверки запроса. 

**Parameters**:
- `obj` (Any): Объект, используемый для генерации значения вызова.
- `**kwargs`: Дополнительные аргументы для генератора псевдослучайных чисел.

**Returns**:
- `float`: Значение вызова для проверки запроса.

**How the Function Works**:
-  Функция `generate_challenge()`  генерирует начальное значение для генератора псевдослучайных чисел с помощью функции `generate_challenge_seed()`  и использует его для вызова функции `prng_general()`  с дополнительными аргументами.
-  Функция `prng_general()`  генерирует псевдослучайное число, которое используется как значение вызова.

## Examples

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Phind import Phind
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.Provider import Messages
>>> messages = Messages(
...     [
...         {"role": "system", "content": "You are a helpful assistant."},
...         {"role": "user", "content": "What is the meaning of life?"},
...     ]
... )
>>> async_result = await Phind.create_async_generator(
...     model="gpt-4",
...     messages=messages,
...     proxy=None,
...     timeout=120,
...     creative_mode=False
... )
>>> async for chunk in async_result:
...     print(chunk, end="")
The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one answer that everyone agrees on, but some common themes include finding purpose, meaning, and fulfillment in life. Some believe that the meaning of life is to be happy, while others believe that it is to serve a higher purpose. Ultimately, the meaning of life is up to each individual to decide.
```