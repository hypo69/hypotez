# Сценарий создания мехирона для Сергея Казаринова

## Обзор

Этот скрипт является частью директории `hypotez/src/endpoints/kazarinov/scenarios` и предназначен для автоматизации процесса создания "мехирона" для Сергея Казаринова. Скрипт извлекает, парсит и обрабатывает данные о продуктах от различных поставщиков, подготавливает данные, обрабатывает их через ИИ и интегрирует с Facebook для публикации продуктов.

## Подробней

Данный сценарий автоматизирует процесс извлечения, обработки и публикации данных о продуктах. Он предназначен для упрощения и ускорения работы с данными от различных поставщиков, а также для интеграции этих данных с Facebook. Скрипт использует веб-драйвер Selenium, асинхронные операции и модель Google Generative AI для достижения этой цели.

## TOC

- [Класс: `MexironBuilder`](#класс-mexironbuilder)
  - [Метод: `__init__`](#метод-__init__)
  - [Метод: `run_scenario`](#метод-run_scenario)
  - [Метод: `get_graber_by_supplier_url`](#метод-get_graber_by_supplier_url)
  - [Метод: `convert_product_fields`](#метод-convert_product_fields)
  - [Метод: `save_product_data`](#метод-save_product_data)
  - [Метод: `process_ai`](#метод-process_ai)
  - [Метод: `post_facebook`](#метод-post_facebook)
  - [Метод: `create_report`](#метод-create_report)
- [Использование](#использование)
- [Зависимости](#зависимости)
- [Обработка ошибок](#обработка-ошибок)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Классы

### `MexironBuilder`

**Описание**: Класс `MexironBuilder` предназначен для автоматизации процесса создания "мехирона". Он включает методы для извлечения, обработки, сохранения и публикации данных о продуктах.

**Принцип работы**: Класс инициализируется с драйвером Selenium и пользовательским именем мехирона. Он загружает конфигурацию из JSON, устанавливает пути экспорта и системные инструкции, инициализирует модель Google Generative AI и выполняет основной сценарий.

**Атрибуты**:
- `driver`: Экземпляр Selenium WebDriver.
- `export_path`: Путь для экспорта данных.
- `mexiron_name`: Пользовательское имя для процесса мехирона.
- `price`: Цена для обработки.
- `timestamp`: Метка времени для процесса.
- `products_list`: Список обработанных данных о продуктах.
- `model`: Модель Google Generative AI.
- `config`: Конфигурация, загруженная из JSON.

**Методы**:

#### `__init__(self, driver: Driver, mexiron_name: Optional[str] = None)`

```python
def __init__(self, driver: Driver, mexiron_name: Optional[str] = None) -> None:
    """
    Инициализирует класс `MexironBuilder` с необходимыми компонентами.

    Args:
        driver (Driver): Экземпляр Selenium WebDriver.
        mexiron_name (Optional[str], optional): Пользовательское имя для процесса мехирона. По умолчанию `None`.

    Raises:
        Exception: Если драйвер не инициализирован.
    """
    ...
```

**Назначение**: Инициализирует класс `MexironBuilder` с драйвером Selenium и пользовательским именем мехирона.

**Параметры**:
- `driver`: Экземпляр Selenium WebDriver, используемый для автоматизации браузера.
- `mexiron_name`: Пользовательское имя для процесса мехирона (необязательный параметр).

**Как работает функция**:

1. Проверяется, был ли передан драйвер. Если драйвер не передан, выбрасывается исключение.
2. Инициализируются атрибуты класса, такие как драйвер, имя мехирона, список продуктов и другие параметры.
3. Загружается конфигурация из файла `config.json` с использованием функции `j_loads`.
4. Устанавливается путь экспорта данных, используя имя мехирона и временную метку.
5. Загружаются системные инструкции из файла `system_instruction.txt`.
6. Инициализируется модель Google Generative AI для обработки данных.

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")
```

#### `run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool`

```python
def run_scenario(self, system_instruction: Optional[str] = None, price: Optional[str] = None, mexiron_name: Optional[str] = None, urls: Optional[str | List[str]] = None, bot = None) -> bool:
    """
    Выполняет сценарий: парсит продукты, обрабатывает их через ИИ и сохраняет данные.

    Args:
        system_instruction (Optional[str], optional): Системные инструкции для модели ИИ. По умолчанию `None`.
        price (Optional[str], optional): Цена для обработки. По умолчанию `None`.
        mexiron_name (Optional[str], optional): Пользовательское имя мехирона. По умолчанию `None`.
        urls (Optional[str | List[str]], optional): URLs страниц продуктов. По умолчанию `None`.

    Returns:
        bool: `True`, если сценарий выполнен успешно, иначе `False`.
    """
    ...
```

**Назначение**: Выполняет основной сценарий, включающий парсинг данных о продуктах, обработку через ИИ и сохранение результатов.

**Параметры**:
- `system_instruction`: Системные инструкции для модели ИИ (необязательный параметр).
- `price`: Цена для обработки (необязательный параметр).
- `mexiron_name`: Пользовательское имя мехирона (необязательный параметр).
- `urls`: Список URL-адресов страниц продуктов для парсинга.
- `bot`: Экземпляр бота (необязательный параметр).

**Возвращает**:
- `bool`: Возвращает `True`, если сценарий выполнен успешно, и `False` в противном случае.

**Как работает функция**:

1. **Проверка источника URL (IsOneTab)**:
   - Если URL из OneTab, данные извлекаются из OneTab.
   - Если URL не из OneTab, пользователю отправляется сообщение "Try again".
2. **Проверка валидности данных (IsDataValid)**:
   - Если данные не валидны, пользователю отправляется сообщение "Incorrect data".
   - Если данные валидны, запускается сценарий Mexiron.
3. **Поиск грабера (IsGraberFound)**:
   - Если грабер найден, начинается парсинг страницы.
   - Если грабер не найден, логируется сообщение о том, что грабер отсутствует для данного URL.
4. **Парсинг страницы (StartParsing)**:
   - Если парсинг успешен, данные преобразуются в нужный формат.
   - Если парсинг не удался, логируется ошибка.
5. **Преобразование данных (ConvertProductFields)**:
   - Если преобразование успешно, данные сохраняются.
   - Если преобразование не удалось, логируется ошибка.
6. **Сохранение данных (SaveProductData)**:
   - Если данные сохранены, они добавляются в список продуктов.
   - Если данные не сохранены, логируется ошибка.
7. **Обработка через AI (ProcessAIHe, ProcessAIRu)**:
   - Данные обрабатываются AI для языков `he` (иврит) и `ru` (русский).
8. **Сохранение JSON (SaveHeJSON, SaveRuJSON)**:
   - Результаты обработки сохраняются в формате JSON для каждого языка.
   - Если сохранение не удалось, логируется ошибка.
9. **Генерация отчетов (GenerateReports)**:
    - Создаются HTML и PDF отчеты для каждого языка.
    - Если создание отчета не удалось, логируется ошибка.
10. **Отправка PDF через Telegram (SendPDF)**:
     - PDF-файлы отправляются через Telegram.
     - Если отправка не удалась, логируется ошибка.
11. **Завершение (ReturnTrue)**:
     - Сценарий завершается, возвращая `True`.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
├── IsOneTab?
│   ├── Yes: GetDataFromOneTab
│   └── No: ReplyTryAgain
│
GetDataFromOneTab
│
├── IsDataValid?
│   ├── Yes: RunMexironScenario
│   └── No: ReplyIncorrectData
│
RunMexironScenario
│
├── IsGraberFound?
│   ├── Yes: StartParsing
│   └── No: LogNoGraber
│
StartParsing
│
├── IsParsingSuccessful?
│   ├── Yes: ConvertProductFields
│   └── No: LogParsingFailed
│
ConvertProductFields
│
├── IsConversionSuccessful?
│   ├── Yes: SaveProductData
│   └── No: LogConversionFailed
│
SaveProductData
│
├── IsDataSaved?
│   ├── Yes: AppendToProductsList
│   └── No: LogDataNotSaved
│
AppendToProductsList
│
ProcessAIHe
│
ProcessAIRu
│
├── SaveHeJSON?
│   ├── Yes: SaveRuJSON
│   └── No: LogHeJSONError
│
SaveRuJSON
│
├── IsRuJSONSaved?
│   ├── Yes: GenerateReports
│   └── No: LogRuJSONError
│
GenerateReports
│
├── IsReportGenerationSuccessful?
│   ├── Yes: SendPDF
│   └── No: LogPDFError
│
SendPDF
│
ReturnTrue
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Запуск сценария с URL-ами
urls = ['https://example.com/product1', 'https://example.com/product2']
result = mexiron_builder.run_scenario(urls=urls)
print(f"Сценарий выполнен: {result}")
```

#### `get_graber_by_supplier_url(self, url: str) -> None`

```python
def get_graber_by_supplier_url(self, url: str) -> None:
    """
    Возвращает соответствующий грабер для данного URL поставщика.

    Args:
        url (str): URL страницы поставщика.

    Returns:
        graber | None: Экземпляр грабера, если найден, иначе `None`.
    """
    ...
```

**Назначение**: Возвращает соответствующий грабер (парсер) для заданного URL поставщика.

**Параметры**:
- `url`: URL страницы поставщика, для которого требуется получить грабер.

**Возвращает**:
- Экземпляр грабера, если он найден для данного URL.
- `None`, если грабер не найден.

**Как работает функция**:

1. Функция проходит по списку доступных граберов (парсеров).
2. Для каждого грабера проверяется, соответствует ли его домен URL поставщика.
3. Если соответствие найдено, функция возвращает экземпляр этого грабера.
4. Если ни один грабер не соответствует URL, функция возвращает `None`.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
For each graber in grabers:
│
  ├── Does graber's domain match URL?
  │   ├── Yes: Return graber
  │   └── No: Continue to next graber
│
Return None
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# URL поставщика
url = "https://example.com/product"

# Получение грабера для URL
graber = mexiron_builder.get_graber_by_supplier_url(url)

# Проверка, был ли найден грабер
if graber:
    print(f"Найден грабер: {graber.__class__.__name__}")
else:
    print("Грабер не найден для данного URL")
```

#### `convert_product_fields(self, f: ProductFields) -> dict`

```python
def convert_product_fields(self, f: ProductFields) -> dict:
    """
    Конвертирует поля продукта в словарь.

    Args:
        f (ProductFields): Объект, содержащий парсированные данные о продукте.

    Returns:
        dict: Форматированный словарь данных о продукте.
    """
    ...
```

**Назначение**: Преобразует поля продукта из объекта `ProductFields` в словарь.

**Параметры**:
- `f`: Объект `ProductFields`, содержащий парсированные данные о продукте.

**Возвращает**:
- `dict`: Форматированный словарь, содержащий данные о продукте.

**Как работает функция**:

1. Функция принимает объект `ProductFields`, который содержит парсированные данные о продукте.
2. Создается пустой словарь `product`.
3. Извлекаются необходимые поля из объекта `f` (например, название, цена, описание и т.д.).
4. Поля добавляются в словарь `product` с соответствующими ключами.
5. Функция возвращает сформированный словарь `product`.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
Receive ProductFields object (f)
│
Create empty dictionary (product)
│
Extract fields from f and add to product dictionary
│
Return product dictionary
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder
from types import SimpleNamespace

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Создание объекта ProductFields (пример)
product_fields = SimpleNamespace(
    name="Test Product",
    price="100",
    description="Test description",
    image_url="https://example.com/image.jpg"
)

# Преобразование полей продукта в словарь
product_data = mexiron_builder.convert_product_fields(product_fields)

# Вывод результата
print(product_data)
```

#### `save_product_data(self, product_data: dict) -> None`

```python
def save_product_data(self, product_data: dict) -> None:
    """
    Сохраняет данные о продукте в файл.

    Args:
        product_data (dict): Форматированные данные о продукте.
    """
    ...
```

**Назначение**: Сохраняет данные о продукте в файл JSON.

**Параметры**:
- `product_data`: Словарь, содержащий форматированные данные о продукте.

**Как работает функция**:

1. Функция принимает словарь `product_data`, содержащий данные о продукте.
2. Формируется имя файла для сохранения данных, используя имя мехирона и временную метку.
3. Создается директория для сохранения данных, если она не существует.
4. Данные записываются в файл JSON с использованием кодировки UTF-8.
5. Если происходит ошибка при записи файла, логируется сообщение об ошибке.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
Receive product_data dictionary
│
Generate filename
│
Create directory if not exists
│
Try:
│   Write product_data to JSON file
│
Except:
│   Log error
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Пример данных о продукте
product_data = {
    "name": "Test Product",
    "price": "100",
    "description": "Test description",
    "image_url": "https://example.com/image.jpg"
}

# Сохранение данных о продукте
mexiron_builder.save_product_data(product_data)
```

#### `process_ai(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool`

```python
def process_ai(self, products_list: List[str], lang: str, attempts: int = 3) -> tuple | bool:
    """
    Обрабатывает список продуктов через модель ИИ.

    Args:
        products_list (List[str]): Список словарей данных о продуктах в виде строки.
        attempts (int): Количество попыток повторного запроса в случае неудачи.

    Returns:
        tuple | bool: Обработанный ответ в форматах `ru` и `he`.
    """
    ...
```

**Назначение**: Обрабатывает список продуктов с использованием модели искусственного интеллекта (AI).

**Параметры**:
- `products_list`: Список словарей данных о продуктах в виде строки.
- `lang`: Язык, на котором нужно обработать данные (`ru` или `he`).
- `attempts`: Количество попыток повторного запроса в случае неудачи.

**Возвращает**:
- `tuple`: Кортеж с обработанными данными для языков `ru` и `he`, если обработка успешна.
- `bool`: `False`, если обработка не удалась после нескольких попыток.

**Как работает функция**:

1. Функция принимает список продуктов и язык обработки.
2. Она отправляет запрос в модель AI для обработки данных на указанном языке.
3. Если запрос не удался, функция повторяет попытку несколько раз.
4. Если после нескольких попыток обработка все еще не удалась, функция возвращает `False`.
5. Если обработка успешна, функция возвращает обработанные данные в формате кортежа.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
Receive products_list and lang
│
For i in range(attempts):
│   Try:
│       Send request to AI model
│       If successful:
│           Return processed data
│   Except:
│       Log error
│
Return False
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Пример списка продуктов
products_list = [
    {"name": "Test Product 1", "price": "100", "description": "Description 1"},
    {"name": "Test Product 2", "price": "200", "description": "Description 2"}
]

# Обработка данных на русском языке
result = mexiron_builder.process_ai(products_list, lang="ru")

# Вывод результата
if result:
    print(f"Данные успешно обработаны: {result}")
else:
    print("Не удалось обработать данные после нескольких попыток")
```

#### `post_facebook(self, mexiron: SimpleNamespace) -> bool`

```python
def post_facebook(self, mexiron: SimpleNamespace) -> bool:
    """
    Выполняет сценарий публикации в Facebook.

    Args:
        mexiron (SimpleNamespace): Обработанные данные для публикации.

    Returns:
        bool: `True`, если публикация успешна, иначе `False`.
    """
    ...
```

**Назначение**: Публикует данные в Facebook.

**Параметры**:
- `mexiron`: Пространство имен, содержащее обработанные данные для публикации.

**Возвращает**:
- `True`, если публикация прошла успешно.
- `False`, если возникла ошибка при публикации.

**Как работает функция**:

1. Функция принимает данные, которые нужно опубликовать в Facebook.
2. Она использует API Facebook для создания и публикации поста.
3. Если публикация прошла успешно, функция возвращает `True`.
4. Если возникла ошибка, функция логирует ошибку и возвращает `False`.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
Receive mexiron data
│
Try:
│   Post data to Facebook using API
│   If successful:
│       Return True
│
Except:
│   Log error
│   Return False
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder
from types import SimpleNamespace

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Пример данных для публикации
mexiron_data = SimpleNamespace(
    name="Test Product",
    price="100",
    description="Test description",
    image_url="https://example.com/image.jpg"
)

# Публикация в Facebook
result = mexiron_builder.post_facebook(mexiron_data)

# Вывод результата
if result:
    print("Публикация в Facebook прошла успешно")
else:
    print("Ошибка при публикации в Facebook")
```

#### `create_report(self, data: dict, html_file: Path, pdf_file: Path) -> None`

```python
def create_report(self, data: dict, html_file: Path, pdf_file: Path) -> None:
    """
    Генерирует HTML и PDF отчеты из обработанных данных.

    Args:
        data (dict): Обработанные данные.
        html_file (Path): Путь для сохранения HTML отчета.
        pdf_file (Path): Путь для сохранения PDF отчета.
    """
    ...
```

**Назначение**: Создает HTML и PDF отчеты на основе предоставленных данных.

**Параметры**:
- `data`: Словарь, содержащий данные для отчета.
- `html_file`: Путь к файлу, в который будет сохранен HTML отчет.
- `pdf_file`: Путь к файлу, в который будет сохранен PDF отчет.

**Как работает функция**:

1. Функция принимает словарь данных и пути к файлам для HTML и PDF отчетов.
2. Генерирует HTML отчет на основе предоставленных данных и шаблона.
3. Сохраняет HTML отчет в указанный файл.
4. Преобразует HTML отчет в PDF формат.
5. Сохраняет PDF отчет в указанный файл.

**Внутренние функции**: Отсутствуют

**ASCII flowchart**:

```
Start
│
Receive data, html_file, pdf_file
│
Generate HTML report
│
Save HTML report to html_file
│
Convert HTML report to PDF
│
Save PDF report to pdf_file
```

**Примеры**:

```python
from src.webdriver import Driver
from src.webdriver.chrome import Chrome
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder
from pathlib import Path

# Инициализация драйвера
driver = Driver(Chrome)

# Инициализация MexironBuilder с драйвером
mexiron_builder = MexironBuilder(driver, mexiron_name="TestMexiron")

# Пример данных для отчета
report_data = {
    "products": [
        {"name": "Test Product 1", "price": "100", "description": "Description 1"},
        {"name": "Test Product 2", "price": "200", "description": "Description 2"}
    ]
}

# Пути к файлам для отчетов
html_file = Path("report.html")
pdf_file = Path("report.pdf")

# Создание отчета
mexiron_builder.create_report(report_data, html_file, pdf_file)
```

## Использование

Для использования этого скрипта выполните следующие шаги:

1. **Инициализация Driver**: Создайте экземпляр класса `Driver`.
2. **Инициализация MexironBuilder**: Создайте экземпляр класса `MexironBuilder` с драйвером.
3. **Запуск сценария**: Вызовите метод `run_scenario` с необходимыми параметрами.

#### Пример

```python
from src.webdriver.driver import Driver
from src.endpoints.kazarinov.scenarios.scenario_pricelist import MexironBuilder

# Инициализация Driver
driver = Driver(...)

# Инициализация MexironBuilder
mexiron_builder = MexironBuilder(driver)

# Запуск сценария
urls = ['https://example.com/product1', 'https://example.com/product2']
mexiron_builder.run_scenario(urls=urls)
```

## Зависимости

- `selenium`: Для веб-автоматизации.
- `asyncio`: Для асинхронных операций.
- `pathlib`: Для обработки путей к файлам.
- `types`: Для создания простых пространств имен.
- `typing`: Для аннотаций типов.
- `src.ai.gemini`: Для обработки данных через ИИ.
- `src.suppliers.*.graber`: Для извлечения данных от различных поставщиков.
- `src.endpoints.advertisement.facebook.scenarios`: Для публикации в Facebook.

## Обработка ошибок

Скрипт включает надежную обработку ошибок, чтобы обеспечить продолжение выполнения даже в случае, если некоторые элементы не найдены или если возникли проблемы с веб-страницей. Это особенно полезно для обработки динамических или нестабильных веб-страниц.

## Вклад

Вклад в этот скрипт приветствуется. Пожалуйста, убедитесь, что любые изменения хорошо документированы и включают соответствующие тесты.

## Лицензия

Этот скрипт лицензирован под MIT License. Подробности смотрите в файле `LICENSE`.