### **Инструкция по использованию блока кодов исключений**

=========================================================================================

Описание
-------------------------
Данный блок кода определяет набор пользовательских исключений, используемых в проекте `hypotez` для обработки различных ошибок, которые могут возникнуть при работе с GPT4Free и другими связанными сервисами. Каждое исключение представляет собой конкретный тип ошибки, что позволяет более точно обрабатывать исключительные ситуации.

Шаги выполнения
-------------------------
1. **Импорт исключений**: Импортируйте необходимые классы исключений в модуль, где они будут использоваться.
2. **Обработка ошибок**: В блоках `try...except` перехватывайте конкретные исключения для обработки соответствующих ошибок.
3. **Генерирование исключений**: В случае возникновения ошибки, генерируйте соответствующие исключения с помощью оператора `raise`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.errors import ProviderNotFoundError, ModelNotFoundError

def process_request(provider: str, model: str):
    """
    Функция пытается обработать запрос с использованием заданного провайдера и модели.
    """
    try:
        # Попытка использовать провайдера и модель для обработки запроса
        if not is_provider_available(provider):
            raise ProviderNotFoundError(f"Провайдер {provider} не найден.")
        if not is_model_available(model):
            raise ModelNotFoundError(f"Модель {model} не найдена.")
        
        # Код обработки запроса здесь
        result = f"Запрос успешно обработан с использованием {provider} и {model}."
        return result
    except ProviderNotFoundError as e:
        print(f"Ошибка: {e}")
        return None
    except ModelNotFoundError as e:
        print(f"Ошибка: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None

def is_provider_available(provider: str) -> bool:
    """
    Функция для проверки доступности провайдера.
    """
    available_providers = ["ProviderA", "ProviderB"]
    return provider in available_providers

def is_model_available(model: str) -> bool:
    """
    Функция для проверки доступности модели.
    """
    available_models = ["ModelX", "ModelY"]
    return model in available_models

# Пример вызова функции
result = process_request("ProviderC", "ModelZ")
if result:
    print(result)
```
```python
from src.endpoints.gpt4free.g4f.errors import ProviderNotFoundError, ModelNotFoundError

def process_request(provider: str, model: str) -> str | None:
    """
    Функция пытается обработать запрос с использованием заданного провайдера и модели.

    Args:
        provider (str): Имя провайдера.
        model (str): Имя модели.

    Returns:
        str | None: Результат обработки запроса или None в случае ошибки.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        Exception: В случае других ошибок.
    """
    try:
        # Проверка доступности провайдера
        if not is_provider_available(provider):
            raise ProviderNotFoundError(f"Провайдер {provider} не найден.")

        # Проверка доступности модели
        if not is_model_available(model):
            raise ModelNotFoundError(f"Модель {model} не найдена.")

        # Код обработки запроса здесь
        result = f"Запрос успешно обработан с использованием {provider} и {model}."
        return result
    except ProviderNotFoundError as e:
        print(f"Ошибка: {e}")
        return None
    except ModelNotFoundError as e:
        print(f"Ошибка: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None

def is_provider_available(provider: str) -> bool:
    """
    Функция для проверки доступности провайдера.

    Args:
        provider (str): Имя провайдера.

    Returns:
        bool: True, если провайдер доступен, иначе False.
    """
    available_providers = ["ProviderA", "ProviderB"]
    return provider in available_providers

def is_model_available(model: str) -> bool:
    """
    Функция для проверки доступности модели.

    Args:
        model (str): Имя модели.

    Returns:
        bool: True, если модель доступна, иначе False.
    """
    available_models = ["ModelX", "ModelY"]
    return model in available_models

# Пример вызова функции
result = process_request("ProviderC", "ModelZ")
if result:
    print(result)