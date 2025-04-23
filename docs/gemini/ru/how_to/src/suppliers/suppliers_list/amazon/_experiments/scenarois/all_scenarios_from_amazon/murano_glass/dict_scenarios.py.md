### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода содержит словарь `scenario`, который определяет сценарий для поиска и обработки товаров "Murano Glass" на платформе Amazon. В словаре указаны URL для поиска, состояние товара, категории PrestaShop и правило для определения цены.

Шаги выполнения
-------------------------
1. **Определение URL**: Указывается URL для поиска товаров "Art Deco murano glass" на Amazon.
2. **Определение состояния товара**: Устанавливается состояние товара как "new".
3. **Определение категорий PrestaShop**: Задается соответствие категории "MURANO GLASS" в PrestaShop идентификатору 11209.
4. **Определение правила цены**: Указывается правило цены с идентификатором 1.

Пример использования
-------------------------

```python
scenario: dict = {
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category":{"11209":"MURANO GLASS"}
        },
        "price_rule": 1
    }
}

# Пример использования:
# Доступ к URL
url = scenario["Murano Glass"]["url"]
print(f"URL для поиска: {url}")

# Доступ к состоянию товара
condition = scenario["Murano Glass"]["condition"]
print(f"Состояние товара: {condition}")

# Доступ к категориям PrestaShop
presta_categories = scenario["Murano Glass"]["presta_categories"]
print(f"Категории PrestaShop: {presta_categories}")

# Доступ к правилу цены
price_rule = scenario["Murano Glass"]["price_rule"]
print(f"Правило цены: {price_rule}")