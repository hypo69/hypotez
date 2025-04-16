# Модуль `quotation_builder`

## Обзор

Модуль предназначен для обработки извлечения, разбора и сохранения данных о товарах поставщиков, а также для интеграции с рекламным модулем Facebook и генерации отчетов.

## Подробней

Модуль предоставляет класс `QuotationBuilder`, который выполняет следующие задачи:

1.  Извлечение данных о товарах с веб-сайтов поставщиков.
2.  Разбор и преобразование полученных данных.
3.  Сохранение обработанных данных в файлы.
4.  Интеграция с моделью Google Gemini для обработки текстовой информации.
5.  Интеграция с Facebook для публикации рекламных объявлений.
6.  Генерация отчетов в формате HTML и PDF.

## Классы

### `Config`

**Описание**: Класс конфигурации для модуля `quotation_builder`.

**Атрибуты**:

*   `ENDPOINT` (str): Конечная точка API (значение: `'kazarinov'`).

### `QuotationBuilder`

**Описание**: Класс для обработки извлечения, разбора и сохранения данных о товарах поставщиков.

**Атрибуты**:

*   `base_path` (Path): Базовый путь к директории модуля.
*   `config` (SimpleNamespace): Объект с конфигурационными параметрами, загруженными из JSON-файла.
*   `html_path` (str | Path): Путь к HTML-файлу отчета.
*   `pdf_path` (str | Path): Путь к PDF-файлу отчета.
*   `docx_path` (str | Path): Путь к DOCX-файлу отчета.
*   `driver` (Driver): Экземпляр Selenium WebDriver.
*   `export_path` (Path): Путь для экспорта данных.
*   `mexiron_name` (str): Имя мехирона.
*   `price` (float): Цена.
*   `timestamp` (str): Временная метка.
*   `products_list` (List): Список обработанных данных о товарах.
*   `model` (GoogleGenerativeAi): Объект GoogleGenerativeAi для взаимодействия с моделью Gemini.
*   `translations` (SimpleNamespace): Объект с переводами, загруженными из JSON-файла.
*   `required_fields` (tuple): Кортеж с необходимыми полями товара.

**Методы**:

*   `__init__`: Инициализирует объект `QuotationBuilder`.
*   `convert_product_fields`: Конвертирует поля товара из объекта `ProductFields` в словарь.
*   `process_llm`: Обрабатывает список товаров с использованием ИИ модели.
*   `process_llm_async`: Асинхронно обрабатывает список товаров с использованием ИИ модели.
*   `save_product_data`: Сохраняет данные о товаре в файл.
*   `post_facebook_async`: Асинхронно публикует сообщение в Facebook.

### `__init__`

```python
def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None,  **kwards):
    """
    Initializes Mexiron class with required components.

    Args:
        driver (Driver): Selenium WebDriver instance.
        mexiron_name (Optional[str]): Custom name for the Mexiron process.
        webdriver_name (Optional[str]): Name of the WebDriver to use. Defaults to 'firefox'. call to Firefox or Playwrid
        window_mode (Optional[str]): Оконный режим вебдрайвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'

    """
    ...
```

**Назначение**: Инициализирует объект `QuotationBuilder`.

**Параметры**:

*   `mexiron_name` (Optional[str]): Название мехирона. По умолчанию используется текущее время (`gs.now`).
*   `driver` (Optional[Firefox | Playwrid | str]): Экземпляр веб-драйвера или его название (`'firefox'`, `'playwright'`). По умолчанию используется Firefox.
*   `**kwards`: Дополнительные параметры для веб-драйвера.

**Как работает функция**:

1.  Устанавливает имя мехирона `mexiron_name` и формирует путь для экспорта данных `export_path`.
2.  Инициализирует веб-драйвер на основе переданного аргумента `driver` (Firefox или Playwright).
3.  Инициализирует модель Gemini для обработки текста.

### `convert_product_fields`

```python
def convert_product_fields(self, f: ProductFields) -> dict:
    """
    Converts product fields into a dictionary. 
    Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ии.

    Args:
        f (ProductFields): Object containing parsed product data.

    Returns:
        dict: Formatted product data dictionary.

    .. note:: Правила построения полей определяются в `ProductFields`
    """
    ...
```

**Назначение**: Преобразует поля товара из объекта `ProductFields` в словарь.

**Параметры**:

*   `f` (ProductFields): Объект `ProductFields`, содержащий данные о товаре.

**Возвращает**:

*   `dict`: Словарь с данными о товаре.

**Как работает функция**:

1.  Извлекает значения нужных полей из объекта `ProductFields`.
2.  Формирует словарь с данными о товаре.

### `process_llm`

```python
def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    """
    Processes the product list through the AI model.

    Args:
        products_list (str): List of product data dictionaries as a string.
        attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

    Returns:
        tuple: Processed response in `ru` and `he` formats.
        bool: False if unable to get a valid response after retries.

    .. note::
        Модель может возвращать невалидный результат.
        В таком случае я переспрашиваю модель разумное количество раз.
    """
    ...
```

