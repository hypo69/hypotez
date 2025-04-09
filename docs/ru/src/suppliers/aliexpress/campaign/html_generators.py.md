# Модуль для генерации HTML контента рекламной кампании

## Обзор

Этот модуль предназначен для генерации HTML-страниц для рекламных кампаний, ориентированных на товары с AliExpress. Он включает классы для создания HTML-страниц как для отдельных товаров, так и для категорий товаров и общей страницы кампании.

## Подробнее

Модуль содержит три основных класса: `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`. Каждый класс отвечает за создание HTML-страниц определенного уровня:

- `ProductHTMLGenerator` создает HTML-страницу для одного товара, отображая его название, изображение, цену и ссылку на покупку.
- `CategoryHTMLGenerator` создает HTML-страницу для категории товаров, перечисляя все товары в данной категории с аналогичной информацией.
- `CampaignHTMLGenerator` создает общую HTML-страницу кампании, содержащую список категорий товаров, представленных в кампании, со ссылками на соответствующие страницы категорий.

## Классы

### `ProductHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы отдельного продукта.

**Принцип работы**:
Класс `ProductHTMLGenerator` содержит один статический метод `set_product_html`, который принимает информацию о продукте и путь для сохранения HTML-файла. Этот метод создает HTML-страницу, содержащую информацию о продукте, такую как название, изображение, цена и ссылку на покупку. Затем он использует функцию `save_text_file` для сохранения созданного HTML-контента в файл.

#### `set_product_html`

```python
    @staticmethod
    def set_product_html(product: SimpleNamespace, category_path: str | Path):
        """ Creates an HTML file for an individual product.
        
        @param product: The product details to include in the HTML.
        @param category_path: The path to save the HTML file.
        """
        ...
```

**Назначение**: Создает HTML-файл для отдельного продукта.

**Параметры**:
- `product` (SimpleNamespace): Объект, содержащий детали продукта, такие как название, описание, цена, URL изображения и ссылку на покупку.
- `category_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл продукта.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- Отсутствуют явные исключения.

**Как работает функция**:

1. **Определение имени категории и пути к HTML-файлу**: Извлекается имя категории из `category_path` и формируется путь к HTML-файлу продукта.
2. **Формирование HTML-контента**: Создается HTML-контент, включающий метаданные, стили CSS и информацию о продукте (название, изображение, цена, ссылка на покупку).
3. **Сохранение HTML-файла**: Используется функция `save_text_file` для сохранения HTML-контента в файл по указанному пути.

```ascii
Определение имени категории и пути к HTML-файлу
│
↓
Формирование HTML-контента
│
↓
Сохранение HTML-файла
```

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример данных о продукте
product = SimpleNamespace(
    product_id='12345',
    product_title='Example Product',
    local_image_path='images/example.jpg',
    target_sale_price='19.99',
    target_sale_price_currency='USD',
    target_original_price='29.99',
    target_original_price_currency='USD',
    second_level_category_name='Electronics',
    promotion_link='https://example.com/product/12345'
)

# Пример пути к категории
category_path = 'campaign/category1'

# Вызов функции для создания HTML-файла продукта
ProductHTMLGenerator.set_product_html(product, category_path)
```

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы категории продуктов.

**Принцип работы**:
Класс `CategoryHTMLGenerator` содержит статический метод `set_category_html`, который создает HTML-страницу для отображения списка продуктов в заданной категории. Он принимает список объектов продуктов и путь для сохранения HTML-файла. Метод генерирует HTML-контент, содержащий информацию о каждом продукте в списке, и сохраняет его в файл `index.html` в указанном каталоге.

#### `set_category_html`

```python
    @staticmethod
    def set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path):
        """ Creates an HTML file for the category.
        
        @param products_list: List of products to include in the HTML.
        @param category_path: Path to save the HTML file.
        """
        ...
```

**Назначение**: Создает HTML-файл для категории продуктов.

