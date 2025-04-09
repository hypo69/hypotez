# Модуль `Bing.py`

## Обзор

Модуль предоставляет интерфейс для взаимодействия с чат-ботом Bing AI. Он позволяет создавать диалоги, отправлять запросы и получать ответы в режиме стриминга. Модуль использует асинхронные запросы для обеспечения неблокирующего взаимодействия.

## Подробней

Этот модуль является провайдером для библиотеки `g4f`, обеспечивая взаимодействие с Bing AI. Он включает в себя функции для создания новых сессий чата, форматирования сообщений и асинхронной генерации ответов с использованием веб-сокетов. Модуль также обрабатывает ошибки и поддерживает контекст диалога.

## Классы

### `optionsSets`

Описание настроек для различных опций, используемых при взаимодействии с Bing AI.

**Атрибуты:**

-   `optionSet` (dict): Словарь, определяющий структуру набора опций.
    Содержит информацию о `tone` (тип: str) и `optionsSets` (тип: list).
-   `jailbreak` (dict): Набор опций, предназначенный для "обхода" ограничений Bing AI.
    Включает список `optionsSets` с различными идентификаторами.

### `Defaults`

Содержит значения по умолчанию для различных параметров, используемых в модуле.

**Атрибуты:**

-   `delimiter` (str): Разделитель сообщений, используемый при обмене данными с Bing AI (`\x1e`).
-   `ip_address` (str): IP-адрес, используемый для обхода ограничений Bing AI. Генерируется случайным образом.
-   `allowedMessageTypes` (list): Список разрешенных типов сообщений для Bing AI.
-   `sliceIds` (list): Список идентификаторов "срезов", используемых для настройки поведения Bing AI.
-   `location` (dict): Информация о местоположении, используемая для настройки Bing AI. Включает `locale`, `market`, `region` и `locationHints`.

## Функции

### `_format`

```python
def _format(msg: dict) -> str:
    """Форматирует сообщение в JSON-формат с добавлением разделителя.

    Args:
        msg (dict): Словарь с сообщением для форматирования.

    Returns:
        str: JSON-представление сообщения с добавленным разделителем `Defaults.delimiter`.
    """
    ...
```

**Назначение**: Форматирует словарь `msg` в JSON-строку и добавляет разделитель `Defaults.delimiter` в конце.

**Параметры**:

-   `msg` (dict): Словарь, который необходимо преобразовать в JSON.

**Возвращает**:

-   `str`: JSON-представление словаря `msg` с добавленным разделителем.

**Как работает функция**:

1.  Преобразует словарь `msg` в JSON-формат с помощью `json.dumps`, отключая экранирование символов Unicode (`ensure_ascii=False`).
2.  Добавляет разделитель `Defaults.delimiter` в конец JSON-строки.

```
    msg (dict)
     |
     | json.dumps(msg, ensure_ascii=False)
     |
     | + Defaults.delimiter
     |
    JSON string + delimiter
```

### `create_conversation`

```python
async def create_conversation():
    """Создает новый разговор с Bing AI.

    Returns:
        tuple[str, str, str]: Кортеж, содержащий conversationId, clientId и conversationSignature.

    Raises:
        Exception: Если не удалось создать разговор после нескольких попыток.
    """
    ...
```

**Назначение**: Создает новый разговор с Bing AI, получая `conversationId`, `clientId` и `conversationSignature`.

**Возвращает**:

-   `tuple[str, str, str]`: Кортеж, содержащий идентификатор разговора (`conversationId`), идентификатор клиента (`clientId`) и подпись разговора (`conversationSignature`).

**Вызывает исключения**:

-   `Exception`: Если после 5 попыток не удается получить необходимые данные для создания разговора.

**Как работает функция**:

1.  Выполняет до 5 попыток запроса к API Bing для создания разговора.
2.  Отправляет GET-запрос к `https://www.bing.com/turing/conversation/create` с необходимыми заголовками.
3.  Извлекает `conversationId`, `clientId` и `conversationSignature` из JSON-ответа.
4.  Если все три параметра успешно получены, возвращает их в виде кортежа.
5.  Если после 5 попыток не удается получить все необходимые параметры, выбрасывает исключение `Exception`.

