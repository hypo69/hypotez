### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `PrestaSupplier`, который предназначен для работы с поставщиками в PrestaShop. Он наследуется от класса `PrestaShop` и предоставляет функциональность для инициализации и настройки соединения с API PrestaShop.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `SimpleNamespace`, `Optional` и `header`.
   - Импортируются модули `gs`, `logger` из `src`, `j_loads_ns` из `src.utils.jjson` и `PrestaShop` из `.api`.

2. **Определение класса `PrestaSupplier`**:
   - Определяется класс `PrestaSupplier`, который наследуется от `PrestaShop`.

3. **Инициализация класса `PrestaSupplier` (`__init__`)**:
   - Метод `__init__` принимает параметры `credentials` (словарь или объект `SimpleNamespace` с `api_domain` и `api_key`), `api_domain` и `api_key`.
   - Если `credentials` переданы, из них извлекаются значения `api_domain` и `api_key`.
   - Проверяется, что `api_domain` и `api_key` не пусты. Если хотя бы один из них отсутствует, выбрасывается исключение `ValueError`.
   - Вызывается конструктор родительского класса `PrestaShop` с переданными параметрами.

Пример использования
-------------------------

```python
from types import SimpleNamespace
from src.endpoints.prestashop.supplier import PrestaSupplier

# Пример 1: Инициализация с использованием отдельных параметров
supplier = PrestaSupplier(
    api_domain='your_api_domain',
    api_key='your_api_key'
)

# Пример 2: Инициализация с использованием словаря credentials
credentials_dict = {
    'api_domain': 'your_api_domain',
    'api_key': 'your_api_key'
}
supplier = PrestaSupplier(credentials=credentials_dict)

# Пример 3: Инициализация с использованием SimpleNamespace credentials
credentials_ns = SimpleNamespace(
    api_domain='your_api_domain',
    api_key='your_api_key'
)
supplier = PrestaSupplier(credentials=credentials_ns)

# Пример 4: Обработка ошибки при отсутствии api_domain или api_key
try:
    supplier = PrestaSupplier()
except ValueError as e:
    print(f"Ошибка: {e}")

```