# Модуль `Glider`

## Обзор

Модуль `Glider` предоставляет класс `Glider`, который является подклассом `OpenaiTemplate` и предназначен для взаимодействия с сервисом Glider. Он определяет специфические параметры, такие как URL, API endpoint и список поддерживаемых моделей.

## Подробнее

Модуль определяет класс `Glider`, который наследуется от `OpenaiTemplate`. Класс `Glider` содержит информацию о конкретном провайдере Glider, такую как URL, API endpoint, поддерживаемые модели и их алиасы. Это позволяет унифицировать взаимодействие с различными провайдерами в рамках проекта `hypotez`.

## Классы

### `Glider`

**Описание**: Класс `Glider` предназначен для взаимодействия с сервисом Glider.

**Наследует**:
- `OpenaiTemplate`: Класс `Glider` наследует функциональность от `OpenaiTemplate`, что позволяет использовать общие методы для работы с разными OpenAI-подобными сервисами.

**Атрибуты**:
- `label` (str): Название провайдера ("Glider").
- `url` (str): URL сервиса Glider ("https://glider.so").
- `api_endpoint` (str): URL API endpoint сервиса Glider ("https://glider.so/api/chat").
- `working` (bool): Указывает, работает ли провайдер (True).
- `default_model` (str): Модель, используемая по умолчанию ('chat-llama-3-1-70b').
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь с алиасами моделей.

## Функции

В данном модуле нет отдельных функций, только класс `Glider` с атрибутами.
```python
class Glider(OpenaiTemplate):
    """Класс для взаимодействия с сервисом Glider.

    Inherits:
        OpenaiTemplate: Наследует функциональность от OpenaiTemplate.

    Attributes:
        label (str): Название провайдера ("Glider").
        url (str): URL сервиса Glider ("https://glider.so").
        api_endpoint (str): URL API endpoint сервиса Glider ("https://glider.so/api/chat").
        working (bool): Указывает, работает ли провайдер (True).
        default_model (str): Модель, используемая по умолчанию ('chat-llama-3-1-70b').
        models (list): Список поддерживаемых моделей.
        model_aliases (dict): Словарь с алиасами моделей.
    """
```
**Принцип работы**:
Класс `Glider` переопределяет атрибуты класса `OpenaiTemplate`, чтобы указать на конкретный сервис Glider и его особенности. Это позволяет использовать общую логику `OpenaiTemplate` для взаимодействия с Glider.

**Примеры**:
```python
# Пример создания экземпляра класса Glider
glider = Glider()
print(glider.label)  # Вывод: Glider
print(glider.url)  # Вывод: https://glider.so
print(glider.models) # Вывод: ['chat-llama-3-1-70b', 'chat-llama-3-1-8b', 'chat-llama-3-2-3b', 'deepseek-ai/DeepSeek-R1']