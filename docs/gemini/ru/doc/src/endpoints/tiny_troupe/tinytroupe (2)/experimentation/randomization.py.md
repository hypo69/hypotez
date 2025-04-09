# Модуль для рандомизации A/B тестов
## Обзор

Модуль предоставляет класс `ABRandomizer`, предназначенный для рандомизации и дерандомизации вариантов в A/B-тестах. Он позволяет временно заменять реальные названия вариантов на условные обозначения, чтобы избежать предвзятости при выборе.

## Подробней

Этот модуль полезен для проведения A/B-тестов, где необходимо случайным образом распределять пользователей между двумя группами (контрольной и тестовой) и затем анализировать результаты, возвращаясь к исходным обозначениям вариантов. Класс `ABRandomizer` хранит информацию о произведенных заменах, что позволяет корректно интерпретировать результаты тестов.

## Классы

### `ABRandomizer`

**Описание**: Класс для рандомизации и дерандомизации вариантов в A/B-тестах.

**Атрибуты**:
- `choices` (dict): Словарь, хранящий информацию о произведенной рандомизации для каждого элемента. Ключом является индекс элемента, значением - кортеж (0, 1) или (1, 0), указывающий, были ли переставлены варианты.
- `real_name_1` (str): Реальное название первого варианта (например, "control").
- `real_name_2` (str): Реальное название второго варианта (например, "treatment").
- `blind_name_a` (str): Условное обозначение первого варианта (например, "A").
- `blind_name_b` (str): Условное обозначение второго варианта (например, "B").
- `passtrough_name` (list): Список названий, которые не подлежат рандомизации и возвращаются без изменений.
- `random_seed` (int): Зерно для генератора случайных чисел, обеспечивающее воспроизводимость рандомизации.

**Принцип работы**:
1.  При инициализации класса задаются реальные и условные названия вариантов, а также зерно для генератора случайных чисел.
2.  Метод `randomize` случайным образом меняет местами два варианта и сохраняет информацию об этом в словаре `choices`.
3.  Метод `derandomize` восстанавливает исходный порядок вариантов на основе информации из словаря `choices`.
4.  Метод `derandomize_name` преобразует условное обозначение варианта обратно в реальное название, используя информацию из словаря `choices`.

**Методы**:
- `__init__`: Инициализация класса `ABRandomizer`.
- `randomize`: Случайная перестановка двух вариантов.
- `derandomize`: Восстановление исходного порядка вариантов.
- `derandomize_name`: Преобразование условного обозначения варианта в реальное название.

## Функции

### `__init__`

```python
def __init__(self, real_name_1="control", real_name_2="treatment",
                       blind_name_a="A", blind_name_b="B",
                       passtrough_name=[],
                       random_seed=42):
    """
    An utility class to randomize between two options, and de-randomize later.
    The choices are stored in a dictionary, with the index of the item as the key.
    The real names are the names of the options as they are in the data, and the blind names
    are the names of the options as they are presented to the user. Finally, the passtrough names
    are names that are not randomized, but are always returned as-is.\n
    Args:\n
        real_name_1 (str): the name of the first option\n
        real_name_2 (str): the name of the second option\n
        blind_name_a (str): the name of the first option as seen by the user\n
        blind_name_b (str): the name of the second option as seen by the user\n
        passtrough_name (list): a list of names that should not be randomized and are always\n
                                returned as-is.\n
        random_seed (int): the random seed to use
    """
```

**Назначение**: Инициализация экземпляра класса `ABRandomizer`.

**Параметры**:
- `real_name_1` (str): Реальное название первого варианта (по умолчанию "control").
- `real_name_2` (str): Реальное название второго варианта (по умолчанию "treatment").
- `blind_name_a` (str): Условное обозначение первого варианта (по умолчанию "A").
- `blind_name_b` (str): Условное обозначение второго варианта (по умолчанию "B").
- `passtrough_name` (list): Список названий, которые не подлежат рандомизации (по умолчанию пустой список `[]`).
- `random_seed` (int): Зерно для генератора случайных чисел (по умолчанию 42).

**Как работает функция**:
1.  Инициализирует словарь `self.choices` для хранения информации о рандомизации.
2.  Сохраняет реальные и условные названия вариантов, а также зерно для генератора случайных чисел в атрибутах экземпляра класса.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1="контроль", real_name_2="тест", blind_name_a="A", blind_name_b="B", passtrough_name=["pass"], random_seed=123)
```

### `randomize`

```python
def randomize(self, i, a, b):
    """
    Randomly switch between a and b, and return the choices.
    Store whether the a and b were switched or not for item i, to be able to
    de-randomize later.\n
    Args:\n
        i (int): index of the item\n
        a (str): first choice\n
        b (str): second choice
    """
    # use the seed
    if random.Random(self.random_seed).random() < 0.5:
        self.choices[i] = (0, 1)
        return a, b
        
    else:
        self.choices[i] = (1, 0)
        return b, a
