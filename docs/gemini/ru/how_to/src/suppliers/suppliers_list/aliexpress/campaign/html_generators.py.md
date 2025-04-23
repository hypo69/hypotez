## \file /src/suppliers/aliexpress/campaign/html_generators.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.campaign
	:platform: Windows, Unix
	:synopsis: Генератор HTML контента рекламной кампании

"""


import header

from pathlib import Path
from types import SimpleNamespace
from src.utils.file import save_text_file
import html

class ProductHTMLGenerator:
    """ Class for generating HTML for individual products."""

    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path):
        """ Creates an HTML file for an individual product.

        Args:
            product (SimpleNamespace): The product details to include in the HTML.
            category_path (str | Path): The path to save the HTML file.
        """
        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / f"{product.product_id}.html"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(product.product_title)}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css"> <!-- Link to custom CSS file -->
</head>
<body>
    <div class="container">
        <h1 class="my-4">{html.escape(product.product_title)}</h1>
        <div class="card">
            <img src="{Path(product.local_image_path).as_posix()}" alt="{html.escape(product.product_title)}" class="card-img-top">
            <div class="card-body">
                <p class="card-text">Price: <span class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                <p class="card-text">Original Price: <span class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</span></p>
                <p class="card-text">Category: <span class="product-category">{html.escape(product.second_level_category_name)}</span></p>
                <a href="{product.promotion_link}" class="btn btn-primary">Buy Now</a>
            </div>
        </div>
    </div>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        save_text_file(html_content, html_path)

class CategoryHTMLGenerator:
    """ Class for generating HTML for product categories."""

    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Creates an HTML file for the category.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): List of products to include in the HTML.
            category_path (str | Path): Path to save the HTML file.
        """
        products_list = products_list if isinstance(products_list, list) else [products_list]

        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(category_name)} Products</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css"> <!-- Link to custom CSS file -->
</head>
<body>
    <div class="container">
        <h1 class="my-4">{html.escape(category_name)} Products</h1>
        <div class="row product-grid">
    """

        for product in products_list:
            image_url = Path(product.local_image_path).as_posix()
            html_content += f"""
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <img src="{image_url}" alt="{html.escape(product.product_title)}" class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">{html.escape(product.product_title)}</h5>
                            <p class="card-text">Price: <span class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                            <p class="card-text">Original Price: <span class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</span></p>
                            <p class="card-text">Category: <span class="product-category">{html.escape(product.second_level_category_name)}</span></p>
                            <a href="{product.promotion_link}" class="btn btn-primary">Buy Now</a>
                        </div>
                    </div>
                </div>
            """

        html_content += """
        </div>
    </div>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        save_text_file(html_content, html_path)

class CampaignHTMLGenerator:
    """ Class for generating HTML for a campaign."""

    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path):
        """ Creates an HTML file for the campaign, listing all categories.

        Args:
            categories (list[str]): List of category names.
            campaign_path (str | Path): Path to save the HTML file.
        """
        html_path = Path(campaign_path) / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaign Overview</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css"> <!-- Link to custom CSS file -->
</head>
<body>
    <div class="container">
        <h1 class="my-4">Campaign Overview</h1>
        <ul class="list-group">
    """

        for category in categories:
            html_content += f"""
                <li class="list-group-item">
                    <a href="{category}/index.html">{html.escape(category)}</a>
                </li>
            """

        html_content += """
        </ul>
    </div>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        save_text_file(html_content, html_path)
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит классы для автоматической генерации HTML-страниц для товаров, категорий и кампаний AliExpress. Он использует строковые шаблоны и сохраняет их в HTML-файлы.

Шаги выполнения
-------------------------
1. **ProductHTMLGenerator**:
   - Функция `set_product_html` создает HTML-страницу для отдельного товара.
   - Извлекает детали товара из объекта `product` (например, название, цену, изображение).
   - Формирует HTML-контент, заполняя шаблон данными товара.
   - Сохраняет HTML-файл в указанный `category_path` в поддиректории `html`.

2. **CategoryHTMLGenerator**:
   - Функция `set_category_html` создает HTML-страницу для списка товаров в категории.
   - Проверяет, является ли входной параметр `products_list` списком, и преобразует его в список, если это не так.
   - Формирует HTML-контент, перебирая список товаров и добавляя информацию о каждом товаре в HTML-шаблон.
   - Сохраняет HTML-файл (`index.html`) в указанный `category_path` в поддиректории `html`.

3. **CampaignHTMLGenerator**:
   - Функция `set_campaign_html` создает HTML-страницу для кампании, содержащую список категорий.
   - Формирует HTML-контент, перебирая список категорий и создавая ссылки на HTML-страницы каждой категории.
   - Сохраняет HTML-файл (`index.html`) в указанный `campaign_path`.

Пример использования
-------------------------

```python
from types import SimpleNamespace
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator

# Пример использования ProductHTMLGenerator
product_data = SimpleNamespace(
    product_id='12345',
    product_title='Cool Gadget',
    local_image_path='images/gadget.jpg',
    target_sale_price=25.00,
    target_sale_price_currency='USD',
    target_original_price=30.00,
    target_original_price_currency='USD',
    second_level_category_name='Electronics',
    promotion_link='http://example.com/gadget'
)
category_path = 'output/electronics'
ProductHTMLGenerator.set_product_html(product_data, category_path)

# Пример использования CategoryHTMLGenerator
product_list = [
    SimpleNamespace(
        product_id='12345',
        product_title='Cool Gadget',
        local_image_path='images/gadget.jpg',
        target_sale_price=25.00,
        target_sale_price_currency='USD',
        target_original_price=30.00,
        target_original_price_currency='USD',
        second_level_category_name='Electronics',
        promotion_link='http://example.com/gadget'
    ),
    SimpleNamespace(
        product_id='67890',
        product_title='Awesome Device',
        local_image_path='images/device.jpg',
        target_sale_price=45.00,
        target_sale_price_currency='USD',
        target_original_price=50.00,
        target_original_price_currency='USD',
        second_level_category_name='Electronics',
        promotion_link='http://example.com/device'
    )
]
CategoryHTMLGenerator.set_category_html(product_list, category_path)

# Пример использования CampaignHTMLGenerator
categories = ['electronics', 'clothing', 'home']
campaign_path = 'output/campaign'
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)