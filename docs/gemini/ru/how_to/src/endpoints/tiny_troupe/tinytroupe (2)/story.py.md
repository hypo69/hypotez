### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предоставляет класс `TinyStory`, предназначенный для создания и развития истории, основанной на симуляции с участием агентов (`TinyPerson`) в определенном окружении (`TinyWorld`). Класс позволяет задавать цели истории, добавлять контекст, а также включать информацию о взаимодействиях агентов в симуляции.

Шаги выполнения
-------------------------
1. **Инициализация `TinyStory`**:
   - Создается экземпляр класса `TinyStory` с указанием либо окружения (`environment`), либо агента (`agent`), вокруг которого будет строиться история.
   - Задается цель (`purpose`) истории, которая будет использоваться для направления генерации текста.
   - Указывается начальный контекст (`context`), к которому будет добавляться новая информация.
   - Определяется количество первых (`first_n`) и последних (`last_n`) взаимодействий, которые будут включены в историю.
   - Указывается, следует ли включать информацию об опущенных взаимодействиях (`include_omission_info`).

2. **Запуск истории (`start_story`)**:
   - Метод `start_story` генерирует начало истории на основе заданных требований (`requirements`), количества слов (`number_of_words`) и необходимости включения сюжетного поворота (`include_plot_twist`).
   - Используются шаблоны (`story.start.system.mustache` и `story.start.user.mustache`) для формирования запроса к языковой модели (LLM) через `openai_utils.client()`.
   - Полученный текст добавляется к текущей истории (`self.current_story`).

3. **Продолжение истории (`continue_story`)**:
   - Метод `continue_story` предлагает продолжение истории, основываясь на текущем контексте и новых требованиях.
   - Аналогично `start_story`, используются шаблоны (`story.continuation.system.mustache` и `story.continuation.user.mustache`) и `openai_utils.client()` для генерации продолжения.
   - Сгенерированный текст добавляется к `self.current_story`.

4. **Получение текущей истории (`_current_story`)**:
   - Метод `_current_story` возвращает текущую историю, включая информацию о взаимодействиях агентов или изменениях в окружении.
   - Используется метод `pretty_current_interactions` агента или окружения для получения отформатированной информации о взаимодействиях.
   - Информация о взаимодействиях добавляется к `self.current_story`.

Пример использования
-------------------------

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.story import TinyStory

# Пример создания агента и окружения (предположим, что они уже определены)
agent = TinyPerson()
environment = TinyWorld()

# Создание экземпляра TinyStory для агента
story = TinyStory(agent=agent, purpose="To explore the agent's social interactions.")

# Запуск истории
start = story.start_story(requirements="The agent wakes up in a new city.", number_of_words=50)
print(f"Начало истории: {start}")

# Продолжение истории
continuation = story.continue_story(requirements="The agent meets a stranger.", number_of_words=50)
print(f"Продолжение истории: {continuation}")

# Получение текущей истории
current_story = story._current_story()
print(f"Текущая история: {current_story}")