# Модуль `DeepInfraChat.py`

## Обзор

Модуль `DeepInfraChat.py` предназначен для работы с сервисом DeepInfra Chat. Он предоставляет класс `DeepInfraChat`, который наследуется от `OpenaiTemplate` и содержит настройки для взаимодействия с API DeepInfra. Этот модуль определяет URL, базовый API, список поддерживаемых моделей и псевдонимы моделей.

## Более подробно

Этот модуль используется для интеграции с платформой DeepInfra Chat, позволяя выбирать различные модели для обработки текста и изображений. Он содержит список моделей, доступных для использования, и обеспечивает удобные псевдонимы для упрощения выбора моделей.

## Классы

### `DeepInfraChat`

**Описание**: Класс `DeepInfraChat` предоставляет настройки для работы с API DeepInfra Chat.

**Наследует**:
- `OpenaiTemplate`: Класс, предоставляющий базовые шаблоны для работы с OpenAI-подобными API.

**Атрибуты**:
- `url` (str): URL сервиса DeepInfra Chat (`https://deepinfra.com/chat`).
- `api_base` (str): Базовый URL API DeepInfra (`https://api.deepinfra.com/v1/openai`).
- `working` (bool): Указывает, что сервис работает (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`deepseek-ai/DeepSeek-V3`).
- `default_vision_model` (str): Модель для работы с изображениями, используемая по умолчанию (`openbmb/MiniCPM-Llama3-V-2_5`).
- `vision_models` (list): Список моделей для работы с изображениями, включая модель по умолчанию и `meta-llama/Llama-3.2-90B-Vision-Instruct`.
- `models` (list): Список поддерживаемых моделей, включая модели `meta-llama`, `mistralai`, `deepseek-ai`, `microsoft`, `Qwen`, `01-ai`, `cognitivecomputations`, `databricks`, `deepinfra` и `lizpreciatior`, а также модели для работы с изображениями.
- `model_aliases` (dict): Словарь псевдонимов моделей для упрощения выбора, например, `"llama-3.1-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct"`.

**Принцип работы**:
Класс `DeepInfraChat` определяет основные параметры для взаимодействия с API DeepInfra Chat. Он наследует функциональность от `OpenaiTemplate` и задает специфичные для DeepInfra значения URL, базового API, моделей и псевдонимов моделей. Это позволяет легко настраивать и использовать различные модели, предоставляемые DeepInfra.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

# Пример использования класса DeepInfraChat
deep_infra_chat = DeepInfraChat()
print(f"URL: {deep_infra_chat.url}")
print(f"API Base: {deep_infra_chat.api_base}")
print(f"Default Model: {deep_infra_chat.default_model}")
print(f"Models: {deep_infra_chat.models}")
print(f"Model Aliases: {deep_infra_chat.model_aliases}")