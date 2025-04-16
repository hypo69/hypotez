# Модуль исполнения сценария `emil-design.com`

## Обзор

Модуль `src.endpoints.emil.scenarios.from_supplier_to_prestashop.py` предназначен для извлечения, разбора и обработки данных о товарах от различных поставщиков и их интеграции с Prestashop.

## Подробней

Модуль содержит класс `SupplierToPrestashopProvider`, который выполняет извлечение, разбор и сохранение данных о продуктах поставщиков. Данные могут быть получены как с внешних сайтов, так и из файла JSON. Модуль также включает функциональность для AI-обработки данных и интеграции с Prestashop для публикации товаров.

## Классы

### `Config`

**Описание**: Класс конфигурации для настроек товаров PrestaShop.

**Атрибуты**:

*   `ENDPOINT` (str): Конечная точка API (значение: `'emil'`).

### `SupplierToPrestashopProvider`

**Описание**: Класс для обработки данных о товарах поставщиков и их интеграции с Prestashop.

**Атрибуты**:

*   `base_dir` (Path): Базовый каталог для хранения данных поставщиков (значение: путь к `src/suppliers/suppliers_list/emil`).
*   `driver` (Driver): Экземпляр Selenium WebDriver.
*   `export_path` (Path): Путь для экспорта данных.
*   `mexiron_name` (str): Название мехирона.
*   `price` (float): Цена.
*   `timestamp` (str): Временная метка.
*   `products_list` (list): Список обработанных данных о товарах.
*   `model` (GoogleGenerativeAi): Экземпляр модели Google Gemini.
*   `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла.
*   `local_images_path` (Path): Путь для сохранения локальных изображений.
*   `lang` (str): Язык.
*   `gemini_api` (str): Ключ API для Gemini.
*   `presta_api` (str): Ключ API для PrestaShop.
*   `presta_url` (str): URL для PrestaShop.

**Методы**:

*   `__init__(self, lang: str, gemini_api: str, presta_api: str, presta_url: str, driver: Optional[Driver] = None)`: Инициализирует экземпляр класса `SupplierToPrestashopProvider`.
*   `initialise_ai_model(self)`: Инициализирует модель Gemini.
*   `run_scenarios(self, urls: list[str], price: Optional[str] = '', mexiron_name: Optional[str] = '', scenarios: dict | list[dict,dict] = None) -> bool`: Выполняет сценарии: разбирает товары и сохраняет данные.
*   `save_product_data(self, product_data: dict)`: Сохраняет данные о товаре в файл.
*   `process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`: Обрабатывает список товаров с помощью AI-модели.
*   `save_in_prestashop(self, products_list: ProductFields | list[ProductFields]) -> bool`: Сохраняет товары в PrestaShop.
*   `post_facebook(self, mexiron: SimpleNamespace) -> bool`: Выполняет сценарий рекламного модуля `facebook`.
*   `create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path) -> bool`: Отправляет задание на создание мехирона в формате `html` и `pdf`.

## Функции

### `main`

```python
def main(mexiron: str,lang: str) ->bool:
```

**Назначение**: Главная функция для запуска сценария.

**Параметры**:

*   `mexiron` (str): Имя мехирона.
*   `lang` (str): Язык отчета.

**Возвращает**:

*   `bool`: True, если функция исполнена успешно

**Как работает функция**:

1.  Определяет базовый путь к данным мехирона.
2.  Загружает данные из JSON-файла.
3.  Определяет пути к HTML- и PDF-файлам.
4.  Создает экземпляр класса `ReportGenerator`.
5.  Запускает процесс создания отчета.

## Методы класса `SupplierToPrestashopProvider`

### `__init__`

```python
def __init__(self, 
             lang:str, 
             gemini_api: str,
             presta_api: str,
             presta_url: str,
             driver: Optional [Driver] = None,
             ):
