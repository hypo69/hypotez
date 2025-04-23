### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует асинхронный класс `PrestaLanguageAync`, который расширяет `PrestaShopAsync` и предназначен для управления языками в магазине PrestaShop. Он включает в себя методы для получения имени языка по его индексу и получения схемы языков.

Шаги выполнения
-------------------------
1. **Инициализация класса `PrestaLanguageAync`**:
   - Создается экземпляр класса `PrestaLanguageAync`, который наследует функциональность для взаимодействия с API PrestaShop асинхронно.

2. **Получение имени языка по индексу**:
   - Вызывается метод `get_lang_name_by_index(lang_index: int | str) -> str`, который принимает индекс языка в таблице PrestaShop и возвращает его ISO-код.
   - Внутри метода вызывается `super().get()` для выполнения запроса к API PrestaShop для получения информации о языке по указанному индексу.
   - В случае ошибки, она логируется с помощью `logger.error()`, и возвращается пустая строка.

3. **Получение схемы языков**:
   - Вызывается метод `get_languages_schema() -> dict`, который возвращает схему языков, доступную в PrestaShop.
   - Внутри метода вызывается `super().get_languages_schema()` для выполнения запроса к API PrestaShop.
   - Результат схемы языков выводится с использованием `print(lang_dict)`.

4. **Асинхронный запуск**:
   - В асинхронной функции `main()` создается экземпляр класса `PrestaLanguageAync`.
   - Вызывается метод `get_languages_schema()` для получения схемы языков.
   - Результат схемы языков выводится с использованием `print(languagas_schema)`.

5. **Запуск `main()` через `asyncio`**:
   - Код запускается с использованием `asyncio.run(main())`, что позволяет асинхронно выполнить функцию `main()`.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.prestashop.language_async import PrestaLanguageAync
from src.logger.logger import logger

async def main():
    """Пример использования PrestaLanguageAync."""
    try:
        lang_class = PrestaLanguageAync()

        # Получение схемы языков
        languages_schema = await lang_class.get_languages_schema()
        print(languages_schema)

        # Получение имени языка по индексу
        lang_name = await lang_class.get_lang_name_by_index(lang_index=1)
        print(f"Имя языка с индексом 1: {lang_name}")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())