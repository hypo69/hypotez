### Анализ кода модуля `html_generators`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разделен на классы, каждый из которых отвечает за генерацию HTML для определенного уровня (продукт, категория, кампания).
    - Использование `html.escape` для предотвращения XSS-атак.
    - Использование `Pathlib` для работы с путями.
- **Минусы**:
    - Отсутствует логирование.
    - Отсутствует обработка исключений.
    - В докстрингах используются параметры `@param` вместо общепринятого стандарта.
    - Использованы двойные кавычки в некоторых местах.
    - Не хватает документации модуля.

**Рекомендации по улучшению:**

1.  **Добавить документацию модуля**:
    -   В начале файла добавить общее описание модуля, его назначения и примеры использования.
2.  **Улучшить документацию классов и методов**:
    -   Перефразировать docstring в соответствии с указанным форматом.
    -   Добавить примеры использования в docstring.
3.  **Добавить логирование**:
    -   Использовать `logger` для записи информации о процессе генерации HTML, а также для записи ошибок.
4.  **Добавить обработку исключений**:
    -   Обрабатывать возможные исключения при записи файлов.
5.  **Унифицировать кавычки**:
    -   Использовать только одинарные кавычки для строк.
6.  **Улучшить обработку `products_list` в `CategoryHTMLGenerator`**:
    -   Убрать избыточное присваивание `products_list = products_list if isinstance(products_list, list) else [products_list]`. Это можно сделать более лаконично.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/html_generators.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML контента рекламной кампании AliExpress.
==============================================================

Модуль содержит классы для генерации HTML-страниц:
- :class:`ProductHTMLGenerator` - для отдельных товаров.
- :class:`CategoryHTMLGenerator` - для категорий товаров.
- :class:`CampaignHTMLGenerator` - для общей страницы кампании.

Пример использования:
----------------------

>>> from pathlib import Path
>>> from types import SimpleNamespace
>>> category_path = Path('path/to/category')
>>> product = SimpleNamespace(
...     product_id='12345',
...     product_title='Example Product',
...     local_image_path='path/to/image.jpg',
...     target_sale_price=10.00,
...     target_sale_price_currency='USD',
...     target_original_price=15.00,
...     target_original_price_currency='USD',
...     second_level_category_name='Example Category',
...     promotion_link='https://example.com'
... )
>>> ProductHTMLGenerator.set_product_html(product, str(category_path))
"""

import header
import html
from pathlib import Path
from types import SimpleNamespace
from typing import List
from src.utils.file import save_text_file
from src.logger import logger # Import logger module


class ProductHTMLGenerator:
    """Класс для генерации HTML для отдельных продуктов."""

    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path) -> None:
        """Создает HTML-файл для отдельного продукта.

        Args:
            product (SimpleNamespace): Детали продукта для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если происходит ошибка при создании HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> category_path = Path('path/to/category')
            >>> product = SimpleNamespace(
            ...     product_id='12345',
            ...     product_title='Example Product',
            ...     local_image_path='path/to/image.jpg',
            ...     target_sale_price=10.00,
            ...     target_sale_price_currency='USD',
            ...     target_original_price=15.00,
            ...     target_original_price_currency='USD',
            ...     second_level_category_name='Example Category',
            ...     promotion_link='https://example.com'
            ... )
            >>> ProductHTMLGenerator.set_product_html(product, str(category_path))
        """
        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / f'{product.product_id}.html'

        html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>{html.escape(product.product_title)}</title>
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css'>
    <link rel='stylesheet' href='styles.css'> <!-- Link to custom CSS file -->
</head>
<body>
    <div class='container'>
        <h1 class='my-4'>{html.escape(product.product_title)}</h1>
        <div class='card'>
            <img src='{Path(product.local_image_path).as_posix()}' alt='{html.escape(product.product_title)}' class='card-img-top'>
            <div class='card-body'>
                <p class='card-text'>Price: <span class='product-price'>{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                <p class='card-text'>Original Price: <span class='product-original-price'>{product.target_original_price} {product.target_original_price_currency}</span></p>
                <p class='card-text'>Category: <span class='product-category'>{html.escape(product.second_level_category_name)}</span></p>
                <a href='{product.promotion_link}' class='btn btn-primary'>Buy Now</a>
            </div>
        </div>
    </div>
    
    <script src='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js'></script>
</body>
</html>
"""
        try:
            save_text_file(html_content, html_path)
        except Exception as ex:
            logger.error(f'Error while saving HTML file for product {product.product_id}', ex, exc_info=True)


