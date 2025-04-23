### Как использовать блок кода с исключениями
=========================================================================================

Описание
-------------------------
Данный блок кода содержит набор пользовательских исключений, используемых в приложении. Он включает базовый класс `CustomException`, который обеспечивает логирование исключений, а также ряд специфических исключений, таких как `FileNotFoundError`, `ProductFieldException`, `KeePassException`, `DefaultSettingsException`, `WebDriverException`, `ExecuteLocatorException`, `PrestaShopException` и `PrestaShopAuthenticationError`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `typing`, `src.logger.logger`, `selenium.common.exceptions` и `pykeepass.exceptions`.
2. **Определение класса `CustomException`**:
   - Создается базовый класс исключений `CustomException`, который наследуется от `Exception`.
   - В конструкторе класса `__init__` инициализируются атрибуты `message`, `original_exception` и `exc_info`.
   - Метод `handle_exception` используется для логирования информации об исключении и оригинальном исключении, если оно есть.
3. **Определение специфических классов исключений**:
   - Определяются классы исключений, такие как `FileNotFoundError`, `ProductFieldException`, `KeePassException`, `DefaultSettingsException`, `WebDriverException`, `ExecuteLocatorException`, `PrestaShopException` и `PrestaShopAuthenticationError`, которые наследуются от `CustomException` или других стандартных исключений.
   - Каждый класс представляет собой конкретный тип ошибки, который может возникнуть в приложении.
4. **Использование исключений в коде**:
   - В коде, где может возникнуть ошибка, генерируется соответствующее исключение.
   - Исключения перехватываются с помощью блоков `try...except` для обработки ошибок и выполнения необходимых действий, таких как логирование или восстановление после ошибки.

Пример использования
-------------------------

```python
from src.logger.exceptions import FileNotFoundError, ProductFieldException, CustomException

def process_file(file_path: str):
    """
    Функция для обработки файла.

    Args:
        file_path (str): Путь к файлу.

    Raises:
        FileNotFoundError: Если файл не найден.
        ProductFieldException: Если возникла ошибка при обработке полей продукта.
        CustomException: Если произошла другая ошибка.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Дополнительная обработка файла
            if not content:
                raise ProductFieldException("Файл пуст")
            print(f"Содержимое файла: {content}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {file_path}", e)
    except ProductFieldException as e:
        raise ProductFieldException(f"Ошибка при обработке полей продукта в файле: {file_path}", e)
    except Exception as e:
        raise CustomException(f"Произошла ошибка при обработке файла: {file_path}", e)

# Пример использования функции
try:
    process_file('example.txt')
except FileNotFoundError as e:
    print(f"Ошибка: {e}")
except ProductFieldException as e:
    print(f"Ошибка: {e}")
except CustomException as e:
    print(f"Ошибка: {e}")