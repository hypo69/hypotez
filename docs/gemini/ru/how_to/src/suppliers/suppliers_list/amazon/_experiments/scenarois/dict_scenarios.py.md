### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет словарь `scenario`, который содержит информацию о сценариях поиска товаров на Amazon. В данном случае, представлен один сценарий для "Murano Glass". Он включает URL для поиска, условие товара ("new"), соответствие категориям PrestaShop и правило ценообразования.

Шаги выполнения
-------------------------
1. **Определение словаря `scenario`**: Создается словарь с ключом "Murano Glass", внутри которого содержатся параметры поиска и обработки товаров.
2. **Указание URL**: Определяется URL для поиска товаров "Art Deco murano glass" на Amazon.
3. **Условие товара**: Указывается, что ищем только новые товары ("condition": "new").
4. **Соответствие категориям PrestaShop**: Определяется соответствие категории товара в PrestaShop, где категория с ID "11209" называется "MURANO GLASS".
5. **Правило ценообразования**: Указывается правило ценообразования с ID "1".

Пример использования
-------------------------

```python
# Пример использования словаря scenario для получения информации о сценарии "Murano Glass"

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

# Функция извлекает URL для поиска
def get_url(scenario_name: str) -> str:
    """
    Args:
        scenario_name (str): Название сценария.

    Returns:
        str: URL для поиска.
    """
    return scenario[scenario_name]["url"]

# Функция извлекает правило для цены
def get_price_rule(scenario_name: str) -> int:
    """
    Args:
        scenario_name (str): Название сценария.

    Returns:
        int: ID правила цены.
    """
    return scenario[scenario_name]["price_rule"]

# Функция извлекает категорию для PrestaShop
def get_presta_category(scenario_name: str) -> dict:
    """
    Args:
        scenario_name (str): Название сценария.

    Returns:
        dict:  категория для PrestaShop.
    """
    return scenario[scenario_name]["presta_categories"]

# Пример использования функций
murano_glass_url = get_url("Murano Glass")
print(f"URL для Murano Glass: {murano_glass_url}")

price_rule = get_price_rule("Murano Glass")
print(f"Правило цены для Murano Glass: {price_rule}")

presta_category = get_presta_category("Murano Glass")
print(f"Правило цены для PrestaShop: {presta_category}")