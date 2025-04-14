# Модуль `DeepAi.py`

## Обзор

Модуль предоставляет интерфейс для взаимодействия с сервисом DeepAI для генерации текста. Он содержит функции для создания запросов к DeepAI API и обработки ответов. Модуль использует библиотеки `requests`, `json`, `hashlib` и `random` для выполнения HTTP-запросов, обработки JSON-данных, создания хешей и генерации случайных чисел соответственно.

## Подробней

Этот модуль предназначен для интеграции с DeepAI API в рамках проекта `hypotez`. Он обеспечивает функциональность для отправки текстовых запросов к DeepAI и получения ответов.

Модуль содержит следующие компоненты:

*   Функция `_create_completion`, которая создает запрос к DeepAI API и возвращает ответ в виде потока текста.
*   Функция `md5`, которая используется для создания хеша MD5 из входной строки.
*   Функция `get_api_key`, которая генерирует ключ API для DeepAI на основе user agent.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к DeepAI API и возвращает ответ в виде потока текста.

    Args:
        model (str): Идентификатор используемой модели DeepAI.
        messages (list): Список сообщений для отправки в DeepAI API.
        stream (bool): Флаг, указывающий, следует ли возвращать ответ в виде потока.
        **kwargs: Дополнительные параметры для передачи в DeepAI API.

    Returns:
        Generator[str, None, None]: Генератор строк, представляющих собой части ответа от DeepAI API.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает функция:
    1.  Определяется внутренняя функция `md5`, которая используется для вычисления MD5-хеша.
    2.  Определяется внутренняя функция `get_api_key`, которая генерирует API-ключ на основе User-Agent.
    3.  Формируются заголовки запроса, включающие API-ключ и User-Agent.
    4.  Формируется тело запроса, включающее стиль чата и историю сообщений.
    5.  Выполняется POST-запрос к DeepAI API.
    6.  Итерируется по содержимому ответа, декодируя каждый чанк и возвращая его в виде строки.

    Внутренние функции:
    ### `md5`
    ```python
    def md5(text: str) -> str:
        """
        Вычисляет MD5-хеш от входной строки.

        Args:
            text (str): Входная строка для вычисления хеша.

        Returns:
            str: MD5-хеш строки.
        """
        ...
    ```
    **Назначение**: Вычисляет MD5-хеш заданной строки.
    **Параметры**:
      - `text` (str): Строка для хеширования.
    **Возвращает**:
      - `str`: MD5-хеш строки в шестнадцатеричном формате.
    **Как работает функция**:
        1. Кодирует входную строку в байты с использованием кодировки UTF-8.
        2. Вычисляет MD5-хеш байтовой строки с помощью hashlib.md5().
        3. Преобразует хеш в шестнадцатеричный формат с помощью hexdigest().
        4. Инвертирует строку, используя срез `[::-1]`.

    ### `get_api_key`
    ```python
    def get_api_key(user_agent: str) -> str:
        """
        Генерирует API-ключ для DeepAI на основе User-Agent.

        Args:
            user_agent (str): User-Agent для генерации ключа.

        Returns:
            str: Сгенерированный API-ключ.
        """
        ...
    ```

    **Назначение**: Генерирует API-ключ для DeepAI на основе User-Agent.
    **Параметры**:
      - `user_agent` (str): Строка User-Agent.
    **Возвращает**:
      - `str`: Сгенерированный API-ключ.
    **Как работает функция**:
        1. Генерирует случайное число в диапазоне от 0 до 10^11.
        2. Вычисляет MD5-хеш User-Agent несколько раз.
        3. Формирует API-ключ, объединяя префикс "tryit-", случайное число и MD5-хеш.

    ASCII flowchart:

    ```
    user_agent --> Получение API-ключа
                  |
                  --> Формирование заголовков
                  |
                  --> Формирование данных
                  |
                  --> Отправка POST-запроса к DeepAI API
                  |
                  --> Обработка ответа и возврат чанков
    ```

    Примеры:

    ```python
    # Пример использования функции _create_completion с минимальным набором параметров
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Hello, DeepAI!"}]
    stream = True
    result = _create_completion(model=model, messages=messages, stream=stream)
    for chunk in result:
        print(chunk)
    ```
    """
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[::-1]


    def get_api_key(user_agent: str) -> str:
        part1 = str(random.randint(0, 10**11))
        part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))
        
        return f"tryit-{part1}-{part2}"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    headers = {
        "api-key": get_api_key(user_agent),
        "user-agent": user_agent
    }

    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, json.dumps(messages))
    }

    r = requests.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True)

    for chunk in r.iter_content(chunk_size=None):
        r.raise_for_status()
        yield chunk.decode()
```

### `md5`

```python
def md5(text: str) -> str:
    """
    Вычисляет MD5-хеш от входной строки.

    Args:
        text (str): Входная строка для вычисления хеша.

    Returns:
        str: MD5-хеш строки.
    """
    return hashlib.md5(text.encode()).hexdigest()[::-1]
```

**Назначение**: Вычисляет MD5-хеш заданной строки.

**Параметры**:

*   `text` (str): Строка для хеширования.

**Возвращает**:

*   `str`: MD5-хеш строки в шестнадцатеричном формате.

**Как работает функция**:

1.  Кодирует входную строку в байты с использованием кодировки UTF-8.
2.  Вычисляет MD5-хеш байтовой строки с помощью `hashlib.md5()`.
3.  Преобразует хеш в шестнадцатеричный формат с помощью `hexdigest()`.
4.  Инвертирует строку, используя срез `[::-1]`.

ASCII flowchart:

```
Входная строка --> Кодирование в байты
                |
                --> Вычисление MD5-хеша
                |
                --> Преобразование в шестнадцатеричный формат
                |
                --> Инвертирование строки
                |
                --> Возврат хеша
```

**Примеры**:

```python
# Пример использования функции md5
text = "Hello, world!"
hashed_text = md5(text)
print(f"MD5 hash of '{text}': {hashed_text}")
```

### `get_api_key`

```python
def get_api_key(user_agent: str) -> str:
    """
    Генерирует API-ключ для DeepAI на основе User-Agent.

    Args:
        user_agent (str): User-Agent для генерации ключа.

    Returns:
        str: Сгенерированный API-ключ.
    """
    part1 = str(random.randint(0, 10**11))
    part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))
    
    return f"tryit-{part1}-{part2}"
```

**Назначение**: Генерирует API-ключ для DeepAI на основе User-Agent.

**Параметры**:

*   `user_agent` (str): Строка User-Agent.

**Возвращает**:

*   `str`: Сгенерированный API-ключ.

**Как работает функция**:

1.  Генерирует случайное число в диапазоне от 0 до 10^11.
2.  Вычисляет MD5-хеш User-Agent несколько раз, используя функцию `md5`.
3.  Формирует API-ключ, объединяя префикс "tryit-", случайное число и MD5-хеш.

ASCII flowchart:

```
User-Agent --> Генерация случайного числа
           |
           --> Вычисление MD5-хеша User-Agent (несколько раз)
           |
           --> Формирование API-ключа
           |
           --> Возврат API-ключа
```

**Примеры**:

```python
# Пример использования функции get_api_key
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
api_key = get_api_key(user_agent)
print(f"Generated API key: {api_key}")
```