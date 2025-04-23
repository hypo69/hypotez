### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код представляет собой класс `GptGs`, который предназначен для управления Google Sheets в рамках рекламных кампаний. Он позволяет очищать листы, обновлять данные, извлекать информацию о категориях и товарах, а также сохранять изменения обратно в Google Sheets. Класс наследуется от `SpreadSheet` и предназначен для работы с данными AliExpress.

Шаги выполнения
-------------------------
1. **Инициализация класса `GptGs`**:
   - При создании экземпляра класса `GptGs` вызывается конструктор `__init__`, который инициализирует класс `SpreadSheet` с указанным ID Google Sheets.

2. **Очистка содержимого**:
   - Функция `clear` удаляет листы продуктов и очищает данные на листах категорий и кампании.
   - Сначала вызывается функция `delete_products_worksheets` для удаления листов продуктов.
   - Затем, если необходимо, можно раскомментировать код для очистки листов категорий и кампании.

3. **Обновление данных в листе**:
   - Функция `update_chat_worksheet` записывает данные кампании в указанный лист Google Sheets.
   - Извлекаются значения `name`, `title`, `description`, `tags` и `products_count` из объекта `SimpleNamespace` или словаря `data`.
   - Подготавливаются обновления для записи в Google Sheets с использованием API `batch_update`.

4. **Чтение данных кампании**:
   - Функция `get_campaign_worksheet` считывает данные кампании из листа с именем `campaign`.
   - Извлекаются значения `name`, `title`, `language`, `currency` и `description` из ячеек листа.
   - Создается объект `SimpleNamespace` с данными кампании и возвращается.

5. **Запись данных категории**:
   - Функция `set_category_worksheet` записывает данные категории из объекта `SimpleNamespace` в лист с именем `category`.
   - Подготавливаются данные для вертикальной записи в лист Google Sheets.
   - Используется метод `update` для записи данных в указанный диапазон ячеек.

6. **Чтение данных категории**:
   - Функция `get_category_worksheet` считывает данные категории из листа с именем `category`.
   - Извлекаются значения `name`, `title`, `description`, `tags` и `products_count` из ячеек листа.
   - Создается объект `SimpleNamespace` с данными категории и возвращается.

7. **Запись данных категорий**:
   - Функция `set_categories_worksheet` записывает данные из объекта `SimpleNamespace`, содержащего несколько категорий, в лист с именем `categories`.
   - Итерируется по атрибутам объекта `categories`, чтобы извлечь данные каждой категории.
   - Подготавливаются обновления для записи в Google Sheets с использованием API `batch_update`.

8. **Чтение данных категорий**:
   - Функция `get_categories_worksheet` считывает данные категорий из листа с именем `categories`.
   - Извлекаются данные из столбцов A по E, начиная со второй строки.
   - Возвращается список строк с данными категорий.

9. **Запись данных продукта**:
   - Функция `set_product_worksheet` записывает данные продукта в новый лист Google Sheets.
   - Копируется лист `product_template` и переименовывается в соответствии с именем категории.
   - Записываются заголовки столбцов и данные продукта в соответствующие ячейки листа.

10. **Чтение данных продукта**:
    - Функция `get_product_worksheet` считывает данные продукта из листа с именем `products`.
    - Извлекаются значения `id`, `name`, `title`, `description`, `tags` и `price` из ячеек листа.
    - Создается объект `SimpleNamespace` с данными продукта и возвращается.

11. **Запись данных продуктов**:
    - Функция `set_products_worksheet` записывает данные из списка объектов `SimpleNamespace`, содержащих информацию о товарах, в лист Google Sheets с именем категории.
    - Итерируется по списку товаров `products_ns` и формируются обновления для каждой строки.
    - Выполняется пакетное обновление данных в листе с помощью метода `batch_update`.

12. **Удаление листов продуктов**:
    - Функция `delete_products_worksheets` удаляет все листы из Google Sheets, кроме листов `categories`, `product`, `category` и `campaign`.
    - Итерируется по всем листам и удаляются те, которые не входят в список исключений.

