# Модуль MiniMax

## Обзор

Модуль `MiniMax` предоставляет класс `MiniMax`, который является подклассом `OpenaiTemplate` и предназначен для взаимодействия с API MiniMax. Он определяет базовые параметры и настройки для работы с MiniMax API, такие как URL, необходимость авторизации, модели и псевдонимы моделей.

## Подробней

Этот модуль является частью системы интеграции с различными AI-провайдерами. Он предоставляет стандартизированный интерфейс для взаимодействия с API MiniMax, упрощая использование этого API в других частях проекта.

## Классы

### `MiniMax`

**Описание**: Класс `MiniMax` является подклассом `OpenaiTemplate` и предоставляет конкретную реализацию для работы с API MiniMax.

**Наследует**:
- `OpenaiTemplate`: Предоставляет общую структуру и функциональность для взаимодействия с API, подобными OpenAI.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера (MiniMax API).
- `url` (str): URL для доступа к MiniMax API.
- `login_url` (str): URL для страницы авторизации MiniMax.
- `api_base` (str): Базовый URL для API запросов.
- `working` (bool): Указывает, работает ли этот провайдер в данный момент (True).
- `needs_auth` (bool): Указывает, требуется ли авторизация для использования API (True).
- `default_model` (str): Модель, используемая по умолчанию ("MiniMax-Text-01").
- `default_vision_model` (str): Модель для задач, связанных с обработкой изображений (совпадает с `default_model`).
- `models` (list[str]): Список поддерживаемых моделей (["MiniMax-Text-01", "abab6.5s-chat"]).
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей ({"MiniMax": default_model}).

**Принцип работы**:
Класс `MiniMax` наследует от `OpenaiTemplate` и переопределяет атрибуты, специфичные для MiniMax API. Это позволяет использовать общую логику `OpenaiTemplate` для взаимодействия с API MiniMax, но с уникальными параметрами и настройками.

```python
from __future__ import annotations

from ..template import OpenaiTemplate

class MiniMax(OpenaiTemplate):
    """
    Класс для работы с MiniMax API.

    Inherits:
        OpenaiTemplate: Предоставляет общую структуру для взаимодействия с API, подобными OpenAI.

    Attributes:
        label (str): Метка, идентифицирующая провайдера (MiniMax API).
        url (str): URL для доступа к MiniMax API.
        login_url (str): URL для страницы авторизации MiniMax.
        api_base (str): Базовый URL для API запросов.
        working (bool): Указывает, работает ли этот провайдер в данный момент (True).
        needs_auth (bool): Указывает, требуется ли авторизация для использования API (True).
        default_model (str): Модель, используемая по умолчанию ("MiniMax-Text-01").
        default_vision_model (str): Модель для задач, связанных с обработкой изображений (совпадает с `default_model`).
        models (list[str]): Список поддерживаемых моделей (["MiniMax-Text-01", "abab6.5s-chat"]).
        model_aliases (dict[str, str]): Словарь псевдонимов моделей ({"MiniMax": default_model}).
    """
    label = "MiniMax API"
    url = "https://www.hailuo.ai/chat"
    login_url = "https://intl.minimaxi.com/user-center/basic-information/interface-key"
    api_base = "https://api.minimaxi.chat/v1"
    working = True
    needs_auth = True

    default_model = "MiniMax-Text-01"
    default_vision_model = default_model
    models = [default_model, "abab6.5s-chat"]
    model_aliases = {"MiniMax": default_model}