**Назначение**: Обрабатывает список товаров с использованием ИИ модели.

**Параметры**:

*   `products_list` (List[str]): Список словарей с данными о товарах в виде строки.
*   `lang` (str): Язык, на котором необходимо получить результат.
*   `attempts` (int, optional): Количество попыток повторной отправки запроса в случае неудачи. По умолчанию 3.

**Возвращает**:

*   `tuple`: Обработанный ответ в форматах `ru` и `he`.
*   `bool`: `False`, если не удалось получить валидный ответ после указанного количества попыток.

**Как работает функция**:

1.  Загружает инструкцию для модели из файла.
2.  Формирует запрос к модели, объединяя инструкцию и список товаров.
3.  Отправляет запрос к модели и получает ответ.
4.  В случае ошибки повторяет попытку несколько раз.
5.  Разбирает ответ модели в словарь.

### `process_llm_async`

```python
async def process_llm_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool:
    """
    Processes the product list through the AI model.

    Args:
        products_list (str): List of product data dictionaries as a string.
        attempts (int, optional): Number of attempts to retry in case of failure. Defaults to 3.

    Returns:
        tuple: Processed response in `ru` and `he` formats.
        bool: False if unable to get a valid response after retries.

    .. note::
        Модель может возвращать невалидный результат.
        В таком случае я переспрашиваю модель разумное количество раз.
    """
    ...
```

**Назначение**: Асинхронно обрабатывает список товаров с использованием ИИ модели.

**Параметры**:

*   `products_list` (List[str]): Список словарей с данными о товарах в виде строки.
*   `lang` (str): Язык, на котором необходимо получить результат.
*   `attempts` (int, optional): Количество попыток повторной отправки запроса в случае неудачи. По умолчанию 3.

**Возвращает**:

*   `tuple`: Обработанный ответ в форматах `ru` и `he`.
*   `bool`: `False`, если не удалось получить валидный ответ после указанного количества попыток.

**Как работает функция**:

1.  Загружает инструкцию для модели из файла.
2.  Формирует запрос к модели, объединяя инструкцию и список товаров.
3.  Отправляет асинхронный запрос к модели и получает ответ.
4.  В случае ошибки повторяет попытку несколько раз.
5.  Разбирает ответ модели в словарь.

### `save_product_data`

```python
async def save_product_data(self, product_data: dict) -> bool:
    """
    Saves individual product data to a file.

    Args:
        product_data (dict): Formatted product data.
    """
    ...
```

**Назначение**: Сохраняет данные о товаре в файл.

**Параметры**:
- `product_data` (dict): Словарь с данными о товаре.

**Возвращает**:
- `bool`: `True`, если данные успешно сохранены, иначе `False`.

**Как работает функция**:

1.  Формирует путь к файлу для сохранения данных о товаре.
2.  Сохраняет словарь с данными о товаре в файл в формате JSON.

### `post_facebook_async`

```python
async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool:
    """Функция исполняет сценарий рекламного модуля `facvebook`."""
    ...
```

**Назначение**: Асинхронно публикует рекламное сообщение в Facebook.

**Параметры**:

*   `mexiron` (SimpleNamespace): Объект SimpleNamespace с данными о мехироне.

**Возвращает**:

*   `bool`: `True`, если публикация прошла успешно, иначе `False`.

**Как работает функция**:

1.  Выполняет шаги, необходимые для публикации сообщения в Facebook, используя методы из модуля `src.endpoints.advertisement.facebook.scenarios`.
2.  Загружает изображение товара и публикует сообщение с заголовком и изображением на странице Facebook.

## Функции

### `main`

```python
def main():
    """"""
    ...
```

**Назначение**: Главная функция модуля, запускающая процесс создания отчетов.

**Как работает функция**:
- Внутри функции находится заглушка `...`, что означает, что реализация данной функции не предоставлена в данном коде.

## Зависимости

*   `selenium`: Для веб-автоматизации.
*   `asyncio`: Для асинхронных операций.
*   `pathlib`: Для обработки путей к файлам.
*   `types`: Для создания простых пространств имен.
*   `typing`: Для аннотаций типов.
*   `src.ai.gemini`: Для обработки данных ИИ.
*   `src.suppliers.*.graber`: Для извлечения данных от различных поставщиков.
*   `src.endpoints.advertisement.facebook.scenarios`: Для публикации в Facebook.
## Примечания
В предоставленном коде присутствуют закомментированные участки, которые, возможно, содержат устаревшие или неиспользуемые реализации. Также стоит обратить внимание на точки интеграции с внешними модулями (такими как `src.endpoints.advertisement.facebook.scenarios` и `src.suppliers.*.graber`), где требуется обеспечить корректную передачу данных и обработку возможных ошибок.
```python
...
```
Данный код указывает на то, что в модуле есть еще не реализованная функциональность.