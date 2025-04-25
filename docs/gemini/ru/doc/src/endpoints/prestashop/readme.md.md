# Модуль PrestaShop

## Обзор

Модуль `prestashop` (`src/endpoints/prestashop/`) - это библиотека Python, предоставляющая набор инструментов для взаимодействия с **API сервиса PrestaShop**. Он обеспечивает унифицированный интерфейс для отправки запросов, обработки ответов, аутентификации и формата данных, упрощая программное управление различными ресурсами онлайн-магазина PrestaShop, с особым акцентом на **товарах**.

## Ключевые задачи

Модуль решает следующие ключевые задачи:

1.  **Унифицированное API-взаимодействие**: Предоставляет удобный интерфейс для выполнения стандартных CRUD-операций (Create, Read, Update, Delete) и поиска по различным ресурсам PrestaShop (товары, категории, налоги, изображения и т.д.).
2.  **Управление товарами**: Специализированные функции для создания и получения данных о товарах, включая обработку мультиязычных полей и связей (категории, характеристики, изображения).
3.  **Структурирование данных**: Использование класса `ProductFields` как стандартизированного контейнера для данных товара, который затем преобразуется в формат, понятный PrestaShop API.
4.  **Обработка данных и форматов**: Поддержка работы с форматами XML и JSON, включая автоматическое преобразование между словарями Python и XML при необходимости.
5.  **Загрузка изображений**: Функции для загрузки изображений товаров как из локальных файлов, так и по URL.
6.  **Конфигурация и гибкость**: Возможность легкого переключения между различными инстансами PrestaShop (dev, prod) и источниками учетных данных (переменные окружения, файлы конфигурации).

## Структура

Модуль состоит из следующих файлов:

```
src/endpoints/prestashop/
├── api.py                 # Базовый класс PrestaShop для API
├── product.py             # Класс PrestaProduct для работы с товарами
├── product_fields.py      # Класс ProductFields (DTO для товара)
├── category.py            # (Предположительно) Класс для работы с категориями
├── utils/                 # Вспомогательные утилиты
│   ├── dict2xml.py        # Конвертер Python dict -> XML
│   └── xml2dict.py        # Конвертер XML -> Python dict
├── product_fields/
│   ├── fields_list.txt    # Список всех полей товара
│   └── product_fields_default_values.json # Значения по умолчанию для полей
└── ...                    # Другие возможные модули (для заказов, клиентов и т.д.)
```

## Зависимости

*   `requests`: Для выполнения HTTP-запросов.
*   `httpx`: (Импортирован `Response`, но не используется активно в показанном коде, возможно, зависимость `requests` достаточна).
*   Стандартные библиотеки Python (`os`, `json`, `xml.etree.ElementTree`, `pathlib`, `typing`, etc.).

## Конфигурация

Конфигурация API (адрес магазина и ключ) задается через класс `Config` внутри `api.py` и `product.py`.

*   **`MODE`**: Определяет, какой набор учетных данных использовать ('dev', 'dev8', 'prod').
*   **`USE_ENV`**: Если `True`, ключи `API_DOMAIN` и `API_KEY` берутся из переменных окружения `HOST` и `API_KEY`.
*   **`API_DOMAIN`**, **`API_KEY`**: Если `USE_ENV` равно `False`, эти значения берутся из объекта `gs.credentials.presta.client...` в зависимости от выбранного `MODE`.
*   **`POST_FORMAT`**: Определяет формат данных для отправки (в `api.py`, но `PrestaProduct` всегда использует XML для создания товара).

## Использование

### 1. Инициализация

```python
from src.endpoints.prestashop.api import PrestaShop
from src.endpoints.prestashop.product import PrestaProduct

# Инициализация базового API клиента (если нужно работать с разными ресурсами)
# Учетные данные будут взяты из Config на основе MODE
api = PrestaShop(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

# Инициализация клиента для работы с товарами
pp = PrestaProduct(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

# Проверка соединения
if api.ping():
    print("API доступно!")
```

### 2. Работа с ProductFields

```python
from src.endpoints.prestashop.product_fields import ProductFields

# Создаем объект ProductFields для языка с ID=2 (Иврит)
pf = ProductFields(id_lang=2)

# Заполняем поля (многие уже имеют значения по умолчанию)
pf.id_supplier = 10 # ID поставщика
pf.reference = "TEST-SKU-123" # Артикул
pf.price = 199.99
pf.name = "מוצר בדיקה" # Название на иврите
pf.description = "<p>תיאור מוצר כאן.</p>" # Описание на иврите
pf.active = 1
pf.id_category_default = 5 # Главная категория

# Добавляем связи
pf.additional_category_append(5) # Добавляем главную категорию в связи
pf.additional_category_append(8) # Добавляем еще одну категорию

# Указываем путь к локальному изображению (если оно было скачано грабером)
pf.local_image_path = "/path/to/downloaded/image.png"

# Получаем словарь для отправки в API
api_data_dict = pf.to_dict()
```

