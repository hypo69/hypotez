### **Анализ кода модуля `html_generators.py`**

## \file /src/suppliers/aliexpress/campaign/html_generators.py

Модуль содержит классы для генерации HTML-контента рекламной кампании AliExpress.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и разбит на классы, каждый из которых отвечает за генерацию HTML для определенной сущности (товар, категория, кампания).
    - Использование `html.escape` для предотвращения XSS-атак.
    - Четкое разделение ответственности между классами.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров функций и возвращаемых значений.
    - Docstring-и написаны на английском языке.
    - Нет обработки возможных исключений.
    - Не используется модуль `logger` для логирования.
    - Не хватает документации модуля в целом.
    - В коде испольются двойные кавычки в строках. Это неправильно.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров функций и возвращаемых значений.
2.  **Перевести docstring на русский язык**:
    - Перевести все docstring-и на русский язык, чтобы соответствовать требованиям.
3.  **Добавить обработку исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений, например, при записи файлов.
4.  **Использовать модуль `logger`**:
    - Использовать модуль `logger` для логирования важных событий, таких как создание HTML-файлов или возникновение ошибок.
5.  **Добавить документацию модуля**:
    - Добавить docstring в начало файла, описывающий назначение модуля.
6.  **Изменить двойные кавычки на одинарные**:\
    - Заменить двойные кавычки на одинарные.
7. **Устранить избыточное импортирование модуля `header`**:\
    - Удалить строку `import header`, так как этот модуль нигде не используется.
8. **Добавить docstring для внутренних функций**:\
    - Если в классе есть внутренняя функция - для нее тоже надо добавить docstring.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/html_generators.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML контента рекламной кампании AliExpress.
===================================================================

Модуль содержит классы для генерации HTML-страниц:
- `ProductHTMLGenerator`: для отдельных товаров.
- `CategoryHTMLGenerator`: для категорий товаров.
- `CampaignHTMLGenerator`: для кампании в целом.

Пример использования:
----------------------
>>> from pathlib import Path
>>> from types import SimpleNamespace
>>> product = SimpleNamespace(product_id='123', product_title='Example Product', local_image_path='img/example.jpg', target_sale_price=10.00, target_sale_price_currency='USD', target_original_price=15.00, target_original_price_currency='USD', second_level_category_name='Example Category', promotion_link='https://example.com')
>>> category_path = Path('./example_category')
>>> ProductHTMLGenerator.set_product_html(product, category_path)
"""

from pathlib import Path
from types import SimpleNamespace
from src.utils.file import save_text_file
import html
from src.logger import logger  # Import logger module
#import header #Удаляю, так как нигде не используется

class ProductHTMLGenerator:
    """Класс для генерации HTML для отдельных продуктов."""

    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path) -> None:
        """
        Создает HTML-файл для отдельного продукта.

        Args:
            product (SimpleNamespace): Детали продукта для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при создании HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> product = SimpleNamespace(product_id='123', product_title='Example Product', local_image_path='img/example.jpg', target_sale_price=10.00, target_sale_price_currency='USD', target_original_price=15.00, target_original_price_currency='USD', second_level_category_name='Example Category', promotion_link='https://example.com')
            >>> category_path = Path('./example_category')
            >>> ProductHTMLGenerator.set_product_html(product, category_path)
        """
        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / f'{product.product_id}.html'

        html_content = f'''<!DOCTYPE html>
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
'''
        try:
            save_text_file(file_path=html_content, data=html_path)
            logger.info(f'HTML file created for product {product.product_id} at {html_path}')
        except Exception as ex:
            logger.error(f'Error creating HTML file for product {product.product_id}', ex, exc_info=True)

class CategoryHTMLGenerator:
    """Класс для генерации HTML для категорий продуктов."""

    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path) -> None:
        """
        Создает HTML-файл для категории.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при создании HTML-файла.
        
        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> products_list = [SimpleNamespace(product_id='123', product_title='Example Product', local_image_path='img/example.jpg', target_sale_price=10.00, target_sale_price_currency='USD', target_original_price=15.00, target_original_price_currency='USD', second_level_category_name='Example Category', promotion_link='https://example.com')]
            >>> category_path = Path('./example_category')
            >>> CategoryHTMLGenerator.set_category_html(products_list, category_path)
        """
        products_list = products_list if isinstance(products_list, list) else [products_list]

        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / 'index.html'

        html_content = f'''<!DOCTYPE html>
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
'''

        for product in products_list:
            image_url = Path(product.local_image_path).as_posix()
            html_content += f'''
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
'''

        html_content += ''' 
        </div>
    </div>
    
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
        try:
            save_text_file(file_path=html_content, data=html_path)
            logger.info(f'HTML file created for category {category_name} at {html_path}')
        except Exception as ex:
            logger.error(f'Error creating HTML file for category {category_name}', ex, exc_info=True)


class CampaignHTMLGenerator:
    """Класс для генерации HTML для кампании."""

    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path) -> None:
        """
        Создает HTML-файл для кампании, перечисляя все категории.

        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при создании HTML-файла.
            
        Example:
            >>> from pathlib import Path
            >>> categories = ['Category1', 'Category2']
            >>> campaign_path = Path('./example_campaign')
            >>> CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
        """
        html_path = Path(campaign_path) / 'index.html'

        html_content = f'''<!DOCTYPE html>
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
'''

        for category in categories:
            html_content += f'''
                <li class="list-group-item">
                    <a href="{category}/index.html">{html.escape(category)}</a>
                </li>
'''

        html_content += ''' 
        </ul>
    </div>
    
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
        try:
            save_text_file(file_path=html_content, data=html_path)
            logger.info(f'HTML file created for campaign at {html_path}')
        except Exception as ex:
            logger.error(f'Error creating HTML file for campaign', ex, exc_info=True)