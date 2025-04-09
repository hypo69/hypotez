# Модуль: `affiliated_products_generator.py`

## Обзор

Модуль `affiliated_products_generator.py` содержит класс `AliAffiliatedProducts`, который отвечает за сбор полных данных о продуктах из AliExpress Affiliate API. Он расширяет класс `AliApi` для обработки URL или идентификаторов продуктов и извлечения подробной информации об партнерских продуктах, включая сохранение изображений, видео и данных JSON.

## Подробней

Этот код используется для автоматизации процесса получения информации о партнерских продуктах из AliExpress, что позволяет создавать рекламные кампании и каталоги товаров. Он обеспечивает возможность извлекать необходимые данные, такие как изображения, видео и описания, и сохранять их локально для дальнейшего использования.

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс для сбора полных данных о продуктах из URL или идентификаторов продуктов с использованием Aliexpress Affiliate API.

**Наследует**:
- `AliApi`: Наследует методы для работы с Aliexpress API.

**Атрибуты**:
- `campaign_name` (str): Название рекламной кампании.
- `campaign_category` (Optional[str]): Категория для кампании (по умолчанию `None`).
- `campaign_path` (Path): Путь к каталогу, где хранятся материалы кампании.
- `language` (str): Язык для кампании (по умолчанию `'EN'`).
- `currency` (str): Валюта для кампании (по умолчанию `'USD'`).
- `locale` (str): Локаль кампании, формируется из языка и валюты (например, `'EN_USD'`).

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AliAffiliatedProducts`.
- `process_affiliate_products`: Обрабатывает список URL и возвращает список продуктов с партнерскими ссылками и сохраненными изображениями.
- `delete_product`: Удаляет продукт, у которого нет партнерской ссылки.

**Принцип работы**:
Класс инициализируется с параметрами рекламной кампании, такими как название, категория, язык и валюта. Он использует API AliExpress для получения информации о продуктах по их URL или ID, сохраняет изображения и видео, а также генерирует партнерские ссылки. Все данные сохраняются в структурированном формате в каталоге кампании.

## Методы класса

### `__init__`

```python
def __init__(self,
             campaign_name: str,
             campaign_category: Optional[str] = None,
             language: str = 'EN',
             currency: str = 'USD',
             *args, **kwargs):
    """
    @param campaign_name `str`: Name of the advertising campaign. The directory with the prepared material is taken by name.
    @param campaign_category `Optional[str]`: Category for the campaign (default None).
    @param language `str`: Language for the campaign (default 'EN').
    @param currency `str`: Currency for the campaign (default 'USD').
    @param tracking_id `str`: Tracking ID for Aliexpress API.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `AliAffiliatedProducts`.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `campaign_category` (Optional[str], optional): Категория для кампании (по умолчанию `None`).
- `language` (str, optional): Язык для кампании (по умолчанию `'EN'`).
- `currency` (str, optional): Валюта для кампании (по умолчанию `'USD'`).
- `*args`: Произвольные позиционные аргументы, которые передаются в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, которые передаются в конструктор родительского класса.

**Как работает функция**:
- Вызывает конструктор родительского класса `AliApi` с указанными языком и валютой.
- Устанавливает значения атрибутов экземпляра на основе переданных аргументов.
- Формирует локаль (например, `'EN_USD'`) на основе языка и валюты.
- Определяет путь к каталогу кампании, используя атрибуты `campaign_name` и `campaign_category`.

**Примеры**:

```python
parser = AliAffiliatedProducts(
    campaign_name='my_campaign',
    campaign_category='electronics',
    language='RU',
    currency='RUB'
)
```

### `process_affiliate_products`

```python
def process_affiliate_products(self, prod_urls: List[str]) -> List[SimpleNamespace]:
    """
    Processes a list of URLs and returns a list of products with affiliate links and saved images.

    :param prod_urls: List of product URLs or IDs.
    :return: List of processed products.
    """
    ...
```

**Назначение**: Обрабатывает список URL или ID продуктов для получения партнерских ссылок, сохранения изображений и видео, а также сохранения деталей продукта.

**Параметры**:
- `prod_urls` (List[str]): Список URL или ID продуктов.

**Возвращает**:
- `List[SimpleNamespace]`: Список объектов `SimpleNamespace`, представляющих обработанные продукты.

**Как работает функция**:

1. **Инициализация переменных**:
   - `_promotion_links`: список для хранения партнерских ссылок.
   - `_prod_urls`: список для хранения URL продуктов.
2. **Подготовка URL**:
   - Функция `ensure_https` преобразует URL в HTTPS.
3. **Получение партнерских ссылок**:
   - Для каждого URL продукта вызывается метод `get_affiliate_links` родительского класса `AliApi`.
   - Если партнерская ссылка найдена, она добавляется в список `_promotion_links`, а URL продукта - в список `_prod_urls`.
4. **Получение деталей продукта**:
   - Вызывается метод `retrieve_product_details` для получения подробной информации о продуктах.
5. **Обработка каждого продукта**:
   - Для каждого продукта и соответствующей партнерской ссылки выполняется следующая обработка:
     - Если `promotion_link` отсутствует, пытается извлечь `aff_short_key` из URL и сформировать короткую ссылку.
     - Если `aff_short_key` отсутствует, продукт удаляется с помощью `delete_product`.
     - Сохраняет изображение продукта локально с использованием `save_png_from_url`.
     - Сохраняет видео продукта локально с использованием `save_video_from_url`.
     - Сохраняет информацию о продукте в формате JSON с использованием `j_dumps`.
6. **Логирование и возврат**:
   - Логирует информацию об успешной обработке продукта.
   - Возвращает список обработанных продуктов.

**Внутренние функции**:
- Отсутствуют

**Примеры**:

```python
prod_urls = [
    'https://www.aliexpress.com/item/123.html',
    '456'
]
parser = AliAffiliatedProducts(
    campaign_name='my_campaign',
    campaign_category='electronics'
)
products = parser.process_affiliate_products(prod_urls)
if products:
    print(f'Processed {len(products)} products')
```

### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Delete a product that does not have an affiliate link"""
    ...
