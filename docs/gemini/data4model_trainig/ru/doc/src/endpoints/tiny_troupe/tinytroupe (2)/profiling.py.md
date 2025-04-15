# Модуль для профилирования агентов Tiny Troupe

## Обзор

Модуль `profiling.py` предоставляет механизмы для анализа и понимания характеристик популяций агентов, таких как их распределение по возрасту, типичные интересы и так далее. Он содержит класс `Profiler`, который используется для вычисления и визуализации распределения атрибутов агентов.

## Подробнее

Этот модуль позволяет создавать профили агентов на основе заданных атрибутов и отображать их распределения в виде графиков. Это полезно для понимания структуры и разнообразия популяций агентов в симуляциях Tiny Troupe.

## Классы

### `Profiler`

**Описание**: Класс `Profiler` предназначен для профилирования агентов на основе заданных атрибутов.

**Атрибуты**:
- `attributes` (List[str]): Список атрибутов, которые будут использоваться для профилирования. По умолчанию `["age", "occupation", "nationality"]`.
- `attributes_distributions` (dict): Словарь, содержащий распределения атрибутов. Ключи - названия атрибутов, значения - DataFrame с данными о распределении.

**Методы**:
- `__init__(attributes: List[str]=["age", "occupation", "nationality"]) -> None`: Инициализирует объект `Profiler` с заданными атрибутами.
- `profile(agents: List[dict]) -> dict`: Профилирует переданных агентов и возвращает словарь с распределениями атрибутов.
- `render() -> None`: Отображает профиль агентов, визуализируя распределения атрибутов.
- `_compute_attributes_distributions(agents: list) -> dict`: Вычисляет распределения всех атрибутов для переданных агентов.
- `_compute_attribute_distribution(agents: list, attribute: str) -> pd.DataFrame`: Вычисляет распределение заданного атрибута для переданных агентов.
- `_plot_attributes_distributions() -> None`: Отображает распределения всех атрибутов.
- `_plot_attribute_distribution(attribute: str) -> pd.DataFrame`: Отображает распределение заданного атрибута.

### `__init__`

```python
def __init__(self, attributes: List[str]=["age", "occupation", "nationality"]) -> None:
    """
    Инициализирует объект `Profiler` с заданными атрибутами.

    Args:
        attributes (List[str], optional): Список атрибутов для профилирования.
            По умолчанию `["age", "occupation", "nationality"]`.
    """
    ...
```

**Назначение**: Инициализирует объект `Profiler`, устанавливая атрибуты для профилирования и пустой словарь для хранения распределений атрибутов.

**Параметры**:
- `attributes` (List[str], optional): Список атрибутов, которые будут использоваться для профилирования. По умолчанию `["age", "occupation", "nationality"]`.

**Как работает функция**:
- Устанавливает атрибут `self.attributes` равным переданному списку атрибутов.
- Инициализирует пустой словарь `self.attributes_distributions` для хранения вычисленных распределений атрибутов.

**Примеры**:
```python
profiler = Profiler()
profiler = Profiler(attributes=["age", "gender"])
```

### `profile`

```python
def profile(self, agents: List[dict]) -> dict:
    """
    Профилирует переданных агентов.

    Args:
        agents (List[dict]): Список агентов для профилирования.

    Returns:
        dict: Словарь с распределениями атрибутов.
    """
    ...
```

**Назначение**: Профилирует переданных агентов, вычисляя распределения заданных атрибутов.

**Параметры**:
- `agents` (List[dict]): Список агентов для профилирования. Каждый агент представлен в виде словаря.

**Возвращает**:
- `dict`: Словарь, где ключи - это названия атрибутов, а значения - DataFrame с данными о распределении для каждого атрибута.

**Как работает функция**:
- Вызывает метод `_compute_attributes_distributions` для вычисления распределений атрибутов переданных агентов.
- Сохраняет вычисленные распределения в атрибуте `self.attributes_distributions`.
- Возвращает словарь `self.attributes_distributions`.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}]
profiler = Profiler()
distributions = profiler.profile(agents)
print(distributions)
```

### `render`

```python
def render(self) -> None:
    """
    Отображает профиль агентов.
    """
    ...
```

**Назначение**: Отображает профиль агентов, визуализируя распределения атрибутов.

**Как работает функция**:
- Вызывает метод `_plot_attributes_distributions` для отображения распределений атрибутов.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}]
profiler = Profiler()
profiler.profile(agents)
profiler.render()
```

