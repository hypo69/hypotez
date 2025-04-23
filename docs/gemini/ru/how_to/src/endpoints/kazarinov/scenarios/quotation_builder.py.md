### Как использовать класс `QuotationBuilder`
=========================================================================================

Описание
-------------------------
Класс `QuotationBuilder` предназначен для извлечения, разбора и сохранения данных о товарах от различных поставщиков. Он инициализирует веб-драйвер, модель машинного обучения Gemini и выполняет различные операции, такие как преобразование полей товара, обработка данных с использованием модели машинного обучения и сохранение данных о товарах.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `QuotationBuilder`, указав имя процесса Mexiron и экземпляр веб-драйвера. Если веб-драйвер не указан, будет использован Firefox по умолчанию.
2. **Преобразование полей товара**: Используйте метод `convert_product_fields` для преобразования объекта `ProductFields` в словарь, пригодный для использования в модели машинного обучения.
3. **Обработка данных с использованием LLM**: Используйте методы `process_llm` или `process_llm_async` для обработки списка товаров с помощью модели машинного обучения Gemini. Эти методы отправляют данные в модель, получают ответы и возвращают обработанные ответы в формате `ru` и `he`.
4. **Сохранение данных о товарах**: Используйте метод `save_product_data` для сохранения отдельных данных о товарах в JSON-файл.
5. **Размещение в Facebook**: Используйте метод `post_facebook_async` для размещения рекламных материалов в Facebook, используя данные, обработанные моделью машинного обучения.

Пример использования
-------------------------

```python
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.webdriver.firefox import Firefox
from src.endpoints.prestashop.product_fields import ProductFields
from pathlib import Path
from types import SimpleNamespace
import asyncio

# 1. Инициализация класса QuotationBuilder
mexiron_name = 'test_mexiron'
driver = Firefox() # или Playwrid()
quotation_builder = QuotationBuilder(mexiron_name=mexiron_name, driver=driver)

# 2. Пример преобразования полей товара
# Допустим, у вас есть объект ProductFields
product_fields = ProductFields(
    id_product='123',
    name={'language': {'value': 'Test Product'}},
    description_short={'language': {'value': 'Short description'}},
    description={'language': {'value': 'Long description'}},
    specification={'language': {'value': 'Specification'}},
    local_image_path=Path('/path/to/image.jpg')
)
product_data = quotation_builder.convert_product_fields(product_fields)
print(product_data)

# 3. Пример обработки списка товаров с использованием LLM
async def process_data():
    products_list = [product_data]
    lang = 'ru'
    processed_data = await quotation_builder.process_llm_async(products_list, lang)
    print(processed_data)

# Запуск асинхронной функции
asyncio.run(process_data())

# 4. Пример сохранения данных о товаре
async def save_data():
    await quotation_builder.save_product_data(product_data)

asyncio.run(save_data())

# 5. Пример размещения в Facebook
async def post_to_facebook():
    # Создаем объект SimpleNamespace с необходимыми данными для размещения
    mexiron = SimpleNamespace(
        title='Заголовок для Facebook',
        description='Описание для Facebook',
        price='100',
        products=['/path/to/image.jpg']
    )
    await quotation_builder.post_facebook_async(mexiron)

asyncio.run(post_to_facebook())