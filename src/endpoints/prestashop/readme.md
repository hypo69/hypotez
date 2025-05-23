# Модуль `prestashop` (`src/endpoints/prestashop/`)

## Назначение

Модуль `prestashop` предоставляет набор инструментов на Python для взаимодействия с **PrestaShop Web Service API**. Он инкапсулирует логику отправки запросов, обработки ответов, аутентификации и форматирования данных, позволяя разработчикам программно управлять различными ресурсами магазина PrestaShop, с особым акцентом на **товарах**.

Ключевые задачи, решаемые модулем:

1.  **Унифицированное API-взаимодействие:** Предоставление удобного интерфейса для выполнения стандартных CRUD-операций (Create, Read, Update, Delete) и поиска по различным ресурсам PrestaShop (товары, категории, налоги, изображения и т.д.).
2.  **Управление товарами:** Специализированные функции для создания и получения данных о товарах, включая обработку мультиязычных полей и связей (категории, характеристики, изображения).
3.  **Структурирование данных:** Использование класса `ProductFields` как стандартизированного контейнера для данных товара, который затем преобразуется в формат, понятный PrestaShop API.
4.  **Обработка данных и форматов:** Поддержка работы с форматами XML и JSON, включая автоматическое преобразование между словарями Python и XML при необходимости.
5.  **Загрузка изображений:** Функции для загрузки изображений товаров как из локальных файлов, так и по URL.
6.  **Конфигурация и гибкость:** Возможность легкого переключения между различными инстансами PrestaShop (dev, prod) и источниками учетных данных (переменные окружения, файлы конфигурации).

Модуль тесно интегрирован с другими частями системы: он принимает данные, подготовленные модулем `graber` в виде объекта `ProductFields`, и использует базовый класс `PrestaShop` для фактической отправки запросов к API.

## Ключевые компоненты и возможности

*   **`PrestaShop` (`api.py`):**
    *   **Базовый класс** для взаимодействия с любым ресурсом PrestaShop API.
    *   Использует `requests.Session` для управления HTTP-соединениями и аутентификации (Basic Auth с API-ключом).
    *   Метод `_exec`: Центральный метод для выполнения HTTP-запросов (GET, POST, PUT, DELETE) к API с обработкой параметров (фильтры, сортировка, лимиты, формат вывода, язык и т.д.).
    *   Методы-обертки для стандартных операций: `create`, `read`, `write`, `unlink`, `search`.
    *   Метод `ping`: Проверка доступности API.
    *   Метод `get_schema`: Получение схемы данных (полей и их типов) для любого ресурса API (полезно для понимания структуры).
    *   Метод `create_binary`: Загрузка бинарных данных (например, изображений) через POST-запрос (`multipart/form-data`).
    *   Метод `upload_image_from_url`: Утилита для скачивания изображения по URL и последующей его загрузки через `create_binary`.
    *   Обработка ответов: `_check_response` (проверка HTTP-статуса) и `_parse_response` (преобразование JSON/XML ответа в словарь Python).
    *   Обработка ошибок: `_parse_response_error` (логирование ошибок API).
    *   Поддержка конфигурации через вложенный класс `Config`.
*   **`ProductFields` (`product_fields.py`):**
    *   **Data Transfer Object (DTO)** / **Контейнер данных** для товара.
    *   Представляет структуру данных товара, максимально приближенную к требованиям PrestaShop API.
    *   Инициализируется значениями по умолчанию из `product_fields_default_values.json` (через `_payload`).
    *   Предоставляет свойства (`@property`) для доступа и установки значений полей товара (из `fields_list.txt`). Сеттеры включают базовую нормализацию данных.
    *   Поддерживает **мультиязычные поля** (name, description, etc.) через метод `_set_multilang_value`, который хранит данные для разных языков.
    *   Управляет **связями (`associations`)**: Содержит методы для добавления (`..._append`) и очистки (`..._clear`) связей с категориями, изображениями, характеристиками, комбинациями, тегами и т.д.
    *   Метод **`to_dict()`**: Ключевой метод, преобразующий объект `ProductFields` в словарь Python, готовый для отправки в API. Он фильтрует пустые значения, конвертирует все значения в строки и правильно форматирует мультиязычные поля и связи.
*   **`PrestaProduct` (`product.py`):**
    *   **Класс, специализирующийся на ресурсе `products`** API. Наследуется от `PrestaShop`.
    *   Метод **`add_new_product(f: ProductFields)`**:
        *   Принимает заполненный объект `ProductFields`.
        *   Вызывает `_add_parent_categories` для автоматического добавления всех родительских категорий товара.
        *   Вызывает `f.to_dict()` для получения словаря данных.
        *   Преобразует словарь в **XML** (`dict2xml`) для отправки (PrestaShop API часто требует XML для создания/обновления сложных ресурсов вроде товаров).
        *   Вызывает унаследованный метод `self.create('products', ...)` для отправки POST-запроса.
        *   Обрабатывает ответ, и в случае успеха пытается загрузить изображение товара (используя `f.local_image_path` или `f.default_image_url`).
        *   Возвращает данные о добавленном товаре или пустой словарь при ошибке.
    *   Метод `get_product(id_product)`: Получает данные конкретного товара по ID.
    *   Метод `get_product_schema`: Получает схему ресурса `products`.
    *   Метод `get_parent_category`: Вспомогательный метод для получения родительской категории.
    *   Метод `_add_parent_categories`: Внутренняя логика для построения дерева категорий.

## Структура модуля

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
