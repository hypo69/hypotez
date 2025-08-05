# Модуль `promote_deal`

## Обзор

Модуль `promote_deal`  предназначен для управления рекламными кампаниями на AliExpress. Он использует класс `AliPromoDeal` для работы с рекламными предложениями. 

## Details

Модуль `promote_deal`  загружает информацию о товарах из `AliPromoDeal`, затем ... 

## Классы

### `AliPromoDeal`

**Описание:** Класс `AliPromoDeal`  представляет рекламное предложение на AliExpress. 

**Атрибуты:** 

- `deal_id` (str): Идентификатор рекламной кампании.

**Методы:**

- `get_next_product()`: Возвращает следующий товар из списка.
- `get_all_products_details()`: Возвращает список с подробной информацией о товарах.

## Функции

### `promote_deal`

**Описание:** 

**Параметры:**

- `deal_id` (str): Идентификатор рекламной кампании.

**Возвращает:**

- `None`: Возвращает `None`.

**Пример:**

```python
deal = AliPromoDeal('150624_baseus_deals')

# Получение следующего товара
product = deal.get_next_product()

# Получение списка всех товаров
products = deal.get_all_products_details()
```