**Параметры**:
- `products_list` (list[SimpleNamespace] | SimpleNamespace): Список объектов, содержащих детали продуктов в категории. Если передан один объект, он преобразуется в список.
- `category_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл категории.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- Отсутствуют явные исключения.

**Как работает функция**:

1. **Преобразование входных данных**: Если `products_list` не является списком, он преобразуется в список, чтобы обеспечить единообразную обработку.
2. **Определение имени категории и пути к HTML-файлу**: Извлекается имя категории из `category_path` и формируется путь к HTML-файлу `index.html` в подкаталоге `html`.
3. **Формирование HTML-контента**: Создается HTML-контент, включающий метаданные, стили CSS и информацию о каждом продукте в списке. Для каждого продукта генерируется HTML-код, содержащий изображение, название, цену и ссылку на покупку.
4. **Сохранение HTML-файла**: Используется функция `save_text_file` для сохранения HTML-контента в файл `index.html` по указанному пути.

```ascii
Преобразование входных данных
│
↓
Определение имени категории и пути к HTML-файлу
│
↓
Формирование HTML-контента
│
↓
Сохранение HTML-файла
```

**Примеры**:

```python
from types import SimpleNamespace
from pathlib import Path

# Пример данных о продуктах
product1 = SimpleNamespace(
    product_id='12345',
    product_title='Example Product 1',
    local_image_path='images/example1.jpg',
    target_sale_price='19.99',
    target_sale_price_currency='USD',
    target_original_price='29.99',
    target_original_price_currency='USD',
    second_level_category_name='Electronics',
    promotion_link='https://example.com/product/12345'
)

product2 = SimpleNamespace(
    product_id='67890',
    product_title='Example Product 2',
    local_image_path='images/example2.jpg',
    target_sale_price='29.99',
    target_sale_price_currency='USD',
    target_original_price='39.99',
    target_original_price_currency='USD',
    second_level_category_name='Electronics',
    promotion_link='https://example.com/product/67890'
)

products_list = [product1, product2]

# Пример пути к категории
category_path = 'campaign/category1'

# Вызов функции для создания HTML-файла категории
CategoryHTMLGenerator.set_category_html(products_list, category_path)
```

### `CampaignHTMLGenerator`

**Описание**: Класс для генерации HTML-страницы кампании, содержащей список категорий.

**Принцип работы**:
Класс `CampaignHTMLGenerator` содержит статический метод `set_campaign_html`, который создает HTML-страницу для отображения списка категорий товаров в кампании. Он принимает список названий категорий и путь для сохранения HTML-файла. Метод генерирует HTML-контент, содержащий список категорий со ссылками на соответствующие страницы категорий, и сохраняет его в файл `index.html` в указанном каталоге.

#### `set_campaign_html`

```python
    @staticmethod
    def set_campaign_html(categories: list[str], campaign_path: str | Path):
        """ Creates an HTML file for the campaign, listing all categories.
        
        @param categories: List of category names.
        @param campaign_path: Path to save the HTML file.
        """
        ...
```

**Назначение**: Создает HTML-файл для кампании, перечисляющий все категории.

**Параметры**:
- `categories` (list[str]): Список названий категорий товаров в кампании.
- `campaign_path` (str | Path): Путь к каталогу, в котором будет сохранен HTML-файл кампании.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- Отсутствуют явные исключения.

**Как работает функция**:

1. **Определение пути к HTML-файлу**: Формируется путь к HTML-файлу `index.html` в каталоге кампании.
2. **Формирование HTML-контента**: Создается HTML-контент, включающий метаданные, стили CSS и список категорий со ссылками на соответствующие страницы категорий.
3. **Сохранение HTML-файла**: Используется функция `save_text_file` для сохранения HTML-контента в файл `index.html` по указанному пути.

```ascii
Определение пути к HTML-файлу
│
↓
Формирование HTML-контента
│
↓
Сохранение HTML-файла
```

**Примеры**:

```python
from pathlib import Path

# Пример списка категорий
categories = ['category1', 'category2', 'category3']

# Пример пути к кампании
campaign_path = 'campaign'

# Вызов функции для создания HTML-файла кампании
CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
```