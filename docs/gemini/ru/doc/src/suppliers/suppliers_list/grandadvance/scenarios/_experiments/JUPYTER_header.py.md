# Модуль для запуска поставщика

## Обзор

Данный модуль содержит функцию `start_supplier`, которая инициирует работу поставщика. Функция принимает два параметра: `supplier_prefix` - префикс названия поставщика (например, `aliexpress`) и `locale` - язык (например, `en`).

## Подробнее

Этот модуль находится в директории `hypotez/src/suppliers/grandadvance/scenarios/_experiments/JUPYTER_header.py`. Он импортирует несколько модулей, таких как `src.webdriver.driver`, `src.product`, `src.category`, `src.utils` и `src.endpoints.PrestaShop`, которые используются для работы с веб-драйвером, товарами, категориями, строками, и PrestaShop API соответственно.

## Функции

### `start_supplier`

**Назначение**: Инициализация работы поставщика.

**Параметры**:

- `supplier_prefix` (str): Префикс названия поставщика (например, `aliexpress`).
- `locale` (str): Язык (например, `en`).

**Возвращает**:

- `Supplier`: Объект класса `Supplier`, представляющий поставщика.

**Как работает функция**:

Функция создает словарь параметров `params` с ключами `supplier_prefix` и `locale`, которые передаются в качестве аргументов функции. Затем, функция использует этот словарь для создания объекта класса `Supplier` и возвращает его.

**Примеры**:

```python
start_supplier(supplier_prefix='aliexpress', locale='en')
```

В этом примере функция `start_supplier` вызывается с параметрами `supplier_prefix='aliexpress'` и `locale='en'`, что приводит к созданию объекта класса `Supplier` для поставщика Aliexpress на английском языке.