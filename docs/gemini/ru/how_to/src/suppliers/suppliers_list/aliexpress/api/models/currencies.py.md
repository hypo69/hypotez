### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код определяет класс `Currency`, который содержит статические переменные, представляющие коды различных валют. Это позволяет удобно использовать предопределенные значения валют в других частях программы, например, при работе с API AliExpress для указания валюты товара или при конвертации цен.

Шаги выполнения
-------------------------
1. Импортируйте класс `Currency` в модуль, где необходимо использовать коды валют:
   ```python
   from src.suppliers.suppliers_list.aliexpress.api.models.currencies import Currency
   ```
2. Используйте статические переменные класса `Currency` для получения кода нужной валюты:
   ```python
   usd_code = Currency.USD
   eur_code = Currency.EUR
   ```
3. Применяйте полученные коды валют в своих функциях или классах для указания валюты товара или проведения других операций, связанных с валютами.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models.currencies import Currency

def get_aliexpress_product_price(product_id: str, currency: str = Currency.USD) -> float:
    """
    Функция получает цену товара с AliExpress в указанной валюте.
    
    Args:
        product_id (str): ID товара на AliExpress.
        currency (str): Код валюты (по умолчанию USD).
    
    Returns:
        float: Цена товара в указанной валюте.
    """
    # Здесь должна быть логика запроса к API AliExpress для получения цены товара
    # В примере просто возвращается случайное значение
    if currency == Currency.USD:
        return 10.0
    elif currency == Currency.EUR:
        return 9.0
    else:
        return 0.0

# Пример использования функции
product_price_usd = get_aliexpress_product_price("123456789", Currency.USD)
print(f"Цена товара в USD: {product_price_usd}")

product_price_eur = get_aliexpress_product_price("123456789", Currency.EUR)
print(f"Цена товара в EUR: {product_price_eur}")