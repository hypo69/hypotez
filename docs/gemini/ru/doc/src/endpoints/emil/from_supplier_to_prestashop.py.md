# Модуль исполнения сценария `emil-design.com`

## Обзор

Модуль `src/endpoints/emil/scenarios/from_supplier_to_prestashop.py`  предоставляет функциональность для извлечения, разбора и обработки данных о продуктах от различных поставщиков. Модуль обрабатывает подготовку данных, обработку с помощью AI и интеграцию с Prestashop для публикации продуктов.

## Подробней 

Этот модуль используется для автоматизации процесса импорта продуктов с сайта `emil-design.com` в Prestashop. Он включает в себя несколько этапов:

1. **Извлечение данных о продуктах**: Сбор данных о продуктах с различных сайтов поставщиков или из файла JSON.
2. **Обработка данных AI**: Применение моделей AI (например, Google Gemini) для обработки данных о продуктах.
3. **Сохранение данных**: Сохранение обработанных данных о продуктах в файлах JSON.
4. **Публикация в Prestashop**: Добавление обработанных продуктов в Prestashop с помощью API.

## Классы

### `SupplierToPrestashopProvider`

**Описание**: Класс `SupplierToPrestashopProvider` предоставляет функциональность для извлечения, разбора и сохранения данных о продуктах поставщиков. Данные могут быть получены как из сторонних сайтов, так из файла JSON.

**Наследует**: 
    - Данный класс не наследует других классов.

**Атрибуты**:
    - `driver` (Driver): Экземпляр Selenium WebDriver.
    - `export_path` (Path): Путь для экспорта данных.
    - `products_list` (List[dict]): Список обработанных данных о продуктах.
    - `mexiron_name` (str): Имя Мехирона (товара)
    - `price` (float): Цена товара
    - `timestamp` (str): Текущая дата и время 
    - `model` (GoogleGenerativeAi): Модель AI (Google Gemini) 
    - `config` (SimpleNamespace): Конфигурационные настройки
    - `local_images_path` (Path): Путь для локального хранения изображений
    - `lang` (str): Язык (например, "he" - иврит)
    - `gemini_api` (str): API-ключ для Google Gemini
    - `presta_api` (str): API-ключ для Prestashop
    - `presta_url` (str): URL-адрес магазина Prestashop

**Методы**:

- `__init__(self, lang: str, gemini_api: str, presta_api: str, presta_url: str, driver: Optional[Driver] = None)`:
    - **Назначение**: Инициализирует класс `SupplierToPrestashopProvider` с необходимыми компонентами.
    - **Параметры**:
        - `lang` (str): Язык.
        - `gemini_api` (str): API-ключ для Google Gemini.
        - `presta_api` (str): API-ключ для Prestashop.
        - `presta_url` (str): URL-адрес магазина Prestashop.
        - `driver` (Driver, optional): Экземпляр Selenium WebDriver. По умолчанию `None`.

- `initialise_ai_model(self)`:
    - **Назначение**: Инициализация модели Gemini.
    - **Возвращает**:
        - GoogleGenerativeAi: Экземпляр модели Google Gemini.

- `async def process_graber(self, urls: list[str], price: Optional[str] = '', mexiron_name: Optional[str] = '', scenarios: dict | list[dict,dict] = None)`:
    - **Назначение**: Выполняет сценарий: парсит продукты, обрабатывает их с помощью AI и сохраняет данные.
    - **Параметры**:
        - `urls` (list[str]): Список URL-адресов страниц продуктов.
        - `price` (Optional[str]): Цена.
        - `mexiron_name` (Optional[str]): Имя Мехирона.
        - `scenarios` (Optional[dict]): Сценарий исполнения, который находится в директории `src.suppliers.suppliers_list.<supplier>.sceanarios`.
    - **Возвращает**:
        - bool: `True`, если сценарий выполнен успешно, `False` в противном случае.

- `async def process_scenarios(self, suppliers_prefixes: Optional[str] = '')`:
    - **Назначение**: Обработка сценариев для получения данных о товарах.
    - **Параметры**:
        - `suppliers_prefixes` (Optional[str]): Префиксы поставщиков.
    - **Возвращает**:
        - bool: `True` если сценарий выполнен успешно, `False` в противном случае.

