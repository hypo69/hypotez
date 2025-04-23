### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор тестов, предназначенных для проверки функциональности класса `AliPromoCampaign`, используемого для управления рекламными кампаниями на AliExpress. Тесты охватывают различные аспекты, включая инициализацию кампании, получение информации о товарах, создание пространств имен (namespaces) для продуктов, категорий и кампаний, подготовку товаров, извлечение данных о товарах, сохранение продуктов и листинг товаров кампании.

Шаги выполнения
-------------------------
1. **Инициализация кампании**:
   - Функция `test_initialize_campaign` проверяет, правильно ли метод `initialize_campaign` инициализирует данные кампании, такие как имя, заголовок, язык, валюта и категория.
   - Она использует `mocker.patch` для имитации результата загрузки JSON данных и проверяет, что атрибуты кампании установлены правильно.

2. **Получение товаров категории**:
   - Функции `test_get_category_products_no_json_files` и `test_get_category_products_with_json_files` тестируют метод `get_category_products` в случаях, когда JSON файлы отсутствуют или присутствуют.
   - Они используют `mocker.patch` для имитации возвращаемых значений функций `get_filenames` и `j_loads_ns`, а также проверяют, что товары возвращаются правильно.

3. **Создание пространств имен**:
   - Функции `test_create_product_namespace`, `test_create_category_namespace` и `test_create_campaign_namespace` проверяют, правильно ли создаются пространства имен для продуктов, категорий и кампаний соответственно.
   - Они создают тестовые данные и проверяют, что атрибуты созданных объектов установлены правильно.

4. **Подготовка товаров**:
   - Функция `test_prepare_products` тестирует метод `prepare_products`, который должен вызывать метод `process_affiliate_products`.
   - Используется `mocker.patch` для имитации возвращаемых значений функций `get_prepared_products`, `read_text_file` и `get_filenames`, а также проверяется, что метод `process_affiliate_products` был вызван.

5. **Извлечение данных о товарах**:
   - Функция `test_fetch_product_data` тестирует метод `fetch_product_data`, проверяя, что он правильно извлекает данные о товарах на основе их идентификаторов.
   - Используется `mocker.patch` для имитации возвращаемого значения функции `process_affiliate_products` и проверяется, что возвращаемые продукты имеют правильные идентификаторы.

6. **Сохранение продукта**:
   - Функция `test_save_product` тестирует метод `save_product`, проверяя, что он правильно сохраняет данные о продукте в файл.
   - Используется `mocker.patch` для имитации функций `j_dumps` и `Path.write_text` и проверяется, что метод `write_text` был вызван с правильными аргументами.

7. **Листинг товаров кампании**:
   - Функция `test_list_campaign_products` тестирует метод `list_campaign_products`, проверяя, что он правильно возвращает список заголовков товаров кампании.
   - Создаются тестовые продукты и проверяется, что возвращаемый список заголовков соответствует ожидаемому.

Пример использования
-------------------------

```python
import pytest
from pathlib import Path
from types import SimpleNamespace
from src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign
from src.utils.jjson import j_dumps, j_loads_ns
from src.utils.file import save_text_file
from src import gs

# Пример использования fixture campaign для создания экземпляра AliPromoCampaign
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign("test_campaign", "test_category", "EN", "USD")

def test_example(campaign):
    """Пример теста с использованием fixture campaign."""
    # Предположим, что у вас есть метод, который нужно протестировать
    campaign.category.products = [SimpleNamespace(product_title="Product 1"), SimpleNamespace(product_title="Product 2")]
    product_titles = campaign.list_campaign_products()
    assert product_titles == ["Product 1", "Product 2"]