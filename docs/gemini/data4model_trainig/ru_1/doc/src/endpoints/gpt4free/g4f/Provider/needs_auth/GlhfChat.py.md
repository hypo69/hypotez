# Модуль GlhfChat

## Обзор

Модуль `GlhfChat` предоставляет класс `GlhfChat`, который является подклассом `OpenaiTemplate`. Он предназначен для взаимодействия с платформой GLHF Chat, используя API OpenAI. Модуль определяет URL, базовый URL API, флаги для аутентификации и список поддерживаемых моделей.

## Подробней

Модуль `GlhfChat` определяет параметры, необходимые для подключения и взаимодействия с сервисом `glhf.chat`, который использует API OpenAI. Он указывает, что для работы требуется аутентификация и предоставляет список моделей, которые можно использовать. Этот модуль является частью системы, которая позволяет взаимодействовать с различными AI-моделями через единый интерфейс.

## Классы

### `GlhfChat`

**Описание**: Класс `GlhfChat` предназначен для взаимодействия с платформой GLHF Chat через API OpenAI.

**Наследует**:
- `OpenaiTemplate`: Наследует функциональность базового шаблона OpenAI, предоставляя структуру для взаимодействия с API OpenAI.

**Атрибуты**:
- `url` (str): URL платформы GLHF Chat ("https://glhf.chat").
- `login_url` (str): URL для аутентификации на платформе GLHF Chat ("https://glhf.chat/user-settings/api").
- `api_base` (str): Базовый URL API OpenAI на платформе GLHF Chat ("https://glhf.chat/api/openai/v1").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `needs_auth` (bool): Флаг, указывающий, что для работы требуется аутентификация (True).
- `default_model` (str): Модель, используемая по умолчанию ("hf:meta-llama/Llama-3.3-70B-Instruct").
- `models` (List[str]): Список поддерживаемых моделей.

**Принцип работы**:
Класс `GlhfChat` настраивает параметры подключения к платформе GLHF Chat, которая использует API OpenAI. Он определяет URL для подключения, аутентификации и базовый URL API. Также класс содержит флаги, указывающие на необходимость аутентификации и список поддерживаемых моделей.

## Параметры класса

- `url` (str): URL платформы GLHF Chat. Используется для определения адреса сервиса.
- `login_url` (str): URL для аутентификации на платформе GLHF Chat. Используется для получения токена аутентификации.
- `api_base` (str): Базовый URL API OpenAI на платформе GLHF Chat. Используется для формирования запросов к API.
- `working` (bool): Флаг, указывающий, что провайдер работает. Используется для определения доступности сервиса.
- `needs_auth` (bool): Флаг, указывающий, что для работы требуется аутентификация. Используется для проверки необходимости выполнения процедуры аутентификации перед использованием API.
- `default_model` (str): Модель, используемая по умолчанию. Используется, если пользователь не указал конкретную модель.
- `models` (List[str]): Список поддерживаемых моделей. Используется для предоставления пользователю выбора доступных моделей.

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