### 3. Добавление товара

```python
# Используем экземпляр PrestaProduct (pp) и ProductFields (pf) из предыдущих шагов

try:
    added_product_info = pp.add_new_product(pf)
    if added_product_info:
        print(f"Товар успешно добавлен! ID: {added_product_info.id}")
        # Здесь added_product_info - это SimpleNamespace с ответом от API
    else:
        print("Ошибка при добавлении товара.")
except Exception as e:
    print(f"Произошла ошибка: {e}")

```

### 4. Получение данных товара

```python
try:
    product_id_to_get = 123 # ID товара, который нужно получить
    product_data = pp.get_product(product_id_to_get)

    if product_data and 'products' in product_data:
        print("Данные товара:")
        # print(product_data['products'][0]) # Печать словаря товара
    else:
        print(f"Товар с ID {product_id_to_get} не найден или произошла ошибка.")
except Exception as e:
    print(f"Произошла ошибка при получении товара: {e}")
```

### 5. Получение схемы ресурса

```python
# Получить пустую схему для товаров
blank_schema = pp.get_product_schema(schema='blank')
# print(blank_schema)

# Получить полную схему для категорий
full_category_schema = api.get_schema(resource='categories')
# print(full_category_schema)
```

## Формат данных и XML

Хотя API PrestaShop поддерживает JSON для многих операций (особенно GET), для создания и обновления сложных ресурсов, таких как товары (`products`), часто **требуется формат XML**.

*   Класс `ProductFields` методом `to_dict()` создает **словарь Python**.
*   В методе `PrestaProduct.add_new_product` этот словарь **преобразуется в XML** с помощью утилиты `dict2xml`.
*   Именно **XML отправляется** в API при создании товара (`POST /api/products`).
*   Ответы от API (включая ошибки) могут приходить как в JSON, так и в XML. Метод `_parse_response` пытается сначала разобрать ответ как JSON, а затем (если не удалось или формат XML) использует `xml2dict` для преобразования в словарь.

## Обработка ошибок

*   Базовый класс `PrestaShop` проверяет HTTP статус ответа (`_check_response`).
*   При статусах, отличных от 200/201, вызывается `_parse_response_error`, который пытается извлечь код и сообщение об ошибке из тела ответа (JSON или XML) и логирует их.
*   Собственные исключения (`PrestaShopAuthenticationError`, `PrestaShopException`) определены, но в показанном коде активно не генерируются (логируются через `logger.error`). Основная обработка ошибок заключается в логировании и возврате `None`, `False` или `{}` из методов при неудаче.

## Классы

### `PrestaShop` (`api.py`)

**Описание**: Базовый класс для взаимодействия с любым ресурсом PrestaShop API.

**Наследует**: 

**Аттрибуты**:

**Методы**:

*   `_exec`: Центральный метод для выполнения HTTP-запросов (GET, POST, PUT, DELETE) к API с обработкой параметров (фильтры, сортировка, лимиты, формат вывода, язык и т.д.).
*   `create`: Метод-обертка для создания нового ресурса.
*   `read`: Метод-обертка для получения данных о ресурсе.
*   `write`: Метод-обертка для обновления ресурса.
*   `unlink`: Метод-обертка для удаления ресурса.
*   `search`: Метод-обертка для поиска ресурсов.
*   `ping`: Проверка доступности API.
*   `get_schema`: Получение схемы данных (полей и их типов) для любого ресурса API (полезно для понимания структуры).
*   `create_binary`: Загрузка бинарных данных (например, изображений) через POST-запрос (`multipart/form-data`).
*   `upload_image_from_url`: Утилита для скачивания изображения по URL и последующей его загрузки через `create_binary`.
*   `_check_response`: Проверка HTTP-статуса ответа.
*   `_parse_response`: Преобразование JSON/XML ответа в словарь Python.
*   `_parse_response_error`: Логирование ошибок API.

### `ProductFields` (`product_fields.py`)

**Описание**: Data Transfer Object (DTO) / Контейнер данных для товара. Представляет структуру данных товара, максимально приближенную к требованиям PrestaShop API.

**Наследует**: 

**Аттрибуты**:

**Методы**:

