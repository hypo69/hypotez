Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Language`, который содержит статические переменные, представляющие коды различных языков. Он предоставляет централизованный способ хранения и использования кодов языков, поддерживаемых AliExpress.

Шаги выполнения
-------------------------
1. Импортируйте модуль `Language` в свой код:
   ```python
   from src.suppliers.suppliers_list.aliexpress.api.models.languages import Language
   ```
2. Используйте статические переменные класса `Language` для получения кода нужного языка:
   ```python
   english_code = Language.EN
   russian_code = Language.RU
   # и так далее для других языков
   ```
3. Сравните или используйте полученные коды языков в своей логике, например, при формировании запросов к API AliExpress:
   ```python
   def get_products(language_code: str):
       # Функция отправляет запрос к API AliExpress с указанием кода языка
       pass

   get_products(Language.RU)
   ```

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models.languages import Language

def get_localized_products(language: str) -> None:
    """
    Функция выводит код языка для запроса к API AliExpress.

    Args:
        language (str): Название языка, для которого требуется получить код.

    Returns:
        None

    Example:
        >>> get_localized_products("Russian")
        RU
    """
    if language == "Russian":
        print(Language.RU)
    elif language == "English":
        print(Language.EN)
    else:
        print("Язык не поддерживается")

# Пример использования
get_localized_products("Russian")
get_localized_products("English")