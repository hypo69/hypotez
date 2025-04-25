## Как использовать локаторы в проекте Hypotez
=========================================================================================

Описание
-------------------------
Локаторы — это структурированные описания элементов на HTML-странице, используемые для их поиска и взаимодействия с помощью веб-драйвера. Они представляют собой JSON-объекты, содержащие информацию о стратегии поиска, селекторе, атрибутах, действиях и других параметрах, необходимых для работы веб-драйвера.

Шаги выполнения
-------------------------
1. **Определение локатора**: Локаторы хранятся в JSON-файлах, расположенных в директории `locators/` внутри папки каждого конкретного поставщика. 
2. **Загрузка локатора**:  Используйте функцию `j_loads_ns` для загрузки локатора из JSON-файла.
3. **Использование локатора**: 
    - Получите доступ к локатору через атрибут `product_locator` или `category_locator` класса `Graber` или его наследника.
    - Вызовите метод `execute_locator` класса `Driver` с локатором в качестве аргумента.
    - Получите результат действия с помощью методов `await self.name()`, `await self.price()`, и т.д., которые соответствуют ключам в локаторах.


Пример использования
-------------------------

```python
# Внутри класса Graber или его наследника
f = self.fields # Экземпляр ProductFields
# Имя будет получено с использованием локатора "name" из product.json
await self.name() # self.fields.name = await self.driver.execute_locator(self.product_locator.name)
# Цена будет получена с использованием локатора "price"
await self.price() # self.fields.price = await self.driver.execute_locator(self.product_locator.price)
...
```

### Детали:

* **`attribute`**: Указывает атрибут, который необходимо получить от найденного элемента.
* **`by`**: Стратегия поиска элемента, например, `XPATH` или `CSS_SELECTOR`.
* **`selector`**: Селектор, соответствующий выбранной стратегии поиска.
* **`if_list`**: Определяет, как обрабатывать список найденных элементов.
* **`use_mouse`**: Указывает, требуется ли имитация мыши для взаимодействия с элементом.
* **`event`**: Действие, которое необходимо выполнить с элементом, например, `click()`, `screenshot()`, `type()`, `send_keys()`.
* **`mandatory`**: Определяет, является ли нахождение элемента обязательным.
* **`timeout`**: Время ожидания появления элемента на странице.
* **`timeout_for_event`**: Условие ожидания перед выполнением действия.
* **`locator_description`**: Текстовое описание локатора для удобства чтения и отладки.

### Сложные локаторы (Использование списков):

Локатор может содержать списки одинаковой длины для ключей `attribute`, `by`, `selector`, `event`, `use_mouse`, `mandatory`, `locator_description`. Это позволяет выполнять последовательность действий с элементом.

### Пример локатора со списками:

```json
"description": {
    "attribute": [
      null,       // Для первого шага атрибут не нужен
      "innerText" // Для второго шага - получить текст
    ],
    "by": [
      "XPATH",    // Стратегия для первого шага
      "XPATH"     // Стратегия для второго шага
    ],
    "selector": [
      "//a[contains(@href, \'#tab-description\')]", // Селектор для клика по вкладке
      "//div[@id = \'tab-description\']//p"         // Селектор для получения текста описания
    ],
    "timeout": 0, // Общий таймаут (можно тоже списком)
    "timeout_for_event": "presence_of_element_located", // Общее условие ожидания
    "event": [
      "click()",  // На первом шаге - кликнуть
      null        // На втором шаге - действий нет
    ],
    "if_list": "first", // Общее правило для списков (можно списком)
    "use_mouse": false,  // Общее (можно списком)
    "mandatory": [
      true,       // Первый шаг обязателен
      true        // Второй шаг обязателен
    ],
    "locator_description": [
      "Нажимаю на вкладку \'Описание\'.", // Описание первого шага
      "Читаю текст из блока описания."  // Описание второго шага
    ]
  }
```

### Где расположены локаторы:

Файлы с локаторами (`product.json`, `category.json` и т.д.) хранятся в директории `locators` внутри папки каждого конкретного поставщика.

```text
src/
└── suppliers/
    ├── suppliers_list/
    │   ├── ksp/
    │   │   ├── __init__.py
    │   │   ├── graber.py  # <--- Класс Graber для ksp
    │   │   └── locators/  # <--- Папка с локаторами для ksp
    │   │       ├── product.json
    │   │       └── category.json
    │   ├── aliexpress/
    │   │   ├── __init__.py
    │   │   ├── graber.py
    │   │   └── locators/
    │   │       ├── product.json
    │   │       └── category.json
    │   └── ...
    ├── graber.py # Базовый класс Graber
    └── get_graber_by_supplier.py # Фабрика граберов
```

### Создание локаторов для разных версий сайта:

Если сайт имеет разные версии (например, десктопную и мобильную), рекомендуется создавать отдельные файлы локаторов для каждой версии. Выбор нужного файла локаторов можно реализовать в методе `grab_page_async` класса-наследника `Graber`, проверяя, например, текущий URL.

```python
# Внутри класса-наследника Graber (например, KspGraber)
class KspGraber(Graber):
    # ... __init__ ...

    async def grab_page_async(self, *args, **kwargs) -> ProductFields:
        # Проверяем URL перед загрузкой локаторов по умолчанию
        if 'ksp.co.il/mob' in self.driver.current_url:
            logger.info("Обнаружена мобильная версия сайта KSP, загружаю мобильные локаторы.")
            # Перезагружаем локаторы из мобильного файла
            self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product_mobile.json')
            self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category_mobile.json')
        else:
            # Убедимся, что используются десктопные (если не были загружены ранее или переключились с мобильной)
             self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product.json')
             self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category.json')


        # Дальнейшая логика сбора данных...
        try:
            await super().grab_page_async(*args, **kwargs) # Вызываем базовую логику с нужными локаторами
            return self.fields
        except Exception as ex:
            logger.error(f"Ошибка в функции `grab_page_async` KSP", ex)
            return None
```