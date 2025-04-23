### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category` извлекает список URL-адресов товаров со страницы категории, обеспечивая прокрутку страницы при необходимости. Функция `paginator` отвечает за перелистывание страниц, если на странице категории присутствует пагинация. Функция `build_list_categories_from_site` отвечает за сбор актуальных категорий с сайта.

Шаги выполнения
-------------------------
1. **Функция `get_list_products_in_category`**:
   - Получает объект `Driver` и `SimpleNamespace` с данными о странице категории.
   - Ожидает 1 секунду и прокручивает страницу.
   - Извлекает список URL-адресов товаров, используя локатор `l.product_links`.
   - Проверяет, найдены ли ссылки на товары. Если нет, логирует предупреждение и возвращает `None`.
   - Если `d.current_url` не равно `d.previous_url`, вызывает функцию `paginator` для перелистывания страниц.
   - Добавляет новые URL-адреса товаров в список `list_products_in_category`.
   - Преобразует `list_products_in_category` в список, если это строка.
   - Логирует количество найденных товаров и возвращает список URL-адресов товаров.

2. **Функция `paginator`**:
   - Получает объект `Driver`, `locator` с данными о пагинации и список URL-адресов товаров.
   - Выполняет клик на элементе пагинации, используя локатор `locator.pagination.__dict__['<-']`.
   - Проверяет, был ли получен ответ и не является ли он пустым списком. Если нет, возвращает `None`.
   - Возвращает `True`, если перелистывание выполнено успешно.

3. **Функция `build_list_categories_from_site`**:
   - Собирает актуальные категории с сайта.

Пример использования
-------------------------

```python
import asyncio
from types import SimpleNamespace
from typing import List

from src.webdriver.driver import Driver
from src.logger.logger import logger


async def get_list_products_in_category(d: Driver, l: SimpleNamespace) -> List[str]:
    """
    Функция извлекает список URL-адресов товаров со страницы категории.

    Args:
        d (Driver): Объект веб-драйвера.
        l (SimpleNamespace): Объект с данными о странице категории.

    Returns:
        List[str]: Список URL-адресов товаров.
    """

    d.wait(1)
    d.scroll()

    list_products_in_category: List[str] = await d.execute_locator(l.product_links)

    if not list_products_in_category:
        logger.warning('Нет ссылок на товары. Так бывает')
        return []

    while d.current_url != d.previous_url:
        if await paginator(d, l, list_products_in_category):
            new_products = await d.execute_locator(l.product_links)
            if isinstance(new_products, list):
                list_products_in_category.extend(new_products)
            elif isinstance(new_products, str):
                list_products_in_category.append(new_products)
        else:
            break

    logger.debug(f"Found {len(list_products_in_category)} items")
    return list_products_in_category


async def paginator(d: Driver, locator: SimpleNamespace, list_products_in_category: List[str]) -> bool:
    """
    Функция для перелистывания страниц.

    Args:
        d (Driver): Объект веб-драйвера.
        locator (SimpleNamespace): Объект с данными о пагинации.
        list_products_in_category (List[str]): Список URL-адресов товаров.

    Returns:
        bool: True, если перелистывание выполнено успешно, иначе False.
    """
    response = await d.execute_locator(locator.pagination.__dict__['<-'])
    if not response or (isinstance(response, list) and len(response) == 0):
        return False
    return True


def build_list_categories_from_site(s):
    """
    Функция для сборки актуальных категорий с сайта.

    Args:
        s: Объект с данными о сайте.
    """
    # Функция выполняет сбор актуальных категорий с сайта
    ...


async def main():
    """Пример использования функций."""
    class Config:
        product_links = SimpleNamespace(
            by="css",
            selector="a.product-link",
            attribute="href"
        )
        pagination = SimpleNamespace(
            **{'<-': SimpleNamespace(
                by="css",
                selector="a.next-page",
                attribute="href"
            )}
        )
    # Инициализация веб-драйвера (пример)
    driver = Driver(browser='chrome')
    driver.get("https://hb.co.il/category/some-category")
    # Создание объекта SimpleNamespace с данными о странице категории (пример)
    l = Config()

    # Получение списка товаров
    products = await get_list_products_in_category(driver, l)
    if products:
        print(f"Found {len(products)} products:")
        for product_url in products:
            print(product_url)
    else:
        print("No products found in category.")

    # Закрытие веб-драйвера
    await driver.close()

if __name__ == "__main__":
    asyncio.run(main())
```