# Модуль `Vercel`

## Обзор

Модуль `Vercel` предоставляет класс `Vercel`, который является провайдером для взаимодействия с моделями ИИ через API Vercel. Он поддерживает модели `gpt-3.5-turbo` и потоковую передачу данных.
Модуль предназначен для интеграции с сервисами Vercel AI SDK для создания чат-ботов и других приложений, использующих генеративные модели.

## Подробнее

Этот модуль позволяет взаимодействовать с API Vercel для использования различных моделей, таких как `gpt-3.5-turbo`. Он включает в себя функции для создания запросов к API и обработки ответов, в том числе в потоковом режиме. Модуль также содержит вспомогательные функции для получения токена защиты от ботов, необходимого для аутентификации запросов.

## Классы

### `Vercel`

**Описание**: Класс `Vercel` является реализацией абстрактного провайдера `AbstractProvider` и предоставляет методы для взаимодействия с API Vercel.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL для взаимодействия с API Vercel (`https://sdk.vercel.ai`).
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`
    - Отправляет запрос на создание завершения к API Vercel.

## Функции

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    **kwargs
) -> CreateResult:
    """
    Создает запрос на завершение текста, используя API Vercel.

    Args:
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        CreateResult: Генератор токенов ответа от API.

    Raises:
        MissingRequirementsError: Если отсутствует пакет `PyExecJS`.
        ValueError: Если указанная модель не поддерживается.

    Example:
        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> stream = True
        >>> for token in Vercel.create_completion(model, messages, stream):
        ...     print(token, end="")
    """
```

**Назначение**: Создает запрос на завершение текста, используя API Vercel.

**Параметры**:
- `model` (str): Идентификатор модели для использования.
- `messages` (Messages): Список сообщений для передачи в модель.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
- `proxy` (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для передачи в API.

**Возвращает**:
- `CreateResult`: Генератор токенов ответа от API.

**Вызывает исключения**:
- `MissingRequirementsError`: Если отсутствует пакет `PyExecJS`.
- `ValueError`: Если указанная модель не поддерживается.

**Как работает функция**:
1. Проверяет, установлен ли пакет `PyExecJS`. Если нет, вызывает исключение `MissingRequirementsError`.
2. Если `model` не указана, устанавливает значение по умолчанию `"gpt-3.5-turbo"`.
3. Проверяет, поддерживается ли указанная `model`. Если нет, вызывает исключение `ValueError`.
4. Формирует заголовки HTTP-запроса, включая токен защиты от ботов, полученный с помощью функции `get_anti_bot_token()`.
5. Формирует данные JSON-запроса, включая модель, сообщения и параметры.
6. Отправляет POST-запрос к API Vercel (`https://chat.vercel.ai/api/chat`) с использованием `requests.post`.
7. Обрабатывает ответ от API в потоковом режиме, итерируясь по содержимому чанков и декодируя их.
8. Возвращает генератор токенов ответа.

```
A [Проверка наличия PyExecJS]
|
B [Определение модели]
|
C [Проверка поддержки модели]
|
D [Формирование заголовков запроса]
|
E [Формирование данных JSON]
|
F [Отправка POST-запроса к API Vercel]
|
G [Обработка ответа API в потоковом режиме]
|
H [Возврат генератора токенов]
```

**Примеры**:
```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
for token in Vercel.create_completion(model, messages, stream):
    print(token, end="")
```

### `get_anti_bot_token`

```python
def get_anti_bot_token() -> str:
    """
    Получает токен защиты от ботов для аутентификации запросов к API Vercel.

    Returns:
        str: Токен защиты от ботов.

    Raises:
        Exception: Если происходит ошибка при выполнении JavaScript кода.

    Example:
        >>> token = get_anti_bot_token()
        >>> print(token)
        <токен>
    """
```

**Назначение**: Получает токен защиты от ботов для аутентификации запросов к API Vercel.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `str`: Токен защиты от ботов.

**Вызывает исключения**:
- `Exception`: Если происходит ошибка при выполнении JavaScript кода.

**Как работает функция**:
1. Формирует заголовки HTTP-запроса.
2. Отправляет GET-запрос к `https://sdk.vercel.ai/openai.jpeg` для получения данных, необходимых для генерации токена.
3. Декодирует base64-ответ и загружает JSON.
4. Формирует JavaScript-скрипт, который выполняет функцию, полученную из API.
5. Выполняет JavaScript-скрипт с помощью `execjs.compile`.
6. Кодирует результат в base64 и возвращает его.

```
A [Формирование заголовков запроса]
|
B [Отправка GET-запроса к API Vercel]
|
C [Декодирование base64-ответа]
|
D [Формирование JavaScript-скрипта]
|
E [Выполнение JavaScript-скрипта]
|
F [Кодирование результата в base64]
|
G [Возврат токена]
```

**Примеры**:
```python
token = get_anti_bot_token()
print(token)
```

### `ModelInfo`

**Описание**: `TypedDict`, определяющий структуру для хранения информации о модели.

**Атрибуты**:
- `id` (str): Идентификатор модели.
- `default_params` (dict[str, Any]): Словарь параметров по умолчанию для модели.

### `model_info`

**Описание**: Словарь, содержащий информацию о поддерживаемых моделях. Ключи словаря - это идентификаторы моделей, а значения - экземпляры `ModelInfo`.

**Примеры**:
```python
model_info: dict[str, ModelInfo] = {
    'replicate/llama70b-v2-chat': {
        'id': 'replicate:replicate/llama-2-70b-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
    'a16z-infra/llama7b-v2-chat': {
        'id': 'replicate:a16z-infra/llama7b-v2-chat',
        'default_params': {
            'temperature': 0.75,
            'maximumLength': 3000,
            'topP': 1,
            'repetitionPenalty': 1,
        },
    },
}