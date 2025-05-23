## Как использовать блок кода `Graber`
=========================================================================================

### Описание
-------------------------

Блок кода `Graber` представляет собой класс для сбора данных о товарах с Amazon. Он наследует методы от базового класса `src.suppliers.graber.Graber` и предоставляет механизм обработки различных полей товара на странице. 

### Шаги выполнения
-------------------------

1. **Инициализация класса:**
    - Создается объект класса `Graber`, передавая в качестве аргумента объект `driver` (веб-драйвер) и `lang_index` (индекс языка).
    - В конструкторе класса устанавливается префикс поставщика (`supplier_prefix`) равным `'amazon'`.
    - Настраивается контекст с помощью `Context.locator_for_decorator`.

2. **Обработка полей:**
    - Класс `Graber` предоставляет методы для обработки различных полей товара на странице.
    - По умолчанию используется логика из родительского класса `src.suppliers.graber.Graber`.
    - Для нестандартной обработки поля можно переопределить соответствующий метод в классе `Graber`.

3. **Декоратор:**
    - Перед отправкой запроса к вебдрайверу можно выполнить предварительные действия через декоратор `close_pop_up`.
    - Декоратор по умолчанию находится в родительском классе.
    - Декоратор выполняется, если `Context.locator_for_decorator` установлен.
    - Можно реализовать собственный декоратор, раскомментировав соответствующие строки кода.

### Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.amazon.graber import Graber
from src.webdriver.driver import Driver

# Создаем объект веб-драйвера (например, Chrome)
driver = Driver(Chrome)

# Создаем объект класса Graber
graber = Graber(driver, lang_index=0)  # lang_index - индекс языка

# ... (получаем данные о товаре)
```