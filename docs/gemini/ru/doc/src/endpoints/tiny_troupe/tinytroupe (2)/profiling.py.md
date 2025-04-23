# Модуль `profiling.py`

## Обзор

Модуль `profiling.py` предоставляет механизмы для анализа и понимания характеристик популяций агентов, таких как распределение их возраста, типичные интересы и т.д. Он содержит класс `Profiler`, который используется для вычисления и визуализации распределения атрибутов агентов.

## Подробнее

Модуль предназначен для работы с данными об агентах, представленными в виде списка словарей, и позволяет строить графики распределения различных атрибутов, таких как возраст, занятие и национальность. Это полезно для анализа демографических и социальных характеристик модельных агентов в контексте проекта `hypotez`.

## Классы

### `Profiler`

**Описание**: Класс `Profiler` предназначен для профилирования списка агентов, вычисления распределения их атрибутов и визуализации этих распределений в виде графиков.

**Атрибуты**:

- `attributes` (List[str]): Список атрибутов для профилирования (например, `"age"`, `"occupation"`, `"nationality"`).
- `attributes_distributions` (dict): Словарь, содержащий распределения атрибутов, где ключ - имя атрибута, а значение - DataFrame с данными для построения графика.

**Методы**:

- `__init__`: Инициализирует объект `Profiler` с заданным списком атрибутов.
- `profile`: Вычисляет распределения атрибутов для заданных агентов.
- `render`: Визуализирует профиль агентов, отображая графики распределения атрибутов.
- `_compute_attributes_distributions`: Вычисляет распределения для всех указанных атрибутов агентов.
- `_compute_attribute_distribution`: Вычисляет распределение одного атрибута для заданных агентов.
- `_plot_attributes_distributions`: Строит графики распределения для всех атрибутов.
- `_plot_attribute_distribution`: Строит график распределения для одного атрибута.

### `__init__`

```python
def __init__(self, attributes: List[str]=["age", "occupation", "nationality"]) -> None:
    """
    Инициализирует объект `Profiler` с заданным списком атрибутов.

    Args:
        attributes (List[str], optional): Список атрибутов для профилирования. По умолчанию `["age", "occupation", "nationality"]`.
    """
```
**Как работает функция**:

Функция инициализирует объект класса `Profiler`. Она принимает список атрибутов, которые будут профилироваться для каждого агента. По умолчанию, если список атрибутов не предоставлен, используются атрибуты "age", "occupation" и "nationality". Также инициализируется пустой словарь `self.attributes_distributions`, который будет хранить распределения атрибутов в виде pandas DataFrames.

**Примеры**:
```python
# Пример 1: Инициализация Profiler с атрибутами по умолчанию
profiler = Profiler()

# Пример 2: Инициализация Profiler с заданными атрибутами
profiler = Profiler(attributes=["age", "gender", "income"])
```

### `profile`

```python
def profile(self, agents: List[dict]) -> dict:
    """
    Профилирует заданных агентов.

    Args:
        agents (List[dict]): Список агентов для профилирования.

    Returns:
        dict: Словарь распределений атрибутов.
    """
```

**Как работает функция**:
Функция `profile` принимает список агентов, представленных в виде словарей, и вычисляет распределения их атрибутов с помощью метода `_compute_attributes_distributions`. Результаты сохраняются в `self.attributes_distributions` и возвращаются.

**Примеры**:

```python
# Пример: Профилирование списка агентов
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
distributions = profiler.profile(agents)
# distributions будет содержать распределения атрибутов 'age', 'occupation' и 'nationality'
```

### `render`

```python
def render(self) -> None:
    """
    Визуализирует профиль агентов.
    """
```

**Как работает функция**:

Функция `render` вызывает метод `_plot_attributes_distributions` для отображения графиков распределения атрибутов агентов.

**Примеры**:

```python
# Пример: Визуализация профиля агентов
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
profiler.profile(agents)
profiler.render()  # Вызовется отображение графиков распределения атрибутов
```

### `_compute_attributes_distributions`

```python
def _compute_attributes_distributions(self, agents: list) -> dict:
    """
    Вычисляет распределения атрибутов для заданных агентов.

    Args:
        agents (list): Список агентов, для которых вычисляются распределения атрибутов.

    Returns:
        dict: Словарь распределений атрибутов.
    """
```

**Как работает функция**:

Функция `_compute_attributes_distributions` принимает список агентов и для каждого атрибута из `self.attributes` вызывает метод `_compute_attribute_distribution` для вычисления распределения. Результаты сохраняются в словаре, где ключами являются имена атрибутов, а значениями - DataFrame с данными распределения.

**Примеры**:

```python
# Пример: Вычисление распределений атрибутов
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
distributions = profiler._compute_attributes_distributions(agents)
# distributions будет содержать DataFrame для атрибутов 'age', 'occupation' и 'nationality'
```

### `_compute_attribute_distribution`

```python
def _compute_attribute_distribution(self, agents: list, attribute: str) -> pd.DataFrame:
    """
    Вычисляет распределение заданного атрибута для агентов.

    Args:
        agents (list): Список агентов, для которых вычисляется распределение атрибута.
        attribute (str): Атрибут, для которого вычисляется распределение.

    Returns:
        pd.DataFrame: DataFrame с данными распределения атрибута.
    """
```

**Как работает функция**:

Функция `_compute_attribute_distribution` извлекает значения заданного атрибута из каждого агента в списке, создает DataFrame на основе этих значений и вычисляет частоту каждого значения атрибута. Результат сортируется по значению атрибута и возвращается в виде DataFrame.

**Примеры**:

```python
# Пример: Вычисление распределения атрибута 'age'
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
age_distribution = profiler._compute_attribute_distribution(agents, "age")
# age_distribution будет содержать DataFrame с распределением возраста
```

### `_plot_attributes_distributions`

```python
def _plot_attributes_distributions(self) -> None:
    """
    Строит графики распределения для всех атрибутов.
    """
```

**Как работает функция**:

Функция `_plot_attributes_distributions` проходит по списку атрибутов `self.attributes` и для каждого атрибута вызывает метод `_plot_attribute_distribution`, который строит график распределения.

**Примеры**:

```python
# Пример: Отображение графиков распределения всех атрибутов
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
profiler.profile(agents)
profiler._plot_attributes_distributions()  # Вызовется отображение графиков распределения для всех атрибутов
```

### `_plot_attribute_distribution`

```python
def _plot_attribute_distribution(self, attribute: str) -> pd.DataFrame:
    """
    Строит график распределения для заданного атрибута.

    Args:
        attribute (str): Атрибут, для которого строится график распределения.

    Returns:
        pd.DataFrame: Данные, использованные для построения графика.
    """
```

**Как работает функция**:

Функция `_plot_attribute_distribution` извлекает DataFrame распределения для заданного атрибута из `self.attributes_distributions`, строит столбчатый график (bar plot) на основе этих данных и отображает его с помощью `plt.show()`.

**Примеры**:

```python
# Пример: Отображение графика распределения атрибута 'age'
agents = [
    {"age": 25, "occupation": "developer", "nationality": "USA"},
    {"age": 30, "occupation": "manager", "nationality": "Canada"},
    {"age": 25, "occupation": "developer", "nationality": "UK"}
]
profiler = Profiler()
profiler.profile(agents)
profiler._plot_attribute_distribution("age")  # Вызовется отображение графика распределения возраста
```