### Анализ кода модуля `html_generators`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на классы, каждый из которых отвечает за генерацию HTML для определенной сущности (продукт, категория, кампания).
  - Использованы аннотации типов для параметров функций, что улучшает читаемость и упрощает отладку.
  - Применяется `html.escape` для предотвращения XSS-атак.
- **Минусы**:
  - Отсутствует обработка исключений.
  - Не используется логирование.
  - Не все строки документированы.
  - Не хватает документации модуля.
  - Не используются f-strings для форматирования строк (хотя они и присутствуют, но не везде, где это возможно).
  - Есть импорт `header`, но он не используется. Стоит его удалить.
  - Параметр `mode` в функции `save_text_file` не указан.

**Рекомендации по улучшению:**

1. **Добавить документацию модуля**:
   - Описать назначение модуля, основные классы и примеры использования.

2. **Добавить docstring для всех функций и классов**:
   - Описать параметры, возвращаемые значения и возможные исключения.
   - Для внутренних функций также добавить docstring.

3. **Реализовать обработку исключений**:
   - Обернуть запись файлов в блоки `try...except` для обработки возможных ошибок.
   - Использовать `logger.error` для записи информации об ошибках.

4. **Удалить неиспользуемый импорт**:
   - Удалить `import header`, так как он не используется в коде.

5. **Улучшить форматирование строк**:
   - Использовать f-strings для более читаемого форматирования HTML-контента.

6. **Параметр `mode` в функции `save_text_file`**:
   - Добавить параметр `mode` в функцию `save_text_file` для указания режима записи файла.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/html_generators.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML контента рекламной кампании AliExpress.
===============================================================

Модуль содержит классы для создания HTML-страниц для отдельных товаров, категорий и кампаний.
Он использует строковые шаблоны для формирования HTML-кода и сохраняет его в файлы.

Пример использования:
----------------------

>>> from pathlib import Path
>>> from types import SimpleNamespace
>>> product = SimpleNamespace(product_id='123', product_title='Test Product', local_image_path='img/test.jpg', target_sale_price='10.00', target_sale_price_currency='USD', target_original_price='15.00', target_original_price_currency='USD', second_level_category_name='Test Category', promotion_link='http://example.com')
>>> category_path = Path('./test_category')
>>> ProductHTMLGenerator.set_product_html(product, str(category_path))
"""

from pathlib import Path
from types import SimpleNamespace
from src.utils.file import save_text_file
import html
from src.logger import logger  # Добавлен импорт logger


class ProductHTMLGenerator:
    """Класс для генерации HTML для отдельных товаров."""

    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path) -> None:
        """Создает HTML-файл для отдельного товара.

        Args:
            product (SimpleNamespace): Детали продукта для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Raises:
            Exception: Если происходит ошибка при сохранении HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> product = SimpleNamespace(product_id='123', product_title='Test Product', local_image_path='img/test.jpg', target_sale_price='10.00', target_sale_price_currency='USD', target_original_price='15.00', target_original_price_currency='USD', second_level_category_name='Test Category', promotion_link='http://example.com')
            >>> category_path = Path('./test_category')
            >>> ProductHTMLGenerator.set_product_html(product, str(category_path))
        """
        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / f"{product.product_id}.html"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            save_text_file(file_path=html_content, data=html_path)
        except Exception as ex:
            logger.error('Error while saving HTML file', ex, exc_info=True)


class CategoryHTMLGenerator:
    """Класс для генерации HTML для категорий продуктов."""

    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path) -> None:
        """Создает HTML-файл для категории.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Raises:
            Exception: Если происходит ошибка при сохранении HTML-файла.

        Example:
            >>> from pathlib import Path
            >>> from types import SimpleNamespace
            >>> products = [SimpleNamespace(product_id='123', product_title='Test Product', local_image_path='img/test.jpg', target_sale_price='10.00', target_sale_price_currency='USD', target_original_price='15.00', target_original_price_currency='USD', second_level_category_name='Test Category', promotion_link='http://example.com')]
            >>> category_path = Path('./test_category')
            >>> CategoryHTMLGenerator.set_category_html(products, str(category_path))
        """
        products_list = products_list if isinstance(products_list, list) else [products_list]

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
            save_text_file(file_path=html_content, data=html_path)
        except Exception as ex:
            logger.error('Error while saving HTML file', ex, exc_info=True)


class CampaignHTMLGenerator:
    """Класс для генерации HTML для кампании."""

    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path) -> None:
        """Создает HTML-файл для кампании, перечисляющий все категории.

        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.

        Raises:
            Exception: Если происходит ошибка при сохранении HTML-файла.
        
        Example:
            >>> from pathlib import Path
            >>> categories = ['Category1', 'Category2']
            >>> campaign_path = Path('./test_campaign')
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
            save_text_file(file_path=html_content, data=html_path)
        except Exception as ex:
            logger.error('Error while saving HTML file', ex, exc_info=True)