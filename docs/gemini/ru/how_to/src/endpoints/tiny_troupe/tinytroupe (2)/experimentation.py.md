### **Как использовать класс `ABRandomizer`**

=========================================================================================

Описание
-------------------------
Класс `ABRandomizer` используется для случайного выбора между двумя вариантами (`a` и `b`) и последующей дерандомизации. Он полезен для A/B-тестирования, где нужно показывать пользователям разные варианты контента и затем анализировать их предпочтения.

Шаги выполнения
-------------------------
1. **Инициализация `ABRandomizer`**:
   - Создайте экземпляр класса `ABRandomizer`, указав имена вариантов и случайное зерно для воспроизводимости.
2. **Рандомизация**:
   - Используйте метод `randomize(i, a, b)`, чтобы случайно переключить варианты `a` и `b` для элемента с индексом `i`.
   - Метод возвращает переставленные варианты и сохраняет информацию о переключении.
3. **Дерандомизация**:
   - Используйте метод `derandomize(i, a, b)`, чтобы восстановить исходный порядок вариантов `a` и `b` для элемента с индексом `i`.
4. **Декодирование выбора пользователя**:
   - Используйте метод `derandomize_name(i, blind_name)`, чтобы определить, какой реальный вариант (`real_name_1` или `real_name_2`) соответствует выбору пользователя (`blind_name`).

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
randomizer = ABRandomizer(real_name_1="control", real_name_2="treatment", 
                            blind_name_a="A", blind_name_b="B", 
                            random_seed=42)

# Рандомизация вариантов для элемента с индексом 1
variant_a = "Option A"
variant_b = "Option B"
randomized_a, randomized_b = randomizer.randomize(1, variant_a, variant_b)
print(f"Randomized: A = {randomized_a}, B = {randomized_b}")

# Дерандомизация вариантов для элемента с индексом 1
derandomized_a, derandomized_b = randomizer.derandomize(1, randomized_a, randomized_b)
print(f"Derandomized: A = {derandomized_a}, B = {derandomized_b}")

# Декодирование выбора пользователя
user_choice = "A"
real_name = randomizer.derandomize_name(1, user_choice)
print(f"User chose {user_choice}, which corresponds to {real_name}")