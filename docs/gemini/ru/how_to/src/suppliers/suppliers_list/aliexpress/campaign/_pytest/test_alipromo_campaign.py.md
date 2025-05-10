## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит модульные тесты для класса `AliPromoCampaign`, который реализует функциональность кампаний в AliExpress. 

Шаги выполнения
-------------------------
1. **Создание фикстуры `campaign`:** 
    - Фикстура создает экземпляр `AliPromoCampaign` с заданными значениями для имени кампании, категории, языка и валюты.
2. **Тестирование метода `initialize_campaign`:**
    - Тест имитирует загрузку данных JSON, используя `mocker.patch` для функции `j_loads_ns`.
    - Проверяет, что метод правильно инициализирует атрибуты `campaign.campaign.name` и `campaign.campaign.category.test_category.name`.
3. **Тестирование метода `get_category_products`:**
    - Тест проверяет два сценария: 
        - Отсутствие файлов JSON (тест `test_get_category_products_no_json_files`).
        - Наличие файлов JSON (тест `test_get_category_products_with_json_files`).
    - В обоих случаях используются `mocker.patch` для имитации поведения функций `get_filenames`, `fetch_product_data`, и `j_loads_ns`.
4. **Тестирование методов создания пространств имен (`create_product_namespace`, `create_category_namespace`, `create_campaign_namespace`):**
    - Каждый тест создает пространство имен с заданными данными и проверяет, что атрибуты пространства имен совпадают с ожидаемыми.
5. **Тестирование метода `prepare_products`:**
    - Тест проверяет, что метод вызывает `process_affiliate_products`, используя `mocker.patch` для имитации поведения функций `get_prepared_products`, `read_text_file`, и `get_filenames`.
6. **Тестирование метода `fetch_product_data`:**
    - Тест имитирует обработку аффилированных товаров с помощью `mocker.patch` для функции `process_affiliate_products`.
    - Проверяет, что метод возвращает список товаров с правильными идентификаторами.
7. **Тестирование метода `save_product`:**
    - Тест имитирует сериализацию товара в JSON с помощью `mocker.patch` для функций `j_dumps` и `Path.write_text`.
    - Проверяет, что метод правильно сохраняет товар в файл.
8. **Тестирование метода `list_campaign_products`:**
    - Тест добавляет тестовые товары в список `campaign.category.products` и проверяет, что метод правильно возвращает список названий товаров.

Пример использования
-------------------------

```python
import pytest
from src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign

@pytest.fixture
def campaign():
    """Создает экземпляр AliPromoCampaign для тестов."""
    return AliPromoCampaign("test_campaign", "test_category", "EN", "USD")

def test_initialize_campaign(mocker, campaign):
    """Проверяет, что метод initialize_campaign правильно инициализирует данные кампании."""
    mock_json_data = {
        "name": "test_campaign",
        "title": "Test Campaign",
        "language": "EN",
        "currency": "USD",
        "category": {
            "test_category": {
                "name": "test_category",
                "tags": "tag1, tag2",
                "products": [],
                "products_count": 0
            }
        }
    }
    mocker.patch("src.utils.jjson.j_loads_ns", return_value=SimpleNamespace(**mock_json_data))

    campaign.initialize_campaign()
    assert campaign.campaign.name == "test_campaign"
    assert campaign.campaign.category.test_category.name == "test_category"

```