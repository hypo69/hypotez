# Модуль для генерации HTML контента рекламной кампании

## Обзор

Модуль содержит классы для генерации HTML-страниц, представляющих товары, категории и общую структуру рекламной кампании. Он включает в себя классы `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`, которые отвечают за создание HTML-файлов для отдельных продуктов, категорий продуктов и общего представления рекламной кампании соответственно.

## Подробнее

Этот модуль предоставляет функциональность для автоматического создания HTML-страниц на основе данных о товарах и категориях, полученных, например, из AliExpress. Он использует строковые шаблоны и функцию `save_text_file` для сохранения HTML-контента в файлы. Модуль предназначен для упрощения процесса создания рекламных кампаний, позволяя автоматически генерировать HTML-страницы с информацией о товарах и категориях.

## Классы

### `ProductHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для отдельного товара.

**Методы**:

- `set_product_html(product: SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для отдельного товара.

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для категории товаров.

**Методы**:

- `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для категории продуктов.

### `CampaignHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для рекламной кампании.

**Методы**:

- `set_campaign_html(categories: list[str], campaign_path: str | Path)`: Создает HTML-файл для кампании, перечисляющий все категории.

## Методы класса `ProductHTMLGenerator`

### `set_product_html`

```python
@staticmethod
def set_product_html(product: SimpleNamespace, category_path: str | Path):
    """Создает HTML-файл для отдельного товара.

    Args:
        product (SimpleNamespace): Детали продукта, которые необходимо включить в HTML.
        category_path (str | Path): Путь для сохранения HTML-файла.
    """
```

**Назначение**: Создает HTML-файл для отдельного товара на основе предоставленных данных о продукте.

**Параметры**:

- `product` (SimpleNamespace): Объект, содержащий детали продукта, такие как `product_title`, `product_id`, `local_image_path`, `target_sale_price`, `target_sale_price_currency`, `target_original_price`, `target_original_price_currency`, `second_level_category_name` и `promotion_link`.
- `category_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл продукта.

**Как работает функция**:

1. Извлекает имя категории из `category_path`.
2. Формирует путь к HTML-файлу продукта: `<category_path>/html/<product.product_id>.html`.
3. Создает HTML-контент, используя данные из объекта `product`. HTML-контент включает заголовок страницы, изображение продукта, цену, оригинальную цену, категорию и ссылку для покупки.
4. Вызывает функцию `save_text_file` для сохранения HTML-контента в файл по указанному пути.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример объекта product
product = SimpleNamespace(
    product_title="Example Product",
    product_id="12345",
    local_image_path="/path/to/image.jpg",
    target_sale_price="19.99",
    target_sale_price_currency="USD",
    target_original_price="29.99",
    target_original_price_currency="USD",
    second_level_category_name="Example Category",
    promotion_link="https://example.com/product/12345"
)

# Пример пути к категории
category_path = "path/to/category"

# Вызов функции для создания HTML-файла продукта
ProductHTMLGenerator.set_product_html(product, category_path)
```

## Методы класса `CategoryHTMLGenerator`

### `set_category_html`

```python
@staticmethod
def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
    """Создает HTML-файл для категории.

    Args:
        products_list (list[SimpleNamespace] | SimpleNamespace): Список товаров для включения в HTML.
        category_path (str | Path): Путь для сохранения HTML-файла.
    """
```

**Назначение**: Создает HTML-файл для категории продуктов, отображая список товаров в этой категории.

**Параметры**:

- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов, содержащих информацию о продуктах в категории. Если передан один объект, он преобразуется в список.
- `category_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл категории.

**Как работает функция**:

1. Преобразует `products_list` в список, если это не список.
2. Извлекает имя категории из `category_path`.
3. Формирует путь к HTML-файлу категории: `<category_path>/html/index.html`.
4. Создает HTML-контент, начиная с заголовка страницы и структуры таблицы.
5. Итерируется по списку продуктов и добавляет HTML-код для каждого продукта, включая изображение, название, цену, оригинальную цену, категорию и ссылку для покупки.
6. Завершает HTML-контент закрывающими тегами.
7. Вызывает функцию `save_text_file` для сохранения HTML-контента в файл по указанному пути.

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример списка products
products_list = [
    SimpleNamespace(
        product_title="Example Product 1",
        local_image_path="/path/to/image1.jpg",
        target_sale_price="19.99",
        target_sale_price_currency="USD",
        target_original_price="29.99",
        target_original_price_currency="USD",
        second_level_category_name="Example Category",
        promotion_link="https://example.com/product/1"
    ),
    SimpleNamespace(
        product_title="Example Product 2",
        local_image_path="/path/to/image2.jpg",
        target_sale_price="29.99",
        target_sale_price_currency="USD",
        target_original_price="39.99",
        target_original_price_currency="USD",
        second_level_category_name="Example Category",
        promotion_link="https://example.com/product/2"
    )
]

# Пример пути к категории
category_path = "path/to/category"

# Вызов функции для создания HTML-файла категории
CategoryHTMLGenerator.set_category_html(products_list, category_path)
```

## Методы класса `CampaignHTMLGenerator`

### `set_campaign_html`

```python
@staticmethod
def set_campaign_html(categories: list[str], campaign_path: str | Path):
    """Создает HTML-файл для кампании, перечисляющий все категории.

    Args:
        categories (list[str]): Список названий категорий.
        campaign_path (str | Path): Путь для сохранения HTML-файла.
    """
```

**Назначение**: Создает HTML-файл для рекламной кампании, который содержит список категорий, представленных в кампании.

**Параметры**:

- `categories` (list[str]): Список названий категорий, которые будут отображены в HTML-файле кампании.
- `campaign_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл кампании.

**Как работает функция**:

1. Формирует путь к HTML-файлу кампании: `<campaign_path>/index.html`.
2. Создает HTML-контент, начиная с заголовка страницы и структуры списка категорий.
3. Итерируется по списку категорий и добавляет HTML-код для каждой категории, создавая ссылку на HTML-файл категории.
4. Завершает HTML-контент закрывающими тегами.
5. Вызывает функцию `save_text_file` для сохранения HTML-контента в файл по указанному пути.

**Примеры**:

```python
from pathlib import Path

# Пример списка категорий
categories = ["Category1", "Category2", "Category3"]

# Пример пути к кампании
campaign_path = "path/to/campaign"

# Вызов функции для создания HTML-файла кампании
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)