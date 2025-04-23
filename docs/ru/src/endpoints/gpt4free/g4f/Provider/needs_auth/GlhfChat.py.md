# Модуль `GlhfChat`

## Обзор

Модуль `GlhfChat` представляет собой класс, предназначенный для взаимодействия с сервисом `glhf.chat`. Он наследует функциональность от класса `OpenaiTemplate` и предоставляет специфические настройки для работы с этим провайдером, включая URL, базовый API, информацию об аутентификации и список поддерживаемых моделей.

## Подробнее

Модуль определяет базовые параметры для взаимодействия с провайдером `glhf.chat`. Он указывает, что для работы требуется аутентификация (`needs_auth = True`) и предоставляет список моделей, доступных для использования через этот сервис.

## Классы

### `GlhfChat`

**Описание**: Класс `GlhfChat` расширяет `OpenaiTemplate` для обеспечения взаимодействия с сервисом `glhf.chat`.

**Наследует**:
- `OpenaiTemplate`: Предоставляет базовую структуру для работы с API, совместимыми с OpenAI.

**Атрибуты**:
- `url` (str): URL для доступа к сервису `glhf.chat`.
- `login_url` (str): URL для аутентификации на сервисе `glhf.chat`.
- `api_base` (str): Базовый URL для API `glhf.chat`.
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

**Принцип работы**:
Класс `GlhfChat` предназначен для настройки специфических параметров, необходимых для взаимодействия с API `glhf.chat`. Он наследует общую логику работы с API от `OpenaiTemplate` и переопределяет атрибуты, специфичные для данного провайдера.

## Методы класса

У класса `GlhfChat` нет явно определенных методов, кроме атрибутов класса. Однако, он наследует методы от `OpenaiTemplate`.

## Параметры класса

- `url` (str): URL для доступа к сервису `glhf.chat`.
- `login_url` (str): URL для аутентификации на сервисе `glhf.chat`.
- `api_base` (str): Базовый URL для API `glhf.chat`.
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером.
- `default_model` (str): Модель, используемая по умолчанию ("hf:meta-llama/Llama-3.3-70B-Instruct").
- `models` (List[str]): Список поддерживаемых моделей, включающий различные модели от "hf:meta-llama/Llama-3.1-405B-Instruct" до "hf:nvidia/Llama-3.1-Nemotron-70B-Instruct-HF".

## Примеры

```python
from __future__ import annotations

from ..template import OpenaiTemplate

class GlhfChat(OpenaiTemplate):
    url = "https://glhf.chat"
    login_url = "https://glhf.chat/user-settings/api"
    api_base = "https://glhf.chat/api/openai/v1"

    working = True
    needs_auth = True

    default_model = "hf:meta-llama/Llama-3.3-70B-Instruct"
    models = ["hf:meta-llama/Llama-3.1-405B-Instruct", default_model, "hf:deepseek-ai/DeepSeek-V3", "hf:Qwen/QwQ-32B-Preview", "hf:huihui-ai/Llama-3.3-70B-Instruct-abliterated", "hf:anthracite-org/magnum-v4-12b", "hf:meta-llama/Llama-3.1-70B-Instruct", "hf:meta-llama/Llama-3.1-8B-Instruct", "hf:meta-llama/Llama-3.2-3B-Instruct", "hf:meta-llama/Llama-3.2-11B-Vision-Instruct", "hf:meta-llama/Llama-3.2-90B-Vision-Instruct", "hf:Qwen/Qwen2.5-72B-Instruct", "hf:Qwen/Qwen2.5-Coder-32B-Instruct", "hf:google/gemma-2-9b-it", "hf:google/gemma-2-27b-it", "hf:mistralai/Mistral-7B-Instruct-v0.3", "hf:mistralai/Mixtral-8x7B-Instruct-v0.1", "hf:mistralai/Mixtral-8x22B-Instruct-v0.1", "hf:NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", "hf:Qwen/Qwen2.5-7B-Instruct", "hf:upstage/SOLAR-10.7B-Instruct-v1.0", "hf:nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"]