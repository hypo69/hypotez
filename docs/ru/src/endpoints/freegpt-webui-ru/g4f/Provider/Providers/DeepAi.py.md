# Модуль `DeepAi.py`

## Обзор

Модуль предназначен для взаимодействия с провайдером DeepAI для получения ответов на запросы. Он предоставляет функцию `_create_completion`, которая отправляет запросы к API DeepAI и возвращает результаты. Модуль также определяет параметры, поддерживаемые провайдером.

## Подробней

Этот модуль используется для интеграции с сервисом DeepAI в проекте `hypotez`. Он содержит логику для формирования запросов к API DeepAI, обработки ответов и предоставления результатов в нужном формате. Модуль также включает функции для генерации ключей API и обработки ошибок.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция отправляет запрос в DeepAI и возвращает ответ.

    Args:
        model (str): Название используемой модели.
        messages (list): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные аргументы.

    Returns:
        Generator[str, None, None]: Генератор строк, содержащих ответ от DeepAI.

    Raises:
        requests.exceptions.HTTPError: Если возникает ошибка при отправке запроса.

    **Внутренние функции**:
    - `md5(text: str) -> str`
    - `get_api_key(user_agent: str) -> str`

    **Как работает функция**:
    1. Определяет внутреннюю функцию `md5` для вычисления MD5-хеша строки.
    2. Определяет внутреннюю функцию `get_api_key` для генерации ключа API на основе user-agent.
    3. Формирует заголовки запроса, включая ключ API и user-agent.
    4. Формирует данные запроса, включая стиль чата и историю сообщений.
    5. Отправляет POST-запрос к API DeepAI с использованием потоковой передачи данных.
    6. Итерируется по чанкам ответа и возвращает их в виде генератора строк.
    7. Обрабатывает возможные ошибки при отправке запроса.

    ```
    A [Определение внутренних функций md5 и get_api_key]
    |
    B [Формирование заголовков запроса (headers) с использованием get_api_key]
    |
    C [Формирование данных запроса (files) с использованием chat_style и chatHistory]
    |
    D [Отправка POST-запроса к API DeepAI с использованием потоковой передачи (stream=True)]
    |
    E [Итерация по чанкам ответа и их декодирование]
    |
    F [Возврат чанков ответа в виде генератора строк]
    ```

    **Примеры**:
    ```python
    # Пример вызова функции _create_completion
    model = 'gpt-3.5-turbo'
    messages = [{'role': 'user', 'content': 'Hello'}]
    stream = True
    result = _create_completion(model, messages, stream)
    for chunk in result:
        print(chunk, end='')
    ```
    """
    def md5(text: str) -> str:
        """ Функция вычисляет MD5-хеш заданной строки.

        Args:
            text (str): Строка для вычисления хеша.

        Returns:
            str: MD5-хеш строки в обратном порядке.
        """
        return hashlib.md5(text.encode()).hexdigest()[::-1]

    def get_api_key(user_agent: str) -> str:
        """ Функция генерирует ключ API на основе user-agent.

        Args:
            user_agent (str): User-agent для генерации ключа.

        Returns:
            str: Сгенерированный ключ API.
        """
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

## Параметры

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Описание параметров, поддерживаемых провайдером DeepAI.
```