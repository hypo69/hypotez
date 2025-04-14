# Модуль `amazon_murano_glass`

## Обзор

Модуль `amazon_murano_glass.py` предназначен для запуска сценария работы с поставщиком "amazon" для категории "Murano Glass".  Он использует функциональность из модуля `header` для инициализации поставщика и запуска сценария, определенного в `dict_scenarios`.

## Подробней

Модуль выполняет следующие шаги:

1.  Импортирует необходимые модули и функции из `header` и `dict_scenarios`.
2.  Инициализирует поставщика "amazon" с помощью функции `start_supplier` из модуля `header`.
3.  Запускает сценарий "Murano Glass", используя метод `run_scenario` класса `Supplier`.
4.  Извлекает первый ключ из словаря `presta_categories` текущего сценария.

## Функции

### `start_supplier`

```python
def start_supplier(name: str) -> Supplier:
    """
    Создает и возвращает экземпляр класса Supplier.

    Args:
        name (str): Имя поставщика.

    Returns:
        Supplier: Экземпляр класса Supplier.
    """
    ...
```

**Назначение**:

Функция `start_supplier` предназначена для создания и инициализации экземпляра класса `Supplier` с заданным именем.

**Параметры**:

*   `name` (str): Имя поставщика, которое будет присвоено экземпляру класса `Supplier`.

**Возвращает**:

*   `Supplier`: Возвращает экземпляр класса `Supplier`, созданный с указанным именем.

**Как работает функция**:

1.  Функция принимает имя поставщика в качестве аргумента.
2.  Создает экземпляр класса `Supplier` с указанным именем.
3.  Возвращает созданный экземпляр класса `Supplier`.

**Примеры**:

```python
supplier = start_supplier('amazon')
```

Здесь создается экземпляр класса `Supplier` с именем "amazon", который затем присваивается переменной `supplier`.

## Переменные

*   `s`: Экземпляр класса `Supplier`, созданный с именем 'amazon'.

## Другие функции

### `Supplier.run_scenario`

```python
def run_scenario(scenario: dict) -> None:
    """
    Запускает сценарий, определенный в словаре.

    Args:
        scenario (dict): Словарь, содержащий сценарий для выполнения.

    Returns:
        None
    """
    ...
```

**Назначение**:

Метод `run_scenario` класса `Supplier` предназначен для запуска сценария, определенного в виде словаря.

**Параметры**:

*   `scenario` (dict): Словарь, содержащий шаги и параметры сценария для выполнения.

**Возвращает**:

*   `None`: Метод ничего не возвращает.

**Как работает функция**:

1.  Функция принимает словарь `scenario`, содержащий описание шагов и параметров сценария.
2.  Выполняет шаги, описанные в словаре `scenario`, используя методы класса `Supplier`.

**Примеры**:

```python
s.run_scenario(scenario['Murano Glass'])
```

В данном примере запускается сценарий "Murano Glass", определенный в словаре `scenario`.

## Переменные

*   `k`: Первый ключ из словаря `presta_categories['default_category']` текущего сценария.

## ASCII flowchart: `amazon_murano_glass.py`

```
start_supplier('amazon')   
↓
s = <Supplier object>       
↓
s.run_scenario(scenario['Murano Glass'])
↓
k = list(s.current_scenario['presta_categories']['default_category'].keys())[0]