```

**Назначение**: Случайная перестановка двух вариантов.

**Параметры**:
- `i` (int): Индекс элемента.
- `a` (str): Первый вариант.
- `b` (str): Второй вариант.

**Возвращает**:
- Кортеж из двух элементов, содержащий варианты `a` и `b` в случайном порядке.

**Как работает функция**:
1.  Использует генератор случайных чисел с заданным зерном (`self.random_seed`) для определения, нужно ли менять местами варианты `a` и `b`.
2.  Если случайное число меньше 0.5, варианты остаются в исходном порядке, и в словарь `self.choices` записывается кортеж `(0, 1)`.
3.  В противном случае варианты меняются местами, и в словарь `self.choices` записывается кортеж `(1, 0)`.
4.  Возвращает кортеж из двух элементов, содержащий варианты `a` и `b` в случайном порядке.

**Примеры**:

```python
randomizer = ABRandomizer()
a, b = randomizer.randomize(0, "контроль", "тест")
print(f"Вариант A: {a}, Вариант B: {b}")
```

### `derandomize`

```python
def derandomize(self, i, a, b):
    """
    De-randomize the choices for item i, and return the choices.\n
    Args:\n
        i (int): index of the item\n
        a (str): first choice\n
        b (str): second choice
    """
    if self.choices[i] == (0, 1):
        return a, b
    elif self.choices[i] == (1, 0):
        return b, a
    else:
        raise Exception(f"No randomization found for item {i}")
```

**Назначение**: Восстановление исходного порядка вариантов.

**Параметры**:
- `i` (int): Индекс элемента.
- `a` (str): Первый вариант.
- `b` (str): Второй вариант.

**Возвращает**:
- Кортеж из двух элементов, содержащий варианты `a` и `b` в исходном порядке.

**Вызывает исключения**:
- `Exception`: Если для элемента `i` не найдена информация о рандомизации.

**Как работает функция**:
1.  Проверяет значение в словаре `self.choices` для элемента `i`.
2.  Если значение равно `(0, 1)`, возвращает варианты `a` и `b` в исходном порядке.
3.  Если значение равно `(1, 0)`, возвращает варианты `b` и `a` (меняет их местами).
4.  Если для элемента `i` не найдена информация о рандомизации, выбрасывает исключение `Exception`.

**Примеры**:

```python
randomizer = ABRandomizer()
a, b = randomizer.randomize(0, "контроль", "тест")
a, b = randomizer.derandomize(0, a, b)
print(f"Вариант A: {a}, Вариант B: {b}")
```

### `derandomize_name`

```python
def derandomize_name(self, i, blind_name):
    """
    Decode the choice made by the user, and return the choice. \n
    Args:\n
        i (int): index of the item\n
        choice_name (str): the choice made by the user
    """
    # was the choice i randomized?
    if self.choices[i] == (0, 1):
        # no, so return the choice
        if blind_name == self.blind_name_a:
            return self.real_name_1
        elif blind_name == self.blind_name_b:
            return self.real_name_2
        elif blind_name in self.passtrough_name:
            return blind_name
        else:
            raise Exception(f"Choice \'{blind_name}\' not recognized")
        
    elif self.choices[i] == (1, 0):
        # yes, it was randomized, so return the opposite choice
        if blind_name == self.blind_name_a:
            return self.real_name_2
        elif blind_name == self.blind_name_b:
            return self.real_name_1
        elif blind_name in self.passtrough_name:
            return blind_name
        else:
            raise Exception(f"Choice \'{blind_name}\' not recognized")
    else:
        raise Exception(f"No randomization found for item {i}")
```

**Назначение**: Преобразование условного обозначения варианта в реальное название.

**Параметры**:
- `i` (int): Индекс элемента.
- `blind_name` (str): Условное обозначение варианта.

**Возвращает**:
- Реальное название варианта.

**Вызывает исключения**:
- `Exception`: Если для элемента `i` не найдена информация о рандомизации.
- `Exception`: Если условное обозначение варианта не распознано.

**Как работает функция**:
1.  Проверяет значение в словаре `self.choices` для элемента `i`.
2.  Если значение равно `(0, 1)`, это означает, что варианты не были переставлены.
    -   Если `blind_name` соответствует `self.blind_name_a`, возвращает `self.real_name_1`.
    -   Если `blind_name` соответствует `self.blind_name_b`, возвращает `self.real_name_2`.
    -   Если `blind_name` находится в списке `self.passtrough_name`, возвращает `blind_name` без изменений.
    -   В противном случае выбрасывает исключение `Exception`.
3.  Если значение равно `(1, 0)`, это означает, что варианты были переставлены.
    -   Если `blind_name` соответствует `self.blind_name_a`, возвращает `self.real_name_2`.
    -   Если `blind_name` соответствует `self.blind_name_b`, возвращает `self.real_name_1`.
    -   Если `blind_name` находится в списке `self.passtrough_name`, возвращает `blind_name` без изменений.
    -   В противном случае выбрасывает исключение `Exception`.
4.  Если для элемента `i` не найдена информация о рандомизации, выбрасывает исключение `Exception`.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1="контроль", real_name_2="тест", blind_name_a="A", blind_name_b="B")
randomizer.randomize(0, "A", "B")
real_name = randomizer.derandomize_name(0, "A")
print(f"Реальное название варианта: {real_name}")
```
```
A
↓
проверка рандомизации (choices[i])
↓
нет (0, 1) → проверка blind_name
↓
blind_name == blind_name_a → возврат real_name_1
↓
да (1, 0) → проверка blind_name
↓
blind_name == blind_name_a → возврат real_name_2
↓
исключение (если нет информации о рандомизации или blind_name не распознан)