# Модуль src.scenario._experiments.amazon_murano_glass

## Обзор

Модуль представляет собой эксперимент для работы с поставщиком "amazon" и предназначен для выполнения сценария, связанного с категорией "Murano Glass". Модуль использует функциональность, предоставляемую классом `Supplier` из модуля `header`, а также сценарии из модуля `dict_scenarios`.

## Подробней

Модуль выполняет следующие шаги:

1.  Инициализирует поставщика "amazon" с помощью функции `start_supplier` из модуля `header`. Результат инициализации сохраняется в переменной `s`.
2.  Запускает сценарий "Murano Glass" с помощью метода `run_scenario` объекта `s`. Сценарий берется из словаря `scenario` в модуле `dict_scenarios`.
3.  Извлекает первый ключ из словаря `default_category` внутри `presta_categories` текущего сценария и сохраняет его в переменной `k`.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_name: str) -> Supplier:
    """ Функция инициализирует и возвращает объект поставщика.

    Args:
        supplier_name (str): Имя поставщика, которого необходимо инициализировать.

    Returns:
        Supplier: Объект поставщика.
    """
```

## Переменные

-   `s`: Объект класса `Supplier`, представляющий поставщика "amazon". Инициализируется с помощью функции `start_supplier('amazon')`.
-   `scenario`: Словарь, содержащий различные сценарии. Используется для получения сценария "Murano Glass".
-   `k`: Первый ключ из словаря `default_category` внутри `presta_categories` текущего сценария.

## Как работает модуль:

1.  Сначала происходит инициализация поставщика `amazon` через функцию `start_supplier`, результат сохраняется в переменной `s`.
2.  Далее запускается сценарий Murano Glass с помощью метода `s.run_scenario(scenario['Murano Glass'])`. Это означает, что для поставщика `amazon` будет выполнен сценарий, определенный для "Murano Glass" в словаре `scenario`.
3.  После выполнения сценария извлекается категория по умолчанию (default_category) из текущего сценария и берется первый ключ из этой категории. Ключ сохраняется в переменной `k`.

## Примеры

Пример инициализации поставщика и запуска сценария:

```python
import header
from header import start_supplier
from dict_scenarios import scenario

s = start_supplier('amazon')
s.run_scenario(scenario['Murano Glass'])
```

Пример извлечения ключа из категории по умолчанию:

```python
k = list(s.current_scenario['presta_categories']['default_category'].keys())[0]
print(k)