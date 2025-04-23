# Документация для модуля Groq

## Обзор

Модуль `Groq.py` предназначен для работы с провайдером Groq в рамках проекта `hypotez`. Он наследует функциональность от класса `OpenaiTemplate` и содержит специфические параметры и настройки, необходимые для взаимодействия с API Groq. Модуль определяет URL, точки входа для логина и базовый URL API, а также список поддерживаемых моделей.

## More details

Модуль содержит настройки для работы с API Groq, включая URL, точки входа для логина и базовый URL API. Он также предоставляет список поддерживаемых моделей и их алиасов. Этот модуль используется для настройки шаблона OpenAI для конкретного провайдера Groq.

## Classes

### `Groq`

**Description**: Класс `Groq` наследуется от `OpenaiTemplate` и предназначен для настройки и использования API Groq.

**Inherits**:
- `OpenaiTemplate`: Предоставляет базовый шаблон для работы с API OpenAI.

**Attributes**:
- `url` (str): URL для доступа к playground Groq.
- `login_url` (str): URL для страницы логина Groq.
- `api_base` (str): Базовый URL для API Groq.
- `working` (bool): Указывает, является ли провайдер рабочим (в данном случае `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (в данном случае `True`).
- `default_model` (str): Модель, используемая по умолчанию (`mixtral-8x7b-32768`).
- `fallback_models` (List[str]): Список резервных моделей, которые можно использовать.
- `model_aliases` (dict): Словарь с алиасами моделей для удобства использования.

**Working principle**:
Класс `Groq` переопределяет атрибуты класса `OpenaiTemplate`, чтобы предоставить конкретные настройки для работы с API Groq. Это позволяет использовать стандартные методы `OpenaiTemplate` с параметрами, специфичными для Groq.

## Class Parameters

- `url` (str): URL для доступа к playground Groq.
- `login_url` (str): URL для страницы логина Groq.
- `api_base` (str): Базовый URL для API Groq.
- `working` (bool): Флаг, указывающий, что провайдер работает.
- `needs_auth` (bool): Флаг, указывающий, что требуется аутентификация.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (List[str]): Список резервных моделей.
- `model_aliases` (dict): Алиасы моделей.

```python
class Groq(OpenaiTemplate):
    """
    Класс для настройки и использования API Groq.

    Inherits:
        OpenaiTemplate: Предоставляет базовый шаблон для работы с API OpenAI.

    Attributes:
        url (str): URL для доступа к playground Groq.
        login_url (str): URL для страницы логина Groq.
        api_base (str): Базовый URL для API Groq.
        working (bool): Указывает, является ли провайдер рабочим (в данном случае `True`).
        needs_auth (bool): Указывает, требуется ли аутентификация для использования провайдера (в данном случае `True`).
        default_model (str): Модель, используемая по умолчанию ('mixtral-8x7b-32768').
        fallback_models (List[str]): Список резервных моделей, которые можно использовать.
        model_aliases (dict): Словарь с алиасами моделей для удобства использования.
    """
    url = "https://console.groq.com/playground"
    login_url = "https://console.groq.com/keys"
    api_base = "https://api.groq.com/openai/v1"
    working = True
    needs_auth = True
    default_model = "mixtral-8x7b-32768"
    fallback_models = [
        "distil-whisper-large-v3-en",
        "gemma2-9b-it",
        "gemma-7b-it",
        "llama3-groq-70b-8192-tool-use-preview",
        "llama3-groq-8b-8192-tool-use-preview",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-1b-preview",
        "llama-3.2-3b-preview",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview",
        "llama-guard-3-8b",
        "llava-v1.5-7b-4096-preview",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "whisper-large-v3",
        "whisper-large-v3-turbo",
    ]
    model_aliases = {"mixtral-8x7b": "mixtral-8x7b-32768", "llama2-70b": "llama2-70b-4096"}
```