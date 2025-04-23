### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Graber`, который предназначен для сбора данных о товарах с веб-сайта Ebay. Класс наследуется от базового класса `Graber` (Grbr) из модуля `src.suppliers.graber` и предоставляет методы для обработки различных полей товара на странице Ebay. Также, в классе задается префикс поставщика (`supplier_prefix`) для Ebay.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются необходимые модули, такие как `typing`, `SimpleNamespace`, `header`, `Graber` (как `Grbr`), `Config`, `close_pop_up` и `logger`.
2. **Определение класса `Graber`**: Создается класс `Graber`, который наследуется от `Grbr`. Этот класс предназначен для сбора данных о товарах с Ebay.
3. **Инициализация класса**: В методе `__init__` класса `Graber` устанавливается префикс поставщика (`supplier_prefix`) как `'ebay'`, вызывается конструктор родительского класса с указанием префикса поставщика, драйвера и индекса языка.
4. **Декоратор `close_pop_up`**: В классе `Graber` можно использовать декоратор `@close_pop_up` для закрытия всплывающих окон перед выполнением основной логики функции.
5. **Использование декоратора**: Если необходимо выполнить предварительные действия перед отправкой запроса к вебдрайверу, можно установить значение `Config.locator_for_decorator`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.ebay.graber import Graber
from src.webdriver import Driver, Firefox
from src.logger.logger import logger
from typing import Optional

# Пример использования класса Graber
def grab_ebay_data(url: str, lang_index: Optional[int] = 0) -> None:
    """
    Функция для сбора данных о товаре с Ebay.

    Args:
        url (str): URL страницы товара на Ebay.
        lang_index (Optional[int]): Индекс языка (по умолчанию 0).

    Returns:
        None: Функция ничего не возвращает, но логирует информацию о процессе.
    """
    try:
        # Инициализация драйвера
        driver = Driver(browser=Firefox)

        # Создание экземпляра класса Graber для Ebay
        ebay_graber = Graber(driver=driver, lang_index=lang_index)

        # Открытие страницы товара
        driver.get(url)

        # Пример: Получение наименования товара (если метод get_title реализован)
        title = ebay_graber.get_title()
        logger.info(f"Наименование товара: {title}")

        # Закрытие драйвера
        driver.quit()

    except Exception as e:
        logger.error(f"Произошла ошибка при сборе данных с Ebay: {e}")

# Пример вызова функции
if __name__ == '__main__':
    ebay_url = "https://www.ebay.com/itm/example"  # Замените на реальный URL товара
    grab_ebay_data(ebay_url)