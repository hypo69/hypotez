# Модуль: `claude.py`

## Обзор

Модуль `claude.py` предоставляет клиент для взаимодействия с API Claude от Anthropic. Он содержит класс `ClaudeClient`, который позволяет генерировать текст, анализировать тональность и переводить текст с использованием модели Claude.

## Подробней

Этот модуль упрощает взаимодействие с сервисами Claude, предоставляя удобный интерфейс для выполнения различных задач обработки текста. Класс `ClaudeClient` инициализируется с использованием API-ключа и предоставляет методы для генерации текста на основе запроса, анализа тональности текста и перевода текста с одного языка на другой.

## Классы

### `ClaudeClient`

**Описание**:
Класс `ClaudeClient` предоставляет интерфейс для взаимодействия с API Claude от Anthropic.

**Атрибуты**:
- `client` (anthropic.Client): Клиент Anthropic, используемый для выполнения запросов к API Claude.

**Методы**:
- `__init__(api_key: str) -> None`: Инициализирует клиент Claude с предоставленным API-ключом.
- `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе предоставленного запроса.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность предоставленного текста.
- `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит предоставленный текст с исходного языка на целевой язык.

#### `__init__`

```python
def __init__(self, api_key: str) -> None:
    """
    Инициализирует клиент Claude с предоставленным API-ключом.

    Args:
        api_key (str): API-ключ для доступа к сервисам Claude.

    Example:
        >>> claude_client = ClaudeClient('your_api_key')
    """
```

**Назначение**:
Инициализация экземпляра класса `ClaudeClient`.

**Параметры**:
- `api_key` (str): API-ключ, используемый для аутентификации и авторизации при взаимодействии с API Claude.

**Принцип работы**:
- Функция инициализирует клиент Anthropic с предоставленным API-ключом. Этот клиент будет использоваться для выполнения запросов к API Claude.

**Примеры**:

```python
claude_client = ClaudeClient('your_api_key')
```

#### `generate_text`

```python
def generate_text(self, prompt: str, max_tokens_to_sample: int = 100) -> str:
    """
    Генерирует текст на основе предоставленного запроса.

    Args:
        prompt (str): Запрос для генерации текста.
        max_tokens_to_sample (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

    Returns:
        str: Сгенерированный текст.

    Example:
        >>> claude_client.generate_text('Write a short story.')
        'A short story about...'
    """
```

**Назначение**:
Генерация текста с использованием API Claude на основе предоставленного запроса.

**Параметры**:
- `prompt` (str): Текст запроса, на основе которого генерируется новый текст.
- `max_tokens_to_sample` (int, optional): Максимальное количество токенов, которое может быть сгенерировано. По умолчанию равно 100.

**Возвращает**:
- `str`: Сгенерированный текст.

**Принцип работы**:
- Функция отправляет запрос к API Claude с предоставленным запросом и параметрами генерации.
- Полученный ответ содержит сгенерированный текст, который возвращается функцией.

**Примеры**:

```python
claude_client.generate_text('Write a short story about a robot learning to love.')
```

#### `analyze_sentiment`

```python
def analyze_sentiment(self, text: str) -> str:
    """
    Анализирует тональность предоставленного текста.

    Args:
        text (str): Текст для анализа.

    Returns:
        str: Результат анализа тональности.

    Example:
        >>> claude_client.analyze_sentiment('I am very happy!')
        'Positive'
    """
```

**Назначение**:
Анализ тональности предоставленного текста с использованием API Claude.

**Параметры**:
- `text` (str): Текст, который необходимо проанализировать на предмет тональности.

**Возвращает**:
- `str`: Результат анализа тональности текста (например, "Positive", "Negative" или "Neutral").

**Принцип работы**:
- Функция отправляет запрос к API Claude с текстом для анализа тональности.
- API Claude анализирует текст и возвращает результат анализа, который затем возвращается функцией.

**Примеры**:

```python
claude_client.analyze_sentiment('I am very happy today!')
```

#### `translate_text`

```python
def translate_text(self, text: str, source_language: str, target_language: str) -> str:
    """
    Переводит предоставленный текст с исходного языка на целевой язык.

    Args:
        text (str): Текст для перевода.
        source_language (str): Код исходного языка.
        target_language (str): Код целевого языка.

    Returns:
        str: Переведенный текст.

    Example:
        >>> claude_client.translate_text('Hello', 'en', 'es')
        'Hola'
    """
```

**Назначение**:
Перевод текста с одного языка на другой с использованием API Claude.

**Параметры**:
- `text` (str): Текст, который необходимо перевести.
- `source_language` (str): Код языка, с которого нужно перевести текст (например, 'en' для английского).
- `target_language` (str): Код языка, на который нужно перевести текст (например, 'es' для испанского).

**Возвращает**:
- `str`: Переведенный текст.

**Принцип работы**:
- Функция отправляет запрос к API Claude с текстом, исходным языком и целевым языком.
- API Claude переводит текст и возвращает переведенный текст, который затем возвращается функцией.

**Примеры**:

```python
claude_client.translate_text('Hello, how are you?', 'en', 'es')