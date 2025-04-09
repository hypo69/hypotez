# Модуль `src.endpoints.prestashop.product`

## Обзор

Модуль предназначен для взаимодействия с товарами в PrestaShop. Он предоставляет классы и функции для получения информации о товарах, добавления новых товаров, а также для работы с категориями товаров.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с PrestaShop API для управления товарами. Он включает в себя классы для конфигурации соединения с API, а также для представления и обработки данных о товарах. Модуль использует модуль `src.logger` для логирования событий и ошибок.

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек продукта PrestaShop.

**Принцип работы**:
Класс `Config` содержит статические параметры, необходимые для подключения к API PrestaShop, такие как домен API и ключ API. Он также определяет, использовать ли переменные окружения или параметры из `keepass` для получения этих значений. Класс предоставляет различные режимы работы (`dev`, `dev8`, по умолчанию), каждый из которых использует соответствующие учетные данные для доступа к API.

**Аттрибуты**:
- `USE_ENV` (bool): Указывает, использовать ли переменные окружения для конфигурации API. По умолчанию `False`.
- `MODE` (str): Режим работы (`dev`, `dev8`, или другой). По умолчанию `'dev'`.
- `POST_FORMAT` (str): Формат данных для отправки запросов (XML). По умолчанию `'XML'`.
- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

### `PrestaProduct(PrestaShop)`

**Описание**: Класс для управления товарами в PrestaShop.

**Принцип работы**:
Класс `PrestaProduct` наследует функциональность от класса `PrestaShop` и расширяет её методами для работы с товарами. Он позволяет получать схему товара, добавлять новые товары, а также получать информацию о родительских категориях.

**Наследует**:
- `PrestaShop`: Предоставляет базовую функциональность для взаимодействия с PrestaShop API.

**Методы**:
- `__init__(api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`: Инициализирует объект `PrestaProduct`.
- `get_product_schema(resource_id: Optional[str | int] = None, schema: Optional[str] = 'blank') -> dict`: Возвращает схему ресурса товара из PrestaShop.
- `get_parent_category(id_category: int) -> Optional[int]`: Рекурсивно извлекает родительские категории из PrestaShop для заданной категории.
- `_add_parent_categories(f: ProductFields) -> None`: Вычисляет и добавляет все родительские категории для списка ID категорий в объект `ProductFields`.
- `get_product(id_product: int, **kwards) -> dict`: Возвращает словарь полей товара из магазина PrestaShop.
- `add_new_product(self, f: ProductFields) -> dict`: Добавляет новый продукт в PrestaShop.

## Функции

### `example_add_new_product() -> None`

**Назначение**: Пример добавления товара в PrestaShop.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:

1. **Создание экземпляра класса `PrestaProduct`**:
   - Создается экземпляр класса `PrestaProduct` с использованием ключа API и домена API, взятых из класса `Config`.
     ```python
     p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
     ```

2. **Загрузка примера данных о продукте**:
   - Загружаются пример данных о продукте из JSON-файла. Этот файл имитирует структуру XML, используемую PrestaShop.
     ```python
     example_data: dict = j_loads(
         gs.path.endpoints / 'emil' / '_experiments' / 'product_schema.2191_250319224027026.json'
     )
     ```

3. **Преобразование данных в XML**:
   - Если данные успешно загружены, они преобразуются в XML-формат, требуемый для отправки в PrestaShop API.
     ```python
     presta_product_xml = presta_fields_to_xml(example_data)  # <- XML
     save_xml(presta_product_xml, gs.path.endpoints / 'emil' / '_experiments' / f'{gs.now}_presta_product.xml')
     ```

4. **Определение параметров запроса**:
   - Определяются параметры запроса, включая формат ввода-вывода (`io_format`). В данном примере используется JSON.
     ```python
     kwards: dict = {
         'io_format': 'JSON',
     }
     ```

5. **Выполнение запроса к API PrestaShop**:
   - Выполняется POST-запрос к API PrestaShop для добавления продукта. Используются данные о продукте (в формате JSON или XML) и параметры запроса.
     ```python
     response = p._exec(
         resource='products',
         method='POST',
         data=example_data if kwards['io_format'] == 'JSON' else presta_product_xml,
         **kwards,
     )
     ```

6. **Вывод ответа**:
   - Выводится ответ, полученный от API PrestaShop.
     ```python
     print(response)
     ```

7. **Обработка ошибок**:
   - Если файл с примером данных не существует или имеет неправильный формат, регистрируется ошибка.
     ```python
     if not example_data:
         logger.error(f'Файл не существует или неправильный формат файла')
         ...
         return
     ```

**ASCII Flowchart**:

```
Начало --> Загрузка данных о продукте (example_data)
|
V
Данные загружены? -- Нет --> Ошибка: Файл не существует --> Конец
|
Да
V
Преобразование данных в XML (presta_product_xml)
|
V
Определение параметров запроса (kwards)
|
V
Выполнение POST-запроса к API PrestaShop (response)
|
V
Вывод ответа (print(response)) --> Конец
```

**Примеры**:

```python
example_add_new_product()
```

### `example_get_product(id_product: int, **kwards) -> None`

**Назначение**: Пример получения информации о товаре из PrestaShop.

**Параметры**:
- `id_product` (int): ID товара, информацию о котором нужно получить.
- `**kwards`: Дополнительные параметры запроса.

**Возвращает**:
- `None`

**Как работает функция**:

1. **Создание экземпляра класса `PrestaProduct`**:
   - Создается экземпляр класса `PrestaProduct` с использованием ключа API и домена API, взятых из класса `Config`.
     ```python
     p = PrestaProduct(API_KEY=Config.API_KEY, API_DOMAIN=Config.API_DOMAIN)
     ```

2. **Определение параметров запроса**:
   - Определяются параметры запроса, включая формат данных (`data_format`), уровень детализации (`display`) и схему (`schema`).
     ```python
     kwards: dict = {
         'data_format': 'JSON',
         'display': 'full',
         'schema': 'blank',
     }
     ```

3. **Получение информации о товаре**:
   - Вызывается метод `get_product` для получения информации о товаре с заданным ID.
     ```python
     presta_product = p.get_product(id_product, **kwards)
     ```

4. **Обработка ответа**:
   - Если ответ содержит список, берется первый элемент.
     ```python
     presta_product = presta_product[0] if isinstance(presta_product, list) else presta_product
     ```

5. **Сохранение ответа в файл**:
   - Ответ сохраняется в JSON-файл для отладки и анализа.
     ```python
     j_dumps(
         presta_product, gs.path.endpoints / 'emil' / '_experiments' / f'presta_response_product_{id_product}.json'
     )
     ```

**ASCII Flowchart**:

```
Начало --> Создание экземпляра PrestaProduct (p)
|
V
Определение параметров запроса (kwards)
|
V
Получение информации о товаре (presta_product)
|
V
Обработка ответа (presta_product)
|
V
Сохранение ответа в файл --> Конец
```

**Примеры**:

```python
example_get_product(2191)