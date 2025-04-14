# Модуль для генерации HTML контента рекламной кампании

## Обзор

Модуль `html_generators.py` предназначен для генерации HTML-страниц, отображающих информацию о товарах и категориях товаров для рекламных кампаний. Он включает классы для создания HTML-страниц для отдельных продуктов, категорий продуктов и общей страницы кампании.

## Подробнее

Модуль содержит три основных класса: `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`. Каждый класс отвечает за создание HTML-страниц определенного уровня: отдельные продукты, категории продуктов и общая страница кампании, соответственно.

## Классы

### `ProductHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы отдельного продукта.

**Методы**:

- `set_product_html(product: SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для отдельного продукта.

#### `set_product_html`

```python
    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path):
        """ Создает HTML-файл для отдельного продукта.
        
        Args:
            product (SimpleNamespace): Объект, содержащий детали продукта для включения в HTML.
            category_path (str | Path): Путь, по которому нужно сохранить HTML-файл.
        """
```

**Как работает функция**:

Функция `set_product_html` генерирует HTML-страницу для заданного продукта. Она принимает объект `product`, содержащий информацию о продукте (название, цена, изображение, категория, ссылка на покупку), и путь `category_path`, указывающий, где сохранить HTML-файл. Функция создает HTML-файл с именем `product.product_id.html` в поддиректории `html` указанного пути `category_path`. В HTML-файле отображается название продукта, изображение, цена (обычная и акционная), категория и ссылка для покупки.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Пример объекта product
product = SimpleNamespace(
    product_id="12345",
    product_title="Example Product",
    local_image_path="images/example.jpg",
    target_sale_price="100",
    target_sale_price_currency="USD",
    target_original_price="120",
    target_original_price_currency="USD",
    second_level_category_name="Example Category",
    promotion_link="https://example.com/buy"
)

# Пример пути к категории
category_path = "campaign/category1"

# Вызов функции для создания HTML-страницы продукта
ProductHTMLGenerator.set_product_html(product, category_path)
```

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы категории продуктов.

**Методы**:

- `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для категории продуктов.

#### `set_category_html`

```python
    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Создает HTML-файл для категории.
        
        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.
        """
```

**Как работает функция**:

Функция `set_category_html` создает HTML-страницу для категории продуктов. Она принимает список объектов `products_list`, содержащих информацию о продуктах в данной категории, и путь `category_path`, где сохранить HTML-файл. Если `products_list` является одним объектом `SimpleNamespace`, он преобразуется в список. Функция создает HTML-файл с именем `index.html` в поддиректории `html` указанного пути `category_path`. В HTML-файле отображается название категории и список продуктов с изображениями, названиями, ценами и ссылками для покупки.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Пример списка продуктов
products_list = [
    SimpleNamespace(
        product_id="12345",
        product_title="Example Product 1",
        local_image_path="images/example1.jpg",
        target_sale_price="100",
        target_sale_price_currency="USD",
        target_original_price="120",
        target_original_price_currency="USD",
        second_level_category_name="Example Category",
        promotion_link="https://example.com/buy1"
    ),
    SimpleNamespace(
        product_id="67890",
        product_title="Example Product 2",
        local_image_path="images/example2.jpg",
        target_sale_price="200",
        target_sale_price_currency="USD",
        target_original_price="240",
        target_original_price_currency="USD",
        second_level_category_name="Example Category",
        promotion_link="https://example.com/buy2"
    )
]

# Пример пути к категории
category_path = "campaign/category1"

# Вызов функции для создания HTML-страницы категории
CategoryHTMLGenerator.set_category_html(products_list, category_path)
```

### `CampaignHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы кампании.

**Методы**:

- `set_campaign_html(categories: list[str], campaign_path: str | Path)`: Создает HTML-файл для кампании, перечисляющий все категории.

#### `set_campaign_html`

```python
    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path):
        """ Создает HTML-файл для кампании, перечисляющий все категории.
        
        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.
        """
```

**Как работает функция**:

Функция `set_campaign_html` создает HTML-страницу для кампании, которая содержит список категорий. Она принимает список `categories`, содержащий названия категорий, и путь `campaign_path`, где сохранить HTML-файл. Функция создает HTML-файл с именем `index.html` в указанном пути `campaign_path`. В HTML-файле отображается заголовок кампании и список категорий, каждая из которых является ссылкой на HTML-страницу соответствующей категории.

**Примеры**:

```python
from pathlib import Path

# Пример списка категорий
categories = ["category1", "category2", "category3"]

# Пример пути к кампании
campaign_path = "campaign"

# Вызов функции для создания HTML-страницы кампании
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)