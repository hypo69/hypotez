### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category` считывает URL товаров со страницы категории на сайте Aliexpress. Если в категории несколько страниц, функция переходит по ним и собирает все URL товаров. Вебдрайвер должен быть предварительно настроен и открыт на странице категории.

Шаги выполнения
-------------------------
1. Функция `get_list_products_in_category` принимает экземпляр класса `Supplier` в качестве аргумента.
2. Вызывается функция `get_prod_urls_from_pagination(s)` для сбора URL товаров с перелистыванием страниц.
3. Функция `get_prod_urls_from_pagination` извлекает локаторы для ссылок на товары и пагинации из объекта поставщика (`s.locators['category']['product_links']` и `s.locators['category']['pagination']['->']`).
4. Функция `_d.execute_locator(_l)` исполняет локатор для получения списка URL товаров с текущей страницы.
5. Если список URL пуст, функция возвращает пустой список (это нормально, если в категории нет товаров).
6. Если список URL не пуст, начинается цикл перелистывания страниц.
7. На каждой итерации цикла функция пытается нажать на кнопку "следующая страница" (`_d.execute_locator(s.locators['category']['pagination']['->'])`).
8. Если кнопки "следующая страница" нет, цикл завершается.
9. На каждой странице собираются URL товаров, которые добавляются к общему списку `list_products_in_category`.
10. Функция возвращает список собранных URL товаров.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.scenario import get_list_products_in_category
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome
from src import config

# Инициализация вебдрайвера и открытие страницы категории
driver = Driver(Chrome)
driver.get_url("https://aliexpress.ru/category/123456/some-category.html")

# Создание экземпляра поставщика
supplier = Supplier(driver=driver, config=config,locators={
        'category': {
            'product_links': {
                'by': 'XPATH',
                'selector': '//a[@class="product-url"]',
            },
            'pagination': {
                '->': {
                    'by': 'XPATH',
                    'selector': '//a[@class="next-page"]',
                }
            }
        }
    })

# Получение списка URL товаров
list_products = get_list_products_in_category(supplier)

# Вывод списка URL товаров
if list_products:
    for url in list_products:
        print(url)
else:
    print("В категории нет товаров.")

driver.quit()
```
```markdown
### **Как использовать функцию `update_categories_in_scenario_file`**

=========================================================================================

Описание
-------------------------
Функция `update_categories_in_scenario_file` проверяет и обновляет информацию о категориях в файле сценария на основе данных, полученных с сайта Aliexpress. Она сравнивает список идентификаторов категорий, хранящихся в файле сценария, со списком идентификаторов, полученных с сайта, и добавляет или отключает категории в файле сценария в соответствии с изменениями.

Шаги выполнения
-------------------------
1. **Загрузка данных из файла сценария**:
   - Функция `j_loads` используется для загрузки JSON-данных из файла сценария, указанного в `scenario_filename`.
   - Из загруженного JSON извлекается список сценариев (категорий) из ключа `'scenarios'`.
2. **Получение списка категорий с сайта**:
   - Вызывается функция `get_list_categories_from_site()`, чтобы получить актуальный список категорий с сайта Aliexpress.
3. **Обновление идентификаторов категорий в файле**:
   - Внутренняя функция `_update_all_ids_in_file()` обновляет список идентификаторов категорий (`all_ids_in_file`), извлекая их из файла сценария.
   - Если идентификатор категории не определен в файле, он извлекается из URL категории и добавляется в список.
4. **Получение данных о категориях с сайта Aliexpress**:
   - Отправляется HTTP-запрос GET для получения JSON-файла с категориями магазина, URL которого указан в файле сценария (`scenario_json['store']['shop categories json file']`).
   - Если запрос успешен (код состояния 200), JSON-ответ сохраняется в `categories_from_aliexpress_shop_json`. В противном случае, регистрируется ошибка.
