## Как использовать класс `Profiler`
=========================================================================================

Описание
-------------------------
Класс `Profiler` предназначен для анализа характеристик агентов в популяции. Он позволяет вычислить распределение значений различных атрибутов агентов, таких как возраст, профессия, национальность, и визуализировать эти распределения в виде гистограмм.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте экземпляр класса `Profiler`, указав в качестве аргумента список атрибутов агентов, которые вы хотите анализировать. Например, `profiler = Profiler(attributes=['age', 'occupation', 'nationality'])`.
2. **Профилирование**: Вызовите метод `profile` с списком агентов в качестве аргумента. Метод `profile` вычисляет распределение значений каждого атрибута и сохраняет их в словарь `self.attributes_distributions`.
3. **Визуализация**: Вызовите метод `render` для визуализации распределений атрибутов. Метод `render` рисует гистограммы для каждого атрибута, используя данные, сохраненные в словаре `self.attributes_distributions`.

Пример использования
-------------------------

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.profiling import Profiler

# Создаем список агентов
agents = [
    TinyPerson(age=25, occupation="Engineer", nationality="Russian"),
    TinyPerson(age=30, occupation="Doctor", nationality="American"),
    TinyPerson(age=25, occupation="Teacher", nationality="Russian"),
    TinyPerson(age=40, occupation="Engineer", nationality="American"),
    TinyPerson(age=35, occupation="Doctor", nationality="Russian"),
]

# Создаем экземпляр Profiler
profiler = Profiler(attributes=['age', 'occupation', 'nationality'])

# Вычисляем распределения атрибутов
profiler.profile(agents)

# Визуализируем распределения
profiler.render()
```

В данном примере мы создаем список агентов, затем инициализируем `Profiler`, чтобы анализировать возраст, профессию и национальность. После профилирования агентов, мы вызываем `render` для визуализации полученных распределений.