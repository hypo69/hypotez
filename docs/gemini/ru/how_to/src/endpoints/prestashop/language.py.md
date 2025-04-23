### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет класс `PrestaLanguage`, который предназначен для управления языками в магазине PrestaShop. Он включает функции для добавления, удаления, обновления и получения информации о языках через API PrestaShop.

Шаги выполнения
-------------------------
1. **Инициализация класса `PrestaLanguage`**:
   - Создайте экземпляр класса `PrestaLanguage`, передав необходимые параметры API (API_DOMAIN и API_KEY).

2. **Получение имени языка по индексу**:
   - Вызовите метод `get_lang_name_by_index(lang_index)`, чтобы получить ISO код языка по его индексу в PrestaShop.

3. **Получение схемы языков**:
   - Вызовите метод `get_languages_schema()`, чтобы получить словарь, содержащий информацию обо всех языках, доступных в магазине.

Пример использования
-------------------------

```python
import asyncio

from src.endpoints.prestashop.language import PrestaLanguage
from src.logger.logger import logger


async def main():
    """
    Пример использования класса PrestaLanguage для получения информации о языках в PrestaShop.
    """
    try:
        # Инициализация класса PrestaLanguage с параметрами API
        API_DOMAIN = "your_api_domain"  # Замените на ваш API domain
        API_KEY = "your_api_key"  # Замените на ваш API key
        presta_language = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)

        # Получение имени языка по индексу
        lang_index = 1  # Индекс языка, который нужно получить
        lang_name = presta_language.get_lang_name_by_index(lang_index)
        logger.info(f"Имя языка с индексом {lang_index}: {lang_name}")

        # Получение схемы языков
        languages_schema = presta_language.get_languages_schema()
        logger.info(f"Схема языков: {languages_schema}")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())