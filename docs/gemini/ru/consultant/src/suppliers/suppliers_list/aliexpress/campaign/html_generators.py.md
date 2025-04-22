### **Анализ кода модуля `html_generators.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на классы, каждый из которых отвечает за генерацию HTML для определенного уровня (товар, категория, кампания).
  - Использование `html.escape` для предотвращения XSS-атак.
  - Применение `Path` для работы с путями.
- **Минусы**:
  - Не все параметры функций аннотированы типами.
  - Отсутствуют docstring для классов.
  - Docstring написаны на английском языке, требуется перевод на русский.
  - Используется f-строки для формирования HTML, что может быть не самым эффективным способом при больших объемах данных.
  - Нет обработки исключений при сохранении файлов.
  - Не используется модуль `logger` для логирования.
  - Не указаны `Args` и `Returns` в docstring.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:

    *   Добавьте аннотации типов для всех параметров функций и возвращаемых значений, где это необходимо.

2.  **Добавить docstring для классов**:

    *   Добавьте подробные docstring для каждого класса, описывающие его назначение, атрибуты и методы.

3.  **Перевести docstring на русский язык**:

    *   Переведите все docstring на русский язык, чтобы соответствовать требованиям проекта.

4.  **Использовать шаблонизатор**:

    *   Рассмотрите возможность использования шаблонизатора (например, Jinja2) для генерации HTML. Это улучшит читаемость кода и упростит поддержку.

5.  **Добавить обработку исключений**:

    *   Добавьте блоки `try...except` для обработки возможных исключений при сохранении файлов.

6.  **Использовать логирование**:

    *   Используйте модуль `logger` для логирования важных событий, таких как создание HTML-файлов, возникновение ошибок и т.д.

7.  **Улучшить docstring**:

    *   Добавьте `Args` и `Returns` в docstring для каждой функции и метода.
    *   Добавьте примеры использования в docstring.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/html_generators.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress.campaign
    :platform: Windows, Unix
    :synopsis: Генератор HTML контента рекламной кампании

"""

import header
import html
from pathlib import Path
from types import SimpleNamespace
from typing import List
from src.utils.file import save_text_file
from src.logger import logger  # Добавлен импорт logger


class ProductHTMLGenerator:
    """
    Класс для генерации HTML для отдельного товара.
    =================================================

    Этот класс предоставляет метод для создания HTML-файла, содержащего информацию о товаре,
    включая изображение, цену, категорию и ссылку на покупку.

    """

    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path) -> None:
        """
        Создает HTML-файл для отдельного товара.

        Args:
            product (SimpleNamespace): Объект с деталями товара для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

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
                <p class="card-text">Цена: <span class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                <p class="card-text">Оригинальная цена: <span class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</span></p>
                <p class="card-text">Категория: <span class="product-category">{html.escape(product.second_level_category_name)}</span></p>
                <a href="{product.promotion_link}" class="btn btn-primary">Купить сейчас</a>
            </div>
        </div>
    </div>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
        try:
            save_text_file(html_content, html_path)
            logger.info(f"HTML-файл для товара {product.product_id} успешно создан в {html_path}")  # Логгирование
        except Exception as ex:
            logger.error(f"Ошибка при создании HTML-файла для товара {product.product_id}", ex, exc_info=True)  # Логгирование ошибки


class CategoryHTMLGenerator:
    """
    Класс для генерации HTML для категории товаров.
    =================================================

    Этот класс предоставляет метод для создания HTML-файла, содержащего список товаров в категории,
    с изображениями, ценами, категориями и ссылками на покупку.

    """

    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path) -> None:
        """
        Создает HTML-файл для категории товаров.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список товаров для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        """
        products_list = products_list if isinstance(products_list, list) else [products_list]

        category_name = Path(category_path).name
        html_path = Path(category_path) / 'html' / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(category_name)} Товары</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css"> <!-- Link to custom CSS file -->
</head>
<body>
    <div class="container">
        <h1 class="my-4">{html.escape(category_name)} Товары</h1>
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
                            <p class="card-text">Цена: <span class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</span></p>
                            <p class="card-text">Оригинальная цена: <span class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</span></p>
                            <p class="card-text">Категория: <span class="product-category">{html.escape(product.second_level_category_name)}</span></p>
                            <a href="{product.promotion_link}" class="btn btn-primary">Купить сейчас</a>
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
        try:
            save_text_file(html_content, html_path)
            logger.info(f"HTML-файл для категории {category_name} успешно создан в {html_path}")  # Логгирование
        except Exception as ex:
            logger.error(f"Ошибка при создании HTML-файла для категории {category_name}", ex, exc_info=True)  # Логгирование ошибки


class CampaignHTMLGenerator:
    """
    Класс для генерации HTML для кампании.
    =================================================

    Этот класс предоставляет метод для создания HTML-файла, содержащего список категорий в кампании
    со ссылками на соответствующие страницы категорий.

    """

    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path) -> None:
        """
        Создает HTML-файл для кампании, перечисляющий все категории.

        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            None

        """
        html_path = Path(campaign_path) / 'index.html'

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Обзор кампании</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="styles.css"> <!-- Link to custom CSS file -->
</head>
<body>
    <div class="container">
        <h1 class="my-4">Обзор кампании</h1>
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
        try:
            save_text_file(html_content, html_path)
            logger.info(f"HTML-файл для кампании успешно создан в {html_path}")  # Логгирование
        except Exception as ex:
            logger.error(f"Ошибка при создании HTML-файла для кампании", ex, exc_info=True)  # Логгирование ошибки