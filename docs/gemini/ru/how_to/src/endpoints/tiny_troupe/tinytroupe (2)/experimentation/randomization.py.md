### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Класс `ABRandomizer` предоставляет функциональность для проведения A/B-тестирования, позволяя случайным образом назначать один из двух вариантов (control/treatment) для каждого элемента (например, пользователя) и сохранять информацию о сделанном выборе для последующей дерандомизации. Этот класс полезен, когда необходимо представить пользователям варианты A и B в случайном порядке, а затем анализировать результаты, зная, какой вариант был показан каждому пользователю. Также поддерживаются "сквозные" имена, которые не подвергаются рандомизации.

Шаги выполнения
-------------------------
1. **Инициализация класса `ABRandomizer`**:
   - Создайте экземпляр класса `ABRandomizer`, указав имена для вариантов A и B (как реальные, так и "слепые"), а также список "сквозных" имен, если необходимо.
   - Пример:
     ```python
     randomizer = ABRandomizer(real_name_1="control_group", real_name_2="treatment_group",
                                blind_name_a="Вариант A", blind_name_b="Вариант B",
                                passtrough_name=["Не рандомизировать"], random_seed=123)
     ```

2. **Рандомизация вариантов с использованием метода `randomize`**:
   - Для каждого элемента, который нужно рандомизировать, вызовите метод `randomize`, передав индекс элемента и два варианта (A и B).
   - Метод случайным образом выбирает порядок вариантов и возвращает их. Информация о сделанном выборе сохраняется для последующей дерандомизации.
   - Пример:
     ```python
     index = 1
     variant_a = "Значение A"
     variant_b = "Значение B"
     randomized_a, randomized_b = randomizer.randomize(index, variant_a, variant_b)
     print(f"Рандомизированные варианты для элемента {index}: A = {randomized_a}, B = {randomized_b}")
     ```

3. **Дерандомизация вариантов с использованием метода `derandomize`**:
   - После того, как пользователи сделали свой выбор, используйте метод `derandomize`, чтобы восстановить исходный порядок вариантов для каждого элемента.
   - Метод возвращает исходные варианты в правильном порядке на основе информации, сохраненной при рандомизации.
   - Пример:
     ```python
     index = 1
     derandomized_a, derandomized_b = randomizer.derandomize(index, randomized_a, randomized_b)
     print(f"Дерандомизированные варианты для элемента {index}: A = {derandomized_a}, B = {derandomized_b}")
     ```

4. **Декодирование выбора пользователя с использованием метода `derandomize_name`**:
   - Если необходимо узнать, какой реальный вариант соответствует выбору пользователя (сделанному на основе "слепых" имен), используйте метод `derandomize_name`.
   - Метод возвращает реальное имя варианта на основе выбора пользователя и информации о рандомизации.
   - Пример:
     ```python
     index = 1
     user_choice = "Вариант A"  # Предположим, что пользователь выбрал "Вариант A"
     real_choice = randomizer.derandomize_name(index, user_choice)
     print(f"Реальный выбор пользователя для элемента {index}: {real_choice}")
     ```

Пример использования
-------------------------

```python
import random
import pandas as pd
from tinytroupe.agent import TinyPerson

class ABRandomizer():

    def __init__(self, real_name_1="control", real_name_2="treatment",
                       blind_name_a="A", blind_name_b="B",
                       passtrough_name=[],
                       random_seed=42):
        """
        An utility class to randomize between two options, and de-randomize later.
        The choices are stored in a dictionary, with the index of the item as the key.
        The real names are the names of the options as they are in the data, and the blind names
        are the names of the options as they are presented to the user. Finally, the passtrough names
        are names that are not randomized, but are always returned as-is.

        Args:
            real_name_1 (str): the name of the first option
            real_name_2 (str): the name of the second option
            blind_name_a (str): the name of the first option as seen by the user
            blind_name_b (str): the name of the second option as seen by the user
            passtrough_name (list): a list of names that should not be randomized and are always
                                    returned as-is.
            random_seed (int): the random seed to use
        """

        self.choices = {}
        self.real_name_1 = real_name_1
        self.real_name_2 = real_name_2
        self.blind_name_a = blind_name_a
        self.blind_name_b = blind_name_b
        self.passtrough_name = passtrough_name
        self.random_seed = random_seed

    def randomize(self, i, a, b):
        """
        Randomly switch between a and b, and return the choices.
        Store whether the a and b were switched or not for item i, to be able to
        de-randomize later.

        Args:
            i (int): index of the item
            a (str): first choice
            b (str): second choice
        """
        # use the seed
        if random.Random(self.random_seed).random() < 0.5:
            self.choices[i] = (0, 1)
            return a, b
            
        else:
            self.choices[i] = (1, 0)
            return b, a
    
    def derandomize(self, i, a, b):
        """
        De-randomize the choices for item i, and return the choices.

        Args:
            i (int): index of the item
            a (str): first choice
            b (str): second choice
        """
        if self.choices[i] == (0, 1):
            return a, b
        elif self.choices[i] == (1, 0):
            return b, a
        else:
            raise Exception(f"No randomization found for item {i}")
    
    def derandomize_name(self, i, blind_name):
        """
        Decode the choice made by the user, and return the choice. 

        Args:
            i (int): index of the item
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

# Пример использования ABRandomizer
randomizer = ABRandomizer(real_name_1="control_group", real_name_2="treatment_group",
                            blind_name_a="Вариант A", blind_name_b="Вариант B",
                            passtrough_name=["Не рандомизировать"], random_seed=123)

# Рандомизация вариантов
index = 1
variant_a = "Значение A"
variant_b = "Значение B"
randomized_a, randomized_b = randomizer.randomize(index, variant_a, variant_b)
print(f"Рандомизированные варианты для элемента {index}: A = {randomized_a}, B = {randomized_b}")

# Дерандомизация вариантов
derandomized_a, derandomized_b = randomizer.derandomize(index, randomized_a, randomized_b)
print(f"Дерандомизированные варианты для элемента {index}: A = {derandomized_a}, B = {derandomized_b}")

# Декодирование выбора пользователя
user_choice = "Вариант A"  # Предположим, что пользователь выбрал "Вариант A"
real_choice = randomizer.derandomize_name(index, user_choice)
print(f"Реальный выбор пользователя для элемента {index}: {real_choice}")