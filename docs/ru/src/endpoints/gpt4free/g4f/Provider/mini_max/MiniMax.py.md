# Документация для модуля MiniMax

## Обзор

Модуль `MiniMax` предоставляет класс `MiniMax`, который является наследником `OpenaiTemplate` и предназначен для взаимодействия с API MiniMax. Он содержит информацию о MiniMax API, такую как URL, URL для входа, базовый URL API, флаги работоспособности и аутентификации, а также модели, поддерживаемые MiniMax.

## Подробнее

Модуль определяет параметры для работы с MiniMax API, включая URL, необходимость аутентификации и список поддерживаемых моделей. `MiniMax` используется для интеграции с сервисом MiniMax, предоставляя доступ к его возможностям через стандартизированный интерфейс `OpenaiTemplate`.

## Классы

### `MiniMax`

**Описание**: Класс `MiniMax` предназначен для взаимодействия с API MiniMax.

**Наследует**:
- `OpenaiTemplate`: Наследует базовый функционал шаблона OpenAI.

**Атрибуты**:
- `label` (str): Метка API ("MiniMax API").
- `url` (str): URL сервиса MiniMax ("https://www.hailuo.ai/chat").
- `login_url` (str): URL для входа в MiniMax ("https://intl.minimaxi.com/user-center/basic-information/interface-key").
- `api_base` (str): Базовый URL API MiniMax ("https://api.minimaxi.chat/v1").
- `working` (bool): Флаг, указывающий, работает ли API (True).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True).
- `default_model` (str): Модель по умолчанию ("MiniMax-Text-01").
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (совпадает с `default_model`).
- `models` (list[str]): Список поддерживаемых моделей ([`default_model`, "abab6.5s-chat"]).
- `model_aliases` (dict[str, str]): Псевдонимы моделей ({"MiniMax": `default_model`}).

**Принцип работы**:

Класс `MiniMax` наследует от `OpenaiTemplate`, что позволяет ему использовать общую логику для взаимодействия с API, следуя шаблону, принятому в проекте. Он задаёт специфичные для MiniMax параметры, такие как URL, необходимость аутентификации и список поддерживаемых моделей.

## Параметры класса

- `label` (str): Метка API ("MiniMax API"). Используется для идентификации провайдера.
- `url` (str): URL сервиса MiniMax ("https://www.hailuo.ai/chat"). Ссылка на главную страницу сервиса.
- `login_url` (str): URL для входа в MiniMax ("https://intl.minimaxi.com/user-center/basic-information/interface-key"). Ссылка на страницу получения ключа API.
- `api_base` (str): Базовый URL API MiniMax ("https://api.minimaxi.chat/v1"). Используется для формирования запросов к API.
- `working` (bool): Флаг, указывающий, работает ли API (True). Показывает, доступен ли провайдер для использования.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True). Определяет необходимость авторизации для работы с API.
- `default_model` (str): Модель по умолчанию ("MiniMax-Text-01"). Используется, если модель явно не указана.
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (совпадает с `default_model`). Используется для задач, связанных с обработкой изображений.
- `models` (list[str]): Список поддерживаемых моделей ([`default_model`, "abab6.5s-chat"]). Определяет, какие модели можно использовать через этот класс.
- `model_aliases` (dict[str, str]): Псевдонимы моделей ({"MiniMax": `default_model`}). Позволяет использовать короткие имена для обращения к моделям.

**Примеры**:

```python
from __future__ import annotations
from ..template import OpenaiTemplate

class MiniMax(OpenaiTemplate):
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

# Пример использования атрибутов класса
print(MiniMax.label)
print(MiniMax.api_base)
```