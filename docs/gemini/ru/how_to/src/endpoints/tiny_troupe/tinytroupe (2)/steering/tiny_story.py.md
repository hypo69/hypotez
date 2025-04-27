## Как использовать класс `TinyStory`
=========================================================================================

Описание
-------------------------
Класс `TinyStory` используется для создания и управления историей, связанной с симуляциями в TinyTroupe. Он может создавать истории об агенте или среде, используя заданную цель и контекст. 

Шаги выполнения
-------------------------
1. **Инициализация**: 
    - Создайте экземпляр класса `TinyStory`, передав в конструктор объект `TinyWorld` (среда) или `TinyPerson` (агент), а также цель истории (`purpose`), контекст (`context`), количество первых и последних взаимодействий (`first_n`, `last_n`) и флаг, указывающий, нужно ли включать информацию об упущенных взаимодействиях (`include_omission_info`).
2. **Начало истории**: 
    - Вызовите метод `start_story()`, чтобы начать новую историю. Передайте в него требования к истории (`requirements`), желаемое количество слов (`number_of_words`) и флаг, указывающий, нужно ли включать неожиданный поворот в сюжет (`include_plot_twist`).
3. **Продолжение истории**: 
    - Вызовите метод `continue_story()`, чтобы предложить продолжение истории. Параметры метода аналогичны параметрам `start_story()`.
4. **Получение текущей истории**: 
    - Метод `_current_story()` возвращает текущую историю, включая контекст и историю взаимодействий.

Пример использования
-------------------------

```python
from tinytroupe.extraction import logger
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from tinytroupe.steering.tiny_story import TinyStory

# Создаем агента и среду
agent = TinyPerson(name="Alice", age=30, job="Software Engineer")
environment = TinyWorld(name="City", description="A bustling city with diverse population and vibrant culture.")

# Создаем историю об агенте
story = TinyStory(agent=agent, purpose="Tell a story about a software engineer who moves to a new city.", context="Once upon a time...")

# Начинаем историю
start = story.start_story(requirements="The story should start with Alice arriving in the city and finding a place to live.", number_of_words=100)

# Печатаем начало истории
print(start)

# Продолжаем историю
continuation = story.continue_story(requirements="Alice meets a new friend in the city who helps her navigate the new environment.")

# Печатаем продолжение истории
print(continuation)

# Получаем текущую историю
current_story = story._current_story()

# Печатаем текущую историю
print(current_story)
```