13. **Сохранение данных категорий из листа**:
    - Функция `save_categories_from_worksheet` сохраняет данные категорий, отредактированные в Google Sheets, в объект `SimpleNamespace`.
    - Считываются данные из листа `categories` с помощью `get_categories_worksheet`.
    - Создается объект `SimpleNamespace` для каждой категории и устанавливается как атрибут объекта `_categories_ns`.
    - Обновляется атрибут `category` объекта `campaign` и, при необходимости, выполняется обновление кампании.

14. **Сохранение данных кампании из листа**:
    - Функция `save_campaign_from_worksheet` сохраняет данные рекламной кампании, отредактированные в Google Sheets.
    - Сначала сохраняются данные категорий с помощью `save_categories_from_worksheet`.
    - Затем считываются данные кампании из листа с помощью `get_campaign_worksheet`.
    - Обновляется атрибут `category` объекта `campaign` и выполняется обновление кампании.

Пример использования
-------------------------

```python
from types import SimpleNamespace

# Пример использования класса GptGs
gpt_gs = GptGs()

# Очистка содержимого Google Sheets
gpt_gs.clear()

# Создание объекта SimpleNamespace с данными кампании
campaign_data = SimpleNamespace(
    name='Summer Sale',
    title='Summer Sale Campaign',
    language='en',
    currency='USD',
    description='Summer sale campaign description'
)

# Обновление данных в листе кампании
gpt_gs.update_chat_worksheet(campaign_data, conversation_name='campaign')

# Чтение данных кампании из листа
campaign_data = gpt_gs.get_campaign_worksheet()
print(f"Campaign Name: {campaign_data.name}")

# Создание объекта SimpleNamespace с данными категории
category_data = SimpleNamespace(
    name='Shoes',
    title='Shoes Category',
    description='Shoes category description',
    tags=['shoes', 'footwear', 'summer'],
    products_count=100
)

# Запись данных категории в лист
gpt_gs.set_category_worksheet(category_data)

# Чтение данных категории из листа
category_data = gpt_gs.get_category_worksheet()
print(f"Category Name: {category_data.name}")

# Создание объекта SimpleNamespace с данными категорий
categories_data = SimpleNamespace()
setattr(categories_data, 'shoes', category_data)

# Запись данных категорий в лист
gpt_gs.set_categories_worksheet(categories_data)

# Чтение данных категорий из листа
categories_data = gpt_gs.get_categories_worksheet()
print(f"Categories Data: {categories_data}")

# Создание объекта SimpleNamespace с данными продукта
product_data = SimpleNamespace(
    product_id='12345',
    app_sale_price='10.00',
    original_price='20.00',
    sale_price='15.00',
    discount='50%',
    product_main_image_url='http://example.com/image.jpg',
    local_image_path='/path/to/image.jpg',
    product_small_image_urls=['http://example.com/image1.jpg', 'http://example.com/image2.jpg'],
    product_video_url='http://example.com/video.mp4',
    local_video_path='/path/to/video.mp4',
    first_level_category_id='1',
    first_level_category_name='Clothing',
    second_level_category_id='2',
    second_level_category_name='Shoes',
    target_sale_price='12.00',
    target_sale_price_currency='USD',
    target_app_sale_price_currency='USD',
    target_original_price_currency='USD',
    original_price_currency='USD',
    product_title='Example Product',
    evaluate_rate='4.5',
    promotion_link='http://example.com/promotion',
    shop_url='http://example.com/shop',
    shop_id='67890',
    tags=['example', 'product']
)

# Запись данных продукта в лист
gpt_gs.set_product_worksheet(product_data, category_name='Shoes')

# Чтение данных продукта из листа
# product_data = gpt_gs.get_product_worksheet()
# print(f"Product Name: {product_data.name}")

# Удаление листов продуктов
gpt_gs.delete_products_worksheets()
```