- `async def save_product_data(self, product_data: dict)`:
    - **Назначение**: Сохраняет данные об отдельном продукте в файл.
    - **Параметры**:
        - `product_data` (dict): Форматированные данные о продукте.
    - **Возвращает**:
        - bool: `True`, если данные сохранены успешно, `False` в противном случае.

- `async def process_llm(self, products_list: List[str], lang: str, attempts: int = 3)`:
    - **Назначение**: Обрабатывает список продуктов с помощью модели AI.
    - **Параметры**:
        - `products_list` (List[str]): Список данных о продуктах в виде строки.
        - `lang` (str): Язык.
        - `attempts` (int): Количество попыток повторной обработки в случае ошибки.
    - **Возвращает**:
        - tuple: Обработанный ответ в форматах `ru` и `he`.
        - bool: `False`, если не удалось получить действительный ответ после повторных попыток.

- `async def save_in_prestashop(self, products_list: ProductFields | list[ProductFields])`:
    - **Назначение**: Функция, которая сохраняет товары в Prestashop `emil-design.com`.
    - **Параметры**:
        - `products_list` (ProductFields | list[ProductFields]): Данные о товарах в формате `ProductFields`.

- `async def post_facebook(self, mexiron: SimpleNamespace)`:
    - **Назначение**: Функция исполняет сценарий рекламного модуля `facvebook`.
    - **Параметры**:
        - `mexiron` (SimpleNamespace): Данные о Мехироне.

- `async def create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path)`:
    - **Назначение**: Функция отправляет задание на создание Мехирона в форматах `html` и `pdf`.
    - **Параметры**:
        - `data` (dict): Данные о Мехироне.
        - `lang` (str): Язык.
        - `html_file` (Path): Путь к файлу `html`.
        - `pdf_file` (Path): Путь к файлу `pdf`.

## Внутренние функции

- `async def convert_product_fields(self, f: dict)`:
    - **Назначение**: Преобразует данные о продукте в нужный формат.
    - **Параметры**:
        - `f` (dict): Данные о продукте.
    - **Возвращает**:
        - dict: Преобразованные данные о продукте.

## Функции

### `async def upload_redacted_images_from_emil()`:
    - **Назначение**: Загрузка отредактированных изображений продуктов из `emil`. 
    - **Параметры**:
        -  `lang` (str): Язык.
    - **Возвращает**:
        - bool: `True` если задача выполнена успешно, `False` в противном случае.

### `async def main()`:
    - **Назначение**: Основная функция, которая запускает процесс импорта продуктов.
    - **Параметры**:
        - None.


## Параметры

- `ENDPOINT` (str): Имя точки доступа `emil`.
- `base_dir` (Path): Основная директория для работы с поставщиками.
- `local_images_path` (Path): Путь для хранения изображений продуктов.

## Примеры

```python
# Инициализация класса SupplierToPrestashopProvider
suppier_to_presta = SupplierToPrestashopProvider(
    lang='he', 
    gemini_api='YOUR_GEMINI_API_KEY', 
    presta_api='YOUR_PRESTASHOP_API_KEY', 
    presta_url='YOUR_PRESTASHOP_URL'
)

# Обработка списка URL-адресов продуктов
await suppier_to_presta.process_graber(
    urls=['https://www.emil-design.com/product1', 'https://www.emil-design.com/product2'],
    price='100', 
    mexiron_name='Mexiron Name'
)

# Сохранение данных о товарах в Prestashop
await suppier_to_presta.save_in_prestashop(products_list)

# Публикация информации о товаре в Facebook
await suppier_to_presta.post_facebook(mexiron)
```

## Твое поведение при анализе кода:

- Внутри кода ты можешь встретить выражение между `<` `>`. Например: `<инструкция для модели gemini:Загрузка описаний продуктов в PrestaShop.>, <далее, если есть>. Это заготовки, куда ты вставляешь релевантное значение.
- Всегда смотри системную инструкцию для обработки кода проекта `hypotez`.
- Анализируй расположение файла в проекте. Это поможет понять его назначение и взаимосвязь с другими файлами. Расположение файла ты найдешь в самой превой строке кода, начинающейся с `## \\file /...`.
- Запоминай предоставленный код и анализируй его связь с другими частями проекта.
- В этой инструкции не надо предлагать улучшение кода. Четко следуй пункту 5. **Пример файла** при составлении ответа.