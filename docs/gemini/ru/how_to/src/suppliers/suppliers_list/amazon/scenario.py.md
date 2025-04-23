### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код извлекает список URL-адресов товаров со страницы категории на сайте Amazon. Сначала он прокручивает страницу для загрузки всего контента, затем извлекает ссылки на товары с использованием заданного локатора. Если ссылки не найдены, регистрируется предупреждение. В конце возвращается список URL-адресов товаров.

Шаги выполнения
-------------------------
1. **Прокрутка страницы**:
   - Функция `d.scroll()` выполняет прокрутку страницы, чтобы гарантировать загрузку всех элементов, включая ссылки на товары. Это необходимо для динамически загружаемых страниц.

2. **Извлечение ссылок на товары**:
   - Функция `d.execute_locator(l['product_links'])` использует локатор `product_links` для поиска и извлечения всех ссылок на товары на странице. Результат сохраняется в переменной `list_products_in_category`.
   - Если `list_products_in_category` является строкой, она преобразуется в список, содержащий только эту строку.

3. **Проверка наличия ссылок**:
   - Проверяется, найдены ли ссылки на товары. Если `list_products_in_category` пуст, в лог записывается предупреждение `'Нет ссылок на товары'`, и функция возвращает `None`.

4. **Логирование количества найденных товаров**:
   - Если ссылки найдены, в лог записывается информационное сообщение с количеством найденных товаров: `logger.info(f"Найдено {len(list_products_in_category)} товаров")`.

5. **Возврат списка ссылок**:
   - Функция возвращает список URL-адресов товаров `list_products_in_category`.

Пример использования
-------------------------

```python
from src.webdriver import Driver
from src.logger.logger import logger

async def get_list_products_in_category(d:'Driver', l:dict) -> list[str,str,None]:    
    """ Returns list of products urls from category page
    Если надо пролистстать - страницы категорий - листаю ??????

    Attrs:
    @param s: Supplier - Supplier intstance
    @returns list or one of products urls or None
    """

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
    #    _asin = asin.split(f'''/''')[-2]
    #    _sku = f'''{s.supplier_id}_{_asin}''' 
    #    if PrestaShopProduct.check(_sku) == False:
    #        """ Синтаксис для того, чтобы помнить,
    #        что я проверяю ОТСУТСТВИЕ товара в базе данных
    #        """
    #        continue
    #    else:
    #        """ Товар в базе данных """
    #        continue
            #TODO: Логику 


    return list_products_in_category

# Пример вызова функции
async def main():
    driver = Driver("chrome")  # Инициализация веб-драйвера
    locator = {'product_links': {'by': 'css', 'selector': '.product-link', 'attribute': 'href'}}  # Пример локатора
    products = await get_list_products_in_category(driver, locator)

    if products:
        print(f"Найдено {len(products)} товаров.")
        for product_url in products:
            print(product_url)
    else:
        print("Товары не найдены.")

    await driver.close()

# Запуск примера
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())