## Как использовать `get_graber_by_supplier_url` и `get_graber_by_supplier_prefix`
=========================================================================================

### Описание
-------------------------
Модуль `get_graber_by_supplier` предоставляет функции `get_graber_by_supplier_url` и `get_graber_by_supplier_prefix`, которые  позволяют получить объект грабера для конкретного поставщика на основе URL-адреса или префикса имени поставщика. 

Каждый поставщик имеет свой собственный класс грабера, который извлекает данные с целевой HTML-страницы.


### Шаги выполнения
-------------------------
1. **Импортируйте необходимые модули:**
   - `get_graber_by_supplier` для доступа к функциям.
   - `Driver` (веб-драйвер) из `src.webdriver`. 
   - `Graber` из `src.suppliers.graber` для получения грабера.
   - `logger` из `src.logger.logger` для логирования.

2. **Инициализируйте экземпляр веб-драйвера:**
   - Создайте экземпляр класса `Driver` с нужным типом драйвера (Chrome, Firefox, Playwright и т.д.).

3. **Используйте функцию `get_graber_by_supplier_url` для получения грабера по URL:**
   - Передайте экземпляр веб-драйвера (`driver`), URL-адрес поставщика (`url`) и индекс языка (`lang_index`) в функцию `get_graber_by_supplier_url`. 
   - Функция возвращает экземпляр класса `Graber` для соответствующего поставщика, если URL-адрес совпадает с одним из поддерживаемых, в противном случае возвращает `None`.
   - Проверьте результат. Если грабер найден, вы можете использовать его для извлечения данных.
   - Если грабер не найден, обработайте эту ситуацию.

4. **Используйте функцию `get_graber_by_supplier_prefix` для получения грабера по префиксу:**
   - Передайте экземпляр веб-драйвера (`driver`), строковый префикс поставщика (`supplier_prefix`) и индекс языка (`lang_index`) в функцию `get_graber_by_supplier_prefix`.
   - Функция возвращает экземпляр класса `Graber` для соответствующего поставщика, если префикс совпадает с одним из поддерживаемых, в противном случае возвращает `None`.
   - Проверьте результат. Если грабер найден, вы можете использовать его для извлечения данных.
   - Если грабер не найден, обработайте эту ситуацию.

### Пример использования
-------------------------
```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url, get_graber_by_supplier_prefix
    from src.webdriver import Driver # Предполагается, что Driver импортируется так
    from src.logger.logger import logger

    # Инициализация драйвера (пример)
    driver = Driver() 
    url = 'https://www.example.com'
    graber = get_graber_by_supplier_url(driver, url, 2) # Пример с lang_index = 2

    if graber:
        # Использование грабера для извлечения данных
        product_data = graber.get_product_data()
        print(f'Data extracted: {product_data}')
    else:
        # Обработка случая, когда грабер не найден
        print(f'No grabber found for URL: {url}')

    # Пример использования get_graber_by_supplier_prefix
    supplier_prefix = 'ksp'
    graber = get_graber_by_supplier_prefix(driver, supplier_prefix, 2)

    if graber:
        # Использование грабера для извлечения данных
        product_data = graber.get_product_data()
        print(f'Data extracted: {product_data}')
    else:
        # Обработка случая, когда грабер не найден
        logger.debug(f'грабер для префикса поставщика не найден: {supplier_prefix}')
        print(f'No grabber found for supplier prefix: {supplier_prefix}')

```