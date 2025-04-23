# Документация для модуля GlhfChat

## Обзор

Модуль `GlhfChat.py` является частью проекта `hypotez` и предназначен для работы с сервисом GlhfChat, предоставляющим доступ к различным моделям искусственного интеллекта. Он наследует функциональность от класса `OpenaiTemplate` и содержит специфические настройки для взаимодействия с API GlhfChat.

## Подробнее

Модуль определяет URL для доступа к сервису, URL для авторизации, базовый URL для API, а также список поддерживаемых моделей. Также указывается, что для работы с сервисом требуется авторизация.

## Классы

### `GlhfChat`

**Описание**: Класс `GlhfChat` предназначен для взаимодействия с сервисом GlhfChat. Он наследуется от `OpenaiTemplate` и содержит настройки, специфичные для данного сервиса.

**Наследует**:

- `OpenaiTemplate`: Предоставляет базовый функционал для работы с API OpenAI-подобных сервисов.

**Атрибуты**:

- `url` (str): URL для доступа к сервису GlhfChat (`https://glhf.chat`).
- `login_url` (str): URL для авторизации в сервисе GlhfChat (`https://glhf.chat/user-settings/api`).
- `api_base` (str): Базовый URL для API GlhfChat (`https://glhf.chat/api/openai/v1`).
- `working` (bool): Флаг, указывающий на работоспособность сервиса (всегда `True`).
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации для работы с сервисом (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию (`hf:meta-llama/Llama-3.3-70B-Instruct`).
- `models` (List[str]): Список поддерживаемых моделей.

**Принцип работы**:

Класс `GlhfChat` переопределяет атрибуты класса `OpenaiTemplate`, чтобы соответствовать особенностям API GlhfChat. Это позволяет использовать общую логику `OpenaiTemplate` для взаимодействия с различными моделями, предоставляемыми GlhfChat.

## Параметры класса

- `url` (str): URL для доступа к сервису GlhfChat.
- `login_url` (str): URL для авторизации в сервисе GlhfChat.
- `api_base` (str): Базовый URL для API GlhfChat.
- `working` (bool): Флаг, указывающий на работоспособность сервиса.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации для работы с сервисом.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

**Примеры**

Пример создания экземпляра класса `GlhfChat`:

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.GlhfChat import GlhfChat

glhf_chat = GlhfChat()
print(glhf_chat.url)
print(glhf_chat.default_model)
```