*   `_payload`: Инициализирует объект значениями по умолчанию из `product_fields_default_values.json`.
*   `_set_multilang_value`: Хранит мультиязычные данные для разных языков.
*   `..._append`: Методы для добавления связей с категориями, изображениями, характеристиками, комбинациями, тегами и т.д.
*   `..._clear`: Методы для очистки связей с категориями, изображениями, характеристиками, комбинациями, тегами и т.д.
*   `to_dict()`: Преобразует объект `ProductFields` в словарь Python, готовый для отправки в API.

### `PrestaProduct` (`product.py`)

**Описание**: Класс, специализирующийся на ресурсе `products` API. Наследуется от `PrestaShop`.

**Наследует**: 

**Аттрибуты**:

**Методы**:

*   `add_new_product(f: ProductFields)`:
    *   Принимает заполненный объект `ProductFields`.
    *   Вызывает `_add_parent_categories` для автоматического добавления всех родительских категорий товара.
    *   Вызывает `f.to_dict()` для получения словаря данных.
    *   Преобразует словарь в **XML** (`dict2xml`) для отправки (PrestaShop API часто требует XML для создания/обновления сложных ресурсов вроде товаров).
    *   Вызывает унаследованный метод `self.create('products', ...)` для отправки POST-запроса.
    *   Обрабатывает ответ, и в случае успеха пытается загрузить изображение товара (используя `f.local_image_path` или `f.default_image_url`).
    *   Возвращает данные о добавленном товаре или пустой словарь при ошибке.
*   `get_product(id_product)`: Получает данные конкретного товара по ID.
*   `get_product_schema`: Получает схему ресурса `products`.
*   `get_parent_category`: Вспомогательный метод для получения родительской категории.
*   `_add_parent_categories`: Внутренняя логика для построения дерева категорий.


## Примеры

### Создание товара

```python
# Создаем объект ProductFields
pf = ProductFields(id_lang=2)
pf.id_supplier = 1
pf.reference = "TEST-SKU"
pf.price = 100
pf.name = "Тестовый товар"
pf.description = "<p>Описание тестового товара</p>"
pf.active = 1
pf.id_category_default = 5
pf.additional_category_append(8)
pf.local_image_path = "/path/to/image.png"

# Добавляем товар в PrestaShop
try:
    added_product_info = pp.add_new_product(pf)
    if added_product_info:
        print(f"Товар успешно добавлен! ID: {added_product_info.id}")
    else:
        print("Ошибка при добавлении товара.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
```

### Получение данных товара

```python
try:
    product_data = pp.get_product(123)
    if product_data:
        print(product_data)
    else:
        print("Товар не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
```

### Получение схемы ресурса

```python
try:
    schema = pp.get_product_schema(schema='blank')
    print(schema)
except Exception as e:
    print(f"Произошла ошибка: {e}")
```

## Внутренние функции

### `PrestaShop._exec`

**Описание**: Выполняет HTTP-запрос к API PrestaShop.

**Параметры**:

*   `method`: HTTP-метод (GET, POST, PUT, DELETE).
*   `resource`: Ресурс API (например, 'products', 'categories').
*   `data`: Данные для отправки в запросе.
*   `params`: Дополнительные параметры запроса (фильтры, сортировка, лимиты, формат вывода, язык и т.д.).
*   `files`: Файлы для загрузки (multipart/form-data).

**Возвращает**:

*   Объект `Response` (httpx) с ответом от API.

**Вызывает исключения**:

*   `PrestaShopAuthenticationError`: В случае ошибки аутентификации.
*   `PrestaShopException`: В случае других ошибок API.

**Как работает**:

*   Формирует URL запроса на основе `API_DOMAIN` и `resource`.
*   Создает объект `Request` с заданными параметрами.
*   Выполняет запрос к API через `self.session.request`.
*   Возвращает объект `Response` с ответом от API.

### `PrestaProduct._add_parent_categories`

**Описание**: Рекурсивно добавляет родительские категории для товара в API PrestaShop.

**Параметры**:

*   `id_category`: ID категории товара.

**Возвращает**:

*   `None`.

**Как работает**:

*   Получает информацию о текущей категории (используя `self.api.read('categories', id_category)`).
*   Получает ID родительской категории.
*   Если ID родительской категории существует, рекурсивно вызывает `_add_parent_categories` для родительской категории.
*   Добавляет текущую категорию в API PrestaShop (используя `self.api.create('categories', ...)`).

## Дополнительные замечания

*   Модуль `prestashop` интегрирован с другими частями системы, такими как модуль `graber`, который предоставляет данные о товарах в виде объекта `ProductFields`.
*   Модуль использует класс `Driver` для взаимодействия с браузером (Selenium) при необходимости (например, для загрузки изображений).
*   Для обработки XML используется библиотека `xml2dict`.

```