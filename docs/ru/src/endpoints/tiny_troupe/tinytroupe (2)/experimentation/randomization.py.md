# Модуль для рандомизации A/B-тестов

## Обзор

Модуль `randomization.py` предоставляет утилитарный класс `ABRandomizer` для проведения A/B-тестирования, позволяя рандомизировать варианты и восстанавливать исходные данные после проведения тестов. Класс предназначен для упрощения процесса A/B-тестирования, обеспечивая сохранение и восстановление информации о рандомизации.

## Подробнее

Класс `ABRandomizer` позволяет инициализировать параметры A/B-теста, такие как имена контрольной и тестовой групп, а также имена, используемые для представления этих групп пользователю. Это позволяет абстрагироваться от реальных названий вариантов и представлять их в более понятном виде. Также поддерживается список названий, которые не должны быть рандомизированы.

## Классы

### `ABRandomizer`

**Описание**: Класс для рандомизации между двумя вариантами в A/B-тестах и последующей дерандомизации.

**Атрибуты**:

-   `choices` (dict): Словарь, хранящий информацию о том, какие варианты были переключены для каждого элемента. Ключом является индекс элемента.
-   `real_name_1` (str): Название первого варианта (контрольная группа).
-   `real_name_2` (str): Название второго варианта (тестовая группа).
-   `blind_name_a` (str): Название первого варианта, отображаемое пользователю.
-   `blind_name_b` (str): Название второго варианта, отображаемое пользователю.
-   `passtrough_name` (list): Список названий, которые не должны быть рандомизированы.
-   `random_seed` (int): Зерно для генератора случайных чисел, обеспечивающее воспроизводимость результатов.

**Методы**:

-   `__init__(real_name_1, real_name_2, blind_name_a, blind_name_b, passtrough_name, random_seed)`: Инициализирует экземпляр класса `ABRandomizer`.
-   `randomize(i, a, b)`: Случайным образом переключает варианты `a` и `b` и возвращает их.
-   `derandomize(i, a, b)`: Возвращает варианты `a` и `b` в исходном порядке, основываясь на информации о рандомизации.
-   `derandomize_name(i, blind_name)`: Декодирует выбор, сделанный пользователем, и возвращает соответствующее реальное имя варианта.

### `__init__(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=[], random_seed=42)`

**Назначение**: Инициализирует класс `ABRandomizer` с заданными параметрами.

**Параметры**:

-   `real_name_1` (str, optional): Название первого варианта (контроль). По умолчанию `"control"`.
-   `real_name_2` (str, optional): Название второго варианта (тест). По умолчанию `"treatment"`.
-   `blind_name_a` (str, optional): Имя, отображаемое для первого варианта. По умолчанию `"A"`.
-   `blind_name_b` (str, optional): Имя, отображаемое для второго варианта. По умолчанию `"B"`.
-   `passtrough_name` (list, optional): Список имен, которые не нужно рандомизировать. По умолчанию `[]`.
-   `random_seed` (int, optional): Зерно для рандомизации. По умолчанию `42`.

**Как работает функция**:

