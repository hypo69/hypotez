### **Инструкции по использованию кода**

=========================================================================================

Описание
-------------------------
Этот код определяет два класса: `Custom` и `Feature`, которые являются наследниками класса `OpenaiTemplate`. Класс `Custom` предоставляет базовую конфигурацию для пользовательского провайдера, а класс `Feature` представляет собой провайдер с дополнительными функциями, который в данный момент не работает.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Из модуля `..template` импортируется класс `OpenaiTemplate`.

2. **Определение класса `Custom`**:
   - `label`: Устанавливается как "Custom Provider".
   - `working`: Устанавливается как `True`, что указывает на то, что провайдер работает.
   - `needs_auth`: Устанавливается как `False`, что означает, что провайдер не требует аутентификации.
   - `api_base`: Устанавливается как `"http://localhost:8080/v1"`, что определяет базовый URL для API провайдера.
   - `sort_models`: Устанавливается как `False`, что указывает на то, что модели не нужно сортировать.

3. **Определение класса `Feature`**:
   - `label`: Устанавливается как "Feature Provider".
   - `working`: Устанавливается как `False`, что указывает на то, что провайдер в данный момент не работает.
   - Наследует все остальные атрибуты от класса `Custom`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.Custom import Custom, Feature

# Создание экземпляра Custom провайдера
custom_provider = Custom()
print(f"Label: {custom_provider.label}")
print(f"Working: {custom_provider.working}")
print(f"API Base: {custom_provider.api_base}")

# Создание экземпляра Feature провайдера
feature_provider = Feature()
print(f"Label: {feature_provider.label}")
print(f"Working: {feature_provider.working}")
print(f"API Base: {feature_provider.api_base}")