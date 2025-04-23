### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный код предоставляет класс `Profiler` для анализа и визуализации характеристик популяции агентов, таких как распределение возраста, типичные интересы и национальности. Он вычисляет распределение атрибутов агентов и отображает их в виде графиков.

Шаги выполнения
-------------------------
1. **Инициализация класса `Profiler`**:
   - Создание экземпляра класса `Profiler` с указанием списка атрибутов для анализа. Если список атрибутов не указан, используются значения по умолчанию: `["age", "occupation", "nationality"]`.
   - В конструкторе инициализируется атрибут `attributes` списком переданных атрибутов и атрибут `attributes_distributions` как пустой словарь, в котором будут храниться распределения атрибутов.

2. **Профилирование агентов**:
   - Вызов метода `profile` с передачей списка агентов (словарей) для анализа.
   - Метод `profile` вызывает метод `_compute_attributes_distributions` для вычисления распределений атрибутов агентов.
   - Возвращается словарь `attributes_distributions`, содержащий распределения атрибутов.

3. **Вычисление распределений атрибутов**:
   - Метод `_compute_attributes_distributions` перебирает атрибуты из списка `self.attributes` и для каждого атрибута вызывает метод `_compute_attribute_distribution`.
   - Результаты вычислений сохраняются в словаре `distributions`.

4. **Вычисление распределения атрибута**:
   - Метод `_compute_attribute_distribution` извлекает значения атрибута из каждого агента.
   - Создается Pandas DataFrame на основе полученных значений и вычисляется частота встречаемости каждого значения атрибута с помощью метода `value_counts()`.
   - DataFrame сортируется по индексу (значению атрибута) и возвращается.

5. **Отображение профиля агентов**:
   - Вызов метода `render` для отображения графиков распределения атрибутов.
   - Метод `render` вызывает метод `_plot_attributes_distributions`.

6. **Построение графиков распределения атрибутов**:
   - Метод `_plot_attributes_distributions` перебирает атрибуты из списка `self.attributes` и для каждого атрибута вызывает метод `_plot_attribute_distribution`.

7. **Построение графика распределения атрибута**:
   - Метод `_plot_attribute_distribution` извлекает DataFrame с распределением атрибута из словаря `self.attributes_distributions`.
   - Строится столбчатая диаграмма (bar plot) на основе DataFrame с использованием `matplotlib.pyplot`.
   - Отображается заголовок графика, содержащий название атрибута.
   - График отображается с помощью `plt.show()`.

Пример использования
-------------------------

```python
    import pandas as pd
    import matplotlib.pyplot as plt
    from typing import List


    class Profiler:

        def __init__(self, attributes: List[str]=["age", "occupation", "nationality"]) -> None: 
            self.attributes = attributes
            
            self.attributes_distributions = {} # attribute -> Dataframe

        def profile(self, agents: List[dict]) -> dict:   
            """
            Profiles the given agents.

            Args:
                agents (List[dict]): The agents to be profiled.
            
            """

            self.attributes_distributions = self._compute_attributes_distributions(agents)
            return self.attributes_distributions

        def render(self) -> None:
            """
            Renders the profile of the agents.
            """
            return self._plot_attributes_distributions()
            

        def _compute_attributes_distributions(self, agents:list) -> dict:
            """
            Computes the distributions of the attributes for the agents.

            Args:
                agents (list): The agents whose attributes distributions are to be computed.
            
            Returns:
                dict: The distributions of the attributes.
            """
            distributions = {}
            for attribute in self.attributes:
                distributions[attribute] = self._compute_attribute_distribution(agents, attribute)
            
            return distributions
        
        def _compute_attribute_distribution(self, agents: list, attribute: str) -> pd.DataFrame:
            """
            Computes the distribution of a given attribute for the agents and plots it.

            Args:
                agents (list): The agents whose attribute distribution is to be plotted.
            
            Returns:
                pd.DataFrame: The data used for plotting.
            """
            values = [agent.get(attribute) for agent in agents]

            # corresponding dataframe of the value counts. Must be ordered by value, not counts 
            df = pd.DataFrame(values, columns=[attribute]).value_counts().sort_index()

            return df
        
        def _plot_attributes_distributions(self) -> None:
            """
            Plots the distributions of the attributes for the agents.
            """

            for attribute in self.attributes:
                self._plot_attribute_distribution(attribute)
            
        def _plot_attribute_distribution(self, attribute: str) -> pd.DataFrame:
            """
            Plots the distribution of a given attribute for the agents.

            Args:
                attribute (str): The attribute whose distribution is to be plotted.
            
            Returns:
                pd.DataFrame: The data used for plotting.
            """

            df = self.attributes_distributions[attribute]
            df.plot(kind='bar', title=f"{attribute.capitalize()} distribution")
            plt.show()
    
    # Пример использования:
    agents = [
        {"age": 25, "occupation": "engineer", "nationality": "USA"},
        {"age": 30, "occupation": "doctor", "nationality": "Canada"},
        {"age": 25, "occupation": "teacher", "nationality": "USA"},
        {"age": 35, "occupation": "engineer", "nationality": "UK"},
    ]

    profiler = Profiler(attributes=["age", "occupation", "nationality"])
    profiler.profile(agents)
    profiler.render()