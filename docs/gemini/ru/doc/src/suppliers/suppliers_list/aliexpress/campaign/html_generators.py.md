# Модуль для генерации HTML-контента рекламной кампании AliExpress

## Обзор

Модуль содержит классы для генерации HTML-контента рекламной кампании, включая отдельные продукты, категории и общую страницу кампании. Он обеспечивает создание структурированных HTML-файлов с использованием данных о продуктах и категориях, а также стилей Bootstrap.

## Подробней

Модуль `html_generators.py` предназначен для автоматического создания HTML-страниц для рекламных кампаний AliExpress. Он включает три класса: `ProductHTMLGenerator`, `CategoryHTMLGenerator` и `CampaignHTMLGenerator`, каждый из которых отвечает за генерацию HTML-кода для определенного уровня кампании: отдельного продукта, категории продуктов и общей страницы кампании соответственно.

Код использует библиотеки `pathlib` для работы с путями к файлам и `html` для экранирования текста, чтобы предотвратить XSS-атаки. Он также использует `SimpleNamespace` для представления данных о продуктах.

## Классы

### `ProductHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для отдельных продуктов.

**Методы**:

- `set_product_html(product: SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для отдельного продукта.

   **Назначение**: Генерация HTML-страницы продукта на основе предоставленных данных.

   **Параметры**:
   - `product` (`SimpleNamespace`): Объект, содержащий информацию о продукте.
   - `category_path` (`str` | `Path`): Путь к каталогу, в котором нужно сохранить HTML-файл.

   **Возвращает**:
   - `None`: Функция ничего не возвращает, но создает HTML-файл.

   **Как работает функция**:
   - Функция принимает данные о продукте и путь к категории.
   - Формирует путь к HTML-файлу продукта, используя `product_id`.
   - Создает HTML-структуру страницы продукта, включая заголовок, изображение, цену, категорию и ссылку для покупки.
   - Использует метод `save_text_file` для сохранения HTML-кода в файл.

   **Примеры**:
   ```python
   from types import SimpleNamespace
   from pathlib import Path
   product_data = SimpleNamespace(
       product_id='12345',
       product_title='Test Product',
       local_image_path='images/test.jpg',
       target_sale_price='10.00',
       target_sale_price_currency='USD',
       target_original_price='12.00',
       target_original_price_currency='USD',
       second_level_category_name='Test Category',
       promotion_link='https://example.com'
   )
   category_path = 'test_category'
   ProductHTMLGenerator.set_product_html(product_data, category_path)
   # Будет создан файл test_category/html/12345.html с HTML-содержимым продукта
   ```

### `CategoryHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для категорий продуктов.

**Методы**:

- `set_category_html(products_list: list[SimpleNamespace] | SimpleNamespace, category_path: str | Path)`: Создает HTML-файл для категории продуктов.

   **Назначение**: Генерация HTML-страницы категории, отображающей список продуктов.

   **Параметры**:
   - `products_list` (`list[SimpleNamespace]` | `SimpleNamespace`): Список объектов `SimpleNamespace`, содержащих информацию о продуктах.
   - `category_path` (`str` | `Path`): Путь к каталогу, в котором нужно сохранить HTML-файл.

   **Возвращает**:
   - `None`: Функция ничего не возвращает, но создает HTML-файл.

   **Как работает функция**:
   - Функция принимает список данных о продуктах и путь к категории.
   - Формирует путь к HTML-файлу категории (`index.html`).
   - Создает HTML-структуру страницы категории, включая заголовок и сетку продуктов.
   - Для каждого продукта в списке генерирует HTML-код карточки продукта с изображением, заголовком, ценой, категорией и ссылкой для покупки.
   - Использует метод `save_text_file` для сохранения HTML-кода в файл.

   **Примеры**:
   ```python
   from types import SimpleNamespace
   from pathlib import Path
   product_data1 = SimpleNamespace(
       product_id='12345',
       product_title='Test Product 1',
       local_image_path='images/test1.jpg',
       target_sale_price='10.00',
       target_sale_price_currency='USD',
       target_original_price='12.00',
       target_original_price_currency='USD',
       second_level_category_name='Test Category',
       promotion_link='https://example.com/1'
   )
   product_data2 = SimpleNamespace(
       product_id='67890',
       product_title='Test Product 2',
       local_image_path='images/test2.jpg',
       target_sale_price='20.00',
       target_sale_price_currency='USD',
       target_original_price='24.00',
       target_original_price_currency='USD',
       second_level_category_name='Test Category',
       promotion_link='https://example.com/2'
   )
   products_list = [product_data1, product_data2]
   category_path = 'test_category'
   CategoryHTMLGenerator.set_category_html(products_list, category_path)
   # Будет создан файл test_category/html/index.html с HTML-содержимым категории и списком продуктов
   ```

### `CampaignHTMLGenerator`

**Описание**: Класс для генерации HTML-кода для кампании.

**Методы**:

- `set_campaign_html(categories: list[str], campaign_path: str | Path)`: Создает HTML-файл для кампании, перечисляющий все категории.

   **Назначение**: Генерация HTML-страницы кампании, содержащей список ссылок на категории.

   **Параметры**:
   - `categories` (`list[str]`): Список названий категорий.
   - `campaign_path` (`str` | `Path`): Путь к каталогу, в котором нужно сохранить HTML-файл.

   **Возвращает**:
   - `None`: Функция ничего не возвращает, но создает HTML-файл.

   **Как работает функция**:
   - Функция принимает список названий категорий и путь к кампании.
   - Формирует путь к HTML-файлу кампании (`index.html`).
   - Создает HTML-структуру страницы кампании, включая заголовок и список категорий в виде ссылок.
   - Для каждой категории в списке генерирует HTML-код элемента списка со ссылкой на страницу категории.
   - Использует метод `save_text_file` для сохранения HTML-кода в файл.

   **Примеры**:
   ```python
   from pathlib import Path
   categories = ['category1', 'category2', 'category3']
   campaign_path = 'test_campaign'
   CampaignHTMLGenerator.set_campaign_html(categories, campaign_path)
   # Будет создан файл test_campaign/index.html с HTML-содержимым кампании и списком категорий
   ```