```
    Loop (5 attempts)
     |
     | GET request to Bing API
     |
     | Extract conversationId, clientId, conversationSignature
     |
     | If all parameters are not None
     |
     | Return (conversationId, clientId, conversationSignature)
     |
    Raise Exception if all parameters are not available after 5 attempts
```

### `stream_generate`

```python
async def stream_generate(prompt: str, mode: optionsSets.optionSet = optionsSets.jailbreak, context: bool | str = False):
    """Генерирует ответ от Bing AI в режиме стриминга.

    Args:
        prompt (str): Текст запроса.
        mode (optionsSets.optionSet, optional): Набор опций для запроса. По умолчанию `optionsSets.jailbreak`.
        context (bool | str, optional): Контекст для запроса. По умолчанию `False`.

    Yields:
        str: Части ответа от Bing AI.

    Raises:
        Exception: Если произошла ошибка при генерации ответа.
    """
    ...
```

**Назначение**: Генерирует ответ от Bing AI в режиме стриминга, используя веб-сокеты.

**Параметры**:

-   `prompt` (str): Текст запроса, который отправляется Bing AI.
-   `mode` (optionsSets.optionSet, optional): Набор опций для запроса. По умолчанию используется `optionsSets.jailbreak`.
-   `context` (bool | str, optional): Контекст для запроса. Может быть `False` или строкой с контекстной информацией. По умолчанию `False`.

**Возвращает**:

-   `Generator[str, None, None]`: Генератор, выдающий части ответа от Bing AI в виде строк.

**Вызывает исключения**:

-   `Exception`: Если во время генерации ответа происходит ошибка, например, если Bing AI возвращает сообщение об ошибке.

**Как работает функция**:

1.  Создает новую сессию с Bing AI, используя функцию `create_conversation`, и получает `conversationId`, `clientId` и `conversationSignature`.
2.  Устанавливает соединение с веб-сокетом Bing AI (`wss://sydney.bing.com/sydney/ChatHub`) с необходимыми заголовками.
3.  Отправляет начальное сообщение для установления протокола (`{\'protocol\': \'json\', \'version\': 1}`).
4.  Формирует структуру запроса (`struct`), содержащую параметры запроса, включая `prompt`, `mode`, `context`, `conversationSignature`, `participant` и `conversationId`.
5.  Отправляет структуру запроса Bing AI через веб-сокет.
6.  Получает ответы от Bing AI в цикле, пока не будет получен финальный ответ.
7.  Разбирает ответы, извлекая текст ответа и возвращая его частями с помощью `yield`.
8.  Обрабатывает ошибки, проверяя наличие ошибок в ответах и выбрасывая исключения в случае их обнаружения.
9.  Закрывает соединение с веб-сокетом и сессию после получения финального ответа.

```
    create_conversation() -> conversationId, clientId, conversationSignature
     |
     | Establish WebSocket connection with Bing AI
     |
     | Send initial protocol message
     |
     | Create request structure (struct) with prompt, mode, context, etc.
     |
     | Send request structure to Bing AI
     |
     | Loop:
     |  Receive response from Bing AI
     |  Parse response, extract text
     |  Yield text part
     |  Check for errors
     |  If final response is received:
     |   Close WebSocket connection and session
     |   Break loop
     |
    Exception: If an error occurs during response generation
```

### `run`

```python
def run(generator):
    """Запускает асинхронный генератор и возвращает его значения синхронно.

    Args:
        generator: Асинхронный генератор.

    Yields:
        Any: Значения, возвращаемые асинхронным генератором.
    """
    ...
```

**Назначение**: Запускает асинхронный генератор и возвращает его значения синхронно.

**Параметры**:

-   `generator`: Асинхронный генератор, который необходимо запустить.

**Возвращает**:

-   `Generator[Any, None, None]`: Генератор, выдающий значения, возвращаемые асинхронным генератором.

