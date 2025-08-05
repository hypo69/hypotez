# Profiler

## Overview

The module provides mechanisms for creating an understanding of the characteristics of agent populations, such as their age distribution, typical interests, and so on.

## Details

This module is used to analyze and visualize the characteristics of a population of agents. It provides functions for calculating attribute distributions and plotting them. 

## Classes

### `Profiler`

**Description**: The `Profiler` class is responsible for profiling a population of agents by calculating and visualizing attribute distributions.

**Inherits**: N/A

**Attributes**:
- `attributes` (List[str]): A list of attributes to be profiled. Defaults to `["age", "occupation", "nationality"]`.
- `attributes_distributions` (dict): A dictionary that stores the distributions of the attributes. The key is the attribute name, and the value is a Pandas DataFrame.

**Methods**:

- `profile(agents: List[dict]) -> dict`: Profiles the given agents. It calculates the distributions of the attributes for the given agents and stores them in `self.attributes_distributions`.
- `render() -> None`: Renders the profile of the agents by plotting the distributions of the attributes.
- `_compute_attributes_distributions(agents:list) -> dict`: Computes the distributions of the attributes for the given agents. 
- `_compute_attribute_distribution(agents: list, attribute: str) -> pd.DataFrame`: Computes the distribution of a given attribute for the given agents and plots it.
- `_plot_attributes_distributions() -> None`: Plots the distributions of the attributes for the given agents.
- `_plot_attribute_distribution(attribute: str) -> pd.DataFrame`: Plots the distribution of a given attribute for the given agents.

## Class Methods

### `profile(agents: List[dict]) -> dict`

```python
    def profile(self, agents: List[dict]) -> dict:   
        """
        Profiles the given agents.

        Args:
            agents (List[dict]): The agents to be profiled.

        """

        self.attributes_distributions = self._compute_attributes_distributions(agents)
        return self.attributes_distributions
```

**Purpose**: Profiles the given agents by calculating the distributions of the attributes and storing them in `self.attributes_distributions`.

**Parameters**:
- `agents` (List[dict]): The agents to be profiled.

**Returns**:
- `dict`: The distributions of the attributes.

**How the Function Works**:
- The function first calls `self._compute_attributes_distributions(agents)` to calculate the distributions of the attributes.
- Then, it stores the calculated distributions in `self.attributes_distributions` and returns the distributions.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> distributions = profiler.profile(agents)
>>> print(distributions)
{'age':        age
 25    1
 28    1
 30    1
 32    1
 Name: age, dtype: int64, 'occupation':                occupation
 Data Analyst            1
 Data Scientist         1
 Software Engineer      2
 Name: occupation, dtype: int64, 'nationality':       nationality
 Canada         2
 USA           2
 Name: nationality, dtype: int64}
```

### `render() -> None`

```python
    def render(self) -> None:
        """
        Renders the profile of the agents.
        """
        return self._plot_attributes_distributions()
```

**Purpose**: Renders the profile of the agents by plotting the distributions of the attributes.

**Parameters**: None

**Returns**:
- `None`

**How the Function Works**:
- The function calls `self._plot_attributes_distributions()` to plot the distributions of the attributes.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> profiler.profile(agents)
>>> profiler.render()
```

### `_compute_attributes_distributions(agents:list) -> dict`

```python
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
```

**Purpose**: Computes the distributions of the attributes for the given agents.

**Parameters**:
- `agents` (list): The agents whose attributes distributions are to be computed.

**Returns**:
- `dict`: The distributions of the attributes.

**How the Function Works**:
- The function iterates over each attribute in `self.attributes`.
- For each attribute, it calls `self._compute_attribute_distribution(agents, attribute)` to calculate the distribution of that attribute.
- It then stores the calculated distributions in a dictionary called `distributions` and returns it.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> distributions = profiler._compute_attributes_distributions(agents)
>>> print(distributions)
{'age':        age
 25    1
 28    1
 30    1
 32    1
 Name: age, dtype: int64, 'occupation':                occupation
 Data Analyst            1
 Data Scientist         1
 Software Engineer      2
 Name: occupation, dtype: int64, 'nationality':       nationality
 Canada         2
 USA           2
 Name: nationality, dtype: int64}
```

### `_compute_attribute_distribution(agents: list, attribute: str) -> pd.DataFrame`

```python
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
```

**Purpose**: Computes the distribution of a given attribute for the agents and plots it.

**Parameters**:
- `agents` (list): The agents whose attribute distribution is to be plotted.
- `attribute` (str): The attribute whose distribution is to be plotted.

**Returns**:
- `pd.DataFrame`: The data used for plotting.

**How the Function Works**:
- The function first extracts the values of the given attribute from the agents using a list comprehension.
- Then, it creates a Pandas DataFrame from these values and calculates the value counts of each unique attribute value.
- Finally, it sorts the DataFrame by the attribute value and returns it.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> df = profiler._compute_attribute_distribution(agents, "age")
>>> print(df)
        age
 25    1
 28    1
 30    1
 32    1
 Name: age, dtype: int64
```

### `_plot_attributes_distributions() -> None`

```python
    def _plot_attributes_distributions(self) -> None:
        """
        Plots the distributions of the attributes for the agents.
        """

        for attribute in self.attributes:
            self._plot_attribute_distribution(attribute)
```

**Purpose**: Plots the distributions of the attributes for the agents.

**Parameters**: None

**Returns**:
- `None`

**How the Function Works**:
- The function iterates over each attribute in `self.attributes`.
- For each attribute, it calls `self._plot_attribute_distribution(attribute)` to plot the distribution of that attribute.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> profiler.profile(agents)
>>> profiler._plot_attributes_distributions()
```

### `_plot_attribute_distribution(attribute: str) -> pd.DataFrame`

```python
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
```

**Purpose**: Plots the distribution of a given attribute for the agents.

**Parameters**:
- `attribute` (str): The attribute whose distribution is to be plotted.

**Returns**:
- `pd.DataFrame`: The data used for plotting.

**How the Function Works**:
- The function retrieves the distribution of the given attribute from `self.attributes_distributions`.
- Then, it uses Matplotlib to create a bar chart of the distribution.
- The chart's title is set to `f"{attribute.capitalize()} distribution"`.
- Finally, the chart is displayed using `plt.show()`.

**Examples**:

```python
>>> profiler = Profiler()
>>> agents = [
...     {"age": 25, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 30, "occupation": "Data Scientist", "nationality": "Canada"},
...     {"age": 28, "occupation": "Software Engineer", "nationality": "USA"},
...     {"age": 32, "occupation": "Data Analyst", "nationality": "Canada"},
... ]
>>> profiler.profile(agents)
>>> profiler._plot_attribute_distribution("age")
```