5. **Сравнение списков категорий**:
   - Из `categories_from_aliexpress_shop_json` извлекается список групп категорий (`groups`).
   - Создаются два списка: `all_ids_on_site` (идентификаторы категорий на сайте) и `all_categories_on_site` (полные данные о категориях на сайте).
   - Списки заполняются данными из `groups` и их подгрупп.
   - Создаются списки `removed_categories` (категории, удаленные с сайта) и `added_categories` (категории, добавленные на сайт) путем сравнения `all_ids_in_file` и `all_ids_on_site`.
6. **Обработка добавленных категорий**:
   - Если есть добавленные категории (`len(added_categories) > 0`):
     - Для каждой добавленной категории извлекаются её имя и URL.
     - В `categories_in_file` добавляется новая запись с информацией о категории.
     - Обновленный список категорий сохраняется в файле сценария.
     - Отправляется уведомление о добавлении новых категорий.
7. **Обработка удаленных категорий**:
   - Если есть удаленные категории (`len(removed_categories) > 0`):
     - Для каждой удаленной категории устанавливается флаг `active` в `False`.
     - Обновленный список категорий сохраняется в файле сценария.
     - Отправляется уведомление об отключении категорий.
8. **Возврат значения**:
   - Функция возвращает `True`, если обновление выполнено успешно.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.scenario import update_categories_in_scenario_file
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome
from src import gs
from src import config

# Инициализация вебдрайвера
driver = Driver(Chrome)

# Создание экземпляра поставщика
supplier = Supplier(driver=driver, config=config)

# Имя файла сценария
scenario_filename = "aliexpress_scenario.json"

# Обновление категорий в файле сценария
result = update_categories_in_scenario_file(supplier, scenario_filename)

if result:
    print(f"Файл сценария {scenario_filename} успешно обновлен.")
else:
    print(f"Не удалось обновить файл сценария {scenario_filename}.")

driver.quit()
```
```markdown
### **Как использовать `get_list_categories_from_site`**

=========================================================================================

Описание
-------------------------
Функция `get_list_categories_from_site` предназначена для получения списка категорий с сайта. Она использует веб-драйвер для открытия страницы с категориями магазина, указанной в файле сценария, и выполняет действия для извлечения списка категорий.

Шаги выполнения
-------------------------
1. Функция принимает экземпляр `Supplier` в качестве аргумента.
2. Функция загружает JSON-конфигурацию из файла сценария, используя `json_loads`. Путь к файлу формируется на основе `gs.dir_scenarios` и `scenario_file`.
3. Из конфигурации извлекается URL страницы с категориями магазина (`scenario_json['store']['shop categories page']`).
4. Веб-драйвер переходит по указанному URL, используя метод `_d.get_url()`.
5.  `...`

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.scenario import get_list_categories_from_site
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome
from src import gs
from src import config

# Инициализация вебдрайвера
driver = Driver(Chrome)

# Создание экземпляра поставщика
supplier = Supplier(driver=driver, config=config)
supplier.driver = driver # fix me!
scenario_file = "aliexpress_scenario.json"  #  Укажите имя файла сценария

# Получение списка категорий с сайта
categories = get_list_categories_from_site(supplier, scenario_file)

# Вывод списка категорий
if categories:
    for category in categories:
        print(category)
else:
    print("Не удалось получить список категорий с сайта.")

driver.quit()
```

### **Как использовать `DBAdaptor`**

=========================================================================================

Описание
-------------------------
Класс `DBAdaptor` предоставляет методы для выполнения операций с базой данных, таких как выборка, вставка, обновление и удаление записей в таблице `AliexpressCategory`.

Шаги выполнения
-------------------------
1. **Инициализация класса**:
   - Создается экземпляр класса `DBAdaptor`.
2. **Выполнение операций с базой данных**:
   - Вызываются методы `select`, `insert`, `update` или `delete` для выполнения соответствующих операций с базой данных.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.scenario import DBAdaptor

# Создание экземпляра класса DBAdaptor
db_adaptor = DBAdaptor()

# Пример операции SELECT
db_adaptor.select(parent_id='parent_id_value')

# Пример операции INSERT
db_adaptor.insert()

# Пример операции UPDATE
db_adaptor.update()

# Пример операции DELETE
db_adaptor.delete()