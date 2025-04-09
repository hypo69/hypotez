# Модуль DeepInfraChat для работы с DeepInfra API

## Обзор

Модуль `DeepInfraChat` предназначен для взаимодействия с API DeepInfra. Он наследует функциональность от класса `OpenaiTemplate` и предоставляет специфические настройки для работы с моделями, размещенными на платформе DeepInfra.

## Подробней

Этот модуль содержит информацию о доступных моделях, URL для API и другие параметры, необходимые для правильной работы с DeepInfra. Он определяет модели, которые можно использовать для чата и обработки изображений, а также предоставляет псевдонимы для удобства выбора моделей.

## Классы

### `DeepInfraChat`

**Описание**: Класс `DeepInfraChat` расширяет `OpenaiTemplate` и предоставляет конфигурацию для работы с моделями DeepInfra.

**Наследует**:

- `OpenaiTemplate`: Этот класс предоставляет общую структуру для взаимодействия с API, подобными OpenAI.

**Атрибуты**:

- `url` (str): URL для доступа к DeepInfra API (`https://deepinfra.com/chat`).
- `api_base` (str): Базовый URL для OpenAI-совместимого API DeepInfra (`https://api.deepinfra.com/v1/openai`).
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`deepseek-ai/DeepSeek-V3`).
- `default_vision_model` (str): Модель для обработки изображений по умолчанию (`openbmb/MiniCPM-Llama3-V-2_5`).
- `vision_models` (List[str]): Список моделей, поддерживающих обработку изображений.
- `models` (List[str]): Список доступных моделей для использования.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для удобства выбора.

**Методы**:
- Отсутствуют, класс использует методы родительского класса `OpenaiTemplate`.

## Функции

В данном модуле отсутствуют отдельные функции, так как основная логика реализована через класс `DeepInfraChat` и его атрибуты.

## Примеры

Пример использования класса `DeepInfraChat`:

```python
from g4f.Provider import DeepInfraChat

# Создание экземпляра класса DeepInfraChat
deep_infra_chat = DeepInfraChat()

# Вывод URL API
print(deep_infra_chat.url)  # Вывод: https://deepinfra.com/chat

# Вывод списка доступных моделей
print(deep_infra_chat.models)
# Вывод: ['meta-llama/Meta-Llama-3.1-8B-Instruct', 'meta-llama/Llama-3.3-70B-Instruct-Turbo', 'meta-llama/Llama-3.3-70B-Instruct', 'deepseek-ai/DeepSeek-V3', 'mistralai/Mistral-Small-24B-Instruct-2501', 'deepseek-ai/DeepSeek-R1', 'deepseek-ai/DeepSeek-R1-Turbo', 'deepseek-ai/DeepSeek-R1-Distill-Llama-70B', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', 'microsoft/phi-4', 'microsoft/WizardLM-2-8x22B', 'Qwen/Qwen2.5-72B-Instruct', '01-ai/Yi-34B-Chat', 'Qwen/Qwen2-72B-Instruct', 'cognitivecomputations/dolphin-2.6-mixtral-8x7b', 'cognitivecomputations/dolphin-2.9.1-llama-3-70b', 'databricks/dbrx-instruct', 'deepinfra/airoboros-70b', 'lizpreciatior/lzlv_70b_fp16_hf', 'microsoft/WizardLM-2-7B', 'mistralai/Mixtral-8x22B-Instruct-v0.1', 'openbmb/MiniCPM-Llama3-V-2_5', 'meta-llama/Llama-3.2-90B-Vision-Instruct']