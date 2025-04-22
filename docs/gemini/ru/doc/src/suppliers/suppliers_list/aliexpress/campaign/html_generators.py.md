# Модуль: Генераторы HTML контента рекламной кампании

## Обзор

Модуль содержит классы для генерации HTML-страниц, представляющих товары, категории и общую структуру рекламной кампании.
Он включает в себя классы `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`, каждый из которых отвечает за создание HTML-кода для соответствующего уровня представления данных.

## Подробнее

Модуль предназначен для автоматизации создания HTML-страниц, используемых в рекламных кампаниях.
Он позволяет генерировать отдельные страницы товаров, страницы категорий с перечнем товаров и общую страницу кампании со списком категорий.
Для стилизации используются Bootstrap и пользовательские CSS-стили.

## Классы

### `ProductHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы отдельного товара.

**Атрибуты**:
- Отсутствуют

**Методы**:
- `set_product_html()`: Создает HTML-файл для отдельного товара.

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы категории товаров.

**Атрибуты**:
- Отсутствуют

**Методы**:
- `set_category_html()`: Создает HTML-файл для категории товаров.

### `CampaignHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы кампании.

**Атрибуты**:
- Отсутствуют

**Методы**:
- `set_campaign_html()`: Создает HTML-файл для кампании, перечисляющий все категории.

## Методы классов

### `ProductHTMLGenerator.set_product_html`

```python
    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path):
        """ Создает HTML-файл для отдельного товара.

        Args:
            product (SimpleNamespace): Объект с деталями продукта для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.
        """
```

**Назначение**: Создает HTML-файл для отображения информации о конкретном товаре.

**Параметры**:
- `product` (SimpleNamespace): Объект, содержащий информацию о товаре, такую как ID, заголовок, цены, URL изображения и ссылку на продвижение.
- `category_path` (str | Path): Путь к директории, в которой будет сохранен HTML-файл товара.

**Возвращает**:
- Ничего. Функция сохраняет HTML-файл в указанной директории.

**Как работает функция**:
- Функция принимает информацию о товаре и путь к категории, в которой нужно сохранить HTML-файл.
- Формирует имя HTML-файла на основе ID товара.
- Создает HTML-структуру страницы, включая мета-теги, стили CSS (Bootstrap и custom styles), заголовок страницы, информацию о цене товара, ссылку на изображение и кнопку "Купить сейчас".
- Использует функцию `save_text_file` для сохранения сгенерированного HTML-кода в файл.
- Для экранирования небезопасных символов в product_title использует `html.escape(product.product_title)`.
- Сохраняет изображение товара, используя `product.local_image_path`.
- Сохраняет цену товара, используя `product.target_sale_price` и `product.target_sale_price_currency`.
- Ссылка на категорию: `product.second_level_category_name`.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Создание примера объекта товара
product = SimpleNamespace(
    product_id='12345',
    product_title='Example Product',
    target_sale_price=25.00,
    target_sale_price_currency='USD',
    target_original_price=30.00,
    target_original_price_currency='USD',
    second_level_category_name='Example Category',
    promotion_link='http://example.com/product/12345',
    local_image_path='/path/to/image.jpg'
)

# Определение пути для сохранения HTML-файла
category_path = 'path/to/category'

# Вызов функции для создания HTML-файла продукта
ProductHTMLGenerator.set_product_html(product, category_path)
```

### `CategoryHTMLGenerator.set_category_html`

```python
    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Создает HTML-файл для категории.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список продуктов для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML-файла.
        """
```

**Назначение**: Создает HTML-файл, отображающий список товаров в заданной категории.

**Параметры**:
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов, содержащих информацию о товарах в категории. Если передан один объект `SimpleNamespace`, он преобразуется в список.
- `category_path` (str | Path): Путь к директории, в которой будет сохранен HTML-файл категории.

**Возвращает**:
- Ничего. Функция сохраняет HTML-файл в указанной директории.

**Как работает функция**:
- Функция принимает список товаров и путь к категории, в которой нужно сохранить HTML-файл.
- Формирует имя HTML-файла как "index.html".
- Создает HTML-структуру страницы, включая мета-теги, стили CSS (Bootstrap и custom styles), заголовок страницы и сетку товаров.
- Для каждого товара в списке генерирует HTML-код, отображающий изображение, заголовок, цену, оригинальную цену и ссылку "Купить сейчас".
- Использует функцию `save_text_file` для сохранения сгенерированного HTML-кода в файл.
- Проверяет тип входного параметра `products_list` и преобразует его в список, если это не список.
- Экранирует имя категории и заголовки продуктов с использованием `html.escape()`.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Создание списка примеров объектов товаров
products_list = [
    SimpleNamespace(
        product_id='12345',
        product_title='Example Product 1',
        target_sale_price=25.00,
        target_sale_price_currency='USD',
        target_original_price=30.00,
        target_original_price_currency='USD',
        second_level_category_name='Example Category',
        promotion_link='http://example.com/product/12345',
        local_image_path='/path/to/image1.jpg'
    ),
    SimpleNamespace(
        product_id='67890',
        product_title='Example Product 2',
        target_sale_price=15.00,
        target_sale_price_currency='USD',
        target_original_price=20.00,
        target_original_price_currency='USD',
        second_level_category_name='Example Category',
        promotion_link='http://example.com/product/67890',
        local_image_path='/path/to/image2.jpg'
    )
]

# Определение пути для сохранения HTML-файла
category_path = 'path/to/category'

# Вызов функции для создания HTML-файла категории
CategoryHTMLGenerator.set_category_html(products_list, category_path)
```

### `CampaignHTMLGenerator.set_campaign_html`

```python
    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path):
        """ Creates an HTML file for the campaign, listing all categories.

        Args:
            categories (list[str]): Список названий категорий.
            campaign_path (str | Path): Путь для сохранения HTML-файла.
        """
```

**Назначение**: Создает HTML-файл, содержащий обзор кампании со списком категорий.

**Параметры**:
- `categories` (list[str]): Список строк, представляющих названия категорий в кампании.
- `campaign_path` (str | Path): Путь к директории, в которой будет сохранен HTML-файл кампании.

**Возвращает**:
- Ничего. Функция сохраняет HTML-файл в указанной директории.

**Как работает функция**:
- Функция принимает список категорий и путь к директории для сохранения HTML-файла.
- Формирует имя HTML-файла как "index.html".
- Создает HTML-структуру страницы, включая мета-теги, стили CSS (Bootstrap и custom styles), заголовок страницы и список категорий в виде ссылок.
- Для каждой категории генерирует HTML-код, создающий элемент списка со ссылкой на HTML-страницу категории.
- Использует функцию `save_text_file` для сохранения сгенерированного HTML-кода в файл.
- Генерирует HTML-код для каждой категории в списке `categories`.
-  Экранирует имя категории с использованием `html.escape()`.

**Примеры**:

```python
from pathlib import Path

# Создание списка названий категорий
categories = ['Category 1', 'Category 2', 'Category 3']

# Определение пути для сохранения HTML-файла
campaign_path = 'path/to/campaign'

# Вызов функции для создания HTML-файла кампании
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)