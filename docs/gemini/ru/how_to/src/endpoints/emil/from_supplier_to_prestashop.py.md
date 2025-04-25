## Как использовать класс `SupplierToPrestashopProvider` 
=========================================================================================

### Описание
-------------------------
Класс `SupplierToPrestashopProvider` отвечает за обработку данных о товарах поставщиков. Он извлекает, разбирает и сохраняет информацию о продуктах, полученную с сайтов поставщиков или из JSON-файлов. Класс также обрабатывает данные с помощью искусственного интеллекта (ИИ) и интегрирует их в систему Prestashop для публикации товаров. 

### Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте экземпляр класса `SupplierToPrestashopProvider`, передав в конструктор необходимые параметры: 
        - `lang`: Язык, на котором будут обрабатываться данные (например, 'he' для иврита).
        - `gemini_api`: Ключ API для доступа к модели Gemini.
        - `presta_api`: Ключ API для доступа к Prestashop.
        - `presta_url`: URL-адрес магазина Prestashop.
        - `driver`: Опционально, экземпляр Selenium WebDriver для автоматизации браузера. Если не задан, по умолчанию будет использоваться WebDriver с браузером Firefox.

2. **Обработка данных**:
    - Используйте метод `process_graber` для обработки данных с сайтов поставщиков:
        - Передайте в метод список `urls` - URL-адреса страниц с товарами.
        - Опционально можно передать:
            - `price`: Цену товара.
            - `mexiron_name`: Название товара.
            - `scenarios`: Сценарий исполнения для обработки данных, который находится в директории `src.suppliers.suppliers_list.<supplier>.sceanarios`.
    - Используйте метод `process_scenarios` для обработки данных из JSON-файлов.
        - Передайте в метод список `suppliers_prefixes` - префиксы поставщиков, для которых необходимо обработать данные.

3. **Обработка с помощью ИИ**:
    - Метод `process_llm` обрабатывает список данных о товарах с помощью модели ИИ (Gemini):
        - Передайте в метод список `products_list` - данные о товарах в виде списка словарей.
        - `lang`: Язык для обработки данных (например, 'he' для иврита).
        - `attempts`: Количество попыток повтора, если модель не возвращает правильный результат.

4. **Сохранение в Prestashop**:
    - Метод `save_in_prestashop` сохраняет данные о товарах в систему Prestashop:
        - Передайте в метод `products_list` - список данных о товарах в виде объектов `ProductFields`.

5. **Публикация в Facebook**:
    - Метод `post_facebook` публикует информацию о товаре в Facebook:
        - Передайте в метод `mexiron` - объект SimpleNamespace, содержащий данные о товаре (название, описание, цена).

6. **Создание отчета**:
    - Метод `create_report` генерирует отчеты о товарах в форматах HTML и PDF:
        - Передайте в метод:
            - `data`: Данные о товаре в виде словаря.
            - `lang`: Язык для создания отчета.
            - `html_file`: Путь к файлу HTML.
            - `pdf_file`: Путь к файлу PDF.

### Пример использования
-------------------------

```python
from src.endpoints.emil.scenarios.from_supplier_to_prestashop import SupplierToPrestashopProvider

# Инициализация класса
supplier_to_prestashop = SupplierToPrestashopProvider(
    lang='he',
    gemini_api='YOUR_GEMINI_API_KEY',
    presta_api='YOUR_PRESTASHOP_API_KEY',
    presta_url='YOUR_PRESTASHOP_URL'
)

# Обработка товаров с сайта поставщика
urls = [
    'https://www.example.com/product1',
    'https://www.example.com/product2'
]
await supplier_to_prestashop.process_graber(urls=urls)

# Сохранение товаров в Prestashop
products_list = [
    {'product_id': 1, 'name': 'Товар 1', 'description': 'Описание товара 1'},
    {'product_id': 2, 'name': 'Товар 2', 'description': 'Описание товара 2'}
]
await supplier_to_prestashop.save_in_prestashop(products_list)

# Публикация в Facebook
mexiron = SimpleNamespace(title='Название товара', description='Описание товара', price=100)
await supplier_to_prestashop.post_facebook(mexiron)

# Создание отчета
data = {'product_id': 1, 'name': 'Товар 1', 'description': 'Описание товара 1'}
html_file = Path('report.html')
pdf_file = Path('report.pdf')
await supplier_to_prestashop.create_report(data, 'he', html_file, pdf_file)
```