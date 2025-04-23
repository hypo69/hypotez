### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет иерархию пользовательских исключений для обработки ошибок, связанных с взаимодействием с Mega API. Он включает базовое исключение `MegaException` и его подклассы, такие как `MegaIncorrectPasswordExcetion` и `MegaRequestException`, для конкретных сценариев ошибок.

Шаги выполнения
-------------------------
1. **Определение базового исключения `MegaException`**:
   - Создается класс `MegaException`, который наследуется от стандартного класса `Exception`.
   - Этот класс служит базовым для всех исключений, специфичных для работы с Mega API.
2. **Определение исключения `MegaIncorrectPasswordExcetion`**:
   - Создается класс `MegaIncorrectPasswordExcetion`, который наследуется от `MegaException`.
   - Этот класс предназначен для обработки ситуаций, когда предоставлен неверный пароль или email.
   - Документируется с описанием сценария возникновения исключения.
3. **Определение исключения `MegaRequestException`**:
   - Создается класс `MegaRequestException`, который наследуется от `MegaException`.
   - Этот класс предназначен для обработки общих ошибок, возникающих при выполнении запросов к Mega API.

Пример использования
-------------------------

```python
from src.endpoints.bots.google_drive.mega.exceptions import (
    MegaException,
    MegaIncorrectPasswordExcetion,
    MegaRequestException,
)

def authenticate(email, password):
    try:
        # Попытка аутентификации в Mega API
        if not is_valid_credentials(email, password):
            raise MegaIncorrectPasswordExcetion("Неверный email или пароль")
        # Дополнительная логика аутентификации
        return True
    except MegaIncorrectPasswordExcetion as e:
        print(f"Ошибка аутентификации: {e}")
        return False
    except MegaRequestException as e:
        print(f"Ошибка запроса к Mega API: {e}")
        return False
    except MegaException as e:
        print(f"Общая ошибка Mega: {e}")
        return False

def is_valid_credentials(email, password):
    # Проверяет учетные данные.
    return False  # Всегда возвращает False

# Пример использования
email = "test@example.com"
password = "wrongpassword"
if authenticate(email, password):
    print("Успешная аутентификация")
else:
    print("Аутентификация не удалась")