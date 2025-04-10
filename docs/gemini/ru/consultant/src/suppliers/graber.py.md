### **Анализ кода модуля `graber.py`**

## \file /src/suppliers/graber.py

Модуль грабера. Собирает информацию с вестраницы товара
=========================================================

Базовый класс сбора данных со старницы HTML поставщиков.
   Целевые поля страницы (`название`,`описание`,`спецификация`,`артикул`,`цена`,...) собирает вебдрйвер (class: [`Driver`](../webdriver))
   Местополжение поля определяется его локатором. Локаторы хранятся в словарях JSON в директории `locators` каждого поставщика.
   ([подробно о локаторах](locators.ru.md))
    Таблица поставщиков:
             https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526

Для нестендартной обработки полей товара просто переопределите функцию в своем классе.
Пример:

```python
s = `suppler_prefix`
from src.suppliers imoprt Graber
locator = j_loads(gs.path.src.suppliers / f{s} / 'locators' / 'product.json`)

class G(Graber):

   @close_pop_up()
   async def name(self, value:Optional[Any] = None):
       self.fields.name = <Ваша реализация>
       )
```
```rst
.. module:: src.suppliers 
``` 

Список полей: https://github.com/hypo69/hypotez/blob/master/src/endpoints/prestashop/product_fields/fields_list.txt

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая организация кода в виде класса `Graber` с асинхронными методами для получения данных.
  - Использование декоратора `@close_pop_up` для обработки всплывающих окон.
  - Логирование ошибок с использованием `logger.error`.
  - Применение нормализации данных с использованием функций из `src.utils.string.normalizer`.
- **Минусы**:
  - Не везде есть аннотации типов для переменных и возвращаемых значений.
  - Используется `Any` для типов, которые можно уточнить.
  - В некоторых местах отсутствует документация или она не полная.
  - Встречаются конструкции `value or await ... or ''`, которые можно упростить.
  - Много мест с `...` внутри блоков `try-except`, что указывает на необходимость доработки обработки ошибок.

**Рекомендации по улучшению**:
1. **Добавить документацию**:
   - Дополнить docstring для всех функций и методов, особенно для тех, где они отсутствуют или не полные.

2. **Улучшить аннотации типов**:
   - Заменить `Any` на более конкретные типы, где это возможно.
   - Добавить аннотации типов для всех переменных.

3. **Улучшить обработку ошибок**:
   - Заменить `...` в блоках `try-except` на конкретную логику обработки ошибок или логирование.
   - Добавить больше контекста в сообщения об ошибках, чтобы облегчить отладку.

4. **Упростить код**:
   - Избавиться от лишних конструкций `value or await ... or ''`, используя более читаемые способы присваивания значений по умолчанию.

5. **Добавить больше комментариев**:
   - Добавить комментарии для сложных участков кода, чтобы улучшить понимание логики.

6. **Унифицировать стиль кода**:
   - Проверить и исправить все места, где не соблюдены стандарты PEP8.

**Оптимизированный код**:

```python
## \file /src/suppliers/graber.py
# -*- coding: utf-8 -*-\n#! .pyenv/bin/python3

"""
Модуль грабера. Собирает информацию с веб-страницы товара
=========================================================
Базовый класс для сбора данных со страниц HTML поставщиков.
Целевые поля страницы (`название`, `описание`, `спецификация`, `артикул`, `цена` и т.д.) собираются веб-драйвером (class: [`Driver`](../webdriver)).
Местоположение поля определяется его локатором. Локаторы хранятся в словарях JSON в директории `locators` каждого поставщика.
([подробно о локаторах](locators.ru.md))

Таблица поставщиков:
https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526

Для нестандартной обработки полей товара просто переопределите функцию в своем классе.

Пример:
```python
s = 'suppler_prefix'
from src.suppliers import Graber
locator = j_loads(gs.path.src.suppliers / f'{s}' / 'locators' / 'product.json')

class G(Graber):

   @close_pop_up()
   async def name(self, value: Optional[Any] = None):
       self.fields.name = <Ваша реализация>
```
"""

import datetime
import asyncio
from pathlib import Path
from typing import Optional, Any, Callable, List
from types import SimpleNamespace
from functools import wraps

