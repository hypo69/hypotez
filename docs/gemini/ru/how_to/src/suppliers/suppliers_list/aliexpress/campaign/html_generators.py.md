## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет классы для генерации HTML-файлов для рекламных кампаний AliExpress, отдельных категорий товаров и товаров. 

Шаги выполнения
-------------------------
1. **Инициализация:**  Создаются объекты классов `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`. 
2. **Генерация HTML для отдельных товаров:**
    - Метод `set_product_html` в классе `ProductHTMLGenerator` генерирует HTML-файл для конкретного товара, используя данные о товаре и путь к директории категории. 
    - В HTML-файле отображается название товара, изображение, цены (обычная и со скидкой), категория и ссылка для покупки. 
3. **Генерация HTML для категорий товаров:**
    - Метод `set_category_html` в классе `CategoryHTMLGenerator` генерирует HTML-файл для категории,  отображая список товаров, входящих в нее. 
    - HTML-файл представляет собой сетку товаров, где каждый товар отображается с названием, изображением, ценами, категорией и кнопкой покупки.
4. **Генерация HTML для рекламной кампании:**
    - Метод `set_campaign_html` в классе `CampaignHTMLGenerator` генерирует HTML-файл для рекламной кампании, отображая список категорий товаров, участвующих в ней. 
    - HTML-файл представляет собой список категорий, каждая из которых ведет на HTML-страницу категории, сгенерированную на предыдущем шаге. 

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator
from types import SimpleNamespace
from pathlib import Path


# Пример данных товара
product = SimpleNamespace(
    product_id='123456789',
    product_title='Название товара',
    local_image_path='images/product.jpg',
    target_sale_price=10.99,
    target_sale_price_currency='USD',
    target_original_price=15.99,
    target_original_price_currency='USD',
    second_level_category_name='Category Name',
    promotion_link='https://aliexpress.com/product/123456789'
)

# Пример данных категорий
categories = [
    'Category 1',
    'Category 2',
    'Category 3'
]

# Пример данных о категории
products_list = [
    SimpleNamespace(
        product_id='123456789',
        product_title='Название товара 1',
        local_image_path='images/product1.jpg',
        target_sale_price=10.99,
        target_sale_price_currency='USD',
        target_original_price=15.99,
        target_original_price_currency='USD',
        second_level_category_name='Category Name',
        promotion_link='https://aliexpress.com/product/123456789'
    ),
    SimpleNamespace(
        product_id='987654321',
        product_title='Название товара 2',
        local_image_path='images/product2.jpg',
        target_sale_price=12.99,
        target_sale_price_currency='USD',
        target_original_price=19.99,
        target_original_price_currency='USD',
        second_level_category_name='Category Name',
        promotion_link='https://aliexpress.com/product/987654321'
    )
]


# Генерация HTML для товара
ProductHTMLGenerator.set_product_html(product, Path('path/to/category'))

# Генерация HTML для категории
CategoryHTMLGenerator.set_category_html(products_list, Path('path/to/category'))

# Генерация HTML для кампании
CampaignHTMLGenerator.set_campaign_html(categories, Path('path/to/campaign'))
```