### `_compute_attributes_distributions`

```python
def _compute_attributes_distributions(self, agents: list) -> dict:
    """
    Вычисляет распределения всех атрибутов для переданных агентов.

    Args:
        agents (list): Список агентов, для которых вычисляются распределения атрибутов.

    Returns:
        dict: Словарь с распределениями атрибутов.
    """
    ...
```

**Назначение**: Вычисляет распределения всех атрибутов, заданных в `self.attributes`, для переданных агентов.

**Параметры**:
- `agents` (list): Список агентов, для которых вычисляются распределения атрибутов.

**Возвращает**:
- `dict`: Словарь, где ключи - это названия атрибутов, а значения - DataFrame с данными о распределении для каждого атрибута.

**Как работает функция**:
- Инициализирует пустой словарь `distributions`.
- Итерируется по списку атрибутов `self.attributes`.
- Для каждого атрибута вызывает метод `_compute_attribute_distribution` для вычисления распределения атрибута.
- Сохраняет вычисленное распределение в словаре `distributions`.
- Возвращает словарь `distributions`.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}]
profiler = Profiler()
distributions = profiler._compute_attributes_distributions(agents)
print(distributions)
```

### `_compute_attribute_distribution`

```python
def _compute_attribute_distribution(self, agents: list, attribute: str) -> pd.DataFrame:
    """
    Вычисляет распределение заданного атрибута для переданных агентов и отображает его.

    Args:
        agents (list): Список агентов, для которых вычисляется распределение атрибута.
        attribute (str): Атрибут, для которого вычисляется распределение.

    Returns:
        pd.DataFrame: DataFrame с данными о распределении атрибута.
    """
    ...
```

**Назначение**: Вычисляет распределение заданного атрибута для переданных агентов.

**Параметры**:
- `agents` (list): Список агентов, для которых вычисляется распределение атрибута.
- `attribute` (str): Атрибут, для которого вычисляется распределение.

**Возвращает**:
- `pd.DataFrame`: DataFrame с данными о распределении атрибута. Индекс DataFrame содержит уникальные значения атрибута, а столбец - количество появлений каждого значения.

**Как работает функция**:
- Извлекает значения заданного атрибута из каждого агента в списке `agents`.
- Создает DataFrame из извлеченных значений.
- Вычисляет количество появлений каждого уникального значения атрибута с помощью метода `value_counts()`.
- Сортирует результат по индексу (значению атрибута) с помощью метода `sort_index()`.
- Возвращает полученный DataFrame.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}, {"age": 20, "occupation": "teacher"}]
profiler = Profiler()
age_distribution = profiler._compute_attribute_distribution(agents, "age")
print(age_distribution)
```

### `_plot_attributes_distributions`

```python
def _plot_attributes_distributions(self) -> None:
    """
    Отображает распределения всех атрибутов.
    """
    ...
```

**Назначение**: Отображает распределения всех атрибутов, заданных в `self.attributes`.

**Как работает функция**:
- Итерируется по списку атрибутов `self.attributes`.
- Для каждого атрибута вызывает метод `_plot_attribute_distribution` для отображения распределения атрибута.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}]
profiler = Profiler()
profiler.profile(agents)
profiler._plot_attributes_distributions()
```

### `_plot_attribute_distribution`

```python
def _plot_attribute_distribution(self, attribute: str) -> pd.DataFrame:
    """
    Отображает распределение заданного атрибута.

    Args:
        attribute (str): Атрибут, распределение которого необходимо отобразить.

    Returns:
        pd.DataFrame: DataFrame с данными, использованными для построения графика.
    """
    ...
```

**Назначение**: Отображает распределение заданного атрибута в виде столбчатой диаграммы.

**Параметры**:
- `attribute` (str): Атрибут, распределение которого необходимо отобразить.

**Возвращает**:
- `pd.DataFrame`: DataFrame с данными, использованными для построения графика.

**Как работает функция**:
- Извлекает DataFrame с данными о распределении атрибута из словаря `self.attributes_distributions`.
- Строит столбчатую диаграмму на основе данных DataFrame с заголовком, содержащим название атрибута.
- Отображает график с помощью `plt.show()`.

**Примеры**:
```python
agents = [{"age": 20, "occupation": "student"}, {"age": 30, "occupation": "teacher"}]
profiler = Profiler()
profiler.profile(agents)
profiler._plot_attribute_distribution("age")
```