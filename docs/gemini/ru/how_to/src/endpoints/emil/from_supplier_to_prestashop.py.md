### **Инструкции по использованию блока кода**

=========================================================================================

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует класс `SupplierToPrestashopProvider`, предназначенный для извлечения, обработки и сохранения данных о товарах от поставщиков с последующей интеграцией этих данных в Prestashop. Он включает в себя функциональность для получения данных как с сайтов поставщиков, так и из JSON-файлов, обработки данных с использованием AI, а также сохранения обработанных данных в Prestashop.

Шаги выполнения
-------------------------
1. **Инициализация класса `SupplierToPrestashopProvider`**:
   - Создается экземпляр класса `SupplierToPrestashopProvider` с передачей необходимых параметров, таких как язык (`lang`), ключи API для Gemini и Prestashop, а также URL Prestashop.
   - При инициализации загружается конфигурация из JSON-файла, инициализируется Selenium WebDriver (если не передан), и настраивается AI модель Gemini.

2. **Обработка данных о товарах**:
   - Используется метод `process_graber` для получения данных о товарах с использованием URL поставщиков. Этот метод выполняет следующие действия:
     - Получает грабер (парсер) для каждого URL поставщика.
     - Извлекает данные о товаре с использованием грабера.
     - Преобразует полученные данные о товаре в нужный формат.
     - Сохраняет преобразованные данные.

3. **Преобразование данных о товаре**:
   - Метод `convert_product_fields` преобразует извлеченные поля товара в формат, подходящий для дальнейшей обработки и сохранения.

4. **Сохранение данных о товаре**:
   - Метод `save_product_data` сохраняет данные о товаре в JSON-файл.

5. **Обработка данных с использованием AI**:
   - Метод `process_llm` отправляет данные о товарах в AI модель Gemini для дальнейшей обработки, например, для генерации описаний или других атрибутов товара.

6. **Сохранение данных в Prestashop**:
   - Метод `save_in_prestashop` сохраняет обработанные данные о товарах в Prestashop с использованием API Prestashop.

7. **Публикация в Facebook (опционально)**:
   - Метод `post_facebook` публикует информацию о товаре в Facebook, используя Selenium WebDriver для взаимодействия с интерфейсом Facebook.

8. **Создание отчета (опционально)**:
   - Метод `create_report` генерирует отчет о товаре в формате HTML и PDF и отправляет PDF-файл боту.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.emil.from_supplier_to_prestashop import SupplierToPrestashopProvider
from src.webdriver.firefox import Firefox
from src.webdriver.driver import Driver

async def main():
    # Инициализация параметров
    lang = 'he'
    gemini_api = 'your_gemini_api_key'
    presta_api = 'your_prestashop_api_key'
    presta_url = 'your_prestashop_url'
    urls = ['https://example.com/product1', 'https://example.com/product2']

    # Инициализация класса SupplierToPrestashopProvider
    driver = Driver(Firefox)
    supplier_to_presta = SupplierToPrestashopProvider(
        lang=lang,
        gemini_api=gemini_api,
        presta_api=presta_api,
        presta_url=presta_url,
        driver=driver
    )

    # Обработка данных о товарах
    await supplier_to_presta.process_graber(urls=urls)

    # Необязательные шаги:
    # await supplier_to_presta.post_facebook(...)
    # await supplier_to_presta.create_report(...)

if __name__ == "__main__":
    asyncio.run(main())
```