**Как работает функция**:

1.  Получает текущий event loop.
2.  Преобразует асинхронный генератор в асинхронный итератор.
3.  В цикле запускает асинхронный итератор с помощью `loop.run_until_complete(gen.__anext__())` и возвращает полученные значения.
4.  Прерывает цикл, когда асинхронный итератор выбрасывает исключение `StopAsyncIteration`.

```
    generator
     |
     | Get event loop
     |
     | Convert generator to async iterator
     |
     | Loop:
     |  Run async iterator until complete
     |  Yield next value
     |  If StopAsyncIteration:
     |   Break loop
     |
    Values from async generator
```

### `convert`

```python
def convert(messages):
    """Преобразует список сообщений в контекст для Bing AI.

    Args:
        messages (list): Список сообщений в формате `[{"role": "user"|"assistant", "content": str}, ...]`.

    Returns:
        str: Контекст для Bing AI в виде строки.
    """
    ...
```

**Назначение**: Преобразует список сообщений в контекст, пригодный для использования с Bing AI.

**Параметры**:

-   `messages` (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами `"role"` (роль отправителя, например, `"user"` или `"assistant"`) и `"content"` (содержимое сообщения).

**Возвращает**:

-   `str`: Строка, представляющая контекст для Bing AI, где каждое сообщение форматируется как `"[role](#message)\ncontent\n\n"`.

**Как работает функция**:

1.  Инициализирует пустую строку `context`.
2.  Проходит по каждому сообщению в списке `messages`.
3.  Форматирует каждое сообщение в виде `"[role](#message)\ncontent\n\n"` и добавляет его в строку `context`.
4.  Возвращает строку `context`.

```
    messages (list)
     |
     | Initialize context = ""
     |
     | Loop:
     |  Format message as "[role](#message)\ncontent\n\n"
     |  Append formatted message to context
     |
     | Return context
```

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Создает запрос к Bing AI и возвращает ответ в виде генератора.

    Args:
        model (str): Модель для использования.
        messages (list): Список сообщений для контекста.
        stream (bool): Флаг, указывающий, использовать ли стриминг.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части ответа от Bing AI.
    """
    ...
```

**Назначение**: Создает запрос к Bing AI и возвращает ответ в виде генератора.

**Параметры**:

-   `model` (str): Имя модели, которую следует использовать для генерации ответа.
-   `messages` (list): Список сообщений, представляющих контекст разговора.
-   `stream` (bool): Флаг, указывающий, следует ли использовать потоковый режим для получения ответа.
-   `**kwargs`: Дополнительные аргументы, которые могут быть переданы в функцию `stream_generate`.

**Возвращает**:

-   `Generator[str, None, None]`: Генератор, выдающий части ответа от Bing AI в виде строк.

**Как работает функция**:

1.  Определяет, использовать ли контекст на основе количества сообщений в списке `messages`. Если сообщений меньше двух, используется только последнее сообщение в качестве запроса, и контекст не используется.
2.  Если сообщений два или больше, используется последнее сообщение в качестве запроса, а предыдущие сообщения преобразуются в контекст с помощью функции `convert`.
3.  Вызывает функцию `stream_generate` с запросом, набором опций `optionsSets.jailbreak` и контекстом.
4.  Перебирает ответы, полученные от генератора `stream_generate`, и возвращает их с помощью `yield`.

```
    messages (list), model (str), stream (bool), **kwargs
     |
     | If len(messages) < 2
     |  prompt = messages[0]['content']
     |  context = False
     | Else
     |  prompt = messages[-1]['content']
     |  context = convert(messages[:-1])
     |
     | stream_generate(prompt, optionsSets.jailbreak, context)
     |
     | Yield tokens from stream_generate
```

## Переменные

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    \'(%s)\' % \', \'.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Описание**: Строка, содержащая информацию о поддерживаемых параметрах функции `_create_completion`.
Содержит информацию о типах параметров функции `_create_completion`, полученную с использованием `get_type_hints`.