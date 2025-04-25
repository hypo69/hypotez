## Как использовать класс `PrestaLanguageAync`
=========================================================================================

Описание
-------------------------
Класс `PrestaLanguageAync` предоставляет интерфейс для взаимодействия с настройками языков в Prestashop. Он позволяет получить информацию о языках, добавить, удалить или обновить языки в магазине Prestashop.

Важно помнить, что у каждого магазина своя нумерация языков.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Создайте объект класса `PrestaLanguageAync`, передав необходимые параметры, такие как `API_DOMAIN` и `API_KEY`.
2. **Получение информации о языках**:
   - Используйте метод `get_languages_schema()` для получения схемы языков, которая содержит список языков с их индексами и названиями ISO.
   - Используйте метод `get_lang_name_by_index(lang_index:int|str )` для получения имени языка ISO по его индексу в таблице Prestashop.
   - Используйте метод `get_language_id_by_name(lang_name: str)` для получения индекса языка из таблицы Prestashop по его имени ISO.
3. **Добавление, удаление или обновление языков**:
   - Используйте метод `add_language_PrestaShop(lang_name:str, lang_string:str)` для добавления нового языка в магазин Prestashop.
   - Используйте метод `delete_language_PrestaShop(lang_id:int)` для удаления языка из магазина Prestashop.
   - Используйте метод `update_language_PrestaShop(lang_id:int, lang_name:str)` для обновления имени языка в магазине Prestashop.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.prestashop.language_async import PrestaLanguageAync

API_DOMAIN = 'your_api_domain'
API_KEY = 'your_api_key'

async def main():
    """Пример использования класса `PrestaLanguageAync`."""
    lang_class = PrestaLanguageAync(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)

    # Получение схемы языков
    languages_schema = await lang_class.get_languages_schema()
    print(languages_schema)

    # Получение имени языка по индексу
    lang_name = await lang_class.get_lang_name_by_index(1)
    print(f"Название языка с индексом 1: {lang_name}")

    # Получение индекса языка по имени
    lang_id = await lang_class.get_language_id_by_name('en')
    print(f"Индекс языка 'en': {lang_id}")

    # Добавление нового языка
    await lang_class.add_language_PrestaShop('Spanish', 'es')

    # Удаление языка
    await lang_class.delete_language_PrestaShop(3)

    # Обновление имени языка
    await lang_class.update_language_PrestaShop(4, 'Updated Language Name')

if __name__ == '__main__':
    asyncio.run(main())
```