## Как использовать класс `Graber` для сбора данных с Grandadvance
=========================================================================================

Описание
-------------------------
Класс `Graber` предназначен для сбора данных о товарах с веб-сайта `grandadvance.com`. Он наследуется от базового класса `src.suppliers.graber.Graber` и предоставляет методы для обработки различных полей товара на странице. В случае необходимости нестандартной обработки поля, метод может быть переопределен.

Шаги выполнения
-------------------------
1. **Инициализация:**  Создайте экземпляр класса `Graber`, передав в конструктор объект WebDriver и индекс языка. 
    - `driver`: объект WebDriver, используемый для взаимодействия с браузером.
    - `lang_index`: индекс языка, определяющий версию сайта Grandadvance. 
2. **Загрузка конфигурации:**  Конструктор класса загружает конфигурацию из JSON-файла, расположенного в папке `src/suppliers/grandadvance/grandadvance.json`, а также локаторы элементов для обработки данных в `src/suppliers/grandadvance/locators/product.json`.
3. **Использование методов:**  Используйте методы класса `Graber` для сбора данных с Grandadvance. 
    -  **`get_product_data`**:  Получает данные о товаре с текущей страницы.
    - **`get_specifications_data`**:  Получает данные о спецификациях товара.
    - **`get_pictures_data`**:  Получает информацию об изображениях товара. 
    - **`get_price_data`**:  Получает данные о цене товара. 

Пример использования
-------------------------

```python
from src.suppliers.grandadvance.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.drivers.chrome import Chrome

driver = Driver(Chrome)
graber = Graber(driver, lang_index=0)  # Инициализация экземпляра Graber

# Получаем данные о товаре
product_data = graber.get_product_data() 

# Получаем данные о спецификациях
specifications_data = graber.get_specifications_data()

# Получаем изображения товара
pictures_data = graber.get_pictures_data()

# Получаем данные о цене
price_data = graber.get_price_data() 

print(product_data)
print(specifications_data)
print(pictures_data)
print(price_data) 
```

**Важно:**

- Перед использованием класса `Graber` убедитесь, что WebDriver инициализирован и открыта страница Grandadvance. 
- Класс `Graber` может быть расширен для добавления новых методов или переопределения существующих, чтобы обеспечить специфическую обработку данных.
- В случае нестандартной обработки данных вы можете переопределить методы класса `Graber`, чтобы удовлетворить потребности вашего приложения.