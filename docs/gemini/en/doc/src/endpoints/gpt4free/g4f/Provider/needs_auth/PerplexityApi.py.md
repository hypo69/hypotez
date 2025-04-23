# Документация для `PerplexityApi.py`

## Обзор

Файл `PerplexityApi.py` определяет класс `PerplexityApi`, который является подклассом `OpenaiTemplate` и предоставляет функциональность для работы с API Perplexity. Этот класс содержит информацию о URL-адресе, требованиях к аутентификации, базовом URL-адресе API и поддерживаемых моделях Perplexity.

## Более подробно

Этот файл содержит конфигурацию для работы с API Perplexity, включая URL-адреса для входа и базовый API, а также список поддерживаемых моделей. Класс `PerplexityApi` наследуется от `OpenaiTemplate`, что позволяет ему использовать общие методы и атрибуты для взаимодействия с API на основе шаблона OpenAI.

## Классы

### `PerplexityApi`

**Описание**: Класс `PerplexityApi` предоставляет интерфейс для взаимодействия с API Perplexity, наследуясь от `OpenaiTemplate`.

**Наследует**:
- `OpenaiTemplate`: Обеспечивает базовую функциональность для работы с API, совместимыми с OpenAI.

**Атрибуты**:
- `label` (str): Отображаемое имя провайдера "Perplexity API".
- `url` (str): URL-адрес веб-сайта Perplexity AI ("https://www.perplexity.ai").
- `login_url` (str): URL-адрес страницы настроек API Perplexity ("https://www.perplexity.ai/settings/api").
- `working` (bool): Указывает, работает ли данный API (значение `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с API (значение `True`).
- `api_base` (str): Базовый URL-адрес API Perplexity ("https://api.perplexity.ai").
- `default_model` (str): Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
- `models` (List[str]): Список поддерживаемых моделей Perplexity, включая "llama-3-sonar-small-32k-chat", "llama-3-sonar-large-32k-chat", "llama-3-sonar-large-32k-online", "llama-3-8b-instruct", "llama-3-70b-instruct".

**Принцип работы**:
Класс `PerplexityApi` наследует функциональность от `OpenaiTemplate` и определяет специфические параметры для работы с API Perplexity. Он предоставляет информацию о необходимых URL-адресах, требованиях к аутентификации и поддерживаемых моделях.

## Параметры класса

- `label` (str): Отображаемое имя провайдера "Perplexity API".
- `url` (str): URL-адрес веб-сайта Perplexity AI ("https://www.perplexity.ai").
- `login_url` (str): URL-адрес страницы настроек API Perplexity ("https://www.perplexity.ai/settings/api").
- `working` (bool): Указывает, работает ли данный API (значение `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с API (значение `True`).
- `api_base` (str): Базовый URL-адрес API Perplexity ("https://api.perplexity.ai").
- `default_model` (str): Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
- `models` (List[str]): Список поддерживаемых моделей Perplexity.

## Примеры

Пример определения класса `PerplexityApi`:

```python
from ..template import OpenaiTemplate

class PerplexityApi(OpenaiTemplate):
    label = "Perplexity API"
    url = "https://www.perplexity.ai"
    login_url = "https://www.perplexity.ai/settings/api"
    working = True
    needs_auth = True
    api_base = "https://api.perplexity.ai"
    default_model = "llama-3-sonar-large-32k-online"
    models = [
        "llama-3-sonar-small-32k-chat",
        default_model,
        "llama-3-sonar-large-32k-chat",
        "llama-3-sonar-large-32k-online",
        "llama-3-8b-instruct",
        "llama-3-70b-instruct",
    ]