```

**Назначение**: Инициализирует экземпляр класса `SupplierToPrestashopProvider`.

**Параметры**:

*   `lang` (str): Язык.
*   `gemini_api` (str): Ключ API для Gemini.
*   `presta_api` (str): Ключ API для PrestaShop.
*   `presta_url` (str): URL для PrestaShop.
*   `driver` (Optional[Driver], optional): Экземпляр веб-драйвера. Defaults to `None`.

**Как работает функция**:

1.  Инициализирует атрибуты класса.
2.  Загружает конфигурацию из JSON-файла.
3.  Инициализирует веб-драйвер и модель Gemini.

### `initialise_ai_model`

```python
def initialise_ai_model(self):
```

**Назначение**: Инициализирует модель Gemini.

**Как работает функция**:

1.  Читает системную инструкцию из файла.
2.  Создает экземпляр класса `GoogleGenerativeAi` с ключом API, системной инструкцией и конфигурацией генерации.

### `run_scenarios`

```python
async def run_scenarios(
    self, 
    urls: list[str],
    price: Optional[str] = '', 
    mexiron_name: Optional[str] = '', 
    scenarios: dict | list[dict,dict] = None,

) -> bool:
```

**Назначение**: Выполняет сценарии: разбирает товары и сохраняет данные.

**Параметры**:

*   `urls` (list[str]): Список URL-адресов товаров.
*   `price` (Optional[str], optional): Цена. Defaults to ''.
*   `mexiron_name` (Optional[str], optional): Имя мехирона. Defaults to ''.
*   `scenarios` (dict | list[dict,dict]], optional): Сценарии для выполнения. Defaults to `None`.

**Возвращает**:

*   `bool`: True, если сценарий выполнен успешно, False в противном случае.

**Как работает функция**:

1.  Итерируется по списку URL-адресов товаров.
2.  Получает грабер для каждого URL-адреса.
3.  Выполняет сценарии грабера.
4.  Конвертирует поля товара с помощью `convert_product_fields`.
5.  Сохраняет данные о товаре с помощью `save_product_data`.

### `save_product_data`

```python
async def save_product_data(self, product_data: dict):
```

**Назначение**: Сохраняет данные о товаре в файл.

**Параметры**:

*   `product_data` (dict): Данные о товаре.

**Возвращает**:

*   `bool`: True, если сохранение прошло успешно, False в противном случае.

**Как работает функция**:

1.  Определяет путь к файлу для сохранения данных.
2.  Сохраняет данные в JSON-файл.

### `process_llm`

```python
async def process_llm(self, products_list: List[str], lang: str,  attempts: int = 3) -> tuple | bool:
```

**Назначение**: Обрабатывает список товаров с помощью AI-модели.

**Параметры**:

*   `products_list` (List[str]): Список данных о товарах.
*   `lang` (str): Язык.
*   `attempts` (int, optional): Количество попыток. Defaults to 3.

**Возвращает**:

*   `tuple | bool`: Обработанные ответы в форматах `ru` и `he`, или False, если не удалось получить ответ после нескольких попыток.

**Как работает функция**:

1.  Читает системную инструкцию для AI-модели из файла.
2.  Отправляет запрос к AI-модели.
3.  Обрабатывает ответ от AI-модели и возвращает результат.

### `save_in_prestashop`

```python
async def save_in_prestashop(self, products_list:ProductFields | list[ProductFields]) -> bool:
```

**Назначение**: Сохраняет товары в PrestaShop.

**Параметры**:

*   `products_list` (ProductFields | list[ProductFields]): Список объектов ProductFields, представляющих товары.

**Как работает функция**:

1.  Проверяет, является ли `products_list` списком. Если нет, преобразует его в список.
2.  Создает экземпляр класса `PrestaProduct` для взаимодействия с API PrestaShop.
3.  Для каждого товара вызывает метод `add_new_product` для добавления товара в PrestaShop.

### `post_facebook`

```python
async def post_facebook(self, mexiron:SimpleNamespace) -> bool:
```

**Назначение**: Выполняет сценарий рекламного модуля `facebook`.

**Параметры**:

*   `mexiron` (SimpleNamespace): данные для публикации в facebook

**Как работает функция**:

*   Вызывает метод `post_message_title`, чтобы отправить название мехирона
*   Вызывает метод `upload_post_media`, чтобы отправить media
*   Вызывает метод `message_publish`, чтобы опубликовать
### `create_report`

```python
async def create_report(self, data: dict, lang:str, html_file: Path, pdf_file: Path) -> bool:
```

**Назначение**: Отправляет задание на создание мехирона в формате `html` и `pdf`.

**Параметры**:

*   `data` (dict): Данные для формирования отчета.
*   `lang` (str): Язык.
*   `html_file` (Path): Путь к файлу для сохранения HTML-версии отчета.
*   `pdf_file` (Path): Путь к файлу для сохранения PDF-версии отчета.

**Как работает функция**:

1.  Создает экземпляр класса `ReportGenerator`.
2.  Вызывает метод `create_report` для создания HTML- и PDF-отчетов.
3.  Отправляет PDF-файл боту.