-   Функция инициализирует атрибуты экземпляра класса, сохраняя переданные значения.
-   `self.choices` инициализируется как пустой словарь для хранения информации о рандомизации.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=[], random_seed=42)
```

### `randomize(i: int, a: str, b: str) -> tuple[str, str]`

**Назначение**: Рандомизирует порядок двух вариантов (`a` и `b`) на основе заданного зерна случайных чисел и сохраняет информацию о переключении для последующей дерандомизации.

**Параметры**:

-   `i` (int): Индекс элемента, для которого выполняется рандомизация. Используется как ключ для сохранения информации о переключении в словаре `self.choices`.
-   `a` (str): Первый вариант.
-   `b` (str): Второй вариант.

**Возвращает**:

-   `tuple[str, str]`: Кортеж, содержащий варианты `a` и `b` в случайном порядке.

**Как работает функция**:

-   Функция использует генератор случайных чисел с фиксированным зерном (`self.random_seed`) для обеспечения воспроизводимости результатов.
-   Если случайное число меньше 0.5, варианты `a` и `b` возвращаются в исходном порядке, и в словаре `self.choices` сохраняется значение `(0, 1)` для индекса `i`.
-   В противном случае варианты `a` и `b` меняются местами, и в словаре `self.choices` сохраняется значение `(1, 0)` для индекса `i`.

**Примеры**:

```python
randomizer = ABRandomizer(random_seed=42)
a, b = randomizer.randomize(1, "Option A", "Option B")
print(f"Рандомизированные варианты: a={a}, b={b}")
```

### `derandomize(i: int, a: str, b: str) -> tuple[str, str]`

**Назначение**: Возвращает исходный порядок двух вариантов (`a` и `b`) на основе информации о рандомизации, сохраненной в словаре `self.choices`.

**Параметры**:

-   `i` (int): Индекс элемента, для которого выполняется дерандомизация. Используется как ключ для получения информации о переключении из словаря `self.choices`.
-   `a` (str): Первый вариант.
-   `b` (str): Второй вариант.

**Возвращает**:

-   `tuple[str, str]`: Кортеж, содержащий варианты `a` и `b` в исходном порядке.

**Вызывает исключения**:

-   `Exception`: Если для данного индекса `i` не найдена информация о рандомизации в словаре `self.choices`.

**Как работает функция**:

-   Функция проверяет значение, сохраненное в словаре `self.choices` для индекса `i`.
-   Если значение равно `(0, 1)`, варианты `a` и `b` возвращаются в исходном порядке.
-   Если значение равно `(1, 0)`, варианты `b` и `a` меняются местами и возвращаются.
-   Если для индекса `i` не найдено информации о рандомизации, вызывается исключение.

**Примеры**:

```python
randomizer = ABRandomizer(random_seed=42)
a, b = randomizer.randomize(1, "Option A", "Option B")
original_a, original_b = randomizer.derandomize(1, a, b)
print(f"Исходные варианты: a={original_a}, b={original_b}")
```

### `derandomize_name(i: int, blind_name: str) -> str`

**Назначение**: Декодирует выбор пользователя на основе "слепого" имени варианта и возвращает соответствующее реальное имя варианта.

**Параметры**:

-   `i` (int): Индекс элемента, для которого выполняется дерандомизация. Используется как ключ для получения информации о переключении из словаря `self.choices`.
-   `blind_name` (str): "Слепое" имя варианта, выбранного пользователем (например, `"A"` или `"B"`).

**Возвращает**:

-   `str`: Реальное имя варианта (например, `"control"` или `"treatment"`).

**Вызывает исключения**:

-   `Exception`: Если для данного индекса `i` не найдена информация о рандомизации в словаре `self.choices`.
-   `Exception`: Если переданное "слепое" имя варианта не распознано.

**Как работает функция**:

-   Функция проверяет значение, сохраненное в словаре `self.choices` для индекса `i`.
-   Если значение равно `(0, 1)`, это означает, что рандомизации не было. Функция проверяет, какому "слепому" имени (`self.blind_name_a` или `self.blind_name_b`) соответствует переданное `blind_name`, и возвращает соответствующее реальное имя (`self.real_name_1` или `self.real_name_2`). Если `blind_name` находится в списке `self.passtrough_name`, возвращается `blind_name` без изменений.
-   Если значение равно `(1, 0)`, это означает, что была выполнена рандомизация. Функция выполняет те же проверки, что и в предыдущем случае, но возвращает противоположные реальные имена.
-   Если для индекса `i` не найдено информации о рандомизации, или если переданное "слепое" имя варианта не распознано, вызывается исключение.

**Примеры**:

```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", random_seed=42)
randomizer.randomize(1, "A", "B")
real_name = randomizer.derandomize_name(1, "A")
print(f"Реальное имя варианта: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.randomize(1, "A", "B")
real_name = randomizer.derandomize_name(1, "C")
print(f"Реальное имя варианта: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
real_name = randomizer.derandomize_name(1, "C")
print(f"Реальное имя варианта: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", random_seed=42)
try:
    real_name = randomizer.derandomize_name(1, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", random_seed=42)
randomizer.randomize(1, "A", "B")
try:
    real_name = randomizer.derandomize_name(2, "A")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", random_seed=42)
try:
    real_name = randomizer.derandomize_name(2, "A")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
try:
    real_name = randomizer.derandomize_name(1, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
try:
    real_name = randomizer.derandomize_name(2, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.choices[1] = (0, 1)

real_name = randomizer.derandomize_name(1, "A")
print(f"Произошла ошибка: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.choices[1] = (0, 1)

real_name = randomizer.derandomize_name(1, "B")
print(f"Произошла ошибка: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.choices[1] = (1, 0)

real_name = randomizer.derandomize_name(1, "A")
print(f"Произошла ошибка: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.choices[1] = (1, 0)

real_name = randomizer.derandomize_name(1, "B")
print(f"Произошла ошибка: {real_name}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
randomizer.choices[1] = (1, 0)
try:
    real_name = randomizer.derandomize_name(1, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", passtrough_name=["C"], random_seed=42)
try:
    real_name = randomizer.derandomize_name(1, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```
```python
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", blind_name_a="A", blind_name_b="B", random_seed=42)
randomizer.choices[1] = (1, 0)
try:
    real_name = randomizer.derandomize_name(1, "C")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```

```
```
```
```
```
```
```
```
```
```
```
```
```