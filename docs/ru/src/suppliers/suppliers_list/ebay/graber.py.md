# Модуль `graber.py` для сбора данных о товарах с Ebay

## Обзор

Модуль содержит класс `Graber`, предназначенный для сбора информации о товарах с веб-сайта Ebay. Он наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

## Подробней

Этот модуль является частью системы сбора данных о товарах от различных поставщиков в проекте `hypotez`. Он специализируется на извлечении информации с сайта Ebay. Класс `Graber` содержит логику для взаимодействия с веб-страницами Ebay и извлечения необходимых данных о товарах.

Для каждого поля страницы товара создана функция обработки поля в родительском `Graber`. Если нужна нестандартная обработка, можно перегрузить метод здесь, в этом классе.

Перед отправкой запроса к веб-драйверу можно совершить предварительные действия через декоратор. Декоратор по умолчанию находится в родительском классе. Для того чтобы декоратор сработал, нужно передать значение в `Context.locator`. Вы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода.

## Классы

### `Graber`

**Описание**: Класс `Graber` предназначен для сбора данных о товарах с сайта Ebay.

**Наследует**: `Graber` наследует класс `src.suppliers.graber.Graber`.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика, используется для идентификации Ebay как поставщика.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Graber`, устанавливает префикс поставщика и вызывает конструктор родительского класса.

#### `__init__`

```python
def __init__(self, driver: Optional['Driver'] = None, lang_index: Optional[int] = None):
    """Инициализация класса сбора полей товара."""
    ...
```

**Назначение**: Инициализирует новый экземпляр класса `Graber`.

**Параметры**:
- `driver` (Optional['Driver'], optional): Драйвер веб-браузера для управления браузером. По умолчанию `None`.
- `lang_index` (Optional[int], optional): Индекс языка. По умолчанию `None`.

**Как работает функция**:
- Устанавливает атрибут `supplier_prefix` в значение 'ebay', чтобы обозначить, что этот грабер работает с Ebay.
- Вызывает конструктор родительского класса `Graber` (из `src.suppliers.graber`) с указанным префиксом поставщика, драйвером и индексом языка.
- Устанавливает `Config.locator_for_decorator` в `None`. Если установить значение, оно выполнится в декораторе `@close_pop_up`.

**Примеры**:

```python
# Пример создания экземпляра класса Graber
graber = Graber()
```
```python
# Пример создания экземпляра класса Graber с указанием драйвера и индекса языка
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)
graber = Graber(driver=driver, lang_index=1)
```
```python
## \\file /src/suppliers/suppliers_list/ebay/graber.py
# -*- coding: utf-8 -*-\n\n#! .pyenv/bin/python3\n\n\"\"\" Модуль для сбора данных о товарах с Ebay.\n=========================================================================================\n\nМодуль содержит класс :class:`Graber`, который используется для сбора данных о товарах\nс веб-сайта `bangood.com`. Он наследуется от базового класса :class:`src.suppliers.graber.Graber`.\n\nКласс `Graber` предоставляет методы для обработки различных полей товара на странице.\nВ случае необходимости нестандартной обработки поля, метод может быть переопределен.\n\nДля каждого поля страницы товара сделана функция обработки поля в родительском `Graber`.\nЕсли нужна нестандертная обработка, можно перегрузить метод здесь, в этом классе.\n------------------\nПеред отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. \nДекоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение \nв `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение.\nВы также можете реализовать свой собственный декоратор, раскомментировав соответствующие строки кода\n\n```rst\n.. module:: src.suppliers.suppliers_list.ebay\n\"\"\"\n\n\nfrom typing import Optional, Any\nfrom types import SimpleNamespace\nimport header\nfrom src.suppliers.graber import Graber as Grbr, Config, close_pop_up\nfrom src.logger.logger import logger\n\n\n#\n#\n#           DECORATOR TEMPLATE. \n#\n# def close_pop_up(value: Any = None) -> Callable:\n#     \"\"\"Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.\n\n#     Args:\n#         value (Any): Дополнительное значение для декоратора.\n\n#     Returns:\n#         Callable: Декоратор, оборачивающий функцию.\n#     \"\"\"\n#     def decorator(func: Callable) -> Callable:\n#         @wraps(func)\n#         async def wrapper(*args, **kwargs):\n#             try:\n#                 # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close  \n#                 ... \n#             except ExecuteLocatorException as e:\n#                 logger.debug(f\'Ошибка выполнения локатора: {e}\')\n#             return await func(*args, **kwargs)  # Await the main function\n#         return wrapper\n#     return decorator\n\nclass Graber(Grbr):\n    \"\"\"Класс для операций захвата Morlevi.\"\"\"\n    supplier_prefix: str\n\n    def __init__(self, driver: Optional[\'Driver\'] = None, lang_index:Optional[int] = None):\n        \"\"\"Инициализация класса сбора полей товара.\"\"\"\n        self.supplier_prefix = \'ebay\'\n        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)\n        # Устанавливаем глобальные настройки через Context\n        \n        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`\n