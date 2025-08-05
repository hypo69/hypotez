# Модуль `dict_scenarios.py`

## Обзор

Модуль содержит словарь `scenario`, который определяет сценарии для поиска и обработки товаров "Murano Glass" на Amazon. В сценарии указывается URL для поиска, состояние товара, категории PrestaShop, к которым следует отнести товары, и правило определения цены.

## Подробней

Этот модуль предназначен для использования в экспериментальных целях, связанных с автоматизацией поиска и категоризации товаров на Amazon. Словарь `scenario` содержит конфигурацию для одного сценария ("Murano Glass"), но может быть расширен для включения других сценариев.

## Переменные

### `scenario`

```python
scenario: dict
```

**Описание**: Словарь, содержащий конфигурации сценариев для поиска и обработки товаров.

**Структура**:

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

**Ключи**:

-   `"Murano Glass"`: Название сценария.
    **Значения**:
    -   `"url"` (str): URL для поиска товаров на Amazon.
    -   `"condition"` (str): Состояние товара ("new").
    -   `"presta_categories"` (dict): Категории PrestaShop, к которым следует отнести товары.
        -   `"default_category"` (dict): Словарь, где ключ - ID категории, значение - название категории.
    -   `"price_rule"` (int): Правило определения цены.

**Как работает**:

Словарь `scenario` определяет параметры для поиска и обработки товаров. В данном случае, он задает URL для поиска "Art Deco murano glass" на Amazon, указывает, что товары должны быть новыми, определяет категорию "MURANO GLASS" в PrestaShop (с ID 11209) и задает правило определения цены с ID 1. Этот словарь используется для настройки процесса автоматического поиска и категоризации товаров.

**Примеры**:

Пример использования словаря `scenario`:

```python
# Пример доступа к URL сценария
url = scenario["Murano Glass"]["url"]
print(url)  # Вывод: https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss