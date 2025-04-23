### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой словарь `scenario`, который содержит информацию о различных товарах (`Apple Wathes`, `Murano Glass`) и их параметрах для использования на сайте Amazon. Каждый товар имеет набор атрибутов, таких как URL страницы товара, условие (состояние) товара, категории PrestaShop, правило цены и другие настройки.

Шаги выполнения
-------------------------
1. **Определение словаря `scenario`**: Создается словарь `scenario`, который содержит информацию о товарах, таких как "Apple Wathes" и "Murano Glass".
2. **Задание URL**: Для каждого товара указывается URL страницы товара на Amazon.
3. **Указание состояния товара**: Определяется состояние товара (`condition`), например, "new".
4. **Настройка категорий PrestaShop**: Для каждого товара задаются категории PrestaShop (`presta_categories`), которые могут быть определены через шаблон или явно.
5. **Установка правила цены**: Указывается правило цены (`price_rule`) для товара.

Пример использования
-------------------------

```python
scenario: dict = {
    "Apple Wathes": {
        "url": "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "template": {"apple": "WATCHES"}
        },
        "checkbox": False,
        "price_rule": 1
    },
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category":{"11209":"MURANO GLASS"}
        },
        "price_rule": 1
    }
}

# Пример использования: извлечение URL для товара "Apple Wathes"
apple_watches_url = scenario["Apple Wathes"]["url"]
print(apple_watches_url)
# Функция возвращает: "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2"