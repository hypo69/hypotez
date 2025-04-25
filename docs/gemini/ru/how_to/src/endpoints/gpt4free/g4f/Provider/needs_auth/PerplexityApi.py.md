## Как использовать блок кода `PerplexityApi`
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `PerplexityApi`, который представляет собой API для взаимодействия с сервисом Perplexity.ai.  Класс наследуется от `OpenaiTemplate`, предоставляя базовую функциональность для работы с API.

Шаги выполнения
-------------------------
1. Определяется название API `label = "Perplexity API"`.
2. Задается URL адрес сервиса `url = "https://www.perplexity.ai"`.
3. Указывается URL для входа в аккаунт `login_url = "https://www.perplexity.ai/settings/api"`.
4. Устанавливается статус работоспособности API `working = True`.
5. Указывается, требуется ли авторизация `needs_auth = True`.
6. Определяется базовый URL для API `api_base = "https://api.perplexity.ai"`.
7. Указывается модель по умолчанию `default_model = "llama-3-sonar-large-32k-online"`.
8. Создается список доступных моделей `models`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth import PerplexityApi

# Создаем экземпляр PerplexityApi
perplexity_api = PerplexityApi()

# Получаем базовый URL для API
api_base = perplexity_api.api_base

# Проверяем статус работоспособности API
is_working = perplexity_api.working

# Проверяем, требуется ли авторизация для API
needs_auth = perplexity_api.needs_auth

# Получаем список доступных моделей
available_models = perplexity_api.models
```