# Модуль PerplexityApi

## Обзор

Модуль `PerplexityApi` предоставляет класс для взаимодействия с API Perplexity AI. Он наследуется от класса `OpenaiTemplate` и предназначен для упрощения интеграции с различными моделями Perplexity, такими как `llama-3-sonar-large-32k-online`.

## Подробней

Этот модуль является частью системы `gpt4free` в проекте `hypotez` и используется для работы с API Perplexity AI. Он предоставляет удобный интерфейс для аутентификации и выбора моделей, поддерживаемых Perplexity.

## Классы

### `PerplexityApi`

**Описание**: Класс для взаимодействия с API Perplexity AI.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера API ("Perplexity API").
- `url` (str): URL главной страницы Perplexity AI ("https://www.perplexity.ai").
- `login_url` (str): URL страницы настроек API для получения ключа ("https://www.perplexity.ai/settings/api").
- `working` (bool): Указывает, работает ли данный API (значение `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для доступа к API (значение `True`).
- `api_base` (str): Базовый URL для API Perplexity AI ("https://api.perplexity.ai").
- `default_model` (str): Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
- `models` (List[str]): Список поддерживаемых моделей.

**Принцип работы**:
Класс `PerplexityApi` наследует функциональность от `OpenaiTemplate` и переопределяет некоторые атрибуты, чтобы соответствовать особенностям API Perplexity AI. Он определяет базовый URL, список поддерживаемых моделей и необходимость аутентификации.

## Параметры класса

- `label` (str): Метка, идентифицирующая провайдера API.
- `url` (str): URL главной страницы Perplexity AI.
- `login_url` (str): URL страницы настроек API для получения ключа.
- `working` (bool): Указывает, работает ли данный API.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для доступа к API.
- `api_base` (str): Базовый URL для API Perplexity AI.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

## Примеры

```python
from g4f.Provider import PerplexityApi

# Создание экземпляра класса PerplexityApi
perplexity_api = PerplexityApi()

# Проверка атрибутов
print(f"Label: {perplexity_api.label}")
print(f"Default model: {perplexity_api.default_model}")
print(f"Needs auth: {perplexity_api.needs_auth}")