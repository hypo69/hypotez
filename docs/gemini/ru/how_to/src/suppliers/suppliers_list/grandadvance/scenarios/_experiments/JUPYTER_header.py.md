## Как использовать блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода инициализирует рабочую среду для работы с поставщиками. Он настраивает пути к необходимым файлам и модулям, а также импортирует необходимые классы и функции для дальнейшей работы. 

Шаги выполнения
-------------------------
1. **Определение корневого каталога проекта**:
    - Используется переменная `dir_root` для определения корневого каталога проекта `hypotez`. 
    - `os.getcwd()` возвращает текущий каталог, а `os.getcwd()[:os.getcwd().rfind('hypotez')+7]` ищет в текущем каталоге слово "hypotez" и возвращает путь до него, добавляя 7 символов (длина слова "hypotez" + 1).
2. **Добавление корневого каталога в `sys.path`**: 
    - `sys.path.append(str(dir_root))` добавляет корневой каталог проекта в список путей, где Python будет искать импортируемые модули.
3. **Определение каталога `src`**:
    - `dir_src = Path(dir_root, 'src')` создает объект `Path` (путь к файлу), который указывает на каталог `src` внутри корневого каталога проекта.
4. **Добавление каталога `src` в `sys.path`**:
    - `sys.path.append(str(dir_root))` добавляет каталог `src` в список путей, где Python будет искать импортируемые модули.
5. **Импорт необходимых модулей**: 
    - `from pathlib import Path` импортирует модуль `Path` для работы с путями к файлам.
    - `import json` импортирует модуль `json` для работы с JSON-файлами.
    - `import re` импортирует модуль `re` для работы с регулярными выражениями.
    - `from src.webdriver.driver import Driver` импортирует класс `Driver` из модуля `driver` в каталоге `src/webdriver`.
    - `from src.product import Product, ProductFields` импортирует класс `Product` и `ProductFields` из модуля `product` в каталоге `src`.
    - `from src.category import Category` импортирует класс `Category` из модуля `category` в каталоге `src`.
    - `from src.utils import StringFormatter, StringNormalizer` импортирует классы `StringFormatter` и `StringNormalizer` из модуля `utils` в каталоге `src`.
    - `from src.utils.printer import pprint` импортирует функцию `pprint` из модуля `printer` в каталоге `src/utils`.
    - `from src.endpoints.PrestaShop import Product as PrestaProduct` импортирует класс `Product` как `PrestaProduct` из модуля `PrestaShop` в каталоге `src/endpoints`.
    - `from src.utils.file.text_file import save_text_file` импортирует функцию `save_text_file` из модуля `text_file` в каталоге `src/utils/file`.
6. **Определение функции `start_supplier`**:
    - Функция `start_supplier` принимает два параметра: 
        - `supplier_prefix` (строка): префикс имени поставщика, по умолчанию "aliexpress".
        - `locale` (строка): язык, по умолчанию "en".
    - Функция создает словарь `params` с ключами `supplier_prefix` и `locale`, в который записывает переданные значения параметров.
    - Функция возвращает объект `Supplier` (имя класса не указано, предположительно, он должен быть импортирован из другого модуля), инициализированный с помощью словаря `params`.

Пример использования
-------------------------

```python
    # Запуск поставщика "aliexpress" на английском языке
    supplier = start_supplier(supplier_prefix='aliexpress', locale='en') 
```