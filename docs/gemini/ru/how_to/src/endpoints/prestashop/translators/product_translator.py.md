## Как использовать `get_translations_from_presta_translations_table`
=========================================================================================

Описание
-------------------------
Функция `get_translations_from_presta_translations_table` извлекает переводы полей товара из таблицы переводов PrestaShop.

Шаги выполнения
-------------------------
1. Получает референс товара, а также локаль перевода.
2. Формирует фильтр поиска по референсу товара.
3. Выполняет поиск в таблице переводов с использованием менеджера `ProductTranslationsManager`.
4. Возвращает список найденных переводов.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.translators.product_translator import get_translations_from_presta_translations_table

# Пример использования
product_reference = "PRD123"
i18n = "ru-RU"  # Локаль перевода

# Получение переводов товара
product_translations = get_translations_from_presta_translations_table(product_reference, i18n)

# Вывод полученных переводов
print(product_translations)
```