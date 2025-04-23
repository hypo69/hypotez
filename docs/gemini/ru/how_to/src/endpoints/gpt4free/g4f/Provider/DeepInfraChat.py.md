### Как использовать блок кода DeepInfraChat
=========================================================================================

Описание
-------------------------
Этот код определяет класс `DeepInfraChat`, который наследуется от `OpenaiTemplate`. Он предназначен для взаимодействия с сервисом DeepInfra Chat, предоставляя информацию о поддерживаемых моделях, URL и базовый API. Класс содержит списки моделей, включая стандартные и vision-модели, а также псевдонимы моделей для упрощения их использования.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируется `OpenaiTemplate` из `.template`.

2. **Определение класса `DeepInfraChat`**:
   - Класс `DeepInfraChat` наследуется от `OpenaiTemplate`.
   - Определяются атрибуты класса:
     - `url` (str): URL сервиса DeepInfra Chat.
     - `api_base` (str): Базовый URL API DeepInfra.
     - `working` (bool): Указывает, что провайдер рабочий.
     - `default_model` (str): Модель, используемая по умолчанию (`deepseek-ai/DeepSeek-V3`).
     - `default_vision_model` (str): Vision-модель, используемая по умолчанию (`openbmb/MiniCPM-Llama3-V-2_5`).
     - `vision_models` (list): Список vision-моделей.
     - `models` (list): Список поддерживаемых моделей, включая vision-модели.
     - `model_aliases` (dict): Словарь псевдонимов моделей для удобства использования.

3. **Использование класса `DeepInfraChat`**:
   - Создается экземпляр класса `DeepInfraChat`.
   - Используются атрибуты класса для получения информации о моделях и API.

Пример использования
-------------------------

```python
    from src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

    # Создание экземпляра класса DeepInfraChat
    deep_infra_chat = DeepInfraChat()

    # Вывод URL сервиса
    print(f"URL сервиса: {deep_infra_chat.url}")

    # Вывод базового URL API
    print(f"Базовый URL API: {deep_infra_chat.api_base}")

    # Вывод списка поддерживаемых моделей
    print("Поддерживаемые модели:")
    for model in deep_infra_chat.models:
        print(f"- {model}")

    # Вывод псевдонимов моделей
    print("Псевдонимы моделей:")
    for alias, model in deep_infra_chat.model_aliases.items():
        print(f"- {alias}: {model}")
```