## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот код представляет собой  заголовок для файла Python, расположенного в директории `src/suppliers/ebay/_experiments/JUPYTER_header.py` проекта `hypotez`.  Он содержит метаданные для файла, импорты необходимых модулей и функцию `start_supplier()`, которая запускает поставщика данных.

### Шаги выполнения
-------------------------
1. **Определение пути**: Код определяет путь к корневой директории проекта `hypotez` и добавляет его в список путей `sys.path`. Это позволяет импортировать модули из любой директории проекта. 
2. **Импорт модулей**:  Код импортирует необходимые модули, такие как `Path`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct` и  `save_text_file`. 
3. **Определение функции `start_supplier`**: Функция `start_supplier` принимает два аргумента: `supplier_prefix` (префикс имени поставщика) и `locale` (локаль).
4. **Создание словаря параметров**:  Функция создает словарь параметров `params` с ключами `supplier_prefix` и `locale`,  используя переданные аргументы.
5. **Инициализация класса `Supplier`**:  Функция использует словарь `params` для инициализации экземпляра класса `Supplier`, который  предположительно отвечает за взаимодействие с поставщиком.
6. **Возврат объекта Supplier**: Функция возвращает созданный объект `Supplier`.

### Пример использования
-------------------------
```python
# Запускаем поставщика AliExpress с локалью 'en'
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Выполняем действия с поставщиком
supplier.get_products() # предположительно, получение списка товаров
supplier.download_data() # предположительно, загрузка данных о товарах
```

### Изменения
-------------------------
- Добавлены  аннотации типов к параметрам и возвращаемому значению функции. 
- Добавлен  комментарий,  объясняющий  назначение  функции  `start_supplier` 
-  Исправлено  неверное  использование  импортов.
- Добавлены  примеры  использования  кода.