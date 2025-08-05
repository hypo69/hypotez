## Как использовать класс TinyStory
=========================================================================================

Описание
-------------------------
Класс `TinyStory` предоставляет механизмы для создания историй, связанных с симуляциями TinyTroupe. Он позволяет создавать истории, которые описывают взаимодействие агентов и окружения, в том числе задавать цель для истории и задавать контекст, который учитывается при генерации текста.

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте объект `TinyStory`.
    - Укажите `environment` (окружение) или `agent` (агента), о котором будет история. 
    - Укажите `purpose` (цель) истории.
    - Дополнительно можно задать `context` (контекст), `first_n` (количество первых взаимодействий), `last_n` (количество последних взаимодействий) и `include_omission_info` (включать ли информацию об упущенных взаимодействиях). 
2. **Запуск истории**:
    - Вызовите метод `start_story()` для начала истории.
    - Задайте `requirements` (требования) для начала истории. 
    - Укажите `number_of_words` (количество слов) в начальной части истории.
    - Дополнительно можно включить `include_plot_twist` (включать ли неожиданный поворот в сюжет).
3. **Продолжение истории**:
    - Вызовите метод `continue_story()` для продолжения истории.
    - Задайте `requirements` (требования) для продолжения истории. 
    - Укажите `number_of_words` (количество слов) в продолжении истории.
    - Дополнительно можно включить `include_plot_twist` (включать ли неожиданный поворот в сюжет).

Пример использования
-------------------------

```python
from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson
from tinytroupe.story import TinyStory

# Создайте окружение 
environment = TinyWorld()
# Создайте агента
agent = TinyPerson()
# Создайте историю об агенте 
story = TinyStory(agent=agent, purpose="Tell a story about a brave adventurer")

# Начинаем историю
start = story.start_story(requirements="Start a story about an agent exploring a mysterious cave.", number_of_words=50)
print(f"Начало истории: {start}")

# Продолжаем историю 
continuation = story.continue_story(requirements="Continue the story with the agent facing a dangerous creature in the cave.", number_of_words=100)
print(f"Продолжение истории: {continuation}")
```