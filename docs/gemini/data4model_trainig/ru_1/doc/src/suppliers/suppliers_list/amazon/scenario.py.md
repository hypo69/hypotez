# Модуль `scenario.py`

## Обзор

Модуль предназначен для сбора информации о товарах с сайта поставщика amazon.com через веб-драйвер. Он содержит функции для получения списка категорий, списка товаров в категориях и обработки страниц товаров.

## Подробней

Этот модуль является частью процесса обработки данных от поставщиков в проекте `hypotez`. Он отвечает за взаимодействие с сайтом amazon.com, извлечение данных о товарах и их передачу для дальнейшей обработки и сохранения в базе данных. Модуль предназначен для работы с категориями товаров, представленными на сайте поставщика.

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category(s) -> list[str,str,None]:
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s: Supplier - экземпляр класса Supplier.

    Returns:
        list[str, str, None]: Список URL товаров или None, если список не был получен.

    Принцип работы:
        Функция получает локаторы элементов страницы категории из объекта Supplier.
        Выполняет прокрутку страницы для загрузки всех элементов.
        Извлекает ссылки на товары, используя локатор `product_links`.
        Проверяет наличие товаров в базе данных магазина PrestaShop (закомментировано).

    Примеры:
        Пример вызова функции:
        >>> s = Supplier()  #  Предположим, что у вас есть экземпляр класса Supplier
        >>> product_urls = get_list_products_in_category(s)
        >>> if product_urls:
        ...     print(f"Найдено {len(product_urls)} товаров")
        ... else:
        ...     print("Список товаров не получен")
    """
    d = s.driver
    l: dict = s.locators['category']
    if not l:
        """ Много проверок, потому, что код можно запускать от лица разных ихполнителей: Supplier, Product, Scenario """
        logger.error(f"А где локаторы? {l}")
        return
    d.scroll()

    #TODO: Нет листалки

    list_products_in_category = d.execute_locator(l['product_links'])
    """ Собираю ссылки на товары.  """
    if not list_products_in_category:
        logger.warning('Нет ссылок на товары')
        return
    
    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category


    logger.info(f""" Найдено {len(list_products_in_category)} товаров """)
    
    #""" Проверяю наличие товара в базе данных магазина """
    #for asin in list_products_in_category:
    #    _asin = asin.split(f\'\'\'/\'\'\')[-2]
    #    _sku = f\'\'\'{s.supplier_id}_{_asin}\'\'\' 
    #    if PrestaShopProduct.check(_sku) == False:\n
    #        """ Синтаксис для того, чтобы помнить,\n
    #        что я проверяю ОТСУТСТВИЕ товара в базе данных\n
    #        """
    #        continue
    #    else:
    #        """ Товар в базе данных """
    #        continue
            #TODO: Логику