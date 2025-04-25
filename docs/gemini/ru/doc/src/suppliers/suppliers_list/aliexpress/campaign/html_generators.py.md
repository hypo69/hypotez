# Модуль для генерации HTML-контента рекламных кампаний

## Обзор

Модуль `html_generators.py` содержит классы для генерации HTML-файлов для продуктов, категорий и всей рекламной кампании. 

## Классы

### `ProductHTMLGenerator`

**Описание**:  Класс для генерации HTML-файлов для отдельных продуктов.

**Атрибуты**: 
    - Нет.

**Методы**:
    - `set_product_html(product: SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для отдельного продукта.

#### `set_product_html`

**Назначение**: 
    - Создает HTML-файл для отдельного продукта, используя данные из объекта `SimpleNamespace`.

**Параметры**:
    - `product` (SimpleNamespace): Объект `SimpleNamespace`, содержащий данные о продукте. 
    - `category_path` (str | Path): Путь к каталогу, в котором нужно сохранить HTML-файл.

**Возвращает**:
    - Нет.

**Вызывает исключения**:
    - Нет.

**Как работает функция**:
    - Функция формирует HTML-контент, используя данные из объекта `product`, включая название, цену, описание и ссылку.
    - Сохраняет полученный HTML-код в файл `html_path`, который определяется путем объединения пути к каталогу `category_path` с именем продукта и суффиксом `.html`.

**Примеры**:
    ```python
    from pathlib import Path
    from types import SimpleNamespace

    product = SimpleNamespace(
        product_id='123456789',
        product_title='Название товара',
        local_image_path='images/product_123456789.jpg',
        target_sale_price=10.00,
        target_sale_price_currency='USD',
        target_original_price=15.00,
        target_original_price_currency='USD',
        second_level_category_name='Категория товара',
        promotion_link='https://www.aliexpress.com/item/123456789'
    )

    category_path = Path('path/to/category')

    ProductHTMLGenerator.set_product_html(product, category_path)
    ```

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-файлов для категорий продуктов.

**Атрибуты**: 
    - Нет.

**Методы**:
    - `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для категории, используя список продуктов.

#### `set_category_html`

**Назначение**: 
    - Создает HTML-файл для категории, используя список продуктов, представленных в виде объектов `SimpleNamespace`.

**Параметры**:
    - `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов `SimpleNamespace`, представляющих продукты, или один объект `SimpleNamespace` (в случае одиночного продукта).
    - `category_path` (str | Path): Путь к каталогу, в котором нужно сохранить HTML-файл.

**Возвращает**:
    - Нет.

**Вызывает исключения**:
    - Нет.

**Как работает функция**:
    - Функция формирует HTML-контент, используя данные из `products_list`, включая название, цену, описание и ссылку на каждый продукт.
    - Сохраняет полученный HTML-код в файл `html_path`, который определяется путем объединения пути к каталогу `category_path` с именем `index.html`.

**Примеры**:
    ```python
    from pathlib import Path
    from types import SimpleNamespace

    products_list = [
        SimpleNamespace(
            product_id='123456789',
            product_title='Название товара 1',
            local_image_path='images/product_123456789.jpg',
            target_sale_price=10.00,
            target_sale_price_currency='USD',
            target_original_price=15.00,
            target_original_price_currency='USD',
            second_level_category_name='Категория товара',
            promotion_link='https://www.aliexpress.com/item/123456789'
        ),
        SimpleNamespace(
            product_id='987654321',
            product_title='Название товара 2',
            local_image_path='images/product_987654321.jpg',
            target_sale_price=20.00,
            target_sale_price_currency='USD',
            target_original_price=25.00,
            target_original_price_currency='USD',
            second_level_category_name='Категория товара',
            promotion_link='https://www.aliexpress.com/item/987654321'
        )
    ]

    category_path = Path('path/to/category')

    CategoryHTMLGenerator.set_category_html(products_list, category_path)
    ```

### `CampaignHTMLGenerator`

**Описание**:  Класс для генерации HTML-файлов для рекламной кампании.

**Атрибуты**: 
    - Нет.

**Методы**:
    - `set_campaign_html(categories: list[str], campaign_path: str | Path)`: Создает HTML-файл для рекламной кампании, используя список категорий.

#### `set_campaign_html`

**Назначение**: 
    - Создает HTML-файл для рекламной кампании, используя список категорий.

**Параметры**:
    - `categories` (list[str]): Список названий категорий.
    - `campaign_path` (str | Path): Путь к каталогу, в котором нужно сохранить HTML-файл.

**Возвращает**:
    - Нет.

**Вызывает исключения**:
    - Нет.

**Как работает функция**:
    - Функция формирует HTML-контент, используя список `categories`, добавляя ссылки на соответствующие HTML-файлы для каждой категории.
    - Сохраняет полученный HTML-код в файл `html_path`, который определяется путем объединения пути к каталогу `campaign_path` с именем `index.html`.

**Примеры**:
    ```python
    from pathlib import Path

    categories = ['Категория 1', 'Категория 2', 'Категория 3']
    campaign_path = Path('path/to/campaign')

    CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
    ```