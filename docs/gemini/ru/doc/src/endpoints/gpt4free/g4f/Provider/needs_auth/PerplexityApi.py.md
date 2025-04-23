# Документация модуля PerplexityApi

## Обзор

Модуль `PerplexityApi` предоставляет класс для взаимодействия с API Perplexity AI. Он наследует функциональность от класса `OpenaiTemplate` и предназначен для использования в проекте `hypotez`. Модуль определяет URL-адреса для входа в систему и API, указывает, что требуется аутентификация, и задает список поддерживаемых моделей.

## Подробнее

Этот модуль является частью системы для работы с различными API, предоставляющими доступ к большим языковым моделям. Он позволяет унифицировать взаимодействие с Perplexity AI, используя общие интерфейсы и шаблоны, определенные в `OpenaiTemplate`.

## Классы

### `PerplexityApi`

**Описание**: Класс `PerplexityApi` предназначен для взаимодействия с API Perplexity AI. Он расширяет класс `OpenaiTemplate`, добавляя специфические для Perplexity AI параметры, такие как URL-адреса, требование аутентификации и список поддерживаемых моделей.

**Наследует**:
- `OpenaiTemplate`: Класс, предоставляющий базовый функционал для работы с OpenAI-подобными API.

**Атрибуты**:
- `label` (str): Название провайдера API ("Perplexity API").
- `url` (str): URL главной страницы Perplexity AI.
- `login_url` (str): URL страницы настроек API для получения ключа.
- `working` (bool): Флаг, указывающий, что API работает (True).
- `needs_auth` (bool): Флаг, указывающий, что для работы с API требуется аутентификация (True).
- `api_base` (str): Базовый URL для API запросов Perplexity AI.
- `default_model` (str): Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
- `models` (list): Список поддерживаемых моделей Perplexity AI.

**Принцип работы**:
Класс `PerplexityApi` наследует основные методы и атрибуты от `OpenaiTemplate`, такие как методы для отправки запросов к API и обработки ответов. Он переопределяет или добавляет атрибуты, специфичные для Perplexity AI, чтобы обеспечить правильную конфигурацию и взаимодействие с этим API. Флаг `needs_auth = True` указывает, что для использования этого класса необходимо предоставить учетные данные.

## Методы класса
В данном классе не определены собственные методы, однако он наследует методы от класса `OpenaiTemplate`.

## Параметры класса

- `label` (str): Отображаемое имя провайдера API. В данном случае "Perplexity API".
- `url` (str): URL-адрес веб-сайта Perplexity AI.
- `login_url` (str): URL-адрес для входа или получения API-ключа Perplexity AI.
- `working` (bool): Логическое значение, указывающее, работает ли API в данный момент. Установлено в `True`.
- `needs_auth` (bool): Логическое значение, указывающее, требуется ли аутентификация для использования API. Установлено в `True`.
- `api_base` (str): Базовый URL для API запросов Perplexity AI.
- `default_model` (str): Имя модели, используемой по умолчанию, если не указана другая.
- `models` (list): Список поддерживаемых моделей Perplexity AI.

**Примеры**:

```python
from __future__ import annotations

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
```
В этом примере показано определение класса `PerplexityApi` с указанием всех необходимых атрибутов для взаимодействия с API Perplexity AI.