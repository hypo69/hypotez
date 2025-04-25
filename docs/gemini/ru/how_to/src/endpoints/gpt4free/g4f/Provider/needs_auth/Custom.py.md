## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет два класса: `Custom` и `Feature`, наследующие от класса `OpenaiTemplate`. Класс `Custom` служит как базовый класс для провайдера API, который требует авторизации. Класс `Feature` наследуется от класса `Custom` и представляет собой специфический провайдер API, который, в отличие от базового класса, не работает.

Шаги выполнения
-------------------------
1. **Определение класса `Custom`**:
   - Создается класс `Custom`, наследующий от `OpenaiTemplate`.
   - Устанавливаются атрибуты: 
     - `label`: "Custom Provider" - имя провайдера.
     - `working`: `True` - означает, что провайдер работает.
     - `needs_auth`: `False` - означает, что провайдер не требует авторизации.
     - `api_base`: "http://localhost:8080/v1" - базовый URL для API.
     - `sort_models`: `False` - не сортировать модели.

2. **Определение класса `Feature`**:
   - Создается класс `Feature`, наследующий от `Custom`.
   - Устанавливаются атрибуты:
     - `label`: "Feature Provider" - имя провайдера.
     - `working`: `False` - означает, что провайдер не работает.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.Custom import Custom, Feature

# Создание экземпляра базового провайдера
custom_provider = Custom()

# Вывод информации о провайдере
print(f"Провайдер: {custom_provider.label}")
print(f"Работает: {custom_provider.working}")
print(f"Требуется авторизация: {custom_provider.needs_auth}")

# Создание экземпляра специфического провайдера
feature_provider = Feature()

# Вывод информации о провайдере
print(f"Провайдер: {feature_provider.label}")
print(f"Работает: {feature_provider.working}")
print(f"Требуется авторизация: {feature_provider.needs_auth}")
```