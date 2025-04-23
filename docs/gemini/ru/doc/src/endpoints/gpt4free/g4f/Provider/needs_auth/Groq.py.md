# Модуль Groq

## Обзор

Модуль `Groq.py` предназначен для работы с провайдером Groq в рамках проекта `hypotez`. Он определяет класс `Groq`, который наследуется от `OpenaiTemplate` и содержит специфические настройки для взаимодействия с API Groq.

## Подробнее

Этот модуль содержит конфигурацию, необходимую для подключения и использования Groq в качестве одного из поставщиков услуг. Включает URL, базовый адрес API, флаги для аутентификации и список моделей, поддерживаемых Groq.

## Классы

### `Groq`

**Описание**: Класс `Groq` предоставляет настройки для работы с API Groq.

**Наследует**:

- `OpenaiTemplate`: Наследует базовые атрибуты и методы класса `OpenaiTemplate`.

**Атрибуты**:

- `url` (str): URL для доступа к playground Groq: `"https://console.groq.com/playground"`.
- `login_url` (str): URL для получения ключей API Groq: `"https://console.groq.com/keys"`.
- `api_base` (str): Базовый URL для API Groq: `"https://api.groq.com/openai/v1"`.
- `working` (bool): Указывает, что провайдер Groq в настоящее время функционирует: `True`.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с Groq: `True`.
- `default_model` (str): Модель, используемая по умолчанию: `"mixtral-8x7b-32768"`.
- `fallback_models` (List[str]): Список запасных моделей, используемых в случае недоступности основной модели.
- `model_aliases` (dict): Словарь псевдонимов моделей для совместимости.

**Принцип работы**:

Класс `Groq` содержит статические атрибуты, определяющие параметры подключения к сервису Groq. При инициализации класса, эти атрибуты могут быть использованы для настройки API клиента. Флаг `needs_auth` указывает на необходимость аутентификации, что важно для правильной настройки заголовков запроса. Список `fallback_models` позволяет переключаться на другие модели в случае проблем с основной моделью.

## Параметры класса

- `url` (str): URL для доступа к playground Groq.
- `login_url` (str): URL для получения ключей API Groq.
- `api_base` (str): Базовый URL для API Groq.
- `working` (bool): Указывает, что провайдер Groq в настоящее время функционирует.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с Groq.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (List[str]): Список запасных моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

## Примеры

Пример использования класса `Groq`:

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.Groq import Groq

groq_provider = Groq()
print(f"URL: {groq_provider.url}")
print(f"API Base: {groq_provider.api_base}")
print(f"Default Model: {groq_provider.default_model}")