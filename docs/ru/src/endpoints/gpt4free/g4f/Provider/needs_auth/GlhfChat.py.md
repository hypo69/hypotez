# Модуль GlhfChat

## Обзор

Модуль `GlhfChat` предоставляет класс `GlhfChat`, который является подклассом `OpenaiTemplate` и предназначен для взаимодействия с сервисом Glhf.chat. Он определяет URL-адреса, необходимые для входа в систему и взаимодействия с API, а также указывает, что для работы требуется аутентификация. Модуль также определяет список поддерживаемых моделей.

## Подробней

Этот модуль является частью системы g4f (gpt4free) и обеспечивает возможность использования моделей Glhf.chat. Он содержит URL-адреса для доступа к API Glhf.chat, определяет, что для работы с сервисом требуется аутенентификация, и задает список моделей, которые могут быть использованы. Класс `GlhfChat` наследует функциональность от класса `OpenaiTemplate`.

## Классы

### `GlhfChat`

**Описание**: Класс `GlhfChat` предназначен для взаимодействия с сервисом Glhf.chat.

**Наследует**:
- `OpenaiTemplate`: Класс наследует функциональность для работы с API OpenAI и предоставляет базовую структуру для реализации других провайдеров.

**Атрибуты**:
- `url` (str): URL-адрес сервиса Glhf.chat.
- `login_url` (str): URL-адрес для аутентификации на сервисе Glhf.chat.
- `api_base` (str): Базовый URL-адрес для API Glhf.chat.
- `working` (bool): Флаг, указывающий, что провайдер находится в рабочем состоянии. Значение `True`.
- `needs_auth` (bool): Флаг, указывающий, что для работы с провайдером требуется аутентификация. Значение `True`.
- `default_model` (str): Модель, используемая по умолчанию. Значение `hf:meta-llama/Llama-3.3-70B-Instruct`.
- `models` (List[str]): Список поддерживаемых моделей.

## Функции

В данном коде функции отсутствуют. Однако ниже будут описаны атрибуты класса `GlhfChat`.

### `url`

**Назначение**: URL-адрес сервиса Glhf.chat.

**Параметры**:
- Нет.

**Возвращает**:
- `str`: URL-адрес "https://glhf.chat".

### `login_url`

**Назначение**: URL-адрес для аутентификации на сервисе Glhf.chat.

**Параметры**:
- Нет.

**Возвращает**:
- `str`: URL-адрес "https://glhf.chat/user-settings/api".

### `api_base`

**Назначение**: Базовый URL-адрес для API Glhf.chat.

**Параметры**:
- Нет.

**Возвращает**:
- `str`: URL-адрес "https://glhf.chat/api/openai/v1".

### `working`

**Назначение**: Флаг, указывающий, что провайдер находится в рабочем состоянии.

**Параметры**:
- Нет.

**Возвращает**:
- `bool`: Значение `True`.

### `needs_auth`

**Назначение**: Флаг, указывающий, что для работы с провайдером требуется аутентификация.

**Параметры**:
- Нет.

**Возвращает**:
- `bool`: Значение `True`.

### `default_model`

**Назначение**: Модель, используемая по умолчанию.

**Параметры**:
- Нет.

**Возвращает**:
- `str`: Значение `"hf:meta-llama/Llama-3.3-70B-Instruct"`.

### `models`

**Назначение**: Список поддерживаемых моделей.

**Параметры**:
- Нет.

**Возвращает**:
- `List[str]`: Список поддерживаемых моделей.

**Примеры**:
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