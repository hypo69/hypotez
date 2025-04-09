# Модуль PerplexityApi

## Обзор

Модуль `PerplexityApi` предоставляет класс для взаимодействия с API Perplexity AI. Он наследует функциональность из класса `OpenaiTemplate` и предназначен для упрощения использования моделей Perplexity AI в проекте `hypotez`. Модуль содержит информацию о URL, необходимости аутентификации, базовом URL API, а также список поддерживаемых моделей.

## Подробней

Этот модуль является частью системы `gpt4free` в проекте `hypotez` и отвечает за интеграцию с API Perplexity AI. Он определяет необходимые параметры для аутентификации и выбора модели, а также предоставляет базовые настройки для работы с API Perplexity AI. Расположение модуля в подкаталоге `needs_auth` указывает на то, что для использования API требуется аутентификация.

## Классы

### `PerplexityApi`

**Описание**: Класс `PerplexityApi` предназначен для работы с API Perplexity AI. Он наследует настройки и методы от класса `OpenaiTemplate` и предоставляет специфические параметры для Perplexity AI, такие как URL, необходимость аутентификации, базовый URL API и список поддерживаемых моделей.

**Наследует**:
- `OpenaiTemplate`: Класс, предоставляющий общую структуру и функциональность для работы с API OpenAI-подобных моделей.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера как "Perplexity API".
- `url` (str): URL веб-сайта Perplexity AI.
- `login_url` (str): URL страницы настроек API для получения ключа API.
- `working` (bool): Флаг, указывающий, что API в настоящее время работает.
- `needs_auth` (bool): Флаг, указывающий, что для доступа к API требуется аутенентификация.
- `api_base` (str): Базовый URL для API Perplexity AI.
- `default_model` (str): Модель, используемая по умолчанию, `"llama-3-sonar-large-32k-online"`.
- `models` (List[str]): Список поддерживаемых моделей Perplexity AI.

**Методы**:
- Отсутствуют, поскольку класс наследует методы от `OpenaiTemplate`.

**Принцип работы**:
1. Класс `PerplexityApi` наследует атрибуты и методы от `OpenaiTemplate`, что позволяет использовать общую логику для работы с API.
2. Определяются специфичные для Perplexity AI атрибуты, такие как URL, базовый URL API и список поддерживаемых моделей.
3. При создании экземпляра класса `PerplexityApi` используются эти атрибуты для настройки соединения и взаимодействия с API Perplexity AI.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.PerplexityApi import PerplexityApi

# Создание экземпляра класса PerplexityApi
perplexity_api = PerplexityApi()

# Вывод базовой информации
print(f"Label: {perplexity_api.label}")
print(f"URL: {perplexity_api.url}")
print(f"API Base: {perplexity_api.api_base}")
print(f"Default Model: {perplexity_api.default_model}")
print(f"Needs Auth: {perplexity_api.needs_auth}")