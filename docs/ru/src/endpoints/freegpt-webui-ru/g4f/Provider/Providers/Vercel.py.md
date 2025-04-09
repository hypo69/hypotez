# Модуль `Vercel.py`

## Обзор

Модуль предоставляет интерфейс для взаимодействия с AI-моделями, размещенными на платформе Vercel. Он включает в себя поддержку различных моделей, таких как Claude, Alpaca, Bloom и другие, а также обеспечивает функциональность для генерации текста на основе заданных параметров.

## Подробнее

Модуль содержит классы и функции для настройки HTTP-запросов, получения токенов авторизации, формирования запросов к API Vercel и обработки потоковых ответов от моделей. Он предназначен для интеграции с другими частями проекта `hypotez`, где требуется использование AI-моделей для генерации контента.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Генерирует текст, используя указанную модель и историю сообщений.

    Args:
        model (str): Идентификатор модели для генерации текста.
        messages (list): Список сообщений, представляющих историю разговора.
                         Каждый элемент списка - словарь, содержащий ключи 'role' (роль отправителя) и 'content' (содержание сообщения).
        stream (bool): Флаг, указывающий, следует ли возвращать результат в виде потока.
        **kwargs: Дополнительные параметры для передачи в модель.

    Yields:
        str: Токены сгенерированного текста.

    Как работает функция:
    1. **Формирование контекста разговора**: На основе списка сообщений формируется строка `conversation`, которая служит контекстом для модели.
    2. **Создание запроса к Vercel API**: Используется класс `Client` для отправки запроса к API Vercel с указанием модели и контекста разговора.
    3. **Обработка потокового ответа**: Полученный ответ от API Vercel обрабатывается в потоковом режиме, и каждый токен возвращается вызывающей стороне.

    flowchart ascii:

       Начало --> Формирование_контекста
       Формирование_контекста --> Отправка_запроса
       Отправка_запроса --> Обработка_ответа
       Обработка_ответа --> Вывод_токена
       Вывод_токена --> Конец

    Примеры:
        >>> messages = [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi'}]
        >>> for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
        ...     print(token)
    """
```

## Классы

### `Client`

```python
class Client:
    """
    Описывает HTTP клиент для взаимодействия с Vercel API.

    Attributes:
        session (requests.Session): HTTP сессия для выполнения запросов.
        headers (dict): Заголовки HTTP-запросов.

    Methods:
        get_token(): Получает токен авторизации.
        get_default_params(model_id: str): Возвращает параметры по умолчанию для указанной модели.
        generate(model_id: str, prompt: str, params: dict): Генерирует текст с использованием указанной модели и параметров.
    """
```

#### `__init__`

```python
def __init__(self):
    """
    Инициализирует экземпляр класса Client, настраивает HTTP-сессию и заголовки.
    """
```

#### `get_token`

```python
def get_token(self):
    """
    Получает токен авторизации, необходимый для выполнения запросов к Vercel API.

    Returns:
        str: Токен авторизации в формате base64.

    Как работает функция:

    1. **Запрос к API**: Функция отправляет GET-запрос по адресу `https://sdk.vercel.ai/openai.jpeg`.
    2. **Извлечение данных**: Из полученного ответа извлекается текст, который представляет собой base64-encoded JSON.
    3. **Декодирование и обработка**: JSON декодируется, и из него извлекаются параметры `c` и `a`.
    4. **Формирование JavaScript-кода**: На основе параметров `c` и `a` формируется JavaScript-код, который содержит функцию `token`.
    5. **Выполнение JavaScript-кода**: С помощью библиотеки `execjs` выполняется JavaScript-код, и вызывается функция `token`. Результат выполнения функции сохраняется в переменной `r`.
    6. **Формирование JSON**: Формируется JSON-объект, содержащий поля `r` (результат выполнения JavaScript-кода) и `t` (параметр из декодированного JSON).
    7. **Кодирование в base64**: JSON кодируется в строку, а затем кодируется в base64.
    8. **Возврат результата**: Возвращается строка в формате base64.

    flowchart ascii:

       Начало --> Запрос_к_API
       Запрос_к_API --> Извлечение_данных
       Извлечение_данных --> Формирование_JavaScript
       Формирование_JavaScript --> Выполнение_JavaScript
       Выполнение_JavaScript --> Формирование_JSON
       Формирование_JSON --> Кодирование_base64
       Кодирование_base64 --> Конец
    """
```

#### `get_default_params`

```python
def get_default_params(self, model_id: str):
    """
    Возвращает параметры по умолчанию для указанной модели.

    Args:
        model_id (str): Идентификатор модели.

    Returns:
        dict: Словарь параметров по умолчанию.

    Как работает функция:

    1. **Извлечение параметров модели**: Из словаря `vercel_models` извлекаются параметры для указанной модели.
    2. **Формирование словаря параметров**: Формируется словарь, содержащий только значения параметров.

    flowchart ascii:

       Начало --> Извлечение_параметров
       Извлечение_параметров --> Формирование_словаря
       Формирование_словаря --> Конец
    """
```

#### `generate`

```python
def generate(self, model_id: str, prompt: str, params: dict = {}):
    """
    Генерирует текст с использованием указанной модели и параметров.

    Args:
        model_id (str): Идентификатор модели для генерации текста.
        prompt (str): Входной текст (prompt) для генерации.
        params (dict, optional): Дополнительные параметры для передачи в модель. По умолчанию {}.

    Yields:
        str: Токены сгенерированного текста.

    Как работает функция:

    1. **Определение ID модели**: Если в `model_id` нет символа ':', то происходит его поиск в словаре `models`.
    2. **Получение параметров по умолчанию**: Получаются параметры по умолчанию для указанной модели с помощью функции `get_default_params`.
    3. **Формирование payload**: Объединяются параметры по умолчанию, переданные параметры и prompt в словарь `payload`.
    4. **Формирование заголовков**: Формируются заголовки HTTP-запроса, включая токен авторизации.
    5. **Инициализация очереди и переменных**: Инициализируется очередь `chunks_queue` для хранения чанков ответа, а также переменные `error` и `response`.
    6. **Определение callback-функции**: Определяется функция `callback`, которая будет вызываться при получении чанков ответа.
    7. **Создание и запуск потока запроса**: Создается и запускается поток `request_thread`, который выполняет POST-запрос к API Vercel.
    8. **Обработка потокового ответа**: В цикле из очереди `chunks_queue` извлекаются чанки ответа, и каждый чанк добавляется к тексту `text`.
    9. **Разделение на строки и извлечение новых слов**: Текст разделяется на строки, и извлекаются новые слова.
    10. **Генерация токенов**: Для каждого нового слова генерируется токен, который возвращается вызывающей стороне.

    flowchart ascii:

       Начало --> Определение_ID_модели
       Определение_ID_модели --> Получение_параметров_по_умолчанию
       Получение_параметров_по_умолчанию --> Формирование_payload
       Формирование_payload --> Формирование_заголовков
       Формирование_заголовков --> Инициализация_очереди
       Инициализация_очереди --> Создание_и_запуск_потока
       Создание_и_запуск_потока --> Обработка_потокового_ответа
       Обработка_потокового_ответа --> Разделение_на_строки
       Разделение_на_строки --> Генерация_токенов
       Генерация_токенов --> Конец
    """
```

## Переменные

### `url`

```python
url: str = 'https://play.vercel.ai'
```

URL для взаимодействия с Vercel API.

### `supports_stream`

```python
supports_stream: bool = True
```

Флаг, указывающий, поддерживается ли потоковая передача данных.

### `needs_auth`

```python
needs_auth: bool = False
```

Флаг, указывающий, требуется ли аутентификация.

### `models`

```python
models: Dict[str, str] = {
    'claude-instant-v1': 'anthropic:claude-instant-v1',
    'claude-v1': 'anthropic:claude-v1',
    'alpaca-7b': 'replicate:replicate/alpaca-7b',
    'stablelm-tuned-alpha-7b': 'replicate:stability-ai/stablelm-tuned-alpha-7b',
    'bloom': 'huggingface:bigscience/bloom',
    'bloomz': 'huggingface:bigscience/bloomz',
    'flan-t5-xxl': 'huggingface:google/flan-t5-xxl',
    'flan-ul2': 'huggingface:google/flan-ul2',
    'gpt-neox-20b': 'huggingface:EleutherAI/gpt-neox-20b',
    'oasst-sft-4-pythia-12b-epoch-3.5': 'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5',
    'santacoder': 'huggingface:bigcode/santacoder',
    'command-medium-nightly': 'cohere:command-medium-nightly',
    'command-xlarge-nightly': 'cohere:command-xlarge-nightly',
    'code-cushman-001': 'openai:code-cushman-001',
    'code-davinci-002': 'openai:code-davinci-002',
    'gpt-3.5-turbo': 'openai:gpt-3.5-turbo',
    'text-ada-001': 'openai:text-ada-001',
    'text-babbage-001': 'openai:text-babbage-001',
    'text-curie-001': 'openai:text-curie-001',
    'text-davinci-002': 'openai:text-davinci-002',
    'text-davinci-003': 'openai:text-davinci-003'
}
```

Словарь, содержащий соответствия между идентификаторами моделей и их полными именами.

### `model`

```python
model: KeysView[str] = models.keys()
```

Список ключей словаря `models`, представляющий доступные модели.

### `vercel_models`

```python
vercel_models: Dict[str, Dict[str, str | int | float | list | dict]] = {
    'anthropic:claude-instant-v1': {'id': 'anthropic:claude-instant-v1', 'provider': 'anthropic', 'providerHumanName': 'Anthropic', 'makerHumanName': 'Anthropic', 'minBillingTier': 'hobby', 'parameters': {'temperature': {'value': 1, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': ['\\n\\nHuman:'], 'range': []}}, 'name': 'claude-instant-v1'},
    'anthropic:claude-v1': {'id': 'anthropic:claude-v1', 'provider': 'anthropic', 'providerHumanName': 'Anthropic', 'makerHumanName': 'Anthropic', 'minBillingTier': 'hobby', 'parameters': {'temperature': {'value': 1, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': ['\\n\\nHuman:'], 'range': []}}, 'name': 'claude-v1'},
    'replicate:replicate/alpaca-7b': {'id': 'replicate:replicate/alpaca-7b', 'provider': 'replicate', 'providerHumanName': 'Replicate', 'makerHumanName': 'Stanford', 'parameters': {'temperature': {'value': 0.75, 'range': [0.01, 5]}, 'maximumLength': {'value': 200, 'range': [50, 512]}, 'topP': {'value': 0.95, 'range': [0.01, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'repetitionPenalty': {'value': 1.1765, 'range': [0.01, 5]}, 'stopSequences': {'value': [], 'range': []}}, 'version': '2014ee1247354f2e81c0b3650d71ca715bc1e610189855f134c30ecb841fae21', 'name': 'alpaca-7b'},
    'replicate:stability-ai/stablelm-tuned-alpha-7b': {'id': 'replicate:stability-ai/stablelm-tuned-alpha-7b', 'provider': 'replicate', 'makerHumanName': 'StabilityAI', 'providerHumanName': 'Replicate', 'parameters': {'temperature': {'value': 0.75, 'range': [0.01, 5]}, 'maximumLength': {'value': 200, 'range': [50, 512]}, 'topP': {'value': 0.95, 'range': [0.01, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'repetitionPenalty': {'value': 1.1765, 'range': [0.01, 5]}, 'stopSequences': {'value': [], 'range': []}}, 'version': '4a9a32b4fd86c2d047f1d271fa93972683ec6ef1cf82f402bd021f267330b50b', 'name': 'stablelm-tuned-alpha-7b'},
    'huggingface:bigscience/bloom': {'id': 'huggingface:bigscience/bloom', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigScience', 'instructions': "Do NOT talk to Bloom as an entity, it\'s not a chatbot but a webpage/blog/article completion model. For the best results: mimic a few words of a webpage similar to the content you want to generate. Start a sentence as if YOU were writing a blog, webpage, math post, coding article and Bloom will generate a coherent follow-up.", 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'bloom'},
    'huggingface:bigscience/bloomz': {'id': 'huggingface:bigscience/bloomz', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigScience', 'instructions': 'We recommend using the model to perform tasks expressed in natural language. For example, given the prompt "Translate to English: Je t\\\'aime.", the model will most likely answer "I love you.".', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'bloomz'},
    'huggingface:google/flan-t5-xxl': {'id': 'huggingface:google/flan-t5-xxl', 'provider': 'huggingface', 'makerHumanName': 'Google', 'providerHumanName': 'HuggingFace', 'name': 'flan-t5-xxl', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}},
    'huggingface:google/flan-ul2': {'id': 'huggingface:google/flan-ul2', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'Google', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'flan-ul2'},
    'huggingface:EleutherAI/gpt-neox-20b': {'id': 'huggingface:EleutherAI/gpt-neox-20b', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'EleutherAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'gpt-neox-20b'},
    'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5': {'id': 'huggingface:OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'OpenAssistant', 'parameters': {'maximumLength': {'value': 200, 'range': [50, 1024]}, 'typicalP': {'value': 0.2, 'range': [0.1, 0.99]}, 'repetitionPenalty': {'value': 1, 'range': [0.1, 2]}}, 'name': 'oasst-sft-4-pythia-12b-epoch-3.5'},
    'huggingface:bigcode/santacoder': {
        'id': 'huggingface:bigcode/santacoder', 'provider': 'huggingface', 'providerHumanName': 'HuggingFace', 'makerHumanName': 'BigCode', 'instructions': 'The model was trained on GitHub code. As such it is not an instruction model and commands like "Write a function that computes the square root." do not work well. You should phrase commands like they occur in source code such as comments (e.g. # the following function computes the sqrt) or write a function signature and docstring and let the model complete the function body.', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 0.95, 'range': [0.01, 0.99]}, 'topK': {'value': 4, 'range': [1, 500]}, 'repetitionPenalty': {'value': 1.03, 'range': [0.1, 2]}}, 'name': 'santacoder'},
    'cohere:command-medium-nightly': {'id': 'cohere:command-medium-nightly', 'provider': 'cohere', 'providerHumanName': 'Cohere', 'makerHumanName': 'Cohere', 'name': 'command-medium-nightly', 'parameters': {'temperature': {'value': 0.9, 'range': [0, 2]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0, 1]}, 'topK': {'value': 0, 'range': [0, 500]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'cohere:command-xlarge-nightly': {'id': 'cohere:command-xlarge-nightly', 'provider': 'cohere', 'providerHumanName': 'Cohere', 'makerHumanName': 'Cohere', 'name': 'command-xlarge-nightly', 'parameters': {'temperature': {'value': 0.9, 'range': [0, 2]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0, 1]}, 'topK': {'value': 0, 'range': [0, 500]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:gpt-4': {'id': 'openai:gpt-4', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'gpt-4', 'minBillingTier': 'pro', 'parameters': {'temperature': {'value': 0.7, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:code-cushman-001': {'id': 'openai:code-cushman-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'code-cushman-001'},
    'openai:code-davinci-002': {'id': 'openai:code-davinci-002', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'code-davinci-002'},
    'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'parameters': {'temperature': {'value': 0.7, 'range': [0, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'topK': {'value': 1, 'range': [1, 500]}, 'presencePenalty': {'value': 1, 'range': [0, 1]}, 'frequencyPenalty': {'value': 1, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}, 'name': 'gpt-3.5-turbo'},
    'openai:text-ada-001': {'id': 'openai:text-ada-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-ada-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-babbage-001': {'id': 'openai:text-babbage-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-babbage-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-curie-001': {'id': 'openai:text-curie-001', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-curie-001', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-davinci-002': {'id': 'openai:text-davinci-002', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-davinci-002', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}},
    'openai:text-davinci-003': {'id': 'openai:text-davinci-003', 'provider': 'openai', 'providerHumanName': 'OpenAI', 'makerHumanName': 'OpenAI', 'name': 'text-davinci-003', 'parameters': {'temperature': {'value': 0.5, 'range': [0.1, 1]}, 'maximumLength': {'value': 200, 'range': [50, 1024]}, 'topP': {'value': 1, 'range': [0.1, 1]}, 'presencePenalty': {'value': 0, 'range': [0, 1]}, 'frequencyPenalty': {'value': 0, 'range': [0, 1]}, 'stopSequences': {'value': [], 'range': []}}}
}
```

Словарь, содержащий подробную информацию о моделях, размещенных на платформе Vercel, включая их параметры и ограничения.

### `params`

```python
params: str = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    f'({", ".join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])})'
```

Строка, формирующая описание поддерживаемых параметров функции `_create_completion`.