### Как использовать блок кода PriceListRequester
=========================================================================================

Описание
-------------------------
Блок кода определяет класс `PriceListRequester`, который предназначен для работы с API PrestaShop для получения списка цен товаров. Класс позволяет запрашивать цены для списка товаров, обновлять источник данных и модифицировать цену товара.

Шаги выполнения
-------------------------
1. **Инициализация класса `PriceListRequester`**:
   - Создается объект класса `PriceListRequester`, при этом передается словарь с учетными данными API PrestaShop, содержащий домен API и ключ API.

2. **Запрос цен товаров**:
   - Вызывается метод `request_prices` с передачей списка товаров, для которых требуется получить цены.
   - Метод отправляет запрос к источнику данных (API PrestaShop) и возвращает словарь, где ключами являются названия товаров, а значениями - их цены.

3. **Обновление источника данных**:
   - Вызывается метод `update_source` с передачей нового источника данных.
   - Метод обновляет источник данных, который будет использоваться для запроса цен.

4. **Модификация цены товара**:
   - Вызывается метод `modify_product_price` с передачей названия товара и новой цены.
   - Метод изменяет цену указанного товара в источнике данных.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.pricelist import PriceListRequester

# Пример использования класса PriceListRequester
api_credentials = {
    'api_domain': 'your_api_domain',
    'api_key': 'your_api_key'
}

# Инициализация объекта класса PriceListRequester
price_requester = PriceListRequester(api_credentials)

# Запрос цен для списка товаров
products = ['product1', 'product2', 'product3']
prices = price_requester.request_prices(products)
print(f"Цены товаров: {prices}")

# Обновление источника данных
new_source = 'new_data_source'
price_requester.update_source(new_source)

# Модификация цены товара
product = 'product1'
new_price = 12.99
price_requester.modify_product_price(product, new_price)