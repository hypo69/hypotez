### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предоставляет класс `ProductFieldsValidator` с набором статических методов для валидации различных полей товара, таких как цена, вес, артикул и URL. Валидация включает в себя очистку, форматирование и проверку соответствия определенным критериям.

Шаги выполнения
-------------------------
1. **Импорт класса `ProductFieldsValidator`**:
   Импортируйте класс `ProductFieldsValidator` из модуля `src.utils.string.validator`.
2. **Вызов статических методов**:
   Вызывайте статические методы класса `ProductFieldsValidator` для валидации соответствующих полей товара.

Пример использования
-------------------------

```python
from src.utils.string.validator import ProductFieldsValidator

# Пример валидации цены
price = "1 234,56 $"
is_valid_price = ProductFieldsValidator.validate_price(price)
print(f"Цена '{price}' валидна: {is_valid_price}")

# Пример валидации веса
weight = "5,00 кг"
is_valid_weight = ProductFieldsValidator.validate_weight(weight)
print(f"Вес '{weight}' валиден: {is_valid_weight}")

# Пример валидации артикула
sku = "  ABC-123  "
is_valid_sku = ProductFieldsValidator.validate_sku(sku)
print(f"Артикул '{sku}' валиден: {is_valid_sku}")

# Пример валидации URL
url = "example.com"
is_valid_url = ProductFieldsValidator.validate_url(url)
print(f"URL '{url}' валиден: {is_valid_url}")

# Пример проверки на целое число
s = "123"
is_int = ProductFieldsValidator.isint(s)
print(f"'{s}' является целым числом: {is_int}")