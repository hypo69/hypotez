## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет функции для валидации различных полей товара, таких как цена, вес, артикул, URL.

Шаги выполнения
-------------------------
1. **Импорт**: Импортируй класс `ProductFieldsValidator` из модуля `src.utils.string.validator`.
2. **Вызов функции**: Вызови статический метод `validate_price`, `validate_weight`, `validate_sku`, `validate_url`  или `isint` с соответствующим значением для проверки.
3. **Обработка результата**:  Функции возвращают `True` если валидация прошла успешно, иначе `False`.

Пример использования
-------------------------

```python
from src.utils.string.validator import ProductFieldsValidator

# Проверка цены
price_to_validate = "123.45"
is_valid_price = ProductFieldsValidator.validate_price(price_to_validate)
print(f"Цена {price_to_validate} валидна: {is_valid_price}")

# Проверка веса
weight_to_validate = "1.5 кг"
is_valid_weight = ProductFieldsValidator.validate_weight(weight_to_validate)
print(f"Вес {weight_to_validate} валиден: {is_valid_weight}")

# Проверка артикула
sku_to_validate = "ABC123"
is_valid_sku = ProductFieldsValidator.validate_sku(sku_to_validate)
print(f"Артикул {sku_to_validate} валиден: {is_valid_sku}")

# Проверка URL
url_to_validate = "https://www.example.com"
is_valid_url = ProductFieldsValidator.validate_url(url_to_validate)
print(f"URL {url_to_validate} валиден: {is_valid_url}")

# Проверка целого числа
number_to_validate = "123"
is_valid_number = ProductFieldsValidator.isint(number_to_validate)
print(f"Число {number_to_validate} является целым: {is_valid_number}")
```

**Дополнительные замечания**:

- Методы `validate_price` и `validate_weight` очищают строку от нецифровых символов, заменяют запятые на точки, а затем пытаются преобразовать строку в число.
- Метод `validate_sku` удаляет спецсимволы, переводы строк и пробелы, а затем проверяет минимальную длину.
- Метод `validate_url`  проверяет наличие протокола (`http` или `https`) и домена. 
- Метод `isint` пытается преобразовать строку в целое число.