```

**Назначение**: Удаляет продукт, у которого отсутствует партнерская ссылка.

**Параметры**:
- `product_id` (str): ID продукта для удаления.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли логировать информацию об исключении (по умолчанию `False`).

**Как работает функция**:

1. **Извлечение ID продукта**:
   - Использует функцию `extract_prod_ids` для извлечения ID продукта из переданного значения.
2. **Определение путей к файлам**:
   - Формирует пути к файлам `sources.txt` и `_sources.txt`, в которых может содержаться информация о продукте.
3. **Чтение списка продуктов**:
   - Читает содержимое файла `sources.txt` с использованием `read_text_file`.
4. **Удаление продукта из списка**:
   - Если файл `sources.txt` существует, функция пытается найти и удалить запись о продукте из этого списка.
   - Если продукт найден и удален, обновленный список сохраняется в файл `prepared_product_path`.
5. **Переименование файла продукта**:
   - Если файл `sources.txt` не существует, функция пытается переименовать файл продукта, добавив к его имени суффикс `_`.
6. **Логирование**:
   - Логирует информацию об успешном переименовании файла или возникших ошибках.

**Внутренние функции**:
- Отсутствуют

**Примеры**:

```python
parser = AliAffiliatedProducts(
    campaign_name='my_campaign',
    campaign_category='electronics'
)
parser.delete_product('123')
```

## Параметры класса

- `campaign_name` (str): Название рекламной кампании, используется для организации файлов и каталогов.
- `campaign_category` (Optional[str]): Категория кампании, позволяет дополнительно структурировать файлы кампании.
- `language` (str): Язык, используемый для получения информации о продуктах и создания локализованных материалов.
- `currency` (str): Валюта, используемая для отображения цен продуктов.

**Примеры**:

```python
parser = AliAffiliatedProducts(
    campaign_name='summer_sale',
    campaign_category='clothing',
    language='EN',
    currency='USD'
)
```