class CategoryHTMLGenerator:
    """Класс для генерации HTML для категорий продуктов."""

    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path) -> None:
        """Создает HTML-файл для категории.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если происходит ошибка при создании HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> category_path = Path('path/to/category')
            >>> products = [SimpleNamespace(
            ...     product_id='12345',
            ...     product_title='Example Product 1',
            ...     local_image_path='path/to/image1.jpg',
            ...     target_sale_price=10.00,
            ...     target_sale_price_currency='USD',
            ...     target_original_price=15.00,
            ...     target_original_price_currency='USD',
            ...     second_level_category_name='Example Category',
            ...     promotion_link='https://example.com'
            ... ),
            ... SimpleNamespace(
            ...     product_id='67890',
            ...     product_title='Example Product 2',
            ...     local_image_path='path/to/image2.jpg',
            ...     target_sale_price=20.00,
            ...     target_sale_price_currency='USD',
            ...     target_original_price=25.00,
            ...     second_level_category_name='Example Category',
            ...     target_original_price_currency='USD',
            ...     promotion_link='https://example.com'
            ... )
            ... ]
            >>> CategoryHTMLGenerator.set_category_html(products, str(category_path))
        """
        products_list = [products_list] if not isinstance(products_list, list) else products_list

        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>{html.escape(category_name)} Products</title>
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css'>
    <link rel='stylesheet' href='styles.css'> <!-- Link to custom CSS file -->
</head>
<body>
    <div class='container'>
        <h1 class='my-4'>{html.escape(category_name)} Products</h1>
        <div class='row product-grid'>
    """

        for product in products_list:
            image_url = Path(product.local_image_path).as_posix()
            html_content += f"""
                <div class='col-md-4 mb-4'>
                    <div class='card'>
                        <img src='{image_url}' alt='{html.escape(product.product_title)}' class='card-img-top'>
                        <div class='card-body'>
                            <h5 class='card-title'>{html.escape(product.product_title)}</h5>
                            <p class='card-text'>Price: <span class='product-price'>{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                            <p class='card-text'>Original Price: <span class='product-original-price'>{product.target_original_price} {product.target_original_price_currency}</span></p>
                            <p class='card-text'>Category: <span class='product-category'>{html.escape(product.second_level_category_name)}</span></p>
                            <a href='{product.promotion_link}' class='btn btn-primary'>Buy Now</a>
                        </div>
                    </div>
                </div>
            """

        html_content += """ 
        </div>
    </div>
    
    <script src='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js'></script>
</body>
</html>
"""
        try:
            save_text_file(html_content, html_path)
        except Exception as ex:
            logger.error(f'Error while saving HTML file for category {category_name}', ex, exc_info=True)


class CampaignHTMLGenerator:
    """Класс для генерации HTML для кампании."""

    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path) -> None:
        """Создает HTML-файл для кампании, перечисляя все категории.

        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        Raises:
            Exception: Если происходит ошибка при создании HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> campaign_path = Path('path/to/campaign')
            >>> categories = ['Category1', 'Category2']
            >>> CampaignHTMLGenerator.set_campaign_html(categories, str(campaign_path))
        """
        html_path = Path(campaign_path) / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Campaign Overview</title>
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css'>
    <link rel='stylesheet' href='styles.css'> <!-- Link to custom CSS file -->
</head>
<body>
    <div class='container'>
        <h1 class='my-4'>Campaign Overview</h1>
        <ul class='list-group'>
    """

        for category in categories:
            html_content += f"""
                <li class='list-group-item'>
                    <a href='{category}/index.html'>{html.escape(category)}</a>
                </li>
            """

        html_content += """ 
        </ul>
    </div>
    
    <script src='https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js'></script>
</body>
</html>
"""
        try:
            save_text_file(html_content, html_path)
        except Exception as ex:
            logger.error(f'Error while saving HTML file for campaign', ex, exc_info=True)