### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот код предназначен для сбора и обработки данных о товарах с веб-страниц поставщика "HB" (hbdeadsea.co.il) и последующей интеграции этих данных в систему PrestaShop. Он использует Selenium для взаимодействия с веб-страницами, извлекает информацию о товарах и приводит её к формату, необходимому для PrestaShop.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Импортируются необходимые библиотеки и модули, включая `os`, `sys`, `Path`, `List`, `Union`, `Dict`, `WebElement`, а также пользовательские модули из проекта `hypotez`.
   - Добавляется корневая директория проекта в `sys.path`, чтобы обеспечить доступ к другим модулям проекта.
   - Инициализируются основные объекты: `Supplier`, `Product`, `ProductFields` и `Driver` для взаимодействия с веб-страницей и данными о товарах.
   - Определяется сценарий (`s.current_scenario`) с URL страницы категории товаров, названием и категориями PrestaShop.
   - Выполняется переход на URL, указанный в сценарии, с помощью `d.get_url()`.

2. **Функция `grab_product_page`**:
   - Основная функция для сбора данных о товаре. Она принимает объект `Supplier` и определяет глобальные переменные для экземпляров классов `Supplier`, `Product` и `ProductFields`.
   - Закрывается всплывающий баннер на странице с помощью `d.execute_locator(l["close_banner"])`.
   - Прокручивается страница для загрузки контента, подгружаемого через AJAX, с помощью `d.scroll()`.

3. **Функция `product_reference_and_volume_and_price_for_100`**:
   - Извлекает информацию об объеме, артикуле поставщика и цене за единицу товара из веб-элементов на странице.
   - Использует `d.execute_locator` для получения списка веб-элементов `product_reference_and_volume_and_price_for_100`.
   - Перебирает веб-элементы и извлекает значения для полей `volume` (объем), `supplier_reference` (артикул поставщика) и цену за единицу товара.

4. **Функция `set_references`**:
   - Устанавливает значения для идентификаторов товара, таких как `id_supplier` и `reference`, на основе данных поставщика и артикула.
   - `f.id_supplier` присваивается значение `s.supplier_id` (ID поставщика).
   - `f.reference` формируется как строка, объединяющая `s.supplier_id` и `f.supplier_reference`.

5. **Сбор дополнительных полей товара**:
   - Вызываются различные функции (`field_additional_shipping_cost`, `field_affiliate_short_link` и т.д.) для сбора значений других полей товара.
   - Некоторые поля (`f.available_for_order`, `f.active`) устанавливаются в зависимости от наличия товара.
   - Извлекаются URL изображений товара.

6. **Извлечение основных данных товара**:
   - Извлекается название товара (`f.name`) и формируется `link_rewrite` (URL товара) на основе названия.

7. **Обработка и нормализация данных**:
   - Некоторые поля нормализуются и очищаются от лишних символов с использованием методов `StringNormalizer`.

8. **Поиск и добавление/обновление товара в PrestaShop**:
   - После сбора всех необходимых данных, функция возвращает объект `ProductFields` (`f`).
   - Убираются пустые ключи из словаря `presta_fields_dict`.
   - Формируется фильтр для поиска товара в PrestaShop по артикулу (`reference`).
   - Используется метод `p.get` для поиска товара в PrestaShop. Если товар не найден, он добавляется с помощью `p.add`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.hb._experiments.ide_experiments_fields import grab_product_page
from src.product import Product
from src.suppliers import Supplier

# Предположим, что s - это экземпляр класса Supplier, d - экземпляр класса Driver
# и они уже настроены и готовы к работе
s: Supplier = Supplier(supplier_prefix='hb')
s.current_scenario: Dict = {
    "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
    "name": "טיפוח כפות ידיים ורגליים",
    "condition": "new",
    "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
    }
}

# d.get_url(s.current_scenario['url'])
# s.driver = d
product_fields = grab_product_page(s)

if product_fields:
    print(f'Название товара: {product_fields.name}')
    print(f'Артикул поставщика: {product_fields.supplier_reference}')
    print(f'Цена: {product_fields.price}')
else:
    print('Не удалось получить данные о товаре.')