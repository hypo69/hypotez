### **Как использовать блок кода `get_graber_by_supplier_url`**

=========================================================================================

Описание
-------------------------
Функция `get_graber_by_supplier_url` определяет и возвращает соответствующий объект-грабер в зависимости от URL поставщика. Каждый поставщик имеет свой собственный грабер, предназначенный для извлечения данных с его страниц.

Шаги выполнения
-------------------------
1. Функция `get_graber_by_supplier_url` принимает URL-адрес страницы поставщика (`url`) и индекс языка (`lang_index`) в качестве входных параметров.
2. Функция выполняет проверку URL-адреса на соответствие известным префиксам URL-адресов поставщиков, таким как "https://aliexpress.com", "https://amazon.com" и т.д.
3. Если URL-адрес соответствует одному из известных префиксов, функция создает экземпляр соответствующего класса грабера (например, `AliexpressGraber`, `AmazonGraber`) и возвращает его. Класс грабера инициализируется с драйвером и индексом языка.
4. Если URL-адрес не соответствует ни одному из известных префиксов, функция записывает отладочное сообщение в лог с помощью `logger.debug` и возвращает `None`.

Пример использования
-------------------------

```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
    from src.webdriver import Driver

    driver = Driver()
    url = 'https://www.aliexpress.com/item/1234567890.html'
    lang_index = 2
    graber = get_graber_by_supplier_url(driver, url, lang_index)

    if graber:
        # Используем грабер для извлечения данных
        product_data = graber.get_data()
        print(product_data)
    else:
        # Обрабатываем случай, когда грабер не найден
        print(f"грабер для URL {url} не найден")
```
```markdown
### **Как использовать блок кода `get_graber_by_supplier_prefix`**

=========================================================================================

Описание
-------------------------
Функция `get_graber_by_supplier_prefix` определяет и возвращает соответствующий объект-грабер в зависимости от префикса поставщика.

Шаги выполнения
-------------------------
1. Функция `get_graber_by_supplier_prefix` принимает префикс поставщика (`supplier_prefix`) и индекс языка (`lang_index`, по умолчанию "2") в качестве входных параметров.
2. Функция выполняет проверку `supplier_prefix` на соответствие известным префиксам поставщиков, таким как "aliexpress", "amazon" и т.д.
3. Если `supplier_prefix` соответствует одному из известных префиксов, функция создает экземпляр соответствующего класса грабера (например, `AliexpressGraber`, `AmazonGraber`) и возвращает его. Класс грабера инициализируется с драйвером и индексом языка.
4. Если `supplier_prefix` не соответствует ни одному из известных префиксов, функция возвращает `grabber or False`.

Пример использования
-------------------------

```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
    from src.webdriver import Driver

    driver = Driver()
    supplier_prefix = 'aliexpress'
    lang_index = '2'
    graber = get_graber_by_supplier_prefix(driver, supplier_prefix, lang_index)

    if graber:
        # Используем грабер для извлечения данных
        product_data = graber.get_data()
        print(product_data)
    else:
        # Обрабатываем случай, когда грабер не найден
        print(f"грабер для префикса {supplier_prefix} не найден")