from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.image import save_image_async, save_image_from_url_async
from src.utils.string.normalizer import (
    normalize_string,
    normalize_int,
    normalize_float,
    normalize_sql_date,
    normalize_sku
)
from src.logger.exceptions import ExecuteLocatorException
from src.logger.logger import logger


class Context:
    """
    Класс для хранения глобальных настроек.

    Attributes:
        driver (Optional['Driver']): Объект драйвера для управления браузером.
        locator_for_decorator (Optional[SimpleNamespace]): Локатор для декоратора `@close_pop_up`.
            Устанавливается при инициализации поставщика, например: `Context.locator = self.locator.close_pop_up`.
        supplier_prefix (Optional[str]): Префикс поставщика.

    Example:
        >>> context = Context()
        >>> context.supplier_prefix = 'prefix'
        >>> print(context.supplier_prefix)
        prefix
    """
    driver: Optional['Driver'] = None
    locator_for_decorator: Optional[SimpleNamespace] = None
    supplier_prefix: Optional[str] = None


def close_pop_up() -> Callable:
    """
    Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

    Функция `driver.execute_locator()` будет вызвана, только если был указан `Context.locator_for_decorator` при инициализации экземпляра класса.

    Args:
        value ('Driver'): Дополнительное значение для декоратора.

    Returns:
        Callable: Декоратор, оборачивающий функцию.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if Context.locator_for_decorator:
                try:
                    # Закрываем всплывающее окно, если локатор установлен
                    await Context.driver.execute_locator(Context.locator_for_decorator)
                except ExecuteLocatorException as ex:
                    logger.debug('Ошибка выполнения локатора:', ex, False)
                finally:
                    # Сбрасываем локатор после первого срабатывания
                    Context.locator_for_decorator = None

            # Вызываем основную функцию
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class Graber:
    """Базовый класс для сбора данных со страницы для всех поставщиков."""

    def __init__(self, supplier_prefix: str, lang_index: int, driver: 'Driver'):
        """
        Инициализация класса Graber.

        Args:
            supplier_prefix (str): Префикс поставщика.
            lang_index (int): Индекс языка.
            driver ('Driver'): Экземпляр класса Driver.
        """
        self.supplier_prefix: str = supplier_prefix
        self.locator: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_prefix / 'locators' / 'product.json')
        self.driver: 'Driver' = driver
        self.fields: ProductFields = ProductFields(lang_index)
        Context.driver = self.driver
        Context.supplier_prefix = None
        Context.locator_for_decorator = None
        # Если будет установлен локатор в Context.locator_for_decorator - выполнится декоратор `@close_pop_up`

    async def error(self, field: str) -> None:
        """Обработчик ошибок для полей."""
        logger.debug(f'Ошибка заполнения поля {field}')

    async def set_field_value(
        self,
        value: Any,
        locator_func: Callable[[], Any],
        field_name: str,
        default: Any = ''
    ) -> Any:
        """
        Универсальная функция для установки значений полей с обработкой ошибок.

        Args:
            value (Any): Значение для установки.
            locator_func (Callable[[], Any]): Функция для получения значения из локатора.
            field_name (str): Название поля.
            default (Any): Значение по умолчанию. По умолчанию пустая строка.

        Returns:
            Any: Установленное значение.
        """
        locator_result: Any = await asyncio.to_thread(locator_func)
        if value:
            return value
        if locator_result:
            return locator_result
        await self.error(field_name)
        return default

    def grab_page(self, *args: Any, **kwargs: Any) -> ProductFields:
        """Запускает асинхронный сбор данных."""
        return asyncio.run(self.grab_page_async(*args, **kwargs))

    async def grab_page_async(self, *args: Any, **kwargs: Any) -> ProductFields:
        """Асинхронная функция для сбора полей продукта."""
        async def fetch_all_data(*args: Any, **kwargs: Any) -> None:
            """Динамический вызов функций для каждого поля из args."""
            if not args:  # Если по какой-то причине не были переданы имена полей для сбора информации
                args: List[str] = ['id_product', 'name', 'description_short', 'description', 'specification', 'local_image_path']
            for filed_name in args:
                function: Callable = getattr(self, filed_name, None)
                if function:
                    # Вызываем асинхронно функцию для сбора данных
                    await function(kwargs.get(filed_name, ''))

        await fetch_all_data(*args, **kwargs)
        return self.fields

    @close_pop_up()
    async def additional_shipping_cost(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает дополнительную стоимость доставки.

        Args:
            value (Any, optional): Значение, переданное через kwargs (additional_shipping_cost). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.additional_shipping_cost)
            self.fields.additional_shipping_cost = normalize_string(value or locator_value or '')

            if not self.fields.additional_shipping_cost:
                logger.error('Поле `additional_shipping_cost` не получило значения')
                return None

            return True
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `additional_shipping_cost`', ex, exc_info=True)
            return None

    @close_pop_up()
    async def delivery_in_stock(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус доставки в наличии.

        Args:
            value (Any, optional): Значение, переданное через kwargs (delivery_in_stock). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.delivery_in_stock)
            self.fields.delivery_in_stock = normalize_string(value or locator_value or '')

            if not self.fields.delivery_in_stock:
                logger.error('Поле `delivery_in_stock` не получило значения')
                return None
            return True
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `delivery_in_stock`', ex, exc_info=True)
            return None

    @close_pop_up()
    async def active(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус активности.

        Args:
            value (Any, optional): Значение, переданное через kwargs (active). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.active)
            self.fields.active = normalize_int(value or locator_value or 1)

            if not self.fields.active:
                return None
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `active`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.active}')
            return None

        # Записываем результат в поле `active` объекта `ProductFields`
        self.fields.active = value
        return True

    @close_pop_up()
    async def additional_delivery_times(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает дополнительное время доставки.

        Args:
            value (Any, optional): Значение, переданное через kwargs (additional_delivery_times). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.additional_delivery_times)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `additional_delivery_times`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.additional_delivery_times}')
            return None

        # Записываем результат в поле `additional_delivery_times` объекта `ProductFields`
        self.fields.additional_delivery_times = value
        return True

    @close_pop_up()
    async def advanced_stock_management(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус расширенного управления складом.

        Args:
            value (Any, optional): Значение, переданное через kwargs (advanced_stock_management). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.advanced_stock_management)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `advanced_stock_management`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.advanced_stock_management}')
            return None

        # Записываем результат в поле `advanced_stock_management` объекта `ProductFields`
        self.fields.advanced_stock_management = value
        return True

    @close_pop_up()
    async def affiliate_short_link(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает короткую ссылку филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_short_link). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.affiliate_short_link)
            self.fields.affiliate_short_link = value or locator_value or ''
            return True
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_short_link`', ex, exc_info=True)
            return None

    @close_pop_up()
    async def affiliate_summary(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает сводку филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_summary). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.affiliate_summary)
            self.fields.affiliate_summary = normalize_string(value or locator_value or '')
            return True
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_summary`', ex, exc_info=True)
            return None

    @close_pop_up()
    async def affiliate_summary_2(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает сводку филиала 2.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_summary_2). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.affiliate_summary_2)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_summary_2`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.affiliate_summary_2}')
            return None

        # Записываем результат в поле `affiliate_summary_2` объекта `ProductFields`
        self.fields.affiliate_summary_2 = value
        return True

    @close_pop_up()
    async def affiliate_text(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает текст филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_text). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.affiliate_text)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_text`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.affiliate_text}')
            return None

        # Записываем результат в поле `affiliate_text` объекта `ProductFields`
        self.fields.affiliate_text = value
        return True

    @close_pop_up()
    async def affiliate_image_large(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает большое изображение филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_image_large). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.affiliate_image_large)
            self.fields.affiliate_image_large = value or locator_value or ''
            return True
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_image_large`', ex, exc_info=True)
            return None

    @close_pop_up()
    async def affiliate_image_medium(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает среднее изображение филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_image_medium). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_result: Any = await self.driver.execute_locator(self.locator.affiliate_image_medium)
            locator_result = value or locator_result or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_image_medium`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not locator_result:
            logger.debug(f'Невалидный результат {locator_result=}')
            return None

        # Записываем результат в поле `affiliate_image_medium` объекта `ProductFields`
        self.fields.affiliate_image_medium = locator_result
        return True

    @close_pop_up()
    async def affiliate_image_small(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает маленькое изображение филиала.

        Args:
            value (Any, optional): Значение, переданное через kwargs (affiliate_image_small). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_result: Any = await self.driver.execute_locator(self.locator.affiliate_image_small)
            locator_result = value or locator_result or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `affiliate_image_small`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not locator_result:
            logger.debug(f'Невалидный результат {locator_result=}')
            return None

        # Записываем результат в поле `affiliate_image_small` объекта `ProductFields`
        self.fields.affiliate_image_small = locator_result
        return True

    @close_pop_up()
    async def available_date(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает дату доступности.

        Args:
            value (Any, optional): Значение, переданное через kwargs (available_date). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_result: Any = await self.driver.execute_locator(self.locator.available_date)
            locator_result = value or locator_result or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `available_date`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not locator_result:
            logger.debug(f'Невалидный результат {locator_result=}')
            return None

        # Записываем результат в поле `available_date` объекта `ProductFields`
        self.fields.available_date = locator_result
        return True

    @close_pop_up()
    async def available_for_order(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "доступно для заказа".

        Args:
            value (Any, optional): Значение, переданное через kwargs (available_for_order). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.available_for_order)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `available_for_order`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.available_for_order}')
            return None

        # Записываем результат в поле `available_for_order` объекта `ProductFields`
        self.fields.available_for_order = value
        return True

    @close_pop_up()
    async def available_later(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "доступно позже".

        Args:
            value (Any, optional): Значение, переданное через kwargs (available_later). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.available_later)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `available_later`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.available_later}')
            return None

        # Записываем результат в поле `available_later` объекта `ProductFields`
        self.fields.available_later = value
        return True

    @close_pop_up()
    async def available_now(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "доступно сейчас".

        Args:
            value (Any, optional): Значение, переданное через kwargs (available_now). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.available_now)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `available_now`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.available_now}')
            return None

        # Записываем результат в поле `available_now` объекта `ProductFields`
        self.fields.available_now = value
        return True

    @close_pop_up()
    async def additional_categories(self, value: Optional[str | list] = None) -> dict:
        """
        Устанавливает дополнительные категории.

        Args:
            value (str | list, optional): Строка или список категорий. Defaults to None.

        Returns:
            dict: Словарь с ID категорий.
        """
        self.fields.additional_categories = value or ''
        return {'additional_categories': self.fields.additional_categories}

    @close_pop_up()
    async def cache_default_attribute(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает атрибут кэша по умолчанию.

        Args:
            value (Any, optional): Значение, переданное через kwargs (cache_default_attribute). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.cache_default_attribute)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `cache_default_attribute`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.cache_default_attribute}')
            return None

        # Записываем результат в поле `cache_default_attribute` объекта `ProductFields`
        self.fields.cache_default_attribute = value
        return True

    @close_pop_up()
    async def cache_has_attachments(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "кэш имеет вложения".

        Args:
            value (Any, optional): Значение, переданное через kwargs (cache_has_attachments). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.cache_has_attachments)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `cache_has_attachments`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.cache_has_attachments}')
            return None

        # Записываем результат в поле `cache_has_attachments` объекта `ProductFields`
        self.fields.cache_has_attachments = value
        return True

    @close_pop_up()
    async def cache_is_pack(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "кэш - это набор".

        Args:
            value (Any, optional): Значение, переданное через kwargs (cache_is_pack). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.cache_is_pack)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `cache_is_pack`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.cache_is_pack}')
            return None

        # Записываем результат в поле `cache_is_pack` объекта `ProductFields`
        self.fields.cache_is_pack = value
        return True

    @close_pop_up()
    async def condition(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает условие продукта.

        Args:
            value (Any, optional): Значение, переданное через kwargs (condition). Defaults to None.

        Returns:
            Optional[bool]: True в случае успеха, None в случае ошибки.
        """
        try:
            # Получаем значение через execute_locator
            locator_value: Any = await self.driver.execute_locator(self.locator.condition)
            value = value or locator_value or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `condition`', ex, exc_info=True)
            return None

        # Проверка валидности `value`
        if not value:
            logger.debug(f'Невалидный результат {value=}\nлокатор {self.locator.condition}')
            return None

        # Записываем результат в поле `condition` объекта `ProductFields`
        self.fields.condition = value
        return True

    @close_pop_up()
    async def customizable(self, value: Optional[Any] = None) -> Optional[bool]:
        """
        Извлекает и устанавливает статус "настраиваемый".

        Args:
            value (Any, optional): Значение, пере