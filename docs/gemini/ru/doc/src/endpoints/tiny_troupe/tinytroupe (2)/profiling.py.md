# Модуль профилирования агентов

## Обзор

Модуль `profiling.py` предоставляет механизмы для создания и понимания характеристик популяции агентов, таких как возрастное распределение, типичные интересы и так далее.

## Подробности

Этот модуль используется для анализа характеристик набора агентов. Он предоставляет методы для подсчета распределения различных атрибутов (например, возраст, профессия, национальность) в популяции агентов. 

## Классы

### `Profiler`

**Описание**: Класс `Profiler`  предназначен для профилирования популяции агентов.

**Наследует**:  Этот класс не наследует другие классы.

**Атрибуты**:
 - `attributes` (List[str]): Список атрибутов, которые будут профилированы. По умолчанию включает в себя "age", "occupation", "nationality".
 - `attributes_distributions` (dict): Словарь, хранящий распределения атрибутов. Ключи словаря - имена атрибутов, а значения - DataFrame'ы с подсчетом значений атрибутов.

**Методы**:

#### `profile`

**Назначение**: Выполняет профилирование заданной популяции агентов.

**Параметры**:
 - `agents` (List[dict]): Список агентов, которые будут профилированы.

**Возвращает**:
 - `dict`: Словарь с распределениями атрибутов.

**Пример**:

```python
# Пример использования 
agents = [
    {'age': 25, 'occupation': 'Software Engineer', 'nationality': 'US'},
    {'age': 30, 'occupation': 'Data Scientist', 'nationality': 'CA'},
    {'age': 28, 'occupation': 'Software Engineer', 'nationality': 'US'}
]
profiler = Profiler()
distributions = profiler.profile(agents)
print(distributions) # Вывод: {'age': ..., 'occupation': ..., 'nationality': ...}
```

#### `render`

**Назначение**:  Отображает графически результаты профилирования.

**Параметры**:  
 - Нет

**Возвращает**:
 - `None` 

**Пример**:

```python
# Пример использования
profiler.render() # Отображает графики распределений атрибутов
```

#### `_compute_attributes_distributions`

**Назначение**: Вычисляет распределение атрибутов для заданной популяции агентов.

**Параметры**:
 - `agents` (list): Список агентов, для которых нужно вычислить распределение атрибутов.

**Возвращает**:
 - `dict`: Словарь с распределениями атрибутов.

**Пример**:

```python
# Пример использования
agents = [
    {'age': 25, 'occupation': 'Software Engineer', 'nationality': 'US'},
    {'age': 30, 'occupation': 'Data Scientist', 'nationality': 'CA'},
    {'age': 28, 'occupation': 'Software Engineer', 'nationality': 'US'}
]
distributions = profiler._compute_attributes_distributions(agents)
print(distributions) # Вывод: {'age': ..., 'occupation': ..., 'nationality': ...}
```

#### `_compute_attribute_distribution`

**Назначение**: Вычисляет распределение заданного атрибута для агентов.

**Параметры**:
 - `agents` (list): Список агентов, для которых нужно вычислить распределение атрибута.
 - `attribute` (str): Имя атрибута, для которого нужно вычислить распределение.

**Возвращает**:
 - `pd.DataFrame`: DataFrame с подсчетом значений атрибута.

**Пример**:

```python
# Пример использования
agents = [
    {'age': 25, 'occupation': 'Software Engineer', 'nationality': 'US'},
    {'age': 30, 'occupation': 'Data Scientist', 'nationality': 'CA'},
    {'age': 28, 'occupation': 'Software Engineer', 'nationality': 'US'}
]
age_distribution = profiler._compute_attribute_distribution(agents, 'age')
print(age_distribution) 
```

#### `_plot_attributes_distributions`

**Назначение**: Строит графики распределений атрибутов.

**Параметры**:
 -  Нет

**Возвращает**:
 - `None`

**Пример**:

```python
# Пример использования
profiler._plot_attributes_distributions() # Строит графики распределений атрибутов
```

#### `_plot_attribute_distribution`

**Назначение**: Строит график распределения заданного атрибута.

**Параметры**:
 - `attribute` (str): Имя атрибута, для которого нужно построить график.

**Возвращает**:
 - `pd.DataFrame`: DataFrame с данными, использованными для построения графика.

**Пример**:

```python
# Пример использования
profiler._plot_attribute_distribution('age') # Строит график распределения возраста 
```

## Примеры

```python
# Пример создания Profiler и профилирования агентов
from tinytroupe.agent import TinyPerson
from tinytroupe.profiling import Profiler

# Создание агентов
agents = [TinyPerson(age=25, occupation='Software Engineer', nationality='US'),
          TinyPerson(age=30, occupation='Data Scientist', nationality='CA'),
          TinyPerson(age=28, occupation='Software Engineer', nationality='US')]

# Создание профилировщика
profiler = Profiler()

# Профилирование агентов
distributions = profiler.profile([agent.to_dict() for agent in agents]) 

# Отображение графика распределения возраста
profiler._plot_attribute_distribution('age')
```

```python
# Профилирование популяции агентов и построение графика распределения возраста
from tinytroupe.agent import TinyPerson
from tinytroupe.profiling import Profiler
from tinytroupe.agent_population import AgentPopulation

# Создание популяции агентов
population = AgentPopulation(size=100, seed=42)

# Профилирование популяции
profiler = Profiler(attributes=['age', 'occupation', 'nationality'])
profiler.profile(population.agents)

# Построение графика распределения возраста
profiler._plot_attribute_distribution('age')
```

```python
# Профилирование агентов с использованием собственных атрибутов
from tinytroupe.agent import TinyPerson
from tinytroupe.profiling import Profiler

# Создание агентов с дополнительными атрибутами
agents = [TinyPerson(age=25, occupation='Software Engineer', nationality='US', hobby='Coding'),
          TinyPerson(age=30, occupation='Data Scientist', nationality='CA', hobby='Hiking'),
          TinyPerson(age=28, occupation='Software Engineer', nationality='US', hobby='Music')]

# Создание профилировщика с указанием дополнительных атрибутов
profiler = Profiler(attributes=['age', 'occupation', 'nationality', 'hobby'])

# Профилирование агентов
profiler.profile([agent.to_dict() for agent in agents])

# Построение графика распределения хобби
profiler._plot_attribute_distribution('hobby')