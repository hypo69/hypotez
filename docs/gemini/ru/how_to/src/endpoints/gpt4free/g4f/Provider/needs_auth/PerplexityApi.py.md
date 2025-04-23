### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `PerplexityApi`, который наследуется от `OpenaiTemplate`. Он содержит конфигурацию для работы с API Perplexity AI, включая URL, информацию об аутентификации, базовый URL API и список поддерживаемых моделей. Класс предназначен для интеграции с системой, использующей шаблоны OpenAI для взаимодействия с различными API.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется `OpenaiTemplate` из `..template`.

2. **Определение класса `PerplexityApi`**:
   - Создается класс `PerplexityApi`, наследуемый от `OpenaiTemplate`.
   - Устанавливаются атрибуты класса:
     - `label`: Отображаемое имя API ("Perplexity API").
     - `url`: URL веб-сайта Perplexity AI.
     - `login_url`: URL страницы настроек API для получения ключа.
     - `working`: Логическое значение, указывающее, работает ли API (в данном случае `True`).
     - `needs_auth`: Логическое значение, указывающее, требуется ли аутентификация для работы с API (в данном случае `True`).
     - `api_base`: Базовый URL API Perplexity AI.
     - `default_model`: Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
     - `models`: Список поддерживаемых моделей API.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.template import OpenaiTemplate
from src.endpoints.gpt4free.g4f.Provider.needs_auth import PerplexityApi

# Создание экземпляра класса PerplexityApi
perplexity_api = PerplexityApi()

# Вывод информации о Perplexity API
print(f"Label: {perplexity_api.label}")
print(f"URL: {perplexity_api.url}")
print(f"Login URL: {perplexity_api.login_url}")
print(f"Working: {perplexity_api.working}")
print(f"Needs Auth: {perplexity_api.needs_auth}")
print(f"API Base: {perplexity_api.api_base}")
print(f"Default Model: {perplexity_api.default_model}")
print(f"Models: {perplexity_api.models}")

# Пример использования атрибутов для настройки запросов к API
api_label = perplexity_api.label
api_base_url = perplexity_api.api_base
default_model = perplexity_api.default_model

print(f"Используем API: {api_label}")
print(f"Базовый URL API: {api_base_url}")
print(f"Модель по умолчанию: {default_model}")