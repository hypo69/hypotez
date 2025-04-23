# Модуль `web_login.py`

## Обзор

Модуль `web_login.py` предназначен для экспериментов с автоматическим логином на сайт AliExpress, сохранения и восстановления cookies.

## Подробней

Модуль содержит код для автоматизации входа на сайт AliExpress, а также для работы с cookies. В частности, он демонстрирует, как можно получить, сохранить и восстановить cookies для автоматического входа в систему.

## Классы

### `Supplier`

**Описание**: Класс Supplier предназначен для представления поставщика, в данном случае AliExpress.
**Наследует**:

**Атрибуты**:

**Методы**:
- `__init__(self, name: str)`: Инициализирует объект Supplier с указанным именем.

```python
class Supplier:
    """ Класс для представления поставщика.
    Args:
        name (str): Имя поставщика.
    """

    def __init__(self, name: str):
        """Инициализирует объект Supplier с указанным именем.

        Args:
            name (str): Имя поставщика.
        """
        ...
```

## Переменные

- `a`: Экземпляр класса `Supplier` с именем 'aliexpress'.
- `d`: Драйвер, полученный из экземпляра класса `Supplier`.

## Код

```python
import header
from pathlib import Path
import pickle
import requests

from src import gs

from src.utils.printer import pprint

a = Supplier('aliexpress')

d = a.driver
d.get_url('https://aliexpress.com')
```

**Объяснение работы кода**:

1.  Импортируются необходимые библиотеки, такие как `header`, `pathlib`, `pickle`, `requests`, `gs` и `pprint` (из `src.utils.printer`).
2.  Создается экземпляр класса `Supplier` с именем 'aliexpress' и присваивается переменной `a`.
3.  Извлекается драйвер из экземпляра `a` и присваивается переменной `d`.
4.  Используется метод `get_url` драйвера `d` для открытия страницы 'https://aliexpress.com'.