# Модуль `dict_scenarios.py`

## Обзор

Модуль содержит словарь `scenario`, предназначенный для хранения информации о сценариях, связанных с товарами на Amazon. В данном случае, представлен пример для "Murano Glass". Словарь включает в себя URL страницы товара, условие ("new"), категории PrestaShop и правило ценообразования.

## Подробнее

Этот модуль, вероятно, используется для автоматизации процесса сбора данных о товарах с Amazon и их последующей загрузки или синхронизации с PrestaShop. Он определяет структуру данных, которая содержит всю необходимую информацию для каждого сценария.

## Переменные

### `scenario`

```python
scenario: dict = {
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category": {"11209": "MURANO GLASS"}
        },
        "price_rule": 1
    }
}
```

**Описание**: Словарь, содержащий информацию о сценариях для различных товаров. Ключом словаря является название товара, а значением - словарь с детальной информацией о сценарии.

**Элементы словаря**:

-   `"Murano Glass"`: Название товара.
    -   `"url"`: URL страницы товара на Amazon.
    -   `"condition"`: Условие товара (в данном случае, "new").
    -   `"presta_categories"`: Словарь, содержащий информацию о категориях товара в PrestaShop.
        -   `"default_category"`: Словарь, где ключ - ID категории в PrestaShop, а значение - название категории.
    -   `"price_rule"`: Правило ценообразования для товара.

**Примеры**

```python
# Пример использования словаря scenario
product_name = "Murano Glass"
product_url = scenario[product_name]["url"]
print(f"URL для {product_name}: {product_url}")

# Вывод: URL для Murano Glass: https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss