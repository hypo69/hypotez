## Как использовать класс `QuotationBuilder`

=========================================================================================

### Описание

-------------------------

Класс `QuotationBuilder` предназначен для обработки данных о товарах от поставщиков, включая извлечение, разбор и сохранение информации, а также генерацию отчетов и публикации в Facebook.

### Шаги выполнения

-------------------------

1. **Инициализация экземпляра класса `QuotationBuilder`**:
    - При создании объекта `QuotationBuilder` необходимо указать название Mexiron-процесса (имя каталога для сохранения информации). 
    - Опционально можно передать экземпляр Selenium WebDriver. 
    - Если вебдрайвер не указан, используется Firefox по умолчанию. 
2. **Обработка данных о товарах**: 
    - Класс имеет метод `convert_product_fields`, который принимает объект `ProductFields` с информацией о товаре и преобразует ее в простой словарь.
    - Для перевода текстов о товарах, используется метод `process_llm` с использованием модели Google Generative AI.
    - Метод `process_llm` отправляет запросы в модель с текстом о товарах, получает перевод на русский и иврит и сохраняет в словарь.
3. **Сохранение данных о товарах**: 
    - Метод `save_product_data` сохраняет обработанные данные о товаре в файл формата JSON.
4. **Генерация отчетов**: 
    - Метод `create_reports` генерирует отчеты о товарах в HTML, PDF и DOCX форматах.
5. **Публикация в Facebook**: 
    - Метод `post_facebook_async` публикует данные о товаре в Facebook (использует сценарии `facvebook` модуля).

### Пример использования

-------------------------

```python
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.jjson import j_loads

# Загружаем данные о товаре из JSON-файла
product_data = j_loads(Path('/path/to/product_data.json'))

# Создаем объект ProductFields из данных о товаре
product_fields = ProductFields(**product_data)

# Создаем экземпляр QuotationBuilder
quotation_builder = QuotationBuilder(mexiron_name='my_mexiron_name')

# Преобразуем данные о товаре в словарь
product_dict = quotation_builder.convert_product_fields(product_fields)

# Обрабатываем текст о товаре с помощью AI
response = quotation_builder.process_llm([product_dict], lang='ru')

# Сохраняем обработанные данные о товаре
quotation_builder.save_product_data(product_dict)

# Генерируем отчеты
quotation_builder.create_reports(product_dict, mexiron_name='my_mexiron_name', lang='ru', html_path='/path/to/report.html', pdf_path='/path/to/report.pdf', docx_path='/path/to/report.docx')

# Публикуем данные о товаре в Facebook
quotation_builder.post_facebook_async(product_dict)
```

### Замечания

- Метод `post_facebook_async` работает асинхронно, поэтому необходимо использовать `asyncio.run` для его запуска.
- Метод `process_llm` использует модель Google Generative AI, для ее работы требуется API-ключ.
- Класс `QuotationBuilder` использует файлы конфигурации, которые должны быть доступны в каталоге проекта.