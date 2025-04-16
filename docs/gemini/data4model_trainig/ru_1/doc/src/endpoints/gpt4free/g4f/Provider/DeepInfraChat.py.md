# Модуль `DeepInfraChat.py`

## Обзор

Модуль определяет класс `DeepInfraChat`, который является подклассом `OpenaiTemplate`. Он предназначен для взаимодействия с платформой DeepInfra Chat. Модуль содержит конфигурации для работы с различными моделями, включая модели для работы с изображениями.

## Подробней

Этот модуль предоставляет интерфейс для использования моделей, размещенных на платформе DeepInfra Chat, через API OpenAI. Он определяет URL, базовый URL API и список поддерживаемых моделей. Также модуль предоставляет словарь `model_aliases` для удобного использования коротких имен моделей.

## Классы

### `DeepInfraChat`

**Описание**: Класс `DeepInfraChat` предоставляет конфигурацию для работы с платформой DeepInfra Chat.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url` (str): URL платформы DeepInfra Chat.
- `api_base` (str): Базовый URL API OpenAI для DeepInfra.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию (`deepseek-ai/DeepSeek-V3`).
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (`openbmb/MiniCPM-Llama3-V-2_5`).
- `vision_models` (List[str]): Список моделей для работы с изображениями.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для удобства использования.

**Принцип работы**:
Класс `DeepInfraChat` определяет основные параметры для подключения и использования моделей, предоставляемых платформой DeepInfra Chat. Он содержит списки поддерживаемых моделей и псевдонимы для упрощения их использования. `DeepInfraChat` наследуется от `OpenaiTemplate`, что позволяет использовать общую логику для работы с OpenAI-совместимыми API.

## Параметры класса

- `url` (str): URL платформы DeepInfra Chat (`"https://deepinfra.com/chat"`).
- `api_base` (str): Базовый URL API OpenAI для DeepInfra (`"https://api.deepinfra.com/v1/openai"`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`'deepseek-ai/DeepSeek-V3'`).
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (`'openbmb/MiniCPM-Llama3-V-2_5'`).
- `vision_models` (List[str]): Список моделей для работы с изображениями (`[default_vision_model, 'meta-llama/Llama-3.2-90B-Vision-Instruct']`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для удобства использования.

## Примеры

```python
from g4f.Provider.DeepInfraChat import DeepInfraChat

# Создание экземпляра класса DeepInfraChat
deepinfra_chat = DeepInfraChat()

# Вывод URL платформы
print(f"URL: {deepinfra_chat.url}")

# Вывод списка поддерживаемых моделей
print(f"Поддерживаемые модели: {deepinfra_chat.models}")

# Вывод псевдонима для модели llama-3.1-8b
print(f"Псевдоним для llama-3.1-8b: {deepinfra_chat.model_aliases.get('llama-3.1-8b')}")