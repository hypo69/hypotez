### **Как использовать этот блок кода**

Описание
-------------------------
Этот блок кода определяет класс `PrestaShopShop`, который предназначен для работы с магазинами, созданными на платформе PrestaShop. Он наследуется от класса `PrestaShop` и предоставляет функциональность для инициализации и настройки соединения с API PrestaShop магазина.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `SimpleNamespace`, `Optional`, `header`, `gs`, `logger`, `j_loads`, `PrestaShop`, `PrestaShopException`, `Path`, `attr`, `attrs`, `sys` и `os`.
2. **Определение класса `PrestaShopShop`**:
   - Создается класс `PrestaShopShop`, наследующийся от класса `PrestaShop`. Этот класс предназначен для работы с магазинами PrestaShop.
3. **Инициализация класса `PrestaShopShop`**:
   - Определяется метод `__init__`, который инициализирует экземпляр класса `PrestaShopShop`.
   - Принимает аргументы:
     - `credentials` (Optional[dict | SimpleNamespace]): Словарь или объект `SimpleNamespace` с параметрами `api_domain` и `api_key`.
     - `api_domain` (Optional[str]): Домен API PrestaShop.
     - `api_key` (Optional[str]): Ключ API PrestaShop.
     - `*args`, `**kwargs`: Дополнительные аргументы, передаваемые в конструктор родительского класса `PrestaShop`.
4. **Обработка параметров инициализации**:
   - Если передан параметр `credentials`, извлекаются значения `api_domain` и `api_key` из него.
   - Проверяется наличие значений `api_domain` и `api_key`. Если хотя бы один из них отсутствует, выбрасывается исключение `ValueError`.
5. **Вызов конструктора родительского класса**:
   - Вызывается конструктор родительского класса `PrestaShop` с передачей параметров `api_domain`, `api_key`, `*args` и `**kwargs`.

Пример использования
-------------------------

```python
from types import SimpleNamespace
from src.endpoints.prestashop.shop import PrestaShopShop

# Пример 1: Инициализация с использованием отдельных параметров
shop = PrestaShopShop(
    api_domain="your_api_domain",
    api_key="your_api_key"
)

# Пример 2: Инициализация с использованием объекта SimpleNamespace
credentials = SimpleNamespace(api_domain="your_api_domain", api_key="your_api_key")
shop = PrestaShopShop(credentials=credentials)

# Пример 3: Обработка исключения при отсутствии параметров
try:
    shop = PrestaShopShop()
except ValueError as e:
    print(f"Ошибка: {e}")
```