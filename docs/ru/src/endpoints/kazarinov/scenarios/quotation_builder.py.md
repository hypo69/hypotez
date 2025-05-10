# Модуль для подготовки данных, обработки AI и интеграции с Facebook для публикации товаров.

## Обзор

Модуль `quotation_builder.py` предназначен для извлечения, разбора и сохранения данных о товарах от различных поставщиков. Он включает в себя подготовку данных, обработку с использованием искусственного интеллекта (AI) и интеграцию с Facebook для публикации товаров.

## Подробнее

Модуль предоставляет функциональность для автоматизации процесса сбора информации о товарах, их обработки и публикации на платформе Facebook. Он использует различные классы и функции для взаимодействия с поставщиками, обработки данных и выполнения задач, связанных с AI.

## Классы

### `Config`

**Описание**: Класс конфигурации для определения констант, используемых в модуле.

**Атрибуты**:
- `ENDPOINT` (str): Константа, определяющая endpoint (`kazarinov`).

### `QuotationBuilder`

**Описание**: Класс, отвечающий за извлечение, разбор и сохранение данных о товарах поставщиков.

**Атрибуты**:
- `base_path` (Path): Базовый путь к директории модуля.
- `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла.
- `html_path` (str | Path): Путь к HTML-файлу.
- `pdf_path` (str | Path): Путь к PDF-файлу.
- `docx_path` (str | Path): Путь к DOCX-файлу.
- `driver` (Driver): Экземпляр Selenium WebDriver для управления браузером.
- `export_path` (Path): Путь для экспорта данных.
- `mexiron_name` (str): Имя процесса Mexiron.
- `price` (float): Цена.
- `timestamp` (str): Временная метка.
- `products_list` (List[dict]): Список обработанных данных о товарах.
- `model` (GoogleGenerativeAi): Экземпляр модели Google Gemini для обработки текста.
- `translations` (SimpleNamespace): Переводы, загруженные из JSON-файла.
- `required_fields` (tuple): Кортеж необходимых полей товара.

**Методы**:
- `__init__`: Инициализирует класс `QuotationBuilder`.
- `convert_product_fields`: Преобразует поля товара в словарь.
- `process_llm`: Обрабатывает список товаров с помощью AI-модели.
- `process_llm_async`: Асинхронно обрабатывает список товаров с помощью AI-модели.
- `save_product_data`: Сохраняет данные товара в файл.
- `post_facebook_async`: Исполняет сценарий рекламного модуля `facebook`.

## Методы класса

### `__init__`

```python
def __init__(self, mexiron_name:Optional[str] = gs.now, driver:Optional[Firefox | Playwrid | str] = None,  **kwargs)
```

**Назначение**: Инициализирует класс `QuotationBuilder` с необходимыми компонентами, такими как WebDriver и модель Gemini.

**Параметры**:
- `mexiron_name` (Optional[str]): Пользовательское имя для процесса Mexiron. По умолчанию `gs.now`.
- `driver` (Optional[Firefox | Playwrid | str]): Экземпляр Selenium WebDriver. Может быть экземпляром `Firefox`, `Playwrid` или строкой (`'firefox'` или `'playwright'`). По умолчанию `None`.
- `kwargs` (dict): Дополнительные аргументы для инициализации WebDriver.

**Как работает функция**:
1. Инициализирует имя процесса `mexiron_name`.
2. Строит путь для экспорта данных на основе имени процесса.
3. Инициализирует WebDriver, используя предоставленный драйвер или создает новый экземпляр `Firefox`, если драйвер не указан. Поддерживает оконные режимы.
4. Инициализирует модель Gemini с использованием API-ключа и системных инструкций.

**Примеры**:

```python
quotation = QuotationBuilder(mexiron_name='test_mexiron', driver='firefox', window_mode='maximized')
quotation = QuotationBuilder(driver=Playwrid(), window_mode='headless')
```

### `convert_product_fields`

```python
def convert_product_fields(self, f: ProductFields) -> dict
```

**Назначение**: Преобразует поля товара из объекта `ProductFields` в словарь для использования в AI-модели.

**Параметры**:
- `f` (ProductFields): Объект, содержащий распарсенные данные о товаре.

**Возвращает**:
- `dict`: Словарь с отформатированными данными товара. Возвращает пустой словарь, если `id_product` отсутствует.

**Как работает функция**:
1. Проверяет наличие `id_product` в данных товара. Если отсутствует, возвращает пустой словарь.
2. Извлекает значения полей товара, таких как `name`, `description`, `description_short` и `specification`.
3. Возвращает словарь, содержащий извлеченные данные товара.

**Примеры**:

```python
product_fields = ProductFields(...)  # Предположим, что product_fields - это экземпляр ProductFields
product_data = quotation.convert_product_fields(product_fields)
```

### `process_llm`

```python
def process_llm(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool
```

**Назначение**: Обрабатывает список товаров с помощью AI-модели Google Gemini.

**Параметры**:
- `products_list` (List[str]): Список данных о товарах в виде строки.
- `lang` (str): Язык, на котором нужно получить ответ от модели.
- `attempts` (int, optional): Количество попыток для повторной отправки запроса в случае неудачи. По умолчанию `3`.

**Возвращает**:
- `dict`: Обработанный ответ от модели в виде словаря.
- `bool`: Возвращает пустой словарь, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:
1. Проверяет количество оставшихся попыток. Если их нет, возвращает пустой словарь.
2. Формирует запрос для AI-модели, объединяя команду и список товаров.
3. Отправляет запрос к AI-модели и получает ответ.
4. Пытается распарсить ответ в формате JSON. Если парсинг не удался, повторяет запрос (если остались попытки).
5. Возвращает распарсенный ответ в виде словаря.

**Примеры**:

```python
products = ['{"product_name": "Example Product", "product_id": "123"}']
response = quotation.process_llm(products, lang='ru')
if response:
    print(response)
```

### `process_llm_async`

```python
async def process_llm_async(self, products_list: List[str], lang:str,  attempts: int = 3) -> tuple | bool
```

**Назначение**: Асинхронно обрабатывает список товаров с помощью AI-модели Google Gemini.

**Параметры**:
- `products_list` (List[str]): Список данных о товарах в виде строки.
- `lang` (str): Язык, на котором нужно получить ответ от модели.
- `attempts` (int, optional): Количество попыток для повторной отправки запроса в случае неудачи. По умолчанию `3`.

**Возвращает**:
- `dict`: Обработанный ответ от модели в виде словаря.
- `bool`: Возвращает пустой словарь, если не удалось получить валидный ответ после всех попыток.

**Как работает функция**:
1. Проверяет количество оставшихся попыток. Если их нет, возвращает пустой словарь.
2. Формирует запрос для AI-модели, объединяя команду и список товаров.
3. Отправляет асинхронный запрос к AI-модели и получает ответ.
4. Пытается распарсить ответ в формате JSON. Если парсинг не удался, повторяет запрос (если остались попытки).
5. Возвращает распарсенный ответ в виде словаря.

**Примеры**:

```python
products = ['{"product_name": "Example Product", "product_id": "123"}']
response = await quotation.process_llm_async(products, lang='ru')
if response:
    print(response)
```

### `save_product_data`

```python
async def save_product_data(self, product_data: dict) -> bool
```

**Назначение**: Сохраняет данные товара в файл в формате JSON.

**Параметры**:
- `product_data` (dict): Словарь с данными товара.

**Возвращает**:
- `bool`: `True`, если данные успешно сохранены, иначе `False`.

**Как работает функция**:
1. Формирует путь к файлу, где будут сохранены данные товара.
2. Сохраняет данные в формате JSON по указанному пути.
3. Возвращает `True` в случае успеха, `False` в случае ошибки.

**Примеры**:

```python
product_data = {"product_name": "Example Product", "product_id": "123"}
result = await quotation.save_product_data(product_data)
if result:
    print("Product data saved successfully.")
```

### `post_facebook_async`

```python
async def post_facebook_async(self, mexiron:SimpleNamespace) -> bool
```

**Назначение**: Публикует информацию о товаре на Facebook, используя рекламный модуль.

**Параметры**:
- `mexiron` (SimpleNamespace): Объект, содержащий информацию о товаре (заголовок, описание, цена, медиафайлы).

**Возвращает**:
- `bool`: `True`, если публикация прошла успешно, иначе `False`.

**Как работает функция**:
1. Переходит на страницу профиля Facebook.
2. Формирует заголовок сообщения, включающий название, описание и цену товара.
3. Отправляет заголовок сообщения.
4. Загружает медиафайлы (изображения) для товара.
5. Публикует сообщение.
6. Возвращает `True` в случае успеха, `False` в случае ошибки.

**Примеры**:

```python
mexiron_data = SimpleNamespace(title='Example Title', description='Example Description', price=100, products=['image1.jpg', 'image2.jpg'])
result = await quotation.post_facebook_async(mexiron_data)
if result:
    print("Posted to Facebook successfully.")
```

## Параметры класса

- `driver` (Driver): Экземпляр Selenium WebDriver.
- `export_path` (Path): Путь для экспорта данных.
- `products_list` (List[dict]): Список обработанных данных о товарах.

## Функция `main`

```python
def main()
```

**Назначение**: Основная функция для запуска процесса создания отчетов.

**Как работает функция**:
1. Определяет параметры, такие как язык, имя Mexiron, базовый путь и пути к файлам отчетов.
2. Загружает данные из JSON-файла.
3. Создает экземпляр класса `QuotationBuilder`.
4. Запускает асинхронное создание отчетов.

**Примеры**:

```python
if __name__ == '__main__':
    main()