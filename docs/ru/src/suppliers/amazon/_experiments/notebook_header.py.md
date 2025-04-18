# Модуль `notebook_header.py`

## Обзор

Модуль предназначен для экспериментов с поставщиком Amazon. Он содержит необходимые импорты и настройки для работы с веб-драйвером, поставщиками, продуктами и категориями.

## Подробней

Модуль содержит код, необходимый для запуска и работы с поставщиком Amazon. Он определяет базовые пути к директориям проекта, добавляет их в `sys.path`, импортирует необходимые классы и функции. Также включает функцию для старта поставщика с заданными параметрами.

## Классы

В данном файле классы не определены.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
```

**Назначение**: Запускает поставщика с заданным префиксом и локалью.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Локаль поставщика.

**Возвращает**:
- `Supplier`: Объект поставщика, созданный с заданными параметрами.
- `str`: Сообщение об ошибке, если не заданы префикс и локаль.

**Как работает функция**:
- Проверяет, заданы ли префикс и локаль поставщика. Если нет, возвращает сообщение об ошибке.
- Создает словарь `params` с параметрами поставщика.
- Создает и возвращает объект класса `Supplier` с переданными параметрами.

**Примеры**:

```python
# Пример вызова функции с заданными параметрами
supplier = start_supplier('amazon', 'us')
print(supplier)  # Выведет объект Supplier, созданный с параметрами 'amazon' и 'us'

# Пример вызова функции без параметров
error_message = start_supplier(None, None)
print(error_message)  # Выведет сообщение "Не задан сценарий и язык"
```