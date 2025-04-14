# Модуль `Glider`

## Обзор

Модуль `Glider` представляет собой реализацию класса `Glider`, который наследуется от `OpenaiTemplate`. Он предназначен для взаимодействия с провайдером Glider, предоставляющим доступ к различным моделям, таким как Llama и DeepSeek. Модуль определяет URL, endpoint API, поддерживаемые модели и их псевдонимы.

## Подробней

Модуль `Glider` является частью системы, использующей API `glider.so` для доступа к различным моделям. Класс `Glider` содержит метаданные, необходимые для подключения и использования API, такие как URL, endpoint API, поддерживаемые модели и их псевдонимы.

## Классы

### `Glider`

**Описание**: Класс `Glider` предоставляет интерфейс для взаимодействия с API `glider.so`.

**Наследует**:
- `OpenaiTemplate`: класс, предоставляющий базовую структуру для работы с API, совместимыми с OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера, в данном случае "Glider".
- `url` (str): URL провайдера, "https://glider.so".
- `api_endpoint` (str): URL endpoint API, "https://glider.so/api/chat".
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию, 'chat-llama-3-1-70b'.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `Glider` наследует функциональность от `OpenaiTemplate` и переопределяет атрибуты, специфичные для API Glider. Это позволяет использовать `Glider` как провайдера для моделей, поддерживаемых Glider.

## Методы класса

В данном коде не предоставлены методы класса `Glider`.

## Параметры класса

- `label` (str): Метка провайдера, в данном случае "Glider".
- `url` (str): URL провайдера, "https://glider.so".
- `api_endpoint` (str): URL endpoint API, "https://glider.so/api/chat".
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию, 'chat-llama-3-1-70b'.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Примеры

Пример создания экземпляра класса `Glider`:

```python
from src.endpoints.gpt4free.g4f.Provider.Glider import Glider

glider = Glider()
print(glider.label)
print(glider.api_endpoint)
print(glider.default_model)