### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для добавления нового товара в PrestaShop. Он берет объект `ProductFields`, преобразует его в формат, понятный для API PrestaShop, и отправляет запрос на добавление товара.

Шаги выполнения
-------------------------
1. **Подготовка данных**:
   - Метод `add_new_product` принимает объект `ProductFields`, содержащий информацию о товаре.
   - Добавляется `id_category_default` в поле `additional_categories` для поиска родительских категорий.
   - Вызывается метод `_add_parent_categories(f)`, чтобы добавить все уникальные родительские категории для товара.

2. **Преобразование в формат PrestaShop**:
   - Формируется словарь `presta_product_dict`, который соответствует структуре XML, ожидаемой PrestaShop API.

3. **Отправка запроса в PrestaShop**:
   - Полученный словарь преобразуется в XML с помощью `dict2xml(presta_product_dict)`.
   - XML-данные отправляются в API PrestaShop методом `self.create('products', data=presta_product_xml)`.

4. **Обработка ответа от PrestaShop**:
   - Если товар успешно добавлен, извлекается `id` добавленного товара из ответа сервера.
   - Если указан локальный путь к изображению товара (`f.local_image_path`), изображение загружается на сервер PrestaShop.
   - В случае успеха возвращается объект `added_product_ns`, содержащий данные о добавленном товаре.
   - Логируется информация о добавленном товаре с использованием `logger.info`.

5. **Обработка ошибок**:
   - Если при разборе ответа от сервера возникает ошибка (`KeyError`, `TypeError`), она логируется, и возвращается пустой словарь.
   - Если при добавлении товара происходит ошибка, она логируется, и возвращается пустой словарь.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.product import PrestaProduct, Config
from src.endpoints.prestashop.product_fields import ProductFields
from src.logger.logger import logger

def add_new_product_example():
    """
    Пример добавления нового товара в PrestaShop.
    """
    try:
        # 1. Инициализация объекта PrestaProduct с ключом API и доменом
        api_key = Config.API_KEY
        api_domain = Config.API_DOMAIN
        presta_product = PrestaProduct(api_key=api_key, api_domain=api_domain)

        # 2. Создание экземпляра ProductFields с данными о товаре
        product_data = {
            'id_category_default': 2,  # ID категории по умолчанию
            'name': [{'language': {'id': 1, 'value': 'Новый товар'}}],  # Название товара
            'price': 10.99,  # Цена товара
            'quantity': 100,  # Количество товара
            'active': 1  # Активен ли товар
        }
        product_fields = ProductFields(**product_data)

        # 3. Добавление товара в PrestaShop
        added_product = presta_product.add_new_product(product_fields)

        # 4. Проверка, успешно ли добавлен товар
        if added_product:
            logger.info(f"Товар успешно добавлен с ID: {added_product.id}")
        else:
            logger.error("Не удалось добавить товар.")

    except Exception as e:
        logger.error(f"Произошла ошибка при добавлении товара: {e}", exc_info=True)

# Вызов функции для примера
# add_new_product_example()