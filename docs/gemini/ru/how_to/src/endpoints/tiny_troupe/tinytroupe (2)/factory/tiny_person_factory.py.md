## Как использовать TinyPersonFactory

=========================================================================================

### Описание
-------------------------
Класс `TinyPersonFactory` - фабрика, которая генерирует экземпляры `TinyPerson` с использованием OpenAI LLM. Фабрика использует контекстную информацию и предоставляет методы для генерации как одного, так и нескольких персонажей с заданными параметрами. 

### Шаги выполнения
-------------------------
1. **Инициализация фабрики**:
    - Создается объект `TinyPersonFactory` с помощью конструтора, передавая контекстную информацию.
    - Конструктор инициализирует путь к шаблону запроса для генерации персонажей и сохраняет контекстную информацию.
2. **Генерация персонажей**:
    -  Используются методы `generate_person` и `generate_people` для генерации одного или нескольких персонажей соответственно.
    -  Методы используют `openai_utils` для отправки запроса к LLM, который сгенерирует описание персонажа на основе заданных параметров и контекста.
    -  Полученные описания обрабатываются, и создаются экземпляры `TinyPerson`.
3. **Контроль уникальности**:
    -  Фабрика отслеживает уже сгенерированные имена персонажей и не позволяет генерировать повторяющиеся имена.
    -  Также отслеживает уже сгенерированные краткие описания персонажей (`minibios`) для более точной генерации.

### Пример использования
-------------------------

```python
from tinytroupe.factory import TinyPersonFactory

# Загружаем текст контекста
context_text = "It was a bright, sunny day in the bustling city of New York. People were rushing to work, some laughing, others with serious expressions."

# Создаем фабрику
factory = TinyPersonFactory(context_text)

# Генерируем одного персонажа с заданными параметрами
person = factory.generate_person(
    agent_particularities="A young woman with a passion for cooking",
    temperature=0.7
)

# Выводим информацию о сгенерированном персонаже
print(person.minibio())
print(person.get("name"))
print(person.get("personality"))

# Генерируем список из 3 персонажей
people = factory.generate_people(number_of_people=3)

# Выводим информацию о сгенерированных персонажах
for person in people:
    print(person.minibio())
    print(person.get("name"))
    print(person.get("personality"))
```