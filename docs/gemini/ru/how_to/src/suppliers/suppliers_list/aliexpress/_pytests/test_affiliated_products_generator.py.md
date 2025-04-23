### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит тесты для класса `AliAffiliatedProducts`, который генерирует партнерские продукты AliExpress. Он проверяет, что методы `check_and_process_affiliate_products` и `process_affiliate_products` вызываются и работают правильно. В тестах используются моки для изоляции тестируемого кода от внешних зависимостей.

Шаги выполнения
-------------------------
1. **Определение фикстуры `ali_affiliated_products`**:
   - Фикстура `ali_affiliated_products` создает экземпляр класса `AliAffiliatedProducts` с предопределенными параметрами (имя кампании, категория, язык и валюта).
   - Эта фикстура используется в тестах для предоставления экземпляра класса `AliAffiliatedProducts`.

2. **Тест `test_check_and_process_affiliate_products`**:
   - Патчит метод `process_affiliate_products` класса `AliAffiliatedProducts` с помощью `patch.object`, чтобы заменить его моком.
   - Вызывает метод `check_and_process_affiliate_products` с фиктивными URL-адресами продуктов (`prod_urls`).
   - Проверяет, что метод `process_affiliate_products` был вызван ровно один раз с правильными аргументами (`prod_urls`).

3. **Тест `test_process_affiliate_products`**:
   - Определяет фиктивные данные о продукте (`mock_product_details`) в виде списка объектов `SimpleNamespace`.
   - Патчит несколько внешних функций и методов:
     - `retrieve_product_details`: возвращает `mock_product_details`.
     - `ensure_https`: возвращает `prod_urls`.
     - `save_image_from_url`: мокируется для предотвращения фактической загрузки изображений.
     - `save_video_from_url`: мокируется для предотвращения фактической загрузки видео.
     - `j_dumps`: мокируется для предотвращения фактической записи в файл.
   - Вызывает метод `process_affiliate_products` с фиктивными URL-адресами продуктов (`prod_urls`).
   - Проверяет, что возвращенный список обработанных продуктов содержит ровно один элемент.
   - Проверяет, что `product_id` первого элемента в списке обработанных продуктов соответствует ожидаемому значению ("123").

Пример использования
-------------------------

```python
import pytest
from unittest.mock import patch, MagicMock
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts
from types import SimpleNamespace

# Пример данных
campaign_name = "sample_campaign"
category_name = "sample_category"
language = "EN"
currency = "USD"
prod_urls = ["https://www.aliexpress.com/item/123.html", "456"]

@pytest.fixture
def ali_affiliated_products():
    # Фикстура создает и возвращает экземпляр AliAffiliatedProducts
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)

def test_check_and_process_affiliate_products(ali_affiliated_products):
    # Мокируем метод process_affiliate_products
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        # Вызываем метод, который должен вызвать process_affiliate_products
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        # Проверяем, что метод process_affiliate_products был вызван с правильными аргументами
        mock_process.assert_called_once_with(prod_urls)

def test_process_affiliate_products(ali_affiliated_products):
    # Пример фиктивных данных о продукте
    mock_product_details = [SimpleNamespace(product_id="123", promotion_link="promo_link", product_main_image_url="image_url", product_video_url="video_url")]
    
    # Мокируем внешние зависимости
    with patch.object(ali_affiliated_products, 'retrieve_product_details', return_value=mock_product_details) as mock_retrieve, \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.ensure_https", return_value=prod_urls), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_image_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_video_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.j_dumps", return_value=True):
        
        # Вызываем метод для обработки партнерских продуктов
        processed_products = ali_affiliated_products.process_affiliate_products(prod_urls)
        
        # Проверяем результаты
        assert len(processed_products) == 1
        assert processed_products[0].product_id == "123"

if __name__ == "__main__":
    pytest.main()