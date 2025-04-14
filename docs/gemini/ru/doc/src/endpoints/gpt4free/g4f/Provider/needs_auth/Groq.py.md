# Модуль Groq

## Обзор

Модуль `Groq.py` предназначен для работы с API Groq, предоставляя интеграцию с моделями Groq, такими как `mixtral-8x7b-32768`. Он наследует функциональность от класса `OpenaiTemplate` и содержит конфигурацию для подключения к сервису Groq. Модуль определяет URL, базовый API, необходимость аутентификации, модели по умолчанию и запасные модели.

## Подробней

Этот модуль является частью подсистемы `gpt4free` в проекте `hypotez`. Он предназначен для упрощения взаимодействия с API Groq. Модуль определяет основные параметры, такие как URL для доступа к API, необходимость аутенентификации и список моделей, доступных для использования. Благодаря наследованию от `OpenaiTemplate`, модуль использует общие механизмы для работы с API, специфичными для Groq.

## Классы

### `Groq`

**Описание**: Класс `Groq` предназначен для настройки и интеграции с API Groq, наследует функциональность от `OpenaiTemplate`.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url` (str): URL для доступа к playground Groq.
- `login_url` (str): URL для страницы получения ключей API Groq.
- `api_base` (str): Базовый URL для API Groq.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `default_model` (str): Модель, используемая по умолчанию, `mixtral-8x7b-32768`.
- `fallback_models` (List[str]): Список запасных моделей для использования.
- `model_aliases` (dict): Словарь с псевдонимами моделей.

**Принцип работы**:
Класс `Groq` настраивает параметры для взаимодействия с API Groq, включая URL, базовый API и список поддерживаемых моделей. Он также указывает на необходимость аутентификации и предоставляет список запасных моделей для обеспечения отказоустойчивости. Использование `OpenaiTemplate` позволяет унифицировать взаимодействие с различными API, включая Groq.

## Параметры класса

- `url` (str): URL для доступа к playground Groq (`https://console.groq.com/playground`).
- `login_url` (str): URL для страницы получения ключей API Groq (`https://console.groq.com/keys`).
- `api_base` (str): Базовый URL для API Groq (`https://api.groq.com/openai/v1`).
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для доступа к API (в данном случае `True`).
- `default_model` (str): Модель, используемая по умолчанию (`mixtral-8x7b-32768`).
- `fallback_models` (List[str]): Список запасных моделей для использования в случае недоступности основной модели.
- `model_aliases` (dict): Словарь с псевдонимами моделей (например, `{"mixtral-8x7b": "mixtral-8x7b-32768", "llama2-70b": "llama2-70b-4096"}`).

## Примеры

Пример использования класса `Groq`:

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq_provider = Groq()
print(f"URL: {groq_provider.url}")
print(f"API Base: {groq_provider.api_base}")
print(f"Default Model: {groq_provider.default_model}")
print(f"Fallback Models: {groq_provider.fallback_models}")